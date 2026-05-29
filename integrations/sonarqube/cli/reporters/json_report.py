"""JSON cluster summary + per-issue array.

Schema (top-level keys):
  - generated_at       — ISO timestamp
  - tlctc_version      — from the mapping envelope
  - sonar_project      — caller-supplied
  - cluster_summary    — { "#N": {count, issue_keys[]} }
  - findings           — array, one entry per ClassifiedFinding with primary_clusters
  - low_confidence     — findings whose CWE verdict was Discouraged or filtered
  - unmapped           — findings whose CWE had no mapping
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Iterable

from ..classifier import ClassifiedFinding, ClusterSummary


def render(
    findings: Iterable[ClassifiedFinding],
    summary: dict[int, ClusterSummary],
    tlctc_version: str,
    sonar_project: str | None = None,
) -> str:
    findings_list = list(findings)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tlctc_version": tlctc_version,
        "sonar_project": sonar_project,
        "totals": {
            "issues_seen": len(findings_list),
            "issues_classified": sum(1 for f in findings_list if f.resolved),
            "issues_low_confidence": sum(1 for f in findings_list if f.low_confidence and not f.resolved),
            "issues_unmapped": sum(1 for f in findings_list if not f.resolved and not f.low_confidence and f.cwe_refs),
            "issues_no_cwe": sum(1 for f in findings_list if not f.cwe_refs),
        },
        "cluster_summary": {
            f"#{cs.cluster.number}": {
                "count": cs.count,
                "tag": cs.cluster.tag,
                "issue_keys": list(cs.issue_keys),
            }
            for cs in summary.values()
        },
        "findings": [_finding_to_dict(f) for f in findings_list if f.resolved],
        "low_confidence": [_finding_to_dict(f) for f in findings_list if f.low_confidence and not f.resolved],
        "unmapped": [
            {
                "issue_key": f.issue_key,
                "component": f.component,
                "cwe_refs": list(f.cwe_refs),
                "reason": "no mapping entry" if not f.cwe_refs else "CWE present but no defensible cluster",
            }
            for f in findings_list
            if not f.resolved and not f.low_confidence and f.cwe_refs
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _finding_to_dict(f: ClassifiedFinding) -> dict:
    return {
        "issue_key": f.issue_key,
        "component": f.component,
        "severity": f.severity,
        "type": f.type,
        "rule": f.rule,
        "message": f.message,
        "cwe_refs": list(f.cwe_refs),
        "primary_clusters": [str(c) for c in f.primary_clusters],
        "tlctc_tags": [c.tag for c in f.tag_clusters],
        "resolutions": [
            {
                "cwe_id": r.entry.cwe_id,
                "verdict": r.entry.verdict,
                "raw_mapping": r.entry.tlctc_mapping,
                "resolved_path": str(r.resolution.resolved),
                "role": r.resolution.role,
                "matched_glob": r.resolution.matched_glob,
                "reason": r.resolution.reason,
                "rationale": r.entry.rationale,
            }
            for r in (f.resolved or f.low_confidence)
        ],
    }
