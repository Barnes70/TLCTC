---
type: "term"
title: "Event Chain"
description: "A sequence of risk events in which each event either brings about the next (a causal edge, with a Δt) or meets a norm's condition or violates it (a normative edge, without one), following the consequence chain SRE → DRE → BRE\\ ."
resource: "tlctc:term:event-chain"
tags:
  - "glossary"
---
# Event Chain

A sequence of risk events in which each event either brings about the next (a causal edge, with a Δt) or meets a norm's condition or violates it (a normative edge, without one), following the consequence chain **SRE → DRE → BRE\***. The chain cascades from the System Risk Event (central event) through Data Risk Events to one or more Business Risk Events. BREs may themselves chain (`BRE₁ → BRE₂ → ... → BREₙ`), each causal transition having its own Δt, the interval that bounds the detection and intervention window in which all six NIST CSF functions apply. Example: System Compromise (SRE) → Data Breach involving PII (DRE [C]) → GDPR notification obligation (BRE₁, normative) + NIS2 incident report filed (BRE₂, a causal response bounded by the reporting deadline) → Regulatory fine (BRE₃). Understanding event chains is critical for designing Respond/Recover controls and regulatory compliance workflows.

**Reference:** Handbook §6.3.1 (The Consequence Chain), V1.9.1 §Data Risk Event Types, §Clarification on Central Event Position; Core paper §3.4




**Related reading:** [The Cyber Bow-Tie — from one pivot to layered bow-ties](https://www.tlctc.net/tlctc-cyber-bow-tie.html), [Propagated Controls — Rule of Propagation](https://www.tlctc.net/tlctc-propagated-controls.html), [Strategic risk management implementation guide v2.1](https://www.tlctc.net/tlctc-big-picture.html)

See also: System Risk Event (SRE), Data Risk Event (DRE), Business Risk Event (BRE), Business Impact (BI), Eₙ Event Notation, RS Container, Propagated PR
