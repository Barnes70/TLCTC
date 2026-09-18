"""Classify one VERIS / VCDB incident record against the VERIS → TLCTC mapping.

The result says what the record can and cannot establish about cause:
clusters that are certain (direct and chain entries), groups of alternatives a rule
would have to decide (conditional entries), companion steps the rules require but the
record does not carry (chains), the cause-side partition rows touched, the Data Risk
Events, the boundary context, and the values that resolve to nothing.
"""
from __future__ import annotations

from .mapping import Mapping, CLUSTER_TYPES

ACTION_FIELDS = ("variety", "vector", "result")
ATTRIBUTE_FIELDS = {
    "confidentiality": ("data_disclosure",),
    "integrity": ("variety",),
    "availability": ("variety",),
}


def _as_list(v) -> list:
    if v is None:
        return []
    if isinstance(v, list):
        return [x for x in v if isinstance(x, str)]
    if isinstance(v, str):
        return [v]
    return []


def veris_ids(record: dict) -> list[str]:
    """Every mapping-relevant VERIS id present in the record, in document order, deduplicated."""
    out: list[str] = []
    seen: set[str] = set()

    def add(i: str) -> None:
        if i not in seen:
            seen.add(i)
            out.append(i)

    action = record.get("action") or {}
    if isinstance(action, dict):
        for cat, block in action.items():
            if not isinstance(block, dict):
                continue
            if cat == "unknown":
                add("action.unknown")
            for field in ACTION_FIELDS:
                for v in _as_list(block.get(field)):
                    add(f"action.{cat}.{field}.{v}")
    attribute = record.get("attribute") or {}
    if isinstance(attribute, dict):
        for cat, fields in ATTRIBUTE_FIELDS.items():
            block = attribute.get(cat)
            if not isinstance(block, dict):
                continue
            for field in fields:
                for v in _as_list(block.get(field)):
                    add(f"attribute.{cat}.{field}.{v}")
    return out


def _cluster_ids(entry: dict) -> list[str]:
    return [t["tlctc"] for t in entry.get("targets", [])]


def classify(record: dict, mapping: Mapping) -> dict:
    items = veris_ids(record)
    certain: list[str] = []
    one_of: list[list[str]] = []
    basis: dict[str, list[str]] = {}
    chain_entries: list[tuple[str, dict]] = []
    partition_rows: set[str] = set()
    off_axis_entries = 0
    dre: set[str] = set()
    dre_potential: set[str] = set()
    boundary_contexts: set[str] = set()
    boundaries: set[str] = set()
    role_hints: set[str] = set()
    intra: set[str] = set()
    unresolved: list[str] = []
    unmapped: list[str] = []

    for vid in items:
        e = mapping.get(vid)
        if e is None:
            unmapped.append(vid)
            continue
        t = e["mapping_type"]
        if t in ("direct", "chain"):
            c = _cluster_ids(e)[0]
            if c not in certain:
                certain.append(c)
            basis.setdefault(c, []).append(vid)
            partition_rows.add("attack")
            if t == "chain":
                chain_entries.append((vid, e))
        elif t == "conditional":
            group = sorted(_cluster_ids(e), key=lambda s: int(s[1:]))
            if group not in one_of:
                one_of.append(group)
            partition_rows.add("attack")
        elif t == "context":
            c = e.get("context", {})
            if c.get("boundary_context"):
                boundary_contexts.add(c["boundary_context"])
            if c.get("boundary"):
                boundaries.add(c["boundary"])
            if c.get("role_hint"):
                role_hints.add(c["role_hint"])
            if c.get("intra_system_boundary"):
                intra.add(c["intra_system_boundary"])
        elif t == "no-cluster":
            partition_rows.add(e["partition_row"])
            off_axis_entries += 1
        elif t == "outcome":
            if e.get("dre"):
                (dre_potential if e.get("certainty") == "potential" else dre).add(e["dre"])
        elif t == "unresolved":
            unresolved.append(vid)

    certain.sort(key=lambda s: int(s[1:]))
    upper = set(certain)
    for g in one_of:
        upper.update(g)

    chains = []
    for vid, e in chain_entries:
        c = _cluster_ids(e)[0]
        side = "before" if e["companion"].get("before") else "after"
        others = sorted((upper - {c}), key=lambda s: int(s[1:]))
        chains.append({
            "cluster": c,
            "item": vid,
            "requires": side,
            "hint": e["companion"].get(side),
            "missing": side if not others else None,
            "recorded_candidates": others,
        })

    has_targets = bool(certain or one_of)
    non_attack_rows = {r for r in partition_rows if r != "attack"}
    return {
        "incident_id": record.get("incident_id"),
        "schema_version": record.get("schema_version"),
        "items": items,
        "clusters": {"certain": certain, "one_of": one_of, "basis": basis},
        "clusters_upper": sorted(upper, key=lambda s: int(s[1:])),
        "chains": chains,
        "partition_rows": sorted(partition_rows),
        "off_axis_only": (not has_targets) and (not unresolved) and off_axis_entries > 0,
        "threat_bearing": has_targets,
        "mixed": has_targets and bool(non_attack_rows),
        "dre": sorted(dre),
        "dre_potential": sorted(dre_potential - dre),
        "context": {
            "boundary_contexts": sorted(boundary_contexts),
            "boundaries": sorted(boundaries),
            "role_hints": sorted(role_hints),
            "intra_system_boundaries": sorted(intra),
        },
        "unresolved": unresolved,
        "unmapped": unmapped,
    }
