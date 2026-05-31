#!/usr/bin/env python3
"""Generate the TLCTC Sigma mapping from SigmaHQ rules.

Deterministic ETL:
  Sigma rule  ->  attack.tXXXX tags  ->  parent technique IDs
  technique   ->  TLCTC cluster (via tlctc-enterprise-attack.json)

Inputs:
  --rules-dir   local clone of SigmaHQ rules (path; commit SHA recorded)
  tlctc-enterprise-attack.json (pinned, in-tree)

Outputs:
  mappings/sigma/tlctc-sigma.json        per-rule records
  mappings/sigma/tlctc-sigma-stats.json  aggregate statistics

No rule detection bodies are copied — only id, title, logsource, techniques,
and our derived clusters (license-safe).
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml  # PyYAML — build-time dependency only

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ATTACK_MAPPING = ROOT / "mappings" / "mitre-attack-enterprise" / "tlctc-enterprise-attack.json"
OUTPUT_MAP = HERE / "tlctc-sigma.json"
OUTPUT_STATS = HERE / "tlctc-sigma-stats.json"

_TECH_RE = re.compile(r"attack\.t(\d+)(?:\.\d+)?$", re.IGNORECASE)


def _techniques_from_tags(tags):
    """Extract parent technique IDs from attack.tXXXX[.YYY] tags, deduped+sorted."""
    out = set()
    for tag in tags or []:
        m = _TECH_RE.match(str(tag).strip())
        if m:
            out.add(f"T{m.group(1)}")
    return sorted(out)


def parse_rule(path: Path):
    doc = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return {
        "ruleId": doc.get("id", ""),
        "ruleTitle": doc.get("title", ""),
        "logsource": doc.get("logsource", {}),
        "techniques": _techniques_from_tags(doc.get("tags", [])),
    }


def walk_rules(rules_dir: Path):
    for path in sorted(Path(rules_dir).rglob("*.yml")):
        try:
            yield parse_rule(path)
        except yaml.YAMLError:
            continue  # skip non-rule YAML (e.g. config) silently
