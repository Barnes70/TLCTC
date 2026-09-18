"""ATT&CK technique → TLCTC lookup over mappings/mitre-attack-enterprise/tlctc-enterprise-attack.json.

The mapping's `tlctcMapping` strings use a small notation: `#N` (a cluster), `#N.M` (a sub-cluster
shorthand), `A → B` (a sequence), `A | B` (alternatives), parentheses for grouping, and `N/A`
(threat potential outside the target domain, e.g. attacker-side preparation). `parse_mapping`
turns a string into a list of alternatives, each alternative a list of clusters in order.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_ATTACK_MAPPING = HERE.parent.parent.parent / "mappings" / "mitre-attack-enterprise" / "tlctc-enterprise-attack.json"

CLUSTER_RE = re.compile(r"#(10|[1-9])(?:\.(\d+))?")


class ParseError(ValueError):
    pass


def _tokens(s: str) -> list[str]:
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
        elif c in "()|":
            out.append(c)
            i += 1
        elif s.startswith("→", i):
            out.append("→")
            i += 1
        elif s.startswith("->", i):
            out.append("→")
            i += 2
        elif c == "#":
            m = CLUSTER_RE.match(s, i)
            if not m:
                raise ParseError(f"bad cluster at {i} in {s!r}")
            out.append(m.group(0))
            i = m.end()
        else:
            raise ParseError(f"unexpected {c!r} at {i} in {s!r}")
    return out


def _strip_sub(cluster: str) -> str:
    return "#" + CLUSTER_RE.match(cluster).group(1)


def parse_mapping(s: str) -> list[list[str]]:
    """Return alternatives (list) of sequences (list of '#N' strings). 'N/A' → []."""
    s = (s or "").strip()
    if not s or s.upper() == "N/A":
        return []
    toks = _tokens(s)
    pos = 0

    def peek():
        return toks[pos] if pos < len(toks) else None

    def parse_alt():  # alt := seq ('|' seq)*
        nonlocal pos
        alts = [parse_seq()]
        while peek() == "|":
            pos += 1
            alts.append(parse_seq())
        return alts

    def parse_seq():  # seq := atom ('→' atom)*  ; atom may itself yield alternatives → distribute
        nonlocal pos
        parts = [parse_atom()]
        while peek() == "→":
            pos += 1
            parts.append(parse_atom())
        # each part is a list of alternatives (each alternative a sequence); distribute
        result = [[]]
        for part in parts:
            result = [r + a for r in result for a in part]
        return result

    def parse_atom():  # atom := cluster | '(' alt ')'   → returns list of alternatives (sequences)
        nonlocal pos
        t = peek()
        if t == "(":
            pos += 1
            inner = parse_alt()
            if peek() != ")":
                raise ParseError(f"missing ')' in {s!r}")
            pos += 1
            return [seq for alt in inner for seq in alt]
        if t and t.startswith("#"):
            pos += 1
            return [[_strip_sub(t)]]
        raise ParseError(f"unexpected token {t!r} in {s!r}")

    alts = parse_alt()
    if pos != len(toks):
        raise ParseError(f"trailing tokens in {s!r}")
    # flatten: parse_alt returns list of (list of sequences)
    flat = [seq for alt in alts for seq in alt]
    # dedupe preserving order
    seen = set()
    out = []
    for seq in flat:
        key = tuple(seq)
        if key not in seen:
            seen.add(key)
            out.append(seq)
    return out


class AttackMapping:
    def __init__(self, doc: dict):
        self.metadata = doc.get("metadata", {})
        self.by_id: dict[str, dict] = {m["techniqueId"]: m for m in doc["mappings"]}

    def lookup(self, technique_id: str | None) -> dict:
        """{status: resolved|rule_dependent|preparation|unmapped|no_technique, alternatives, technique_used, raw}"""
        if not technique_id:
            return {"status": "no_technique", "alternatives": [], "technique_used": None, "raw": None}
        tid = technique_id.strip().upper()
        used = tid
        m = self.by_id.get(tid)
        if m is None and "." in tid:
            used = tid.split(".")[0]
            m = self.by_id.get(used)
        if m is None:
            return {"status": "unmapped", "alternatives": [], "technique_used": None, "raw": None}
        raw = m.get("tlctcMapping", "")
        try:
            alts = parse_mapping(raw)
        except ParseError:
            return {"status": "unmapped", "alternatives": [], "technique_used": used, "raw": raw}
        if not alts:
            return {"status": "preparation", "alternatives": [], "technique_used": used, "raw": raw}
        return {"status": "resolved" if len(alts) == 1 else "rule_dependent", "alternatives": alts, "technique_used": used, "raw": raw}


def load_attack_mapping(path: str | Path | None = None) -> AttackMapping:
    p = Path(path) if path else DEFAULT_ATTACK_MAPPING
    with open(p, encoding="utf-8") as fh:
        return AttackMapping(json.load(fh))
