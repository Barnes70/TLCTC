"""R-ROLE context-aware resolution for ambiguous CWE -> TLCTC mappings.

When a mapping has an Alternation (#2 | #3 or #2 -> #7 | #3 -> #7), pick the
branch whose role matches the file path of the Sonar issue's `component`.

Algorithm:
  1. Non-Alternation nodes pass through unchanged.
  2. For each branch, infer role: any #2 -> "server"; any #3 -> "client".
  3. Match component path against client globs first (more specific), then
     server globs. First match wins.
  4. No match -> `default_role`.
  5. Return the branch whose role matches; record the decision for reporting.
"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from typing import Iterable

from .path_parser import Alternation, Cluster, PathNode, Sequence


ROLE_SERVER = "server"
ROLE_CLIENT = "client"


@dataclass(frozen=True)
class RoleConfig:
    server_globs: tuple[str, ...]
    client_globs: tuple[str, ...]
    default_role: str = ROLE_SERVER

    def __post_init__(self) -> None:
        if self.default_role not in (ROLE_SERVER, ROLE_CLIENT):
            raise ValueError(
                f"default_role must be '{ROLE_SERVER}' or '{ROLE_CLIENT}', "
                f"got {self.default_role!r}"
            )


@dataclass(frozen=True)
class Resolution:
    resolved: PathNode
    role: str | None         # which role's globs matched, None if pass-through
    matched_glob: str | None # the specific glob pattern that matched
    reason: str              # human-readable explanation for reports


def resolve(component_path: str, ast: PathNode, config: RoleConfig) -> Resolution:
    """Resolve an Alternation against the component path. Non-Alternations pass through."""
    if not isinstance(ast, Alternation):
        return Resolution(resolved=ast, role=None, matched_glob=None, reason="no alternation; no role resolution required")

    server_branch = _find_branch_for_role(ast.branches, ROLE_SERVER)
    client_branch = _find_branch_for_role(ast.branches, ROLE_CLIENT)

    matched_glob, matched_role = _match_role(component_path, config)
    if matched_role == ROLE_CLIENT and client_branch is not None:
        return Resolution(
            resolved=client_branch,
            role=ROLE_CLIENT,
            matched_glob=matched_glob,
            reason=f"component path matched client glob '{matched_glob}'",
        )
    if matched_role == ROLE_SERVER and server_branch is not None:
        return Resolution(
            resolved=server_branch,
            role=ROLE_SERVER,
            matched_glob=matched_glob,
            reason=f"component path matched server glob '{matched_glob}'",
        )

    # No glob match — fall back to default role.
    if config.default_role == ROLE_CLIENT and client_branch is not None:
        return Resolution(
            resolved=client_branch,
            role=ROLE_CLIENT,
            matched_glob=None,
            reason="no glob match; fell back to default_role=client",
        )
    if server_branch is not None:
        return Resolution(
            resolved=server_branch,
            role=ROLE_SERVER,
            matched_glob=None,
            reason="no glob match; fell back to default_role=server",
        )

    # Neither role-shaped branch exists (e.g. #1 | #4). Pick the first branch and explain.
    first = ast.branches[0]
    return Resolution(
        resolved=first,
        role=None,
        matched_glob=None,
        reason="alternation does not contain #2/#3 branches; took first branch by convention",
    )


def _find_branch_for_role(branches: tuple, role: str) -> PathNode | None:
    target = 2 if role == ROLE_SERVER else 3
    for branch in branches:
        if _branch_contains_cluster(branch, target):
            return branch
    return None


def _branch_contains_cluster(branch: PathNode, number: int) -> bool:
    if isinstance(branch, Cluster):
        return branch.number == number
    if isinstance(branch, Sequence):
        return any(step.number == number for step in branch.steps)
    return False


def _match_role(component_path: str, config: RoleConfig) -> tuple[str | None, str | None]:
    """Return (matched_glob, role) — client checked first because it's typically more specific."""
    path = _strip_sonar_prefix(component_path)
    glob = _first_match(path, config.client_globs)
    if glob is not None:
        return glob, ROLE_CLIENT
    glob = _first_match(path, config.server_globs)
    if glob is not None:
        return glob, ROLE_SERVER
    return None, None


def _strip_sonar_prefix(component_path: str) -> str:
    """Sonar issue.component is formatted as 'projectKey:relative/path/file'.

    The colon never appears in the path portion (POSIX), so splitting on the
    first ':' is safe. If there is no colon, the path is returned as-is.
    """
    if ":" not in component_path:
        return component_path
    return component_path.split(":", 1)[1]


def _first_match(path: str, globs: Iterable[str]) -> str | None:
    # `fnmatch` doesn't honor `**` as recursive across slashes the way pathspec does.
    # For our heuristic globs ('**/server/**', '**/*.tsx', etc.) we translate '**' to '*'
    # since fnmatchcase already treats '*' as "any chars including '/'".
    for pattern in globs:
        normalized = pattern.replace("**", "*")
        if fnmatch.fnmatchcase(path, normalized):
            return pattern
    return None
