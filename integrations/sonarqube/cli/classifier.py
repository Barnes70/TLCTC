"""Classify a SonarQube issue into a TLCTC ClassifiedFinding.

Pipeline:
  1. Extract CWE references from the issue (tags + securityStandards).
  2. Look up each CWE in the MappingIndex.
  3. Filter by verdict (per `include_verdicts`).
  4. Resolve any Alternation against the component path (R-ROLE).
  5. Return a ClassifiedFinding with full provenance (primary cluster, all
     clusters, resolved path, role resolution, verdict status).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, Sequence as TypingSequence

from . import path_parser
from .context_resolver import RoleConfig, Resolution, resolve
from .mapping_loader import (
    VERDICT_ALLOWED,
    VERDICT_DISCOURAGED,
    VERDICT_PROHIBITED,
    VERDICT_REVIEW,
    MappingEntry,
    MappingIndex,
)
from .path_parser import Cluster, PathNode

CWE_TAG_RE = re.compile(r"cwe[:-]?(\d+)", re.IGNORECASE)


@dataclass(frozen=True)
class ResolvedMapping:
    """A single CWE's classification outcome for this issue."""

    entry: MappingEntry
    resolution: Resolution
    primary_cluster: Cluster | None
    all_clusters: tuple[Cluster, ...]


@dataclass(frozen=True)
class ClassifiedFinding:
    issue_key: str
    component: str
    severity: str
    type: str
    rule: str
    message: str
    cwe_refs: tuple[str, ...]                # ["CWE-79", ...] discovered on the issue
    resolved: tuple[ResolvedMapping, ...]    # entries that passed verdict filter
    low_confidence: tuple[ResolvedMapping, ...] = field(default_factory=tuple)
    unmapped_cwes: tuple[str, ...] = field(default_factory=tuple)
    skipped_prohibited: tuple[str, ...] = field(default_factory=tuple)

    @property
    def primary_clusters(self) -> tuple[Cluster, ...]:
        return tuple(r.primary_cluster for r in self.resolved if r.primary_cluster is not None)

    @property
    def tag_clusters(self) -> tuple[Cluster, ...]:
        seen: dict[int, Cluster] = {}
        for r in self.resolved:
            for c in r.all_clusters:
                seen.setdefault(c.number, c)
        return tuple(seen.values())


def extract_cwe_refs(issue: dict) -> list[str]:
    """Pull every CWE-N reference from an issue's tags + securityStandards."""
    refs: dict[str, None] = {}
    for tag in issue.get("tags", []) or []:
        m = CWE_TAG_RE.fullmatch(str(tag).strip())
        if m:
            refs[f"CWE-{int(m.group(1))}"] = None
    for std in issue.get("securityStandards", []) or []:
        m = CWE_TAG_RE.fullmatch(str(std).strip())
        if m:
            refs[f"CWE-{int(m.group(1))}"] = None
    return list(refs.keys())


def classify(
    issue: dict,
    index: MappingIndex,
    role_config: RoleConfig,
    include_verdicts: TypingSequence[str] = (VERDICT_ALLOWED, VERDICT_REVIEW),
) -> ClassifiedFinding:
    """Turn one Sonar issue dict into a ClassifiedFinding."""
    cwe_refs = extract_cwe_refs(issue)
    component = str(issue.get("component", ""))

    resolved: list[ResolvedMapping] = []
    low_confidence: list[ResolvedMapping] = []
    unmapped: list[str] = []
    skipped: list[str] = []

    include = set(include_verdicts)

    for cwe in cwe_refs:
        entry = index.get(cwe)
        if entry is None:
            unmapped.append(cwe)
            continue
        if entry.verdict == VERDICT_PROHIBITED:
            skipped.append(cwe)
            continue

        is_na = entry.path is None or isinstance(entry.path, path_parser.Unmapped)

        # Discouraged always lands in low_confidence — the verdict itself
        # explains why (the CWE is too generic for a single cluster). This
        # supersedes the "unmapped" routing for N/A paths.
        if entry.verdict == VERDICT_DISCOURAGED:
            mapping = _make_resolved(entry, component, role_config) if not is_na else _make_unmapped(entry)
            low_confidence.append(mapping)
            continue

        if is_na:
            unmapped.append(cwe)
            continue

        mapping = _make_resolved(entry, component, role_config)
        if entry.verdict not in include:
            # Allowed-with-Review when caller restricted to Allowed only, etc.
            low_confidence.append(mapping)
            continue
        resolved.append(mapping)

    return ClassifiedFinding(
        issue_key=str(issue.get("key", "")),
        component=component,
        severity=str(issue.get("severity", "")),
        type=str(issue.get("type", "")),
        rule=str(issue.get("rule", "")),
        message=str(issue.get("message", "")),
        cwe_refs=tuple(cwe_refs),
        resolved=tuple(resolved),
        low_confidence=tuple(low_confidence),
        unmapped_cwes=tuple(unmapped),
        skipped_prohibited=tuple(skipped),
    )


def _make_resolved(entry: MappingEntry, component: str, role_config: RoleConfig) -> ResolvedMapping:
    resolution = resolve(component, entry.path, role_config)
    primary = path_parser.primary_cluster(resolution.resolved)
    all_clusters = tuple(path_parser.all_clusters(resolution.resolved))
    return ResolvedMapping(
        entry=entry,
        resolution=resolution,
        primary_cluster=primary,
        all_clusters=all_clusters,
    )


def _make_unmapped(entry: MappingEntry) -> ResolvedMapping:
    """For Discouraged + N/A: keep the entry visible in low_confidence without a cluster."""
    from .context_resolver import Resolution
    return ResolvedMapping(
        entry=entry,
        resolution=Resolution(resolved=entry.path, role=None, matched_glob=None,
                              reason="CWE is Discouraged and maps to N/A (too generic for a single cluster)"),
        primary_cluster=None,
        all_clusters=(),
    )


@dataclass(frozen=True)
class ClusterSummary:
    cluster: Cluster
    count: int
    issue_keys: tuple[str, ...]


def summarize(findings: Iterable[ClassifiedFinding]) -> dict[int, ClusterSummary]:
    """Group findings by primary cluster (Axiom VI: first step of resolved path)."""
    buckets: dict[int, list[str]] = {}
    cluster_objs: dict[int, Cluster] = {}
    for f in findings:
        for r in f.resolved:
            if r.primary_cluster is None:
                continue
            n = r.primary_cluster.number
            buckets.setdefault(n, []).append(f.issue_key)
            cluster_objs.setdefault(n, r.primary_cluster)
    return {
        n: ClusterSummary(cluster=cluster_objs[n], count=len(keys), issue_keys=tuple(keys))
        for n, keys in sorted(buckets.items())
    }
