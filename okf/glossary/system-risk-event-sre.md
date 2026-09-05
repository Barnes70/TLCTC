---
type: "term"
title: "System Risk Event (SRE)"
description: "Any risk event at the system altitude — the point at which a system's behavior, privileges, data, or trust relationships depart from what its owner controls — and the central event in the TLCTC Cyber Bow Tie model."
resource: "tlctc:term:system-risk-event-sre"
tags:
  - "glossary"
---
# System Risk Event (SRE)

Any risk event at the **system altitude** — the point at which a system's behavior, privileges, data, or trust relationships depart from what its owner controls — and the central event in the TLCTC Cyber Bow-Tie model. Since v2.5 the SRE has **two types at one altitude**: **System Compromise / Loss of Control** (an actor holds capability over the system sufficient to pursue objectives; reached only through cluster steps; the pivot of the bow-tie) and **System Failure / Loss of Function** (no actor holds anything; operational risk, no cluster). Abuse of Rights produces neither type — the system was obeyed, not compromised, and did not fail — so its chain begins at the DRE. The SRE is the pivot point between the cause side (threat clusters exploiting generic vulnerabilities) and the consequence side (data and business risk events). It is the first event in the consequence chain **SRE → DRE → BRE\***, where each transition has its own Δt representing a detection and intervention window. Not every SRE leads to a DRE — detection and containment at the central event can break the chain before data-level consequences materialize.

> **Disambiguation:** "Loss of Control" is always abbreviated **SRE**, never "LoC". The abbreviation **LoC** is reserved exclusively for Loss of Confidentiality, a *consequence*-side Data Risk Event. See **Loss of Confidentiality (LoC)**.

**Reference:** §6.3 (Central Event), §6.3.1 (The Consequence Chain)

See also: Loss of Control / System Compromise, Data Risk Event (DRE), Business Risk Event (BRE)
