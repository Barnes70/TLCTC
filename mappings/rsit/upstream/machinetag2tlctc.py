#!/usr/bin/env python3
"""Render the RSIT -> TLCTC table (rsit_2_tlctc.md) from machinetag.json.

machinetag.json is the RSIT machinev1 taxonomy with one extra field, `tlctc`, on every value
(the way rsit2attck adds `attck`). MISP ignores the field. Standard library only.

Usage: python3 machinetag2tlctc.py machinetag.json rsit_2_tlctc.md
"""
import json
import sys

HEADER = """
# RSIT to TLCTC

Generated from machinetag.json. Please **DO NOT** edit this file directly in github, rather use the machinetag.json file.

RSIT classifies the state of an incident; TLCTC (Top Level Cyber Threat Clusters) classifies its cause.
A machine tag appears only where the RSIT value proves the step happened; other values list candidate clusters
and the question that decides.

| Classification | Incident examples | TLCTC | Description |
|----------------|-------------------|-------|-------------|
"""


def cell(text):
    """Escape a value for a Markdown table cell."""
    return str(text).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def tlctc_cell(elements):
    parts = []
    for el in elements:
        if el.get("machinetag"):
            head = "`%s`" % el["machinetag"]
        elif el.get("candidates"):
            head = " | ".join(el["candidates"])
        elif el.get("mapping_type") == "unresolved":
            head = "?"
        else:
            head = "no cluster"
        parts.append("%s (%s): %s" % (head, el.get("mapping_type", ""), el.get("note", "")))
    return "<br><br>".join(cell(p) for p in parts)


def render(data):
    predicates = {p["value"]: p["expanded"] for p in data["predicates"]}
    lines = [HEADER.lstrip("\n").rstrip("\n")]
    for group in data["values"]:
        for t in group["entry"]:
            lines.append("| %s | %s | %s | %s |" % (
                cell(predicates[group["predicate"]]), cell(t["expanded"]),
                tlctc_cell(t.get("tlctc", [])), cell(t.get("description", ""))))
    return "\n".join(lines) + "\n"


def main(argv):
    if len(argv) != 3:
        print("syntax: %s <machinetag.json> <output.md>" % argv[0], file=sys.stderr)
        return 1
    with open(argv[1], encoding="utf-8") as f:
        data = json.load(f)
    with open(argv[2], "w", encoding="utf-8", newline="\n") as f:
        f.write(render(data))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
