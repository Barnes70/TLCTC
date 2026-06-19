---
type: "term"
title: "R-* Rules Quick Reference"
description: "| Rule | Distinguishes | Key Decision | | | | | | R ROLE | 2 vs 3 | Server role (accepts inbound) → 2 ; Client role (consumes external) → 3 | | R CRED | Acquisition vs Use | Acquisition → enabling cluster; Use → always 4 | | R MITM | Gaining vs Exploiting | Gaining position → enabling cluster; Exploiting position → 5 | | R FLOOD | Capacity vs Defect | Volume exhaustion → 6 ; Implementation defect → 2/ 3 | | R EXEC | FEC Execution | If FEC executes → 7 MUST be recorded (plus enabling cluster) | | R SUPPLY | TAE Placement | 10 at Trust Acceptance Event where third party trust is honored | | R HUMAN | Human Manipulation | Psychological manipulation → 9 ; subsequent tech steps separate | | R PHYSICAL | Physical Access | Physical interaction → 8 ; subsequent tech steps separate | | R ABUSE | Function Misuse | No flaw required, legitimate capability abused → 1 | | R TRANSIT 1 (V2.1) | Distinct Parties | @Transit MUST be distinct from @Source and @Target | | R TRANSIT 2 (V2.1) | True Intermediary Topology | Operator only when intermediary sits between source and target | | R TRANSIT 3 (V2.1) | Transit vs Attack Surface | Vendor code on target device → classify by R ROLE, not transit | | R TRANSIT 4 (V2.1) | Control Relevance | SHOULD annotate when intermediary has control responsibility | | R TRANSIT 5 (V2.1) | Pure Conduit Fallback | MAY omit transit if intermediary adds no useful control surface | | R TRANSIT 6 (V2.1) | Compromise Separation | Intermediary compromise → preceding cluster step; transit alone insufficient | | R TRANSIT 7 (V2.1) | Cluster Independence | Transit annotation MUST NOT change cluster classification | | R TRANSIT 8 (V2.1) | Multiple Transit Parties | Chained transit MAY be used when each party has independent relevance | | R INTRA 1 (V2.1) | Single System Scope | Operator only for boundaries within a single system instance | | R INTRA 2 (V2.1) | Cluster Attachment | Operator MUST be attached to the cluster step | | R INTRA 3 (V2.1) | No Standalone Use | Operator MUST NOT appear without an associated cluster step | | R INTRA 4 (V2.1) | No Cluster Change | Operator MUST NOT change cluster classification | | R INTRA 5 (V2.1) | Optional Precision | Operator is OPTIONAL; recommended for forensic/vendor facing use | | R INTRA 6 (V2.1) | Multiple Crossings | Multiple annotations MAY follow one step when compressed form justified | | R INTRA 7 (V2.1) | Distinct Vulnerabilities | Separately evidenced vulnerability → new cluster step required | | R INTRA 8 (V2.1) | Compressed Form | Compressed single step MAY be used when evidence doesn't distinguish causes | | R INTRA 9 (V2.1) | Anti Effect / Memory Deferral | Effects are not threats; memory boundary type deferred → MUST NOT use | | R UNRES 1 (V2.1) | Semantic Constraint | ?"
resource: "tlctc:term:r-rules-quick-reference"
tags:
  - "glossary"
---
# R-* Rules Quick Reference

| Rule | Distinguishes | Key Decision |
| --- | --- | --- |
| **R-ROLE** | `#2` vs `#3` | Server-role (accepts inbound) → `#2`; Client-role (consumes external) → `#3` |
| **R-CRED** | Acquisition vs Use | Acquisition → enabling cluster; Use → always `#4` |
| **R-MITM** | Gaining vs Exploiting | Gaining position → enabling cluster; Exploiting position → `#5` |
| **R-FLOOD** | Capacity vs Defect | Volume exhaustion → `#6`; Implementation defect → `#2/#3` |
| **R-EXEC** | FEC Execution | If FEC executes → `#7` MUST be recorded (plus enabling cluster) |
| **R-SUPPLY** | TAE Placement | `#10` at Trust Acceptance Event where third-party trust is honored |
| **R-HUMAN** | Human Manipulation | Psychological manipulation → `#9`; subsequent tech steps separate |
| **R-PHYSICAL** | Physical Access | Physical interaction → `#8`; subsequent tech steps separate |
| **R-ABUSE** | Function Misuse | No flaw required, legitimate capability abused → `#1` |
| **R-TRANSIT-1** *(V2.1)* | Distinct Parties | `@Transit` MUST be distinct from `@Source` and `@Target` |
| **R-TRANSIT-2** *(V2.1)* | True Intermediary Topology | Operator only when intermediary sits between source and target |
| **R-TRANSIT-3** *(V2.1)* | Transit vs Attack Surface | Vendor code on target device → classify by R-ROLE, not transit |
| **R-TRANSIT-4** *(V2.1)* | Control Relevance | SHOULD annotate when intermediary has control responsibility |
| **R-TRANSIT-5** *(V2.1)* | Pure Conduit Fallback | MAY omit transit if intermediary adds no useful control surface |
| **R-TRANSIT-6** *(V2.1)* | Compromise Separation | Intermediary compromise → preceding cluster step; transit alone insufficient |
| **R-TRANSIT-7** *(V2.1)* | Cluster Independence | Transit annotation MUST NOT change cluster classification |
| **R-TRANSIT-8** *(V2.1)* | Multiple Transit Parties | Chained transit MAY be used when each party has independent relevance |
| **R-INTRA-1** *(V2.1)* | Single-System Scope | Operator only for boundaries within a single system instance |
| **R-INTRA-2** *(V2.1)* | Cluster Attachment | Operator MUST be attached to the cluster step |
| **R-INTRA-3** *(V2.1)* | No Standalone Use | Operator MUST NOT appear without an associated cluster step |
| **R-INTRA-4** *(V2.1)* | No Cluster Change | Operator MUST NOT change cluster classification |
| **R-INTRA-5** *(V2.1)* | Optional Precision | Operator is OPTIONAL; recommended for forensic/vendor-facing use |
| **R-INTRA-6** *(V2.1)* | Multiple Crossings | Multiple annotations MAY follow one step when compressed form justified |
| **R-INTRA-7** *(V2.1)* | Distinct Vulnerabilities | Separately evidenced vulnerability → new cluster step required |
| **R-INTRA-8** *(V2.1)* | Compressed Form | Compressed single-step MAY be used when evidence doesn't distinguish causes |
| **R-INTRA-9** *(V2.1)* | Anti-Effect / Memory Deferral | Effects are not threats; `memory` boundary type deferred → MUST NOT use |
| **R-UNRES-1** *(V2.1)* | Semantic Constraint | `?` and `…` represent real attack steps, not noise or speculation |
| **R-UNRES-4** *(V2.1)* | Classification Threshold | If any cluster can be defended → use `#X [conf=low]`, not `?` |
| **R-UNRES-5** *(V2.1)* | No DRE on Unresolved | DRE tags MUST NOT be appended to `?` or `…` |
| **R-UNRES-7** *(V2.1)* | Resolution Obligation | Every `?`/`…` is an open analytical task → resolve when evidence arrives |
| **R-UNRES-8** *(V2.1)* | Prose Required | Paths containing `?`/`…` MUST have prose annotation explaining gap |
| **R-UNRES-9** *(V2.1)* | Binary Classification | No partial-confidence operators (`?#4`, `#4?`, `#{2\|7}`) |
