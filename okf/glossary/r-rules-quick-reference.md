---
type: "term"
title: "R-* Rules Quick Reference"
description: "The v2.5 normative registry contains exactly 18 rules : eight core rules and ten v2.1 extension rules."
resource: "tlctc:term:r-rules-quick-reference"
tags:
  - "glossary"
---
# R-* Rules Quick Reference

The v2.5 normative registry contains exactly **18 rules**: eight core rules and ten v2.1 extension rules. This table mirrors the canonical dictionary (`tlctc-framework.v2.5.json`); summaries are condensed, the dictionary statement governs.

**Core rules (8):**

| Rule | Distinguishes | Key Decision |
| --- | --- | --- |
| **R-EXEC** | FEC Execution | If FEC executes → `#7` MUST be recorded (plus enabling cluster) |
| **R-ROLE** | `#2` vs `#3` | Server-role (accepts inbound) → `#2`; Client-role (consumes external) → `#3`; roles set by call direction at any interface, network not required |
| **R-FLOOD** | Capacity vs Defect | Volume exhaustion → `#6`; Implementation defect → `#2/#3` per R-ROLE |
| **R-SUPPLY** | TAE Placement | `#10` at Trust Acceptance Event where third-party trust is honored |
| **R-MITM** | Position vs Action | Gaining position → enabling cluster; Interception/modification/relay → `#5` |
| **R-CHANNEL** *(v2.5)* | Control vs Code Flaw | Defective logic constitutive of channel control → `#5`; Incidental defect → `#2/#3` |
| **R-SUBSTRATE** *(v2.5)* | Property vs Logic | Physical property exploited → `#8`; Physical layer as readout only → `#2/#3` |
| **R-CRED** | Acquisition vs Use | Acquisition → enabling cluster; Use → always `#4` (unless the identity is the presenter's own — self-issued enrolment is `#1`); separate steps |

**v2.1 extension rules (10):**

| Rule | Distinguishes | Key Decision |
| --- | --- | --- |
| **R-TRANSIT-3** *(V2.1)* | Transit vs Attack Surface | Vendor code on target device → classify by R-ROLE, not transit |
| **R-INTRA-7** *(V2.1)* | Annotation vs Classification | Intra-system crossings never change cluster classification |
| **R-INTRA-9** *(V2.1)* | Memory Deferral | `memory` boundary type deferred → MUST NOT use |
| **R-UNRES-2** *(V2.1)* | Annotation vs Cluster | `?`/`…` are epistemic annotations, not clusters (no `#11`/`#12`) |
| **R-UNRES-3** *(V2.1)* | Statistics | `?`/`…` excluded from statistics |
| **R-UNRES-5** *(V2.1)* | No DRE on Unresolved | DRE tags MUST NOT be appended to `?` or `…` |
| **R-UNRES-6** *(V2.1)* | Boundary Compatibility | Boundary operators MAY appear adjacent to `?`/`…` |
| **R-UNRES-7** *(V2.1)* | Resolution Obligation | Every `?`/`…` is an open analytical task → resolve when evidence arrives |
| **R-UNRES-8** *(V2.1)* | Prose Required | Paths containing `?`/`…` MUST have prose annotation explaining gap |
| **R-UNRES-9** *(V2.1)* | Classification Threshold | If any cluster can be defended → use `#X [conf=low]`, not `?` |

**Deprecated / withdrawn rule IDs (do not cite as normative):**

| ID | Status | Where the substance lives now |
| --- | --- | --- |
| **R-ABUSE** | Deprecated v2.0 alias | #1 cluster definition and boundary tests (core §4) |
| **R-HUMAN** | Deprecated v2.0 alias | #9 cluster definition and boundary tests (core §4) |
| **R-PHYSICAL** | Deprecated v2.0 alias | #8 boundary tests (core §4) + R-SUBSTRATE (admission) |
| **R-TRANSIT-1/2/4/5/6/7/8** | Withdrawn v2.1 draft series | Non-normative transit notation practice (see R-TRANSIT entry); cluster independence is SG-2 |
| **R-INTRA-1…6, -8** | Withdrawn v2.1 draft series | Non-normative intra-system notation practice (see R-INTRA entry) |
| **R-UNRES-1, -4** | Consolidated during v2.1 finalization | R-UNRES-1 → R-UNRES-2; draft R-UNRES-4's threshold → canonical R-UNRES-9 |

> **Caution:** the draft series numbered some propositions differently than the canon (draft R-INTRA-7 = "distinct vulnerabilities", canonical R-INTRA-7 = "no cluster change"; draft R-UNRES-4 = the conf=low threshold, canonical R-UNRES-9). Always cite the canonical registry above.
