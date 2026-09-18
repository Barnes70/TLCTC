"""Command line:
    python -m cli classify <flow.afb | bundle.json | dir> [--format json|md] [--summary] [-o OUT]
    python -m cli export <layer3.json> [-o OUT]
    python -m cli validate-input <flow>

Exit codes: 0 success, 1 usage error, 2 unreadable input (the message names the file).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .classify import classify_flow, render_md, summarize
from .export import export_layer3
from .mapping import load_attack_mapping
from .stixflow import detect_and_read


class InputError(Exception):
    pass


def _flows(target: str) -> list[Path]:
    p = Path(target)
    if p.is_dir():
        files = sorted([*p.glob("*.afb"), *p.glob("*.json")])
        if not files:
            raise InputError(f"{p}: no *.afb or *.json files")
        return files
    if not p.exists():
        raise InputError(f"{p}: no such file")
    return [p]


def _read(p: Path):
    try:
        return detect_and_read(p)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise InputError(f"{p}: {exc}") from exc


def render_flow_md(r: dict) -> str:
    out = [f"### {r['flow']}", "", f"Scope: {r['scope'] or '–'} · actions {r['counts']['actions']} · conditions {r['counts']['conditions']} · operators {r['counts']['operators']}", "",
           f"Derived path (compressed): `{r['notation_compressed']}`", "", f"Derived path (raw): `{r['notation_raw']}`", "",
           "| # | action | technique | mapping | status | clusters |", "|---|---|---|---|---|---|"]
    for i, a in enumerate(r["actions"], 1):
        cl = " ".join(a["clusters_certain"]) or (" | ".join(a["clusters_candidates"]) if a["clusters_candidates"] else "–")
        out.append(f"| {i} | {a['name']} | {a['technique_id'] or '–'} | {a['mapping'] or '–'} | {a['status']} | {cl} |")
    if r["path"]["notes"]:
        out += ["", "Notes:"] + [f"- {n}" for n in r["path"]["notes"]]
    out.append("")
    return "\n".join(out)


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="python -m cli", description="TLCTC ↔ Attack Flow converter.")
    sub = ap.add_subparsers(dest="command", required=True)
    c = sub.add_parser("classify", help="classify every action of an Attack Flow through the ATT&CK → TLCTC mapping and derive a TLCTC path")
    c.add_argument("target", help=".afb (attack_flow_v2), Attack Flow STIX bundle, or a directory of them")
    c.add_argument("--mapping", help="path to tlctc-enterprise-attack.json (default: the repository copy)")
    c.add_argument("--format", choices=("json", "md"), default="json")
    c.add_argument("--summary", action="store_true", help="aggregate over all flows instead of listing each")
    c.add_argument("-o", "--output")
    e = sub.add_parser("export", help="export a TLCTC Layer 3 attack path to an Attack Flow STIX bundle with the TLCTC extension")
    e.add_argument("layer3", help="Layer 3 attack path JSON")
    e.add_argument("-o", "--output")
    v = sub.add_parser("validate-input", help="check that a flow file can be read (structure only)")
    v.add_argument("target")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "classify":
            mapping = load_attack_mapping(args.mapping)
            results = [classify_flow(_read(p), mapping) for p in _flows(args.target)]
            if args.summary:
                s = summarize(results)
                text = json.dumps(s, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else render_md(s, title=f"Summary of {args.target}")
            else:
                text = json.dumps(results, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else "\n".join(render_flow_md(r) for r in results)
        elif args.command == "export":
            try:
                bundle = export_layer3(args.layer3)
            except (OSError, ValueError, KeyError) as exc:
                raise InputError(f"{args.layer3}: {exc}") from exc
            text = json.dumps(bundle, ensure_ascii=False, indent=2) + "\n"
        else:
            flows = [_read(p) for p in _flows(args.target)]
            text = "\n".join(f"{f.source}: ok ({len(f.actions)} actions, {len(f.edges)} flow edges)" for f in flows) + "\n"
    except InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if getattr(args, "output", None):
        Path(args.output).write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0
