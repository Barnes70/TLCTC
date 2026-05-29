"""Parse TLCTC path notation ("#2 -> #7 | #3") into a typed AST.

Accepts the Unicode arrow ("→") and ASCII fallback ("->"). Alternation
uses "|". The literal string "N/A" yields the Unmapped sentinel. Cluster IDs
are #1 through #10 — anything else raises PathParseError.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union

ARROW_UNICODE = "→"
ARROW_ASCII = "->"
UNMAPPED_LITERAL = "N/A"


class PathParseError(ValueError):
    """Raised when a tlctcMapping string cannot be parsed."""


@dataclass(frozen=True)
class Cluster:
    """A single TLCTC cluster reference, e.g. #2."""

    number: int  # 1..10

    def __str__(self) -> str:
        return f"#{self.number}"

    @property
    def tag(self) -> str:
        """SonarQube-tag-safe form, e.g. 'tlctc-02'."""
        return f"tlctc-{self.number:02d}"


@dataclass(frozen=True)
class Sequence:
    """An ordered chain of clusters, e.g. #2 -> #7."""

    steps: tuple[Cluster, ...]

    def __str__(self) -> str:
        return f" {ARROW_UNICODE} ".join(str(s) for s in self.steps)


@dataclass(frozen=True)
class Alternation:
    """Mutually exclusive branches, e.g. #2 | #3 or #2 -> #7 | #3 -> #7."""

    branches: tuple[Union["Sequence", Cluster], ...]

    def __str__(self) -> str:
        return " | ".join(str(b) for b in self.branches)


@dataclass(frozen=True)
class Unmapped:
    """Sentinel for tlctcMapping == 'N/A'."""

    def __str__(self) -> str:
        return UNMAPPED_LITERAL


PathNode = Union[Cluster, Sequence, Alternation, Unmapped]


def parse(mapping: str) -> PathNode:
    """Parse a tlctcMapping string into a PathNode AST.

    Raises PathParseError on malformed input.
    """
    if mapping is None:
        raise PathParseError("mapping is None")
    text = mapping.strip()
    if not text:
        raise PathParseError("mapping is empty")
    if text == UNMAPPED_LITERAL:
        return Unmapped()

    normalized = text.replace(ARROW_ASCII, ARROW_UNICODE)
    branches = [b.strip() for b in normalized.split("|")]
    parsed_branches: list[Cluster | Sequence] = []
    for branch in branches:
        if not branch:
            raise PathParseError(f"empty alternation branch in '{mapping}'")
        parsed_branches.append(_parse_sequence(branch, mapping))

    if len(parsed_branches) == 1:
        return parsed_branches[0]
    return Alternation(tuple(parsed_branches))


def _parse_sequence(text: str, original: str) -> Cluster | Sequence:
    steps_text = [t.strip() for t in text.split(ARROW_UNICODE)]
    if any(not s for s in steps_text):
        raise PathParseError(f"empty sequence step in '{original}'")
    clusters = tuple(_parse_cluster(s, original) for s in steps_text)
    if len(clusters) == 1:
        return clusters[0]
    return Sequence(clusters)


def _parse_cluster(token: str, original: str) -> Cluster:
    if not token.startswith("#"):
        raise PathParseError(f"cluster token '{token}' missing '#' in '{original}'")
    digits = token[1:]
    if not digits.isdigit():
        raise PathParseError(f"cluster token '{token}' has non-digit body in '{original}'")
    number = int(digits)
    if not 1 <= number <= 10:
        raise PathParseError(f"cluster number {number} out of range 1..10 in '{original}'")
    return Cluster(number)


def all_clusters(node: PathNode) -> list[Cluster]:
    """Return every Cluster reachable from the node (deduped, order-preserving)."""
    seen: dict[int, Cluster] = {}

    def visit(n: PathNode) -> None:
        if isinstance(n, Cluster):
            seen.setdefault(n.number, n)
        elif isinstance(n, Sequence):
            for step in n.steps:
                seen.setdefault(step.number, step)
        elif isinstance(n, Alternation):
            for branch in n.branches:
                visit(branch)
        # Unmapped contributes nothing.

    visit(node)
    return list(seen.values())


def primary_cluster(node: PathNode) -> Cluster | None:
    """Return the first cluster of the first branch (Axiom VI primary).

    For an Alternation, this is informational only — context_resolver should
    pick the branch first, then call primary_cluster on the result.
    """
    if isinstance(node, Cluster):
        return node
    if isinstance(node, Sequence):
        return node.steps[0]
    if isinstance(node, Alternation):
        return primary_cluster(node.branches[0])
    return None  # Unmapped
