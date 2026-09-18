"""Classify the whole Attack Flow corpus with the ATT&CK → TLCTC mapping and write the study's aggregates.

    python study/run-study.py [--commit SHA] [--cache DIR] [--out DIR] [--images DIR] [--accept-new-corpus]

Downloads corpus/*.afb from the pinned attack-flow commit (file list and sha256 per file in
study/corpus-sha256.json), verifies every file, classifies every flow, compares the two flows that
also exist as hand-classified TLCTC paths, and writes results.json (every count with its
denominator), results.md and three SVG figures. No corpus file is written inside the repository.
Python 3.10+, standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
sys.path.insert(0, str(PKG_ROOT))

from cli.afb import read_afb  # noqa: E402
from cli.classify import CLUSTERS, classify_flow, render_md, summarize  # noqa: E402
from cli.mapping import load_attack_mapping  # noqa: E402

REPO = "center-for-threat-informed-defense/attack-flow"
REPO_ROOT = PKG_ROOT.parent.parent
OVERLAP = {
    "SolarWinds.afb": REPO_ROOT / "json-schemas/layer-3/examples/solarwinds-2020.json",
    "Tesla Kubernetes Breach.afb": REPO_ROOT / "attack-paths/tesla-k8s-cryptojacking-2018.json",
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_corpus(commit: str, names: list[str], cache: Path) -> dict[str, Path]:
    d = cache / commit[:12]
    d.mkdir(parents=True, exist_ok=True)
    out = {}
    for n in names:
        p = d / n
        if not p.exists():
            url = f"https://raw.githubusercontent.com/{REPO}/{commit}/corpus/{urllib.parse.quote(n)}"
            print(f"downloading {n}", file=sys.stderr)
            with urllib.request.urlopen(url) as resp, open(p, "wb") as fh:
                fh.write(resp.read())
        out[n] = p
    return out


def layer3_clusters(path: Path) -> list[dict]:
    """Flatten a Layer 3 path into ordered steps: {cluster or None, step_id, parallel}."""
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    steps = []
    for item in doc["path_sequence"]:
        if "steps" in item:
            for s in item["steps"]:
                steps.append({"step_id": s["step_id"], "cluster": _strategic(s.get("cluster")) if s.get("status") != "unresolved" else None, "parallel": True})
        else:
            steps.append({"step_id": item["step_id"], "cluster": _strategic(item.get("cluster")) if item.get("status") != "unresolved" else None, "parallel": False})
    return steps


def _strategic(c):
    if not c:
        return None
    if c.startswith("#"):
        return "#" + c[1:].split(".")[0]
    if c.startswith("TLCTC-"):
        return f"#{int(c[6:8])}"
    return c


def lcs(a: list, b: list) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            dp[i + 1][j + 1] = dp[i][j] + 1 if a[i] == b[j] else max(dp[i][j + 1], dp[i + 1][j])
    return dp[m][n]


def compare(derived: dict, hand: list[dict]) -> dict:
    d_steps = [s["cluster"] for s in derived["path"]["compressed"] if s["kind"] == "classified"]
    h_steps = [s["cluster"] for s in hand if s["cluster"]]
    d_set, h_set = set(d_steps), set(h_steps)
    return {
        "derived_compressed": derived["notation_compressed"],
        "derived_raw_steps": derived["steps_raw"],
        "hand_notation": " → ".join(h_steps),
        "hand_steps": len(hand),
        "derived_steps": len(derived["path"]["compressed"]),
        "clusters_hand": sorted(h_set, key=lambda s: int(s[1:])),
        "clusters_derived_certain": derived["clusters_certain"],
        "clusters_derived_upper": derived["clusters_upper"],
        "hand_clusters_reached_certain": {"n": len(h_set & d_set), "denominator": len(h_set)},
        "hand_clusters_reached_upper": {"n": len(h_set & set(derived["clusters_upper"])), "denominator": len(h_set)},
        "derived_clusters_not_in_hand": sorted(d_set - h_set, key=lambda s: int(s[1:])),
        "lcs_of_cluster_sequences": {"n": lcs(d_steps, h_steps), "denominator": len(h_steps)},
        "entry_agrees": bool(h_steps) and derived["entry_cluster"] == h_steps[0],
    }


# ---------------------------------------------------------------- figures
def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_frequency(freq: dict, nflows: int, nactions: int) -> str:
    w, left, top, bar_h, gap = 800, 150, 44, 22, 12
    h = top + 10 * (bar_h + gap) + 20
    maxv = max(v["flows_upper"]["n"] for v in freq.values()) or 1
    scale = (w - left - 140) / maxv
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Helvetica, Arial, sans-serif" font-size="12">',
             f'<text x="{left}" y="22" font-size="14" font-weight="bold">Corpus flows touching each cluster (n = {nflows} flows, {nactions} actions); dark = certain, light = with rule-dependent alternatives</text>']
    y = top
    for c in CLUSTERS:
        fc, fu = freq[c]["flows_certain"]["n"], freq[c]["flows_upper"]["n"]
        parts.append(f'<text x="{left - 8}" y="{y + 16}" text-anchor="end">{_esc(c)}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{fu * scale:.1f}" height="{bar_h}" fill="#c7e9c0"/>')
        parts.append(f'<rect x="{left}" y="{y}" width="{fc * scale:.1f}" height="{bar_h}" fill="#238b45"/>')
        parts.append(f'<text x="{left + fu * scale + 6:.1f}" y="{y + 16}">{fc} / {fu} flows · {freq[c]["actions_certain"]["n"]} actions</text>')
        y += bar_h + gap
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def svg_transitions(matrix: dict) -> str:
    n, cell, left, top = 10, 52, 90, 60
    w, h = left + n * cell + 40, top + n * cell + 40
    maxv = max(matrix.values()) or 1
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Helvetica, Arial, sans-serif" font-size="12">',
             f'<text x="{left}" y="24" font-size="14" font-weight="bold">Cluster transitions along corpus flows (row = from, column = to; classified steps only)</text>']
    for i, c in enumerate(CLUSTERS):
        parts.append(f'<text x="{left + i * cell + cell / 2:.0f}" y="{top - 8}" text-anchor="middle">{_esc(c)}</text>')
        parts.append(f'<text x="{left - 8}" y="{top + i * cell + cell / 2 + 4:.0f}" text-anchor="end">{_esc(c)}</text>')
    for i, a in enumerate(CLUSTERS):
        for j, b in enumerate(CLUSTERS):
            v = matrix.get(f"{a}|{b}", 0)
            t = v / maxv
            r, g, bl = int(255 - 220 * t), int(255 - 120 * t), int(255 - 200 * t)
            parts.append(f'<rect x="{left + j * cell}" y="{top + i * cell}" width="{cell - 2}" height="{cell - 2}" fill="rgb({r},{g},{bl})" stroke="#ddd"/>')
            if v:
                parts.append(f'<text x="{left + j * cell + cell / 2 - 1:.0f}" y="{top + i * cell + cell / 2 + 4:.0f}" text-anchor="middle" fill="{"#fff" if t > 0.6 else "#111"}">{v}</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def svg_compression(per_flow: list[dict]) -> str:
    w, left, top, bar_h, gap = 900, 260, 44, 12, 4
    rows = sorted(per_flow, key=lambda f: -f["actions"])
    h = top + len(rows) * (bar_h + gap) + 20
    maxv = max(f["actions"] for f in rows) or 1
    scale = (w - left - 120) / maxv
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Helvetica, Arial, sans-serif" font-size="10">',
             f'<text x="{left}" y="22" font-size="14" font-weight="bold">Actions per flow (light) and derived TLCTC steps after compression (dark)</text>']
    y = top
    for f in rows:
        parts.append(f'<text x="{left - 6}" y="{y + 10}" text-anchor="end">{_esc(f["flow"][:38])}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{f["actions"] * scale:.1f}" height="{bar_h}" fill="#dadaeb"/>')
        parts.append(f'<rect x="{left}" y="{y}" width="{f["steps"] * scale:.1f}" height="{bar_h}" fill="#6a51a3"/>')
        parts.append(f'<text x="{left + f["actions"] * scale + 4:.1f}" y="{y + 10}">{f["actions"]} → {f["steps"]}{" (" + str(f["unresolved"]) + " ?)" if f["unresolved"] else ""}</text>')
        y += bar_h + gap
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    with open(HERE / "corpus-sha256.json", encoding="utf-8") as fh:
        pinned = json.load(fh)
    ap.add_argument("--commit", default=pinned["commit"])
    ap.add_argument("--cache", default=str(Path(tempfile.gettempdir()) / "tlctc-attack-flow"))
    ap.add_argument("--out", default=str(HERE))
    ap.add_argument("--images", default=str(REPO_ROOT / "documentation" / "images"))
    ap.add_argument("--accept-new-corpus", action="store_true", help="for a new commit: rewrite corpus-sha256.json instead of verifying against it")
    args = ap.parse_args(argv)

    names = sorted(pinned["files"])
    files = fetch_corpus(args.commit, names, Path(args.cache))
    hashes = {n: sha256(p) for n, p in files.items()}
    if args.commit == pinned["commit"] and not args.accept_new_corpus:
        bad = [n for n in names if hashes[n] != pinned["files"][n]]
        if bad:
            print(f"error: {len(bad)} corpus file(s) differ from study/corpus-sha256.json: {bad[:3]}", file=sys.stderr)
            return 2
    elif args.accept_new_corpus:
        (HERE / "corpus-sha256.json").write_text(json.dumps({"commit": args.commit, "files": hashes}, indent=2) + "\n", encoding="utf-8", newline="\n")

    mapping = load_attack_mapping()
    results = []
    for n in names:
        flow = read_afb(files[n])
        flow.source = n
        results.append(classify_flow(flow, mapping))
    summary = summarize(results)
    overlap = {}
    for n, l3 in OVERLAP.items():
        r = next((x for x in results if x["source"] == n), None)
        if r and l3.exists():
            overlap[n] = compare(r, layer3_clusters(l3))
            overlap[n]["layer3_file"] = str(l3.relative_to(REPO_ROOT)).replace("\\", "/")
    summary["overlap"] = overlap

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    doc = {
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "corpus": {"repo": REPO, "commit": args.commit, "flows": len(results), "sha256_file": "study/corpus-sha256.json"},
        "attack_mapping": {"file": "mappings/mitre-attack-enterprise/tlctc-enterprise-attack.json", "techniques": len(mapping.by_id), "tlctc_version": mapping.metadata.get("tlctc_version")},
        "tables": summary,
        "flows": [{k: v for k, v in r.items() if k not in ("actions",)} | {"actions": [{k2: v2 for k2, v2 in a.items() if k2 != "attachments"} for a in r["actions"]]} for r in results],
    }
    (out / "results.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    md = [f"# Attack Flow corpus study results", "", f"Generated {doc['generated']} from {REPO} commit `{args.commit}` ({len(results)} flows), ATT&CK→TLCTC mapping with {len(mapping.by_id)} techniques.", "",
          render_md(summary, title="All corpus flows"), "", "### Overlap with hand-classified TLCTC paths", ""]
    for n, o in overlap.items():
        md += [f"**{n}** vs `{o['layer3_file']}`", "", f"- hand path: `{o['hand_notation']}` ({o['hand_steps']} steps)", f"- derived (compressed): `{o['derived_compressed']}` ({o['derived_steps']} steps from {o['derived_raw_steps']} raw)",
               f"- hand clusters reached (certain / upper): {o['hand_clusters_reached_certain']['n']} / {o['hand_clusters_reached_upper']['n']} of {o['hand_clusters_reached_certain']['denominator']}; derived clusters not in the hand path: {', '.join(o['derived_clusters_not_in_hand']) or 'none'}",
               f"- longest common cluster subsequence: {o['lcs_of_cluster_sequences']['n']} of {o['lcs_of_cluster_sequences']['denominator']}; entry cluster agrees: {o['entry_agrees']}", ""]
    (out / "results.md").write_text("\n".join(md), encoding="utf-8", newline="\n")

    images = Path(args.images)
    images.mkdir(parents=True, exist_ok=True)
    (images / "attack-flow-cluster-frequency.svg").write_text(svg_frequency(summary["frequency"], summary["flows"], summary["profile"]["actions"]["n"]), encoding="utf-8", newline="\n")
    (images / "attack-flow-transitions.svg").write_text(svg_transitions(summary["transition_matrix"]), encoding="utf-8", newline="\n")
    (images / "attack-flow-compression.svg").write_text(svg_compression(summary["per_flow"]), encoding="utf-8", newline="\n")
    print(f"wrote {out / 'results.json'}, {out / 'results.md'}, 3 figures in {images}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
