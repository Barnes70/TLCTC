---
type: "term"
title: "System Failure"
description: "The Failure type of the System Risk Event: loss of function with no actor holding capability — software or hardware failure, misconfiguration, capacity exhaustion without an attacker, an external event, or an unintended act (Error in Use) that breaks the system."
resource: "tlctc:term:system-failure"
tags:
  - "glossary"
---
# System Failure

The **Failure type** of the System Risk Event: loss of function with no actor holding capability — software or hardware failure, misconfiguration, capacity exhaustion without an attacker, an external event, or an unintended act (Error in Use) that breaks the system. It sits at the same altitude as System Compromise and passes through the same conditional gate ("only if data is affected") into the data layer, so it shares the consequence chain **SRE → DRE → BRE\*** while having no cause-side classification: operational risk, no cluster, no attacker's view. Named in v2.5 so that the failure branch drawn at the same altitude in the framework's figures is inside the model rather than implicit.

**Reference:** Core paper §3.4; dictionary `system_risk_event.types[failure]`

See also: System Risk Event (SRE), Loss of Control / System Compromise, Error in Use, Cause-Side Partition
