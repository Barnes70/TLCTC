"""Classify an Attack Flow: every action through the ATT&CK → TLCTC mapping, then a derived TLCTC path.

The derived path is a classification report, not a Layer 3 record: it follows the flow's own order,
renders rule-dependent actions as `?` with candidates, leaves attacker-side preparation (N/A) out of
the path, and computes Δt only where two adjacent actions both carry execution_start.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime

from .flow import Flow
from .mapping import AttackMapping

CLUSTERS = [f"#{i}" for i in range(1, 11)]


def _parse_ts(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def fmt_delta(seconds: float) -> str:
    s = abs(seconds)
    if s < 60:
        return f"{int(s)}s"
    if s < 3600:
        return f"{int(s // 60)}m"
    if s < 86400:
        return f"{int(s // 3600)}h"
    return f"{int(s // 86400)}d"


def classify_actions(flow: Flow, mapping: AttackMapping) -> dict[str, dict]:
    out = {}
    for aid, a in flow.actions.items():
        r = mapping.lookup(a.technique_id)
        out[aid] = {
            "action_id": aid, "name": a.name, "technique_id": a.technique_id, "tactic_id": a.tactic_id,
            "status": r["status"], "technique_used": r["technique_used"], "mapping": r["raw"], "framework": r.get("framework"),
            "alternatives": r["alternatives"],
            "clusters_certain": r["alternatives"][0] if r["status"] == "resolved" else [],
            "clusters_candidates": sorted({c for alt in r["alternatives"] for c in alt}, key=lambda s: int(s[1:])) if r["status"] == "rule_dependent" else [],
            "attachments": flow.attachments.get(aid, []),
        }
    return out


def derive_path(flow: Flow, per_action: dict[str, dict]) -> dict:
    """Walk the flow in topological order and build the raw and compressed step lists."""
    order = flow.topological_order()
    raw: list[dict] = []
    alternatives_notes: list[str] = []
    parallel_hint: set[str] = set()   # actions that are direct successors of an AND operator
    for op in flow.operators.values():
        if op.operator == "AND":
            for dst, _ in flow.successors(op.id):
                if dst in flow.actions:
                    parallel_hint.add(dst)
    for n in order:
        if n in flow.conditions:
            falses = [d for d, l in flow.successors(n) if l == "false"]
            if falses:
                alternatives_notes.append(f"condition '{flow.conditions[n].description[:60]}' has a false branch ({len(falses)} node(s)) not followed")
            continue
        if n in flow.operators:
            if flow.operators[n].operator == "OR":
                alternatives_notes.append(f"OR operator with {len(flow.successors(n))} alternatives; all listed in order")
            continue
        r = per_action[n]
        a = flow.actions[n]
        if r["status"] == "resolved":
            for i, c in enumerate(r["alternatives"][0]):
                raw.append({"action_id": n, "cluster": c, "kind": "classified", "implied": i > 0, "parallel_hint": n in parallel_hint and i == 0, "execution_start": a.execution_start})
        elif r["status"] == "rule_dependent":
            raw.append({"action_id": n, "cluster": None, "kind": "unresolved", "candidates": r["clusters_candidates"], "parallel_hint": n in parallel_hint, "execution_start": a.execution_start})
        elif r["status"] in ("no_technique", "unmapped"):
            raw.append({"action_id": n, "cluster": None, "kind": "unresolved", "candidates": [], "reason": r["status"], "parallel_hint": n in parallel_hint, "execution_start": a.execution_start})
        else:  # preparation: outside the path
            continue
    # Δt between consecutive raw steps where both actions have timestamps
    for i in range(len(raw) - 1):
        t0, t1 = _parse_ts(raw[i]["execution_start"]), _parse_ts(raw[i + 1]["execution_start"])
        if t0 and t1 and raw[i]["action_id"] != raw[i + 1]["action_id"]:
            raw[i]["delta_t_to_next"] = fmt_delta((t1 - t0).total_seconds())
    # compressed: consecutive classified steps with the same cluster collapse
    compressed: list[dict] = []
    for s in raw:
        if compressed and s["kind"] == "classified" and compressed[-1]["kind"] == "classified" and compressed[-1]["cluster"] == s["cluster"]:
            compressed[-1]["count"] += 1
            compressed[-1]["action_ids"].append(s["action_id"])
            if s.get("delta_t_to_next"):
                compressed[-1]["delta_t_to_next"] = s["delta_t_to_next"]
            continue
        if compressed and s["kind"] == "unresolved" and compressed[-1]["kind"] == "unresolved" and compressed[-1].get("candidates") == s.get("candidates"):
            compressed[-1]["count"] += 1
            compressed[-1]["action_ids"].append(s["action_id"])
            continue
        c = {k: v for k, v in s.items() if k != "action_id"}
        c["count"] = 1
        c["action_ids"] = [s["action_id"]]
        compressed.append(c)
    return {"raw": raw, "compressed": compressed, "notes": alternatives_notes, "has_cycle": flow.has_cycle()}


def render_notation(steps: list[dict]) -> str:
    """`#N` for a classified step, `?` for one unresolved action, `…` for a run of several unresolved actions (a gap)."""
    parts = []
    for i, s in enumerate(steps):
        if s["kind"] == "classified":
            token = s["cluster"]
        else:
            token = "…" if s.get("count", 1) > 1 else "?"
        parts.append(token)
        if i < len(steps) - 1:
            dt = s.get("delta_t_to_next")
            parts.append(f"→[Δt={dt}]" if dt else "→")
    return " ".join(parts)


def classify_flow(flow: Flow, mapping: AttackMapping) -> dict:
    per_action = classify_actions(flow, mapping)
    path = derive_path(flow, per_action)
    statuses = Counter(r["status"] for r in per_action.values())
    certain = sorted({c for r in per_action.values() for c in r["clusters_certain"]}, key=lambda s: int(s[1:]))
    upper = sorted({c for r in per_action.values() for alt in r["alternatives"] for c in alt}, key=lambda s: int(s[1:]))
    first = next((s["cluster"] for s in path["compressed"] if s["kind"] == "classified"), None)
    entry = first
    entry_is_first_step = bool(path["compressed"]) and path["compressed"][0]["kind"] == "classified"
    return {
        "entry_is_first_step": entry_is_first_step,
        "flow": flow.name, "scope": flow.scope, "source": flow.source,
        "counts": {"actions": len(flow.actions), "conditions": len(flow.conditions), "operators": len(flow.operators), "edges": len(flow.edges),
                   "with_technique": sum(1 for a in flow.actions.values() if a.technique_id), "with_execution_start": sum(1 for a in flow.actions.values() if a.execution_start)},
        "action_status": dict(statuses),
        "actions": [per_action[n] for n in flow.topological_order() if n in per_action],
        "clusters_certain": certain, "clusters_upper": upper,
        "entry_cluster": entry, "first_classified_cluster": first,
        "path": path,
        "notation_raw": render_notation(path["raw"]),
        "notation_compressed": render_notation(path["compressed"]),
        "steps_raw": len(path["raw"]), "steps_compressed": len(path["compressed"]),
        "unresolved_steps": sum(1 for s in path["compressed"] if s["kind"] == "unresolved"),
        "delta_t_edges": sum(1 for s in path["raw"] if s.get("delta_t_to_next")),
    }


def transitions(result: dict) -> list[tuple[str, str]]:
    """Ordered cluster pairs along the compressed path (classified steps only, adjacent)."""
    steps = result["path"]["compressed"]
    out = []
    for a, b in zip(steps, steps[1:]):
        if a["kind"] == "classified" and b["kind"] == "classified":
            out.append((a["cluster"], b["cluster"]))
    return out


def cell(n: int, d: int) -> dict:
    return {"n": n, "denominator": d}


def summarize(results: list[dict]) -> dict:
    nf = len(results)
    na = sum(r["counts"]["actions"] for r in results)
    status = Counter()
    for r in results:
        status.update(r["action_status"])
    freq = {c: {"actions_certain": cell(0, na), "actions_upper": cell(0, na), "flows_certain": cell(0, nf), "flows_upper": cell(0, nf)} for c in CLUSTERS}
    for r in results:
        for c in r["clusters_certain"]:
            freq[c]["flows_certain"]["n"] += 1
        for c in r["clusters_upper"]:
            freq[c]["flows_upper"]["n"] += 1
        for a in r["actions"]:
            for c in a["clusters_certain"]:
                freq[c]["actions_certain"]["n"] += 1
            for c in ({x for alt in a["alternatives"] for x in alt}):
                freq[c]["actions_upper"]["n"] += 1
    entry = Counter(r["entry_cluster"] or "?" for r in results)
    trans = Counter()
    for r in results:
        trans.update(transitions(r))
    comp = [(r["counts"]["actions"], r["steps_compressed"]) for r in results]
    return {
        "flows": nf,
        "profile": {
            "flows": cell(nf, nf), "actions": cell(na, na),
            "actions_with_technique": cell(sum(r["counts"]["with_technique"] for r in results), na),
            "actions_with_execution_start": cell(sum(r["counts"]["with_execution_start"] for r in results), na),
            "conditions": sum(r["counts"]["conditions"] for r in results), "operators": sum(r["counts"]["operators"] for r in results),
            "flows_with_cycle": cell(sum(1 for r in results if r["path"]["has_cycle"]), nf),
            "flows_whose_first_step_is_unresolved": cell(sum(1 for r in results if not r["entry_is_first_step"]), nf),
            "actions_with_atlas_technique": cell(sum(1 for r in results for a in r["actions"] if a.get("framework") == "atlas"), na),
            "flows_using_atlas": cell(sum(1 for r in results if any(a.get("framework") == "atlas" for a in r["actions"])), nf),
            "delta_t_edges": cell(sum(r["delta_t_edges"] for r in results), sum(max(r["steps_raw"] - 1, 0) for r in results)),
        },
        "action_status": {k: cell(status.get(k, 0), na) for k in ("resolved", "rule_dependent", "preparation", "unmapped", "no_technique")},
        "frequency": freq,
        "entry_cluster": {k: cell(v, nf) for k, v in sorted(entry.items(), key=lambda kv: (-kv[1], kv[0]))},
        "transitions": [{"from": a, "to": b, "n": n} for (a, b), n in trans.most_common(15)],
        "transition_matrix": {f"{a}|{b}": trans.get((a, b), 0) for a in CLUSTERS for b in CLUSTERS},
        "compression": {
            "actions_total": sum(a for a, _ in comp), "steps_compressed_total": sum(s for _, s in comp),
            "mean_actions_per_step": round(sum(a for a, _ in comp) / max(sum(s for _, s in comp), 1), 2),
            "flows_fully_classified": cell(sum(1 for r in results if r["unresolved_steps"] == 0 and r["steps_compressed"] > 0), nf),
        },
        "per_flow": [
            {"flow": r["flow"], "scope": r["scope"], "actions": r["counts"]["actions"], "steps": r["steps_compressed"], "unresolved": r["unresolved_steps"],
             "entry": r["entry_cluster"] or "?", "notation": r["notation_compressed"], "status": r["action_status"]}
            for r in sorted(results, key=lambda r: r["flow"].lower())
        ],
    }


def render_md(summary: dict, title: str = "Summary") -> str:
    s = summary
    pct = lambda c: f"{c['n']} ({100.0 * c['n'] / c['denominator']:.1f}%)" if c["denominator"] else f"{c['n']} (–)"
    out = [f"### {title}", "", "| Corpus profile | value |", "|---|---|"]
    for k, v in s["profile"].items():
        out.append(f"| {k} | {pct(v) if isinstance(v, dict) else v} |")
    out += ["", "| Action classification outcome | n (% of actions) |", "|---|---|"]
    for k, v in s["action_status"].items():
        out.append(f"| {k} | {pct(v)} |")
    out += ["", "| Cluster | actions certain | actions upper | flows certain | flows upper |", "|---|---|---|---|---|"]
    for c, v in s["frequency"].items():
        out.append(f"| {c} | {pct(v['actions_certain'])} | {pct(v['actions_upper'])} | {pct(v['flows_certain'])} | {pct(v['flows_upper'])} |")
    out += ["", "| Entry cluster | flows |", "|---|---|"]
    for k, v in s["entry_cluster"].items():
        out.append(f"| {k} | {pct(v)} |")
    out += ["", "| Transition | n |", "|---|---|"]
    for t in s["transitions"]:
        out.append(f"| {t['from']} → {t['to']} | {t['n']} |")
    c = s["compression"]
    out += ["", f"Compression: {c['actions_total']} actions → {c['steps_compressed_total']} steps ({c['mean_actions_per_step']} actions per step); flows fully classified: {pct(c['flows_fully_classified'])}", ""]
    out += ["| Flow | scope | actions | steps | ? | entry | derived path (compressed) |", "|---|---|---|---|---|---|---|"]
    for f in s["per_flow"]:
        out.append(f"| {f['flow']} | {f['scope'] or '–'} | {f['actions']} | {f['steps']} | {f['unresolved']} | {f['entry']} | `{f['notation']}` |")
    out.append("")
    return "\n".join(out)
