"""Render the TLCTC attack path notation from a Layer 3 path_sequence.

Grammar used (CLAUDE.md / core paper §11):
  step      := label [boundary] {intra} [dre]
  label     := cluster id as written | '?' (unresolved single) | '…' (unresolved gap)
  boundary  := '||[' context '][' source {'⇒' transit} '→' target ']||'
  intra     := '|[' type '][' from '→' to ']|'
  dre       := '+ [DRE: ' code {', ' code} ']'
  item      := step | '(' step ' + ' step {' + ' step} ')'
  path      := item {connector item}
  connector := ' →[Δt=' delta '] ' | ' → '
The rendering is faithful to the JSON: every step with `outcomes` carries its own DRE tag.
"""
from __future__ import annotations

import re

from cli.layer3 import item_kind

_DRE_RE = re.compile(r"\s*\+\s*\[DRE:[^\]]*\]")


def render_boundary(b: dict) -> str:
    chain = "⇒".join([b["source_sphere"], *b.get("transit_spheres", [])])
    return f"||[{b['context']}][{chain}→{b['target_sphere']}]||"


def render_intra(b: dict) -> str:
    return f"|[{b['type']}][{b['from']}→{b['to']}]|"


def render_step(step: dict) -> str:
    kind = item_kind(step)
    if kind == "unresolved":
        label = "…" if step.get("unresolved_type") == "gap" else "?"
    else:
        label = step["cluster"]
    parts = [label]
    if step.get("topology_boundary"):
        parts.append(render_boundary(step["topology_boundary"]))
    for b in step.get("intra_system_boundaries") or []:
        parts.append(render_intra(b))
    if kind == "step" and step.get("outcomes"):
        parts.append(f"+ [DRE: {', '.join(step['outcomes'])}]")
    return " ".join(parts)


def render_item(item: dict) -> str:
    if item_kind(item) == "group":
        return "(" + " + ".join(render_step(s) for s in item["steps"]) + ")"
    return render_step(item)


def render_path(sequence: list) -> str:
    out = []
    for i, item in enumerate(sequence):
        out.append(render_item(item))
        if i < len(sequence) - 1:
            dt = item.get("delta_t_to_next")
            out.append(f"→[Δt={dt}]" if dt else "→")
    return " ".join(out)


def strip_dre(notation: str) -> str:
    return _DRE_RE.sub("", notation)
