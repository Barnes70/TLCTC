---
type: "sre"
title: "System Risk Event (two types, one altitude)"
description: "Any risk event at the system altitude: the point at which a system's behaviour, privileges, data, or trust relationships depart from what its owner controls."
resource: "tlctc:framework:system-risk-event"
tags:
  - "taxonomy"
  - "sre"
  - "bow-tie"
  - "central-event"
---
# System Risk Event (SRE)

Any risk event at the system altitude: the point at which a system's behaviour, privileges, data, or trust relationships depart from what its owner controls. The SRE is the central event of the Cyber Bow-Tie and the first node of the consequence chain SRE -> DRE -> BRE*. It has two types at one altitude, distinguished by whether an actor holds capability; the cause-side partition decides which type is reachable.

## Types

| Type | Name | Clusters reach it | Definition |
|---|---|---|---|
| `compromise` | System Compromise — Loss of Control | yes | An actor holds capability over the system's behaviour, privileges, data, or trust relationships sufficient to pursue objectives. Reached only through cluster steps (the Attack row). This is the pivot of the Cyber Bow-Tie: everything the ten clusters classify converges on it, and the detection-and-intervention window between compromise and any Data Risk Event exists only for this type. |
| `failure` | System Failure — Loss of Function | no | The system ceases to perform its function and no actor holds anything: software or hardware failure, misconfiguration, capacity exhaustion without an attacker, an external event, or an unintended act (Error in Use) that breaks the system. Operational risk; no cluster. It sits at the same altitude as Compromise and passes through the same conditional gate ('only if data is affected') into the data layer, so it shares the consequence chain while having no cause-side classification. |

> v2.5 widening (2026-09-05). Earlier v2.5 text defined the SRE as the attacker's loss-of-control event only; System Failure was drawn at the same altitude in the framework's figures without being defined. The widening makes the figure and the text agree: Compromise remains the cyber pivot and the only type the clusters reach; Failure is named so that the failure branch is inside the model rather than implicit. Abuse of Rights produces no SRE of either type: the system was obeyed, not compromised, and did not fail; its chain begins at the DRE (R-SCOPE).

# Schema

- **Consequence chain:** SRE → DRE → BRE* (see [DRE codes](/framework/data-risk-events.md))
- **Cause side:** see [cause-side partition](/framework/cause-side-partition.md)
