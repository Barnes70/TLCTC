"""Load and inspect TLCTC Layer 3 attack path documents.

Structural checks only — full JSON Schema validation is done by the repo's
ajv-based `npm run validate-attack-paths`. Every error names the file and the
offending item so a batch run can report precisely.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

STRATEGIC_RE = re.compile(r"^#([1-9]|10)$")
OPERATIONAL_RE = re.compile(r"^TLCTC-(0[1-9]|10)\.[0-9]{2}$")


class Layer3Error(Exception):
    """A Layer 3 document is structurally unusable (exit code 2 in the CLI)."""


def to_strategic(cluster) -> str:
    """'#7' → '#7'; operational 'TLCTC-07.02' → '#7'. Anything else is an error."""
    if isinstance(cluster, str):
        if STRATEGIC_RE.match(cluster):
            return cluster
        m = OPERATIONAL_RE.match(cluster)
        if m:
            return f"#{int(m.group(1))}"
    raise Layer3Error(f"not a TLCTC cluster id: {cluster!r}")


def item_kind(item) -> str:
    """'step' | 'group' | 'unresolved' for a path_sequence item or group member."""
    if not isinstance(item, dict):
        raise Layer3Error(f"sequence item is not an object: {item!r}")
    if item.get("mode") == "parallel" and "steps" in item:
        return "group"
    if item.get("status") == "unresolved":
        if "step_id" not in item:
            raise Layer3Error("unresolved step without step_id")
        return "unresolved"
    if "step_id" in item and "cluster" in item:
        to_strategic(item["cluster"])
        return "step"
    raise Layer3Error(f"unknown sequence item shape (keys: {sorted(item.keys())})")


def check_document(doc, name: str) -> None:
    """Raise Layer3Error naming `name` and the offending item if `doc` is unusable."""
    if not isinstance(doc, dict):
        raise Layer3Error(f"{name}: top level is not an object")
    meta = doc.get("metadata")
    if not isinstance(meta, dict) or not isinstance(meta.get("incident_id"), str) or not meta["incident_id"]:
        raise Layer3Error(f"{name}: metadata.incident_id is missing")
    seq = doc.get("path_sequence")
    if not isinstance(seq, list) or not seq:
        raise Layer3Error(f"{name}: path_sequence is missing or empty")
    for i, item in enumerate(seq):
        try:
            kind = item_kind(item)
        except Layer3Error as e:
            raise Layer3Error(f"{name}: path_sequence[{i}]: {e}") from None
        if kind == "group":
            if not isinstance(item["steps"], list) or len(item["steps"]) < 2:
                raise Layer3Error(f"{name}: path_sequence[{i}]: parallel group needs at least 2 steps")
            for j, member in enumerate(item["steps"]):
                try:
                    if item_kind(member) == "group":
                        raise Layer3Error("nested parallel group")
                except Layer3Error as e:
                    raise Layer3Error(f"{name}: path_sequence[{i}].steps[{j}]: {e}") from None


def load_layer3(path: Path) -> dict:
    path = Path(path)
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise Layer3Error(f"{path}: cannot read JSON — {e}") from None
    check_document(doc, str(path))
    return doc


def flat_steps(sequence) -> list:
    """Every step / unresolved step in order; group members expanded in place."""
    out = []
    for item in sequence:
        if item_kind(item) == "group":
            out.extend(item["steps"])
        else:
            out.append(item)
    return out


def classified_clusters(sequence) -> list:
    """Distinct strategic clusters of classified steps, first-seen order."""
    seen = []
    for step in flat_steps(sequence):
        if item_kind(step) == "step":
            c = to_strategic(step["cluster"])
            if c not in seen:
                seen.append(c)
    return seen


def entry_cluster(sequence):
    """Strategic cluster of the first item, or None when it cannot be stated."""
    first = sequence[0]
    kind = item_kind(first)
    if kind == "step":
        return to_strategic(first["cluster"])
    if kind == "unresolved":
        return None
    clusters = set()
    for member in first["steps"]:
        if item_kind(member) != "step":
            return None
        clusters.add(to_strategic(member["cluster"]))
    return clusters.pop() if len(clusters) == 1 else None
