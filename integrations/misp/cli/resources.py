"""Object templates and the tlctc taxonomy, read at runtime — nothing hardcoded."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent.parent          # integrations/misp
OBJECTS_DIR = PKG_DIR / "objects"
TAXONOMY_PATH = PKG_DIR / "taxonomies" / "tlctc" / "machinetag.json"


@dataclass(frozen=True)
class Template:
    name: str
    uuid: str
    version: int
    meta_category: str
    description: str
    attributes: dict
    required: list


def load_template(name: str, base: Path | None = None) -> Template:
    p = (base or OBJECTS_DIR) / name / "definition.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    return Template(name=d["name"], uuid=d["uuid"], version=int(d["version"]), meta_category=d["meta-category"],
                    description=d["description"], attributes=d["attributes"], required=list(d.get("required", [])))


def load_taxonomy(path: Path | None = None) -> dict:
    return json.loads((path or TAXONOMY_PATH).read_text(encoding="utf-8"))


class Taxonomy:
    """Lookup over machinetag.json keyed by strategic cluster id ('#1'..'#10')."""

    def __init__(self, data: dict):
        self.namespace = data["namespace"]
        self._entries = {}   # predicate -> {strategic: entry}
        for block in data["values"]:
            self._entries[block["predicate"]] = {f"#{e['numerical_value']}": e for e in block["entry"]}

    def _entry(self, predicate: str, strategic: str) -> dict:
        return self._entries[predicate][strategic]   # KeyError on unknown predicate/cluster

    def value(self, strategic: str) -> str:
        return self._entry("cluster", strategic)["value"]

    def colour(self, strategic: str) -> str:
        return self._entry("cluster", strategic)["colour"]

    def tag(self, predicate: str, strategic: str) -> dict:
        e = self._entry(predicate, strategic)
        return {"name": f'{self.namespace}:{predicate}="{e["value"]}"', "colour": e["colour"]}


@dataclass(frozen=True)
class Resources:
    path_template: Template
    step_template: Template
    taxonomy: Taxonomy

    @classmethod
    def load(cls, base: Path | None = None) -> "Resources":
        base = base or PKG_DIR
        return cls(path_template=load_template("tlctc-attack-path", base / "objects"),
                   step_template=load_template("tlctc-attack-step", base / "objects"),
                   taxonomy=Taxonomy(load_taxonomy(base / "taxonomies" / "tlctc" / "machinetag.json")))
