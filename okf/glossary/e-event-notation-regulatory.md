---
type: "term"
title: "Eₙ Event Notation (Regulatory)"
description: "A numbered event sequence notation used to map attack chains to regulatory compliance triggers: E1: System Compromise / Loss of Control (the central Bow Tie event) E2: Data Risk Event (e.g., PII exposure — GDPR trigger) E3a, E3b, ...: Compliance violation events (e.g., GDPR breach notification, NIS2 incident report) The subscript (a, b, etc.) distinguishes parallel regulatory branches triggered by the same upstream event."
resource: "tlctc:term:e-event-notation-regulatory"
tags:
  - "glossary"
---
# Eₙ Event Notation (Regulatory)

A numbered event sequence notation used to map attack chains to regulatory compliance triggers:

- **E1:** System Compromise / Loss of Control (the central Bow-Tie event)
- **E2:** Data Risk Event (e.g., PII exposure — GDPR trigger)
- **E3a, E3b, ...:** Compliance violation events (e.g., GDPR breach notification, NIS2 incident report)

The subscript (a, b, etc.) distinguishes parallel regulatory branches triggered by the same upstream event. Different regulations trigger at different points: GDPR Art. 33 triggers at E2 (Data Risk Event involving PII), while NIS2 Art. 23 triggers at E1 (Significant Incident). See also: Event Chain Length, RS Container.
