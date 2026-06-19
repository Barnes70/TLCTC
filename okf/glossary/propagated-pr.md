---
type: "term"
title: "Propagated PR"
description: "A Protection Requirement that \"propagates backward\" from a downstream event into the RS (Respond) container of an earlier event due to regulatory or policy requirements."
resource: "tlctc:term:propagated-pr"
tags:
  - "glossary"
---
# Propagated PR

A Protection Requirement that "propagates backward" from a downstream event into the RS (Respond) container of an earlier event due to regulatory or policy requirements. Notation: `RS(Eₙ) = { Response } ∪ { Propagated PR(Eₙ₊₁) } ∪ { Propagated PR(Eₙ₊ₓ) }`.

This mechanism explains how multiple regulatory obligations stack into a single incident response workflow. Example: A ransomware attack triggers E1 (System Compromise). If PII is affected, E2 (Data Risk Event) occurs, propagating GDPR notification requirements back into RS(E1). Simultaneously, if the organization is NIS2-scoped, the incident itself propagates NIS2 reporting into RS(E1). The result: two separate Propagated PR controls in the same RS container, with different timelines (72h vs 24h+72h) and different authorities. See also: RS Container, Eₙ Event Notation.

**Related reading:** [Propagated Controls — Rule of Propagation](https://www.tlctc.net/tlctc-propagated-controls.html)
