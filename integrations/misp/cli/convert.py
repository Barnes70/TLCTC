"""Build a MISP event (core format, {"Event": {...}}) from a TLCTC Layer 3 document.

Deterministic: every uuid is version 5 over the event uuid, which is itself
version 5 over CONVERTER_NS and the incident_id. Re-running yields identical JSON.
"""
from __future__ import annotations

import base64
import json
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from cli.layer3 import classified_clusters, entry_cluster, flat_steps, item_kind, to_strategic
from cli.notation import render_path
from cli.resources import Resources

CONVERTER_NS = uuid.uuid5(uuid.NAMESPACE_DNS, "tlctc-misp-converter")  # 04747785-d115-57e4-8557-c3d2be7f9c80
PATH_KEY = ":path"                 # cannot collide with a step_id (pattern ^[A-Za-z]...)
DRE_ORDER = ["C", "I", "Ii", "If", "A", "Av", "Ac"]
INFO_MAX = 256
_URL_RE = re.compile(r"https?://[^\s<>()\[\]\"']+")


@dataclass
class Options:
    distribution: int = 0
    threat_level: int = 4
    analysis: int = 2
    orgc: str | None = None
    attachment: bool = True


def _timestamps(created_at):
    """(YYYY-MM-DD, epoch-seconds-as-string) from metadata.created_at; epoch 0 when absent."""
    if not created_at:
        return "1970-01-01", "0"
    dt = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.date().isoformat(), str(int(dt.timestamp()))


def build_info(incident_id: str, notation: str) -> str:
    s = " ".join(f"TLCTC {incident_id}: {notation}".split())
    return s if len(s) <= INFO_MAX else s[: INFO_MAX - 1] + "…"


def extract_urls(doc: dict) -> list:
    texts = [doc["metadata"].get("notes") or ""]
    for item in doc["path_sequence"]:
        if item_kind(item) == "group":
            texts.append(item.get("notes") or "")
    for step in flat_steps(doc["path_sequence"]):
        texts.extend(step.get("evidence_refs") or [])
        texts.append(step.get("notes") or "")
    urls = []
    for t in texts:
        for u in _URL_RE.findall(t):
            u = u.rstrip(".,;:")
            if u not in urls:
                urls.append(u)
    return urls


class _Builder:
    def __init__(self, doc, source_bytes, options, res):
        self.doc, self.opt, self.res = doc, options, res
        meta = doc["metadata"]
        self.event_uuid = uuid.uuid5(CONVERTER_NS, meta["incident_id"])
        self.date, self.ts = _timestamps(meta.get("created_at"))
        self.source_bytes = source_bytes

    def _u(self, name: str) -> str:
        return str(uuid.uuid5(self.event_uuid, name))

    def _attr(self, template, key, relation, value, index=None, tags=None, data=None):
        spec = template.attributes[relation]
        a_type = spec["misp-attribute"]
        if isinstance(value, bool):
            value = "1" if value else "0"
        name = f"attribute:{key}:{relation}" + (f":{index}" if index is not None else "")
        a = {
            "type": a_type,
            "category": "External analysis" if a_type in ("attachment", "link") else "Other",
            "object_relation": relation,
            "value": str(value),
            "uuid": self._u(name),
            "timestamp": self.ts,
            "to_ids": False,
            "disable_correlation": bool(spec.get("disable_correlation", False)),
            "distribution": "5",
            "comment": "",
        }
        if data is not None:
            a["data"] = data
        if tags:
            a["Tag"] = tags
        return a

    def _object(self, template, key, attributes):
        return {
            "name": template.name,
            "meta-category": template.meta_category,
            "description": template.description,
            "template_uuid": template.uuid,
            "template_version": str(template.version),
            "uuid": self._u(f"object:{key}"),
            "timestamp": self.ts,
            "distribution": "5",
            "sharing_group_id": "0",
            "comment": "",
            "deleted": False,
            "Attribute": attributes,
            "ObjectReference": [],
        }

    def reference(self, from_key, to_key, relationship, comment=""):
        return {
            "uuid": self._u(f"reference:{from_key}:{to_key}:{relationship}"),
            "timestamp": self.ts,
            "object_uuid": self._u(f"object:{from_key}"),
            "referenced_uuid": self._u(f"object:{to_key}"),
            "relationship_type": relationship,
            "comment": comment,
            "deleted": False,
        }

    def path_object(self, notation: str):
        T, meta, seq = self.res.path_template, self.doc["metadata"], self.doc["path_sequence"]
        attrs = []

        def add(relation, value, **kw):
            attrs.append(self._attr(T, PATH_KEY, relation, value, **kw))

        add("notation", notation)
        add("incident-id", meta["incident_id"])
        if meta.get("tlctc_version"):
            add("tlctc-version", meta["tlctc_version"])
        if meta.get("framework_ref"):
            add("framework-ref", meta["framework_ref"])
        ec = entry_cluster(seq)
        if ec:
            add("entry-cluster", ec)
        if meta.get("analyst_confidence"):
            add("analyst-confidence", meta["analyst_confidence"])
        dres = {o for s in flat_steps(seq) if item_kind(s) == "step" for o in (s.get("outcomes") or [])}
        for i, code in enumerate(c for c in DRE_ORDER if c in dres):
            add("data-risk-event", code, index=i)
        for i, url in enumerate(extract_urls(self.doc)):
            add("reference", url, index=i)
        if meta.get("notes"):
            add("notes", meta["notes"])
        if self.opt.attachment:
            add("layer3-json", f"{meta['incident_id']}.json", data=base64.b64encode(self.source_bytes).decode("ascii"))
        return self._object(T, PATH_KEY, attrs)

    def step_object(self, step: dict):
        T, key = self.res.step_template, step["step_id"]
        attrs = []

        def add(relation, value, **kw):
            attrs.append(self._attr(T, key, relation, value, **kw))

        kind = item_kind(step)
        add("step-id", key)
        add("status", "unresolved" if kind == "unresolved" else "classified")
        if kind == "step":
            strategic = to_strategic(step["cluster"])
            add("cluster", strategic, tags=[self.res.taxonomy.tag("cluster", strategic)])
        else:
            add("unresolved-type", step.get("unresolved_type", "single"))
            for i, c in enumerate(step.get("candidates") or []):
                add("candidates", c, index=i)
        if "fec_executed" in step:
            add("fec-executed", bool(step["fec_executed"]))
        if step.get("delta_t_to_next"):
            add("delta-t-to-next", step["delta_t_to_next"])
        b = step.get("topology_boundary")
        if b:
            add("boundary-context", b["context"])
            add("boundary-source", b["source_sphere"])
            add("boundary-target", b["target_sphere"])
            for i, t in enumerate(b.get("transit_spheres") or []):
                add("boundary-transit", t, index=i)
        for i, ib in enumerate(step.get("intra_system_boundaries") or []):
            add("intra-system-boundary", f"{ib['type']}:{ib['from']}→{ib['to']}", index=i)
        if kind == "step":
            for i, o in enumerate(step.get("outcomes") or []):
                add("data-risk-event", o, index=i)
        for i, e in enumerate(step.get("evidence_refs") or []):
            add("evidence", e, index=i)
        if step.get("notes"):
            add("notes", step["notes"])
        return self._object(T, key, attrs)


def convert(doc: dict, options: Options | None = None, resources: Resources | None = None, source_bytes: bytes | None = None) -> dict:
    options = options or Options()
    res = resources or Resources.load()
    if source_bytes is None:
        source_bytes = (json.dumps(doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    b = _Builder(doc, source_bytes, options, res)
    meta, seq = doc["metadata"], doc["path_sequence"]
    notation = render_path(seq)

    path_obj = b.path_object(notation)
    step_objs, by_key = [], {}
    prev_keys, prev_dt = [], None
    for item in seq:
        members = item["steps"] if item_kind(item) == "group" else [item]
        keys = [m["step_id"] for m in members]
        for m in members:
            o = b.step_object(m)
            step_objs.append(o)
            by_key[m["step_id"]] = o
        comment = f"Δt={prev_dt}" if prev_dt else ""
        for p in prev_keys:
            for k in keys:
                by_key[p]["ObjectReference"].append(b.reference(p, k, "followed-by", comment))
        prev_keys, prev_dt = keys, item.get("delta_t_to_next")
    for k in by_key:
        path_obj["ObjectReference"].append(b.reference(PATH_KEY, k, "includes"))

    tags = [res.taxonomy.tag("cluster", c) for c in classified_clusters(seq)]
    ec = entry_cluster(seq)
    if ec:
        tags.append(res.taxonomy.tag("entry-cluster", ec))

    event = {
        "uuid": str(b.event_uuid),
        "info": build_info(meta["incident_id"], notation),
        "date": b.date,
        "timestamp": b.ts,
        "published": False,
        "analysis": str(options.analysis),
        "threat_level_id": str(options.threat_level),
        "distribution": str(options.distribution),
    }
    if options.orgc:
        event["Orgc"] = {"name": options.orgc}
    event["Tag"] = tags
    event["Attribute"] = []
    event["Object"] = [path_obj, *step_objs]
    return {"Event": event}


def dumps(event: dict) -> str:
    return json.dumps(event, ensure_ascii=False, indent=2) + "\n"
