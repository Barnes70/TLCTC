---
type: "term"
title: "Business Risk Event (BRE)"
description: "A discrete, observable business level event on the consequence side of the Bow Tie model, reached from a Data Risk Event or a preceding BRE by a causal edge (it is brought about, after a Δt) or by a normative edge (a duty arises or a norm is violated; no Δt is defined)."
resource: "tlctc:term:business-risk-event-bre"
tags:
  - "glossary"
---
# Business Risk Event (BRE)

A discrete, observable business-level event on the consequence side of the Bow-Tie model, reached from a Data Risk Event or a preceding BRE by a **causal** edge (it is brought about, after a Δt) or by a **normative** edge (a duty arises or a norm is violated; no Δt is defined). Examples include notification obligations arising (normative), notifications filed, service outage declarations, media coverage, customer churn, and regulatory fines. BREs may **chain**, forming a variable-length consequence sequence (`SRE → DRE → BRE₁ → BRE₂ → ... → BREₙ`). Each causal transition has its own Δt, the interval that bounds the window for detection and intervention; a statutory deadline is not a Δt but bounds the response process from awareness. A BRE can also be entered directly by a normative edge, with no SRE or DRE before it — an unchanged process becomes non-compliant when a norm is amended: compliance risk, no cluster. An organization's Risk Appetite determines at which point a BRE is designated as the terminal **Business Impact (BI)** — BI is a role a BRE can hold, not a separate event category.

**Reference:** Handbook §6.3.1 (The Consequence Chain), V1.9.1 §The Anatomy of Risk; Core paper §3.4; dictionary `consequence_chain` (v2.7)




**Related reading:** [Evolving VERIS — replace Action axis with TLCTC](https://www.tlctc.net/tlctc-veris.html), [blog-cyber-bow-tie-business-risk-event-chain.html](https://www.tlctc.net/blog-cyber-bow-tie-business-risk-event-chain.html), [Agentic AI as consequence amplifier (right side of Bow-Tie)](https://www.tlctc.net/tlctc-agentic-ai-consequences.html), [Propagated Controls — Rule of Propagation](https://www.tlctc.net/tlctc-propagated-controls.html), [TLCTC v2.5 monster prompt — Regulators & Standards](https://www.tlctc.net/tlctc-prompt-regulators.html), [TLCTC+ for NCSCs & CERTs — national reporting](https://www.tlctc.net/tlctc-plus-ncsc-proposal.html)

See also: System Risk Event (SRE), Data Risk Event (DRE), Business Impact (BI), Event Chain, Consequences, Normative Edge
