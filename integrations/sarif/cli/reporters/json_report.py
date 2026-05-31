import json

from cli.reporters import cluster_summary


def _finding_dict(r):
    f = r.finding
    return {
        "rule_id": f.rule_id, "tool": f.tool, "uri": f.uri, "message": f.message,
        "cwe": f.cwe, "cve": f.cve,
        "primary_cluster": r.primary_cluster, "cluster_set": r.cluster_set,
        "role_reason": r.role_reason, "provenance": r.provenance,
    }


def render(classified) -> str:
    out = {
        "cluster_summary": cluster_summary(classified),
        "findings": [_finding_dict(r) for r in classified if r.status == "classified"],
        "low_confidence": [_finding_dict(r) for r in classified if r.status == "low_confidence"],
        "unmapped": [_finding_dict(r) for r in classified if r.status in ("unmapped", "skipped")],
    }
    return json.dumps(out, indent=2)
