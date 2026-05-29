"""Apply TLCTC cluster tags to Sonar issues via the Web API.

This is the only module that mutates SonarQube. Refuses to run without an
explicit opt-in flag set by the CLI; supports `--dry-run` to log planned
POSTs without issuing them.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

from .classifier import ClassifiedFinding
from .sonar_client import SonarApiError, SonarClient, SonarTransportError


@dataclass(frozen=True)
class TagPlan:
    issue_key: str
    existing_tags: tuple[str, ...]
    tlctc_tags: tuple[str, ...]
    merged_tags: tuple[str, ...]


def plan(finding: ClassifiedFinding, existing_tags: tuple[str, ...] = ()) -> TagPlan:
    """Compute the merged tag set (keep non-TLCTC tags, replace tlctc-* tags)."""
    non_tlctc = tuple(t for t in existing_tags if not t.startswith("tlctc-"))
    tlctc_tags = tuple(c.tag for c in finding.tag_clusters)
    merged = tuple(sorted(set(non_tlctc) | set(tlctc_tags)))
    return TagPlan(
        issue_key=finding.issue_key,
        existing_tags=existing_tags,
        tlctc_tags=tlctc_tags,
        merged_tags=merged,
    )


def apply(client: SonarClient, plans: list[TagPlan], dry_run: bool, log) -> int:
    """Apply each plan; return the count of successfully tagged issues."""
    applied = 0
    for tp in plans:
        if not tp.tlctc_tags:
            continue
        if dry_run:
            log(f"[dry-run] set_tags {tp.issue_key} <- {','.join(tp.merged_tags)}")
            continue
        try:
            client.set_tags(tp.issue_key, list(tp.merged_tags))
            applied += 1
            log(f"tagged {tp.issue_key} with {','.join(tp.tlctc_tags)}")
        except (SonarApiError, SonarTransportError) as exc:
            print(f"warning: failed to tag {tp.issue_key}: {exc}", file=sys.stderr)
    return applied
