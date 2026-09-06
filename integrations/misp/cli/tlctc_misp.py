"""argparse entrypoint for the TLCTC → MISP converter.

  python -m cli convert attack-paths/incident.json -o incident.misp.json
  python -m cli convert attack-paths/*.json --out-dir out/
  python -m cli validate incident.misp.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cli import __version__
from cli.convert import Options, convert, dumps
from cli.layer3 import Layer3Error, load_layer3
from cli.resources import Resources
from cli.validate import validate_event


def _cmd_convert(args) -> int:
    if args.output and len(args.inputs) > 1:
        raise SystemExit("--output takes exactly one input; use --out-dir for several files")
    res = Resources.load()
    opt = Options(distribution=args.distribution, threat_level=args.threat_level, analysis=args.analysis,
                  orgc=args.orgc, attachment=not args.no_attachment)
    for src in args.inputs:
        p = Path(src)
        try:
            doc = load_layer3(p)
        except Layer3Error as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        text = dumps(convert(doc, opt, res, source_bytes=p.read_bytes()))
        if args.out_dir:
            out_dir = Path(args.out_dir)
            out_dir.mkdir(parents=True, exist_ok=True)
            target = out_dir / f"{p.stem}.misp.json"
        elif args.output:
            target = Path(args.output)
        else:
            sys.stdout.write(text)
            continue
        target.write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {target}", file=sys.stderr)
    return 0


def _cmd_validate(args) -> int:
    p = Path(args.event_file)
    try:
        event = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"error: {p}: cannot read JSON — {e}")
        return 1
    errors = validate_event(event, Resources.load())
    if errors:
        print(f"INVALID: {p} — {len(errors)} problem(s)")
        for e in errors:
            print(f"  {e}")
        return 1
    ev = event["Event"]
    print(f"OK: {p} — {len(ev.get('Object') or [])} objects, {len(ev.get('Tag') or [])} tags")
    return 0


def _ranged(lo, hi):
    def parse(s):
        v = int(s)
        if not lo <= v <= hi:
            raise argparse.ArgumentTypeError(f"must be between {lo} and {hi}")
        return v
    return parse


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="tlctc-misp", description="Convert TLCTC Layer 3 attack paths to MISP events.")
    p.add_argument("--version", action="version", version=f"tlctc-misp {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("convert", help="convert Layer 3 JSON file(s) to MISP event JSON")
    c.add_argument("inputs", nargs="+", help="Layer 3 attack path file(s)")
    c.add_argument("-o", "--output", help="output file (single input only); default: stdout")
    c.add_argument("--out-dir", help="write <stem>.misp.json per input into this directory")
    c.add_argument("--distribution", type=_ranged(0, 3), default=0, help="MISP distribution level 0-3 (default 0)")
    c.add_argument("--threat-level", type=_ranged(1, 4), default=4, help="MISP threat_level_id 1-4 (default 4 = undefined)")
    c.add_argument("--analysis", type=_ranged(0, 2), default=2, help="MISP analysis 0-2 (default 2 = completed)")
    c.add_argument("--orgc", help="creator organisation name; omitted by default so the importing instance assigns it")
    c.add_argument("--no-attachment", action="store_true", help="skip the layer3-json attachment attribute")
    c.set_defaults(func=_cmd_convert)

    v = sub.add_parser("validate", help="structurally check an emitted MISP event against the templates")
    v.add_argument("event_file")
    v.set_defaults(func=_cmd_validate)

    args = p.parse_args(argv)
    return args.func(args)
