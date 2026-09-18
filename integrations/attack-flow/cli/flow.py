"""The Flow model both readers produce: actions, conditions, operators and the flow edges between them.

Only *flow* edges are kept as edges (action/condition/operator → action/condition/operator).
Edges from an action to an asset, tool, malware, note or other STIX object are *attachments*:
they annotate the action and never carry the flow.
"""
from __future__ import annotations

from dataclasses import dataclass, field

FLOW_KINDS = {"action", "condition", "operator"}


@dataclass
class Action:
    id: str
    name: str
    technique_id: str | None = None
    tactic_id: str | None = None
    description: str | None = None
    execution_start: str | None = None
    execution_end: str | None = None
    confidence: str | None = None


@dataclass
class Condition:
    id: str
    description: str


@dataclass
class Operator:
    id: str
    operator: str  # AND | OR


@dataclass
class Edge:
    src: str
    dst: str
    label: str | None = None  # "true" / "false" for condition branches, else None


@dataclass
class Flow:
    name: str
    scope: str | None = None
    description: str | None = None
    source: str = ""
    actions: dict[str, Action] = field(default_factory=dict)
    conditions: dict[str, Condition] = field(default_factory=dict)
    operators: dict[str, Operator] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    attachments: dict[str, list[str]] = field(default_factory=dict)  # action id → names of attached objects
    start_ids: list[str] = field(default_factory=list)

    # ------------------------------------------------------------ graph helpers
    def kind(self, node_id: str) -> str | None:
        if node_id in self.actions:
            return "action"
        if node_id in self.conditions:
            return "condition"
        if node_id in self.operators:
            return "operator"
        return None

    def nodes(self) -> list[str]:
        return [*self.actions, *self.conditions, *self.operators]

    def successors(self, node_id: str) -> list[tuple[str, str | None]]:
        return [(e.dst, e.label) for e in self.edges if e.src == node_id]

    def predecessors(self, node_id: str) -> list[str]:
        return [e.src for e in self.edges if e.dst == node_id]

    def starts(self) -> list[str]:
        """Declared start nodes, else every flow node without an incoming flow edge, in insertion order."""
        if self.start_ids:
            return [s for s in self.start_ids if self.kind(s)]
        incoming = {e.dst for e in self.edges}
        return [n for n in self.nodes() if n not in incoming]

    def topological_order(self) -> list[str]:
        """Kahn's algorithm over flow nodes; cycles are broken by insertion order (a warning case, recorded by the caller)."""
        indeg = {n: 0 for n in self.nodes()}
        for e in self.edges:
            if e.dst in indeg and e.src in indeg:
                indeg[e.dst] += 1
        order: list[str] = []
        ready = [n for n in self.starts() if indeg.get(n, 0) == 0]
        for n in self.nodes():
            if indeg[n] == 0 and n not in ready:
                ready.append(n)
        seen: set[str] = set()
        while ready:
            n = ready.pop(0)
            if n in seen:
                continue
            seen.add(n)
            order.append(n)
            for dst, _ in self.successors(n):
                if dst not in indeg:
                    continue
                indeg[dst] -= 1
                if indeg[dst] == 0 and dst not in seen:
                    ready.append(dst)
        for n in self.nodes():  # cycle remainder
            if n not in seen:
                order.append(n)
                seen.add(n)
        return order

    def has_cycle(self) -> bool:
        indeg = {n: 0 for n in self.nodes()}
        for e in self.edges:
            if e.dst in indeg and e.src in indeg:
                indeg[e.dst] += 1
        ready = [n for n, d in indeg.items() if d == 0]
        count = 0
        while ready:
            n = ready.pop()
            count += 1
            for dst, _ in self.successors(n):
                if dst in indeg:
                    indeg[dst] -= 1
                    if indeg[dst] == 0:
                        ready.append(dst)
        return count < len(indeg)
