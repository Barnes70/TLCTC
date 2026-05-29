"""Top-level CLI for the TLCTC SonarQube sidecar.

Subcommands:
  classify  - pull issues from Sonar, classify them, emit reports
  tag       - alias of `classify --apply-tags`
  validate  - offline checks of config + mapping integrity
  version   - print version
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from . import __version__
from . import classifier as classifier_mod
from . import config as config_mod
from . import tagger as tagger_mod
from .classifier import ClassifiedFinding
from .context_resolver import RoleConfig
from .mapping_loader import (
    ALL_VERDICTS,
    EXPECTED_TLCTC_VERSION,
    VERDICT_ALLOWED,
    VERDICT_REVIEW,
    MappingIndex,
    load as load_mapping,
)
from .reporters import json_report, markdown_report, sarif_report
from .sonar_client import SonarApiError, SonarClient, SonarTransportError

EXIT_OK = 0
EXIT_GATE = 1
EXIT_USAGE = 2
EXIT_API_AUTH = 3
EXIT_API_NETWORK = 4
EXIT_MAPPING = 5
EXIT_PARTIAL = 6

REPO_ROOT_GUESS = Path(__file__).resolve().parents[3]
DEFAULT_MAPPING = REPO_ROOT_GUESS / "mappings" / "mitre-cwe" / "tlctc-cwe.json"
DEFAULT_CONFIG_LOCAL_CANDIDATES = (
    Path("tlctc-sonar.toml"),
    Path("tlctc-sonar.json"),
)
EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"
DEFAULT_CONFIG_EXAMPLE_CANDIDATES = (
    EXAMPLES_DIR / "tlctc-sonar.toml",
    EXAMPLES_DIR / "tlctc-sonar.json",
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return EXIT_USAGE
    if args.command == "version":
        print(f"tlctc-sonar {__version__}")
        return EXIT_OK
    if args.command == "validate":
        return _cmd_validate(args)
    if args.command in ("classify", "tag"):
        if args.command == "tag":
            args.apply_tags = True
        return _cmd_classify(args)
    parser.error(f"unknown command: {args.command}")
    return EXIT_USAGE


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tlctc-sonar", description="TLCTC ↔ SonarQube SAST sidecar")
    sub = p.add_subparsers(dest="command")

    classify = sub.add_parser("classify", help="Pull issues, classify, emit reports")
    _add_common_flags(classify)
    _add_classify_flags(classify)

    tag = sub.add_parser("tag", help="Alias of `classify --apply-tags`")
    _add_common_flags(tag)
    _add_classify_flags(tag)

    validate = sub.add_parser("validate", help="Offline config + mapping integrity check")
    _add_common_flags(validate)

    sub.add_parser("version", help="Print version and exit")
    return p


def _add_common_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", type=Path, default=None, help="Path to tlctc-sonar.toml (default: ./tlctc-sonar.toml or examples/tlctc-sonar.toml)")
    parser.add_argument("--mapping", type=Path, default=None, help=f"Override mapping file (default: {DEFAULT_MAPPING})")
    parser.add_argument("--quiet", action="store_true", help="Suppress informational logging")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    parser.add_argument("--log-format", choices=("text", "json"), default="text")


def _add_classify_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--sonar-url", default=None, help="SonarQube base URL (env: SONAR_URL). Use file://path.json for offline.")
    parser.add_argument("--token", default=None, help="SonarQube token (env: SONAR_TOKEN)")
    parser.add_argument("--project-key", action="append", default=[], help="Project key (repeatable)")
    parser.add_argument("--component-keys", default=None, help="Comma-separated component keys")
    parser.add_argument("--branch", default=None)
    parser.add_argument("--pull-request", default=None)
    parser.add_argument("--since", default=None, help="createdAfter, e.g. 2026-01-01")
    parser.add_argument("--severities", default=None, help="Comma-separated, e.g. BLOCKER,CRITICAL,MAJOR")
    parser.add_argument("--types", default="VULNERABILITY,SECURITY_HOTSPOT")
    parser.add_argument("--include-verdicts", default=f"{VERDICT_ALLOWED},{VERDICT_REVIEW}",
                        help=f"Comma-separated verdicts to classify (any of {','.join(ALL_VERDICTS)})")
    parser.add_argument("--strict-verdict", action="store_true",
                        help="Exclude Allowed-with-Review from --fail-on-cluster gating")
    parser.add_argument("--out-json", type=Path, default=None)
    parser.add_argument("--out-md", type=Path, default=None)
    parser.add_argument("--out-sarif", type=Path, default=None)
    parser.add_argument("--apply-tags", action="store_true", help="Write tlctc-0N tags back via /api/issues/set_tags")
    parser.add_argument("--dry-run", action="store_true", help="With --apply-tags, log planned POSTs only")
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--max-pages", type=int, default=50)
    parser.add_argument("--fail-on-cluster", default=None,
                        help="Comma-separated cluster IDs; non-zero exit if any finding lands here. e.g. #2,#7")


def _resolve_config_path(arg_config: Path | None) -> Path | None:
    if arg_config is not None:
        return arg_config
    for candidate in DEFAULT_CONFIG_LOCAL_CANDIDATES:
        if candidate.exists():
            return candidate
    for candidate in DEFAULT_CONFIG_EXAMPLE_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def _log(args: argparse.Namespace):
    def emit(msg: str) -> None:
        if args.quiet:
            return
        if args.log_format == "json":
            import json as _json
            print(_json.dumps({"msg": msg}))
        else:
            print(msg, file=sys.stderr)
    return emit


def _cmd_validate(args: argparse.Namespace) -> int:
    log = _log(args)
    config_path = _resolve_config_path(args.config)
    if config_path is None:
        cfg = config_mod.default(repo_root=REPO_ROOT_GUESS)
        log("no config file found; using built-in defaults")
    else:
        try:
            cfg = config_mod.load(config_path, repo_root=REPO_ROOT_GUESS)
        except Exception as exc:
            print(f"config load failed ({config_path}): {exc}", file=sys.stderr)
            return EXIT_USAGE
        log(f"config OK: {config_path} (source={cfg.source})")

    mapping_path = args.mapping or cfg.mapping_file
    try:
        index = load_mapping(mapping_path)
    except Exception as exc:
        print(f"mapping load failed ({mapping_path}): {exc}", file=sys.stderr)
        return EXIT_MAPPING

    if index.version != EXPECTED_TLCTC_VERSION:
        log(f"warning: mapping tlctc_version={index.version!r}, expected {EXPECTED_TLCTC_VERSION!r}")
    log(f"mapping OK: {mapping_path} ({len(index.entries)} entries, tlctc_version={index.version})")
    return EXIT_OK


def _cmd_classify(args: argparse.Namespace) -> int:
    log = _log(args)

    if not (args.out_json or args.out_md or args.out_sarif):
        print("error: at least one of --out-json / --out-md / --out-sarif is required", file=sys.stderr)
        return EXIT_USAGE

    config_path = _resolve_config_path(args.config)
    if config_path is None:
        cfg = config_mod.default(repo_root=REPO_ROOT_GUESS)
        log("no config file found; using built-in defaults")
    else:
        try:
            cfg = config_mod.load(config_path, repo_root=REPO_ROOT_GUESS)
        except Exception as exc:
            print(f"config load failed ({config_path}): {exc}", file=sys.stderr)
            return EXIT_USAGE

    sonar_url = args.sonar_url or config_mod.env_url()
    token = args.token or config_mod.env_token() or ""
    if not sonar_url:
        print("error: --sonar-url (or SONAR_URL) is required", file=sys.stderr)
        return EXIT_USAGE

    mapping_path = args.mapping or cfg.mapping_file
    try:
        index = load_mapping(mapping_path)
    except Exception as exc:
        print(f"mapping load failed ({mapping_path}): {exc}", file=sys.stderr)
        return EXIT_MAPPING

    client = SonarClient(base_url=str(sonar_url), token=str(token))
    include_verdicts = tuple(v.strip() for v in args.include_verdicts.split(",") if v.strip())

    component_keys = [k.strip() for k in args.component_keys.split(",")] if args.component_keys else None
    severities = [s.strip() for s in args.severities.split(",")] if args.severities else None
    types = [t.strip() for t in args.types.split(",")] if args.types else None

    try:
        issues = list(client.search_issues(
            project_keys=args.project_key or None,
            component_keys=component_keys,
            branch=args.branch,
            pull_request=args.pull_request,
            created_after=args.since,
            severities=severities,
            types=types,
            page_size=args.page_size,
            max_pages=args.max_pages,
        ))
    except SonarApiError as exc:
        print(f"Sonar API error: {exc}", file=sys.stderr)
        return EXIT_API_AUTH
    except SonarTransportError as exc:
        print(f"Sonar transport error: {exc}", file=sys.stderr)
        return EXIT_API_NETWORK

    log(f"fetched {len(issues)} issue(s)")

    findings = [
        classifier_mod.classify(issue, index, cfg.role_config, include_verdicts=include_verdicts)
        for issue in issues
    ]
    summary = classifier_mod.summarize(findings)
    log(f"classified {sum(1 for f in findings if f.resolved)} of {len(findings)}")

    project_label = ",".join(args.project_key) if args.project_key else (args.component_keys or sonar_url)
    written = _write_reports(args, findings, summary, index, project_label)
    for path in written:
        log(f"wrote {path}")

    exit_code = EXIT_OK
    if args.apply_tags:
        plans = [tagger_mod.plan(f) for f in findings if f.resolved]
        applied = tagger_mod.apply(client, plans, dry_run=args.dry_run, log=log)
        log(f"tags applied: {applied}/{sum(1 for p in plans if p.tlctc_tags)}")

    gate = _evaluate_gate(args, findings)
    if gate is not None:
        log(f"gate matched: cluster {gate}")
        exit_code = EXIT_GATE
    return exit_code


def _write_reports(
    args: argparse.Namespace,
    findings: list[ClassifiedFinding],
    summary: dict,
    index: MappingIndex,
    project_label: str,
) -> list[Path]:
    written: list[Path] = []
    if args.out_json:
        args.out_json.write_text(
            json_report.render(findings, summary, index.version, project_label),
            encoding="utf-8",
        )
        written.append(args.out_json)
    if args.out_md:
        args.out_md.write_text(
            markdown_report.render(findings, summary, index.version, project_label),
            encoding="utf-8",
        )
        written.append(args.out_md)
    if args.out_sarif:
        args.out_sarif.write_text(
            sarif_report.render(findings, summary, index.version, project_label),
            encoding="utf-8",
        )
        written.append(args.out_sarif)
    return written


def _evaluate_gate(args: argparse.Namespace, findings: list[ClassifiedFinding]) -> str | None:
    if not args.fail_on_cluster:
        return None
    targets = {int(t.strip().lstrip("#")) for t in args.fail_on_cluster.split(",") if t.strip()}
    for f in findings:
        for r in f.resolved:
            if args.strict_verdict and r.entry.verdict == VERDICT_REVIEW:
                continue
            if r.primary_cluster and r.primary_cluster.number in targets:
                return f"#{r.primary_cluster.number}"
    return None


if __name__ == "__main__":
    sys.exit(main())
