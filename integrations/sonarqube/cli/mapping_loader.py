"""Load and index the canonical CWE -> TLCTC mapping.

The on-disk file is `mappings/mitre-cwe/tlctc-cwe.json` with the envelope
`{metadata, mappings[]}`. This module loads it once, parses each mapping's
path notation via `path_parser.parse`, and exposes a lookup by CWE id.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from . import path_parser
from .path_parser import PathNode

EXPECTED_TLCTC_VERSION = "2.1"

VERDICT_ALLOWED = "Allowed"
VERDICT_REVIEW = "Allowed-with-Review"
VERDICT_DISCOURAGED = "Discouraged"
VERDICT_PROHIBITED = "Prohibited"

ALL_VERDICTS = (VERDICT_ALLOWED, VERDICT_REVIEW, VERDICT_DISCOURAGED, VERDICT_PROHIBITED)


class MappingLoadError(RuntimeError):
    """Raised when the canonical mapping cannot be loaded or is structurally invalid."""


@dataclass(frozen=True)
class MappingEntry:
    cwe_id: str            # "CWE-79"
    cwe_name: str
    cwe_status: str
    tlctc_mapping: str     # raw "#2 -> #7 | #3"
    tlctc_mapping_name: str
    rationale: str
    verdict: str
    context_dependent: bool
    cve_references: tuple[str, ...]
    path: PathNode         # parsed AST


@dataclass(frozen=True)
class MappingIndex:
    version: str
    cwe_version: str
    total_entries: int
    entries: dict[str, MappingEntry]   # keyed by cwe_id, e.g. "CWE-79"

    def get(self, cwe_id: str) -> MappingEntry | None:
        return self.entries.get(_normalize_cwe(cwe_id))

    def filter_by_verdict(self, verdicts: Iterable[str]) -> list[MappingEntry]:
        allow = set(verdicts)
        return [e for e in self.entries.values() if e.verdict in allow]


def load(path: str | Path) -> MappingIndex:
    """Load the envelope, validate it, parse every path, return a MappingIndex."""
    p = Path(path)
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MappingLoadError(f"mapping file not found: {p}") from exc
    except json.JSONDecodeError as exc:
        raise MappingLoadError(f"mapping file is not valid JSON: {p}: {exc}") from exc

    if not isinstance(raw, dict) or "metadata" not in raw or "mappings" not in raw:
        raise MappingLoadError(
            f"mapping file missing envelope keys (metadata, mappings): {p}"
        )

    metadata = raw["metadata"]
    version = str(metadata.get("tlctc_version", ""))
    cwe_version = str(metadata.get("cwe_version", ""))
    total = int(metadata.get("total_entries", 0) or 0)

    if version != EXPECTED_TLCTC_VERSION:
        # Not fatal — surface as a warning via the returned index. Callers may log.
        pass

    entries: dict[str, MappingEntry] = {}
    parse_errors: list[str] = []
    for raw_entry in raw["mappings"]:
        try:
            entry = _parse_entry(raw_entry)
        except (KeyError, TypeError, path_parser.PathParseError) as exc:
            parse_errors.append(f"{raw_entry.get('cweId', '<unknown>')}: {exc}")
            continue
        entries[entry.cwe_id] = entry

    if parse_errors:
        head = "; ".join(parse_errors[:5])
        more = f" (+{len(parse_errors) - 5} more)" if len(parse_errors) > 5 else ""
        raise MappingLoadError(f"{len(parse_errors)} mapping entries failed to parse: {head}{more}")

    return MappingIndex(
        version=version,
        cwe_version=cwe_version,
        total_entries=total,
        entries=entries,
    )


def _parse_entry(raw_entry: dict) -> MappingEntry:
    cwe_id = _normalize_cwe(raw_entry["cweId"])
    mapping_str = raw_entry["tlctcMapping"]
    return MappingEntry(
        cwe_id=cwe_id,
        cwe_name=raw_entry.get("cweName", ""),
        cwe_status=raw_entry.get("cweStatus", ""),
        tlctc_mapping=mapping_str,
        tlctc_mapping_name=raw_entry.get("tlctcMappingName", ""),
        rationale=raw_entry.get("mappingRationale", ""),
        verdict=raw_entry.get("mappingVerdict", ""),
        context_dependent=bool(raw_entry.get("contextDependent", False)),
        cve_references=tuple(raw_entry.get("cveReferences", []) or []),
        path=path_parser.parse(mapping_str),
    )


def _normalize_cwe(value: str) -> str:
    """Accept 'CWE-79', '79', 'cwe:79' — always return 'CWE-79'."""
    if value is None:
        return ""
    s = str(value).strip()
    if s.lower().startswith("cwe:"):
        s = "CWE-" + s.split(":", 1)[1]
    if not s.upper().startswith("CWE-"):
        if s.isdigit():
            s = "CWE-" + s
        else:
            return s
    return "CWE-" + s.split("-", 1)[1]
