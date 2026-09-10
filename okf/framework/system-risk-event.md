---
type: "sre"
title: "System Risk Event (System Compromise, the cyber pivot)"
description: "Any risk event at the system altitude: the point at which a system's behaviour, privileges, data, or trust relationships depart from what its owner controls."
resource: "tlctc:framework:system-risk-event"
tags:
  - "taxonomy"
  - "sre"
  - "bow-tie"
  - "central-event"
---
# System Risk Event (SRE)

Any risk event at the system altitude: the point at which a system's behaviour, privileges, data, or trust relationships depart from what its owner controls. The SRE is the central event of the Cyber Bow-Tie and the first node of the consequence chain SRE -> DRE -> BRE*. The SRE the framework defines is System Compromise, reached only through cluster steps; every cluster step records one, so a path of n cluster steps records n SREs, each admitting a Data Risk Event, a further cluster step (a chained SRE, against the same system or another), or both. Other events occur at the same altitude with no actor holding capability - System Failure is the standing example - and are operational risk with no cluster; the framework names them to place the boundary, not to classify them.

## Types

| Type | Name | Clusters reach it | Definition |
|---|---|---|---|
| `compromise` | System Compromise — Loss of Control | yes | An actor holds capability over the system's behaviour, privileges, data, or trust relationships sufficient to pursue objectives. Reached only through cluster steps (the Attack row). This is the pivot of the Cyber Bow-Tie: everything the ten clusters classify converges on it, and the detection-and-intervention window between compromise and any Data Risk Event exists only for this type. |

## Other system-altitude events (outside the clusters)

Events at the same altitude as System Compromise in which no actor holds capability. Operational risk; no cluster; same conditional gate ("only if data is affected") into the data layer, so they share the consequence chain while having no cause-side classification. Named to place the boundary of the ten clusters, not to classify what lies outside it.

| Example | Name | Clusters reach it | Definition |
|---|---|---|---|
| `failure` | System Failure — Loss of Function | no | The system ceases to perform its function and no actor holds anything: software or hardware failure, misconfiguration, capacity exhaustion without an attacker, an external event, or an unintended act (Error in Use) that breaks the system. Operational risk; no cluster. It sits at the same altitude as Compromise and passes through the same conditional gate ('only if data is affected') into the data layer, so it shares the consequence chain while having no cause-side classification. |

> v2.5 widening (2026-09-05): earlier v2.5 text defined the SRE as the attacker's loss-of-control event only; System Failure, drawn at the same altitude in the framework's figures without being defined, was named as a second type. v2.5 re-centering (2026-09-10): that gave Failure a co-equal standing the figures never showed and the clusters never reach. The SRE the framework defines is System Compromise alone; System Failure is retained verbatim as the standing example of other system-altitude events, moved from `types` to `other_system_altitude_events`. The definition now also states the per-step rule the prose had already adopted: every cluster step records an SRE. Abuse of Rights produces no SRE at all: the system was obeyed, not compromised, and did not fail; its chain begins at the DRE (R-SCOPE).

# Schema

- **Consequence chain:** SRE → DRE → BRE* (see [DRE codes](/framework/data-risk-events.md))
- **Cause side:** see [cause-side partition](/framework/cause-side-partition.md)
