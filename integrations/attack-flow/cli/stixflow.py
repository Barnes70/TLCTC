"""Read an Attack Flow STIX 2.1 bundle into a Flow.

Flow edges: attack-flow.start_refs, attack-action.effect_refs, attack-operator.effect_refs,
attack-condition.on_true_refs / on_false_refs. attack-action.asset_refs and command_ref are attachments.
"""
from __future__ import annotations

import json
from pathlib import Path

from .flow import Action, Condition, Edge, Flow, Operator


def read_stix(path: str | Path) -> Flow:
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    objects = doc.get("objects") if isinstance(doc, dict) else None
    if not isinstance(objects, list):
        raise ValueError(f"{path}: not a STIX bundle (no objects array)")
    by_id = {o["id"]: o for o in objects if isinstance(o, dict) and "id" in o}
    flows = [o for o in objects if o.get("type") == "attack-flow"]
    if len(flows) != 1:
        raise ValueError(f"{path}: expected exactly one attack-flow object, found {len(flows)}")
    f = flows[0]
    flow = Flow(name=f.get("name") or Path(path).stem, scope=f.get("scope"), description=f.get("description"), source=str(path))
    flow.start_ids = list(f.get("start_refs") or [])

    for o in objects:
        t = o.get("type")
        if t == "attack-action":
            flow.actions[o["id"]] = Action(
                id=o["id"], name=o.get("name") or "", technique_id=o.get("technique_id"), tactic_id=o.get("tactic_id"),
                description=o.get("description"), execution_start=o.get("execution_start"), execution_end=o.get("execution_end"),
                confidence=str(o["confidence"]) if "confidence" in o else None,
            )
        elif t == "attack-condition":
            flow.conditions[o["id"]] = Condition(id=o["id"], description=o.get("description") or "")
        elif t == "attack-operator":
            flow.operators[o["id"]] = Operator(id=o["id"], operator=str(o.get("operator") or "AND").upper())

    for o in objects:
        t = o.get("type")
        if t == "attack-action":
            for r in o.get("effect_refs") or []:
                if flow.kind(r):
                    flow.edges.append(Edge(o["id"], r))
            for r in o.get("asset_refs") or []:
                a = by_id.get(r)
                if a:
                    flow.attachments.setdefault(o["id"], []).append(f"{a.get('type')}: {a.get('name') or r}")
            if o.get("command_ref") and o["command_ref"] in by_id:
                c = by_id[o["command_ref"]]
                flow.attachments.setdefault(o["id"], []).append(f"{c.get('type')}: {c.get('command_line') or c.get('name') or o['command_ref']}")
        elif t == "attack-operator":
            for r in o.get("effect_refs") or []:
                if flow.kind(r):
                    flow.edges.append(Edge(o["id"], r))
        elif t == "attack-condition":
            for r in o.get("on_true_refs") or []:
                if flow.kind(r):
                    flow.edges.append(Edge(o["id"], r, "true"))
            for r in o.get("on_false_refs") or []:
                if flow.kind(r):
                    flow.edges.append(Edge(o["id"], r, "false"))
    return flow


def detect_and_read(path: str | Path) -> Flow:
    from .afb import read_afb
    p = Path(path)
    with open(p, encoding="utf-8") as fh:
        head = fh.read(4096)
    if '"schema"' in head and "attack_flow_v2" in head:
        return read_afb(p)
    if '"type": "bundle"' in head or '"objects"' in head:
        return read_stix(p)
    if p.suffix == ".afb":
        return read_afb(p)
    return read_stix(p)
