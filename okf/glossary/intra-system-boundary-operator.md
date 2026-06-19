---
type: "term"
title: "Intra-System Boundary Operator (|...|)"
description: "Notation: |[type][@from→@to]| ."
resource: "tlctc:term:intra-system-boundary-operator"
tags:
  - "glossary"
---
# Intra-System Boundary Operator (|...|)

Notation: `|[type][@from→@to]|`. Used to annotate boundary crossings **within a single host or system**, such as sandbox escapes, privilege escalations, process boundary violations, and VM escapes. Uses single pipe delimiters to distinguish from the inter-sphere Domain Boundary Operator (`||...||`). Defined boundary types: `sandbox`, `privilege`, `process`, `hypervisor`. The `memory` type is reserved and MUST NOT be used (R-INTRA-9). Intra-system boundaries are observability annotations and never change cluster classification (R-INTRA-7). Example: `#3 |[sandbox][@renderer→@os]|` — browser exploit escaping renderer sandbox.

**Reference:** §11.3.6 (Intra-System Boundary Operator)

---
