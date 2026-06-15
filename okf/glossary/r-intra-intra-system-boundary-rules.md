---
type: "term"
title: "R-INTRA (Intra-System Boundary Rules)"
description: "The complete intra system boundary rule set governing use of the intra system operator ( |...| ): | Rule | Name | Summary | | | | | | R INTRA 1 | Single System Scope | Operator MUST be used only for boundaries within a single system instance | | R INTRA 2 | Cluster Attachment | Operator MUST be attached to the cluster step that accomplishes the crossing | | R INTRA 3 | No Standalone Use | Operator MUST NOT appear without an associated cluster step | | R INTRA 4 | No Cluster Change | Operator MUST NOT change cluster classification | | R INTRA 5 | Optional Precision | Operator is OPTIONAL; mainly recommended for forensic or vendor facing use | | R INTRA 6 | Multiple Crossings | Multiple annotations MAY follow one step when compressed form is justified | | R INTRA 7 | Distinct Vulnerabilities | If crossing requires a separately evidenced vulnerability, a new cluster step MUST be added | | R INTRA 8 | Compressed Form | If evidence does not distinguish separate exploit causes, compressed single step form MAY be used | | R INTRA 9 | Anti Effect Rule / Memory Deferral | Effects (privilege escalation, sandbox escape, etc.) are NOT independent threat categories; memory boundary type is deferred and MUST NOT be used | Reference: §4.2.5 (R INTRA), §11.3.6 (Intra System Boundary Operator)"
resource: "tlctc:term:r-intra-intra-system-boundary-rules"
tags:
  - "glossary"
---
# R-INTRA (Intra-System Boundary Rules)

The complete intra-system boundary rule set governing use of the intra-system operator (`|...|`):

| Rule | Name | Summary |
|---|---|---|
| **R-INTRA-1** | Single-System Scope | Operator MUST be used only for boundaries within a single system instance |
| **R-INTRA-2** | Cluster Attachment | Operator MUST be attached to the cluster step that accomplishes the crossing |
| **R-INTRA-3** | No Standalone Use | Operator MUST NOT appear without an associated cluster step |
| **R-INTRA-4** | No Cluster Change | Operator MUST NOT change cluster classification |
| **R-INTRA-5** | Optional Precision | Operator is OPTIONAL; mainly recommended for forensic or vendor-facing use |
| **R-INTRA-6** | Multiple Crossings | Multiple annotations MAY follow one step when compressed form is justified |
| **R-INTRA-7** | Distinct Vulnerabilities | If crossing requires a separately evidenced vulnerability, a new cluster step MUST be added |
| **R-INTRA-8** | Compressed Form | If evidence does not distinguish separate exploit causes, compressed single-step form MAY be used |
| **R-INTRA-9** | Anti-Effect Rule / Memory Deferral | Effects (privilege escalation, sandbox escape, etc.) are NOT independent threat categories; `memory` boundary type is deferred and MUST NOT be used |

**Reference:** §4.2.5 (R-INTRA), §11.3.6 (Intra-System Boundary Operator)
