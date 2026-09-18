"""Read an Attack Flow Builder `.afb` (schema attack_flow_v2) file into a Flow.

File shape: {"schema": "attack_flow_v2", "objects": [...], "layout": {...}, "camera": {...}}.
Every object has an `id` (its template name: flow, action, condition, AND_operator, OR_operator,
asset, tool, malware, note, ..., horizontal_anchor, vertical_anchor, generic_latch, generic_handle,
dynamic_line) and an `instance` uuid. Blocks carry `properties` as a list of [key, value] pairs and
`anchors` as {position: anchor instance}; anchors carry `latches`; a `dynamic_line` joins a `source`
latch to a `target` latch. The owner of a latch is the block whose anchor lists it. Condition
blocks expose their outgoing branches on anchors keyed "branch:True" / "branch:False".
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .flow import Action, Condition, Edge, Flow, Operator

ATTACHMENT_KINDS = {
    "asset", "tool", "malware", "note", "file", "infrastructure", "ipv4_addr", "ipv6_addr", "url",
    "process", "threat_actor", "directory", "vulnerability", "user_account", "mitigation",
    "windows_registry_key", "detection", "network_traffic", "campaign", "domain_name", "location",
    "software", "artifact", "course_of_action", "identity", "email_address", "email_addr", "mac_addr",
    "mutex", "x509_certificate", "autonomous_system", "observed_data", "indicator", "attack_pattern",
    "grouping", "intrusion_set", "report", "opinion", "email_message", "location",
}


LABEL_RE = re.compile(r"^\[[A-Z0-9]+\]\s+(\S+)")


def _bare_id(value):
    """Builder 4.0 stores the option label ('[ENT] T1078 Valid Accounts', '[ATL] AML.T0051 …'); keep the id only."""
    if not isinstance(value, str):
        return value
    m = LABEL_RE.match(value)
    return m.group(1) if m else value


def props(obj: dict) -> dict:
    """Properties as a dict; nested list-valued properties are kept as-is."""
    out = {}
    for item in obj.get("properties") or []:
        if isinstance(item, list) and len(item) == 2:
            out[item[0]] = item[1]
    return out


def read_afb(path: str | Path) -> Flow:
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    if doc.get("schema") != "attack_flow_v2":
        raise ValueError(f"{path}: unsupported .afb schema {doc.get('schema')!r} (expected attack_flow_v2)")
    objects = doc.get("objects") or []
    by_instance = {o["instance"]: o for o in objects if "instance" in o}

    flow_obj = next((o for o in objects if o.get("id") == "flow"), None)
    fp = props(flow_obj) if flow_obj else {}
    flow = Flow(name=str(fp.get("name") or Path(path).stem), scope=fp.get("scope"), description=fp.get("description"), source=str(path))

    # anchor instance → (owner block, anchor key)
    anchor_owner: dict[str, tuple[dict, str]] = {}
    for o in objects:
        for key, anc in (o.get("anchors") or {}).items():
            anchor_owner[anc] = (o, key)
    # latch instance → (owner block, anchor key)
    latch_owner: dict[str, tuple[dict, str]] = {}
    for o in objects:
        if o.get("id", "").endswith("_anchor"):
            owner = anchor_owner.get(o["instance"])
            if owner:
                for latch in o.get("latches") or []:
                    latch_owner[latch] = owner

    for o in objects:
        kind = o.get("id")
        p = props(o)
        if kind == "action":
            ttp = p.get("ttp")
            tactic = p.get("tactic_id")
            technique = p.get("technique_id")
            if isinstance(ttp, list):  # [["tactic", ...], ["technique", ...]]
                d = {k: v for k, v in ttp if isinstance(k, str)}
                tactic = tactic or d.get("tactic")
                technique = technique or d.get("technique")
            tactic, technique = _bare_id(tactic), _bare_id(technique)
            flow.actions[o["instance"]] = Action(
                id=o["instance"], name=str(p.get("name") or ""), technique_id=technique or None, tactic_id=tactic or None,
                description=p.get("description"), execution_start=p.get("execution_start"), execution_end=p.get("execution_end"),
                confidence=p.get("confidence") if isinstance(p.get("confidence"), str) else None,
            )
        elif kind == "condition":
            flow.conditions[o["instance"]] = Condition(id=o["instance"], description=str(p.get("description") or ""))
        elif kind in ("AND_operator", "OR_operator"):
            flow.operators[o["instance"]] = Operator(id=o["instance"], operator=kind.split("_")[0])

    for o in objects:
        if o.get("id") != "dynamic_line":
            continue
        s = latch_owner.get(o.get("source"))
        t = latch_owner.get(o.get("target"))
        if not s or not t:
            continue
        (so, skey), (to, tkey) = s, t
        sk, tk = flow.kind(so["instance"]), flow.kind(to["instance"])
        if sk and tk:
            label = None
            if sk == "condition" and isinstance(skey, str) and skey.startswith("branch:"):
                label = skey.split(":", 1)[1].lower()
            flow.edges.append(Edge(src=so["instance"], dst=to["instance"], label=label))
        elif sk == "action" and not tk:
            name = props(to).get("name") or to.get("id")
            flow.attachments.setdefault(so["instance"], []).append(f"{to.get('id')}: {name}")
        elif tk == "action" and not sk:
            name = props(so).get("name") or so.get("id")
            flow.attachments.setdefault(to["instance"], []).append(f"{so.get('id')}: {name}")
    return flow
