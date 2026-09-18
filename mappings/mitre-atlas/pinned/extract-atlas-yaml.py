"""Extract the technique list of an ATLAS v6 data release (mitre-atlas/atlas-data dist/v6/ATLAS-<ver>.yaml)
into a small JSON the validator can read without a YAML parser.

    python extract-atlas-yaml.py <ATLAS-2026.09.yaml> <out.json>

Requires PyYAML (only for this extraction; nothing else in the repository needs it).
"""
import hashlib
import json
import sys

import yaml

src, out = sys.argv[1], sys.argv[2]
raw = open(src, "rb").read()
doc = yaml.safe_load(raw.decode("utf-8"))

def entries(section):
    """Format 6 keeps tactics / techniques / relationships as maps keyed by id; older layouts used lists."""
    if isinstance(section, dict):
        return [v for v in section.values() if isinstance(v, dict)]
    return [v for v in (section or []) if isinstance(v, dict)]


tactic_ids = {t["id"] for t in entries(doc.get("tactics")) if isinstance(t.get("id"), str)}
techniques = {}


def walk(o):
    if isinstance(o, dict):
        i = o.get("id")
        if isinstance(i, str) and i.startswith("AML.T") and not i.startswith("AML.TA") and "name" in o and i not in techniques:
            tac = o.get("tactics") or []
            sub = o.get("subtechnique-of")
            techniques[i] = {
                "id": i,
                "name": o["name"],
                "tactics": [x["id"] if isinstance(x, dict) else x for x in tac],
                "subtechnique_of": sub["id"] if isinstance(sub, dict) else sub,
                "description": (o.get("description") or "").strip(),
            }
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


walk(doc)
# technique → tactic links live in relationships rather than on the technique: in format 6 the section is a
# map keyed by technique id whose values group `achieves` / `specializes` lists of {source, target} entries.
def relationship_entries(section):
    for e in entries(section):
        if "source" in e or "target" in e:
            yield e
        for v in e.values():
            if isinstance(v, list):
                for r in v:
                    if isinstance(r, dict):
                        yield r


for r in relationship_entries(doc.get("relationships")):
    if r.get("relationship-type") not in (None, "achieves"):
        continue
    s, t = r.get("source"), r.get("target")
    s = s.get("id") if isinstance(s, dict) else s
    t = t.get("id") if isinstance(t, dict) else t
    if isinstance(s, str) and isinstance(t, str):
        if s in techniques and t in tactic_ids and t not in techniques[s]["tactics"]:
            techniques[s]["tactics"].append(t)
        if t in techniques and s in tactic_ids and s not in techniques[t]["tactics"]:
            techniques[t]["tactics"].append(s)

result = {
    "source": {"repo": "mitre-atlas/atlas-data", "file": src.split("/")[-1].split("\\")[-1], "sha256": hashlib.sha256(raw).hexdigest(),
               "format_version": doc.get("format-version"), "version": doc.get("version") or (doc.get("collection") or {}).get("version")},
    "tactics": sorted(tactic_ids),
    "techniques": [techniques[k] for k in sorted(techniques)],
}
with open(out, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(result, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print(f"{len(result['techniques'])} techniques, {len(tactic_ids)} tactics, version {result['source']['version']}")
