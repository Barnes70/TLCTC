#!/usr/bin/env python3
"""
Generate TLCTC KEV mapping from CISA Known Exploited Vulnerabilities catalog.

Deterministic ETL:
  CVE  ->  CWE(s) (via KEV catalog)
  CWE  ->  TLCTC cluster (via tlctc-cwe.json)
  R-ROLE '#2 | #3' ambiguity -> product-role-heuristic.json

Inputs (in-tree, pinned):
  mappings/cisa-kev/input/known_exploited_vulnerabilities.v*.json
  mappings/mitre-cwe/tlctc-cwe.json
  mappings/cisa-kev/product-role-heuristic.json

Outputs (regenerated each run):
  mappings/cisa-kev/tlctc-kev.json        -- per-CVE derived records
  mappings/cisa-kev/tlctc-kev-stats.json  -- aggregate statistics

Flags:
  --fetch  -- ad-hoc rebuild from live CISA feed (never in CI; tagged
             releases must be reproducible from in-tree inputs).

The derivation is PURELY mechanical. Every row is auditable: each field
can be traced back to the source CWE mapping + the heuristic rule that
fired. No manual per-CVE classification.

Confidence model:
  Each row inherits the source CWE's mappingVerdict. Multi-CWE rows
  take the WEAKEST verdict across all contributing CWEs. Discouraged /
  Prohibited / Unreviewed are preserved so downstream stats can segment
  them out (CWE-20 class would otherwise dominate the top-line).
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

DEFAULT_KEV_INPUT = HERE / "input" / "known_exploited_vulnerabilities.v2026.04.14.json"
CWE_MAPPING = ROOT / "mappings" / "mitre-cwe" / "tlctc-cwe.json"
HEURISTIC = HERE / "product-role-heuristic.json"

OUTPUT_KEV = HERE / "tlctc-kev.json"
OUTPUT_STATS = HERE / "tlctc-kev-stats.json"

KEV_LIVE_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

# Verdict strength ordering: weakest first. Used to pick the weakest across
# multiple source CWEs for a single CVE (conservative confidence).
VERDICT_STRENGTH = {
    "Prohibited": 0,
    "Discouraged": 1,
    "Unreviewed": 2,
    "Allowed-with-Review": 3,
    "Allowed": 4,
}

CLUSTER_RE = re.compile(r"#(\d+)")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def fetch_live_kev():
    print(f"Fetching live CISA KEV feed from {KEV_LIVE_URL}", file=sys.stderr)
    with urlopen(KEV_LIVE_URL) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_cwe_index(cwe_mapping):
    return {entry["cweId"]: entry for entry in cwe_mapping["mappings"]}


def tokenize_expression(expr):
    """Return all cluster tokens (as '#N') appearing in a mapping expression."""
    if not expr or expr == "N/A":
        return []
    return [f"#{m}" for m in CLUSTER_RE.findall(expr)]


def primary_from_expression(expr):
    """Canonical primary cluster: prefix before ' -> '/'->' (or first alternative).

    Rules from tlctc-cwe.json notation:
      'A -> B'  means A enables/leads to B. A is the cause -> primary = A.
      'A | B'   means either A or B depending on context. Left-most = primary.
      Composite '#2 -> #7 | #3' -> before arrow: '#2'; alternatives: '#2 | ...' -> '#2'.
    """
    if not expr or expr == "N/A":
        return None
    # Normalise arrow variants
    normalised = expr.replace("→", "->").replace("➝", "->")
    before_arrow = normalised.split("->", 1)[0].strip()
    first_alt = before_arrow.split("|", 1)[0].strip()
    m = CLUSTER_RE.search(first_alt)
    return f"#{m.group(1)}" if m else None


def has_ambiguous_role(expr):
    """True if the expression contains '#2 | #3' (the R-ROLE alternation)."""
    if not expr:
        return False
    normalised = re.sub(r"\s+", "", expr)
    # Accept '#2|#3' or '#3|#2' (order-insensitive per pair)
    return "#2|#3" in normalised or "#3|#2" in normalised


def apply_heuristic(vendor, product, heuristic_rules):
    """Return (role, rule_notes) or (None, None) if no match."""
    haystack = f"{vendor or ''} :: {product or ''}".lower()
    vendor_lc = (vendor or "").lower()
    for rule in heuristic_rules:
        if "pattern" in rule:
            if rule["pattern"].lower() in haystack:
                return rule["role"], rule.get("notes", "")
        elif "pattern_vendor" in rule:
            if rule["pattern_vendor"].lower() == vendor_lc:
                return rule["role"], rule.get("notes", "")
    return None, None


def weakest_verdict(verdicts):
    """Given a list of verdict strings, return the weakest."""
    if not verdicts:
        return "Unreviewed"
    return min(verdicts, key=lambda v: VERDICT_STRENGTH.get(v, -1))


def derive_entry(vuln, cwe_index, heuristic_rules):
    cves = vuln.get("cwes") or []
    vendor = vuln.get("vendorProject", "")
    product = vuln.get("product", "")

    record = {
        "cveID": vuln["cveID"],
        "vendorProject": vendor,
        "product": product,
        "vulnerabilityName": vuln.get("vulnerabilityName", ""),
        "dateAdded": vuln.get("dateAdded", ""),
        "dueDate": vuln.get("dueDate", ""),
        "knownRansomwareCampaignUse": vuln.get("knownRansomwareCampaignUse", "Unknown"),
        "shortDescription": vuln.get("shortDescription", ""),
        "sourceCwes": list(cves),
        "derivedMappingExpression": None,
        "primaryCluster": None,
        "clusterSet": [],
        "confidence": None,
        "derivationStatus": None,
        "contextResolvedBy": None,
    }

    if not cves:
        record["derivationStatus"] = "cwe-missing"
        record["confidence"] = "n/a"
        record["contextResolvedBy"] = "unresolved"
        return record

    # Per-CWE sub-derivations
    per_cwe = []
    for cwe_id in cves:
        cwe_entry = cwe_index.get(cwe_id)
        if not cwe_entry:
            per_cwe.append({
                "cwe": cwe_id,
                "status": "cwe-unmapped-in-tlctc",
                "expression": None,
                "verdict": None,
            })
            continue
        expr = cwe_entry.get("tlctcMapping")
        verdict = cwe_entry.get("mappingVerdict", "Unreviewed")
        if not expr or expr == "N/A":
            per_cwe.append({
                "cwe": cwe_id,
                "status": "cwe-too-abstract",
                "expression": expr,
                "verdict": verdict,
            })
            continue
        if verdict in ("Discouraged", "Prohibited"):
            # Still carries an expression but low-confidence. Treat as
            # too-abstract for status purposes (Discouraged) OR keep as ok
            # (Prohibited is category-level — mark too-abstract).
            status = "cwe-too-abstract" if verdict in ("Discouraged", "Prohibited") else "ok"
        else:
            status = "ok"
        per_cwe.append({
            "cwe": cwe_id,
            "status": status,
            "expression": expr,
            "verdict": verdict,
        })

    # Collapse status across CWEs
    distinct_statuses = {p["status"] for p in per_cwe}
    if distinct_statuses == {"ok"}:
        combined_status = "ok"
    elif len(distinct_statuses) == 1:
        combined_status = next(iter(distinct_statuses))
    else:
        combined_status = "mixed"

    ok_sub = [p for p in per_cwe if p["status"] == "ok"]

    if ok_sub:
        # Use first OK CWE's expression for the primary derivation.
        # (Multi-CWE KEV entries are rare; when they occur we still surface
        # all contributing clusters in clusterSet.)
        primary_sub = ok_sub[0]
        expr = primary_sub["expression"]
        record["derivedMappingExpression"] = expr
        record["primaryCluster"] = primary_from_expression(expr)

        # clusterSet: dedup'd union of every cluster referenced by any OK CWE
        tokens = []
        for p in ok_sub:
            tokens.extend(tokenize_expression(p["expression"]))
        # Stable dedup
        seen = set()
        dedup = []
        for t in tokens:
            if t not in seen:
                seen.add(t)
                dedup.append(t)
        record["clusterSet"] = dedup

        # R-ROLE disambiguation on the PRIMARY expression only
        if has_ambiguous_role(expr):
            role, notes = apply_heuristic(vendor, product, heuristic_rules)
            if role:
                record["primaryCluster"] = role
                record["contextResolvedBy"] = "product-heuristic"
                record["contextHeuristicNotes"] = notes
            else:
                # No heuristic rule matched -> fallback to left-most alt
                record["contextResolvedBy"] = "unresolved"
        else:
            record["contextResolvedBy"] = "cwe-unambiguous"

        verdicts = [p["verdict"] for p in ok_sub if p["verdict"]]
        record["confidence"] = weakest_verdict(verdicts)
    else:
        record["confidence"] = "n/a"
        record["contextResolvedBy"] = "unresolved"

    record["derivationStatus"] = combined_status

    # Keep per-CWE trace for auditability
    record["sourceCweTrace"] = per_cwe
    return record


def compute_stats(records, catalog_meta):
    total = len(records)
    by_status = Counter(r["derivationStatus"] for r in records)
    by_confidence = Counter(r.get("confidence") or "n/a" for r in records)

    # Ransomware-flagged
    ransomware = [r for r in records if r["knownRansomwareCampaignUse"] == "Known"]
    ransomware_count = len(ransomware)

    # By primary cluster (OK only)
    ok_records = [r for r in records if r["derivationStatus"] == "ok"]
    by_primary_all = Counter(r["primaryCluster"] for r in ok_records if r["primaryCluster"])
    by_primary_ransomware = Counter(
        r["primaryCluster"] for r in ok_records
        if r["primaryCluster"] and r["knownRansomwareCampaignUse"] == "Known"
    )

    # SEGMENTED stats: exclude low-confidence to show whether top-line numbers
    # are dominated by CWE-20-class abstractions.
    ok_strong = [
        r for r in ok_records
        if r.get("confidence") in ("Allowed", "Allowed-with-Review")
    ]
    by_primary_strong = Counter(r["primaryCluster"] for r in ok_strong if r["primaryCluster"])
    by_primary_strong_ransomware = Counter(
        r["primaryCluster"] for r in ok_strong
        if r["primaryCluster"] and r["knownRansomwareCampaignUse"] == "Known"
    )

    # Top-N vendors per cluster
    vendors_per_cluster = defaultdict(Counter)
    for r in ok_records:
        if r["primaryCluster"]:
            vendors_per_cluster[r["primaryCluster"]][r["vendorProject"]] += 1
    top_vendors = {
        c: counter.most_common(10)
        for c, counter in vendors_per_cluster.items()
    }

    # Monthly dateAdded histogram per cluster
    month_hist = defaultdict(Counter)
    for r in ok_records:
        c = r["primaryCluster"]
        d = r["dateAdded"]
        if c and d and len(d) >= 7:
            month = d[:7]  # YYYY-MM
            month_hist[c][month] += 1
    monthly_by_cluster = {c: dict(sorted(cnt.items())) for c, cnt in month_hist.items()}

    # Context resolution stats (how many R-ROLE ties the heuristic resolved)
    by_context = Counter(r.get("contextResolvedBy") or "n/a" for r in records)

    # CWE absence / abstraction detail
    ambiguous_records = [r for r in ok_records if r.get("contextResolvedBy") == "product-heuristic"]
    unresolved_role = [r for r in ok_records if r.get("contextResolvedBy") == "unresolved"]

    return {
        "metadata": {
            "generated_from_catalog_version": catalog_meta.get("catalogVersion"),
            "catalog_date_released": catalog_meta.get("dateReleased"),
            "total_records": total,
            "caveat": "Counts below reflect the experimental AI-generated CWE mapping. Always read segmented-by-confidence numbers before acting on aggregates.",
        },
        "by_derivation_status": dict(by_status),
        "by_confidence": dict(by_confidence),
        "ransomware": {
            "total_known_ransomware_cves": ransomware_count,
            "as_percentage_of_catalog": round(100.0 * ransomware_count / total, 2) if total else 0.0,
        },
        "by_primary_cluster": {
            "all_ok": dict(sorted(by_primary_all.items())),
            "strong_confidence_only": dict(sorted(by_primary_strong.items())),
        },
        "by_primary_cluster_ransomware": {
            "all_ok": dict(sorted(by_primary_ransomware.items())),
            "strong_confidence_only": dict(sorted(by_primary_strong_ransomware.items())),
        },
        "top_vendors_per_cluster": top_vendors,
        "monthly_histogram_per_cluster": monthly_by_cluster,
        "context_resolution": {
            "by_method": dict(by_context),
            "heuristic_resolved_count": len(ambiguous_records),
            "r_role_unresolved_count": len(unresolved_role),
        },
    }


def sort_records(records):
    # Deterministic order: dateAdded DESC, then cveID ASC.
    return sorted(records, key=lambda r: (r["dateAdded"] or "", r["cveID"]), reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Generate TLCTC KEV mapping.")
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch live CISA feed instead of using the pinned in-tree snapshot. Never use in CI.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_KEV_INPUT,
        help=f"Path to pinned KEV JSON (default: {DEFAULT_KEV_INPUT.relative_to(ROOT)})",
    )
    parser.add_argument(
        "--out-mapping",
        type=Path,
        default=OUTPUT_KEV,
    )
    parser.add_argument(
        "--out-stats",
        type=Path,
        default=OUTPUT_STATS,
    )
    args = parser.parse_args()

    if args.fetch:
        kev = fetch_live_kev()
    else:
        kev = load_json(args.input)

    cwe_mapping = load_json(CWE_MAPPING)
    cwe_index = build_cwe_index(cwe_mapping)

    heuristic = load_json(HEURISTIC)
    heuristic_rules = heuristic["rules"]

    vulns = kev.get("vulnerabilities", [])
    records = [derive_entry(v, cwe_index, heuristic_rules) for v in vulns]

    # Preserve KEV's own order; don't re-sort. Keeps byte-for-byte diffs minimal
    # between successive runs. (If input is stable, output is stable.)
    output = {
        "metadata": {
            "title": "TLCTC KEV Mapping (CISA Known Exploited Vulnerabilities -> TLCTC)",
            "description": "Per-CVE TLCTC cluster derivation from CISA KEV, via CVE -> CWE -> TLCTC traversal with R-ROLE disambiguation.",
            "tlctc_version": "2.3",
            "source_catalog_version": kev.get("catalogVersion"),
            "source_date_released": kev.get("dateReleased"),
            "total_entries": len(records),
            "derived_from": {
                "kev_snapshot": str(args.input.relative_to(ROOT)) if not args.fetch else KEV_LIVE_URL,
                "cwe_mapping": str(CWE_MAPPING.relative_to(ROOT)),
                "product_role_heuristic": str(HEURISTIC.relative_to(ROOT)),
                "cwe_mapping_ai_generated": True,
                "cwe_mapping_experimental": True,
            },
            "license": "CC-BY-4.0",
            "publisher": "TLCTC Project",
            "caveats": [
                "Every row is derived mechanically from the experimental, AI-generated CWE->TLCTC mapping. Per-row confidence is the source CWE's mappingVerdict (weakest across multiple CWEs).",
                "R-ROLE disambiguation is rule-based (product-role-heuristic.json). When no rule fires for a '#2 | #3' ambiguity, contextResolvedBy = 'unresolved'.",
                "derivationStatus enumerates four orthogonal failure modes; do not collapse into a single score."
            ],
            "schema": {
                "derivationStatus": [
                    "ok -- primary cluster derived from at least one mapped CWE",
                    "cwe-missing -- KEV entry has no CWE references",
                    "cwe-too-abstract -- source CWE's tlctcMapping is N/A or its verdict is Discouraged/Prohibited",
                    "cwe-unmapped-in-tlctc -- CWE is not in tlctc-cwe.json",
                    "mixed -- multiple source CWEs with heterogeneous statuses"
                ],
                "contextResolvedBy": [
                    "cwe-unambiguous -- source CWE is not '#2 | #3'",
                    "product-heuristic -- ambiguity resolved by a rule in product-role-heuristic.json",
                    "unresolved -- no heuristic rule matched; primaryCluster is the left-most alternative as fallback"
                ],
                "confidence": "inherited from source CWE's mappingVerdict; weakest across multiple CWEs",
            }
        },
        "entries": records,
    }

    stats = compute_stats(records, kev)

    args.out_mapping.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.out_stats.write_text(
        json.dumps(stats, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Print a tiny summary to stderr for human operators
    print(f"Wrote {len(records)} records to {args.out_mapping.relative_to(ROOT)}", file=sys.stderr)
    print(f"Wrote stats to {args.out_stats.relative_to(ROOT)}", file=sys.stderr)
    print(f"  by_derivation_status: {stats['by_derivation_status']}", file=sys.stderr)
    print(f"  ransomware: {stats['ransomware']['total_known_ransomware_cves']} / {len(records)}", file=sys.stderr)


if __name__ == "__main__":
    main()
