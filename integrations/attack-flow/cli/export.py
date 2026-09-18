"""Export a TLCTC Layer 3 attack path to an Attack Flow STIX 2.1 bundle carrying the TLCTC extension.

One attack-action per step (classified or unresolved), one attack-operator (AND) per parallel group,
effect_refs following the sequence, the Attack Flow extension-definition and the TLCTC
extension-definition with their identities. Ids are uuid5 over the incident id and the step id, so
re-exporting the same file yields the same bundle.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .stixutil import (AF_EXT_ID, TLCTC_EXT_ID, TLCTC_IDENTITY_ID, af_extension_block,
                       load_attack_flow_extension_objects, load_extension_objects, stix_id)

HERE = Path(__file__).resolve().parent
DICTIONARY = HERE.parent.parent.parent / "json-schemas" / "layer-1" / "tlctc-framework.v2.5.json"
TECHNIQUE_RE = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")


def _cluster_names() -> dict[str, str]:
    with open(DICTIONARY, encoding="utf-8") as fh:
        d = json.load(fh)
    return {cid: c["name"] for cid, c in d["clusters"].items()}


def strategic(cluster: str) -> str:
    """'#7' or 'TLCTC-07.30' or '#7.3' → '#7'."""
    m = re.match(r"^#(10|[1-9])(?:\.\d+)?$", cluster)
    if m:
        return f"#{m.group(1)}"
    m = re.match(r"^TLCTC-(0[1-9]|10)\.", cluster)
    if m:
        return f"#{int(m.group(1))}"
    raise ValueError(f"unrecognised cluster id {cluster!r}")


def sub_cluster(cluster: str) -> str | None:
    m = re.match(r"^TLCTC-(0[1-9]|10)\.(\d\d)$", cluster)
    if m:
        return cluster
    m = re.match(r"^#(10|[1-9])\.(\d)$", cluster)
    if m:
        return f"TLCTC-{int(m.group(1)):02d}.{m.group(2)}0"
    return None


def _timestamp(meta: dict) -> str:
    ts = meta.get("created_at") or "2026-01-01T00:00:00Z"
    if ts.endswith("Z") and "." not in ts:
        ts = ts[:-1] + ".000Z"
    return ts


def _find_technique(step: dict) -> str | None:
    for src in (step.get("evidence_refs") or []) + [step.get("notes") or ""]:
        m = TECHNIQUE_RE.search(str(src))
        if m:
            return m.group(0)
    return None


class Exporter:
    def __init__(self, layer3: dict):
        self.doc = layer3
        self.meta = layer3["metadata"]
        self.incident = self.meta["incident_id"]
        self.ts = _timestamp(self.meta)
        self.names = _cluster_names()
        self.objects: list[dict] = []

    def _base(self, obj_type: str, name: str) -> dict:
        return {
            "type": obj_type, "spec_version": "2.1", "id": stix_id(obj_type, f"{self.incident}/{name}"),
            "created_by_ref": TLCTC_IDENTITY_ID, "created": self.ts, "modified": self.ts,
        }

    def _action_for_step(self, step: dict) -> dict:
        sid = step["step_id"]
        a = self._base("attack-action", f"step/{sid}")
        ext: dict = {"extension_type": "property-extension", "tlctc_step_id": sid}
        if step.get("status") == "unresolved":
            a["name"] = "? unresolved step" if step.get("unresolved_type") == "single" else "… unresolved gap"
            ext["tlctc_status"] = "unresolved"
            ext["tlctc_unresolved_type"] = step.get("unresolved_type", "single")
            if step.get("estimated_count"):
                ext["tlctc_estimated_count"] = step["estimated_count"]
            if step.get("candidates"):
                ext["tlctc_candidates"] = [strategic(c) for c in step["candidates"]]
            ext["tlctc_notes"] = step.get("notes") or "unresolved"
        else:
            cl = strategic(step["cluster"])
            a["name"] = f"{cl} {self.names[cl]}"
            ext["tlctc_status"] = "classified"
            ext["tlctc_cluster"] = cl
            sc = sub_cluster(step["cluster"])
            if sc:
                ext["tlctc_sub_cluster"] = sc
            if step.get("fec_executed") is not None:
                ext["tlctc_fec_executed"] = bool(step["fec_executed"])
            if step.get("fec_recorded_in_step_id"):
                ext["tlctc_fec_recorded_in_step_id"] = step["fec_recorded_in_step_id"]
            if step.get("outcomes"):
                ext["tlctc_dre"] = list(dict.fromkeys(step["outcomes"]))
            if step.get("notes"):
                ext["tlctc_notes"] = step["notes"]
        if step.get("delta_t_to_next"):
            ext["tlctc_delta_t_to_next"] = str(step["delta_t_to_next"])
        if step.get("topology_boundary"):
            b = step["topology_boundary"]
            ext["tlctc_boundary"] = {k: b[k] for k in ("context", "source_sphere", "target_sphere") if k in b}
            if b.get("transit_spheres"):
                ext["tlctc_boundary"]["transit_spheres"] = list(b["transit_spheres"])
        if step.get("intra_system_boundaries"):
            ext["tlctc_intra_system_boundaries"] = [{"type": x["type"], "from": x["from"], "to": x["to"]} for x in step["intra_system_boundaries"]]
        if step.get("evidence_refs"):
            ext["tlctc_evidence_refs"] = list(step["evidence_refs"])
        tid = _find_technique(step)
        if tid:
            a["technique_id"] = tid
        if step.get("notes"):
            a["description"] = step["notes"]
        a["extensions"] = {**af_extension_block(), TLCTC_EXT_ID: ext}
        return a

    def export(self) -> dict:
        seq = self.doc["path_sequence"]
        heads: list[list[str]] = []   # per item: ids that enter the item
        tails: list[list[str]] = []   # per item: ids that leave the item
        items: list[dict] = []
        for item in seq:
            if "steps" in item:  # parallel group: the previous item fans out to every member, the members join in an AND operator, the operator leads on
                gid = item.get("group_id") or f"group-{len(items) + 1}"
                op = self._base("attack-operator", f"group/{gid}")
                op["operator"] = "AND"
                ext = {"extension_type": "property-extension", "tlctc_group_id": gid, "tlctc_mode": item.get("mode", "parallel")}
                if item.get("delta_t_to_next"):
                    ext["tlctc_delta_t_to_next"] = str(item["delta_t_to_next"])
                if item.get("notes"):
                    ext["tlctc_notes"] = item["notes"]
                op["extensions"] = {**af_extension_block(), TLCTC_EXT_ID: ext}
                members = [self._action_for_step(s) for s in item["steps"]]
                for m in members:
                    m["effect_refs"] = [op["id"]]
                items.extend(members)
                items.append(op)
                heads.append([m["id"] for m in members])
                tails.append([op["id"]])
            else:
                a = self._action_for_step(item)
                items.append(a)
                heads.append([a["id"]])
                tails.append([a["id"]])
        by_id = {o["id"]: o for o in items}
        for i in range(len(heads) - 1):
            for t in tails[i]:
                by_id[t].setdefault("effect_refs", []).extend(heads[i + 1])
        for o in items:
            if "effect_refs" in o:
                o["effect_refs"] = list(dict.fromkeys(o["effect_refs"]))
        flow = self._base("attack-flow", "flow")
        flow["name"] = self.incident
        flow["scope"] = "incident"
        if self.meta.get("notes"):
            flow["description"] = self.meta["notes"]
        flow["start_refs"] = heads[0] if heads else []
        flow_ext = {"extension_type": "property-extension", "tlctc_version": str(self.meta.get("tlctc_version", "2.5")), "tlctc_incident_id": self.incident, "tlctc_source": "layer3-export"}
        if self.meta.get("framework_ref"):
            flow_ext["tlctc_framework_ref"] = self.meta["framework_ref"]
        if self.meta.get("framework_sha256"):
            flow_ext["tlctc_framework_sha256"] = self.meta["framework_sha256"]
        if self.meta.get("analyst_confidence"):
            flow_ext["tlctc_analyst_confidence"] = self.meta["analyst_confidence"]
        notation = _notation_from_notes(self.meta.get("notes"))
        if notation:
            flow_ext["tlctc_notation"] = notation
        flow["extensions"] = {**af_extension_block(), TLCTC_EXT_ID: flow_ext}
        objects = [*load_attack_flow_extension_objects(), *load_extension_objects(), flow, *items]
        return {"type": "bundle", "id": stix_id("bundle", f"{self.incident}/bundle"), "objects": objects}


def _notation_from_notes(notes: str | None) -> str | None:
    if not notes:
        return None
    m = re.search(r"(#(?:10|[1-9])[^\n]*)", notes)
    return m.group(1).strip().rstrip(".") if m else None


def export_layer3(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    if not isinstance(doc, dict) or "metadata" not in doc or "path_sequence" not in doc:
        raise ValueError(f"{path}: not a TLCTC Layer 3 attack path")
    return Exporter(doc).export()
