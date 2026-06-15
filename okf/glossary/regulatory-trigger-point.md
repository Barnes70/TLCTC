---
type: "term"
title: "Regulatory Trigger Point"
description: "The specific event type in a TLCTC event chain that activates a regulatory notification or compliance obligation."
resource: "tlctc:term:regulatory-trigger-point"
tags:
  - "glossary"
---
# Regulatory Trigger Point

The specific event type in a TLCTC event chain that activates a regulatory notification or compliance obligation. Different regulations have different trigger points within the same attack sequence:

- **Data-triggered regulations** (e.g., GDPR Art. 33): Activate at E2 (Data Risk Event involving PII) — no PII affected means no GDPR notification obligation
- **Incident-triggered regulations** (e.g., NIS2 Art. 23): Activate at E1 (Significant Incident / System Compromise) — regardless of whether PII is involved

Understanding regulatory trigger points enables CISOs to build precise IR playbooks mapping specific RS container actions to logical triggers rather than generic "reporting checklists". See also: Propagated PR, Event Chain Length.
