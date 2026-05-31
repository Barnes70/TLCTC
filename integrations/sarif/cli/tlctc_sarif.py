"""argparse entrypoint for the TLCTC SARIF classifier."""
import argparse
import sys

from cli import __version__
from cli.config import load_config
from cli.mapping_loader import MappingLoader
from cli.sarif_loader import load_findings
from cli.classifier import classify
from cli.reporters import json_report, markdown_report, sarif_report

_REPORTERS = {"json": json_report, "markdown": markdown_report, "sarif": sarif_report}


def _cmd_classify(args):
    cfg = load_config(args.config)
    if args.fail_on_cluster:
        cfg.fail_on_cluster = [c.strip() for c in args.fail_on_cluster.split(",")]
    if args.format:
        cfg.formats = [f.strip() for f in args.format.split(",")]
    ml = MappingLoader(cfg.cwe_mapping_path, cfg.kev_mapping_path)
    findings = load_findings(args.sarif_file)
    classified = [classify(f, ml, cfg.source_globs) for f in findings]
    for fmt in cfg.formats:
        print(_REPORTERS[fmt].render(classified))
    hit = {r.primary_cluster for r in classified
           if r.status == "classified"} & set(cfg.fail_on_cluster)
    return 2 if hit else 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="tlctc-sarif")
    p.add_argument("--version", action="version", version=f"tlctc-sarif {__version__}")
    sub = p.add_subparsers(dest="command", required=True)
    c = sub.add_parser("classify", help="classify a SARIF file")
    c.add_argument("sarif_file")
    c.add_argument("--config")
    c.add_argument("--format")
    c.add_argument("--fail-on-cluster")
    c.set_defaults(func=_cmd_classify)
    args = p.parse_args(argv)
    return args.func(args)
