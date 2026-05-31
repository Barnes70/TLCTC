"""Resolution ladder: Finding → ClassifiedFinding.

CWE-first (verdict-filtered) against tlctc-cwe.json, then CVE→KEV fallback,
else unmapped. '#2 | #3' alternations are resolved by R-ROLE. Every result
carries a provenance record so the cluster assignment is auditable.
"""
import re
from dataclasses import dataclass, field

from cli.context_resolver import resolve_role

_CLUSTER_RE = re.compile(r"#(\d+)")

# Allowed / Allowed-with-Review classify; Discouraged → low-confidence;
# Prohibited / N/A → skipped.
_CLASSIFY_VERDICTS = {"Allowed", "Allowed-with-Review"}


@dataclass
class ClassifiedFinding:
    finding: object
    status: str                      # classified|low_confidence|skipped|unmapped
    primary_cluster: str = None
    cluster_set: list = field(default_factory=list)
    role_reason: str = ""
    provenance: dict = field(default_factory=dict)


def _clusters(expr: str):
    """'#2 | #3' → ['#2','#3']; lowest-numbered first for primary selection."""
    nums = sorted(int(n) for n in _CLUSTER_RE.findall(expr or ""))
    return [f"#{n}" for n in nums]


def _pick_primary(cluster_set, finding, globs):
    if len(cluster_set) <= 1:
        return (cluster_set[0] if cluster_set else None), ""
    # Multiple candidates → try R-ROLE on #2|#3, else lowest-numbered.
    if set(cluster_set) == {"#2", "#3"}:
        cluster, reason = resolve_role(finding.uri, globs)
        if cluster:
            return cluster, reason
        return cluster_set[0], reason  # lowest-numbered fallback
    return cluster_set[0], "multi-cluster: lowest-numbered chosen as primary"


def classify(finding, mapping_loader, source_globs) -> ClassifiedFinding:
    # 1. CWE-first. A usable mapping (classify / low-confidence) wins immediately.
    #    Prohibited or N/A (empty cluster-set) CWEs are not usable on their own,
    #    so we remember the first one and keep scanning the remaining CWEs
    #    instead of terminating — a finding can carry several CWEs.
    skip_prov = None
    for cwe in finding.cwe:
        entry = mapping_loader.cwe(cwe)
        if not entry:
            continue
        verdict = entry.get("mappingVerdict", "Unreviewed")
        cset = _clusters(entry.get("tlctcMapping", ""))
        prov = {"identifier": cwe, "table": "tlctc-cwe", "verdict": verdict}
        if cset and verdict in _CLASSIFY_VERDICTS:
            primary, reason = _pick_primary(cset, finding, source_globs)
            return ClassifiedFinding(finding, "classified", primary, cset, reason, prov)
        if cset and verdict == "Discouraged":
            primary, reason = _pick_primary(cset, finding, source_globs)
            return ClassifiedFinding(finding, "low_confidence", primary, cset, reason, prov)
        # Prohibited verdict or N/A: unusable. Remember the first, keep looking.
        if skip_prov is None:
            skip_prov = prov
    # 2. CVE → KEV fallback (independent evidence; runs even past a Prohibited CWE).
    for cve in finding.cve:
        entry = mapping_loader.kev(cve)
        if entry:
            prov = {"identifier": cve, "table": "tlctc-kev",
                    "confidence": entry.get("confidence")}
            return ClassifiedFinding(
                finding, "classified", entry.get("primaryCluster"),
                entry.get("clusterSet", []), "", prov)
    # 3. A Prohibited / N/A CWE was seen but nothing usable resolved → skipped;
    #    otherwise nothing resolved at all → unmapped.
    if skip_prov is not None:
        return ClassifiedFinding(finding, "skipped", provenance=skip_prov)
    return ClassifiedFinding(finding, "unmapped")
