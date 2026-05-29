"""SARIF 2.1.0 report with TLCTC properties bag.

Design choice: one SARIF rule per TLCTC cluster (10 rules total). CWE detail
moves into each `result.properties.tlctc.cwe`. This keeps the rule namespace
small and stable; consumers pivot by cluster, then drill to CWE.
"""

from __future__ import annotations

import json
from typing import Iterable

from ..classifier import ClassifiedFinding, ClusterSummary

SARIF_VERSION = "2.1.0"
SARIF_SCHEMA = "https://json.schemastore.org/sarif-2.1.0.json"

CLUSTER_DESCRIPTIONS = {
    1: ("Abuse of Functions", "A designed feature is used outside its intended boundaries (per TLCTC #1)."),
    2: ("Exploiting Server", "A server-role component has a coding/implementation flaw (per TLCTC #2)."),
    3: ("Exploiting Client", "A client-role component has a coding/implementation flaw (per TLCTC #3)."),
    4: ("Identity Theft", "A credential, key, or session artifact is stolen, forged, or applied (per TLCTC #4)."),
    5: ("Man in the Middle", "A communication path is intercepted, relayed, or altered (per TLCTC #5)."),
    6: ("Flooding Attack", "Resources are exhausted by volume (per TLCTC #6)."),
    7: ("Malware", "Foreign executable content runs in the target system (per TLCTC #7)."),
    8: ("Physical Attack", "A physical/local attack vector compromises the system (per TLCTC #8)."),
    9: ("Social Engineering", "A human is manipulated into taking an attacker-desired action (per TLCTC #9)."),
    10: ("Supply Chain Attack", "A trusted artifact carrying attacker control is accepted (per TLCTC #10)."),
}

SEVERITY_TO_LEVEL = {
    "BLOCKER": "error",
    "CRITICAL": "error",
    "MAJOR": "warning",
    "MINOR": "note",
    "INFO": "note",
}


def render(
    findings: Iterable[ClassifiedFinding],
    summary: dict[int, ClusterSummary],
    tlctc_version: str,
    sonar_project: str | None = None,
) -> str:
    findings_list = list(findings)
    rules = _build_rules(summary)
    rule_index = {rule["id"]: i for i, rule in enumerate(rules)}
    results = [r for f in findings_list if f.resolved for r in _build_results(f, rule_index)]

    sarif = {
        "$schema": SARIF_SCHEMA,
        "version": SARIF_VERSION,
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "tlctc-sonar",
                        "informationUri": "https://www.tlctc.net",
                        "version": "1.0.0",
                        "rules": rules,
                        "properties": {
                            "tlctc_version": tlctc_version,
                            "sonar_project": sonar_project,
                        },
                    }
                },
                "results": results,
                "properties": {
                    "totals": {
                        "issues_seen": len(findings_list),
                        "issues_classified": sum(1 for f in findings_list if f.resolved),
                    },
                },
            }
        ],
    }
    return json.dumps(sarif, indent=2, ensure_ascii=False)


def _build_rules(summary: dict[int, ClusterSummary]) -> list[dict]:
    rules: list[dict] = []
    for number in sorted(summary.keys()):
        name, desc = CLUSTER_DESCRIPTIONS.get(number, (f"Cluster {number}", ""))
        rules.append({
            "id": f"tlctc-{number:02d}",
            "name": name.replace(" ", ""),
            "shortDescription": {"text": f"#{number} {name}"},
            "fullDescription": {"text": desc},
            "defaultConfiguration": {"level": "warning"},
            "properties": {"tlctc": {"cluster": f"#{number}"}},
        })
    return rules


def _build_results(f: ClassifiedFinding, rule_index: dict[str, int]) -> list[dict]:
    out: list[dict] = []
    for resolved in f.resolved:
        clusters = list(resolved.all_clusters)
        if not clusters:
            continue
        primary = resolved.primary_cluster
        primary_id = f"tlctc-{primary.number:02d}" if primary is not None else clusters[0].tag
        if primary_id not in rule_index:
            continue

        related = []
        for c in clusters[1:]:
            related.append({
                "physicalLocation": {
                    "artifactLocation": {"uri": f.component},
                },
                "message": {"text": f"chained cluster #{c.number} ({c.tag})"},
            })

        out.append({
            "ruleId": primary_id,
            "ruleIndex": rule_index[primary_id],
            "level": SEVERITY_TO_LEVEL.get(f.severity, "warning"),
            "message": {"text": f.message or resolved.entry.rationale},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": f.component},
                },
            }],
            "relatedLocations": related,
            "properties": {
                "tlctc": {
                    "primary_cluster": str(primary) if primary else None,
                    "all_clusters": [str(c) for c in clusters],
                    "tags": [c.tag for c in clusters],
                    "cwe": resolved.entry.cwe_id,
                    "verdict": resolved.entry.verdict,
                    "raw_mapping": resolved.entry.tlctc_mapping,
                    "resolved_path": str(resolved.resolution.resolved),
                    "role_resolution": {
                        "role": resolved.resolution.role,
                        "matched_glob": resolved.resolution.matched_glob,
                        "reason": resolved.resolution.reason,
                    },
                },
                "sonar": {
                    "issue_key": f.issue_key,
                    "rule": f.rule,
                    "severity": f.severity,
                    "type": f.type,
                },
            },
        })
    return out
