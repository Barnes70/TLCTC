---
type: "term"
title: "Tie-Breaker Rules"
description: "Precedence rules applied when a step appears to fit multiple clusters."
resource: "tlctc:term:tie-breaker-rules"
tags:
  - "glossary"
---
# Tie-Breaker Rules

Precedence rules applied when a step appears to fit multiple clusters. Applied in order: (1) classify by initial generic vulnerability, (2) implementation flaw vs legitimate function misuse, (3) credential use always wins for the use step, (4) MitM starts at controlled position, (5) flooding is about capacity, (6) FEC execution must be explicit, (7) human/physical/third-party are not shortcuts, (8) document non-obvious decisions.

**Reference:** §4.2.6 (Tie-Breaker / Precedence Rules)
