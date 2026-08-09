---
type: "term"
title: "R-INTRA (Intra-System Boundary Rules)"
description: "The v2.5 normative registry carries exactly two R INTRA rules governing the intra system operator ( |...| ): | Rule | Summary | | | | | R INTRA 7 | Intra system boundary crossings never change cluster classification."
resource: "tlctc:term:r-intra-intra-system-boundary-rules"
tags:
  - "glossary"
---
# R-INTRA (Intra-System Boundary Rules)

The v2.5 normative registry carries exactly **two** R-INTRA rules governing the intra-system operator (`|...|`):

| Rule | Summary |
|---|---|
| **R-INTRA-7** | Intra-system boundary crossings never change cluster classification. They are observability annotations, not classification inputs. |
| **R-INTRA-9** | The `memory` intra-system boundary type is deferred and MUST NOT be used. |

The remaining usage guidance from the v2.1 drafting is non-normative and preserved as notation practice: the operator applies only to boundaries within a single system instance, attaches to the cluster step that accomplishes the crossing, never appears standalone, is optional (mainly for forensic or vendor-facing precision), and multiple annotations may follow one step. If a crossing requires a **separately evidenced vulnerability**, a new cluster step MUST be added — this follows directly from Axiom VI (see also SG-6) and is not an R-INTRA rule.

> **Numbering erratum (do not cite the v2.1 draft numbers).** Early v2.1 drafts circulated a nine-rule series R-INTRA-1…9 in which "no cluster change" was numbered R-INTRA-4 and "distinct vulnerabilities" was numbered **R-INTRA-7**. In the canonical registry (v2.3 onward) R-INTRA-7 denotes the *no-cluster-change* rule. The draft series is therefore withdrawn: citing "R-INTRA-7" in its draft meaning contradicts the canon. Only the canonical meanings above are valid; this is the single known case in TLCTC history of a rule ID changing propositions between draft and canon, recorded here so it can never happen silently.

**Reference:** core paper §6.2 (R-INTRA-7, R-INTRA-9), §11.3.6 (Intra-System Boundary Operator)
