"""Emit a standalone TLCTC SARIF 2.1.0 report.

This is a fresh SARIF document (driver = ``tlctc-sarif``), NOT an in-place
rewrite of the producer's original file: it carries only the findings TLCTC
classified, each tagged with ``properties.tlctc``. The source location is
preserved — ``artifactLocation.uri`` plus the original ``region`` when present
— so line/column anchors survive for code-scanning UIs, and the originating
tool is recorded under ``properties.tlctc.source_tool``.
"""
import json

_CLUSTERS = {
    "#1": "Abuse of Functions", "#2": "Exploiting Server", "#3": "Exploiting Client",
    "#4": "Identity Theft", "#5": "Man in the Middle", "#6": "Flooding Attack",
    "#7": "Malware", "#8": "Physical Attack", "#9": "Social Engineering",
    "#10": "Supply Chain Attack",
}


def _taxonomy():
    return {
        "name": "TLCTC", "version": "2.1",
        "informationUri": "https://www.tlctc.net/",
        "taxa": [{"id": cid, "name": name} for cid, name in _CLUSTERS.items()],
    }


def render(classified) -> str:
    results = []
    for r in classified:
        if r.status not in ("classified", "low_confidence"):
            continue
        f = r.finding
        phys = {"artifactLocation": {"uri": f.uri}}
        if f.region:
            phys["region"] = f.region
        results.append({
            "ruleId": f.rule_id,
            "message": {"text": f.message},
            "locations": [{"physicalLocation": phys}],
            "properties": {"tlctc": {
                "cluster": r.primary_cluster, "cluster_set": r.cluster_set,
                "status": r.status, "role_resolution": {"reason": r.role_reason},
                "source": r.provenance, "source_tool": f.tool,
            }},
        })
    doc = {"version": "2.1.0",
           "$schema": "https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-schema-2.1.0.json",
           "runs": [{"tool": {"driver": {"name": "tlctc-sarif", "version": "1.0.0"}},
                     "taxonomies": [_taxonomy()], "results": results}]}
    return json.dumps(doc, indent=2)
