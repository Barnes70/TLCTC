"""Command line: python -m cli classify <file.json | dir/> [options]

Exit codes: 0 success, 1 usage error, 2 unreadable input (the message names the file).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import attack_check
from .classify import classify
from .mapping import load_mapping
from .summary import render_md, summarize


class InputError(Exception):
    pass


def load_records(target: str | Path) -> list[dict]:
    p = Path(target)
    if p.is_dir():
        files = sorted(p.glob("*.json"))
        if not files:
            raise InputError(f"{p}: no *.json files")
        records: list[dict] = []
        for f in files:
            records.extend(load_records(f))
        return records
    if not p.exists():
        raise InputError(f"{p}: no such file")
    try:
        with open(p, encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        raise InputError(f"{p}: {exc}") from exc
    if isinstance(doc, list):
        bad = [i for i, r in enumerate(doc) if not isinstance(r, dict)]
        if bad:
            raise InputError(f"{p}: item {bad[0]} is not an object")
        return doc
    if isinstance(doc, dict):
        return [doc]
    raise InputError(f"{p}: top level must be an object or an array")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="python -m cli", description="Classify VERIS / VCDB incident records against the VERIS → TLCTC mapping.")
    sub = ap.add_subparsers(dest="command", required=True)
    c = sub.add_parser("classify", help="classify one file, a joined array, or a directory of records")
    c.add_argument("target", help="incident JSON file, joined JSON array, or directory of *.json")
    c.add_argument("--mapping", help="path to tlctc-veris.json (default: the repository copy)")
    c.add_argument("--format", choices=("json", "md"), default="json")
    c.add_argument("--summary", action="store_true", help="aggregate instead of listing per-record results")
    c.add_argument("--attack-check", action="store_true", help="add the VERIS→ATT&CK→TLCTC transitive comparison")
    c.add_argument("-o", "--output", help="write to this file instead of stdout")
    return ap


def run_classify(args: argparse.Namespace) -> tuple[list[dict], dict | None]:
    mapping = load_mapping(args.mapping)
    records = load_records(args.target)
    results = [classify(r, mapping) for r in records]
    checks = None
    if args.attack_check:
        va = attack_check.load_veris_attack()
        at = attack_check.load_attack_tlctc()
        checks = [attack_check.check(res, va, at, mapping) for res in results]
        for res, chk in zip(results, checks):
            res["attack_check"] = chk
    summary = None
    if args.summary:
        summary = summarize(results)
        if checks is not None:
            summary["attack_agreement"] = attack_check.summarize_agreement(checks, mapping)
    return results, summary


def render_results_md(results: list[dict]) -> str:
    out = ["| incident_id | certain | one_of | lost | rows | DRE | unresolved |", "|---|---|---|---|---|---|---|"]
    for r in results:
        lost = ", ".join(f"{c['cluster']}:{c['missing']}" for c in r["chains"] if c["missing"])
        out.append(f"| {r.get('incident_id') or '–'} | {' '.join(r['clusters']['certain']) or '–'} | {' / '.join('|'.join(g) for g in r['clusters']['one_of']) or '–'} | {lost or '–'} | {' '.join(r['partition_rows']) or '–'} | {' '.join(r['dre']) or '–'} | {len(r['unresolved'])} |")
    out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        results, summary = run_classify(args)
    except InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        text = json.dumps(summary if summary is not None else results, ensure_ascii=False, indent=2) + "\n"
    else:
        text = render_md(summary, title=f"Summary of {args.target}") if summary is not None else render_results_md(results)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0
