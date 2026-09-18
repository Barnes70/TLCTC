"""Transitive consistency check: VERIS → ATT&CK (vz-risk/veris mapping) → TLCTC (this repo).

For a record, the *direct* cluster set is what the VERIS → TLCTC mapping yields
(certain clusters plus every alternative of a conditional group). The *transitive* set is
the union of the TLCTC clusters of every ATT&CK technique the record's VERIS values map to.
The two routes were built independently; agreement is evidence that the direct mapping is
sound, disagreement is a list of values to look at.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

from .mapping import DEFAULT_ATTACK_CSV, DEFAULT_ATTACK_TLCTC, Mapping

CLUSTER_RE = re.compile(r"#(\d+)")


def load_veris_attack(path: str | Path | None = None) -> dict[str, set[str]]:
    p = Path(path) if path else DEFAULT_ATTACK_CSV
    edges: dict[str, set[str]] = {}
    with open(p, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            cap = row.get("capability_id", "").strip()
            tech = row.get("attack_object_id", "").strip()
            if cap and tech:
                edges.setdefault(cap, set()).add(tech)
    return edges


def load_attack_tlctc(path: str | Path | None = None) -> dict[str, set[str]]:
    p = Path(path) if path else DEFAULT_ATTACK_TLCTC
    with open(p, encoding="utf-8") as fh:
        doc = json.load(fh)
    out: dict[str, set[str]] = {}
    for m in doc["mappings"]:
        s = m.get("tlctcMapping", "")
        out[m["techniqueId"]] = {f"#{n}" for n in CLUSTER_RE.findall(s)}
    return out


def technique_clusters(technique: str, attack_tlctc: dict[str, set[str]]) -> set[str]:
    """Clusters of a technique; a sub-technique falls back to its parent when unmapped."""
    if technique in attack_tlctc:
        return attack_tlctc[technique]
    parent = technique.split(".")[0]
    return attack_tlctc.get(parent, set())


def transitive_clusters(items: list[str], veris_attack: dict[str, set[str]], attack_tlctc: dict[str, set[str]]) -> tuple[set[str], dict[str, set[str]]]:
    per_item: dict[str, set[str]] = {}
    for vid in items:
        techs = veris_attack.get(vid)
        if not techs:
            continue
        cl: set[str] = set()
        for t in techs:
            cl |= technique_clusters(t, attack_tlctc)
        per_item[vid] = cl
    union: set[str] = set()
    for cl in per_item.values():
        union |= cl
    return union, per_item


def check(result: dict, veris_attack: dict[str, set[str]], attack_tlctc: dict[str, set[str]]) -> dict:
    direct = set(result["clusters_upper"])
    trans, per_item = transitive_clusters(result["items"], veris_attack, attack_tlctc)
    if not per_item or not trans:
        cls = "no-attack-edge"
    elif not direct:
        cls = "disjoint"
    elif direct <= trans:
        cls = "agree"
    elif direct & trans:
        cls = "subset"
    else:
        cls = "disjoint"
    disagreeing = sorted(vid for vid, cl in per_item.items() if cl and direct and not (cl & direct))
    return {
        "class": cls,
        "direct": sorted(direct, key=lambda s: int(s[1:])),
        "transitive": sorted(trans, key=lambda s: int(s[1:])),
        "disagreeing_items": disagreeing,
    }


def summarize_agreement(checks: list[dict], mapping: Mapping) -> dict:
    total = len(checks)
    classes = Counter(c["class"] for c in checks)
    per_value: Counter = Counter()
    for c in checks:
        for vid in c["disagreeing_items"]:
            per_value[vid] += 1
    top = []
    for vid, n in sorted(per_value.items(), key=lambda kv: (-kv[1], kv[0]))[:10]:
        e = mapping.get(vid)
        direct = ", ".join(t["tlctc"] for t in e.get("targets", [])) if e else "?"
        trans_all: set[str] = set()
        for c in checks:
            if vid in c["disagreeing_items"]:
                trans_all |= set(c["transitive"])
        top.append({"veris_id": vid, "n": n, "direct": direct or e.get("mapping_type", "?") if e else "?", "transitive": ", ".join(sorted(trans_all, key=lambda s: int(s[1:])))})
    return {
        "classes": {k: {"n": classes.get(k, 0), "denominator": total} for k in ("agree", "subset", "disjoint", "no-attack-edge")},
        "top_disagreements": top,
    }
