---
type: "term"
title: "Unresolved-Step Operators (`?`, `…`)"
description: "Notation operators for partially resolved attack paths where forensic evidence confirms that a step (or gap of steps) exists but the cluster cannot yet be determined."
resource: "tlctc:term:unresolved-step-operators"
tags:
  - "glossary"
---
# Unresolved-Step Operators (`?`, `…`)

Notation operators for partially-resolved attack paths where forensic evidence confirms that a step (or gap of steps) exists but the cluster cannot yet be determined. `?` represents exactly one unresolved step; `…` (or ASCII `...`) represents a gap of one or more steps. Governed by the seven canonical R-UNRES rules (2, 3, 5, 6, 7, 8, 9 — the numbering is intentionally non-contiguous; draft rules 1 and 4 were consolidated into adjacent rules during v2.1 finalization). Key constraints: unresolved steps MUST NOT carry DRE tags (R-UNRES-5); if any cluster can be defended even weakly, the step MUST be classified as `#X [conf=low]` rather than left unresolved (R-UNRES-9); every unresolved step MUST be accompanied by a prose annotation (R-UNRES-8).

**Reference:** §11.5.4 (Unresolved-Step Operators)
