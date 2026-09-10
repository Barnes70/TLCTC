---
type: "term"
title: "System Risk Event (SRE)"
description: "Any risk event at the system altitude — the point at which a system's behavior, privileges, data, or trust relationships depart from what its owner controls — and the central event in the TLCTC Cyber Bow Tie model."
resource: "tlctc:term:system-risk-event-sre"
tags:
  - "glossary"
---
# System Risk Event (SRE)

Any risk event at the **system altitude** — the point at which a system's behavior, privileges, data, or trust relationships depart from what its owner controls — and the central event in the TLCTC Cyber Bow-Tie model. Since v2.5 the SRE has **two types at one altitude**: **System Compromise / Loss of Control** (an actor holds capability over the system sufficient to pursue objectives; reached only through cluster steps; the pivot of the bow-tie) and **System Failure / Loss of Function** (no actor holds anything; operational risk, no cluster). Abuse of Rights produces neither type — the system was obeyed, not compromised, and did not fail — so its chain begins at the DRE. One SRE is recorded **per cluster step**: the thought experiment derives each cluster as a generic vulnerability by which control departs from the owner, so every step the framework classifies takes behavior, privileges, data, or trust relationships outside what their owner controls — whether it reaches the system directly (hardware and OT included, under #8) or through a person (#9). A path of *n* cluster steps records *n* SREs, each admitting a DRE, a chained SRE against the same or another system, or both. Compromise is not confined to code execution or persistence: what makes a step a compromise is that the system's behavior passed out of its owner's control, not that the attacker acquired anything — a server-role flaw yielding an arbitrary file read has already made the system serve what its owner never authorized it to serve. The data that comes back is the DRE, on the consequence side; judging the compromise by what was obtained would let an outcome settle a cause-side question, which Axiom III forbids. The SRE is the pivot point between the cause side (threat clusters exploiting generic vulnerabilities) and the consequence side (data and business risk events); the bow-tie is a structure applied *at* an SRE, not a claim that an incident holds only one. It is the first event in the consequence chain **SRE → DRE → BRE\***, where each transition has its own Δt representing a detection and intervention window. Not every SRE leads to a DRE — detection and containment at the central event can break the chain before data-level consequences materialize.

> **Disambiguation:** "Loss of Control" is always abbreviated **SRE**, never "LoC". The abbreviation **LoC** is reserved exclusively for Loss of Confidentiality, a *consequence*-side Data Risk Event. See **Loss of Confidentiality (LoC)**.

**Reference:** §6.3 (Central Event), §6.3.1 (The Consequence Chain)

See also: Loss of Control / System Compromise, Data Risk Event (DRE), Business Risk Event (BRE)
