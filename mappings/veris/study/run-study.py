"""Run the VERIS → TLCTC mapping over the VERIS Community Database and write the study's aggregates.

    python study/run-study.py [--data PATH-or-URL] [--cache DIR] [--out DIR] [--images DIR]

Downloads the pinned VCDB joined zip (see ../PINNED.md), verifies its sha256, classifies every
record, and writes results.json (every number with its denominator), results.md (the tables),
and three SVG figures. No record is written anywhere inside the repository.
Python 3.10+, standard library only. Run from mappings/veris (or anywhere: paths are resolved).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import tempfile
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
sys.path.insert(0, str(PKG_ROOT))

from cli import attack_check  # noqa: E402
from cli.classify import classify  # noqa: E402
from cli.mapping import load_mapping  # noqa: E402
from cli.summary import CLUSTERS, render_md, summarize  # noqa: E402

VCDB_COMMIT = "230cf22b56a481dd1a994b21e4d94c59e2bccea9"
VCDB_URL = f"https://raw.githubusercontent.com/vz-risk/VCDB/{VCDB_COMMIT}/data/joined/vcdb.json.zip"
VCDB_SHA256 = "e4be5dd432ccfad16520a6b60dd83e9d47c63b0f3352c26c4d43a5dd774c32c0"
REPO_ROOT = PKG_ROOT.parent.parent


def fetch(data: str, cache: Path) -> Path:
    if not data.startswith("http"):
        return Path(data)
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / f"vcdb-{VCDB_COMMIT[:12]}.json.zip"
    if not target.exists():
        print(f"downloading {data} -> {target}", file=sys.stderr)
        with urllib.request.urlopen(data) as resp, open(target, "wb") as fh:
            fh.write(resp.read())
    return target


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_records(path: Path) -> list[dict]:
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as z:
            name = next(n for n in z.namelist() if n.endswith(".json"))
            return json.loads(z.read(name).decode("utf-8"))
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    return doc if isinstance(doc, list) else [doc]


def year_band(record: dict) -> str:
    y = (record.get("timeline", {}).get("incident", {}) or {}).get("year")
    if not isinstance(y, int):
        return "year:unknown"
    if y <= 2014:
        return "year:<=2014"
    if y <= 2019:
        return "year:2015-2019"
    return "year:2020-2026"


def sub_source(record: dict) -> str:
    s = (record.get("plus", {}) or {}).get("sub_source")
    if not s:
        return "sub_source:none"
    return f"sub_source:{s}" if s in ("phidbr", "priority") else "sub_source:other"


STRATA_DESCRIPTION = {
    "all": "every record in the joined dataset",
    "year:<=2014": "timeline.incident.year <= 2014",
    "year:2015-2019": "timeline.incident.year in 2015..2019",
    "year:2020-2026": "timeline.incident.year in 2020..2026",
    "year:unknown": "timeline.incident.year missing",
    "sub_source:none": "plus.sub_source absent (random selection per the VCDB README)",
    "sub_source:phidbr": "plus.sub_source = phidbr (healthcare, selected on purpose)",
    "sub_source:priority": "plus.sub_source = priority (selected on purpose)",
    "sub_source:other": "plus.sub_source has another value",
}


# ---------------------------------------------------------------- figures (plain SVG)
def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_frequency(freq: dict, total: int) -> str:
    w, h, left, top, bar_h, gap = 800, 40 + 10 * 34 + 30, 150, 40, 22, 12
    maxv = max(v["upper"]["n"] for v in freq.values()) or 1
    scale = (w - left - 120) / maxv
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Helvetica, Arial, sans-serif" font-size="12">',
             f'<text x="{left}" y="22" font-size="14" font-weight="bold">Records touching each cluster (n = {total}); dark = certain, light = upper bound with rule-dependent alternatives</text>']
    y = top
    for c in CLUSTERS:
        cert, upp = freq[c]["certain"]["n"], freq[c]["upper"]["n"]
        parts.append(f'<text x="{left - 8}" y="{y + 16}" text-anchor="end">{_esc(c)}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{upp * scale:.1f}" height="{bar_h}" fill="#9ecae1"/>')
        parts.append(f'<rect x="{left}" y="{y}" width="{cert * scale:.1f}" height="{bar_h}" fill="#08519c"/>')
        parts.append(f'<text x="{left + upp * scale + 6:.1f}" y="{y + 16}">{cert} / {upp}</text>')
        y += bar_h + gap
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def svg_cooccurrence(matrix: dict, total: int) -> str:
    n, cell, left, top = 10, 52, 90, 60
    w, h = left + n * cell + 40, top + n * cell + 40
    maxv = max(matrix.values()) or 1
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Helvetica, Arial, sans-serif" font-size="12">',
             f'<text x="{left}" y="24" font-size="14" font-weight="bold">Records in which two clusters are both certain (n = {total} records)</text>']
    for i, c in enumerate(CLUSTERS):
        parts.append(f'<text x="{left + i * cell + cell / 2:.0f}" y="{top - 8}" text-anchor="middle">{_esc(c)}</text>')
        parts.append(f'<text x="{left - 8}" y="{top + i * cell + cell / 2 + 4:.0f}" text-anchor="end">{_esc(c)}</text>')
    for i, a in enumerate(CLUSTERS):
        for j, b in enumerate(CLUSTERS):
            if j <= i:
                continue
            v = matrix.get(f"{a}|{b}", 0)
            t = v / maxv
            r, g, bl = int(255 - 200 * t), int(255 - 150 * t), int(255 - 60 * t)
            parts.append(f'<rect x="{left + j * cell}" y="{top + i * cell}" width="{cell - 2}" height="{cell - 2}" fill="rgb({r},{g},{bl})" stroke="#ddd"/>')
            if v:
                parts.append(f'<text x="{left + j * cell + cell / 2 - 1:.0f}" y="{top + i * cell + cell / 2 + 4:.0f}" text-anchor="middle" fill="{"#fff" if t > 0.6 else "#111"}">{v}</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def svg_availability(av: dict) -> str:
    varieties = av["varieties"]
    colours = {"Av": "#b30000", "Ac": "#fc8d59", "A": "#fdd49e"}
    w, left, top, bar_h, gap = 800, 130, 60, 22, 10
    rows = [(k, v) for k, v in varieties.items() if v["n"]]
    h = top + len(rows) * (bar_h + gap) + 120
    maxv = max(v["n"] for _, v in rows) or 1
    scale = (w - left - 160) / maxv
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Helvetica, Arial, sans-serif" font-size="12">',
             '<text x="130" y="24" font-size="14" font-weight="bold">attribute.availability.variety re-read as Data Risk Event codes</text>',
             f'<rect x="130" y="34" width="12" height="12" fill="{colours["Av"]}"/><text x="146" y="45">Av: data gone</text>',
             f'<rect x="260" y="34" width="12" height="12" fill="{colours["Ac"]}"/><text x="276" y="45">Ac: present but unusable</text>',
             f'<rect x="440" y="34" width="12" height="12" fill="{colours["A"]}"/><text x="456" y="45">A: refinement not recorded</text>']
    y = top
    for k, v in rows:
        parts.append(f'<text x="{left - 8}" y="{y + 16}" text-anchor="end">{_esc(k)}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{v["n"] * scale:.1f}" height="{bar_h}" fill="{colours[v["dre"]]}"/>')
        parts.append(f'<text x="{left + v["n"] * scale + 6:.1f}" y="{y + 16}">{v["n"]} ({v["dre"]})</text>')
        y += bar_h + gap
    r = av["ransomware"]
    y += 20
    parts.append(f'<text x="{left}" y="{y}" font-weight="bold">Ransomware records (n = {r["records"]["n"]}): Obscuration/Ac {r["with_obscuration_Ac"]["n"]}, Loss/Av {r["with_loss_Av"]["n"]}, Destruction/Av {r["with_destruction_Av"]["n"]}, Interruption/A {r["with_interruption_A"]["n"]}, no availability attribute {r["with_no_availability_attribute"]["n"]}</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data", default=VCDB_URL, help="path to vcdb.json.zip / joined json, or URL (default: pinned VCDB commit)")
    ap.add_argument("--cache", default=str(Path(tempfile.gettempdir()) / "tlctc-veris"))
    ap.add_argument("--out", default=str(HERE))
    ap.add_argument("--images", default=str(REPO_ROOT / "documentation" / "images"))
    ap.add_argument("--no-hash-check", action="store_true", help="accept a dataset other than the pinned snapshot")
    args = ap.parse_args(argv)

    src = fetch(args.data, Path(args.cache))
    digest = sha256(src)
    if digest != VCDB_SHA256 and not args.no_hash_check:
        print(f"error: {src} sha256 {digest} != pinned {VCDB_SHA256} (use --no-hash-check for another snapshot)", file=sys.stderr)
        return 2
    records = load_records(src)
    mapping = load_mapping()
    va = attack_check.load_veris_attack()
    at = attack_check.load_attack_tlctc()
    print(f"classifying {len(records)} records", file=sys.stderr)
    results = [classify(r, mapping) for r in records]
    checks = [attack_check.check(res, va, at, mapping) for res in results]

    strata: dict[str, list[int]] = {"all": list(range(len(records)))}
    for i, r in enumerate(records):
        strata.setdefault(year_band(r), []).append(i)
        strata.setdefault(sub_source(r), []).append(i)
    order = ["all", "year:<=2014", "year:2015-2019", "year:2020-2026", "year:unknown", "sub_source:none", "sub_source:phidbr", "sub_source:priority", "sub_source:other"]
    tables: dict[str, dict] = {}
    for name in order:
        idx = strata.get(name)
        if not idx:
            continue
        s = summarize([results[i] for i in idx])
        s["attack_agreement"] = attack_check.summarize_agreement([checks[i] for i in idx], mapping)
        tables[name] = s

    schema_versions = Counter(str(r.get("schema_version")) for r in records)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    results_doc = {
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "vcdb": {"commit": VCDB_COMMIT, "url": args.data if args.data.startswith("http") else VCDB_URL, "sha256": digest, "records": len(records),
                 "schema_versions": dict(schema_versions.most_common()), "note": "joined dataset; VCDB's packaging excludes the web-skimmer batch"},
        "mapping_updated": mapping.updated,
        "mapping_veris_version": mapping.veris_version,
        "mapping_tlctc_version": mapping.tlctc_version,
        "strata": {name: {"records": len(strata[name]), "filter": STRATA_DESCRIPTION[name]} for name in tables},
        "tables": tables,
    }
    (out / "results.json").write_text(json.dumps(results_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    md = [f"# VCDB study results", "", f"Generated {results_doc['generated']} from VCDB commit `{VCDB_COMMIT}` ({len(records)} records, sha256 `{digest}`), mapping updated {mapping.updated}.", "",
          "Every cell is n (percentage of the row's denominator). Strata follow the VCDB README's warning that `phidbr` and `priority` records are not randomly selected.", ""]
    for name, s in tables.items():
        md.append(render_md(s, title=f"Stratum `{name}` — {STRATA_DESCRIPTION[name]}"))
    (out / "results.md").write_text("\n".join(md), encoding="utf-8", newline="\n")

    images = Path(args.images)
    images.mkdir(parents=True, exist_ok=True)
    allt = tables["all"]
    (images / "veris-cluster-frequency.svg").write_text(svg_frequency(allt["frequency"], allt["records"]), encoding="utf-8", newline="\n")
    (images / "veris-cooccurrence.svg").write_text(svg_cooccurrence(allt["cooccurrence"]["matrix"], allt["records"]), encoding="utf-8", newline="\n")
    (images / "veris-availability-split.svg").write_text(svg_availability(allt["availability"]), encoding="utf-8", newline="\n")
    print(f"wrote {out / 'results.json'}, {out / 'results.md'}, 3 figures in {images}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
