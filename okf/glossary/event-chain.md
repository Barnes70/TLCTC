---
type: "term"
title: "Event Chain"
description: "A causal sequence where one outcome event triggers subsequent events, following the consequence chain SRE → DRE → BRE\\ ."
resource: "tlctc:term:event-chain"
tags:
  - "glossary"
---
# Event Chain

A causal sequence where one outcome event triggers subsequent events, following the consequence chain **SRE → DRE → BRE\***. The chain cascades from the System Risk Event (central event) through Data Risk Events to one or more Business Risk Events. BREs may themselves chain (`BRE₁ → BRE₂ → ... → BREₙ`), with each transition having its own Δt representing a detection and intervention window where all six NIST CSF functions apply. Example: System Compromise (SRE) → Data Breach involving PII (DRE [C]) → GDPR notification obligation (BRE₁) + NIS2 incident report (BRE₂) → Regulatory fine (BRE₃). Understanding event chains is critical for designing Respond/Recover controls and regulatory compliance workflows.

**Reference:** §6.3.1 (The Consequence Chain), V1.9.1 §Data Risk Event Types, §Clarification on Central Event Position




**Related reading:** [blog-cyber-bow-tie-business-risk-event-chain.html](https://www.tlctc.net/blog-cyber-bow-tie-business-risk-event-chain.html), [Propagated Controls — Rule of Propagation](https://www.tlctc.net/tlctc-propagated-controls.html), [Strategic risk management implementation guide v2.1](https://www.tlctc.net/tlctc-big-picture.html)

See also: System Risk Event (SRE), Data Risk Event (DRE), Business Risk Event (BRE), Business Impact (BI), Eₙ Event Notation, RS Container, Propagated PR
