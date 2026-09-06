"""Structural check of an emitted MISP event against the two TLCTC object templates.

Not a MISP schema validator: it verifies what the converter promises (spec §7):
known relations and types, values_list membership, required attributes, single
vs multiple, unresolved-step invariants, tags, and resolvable object references.
"""
from __future__ import annotations

from cli.resources import Resources

RELATIONSHIPS = {"includes", "followed-by"}
INFO_MAX = 256


def validate_event(event: dict, res: Resources) -> list:
    errors = []
    ev = event.get("Event") if isinstance(event, dict) else None
    if not isinstance(ev, dict):
        return ['top level must be {"Event": {...}}']
    if len(ev.get("info") or "") > INFO_MAX:
        errors.append(f"info exceeds {INFO_MAX} characters")
    for tag in ev.get("Tag") or []:
        if not str(tag.get("name", "")).startswith("tlctc:"):
            errors.append(f"event tag {tag.get('name')!r} is not a tlctc tag")

    templates = {res.path_template.name: res.path_template, res.step_template.name: res.step_template}
    objects = ev.get("Object") or []
    uuids = [o.get("uuid") for o in objects]
    if len(set(uuids)) != len(uuids):
        errors.append("duplicate object uuids")
    uuid_set = set(uuids)
    n_path = sum(1 for o in objects if o.get("name") == res.path_template.name)
    if n_path != 1:
        errors.append(f"expected exactly one {res.path_template.name} object, found {n_path}")

    for o in objects:
        label = f"object {o.get('name')} {o.get('uuid')}"
        T = templates.get(o.get("name"))
        if not T:
            errors.append(f"{label}: unknown object name")
            continue
        if o.get("template_uuid") != T.uuid:
            errors.append(f"{label}: template_uuid {o.get('template_uuid')} != {T.uuid}")
        if str(o.get("template_version")) != str(T.version):
            errors.append(f"{label}: template_version {o.get('template_version')} != {T.version}")
        seen = {}
        for a in o.get("Attribute") or []:
            rel = a.get("object_relation")
            spec = T.attributes.get(rel)
            if not spec:
                errors.append(f"{label}: unknown object_relation {rel!r}")
                continue
            seen[rel] = seen.get(rel, 0) + 1
            if a.get("type") != spec["misp-attribute"]:
                errors.append(f"{label}: {rel} type {a.get('type')!r} != {spec['misp-attribute']!r}")
            if "values_list" in spec and a.get("value") not in spec["values_list"]:
                errors.append(f"{label}: {rel} value {a.get('value')!r} not in values_list")
            if seen[rel] > 1 and not spec.get("multiple"):
                errors.append(f"{label}: {rel} appears more than once but is not multiple")
            if a.get("type") == "attachment" and not a.get("data"):
                errors.append(f"{label}: attachment {rel} has no data")
            for tag in a.get("Tag") or []:
                if not str(tag.get("name", "")).startswith("tlctc:cluster="):
                    errors.append(f"{label}: attribute tag {tag.get('name')!r} is not a tlctc:cluster tag")
        for req in T.required:
            if req not in seen:
                errors.append(f"{label}: required attribute {req} missing")
        status = [a.get("value") for a in o.get("Attribute") or [] if a.get("object_relation") == "status"]
        if status == ["unresolved"] and ("cluster" in seen or "data-risk-event" in seen):
            errors.append(f"{label}: unresolved step carries cluster or data-risk-event (R-UNRES-2/5)")
        for r in o.get("ObjectReference") or []:
            if r.get("relationship_type") not in RELATIONSHIPS:
                errors.append(f"{label}: relationship_type {r.get('relationship_type')!r} not in {sorted(RELATIONSHIPS)}")
            if r.get("object_uuid") != o.get("uuid"):
                errors.append(f"{label}: reference object_uuid does not point back to its object")
            if r.get("referenced_uuid") not in uuid_set:
                errors.append(f"{label}: referenced_uuid {r.get('referenced_uuid')} does not resolve to an object in the event")
    return errors
