"""Select 20 VCDB records as test fixtures (deterministic). Usage: python select-fixtures.py <vcdb.json.zip> <repo-root> [<tree-listing.txt>]"""
import json, sys, zipfile
from pathlib import Path

zip_path, root = sys.argv[1], Path(sys.argv[2])
OUT = root / "mappings/veris/tests/fixtures/vcdb"
OUT.mkdir(parents=True, exist_ok=True)
COMMIT = "230cf22b56a481dd1a994b21e4d94c59e2bccea9"

z = zipfile.ZipFile(zip_path)
data = json.loads(z.read(z.namelist()[0]).decode("utf-8"))
data.sort(key=lambda r: r["incident_id"])

def cats(r):
    return set(r.get("action", {}).keys())

def has(r, cat, field, value):
    return value in (r.get("action", {}).get(cat, {}) or {}).get(field, [])

def vector_partner(r):
    return any(has(r, c, "vector", "Partner") for c in ("hacking", "malware", "social"))

PREDICATES = [
    ("hacking only", lambda r: cats(r) == {"hacking"}),
    ("malware only", lambda r: cats(r) == {"malware"}),
    ("social only", lambda r: cats(r) == {"social"}),
    ("misuse only", lambda r: cats(r) == {"misuse"}),
    ("physical only", lambda r: cats(r) == {"physical"}),
    ("error only", lambda r: cats(r) == {"error"}),
    ("environmental only", lambda r: cats(r) == {"environmental"}),
    ("unknown only", lambda r: cats(r) == {"unknown"}),
    ("social + hacking", lambda r: cats(r) == {"social", "hacking"}),
    ("social + malware", lambda r: cats(r) == {"social", "malware"}),
    ("hacking + malware", lambda r: cats(r) == {"hacking", "malware"}),
    ("three action categories", lambda r: len(cats(r)) == 3),
    ("availability Obscuration", lambda r: "Obscuration" in (r.get("attribute", {}).get("availability", {}) or {}).get("variety", [])),
    ("hacking Use of stolen creds", lambda r: has(r, "hacking", "variety", "Use of stolen creds")),
    ("Partner vector", vector_partner),
    ("data_disclosure Potentially", lambda r: (r.get("attribute", {}).get("confidentiality", {}) or {}).get("data_disclosure") == "Potentially"),
    ("schema_version 1.3.x", lambda r: str(r.get("schema_version", "")).startswith("1.3")),
    ("plus.sub_source phidbr", lambda r: r.get("plus", {}).get("sub_source") == "phidbr"),
    ("plus.sub_source priority", lambda r: r.get("plus", {}).get("sub_source") == "priority"),
    ("Ransomware with Loss (not Obscuration)", lambda r: has(r, "malware", "variety", "Ransomware") and "Loss" in (r.get("attribute", {}).get("availability", {}) or {}).get("variety", []) and "Obscuration" not in (r.get("attribute", {}).get("availability", {}) or {}).get("variety", [])),
]

chosen = []
used = set()
for name, pred in PREDICATES:
    pick = next((r for r in data if r["incident_id"] not in used and pred(r)), None)
    if pick is None:
        raise SystemExit(f"no record for predicate: {name}")
    used.add(pick["incident_id"])
    chosen.append((name, pick))

for old in OUT.glob("*.json"):
    if old.name != "expected.json":
        old.unlink()
rows = []
for name, r in chosen:
    (OUT / f"{r['incident_id']}.json").write_text(json.dumps(r, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    rows.append((name, r["incident_id"], r.get("schema_version"), r.get("plus", {}).get("analysis_status") or ""))

sel = ["# Fixture selection", "",
       f"Twenty records from the VCDB joined dataset at commit `{COMMIT}` (10,047 records, sorted by `incident_id`).",
       "For each predicate below, the first record in that order that satisfies it and was not already chosen. Re-running",
       "`select-fixtures.py` against the same snapshot reproduces the same twenty files.", "",
       "| # | Predicate | incident_id | schema_version |", "|---|---|---|---|"]
for i, (name, iid, sv, _) in enumerate(rows, 1):
    sel.append(f"| {i} | {name} | `{iid}` | {sv} |")
sel.append("")
(OUT / "SELECTION.md").write_text("\n".join(sel), encoding="utf-8", newline="\n")

lic = ["# Licence of the fixture records", "",
       "The twenty `*.json` files in this directory are verbatim records of the **VERIS Community Database (VCDB)**,",
       "https://github.com/vz-risk/VCDB, published by the Verizon RISK Team under the",
       "**Creative Commons Attribution-ShareAlike 4.0 International** licence (CC BY-SA 4.0).",
       "They are reproduced here unchanged, as test fixtures, under that licence; they are not covered by the",
       "CC BY 4.0 licence of the rest of this repository. `expected.json` and `SELECTION.md` are ours (CC BY 4.0).", "",
       f"Snapshot: `data/joined/vcdb.json.zip` at commit `{COMMIT}` (2026-08-04).", "",
       "| incident_id | source |", "|---|---|"]
tree = set(Path(sys.argv[3]).read_text(encoding="utf-8").split()) if len(sys.argv) > 3 else set()
for _, iid, _, _ in rows:
    path = f"data/json/validated/{iid}.json"
    if path in tree:
        lic.append(f"| `{iid}` | https://github.com/vz-risk/VCDB/blob/{COMMIT}/{path} |")
    else:
        lic.append(f"| `{iid}` | joined dataset only: not present as a per-incident file under `data/json/` at this commit; taken from https://github.com/vz-risk/VCDB/blob/{COMMIT}/data/joined/vcdb.json.zip |")
lic.append("")
(OUT / "LICENSE.md").write_text("\n".join(lic), encoding="utf-8", newline="\n")
for name, iid, sv, st in rows:
    print(f"{name:40s} {iid} {sv} {st}")
