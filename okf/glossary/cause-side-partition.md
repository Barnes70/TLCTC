---
type: "term"
title: "Cause-Side Partition"
description: "The partition of the cause side of any risk event into four rows by three questions asked in strict order: Is there an actor?"
resource: "tlctc:term:cause-side-partition"
tags:
  - "glossary"
---
# Cause-Side Partition

The partition of the cause side of any risk event into four rows by three questions asked in strict order: **Is there an actor? Did they intend it? Were they entitled?**

| Actor | Intent | Entitlement | Row | Register | Clusters |
| --- | --- | --- | --- | --- | --- |
| No | — | — | Failure / external event | OpRisk | none |
| Yes | No | — | Error in Use | OpRisk | none |
| Yes | Yes | Yes | Abuse of Rights | OpRisk | none — no SRE; chain starts at the DRE |
| Yes | Yes | No | Attack | Cyber | the ten TLCTC clusters; SRE recorded |

Entitlement is asked only once intent is present (an unentitled actor who did not intend the outcome is Error in Use, not an attack), and *entitled* means entitled, not permitted. The partition is a property of the action, not of the actor (Axiom IV): an outsider with no grant and an insider outside their grant land in the same Attack row. Only the Attack row is in TLCTC scope; the ten clusters classify its steps and only its steps (R-SCOPE). Third party is a modifier over all four rows, carried by the domain-boundary operator, not a fifth row. Decision procedure: (1) actor? no → failure; (2) intended? no → Error in Use; (3) entitlement covering *this* action? yes → Abuse of Rights; (4) implementation flaw required? yes → `#2/#3` per R-ROLE, no → `#1`.

**Reference:** Core paper §3.5; dictionary `cause_side_partition`

See also: Abuse of Rights, Error in Use, Entitlement, R-SCOPE, System Risk Event (SRE), Operational Risk (OpRisk)
