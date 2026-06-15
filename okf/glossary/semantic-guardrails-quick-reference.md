---
type: "term"
title: "Semantic Guardrails Quick Reference"
description: "| ID | Rule | Key Constraint | | | | | | SG 1 | Cause First | Classify by generic vulnerability exploited, not topology or effect | | SG 2 | Topology ≠ Classification | Transit/intra system annotations MUST NOT define or imply a cluster | | SG 3 | Annotations Subordinate | Annotations MUST NOT appear as independent path elements or replace clusters | | SG 4 | Effects ≠ Threats | Sandbox escape, privilege escalation, etc."
resource: "tlctc:term:semantic-guardrails-quick-reference"
tags:
  - "glossary"
---
# Semantic Guardrails Quick Reference

| ID | Rule | Key Constraint |
| --- | --- | --- |
| **SG-1** | Cause First | Classify by generic vulnerability exploited, not topology or effect |
| **SG-2** | Topology ≠ Classification | Transit/intra-system annotations MUST NOT define or imply a cluster |
| **SG-3** | Annotations Subordinate | Annotations MUST NOT appear as independent path elements or replace clusters |
| **SG-4** | Effects ≠ Threats | Sandbox escape, privilege escalation, etc. are not TLCTC clusters |
| **SG-5** | Actors ≠ Threats | Transit parties, vendors, carriers are spheres, not threat categories |
| **SG-6** | Distinct Exploit Rule | Separately evidenced exploit → new cluster step required |
| **SG-7** | Backward Recoverability | Stripping V2.1 annotations MUST leave a valid cluster sequence |

**Reference:** §4.2.4 (Semantic Guardrails), §4.2.5 (Global Mapping Rules)
