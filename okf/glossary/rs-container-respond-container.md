---
type: "term"
title: "RS Container (Respond Container)"
description: "The logical collection of RESPOND function controls and actions for a specific event (Eₙ) in the TLCTC event chain."
resource: "tlctc:term:rs-container-respond-container"
tags:
  - "glossary"
---
# RS Container (Respond Container)

The logical collection of RESPOND-function controls and actions for a specific event (Eₙ) in the TLCTC event chain. An RS Container holds:

- **Direct Response Actions:** Containment, eradication, forensics for the event itself
- **Propagated PR Controls:** Protection requirements inherited from downstream compliance events (E3a, E3b, etc.)

Notation: `RS(Eₙ) = { Response } ∪ { Propagated PR(Eₙ₊₁) } ∪ { Propagated PR(Eₙ₊ₓ) }`. Example: RS(E1) for a ransomware incident may contain both incident containment actions AND propagated GDPR/NIS2 notification controls, each with distinct timelines and reporting authorities. Aligns with NIST CSF RESPOND function. See also: Propagated PR, Regulatory Trigger Point.
