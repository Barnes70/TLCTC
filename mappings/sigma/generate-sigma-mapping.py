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

No rule detection bodies are copied - only id, title, logsource, techniques,
and our derived clusters (license-safe).
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml  # PyYAML - build-time dependency only

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
        except yaml.YAMLError as e:
            print(f"[skip] unparseable Sigma YAML: {path}: {e}", file=sys.stderr)
            continue


_CLUSTER_RE = re.compile(r"#(\d+)")


def load_attack_index(attack_path=ATTACK_MAPPING):
    """techniqueId -> tlctcMapping expression (e.g. 'T1059' -> '#1')."""
    doc = json.loads(Path(attack_path).read_text(encoding="utf-8"))
    return {e["techniqueId"]: e.get("tlctcMapping", "") for e in doc["mappings"]}


def _clusters(expr):
    """'#1 | #7' -> ['#1','#7'] (lowest-numbered first); 'N/A' -> []."""
    nums = sorted(int(n) for n in _CLUSTER_RE.findall(expr or ""))
    return [f"#{n}" for n in nums]


def derive_record(rule, attack_index):
    cluster_set, any_alt, any_unmapped = [], False, False
    for tech in rule["techniques"]:
        expr = attack_index.get(tech)
        clusters = _clusters(expr) if expr is not None else []
        if not clusters:
            any_unmapped = True
            continue
        if len(clusters) > 1:
            any_alt = True
        for c in clusters:
            if c not in cluster_set:
                cluster_set.append(c)
    cluster_set = [f"#{n}" for n in sorted(int(c[1:]) for c in cluster_set)]
    if not cluster_set:
        status, primary = "unmapped", None
    elif any_alt or len(cluster_set) > 1:
        status, primary = "ambiguous", cluster_set[0]
    else:
        status, primary = "ok", cluster_set[0]
    if any_unmapped and cluster_set:
        status = "ambiguous"  # partial resolution
    return {
        "ruleId": rule["ruleId"],
        "ruleTitle": rule["ruleTitle"],
        "logsource": rule["logsource"],
        "techniques": rule["techniques"],
        "clusterSet": cluster_set,
        "primaryCluster": primary,
        "derivationStatus": status,
    }


def build(rules_dir, attack_path, sigma_commit="unknown"):
    idx = load_attack_index(attack_path)
    records = [derive_record(r, idx) for r in walk_rules(rules_dir)]
    mapping = {
        "metadata": {
            "title": "TLCTC Sigma Mapping (SigmaHQ rules -> TLCTC)",
            "description": "Per-rule TLCTC cluster derivation from Sigma ATT&CK tags via ATT&CK->TLCTC.",
            "tlctc_version": "2.3",
            "sigma_commit": sigma_commit,
            "attack_mapping": str(Path(attack_path).name),
            "total_rules": len(records),
            "license": "CC-BY-4.0",
            "publisher": "TLCTC Project",
            "caveats": [
                "Mapping quality depends on each rule's attack.t* tagging; untagged rules are 'unmapped'.",
                "Derived mechanically from the experimental AI-generated ATT&CK->TLCTC mapping.",
                "Sub-techniques are folded to their parent technique.",
                "No Sigma rule detection bodies are reproduced - titles + GUIDs + derivation only.",
            ],
        },
        "mappings": records,
    }
    dist = Counter(r["primaryCluster"] for r in records
                   if r["derivationStatus"] == "ok" and r["primaryCluster"])
    stats = {
        "total_rules": len(records),
        "cluster_distribution": dict(sorted(dist.items(), key=lambda kv: int(kv[0][1:]))),
        "status_counts": dict(Counter(r["derivationStatus"] for r in records)),
        "logsource_breakdown": dict(Counter(
            (r["logsource"] or {}).get("category", "(none)") for r in records)),
    }
    return mapping, stats


def write_outputs(mapping, stats):
    OUTPUT_MAP.write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
    OUTPUT_STATS.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")


def main(argv=None):
    p = argparse.ArgumentParser(description="Generate the TLCTC Sigma mapping.")
    p.add_argument("--rules-dir", required=True, help="path to a SigmaHQ rules clone")
    p.add_argument("--sigma-commit", default="unknown", help="commit SHA of the rules clone")
    args = p.parse_args(argv)
    mapping, stats = build(args.rules_dir, ATTACK_MAPPING, args.sigma_commit)
    write_outputs(mapping, stats)
    print(f"Wrote {len(mapping['mappings'])} rule records to {OUTPUT_MAP.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
