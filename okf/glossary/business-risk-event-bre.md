---
type: "term"
title: "Business Risk Event (BRE)"
description: "A discrete, observable business level event on the consequence side of the Bow Tie model, triggered by a Data Risk Event or by a preceding BRE."
resource: "tlctc:term:business-risk-event-bre"
tags:
  - "glossary"
---
# Business Risk Event (BRE)

A discrete, observable business-level event on the consequence side of the Bow-Tie model, triggered by a Data Risk Event or by a preceding BRE. Examples include regulatory notification obligations, service outage declarations, media coverage, customer churn, and regulatory fines. BREs may **chain**: each BRE can trigger subsequent BREs, forming a variable-length consequence sequence (`SRE → DRE → BRE₁ → BRE₂ → ... → BREₙ`). Each BRE→BRE transition has its own Δt representing a detection and intervention window. An organization's Risk Appetite determines at which point a BRE is designated as the terminal **Business Impact (BI)** — BI is a role a BRE can hold, not a separate event category.

**Reference:** §6.3.1 (The Consequence Chain), V1.9.1 §The Anatomy of Risk




**Related reading:** [Evolving VERIS — replace Action axis with TLCTC](https://www.tlctc.net/tlctc-veris.html), [blog-cyber-bow-tie-business-risk-event-chain.html](https://www.tlctc.net/blog-cyber-bow-tie-business-risk-event-chain.html), [Agentic AI as consequence amplifier (right side of Bow-Tie)](https://www.tlctc.net/tlctc-agentic-ai-consequences.html), [Propagated Controls — Rule of Propagation](https://www.tlctc.net/tlctc-propagated-controls.html), [TLCTC v2.1 monster prompt — Regulators & Standards](https://www.tlctc.net/tlctc-prompt-regulators.html), [TLCTC+ for NCSCs & CERTs — national reporting](https://www.tlctc.net/tlctc-plus-ncsc-proposal.html)

See also: System Risk Event (SRE), Data Risk Event (DRE), Business Impact (BI), Event Chain, Consequences
