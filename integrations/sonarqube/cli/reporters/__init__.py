"""Report writers for ClassifiedFinding lists.

Each module exports a `render(findings, summary, **meta) -> str | bytes`
function. They are intentionally side-effect-free; the caller writes to disk.
"""
