"""Load mappings/veris/tlctc-veris.json and look entries up by VERIS id."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_MAPPING = HERE.parent / "tlctc-veris.json"
DEFAULT_ATTACK_CSV = HERE.parent / "pinned" / "veris-1.4.1_attack-19.1-enterprise.csv"
DEFAULT_ATTACK_TLCTC = HERE.parent.parent / "mitre-attack-enterprise" / "tlctc-enterprise-attack.json"

CLUSTER_TYPES = ("direct", "conditional", "chain")


class Mapping:
    def __init__(self, doc: dict):
        self.metadata: dict = doc["metadata"]
        self.entries: list[dict] = doc["entries"]
        self._by_id = {e["veris_id"]: e for e in self.entries}

    @property
    def veris_version(self) -> str:
        return self.metadata["veris_version"]

    @property
    def tlctc_version(self) -> str:
        return self.metadata["tlctc_version"]

    @property
    def updated(self) -> str:
        return self.metadata["updated"]

    def get(self, veris_id: str) -> dict | None:
        return self._by_id.get(veris_id)

    def __contains__(self, veris_id: str) -> bool:
        return veris_id in self._by_id

    def __len__(self) -> int:
        return len(self.entries)


def load_mapping(path: str | Path | None = None) -> Mapping:
    p = Path(path) if path else DEFAULT_MAPPING
    with open(p, encoding="utf-8") as fh:
        return Mapping(json.load(fh))
