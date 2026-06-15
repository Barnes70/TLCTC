---
type: "term"
title: "Velocity Class"
description: "Categorical labels for Δt ranges that describe the defender's feasible response mode and determine appropriate control strategies."
resource: "tlctc:term:velocity-class"
tags:
  - "glossary"
---
# Velocity Class

Categorical labels for Δt ranges that describe the defender's feasible response mode and determine appropriate control strategies. Four classes are defined:

- **VC-1: Strategic / Latent/Slow** (days → months): Log retention, threat hunting, strategic monitoring
- **VC-2: Tactical / Medium** (hours): SIEM alerting, analyst triage, guided response
- **VC-3: Operational / Fast** (minutes): Automation (SOAR/EDR), rapid containment, prebuilt playbooks
- **VC-4: Real-Time** (seconds → milliseconds): Architecture & circuit breakers, rate-limits, hardening, automatic isolation

**Reference:** §12.4 (Operational Velocity Classes)
