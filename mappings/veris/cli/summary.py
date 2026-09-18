"""Aggregate classification results into the study's tables.

Every cell is {"n": count, "denominator": count} so the numbers travel with their base.
`summarize` works on a list of `classify()` results only; strata are made by the caller
by passing subsets.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations

CLUSTERS = [f"#{i}" for i in range(1, 11)]
CATEGORIES = ("hacking", "malware", "social", "misuse", "physical", "error", "environmental")
AVAILABILITY_VALUES = ("Loss", "Destruction", "Obscuration", "Interruption", "Degradation", "Acceleration", "Other", "Unknown")
AVAILABILITY_DRE = {"Loss": "Av", "Destruction": "Av", "Obscuration": "Ac", "Interruption": "A", "Degradation": "A", "Acceleration": "A", "Other": "A", "Unknown": "A"}
RANSOMWARE = "action.malware.variety.Ransomware"
DISCLOSURE_YES = "attribute.confidentiality.data_disclosure.Yes"

# Ordering hypotheses for co-occurring clusters, from the companion rules:
# #7 and #4 need a step before them (R-EXEC, R-CRED); #9 needs a step after it.
NEEDS_BEFORE = {"#7", "#4"}
NEEDS_AFTER = {"#9"}


def cell(n: int, d: int) -> dict:
    return {"n": n, "denominator": d}


def pair_hypothesis(a: str, b: str) -> str:
    if a in NEEDS_AFTER and b not in NEEDS_AFTER:
        return f"{a} → {b}"
    if b in NEEDS_AFTER and a not in NEEDS_AFTER:
        return f"{b} → {a}"
    if a in NEEDS_BEFORE and b not in NEEDS_BEFORE:
        return f"{b} → {a}"
    if b in NEEDS_BEFORE and a not in NEEDS_BEFORE:
        return f"{a} → {b}"
    if {a, b} == {"#4", "#7"}:
        return "#4 → #7 | #7 → #4"
    return "order unknown"


def summarize(results: list[dict]) -> dict:
    total = len(results)
    threat = [r for r in results if r["threat_bearing"]]
    nt = len(threat)

    # 1. purity
    no_cluster_only = [r for r in results if r["off_axis_only"]]
    rows_of = lambda r: {x for x in r["partition_rows"] if x != "attack"}
    purity = {
        "records": cell(total, total),
        "threat_bearing": cell(nt, total),
        "threat_only": cell(sum(1 for r in threat if not rows_of(r)), total),
        "mixed_threat_and_operational": cell(sum(1 for r in results if r["mixed"]), total),
        "operational_only": cell(len(no_cluster_only), total),
        "operational_only.error_or_failure": cell(sum(1 for r in no_cluster_only if rows_of(r) <= {"error_in_use", "failure"} and rows_of(r)), total),
        "operational_only.abuse_of_rights": cell(sum(1 for r in no_cluster_only if rows_of(r) == {"abuse_of_rights"}), total),
        "operational_only.other_mix": cell(sum(1 for r in no_cluster_only if rows_of(r) and not rows_of(r) <= {"error_in_use", "failure"} and rows_of(r) != {"abuse_of_rights"}), total),
        "out_of_scope_only": cell(sum(1 for r in no_cluster_only if not rows_of(r)), total),
        "unknown_only": cell(sum(1 for r in results if not r["threat_bearing"] and not r["off_axis_only"] and r["unresolved"]), total),
        "empty": cell(sum(1 for r in results if not r["threat_bearing"] and not r["off_axis_only"] and not r["unresolved"]), total),
    }

    # 2. recoverability (denominator: threat-bearing records)
    def lost(r, cluster=None, side=None):
        return any(c["missing"] and (cluster is None or c["cluster"] == cluster) and (side is None or c["missing"] == side) for c in r["chains"])

    lower_sizes = [len(r["clusters"]["certain"]) for r in threat]
    upper_sizes = [len(r["clusters_upper"]) for r in threat]
    recoverability = {
        "threat_bearing": cell(nt, nt),
        "resolved": cell(sum(1 for r in threat if not r["clusters"]["one_of"] and not lost(r)), nt),
        "rule_dependent": cell(sum(1 for r in threat if r["clusters"]["one_of"]), nt),
        "cause_lost": cell(sum(1 for r in threat if lost(r)), nt),
        "cause_lost.malware_without_enabler": cell(sum(1 for r in threat if lost(r, "#7", "before")), nt),
        "cause_lost.credential_use_without_acquisition": cell(sum(1 for r in threat if lost(r, "#4", "before")), nt),
        "cause_lost.social_without_follow_on": cell(sum(1 for r in threat if lost(r, "#9", "after")), nt),
        "cause_lost.interception_without_position": cell(sum(1 for r in threat if lost(r, "#5", "before")), nt),
        "single_cluster_records": cell(sum(1 for r in threat if len(r["clusters_upper"]) == 1), nt),
        "multi_cluster_records": cell(sum(1 for r in threat if len(r["clusters_upper"]) >= 2), nt),
        "mean_clusters_lower_bound": round(sum(lower_sizes) / nt, 3) if nt else None,
        "mean_clusters_upper_bound": round(sum(upper_sizes) / nt, 3) if nt else None,
    }

    # 3. frequency and co-occurrence
    cert = Counter()
    upp = Counter()
    for r in results:
        for c in r["clusters"]["certain"]:
            cert[c] += 1
        for c in r["clusters_upper"]:
            upp[c] += 1
    frequency = {c: {"certain": cell(cert[c], total), "upper": cell(upp[c], total)} for c in CLUSTERS}
    pairs = Counter()
    for r in results:
        for a, b in combinations(r["clusters"]["certain"], 2):
            pairs[(a, b)] += 1
    cooccurrence = {
        "records_with_two_or_more_certain": cell(sum(1 for r in results if len(r["clusters"]["certain"]) >= 2), total),
        "matrix": {f"{a}|{b}": pairs[(a, b)] for a, b in combinations(CLUSTERS, 2)},
        "top_pairs": [
            {"pair": f"{a} + {b}", "n": n, "hypothesis": pair_hypothesis(a, b)}
            for (a, b), n in sorted(pairs.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
        ],
    }

    # 4. availability: Av versus Ac
    av_values = Counter()
    for r in results:
        for i in r["items"]:
            if i.startswith("attribute.availability.variety."):
                av_values[i.rsplit(".", 1)[1]] += 1
    dre_codes = Counter()
    for r in results:
        for d in r["dre"]:
            dre_codes[d] += 1
    ransom = [r for r in results if RANSOMWARE in r["items"]]
    nr = len(ransom)
    def ransom_with(value):
        return sum(1 for r in ransom if f"attribute.availability.variety.{value}" in r["items"])
    availability = {
        "records_with_availability_attribute": cell(sum(1 for r in results if any(i.startswith("attribute.availability.variety.") for i in r["items"])), total),
        "varieties": {v: {"n": av_values[v], "denominator": total, "dre": AVAILABILITY_DRE[v]} for v in AVAILABILITY_VALUES},
        "dre_codes": {d: cell(dre_codes[d], total) for d in ("C", "I", "Ii", "If", "A", "Av", "Ac")},
        "ransomware": {
            "records": cell(nr, total),
            "with_obscuration_Ac": cell(ransom_with("Obscuration"), nr),
            "with_loss_Av": cell(ransom_with("Loss"), nr),
            "with_destruction_Av": cell(ransom_with("Destruction"), nr),
            "with_interruption_A": cell(ransom_with("Interruption"), nr),
            "with_no_availability_attribute": cell(sum(1 for r in ransom if not any(i.startswith("attribute.availability.variety.") for i in r["items"])), nr),
            "with_confirmed_disclosure_C": cell(sum(1 for r in ransom if DISCLOSURE_YES in r["items"]), nr),
        },
    }

    # 5. unknown collapse
    def has_value(r, cat, value):
        return f"action.{cat}.variety.{value}" in r["items"]
    unknown = {
        "action_unknown": cell(sum(1 for r in results if "action.unknown" in r["items"]), total),
        "any_unresolved_item": cell(sum(1 for r in results if r["unresolved"]), total),
        "unknown_only": purity["unknown_only"],
        "per_category": {
            cat: {
                "records": cell(sum(1 for r in results if any(i.startswith(f"action.{cat}.") for i in r["items"])), total),
                "variety_unknown": cell(sum(1 for r in results if has_value(r, cat, "Unknown")), total),
                "variety_other": cell(sum(1 for r in results if has_value(r, cat, "Other")), total),
            }
            for cat in CATEGORIES
        },
        "unmapped_values": cell(sum(1 for r in results if r["unmapped"]), total),
    }

    return {
        "records": total,
        "purity": purity,
        "recoverability": recoverability,
        "frequency": frequency,
        "cooccurrence": cooccurrence,
        "availability": availability,
        "unknown": unknown,
    }


def _pct(c: dict) -> str:
    d = c["denominator"]
    return f"{c['n']} ({100.0 * c['n'] / d:.1f}%)" if d else f"{c['n']} (–)"


def render_md(summary: dict, title: str = "Summary") -> str:
    s = summary
    out = [f"### {title}", "", f"Records: {s['records']}", ""]
    out += ["| Threat-axis purity | n (% of records) |", "|---|---|"]
    for k, v in s["purity"].items():
        out.append(f"| {k} | {_pct(v)} |")
    out += ["", "| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |", "|---|---|"]
    for k, v in s["recoverability"].items():
        out.append(f"| {k} | {_pct(v) if isinstance(v, dict) else v} |")
    out += ["", "| Cluster | certain | upper bound |", "|---|---|---|"]
    for c, v in s["frequency"].items():
        out.append(f"| {c} | {_pct(v['certain'])} | {_pct(v['upper'])} |")
    out += ["", f"Records with two or more certain clusters: {_pct(s['cooccurrence']['records_with_two_or_more_certain'])}", "", "| Pair | n | ordering hypothesis |", "|---|---|---|"]
    for p in s["cooccurrence"]["top_pairs"]:
        out.append(f"| {p['pair']} | {p['n']} | {p['hypothesis']} |")
    out += ["", "| attribute.availability.variety | n | DRE |", "|---|---|---|"]
    for k, v in s["availability"]["varieties"].items():
        out.append(f"| {k} | {v['n']} | {v['dre']} |")
    out += ["", "| Ransomware records | n (% of ransomware) |", "|---|---|"]
    for k, v in s["availability"]["ransomware"].items():
        out.append(f"| {k} | {_pct(v)} |")
    out += ["", "| Unknown collapse | n (% of records) |", "|---|---|"]
    for k, v in s["unknown"].items():
        if isinstance(v, dict) and "n" in v:
            out.append(f"| {k} | {_pct(v)} |")
    out += ["", "| Category | records | variety Unknown | variety Other |", "|---|---|---|---|"]
    for cat, v in s["unknown"]["per_category"].items():
        out.append(f"| {cat} | {_pct(v['records'])} | {_pct(v['variety_unknown'])} | {_pct(v['variety_other'])} |")
    if "attack_agreement" in s:
        out += ["", "| ATT&CK-transitive agreement | n (% of records) |", "|---|---|"]
        for k, v in s["attack_agreement"]["classes"].items():
            out.append(f"| {k} | {_pct(v)} |")
        out += ["", "| VERIS value | disagreeing records | direct | transitive |", "|---|---|---|---|"]
        for d in s["attack_agreement"]["top_disagreements"]:
            out.append(f"| {d['veris_id']} | {d['n']} | {d['direct']} | {d['transitive']} |")
    out.append("")
    return "\n".join(out)
