---
type: "dre-tree"
title: "Data Risk Event type codes (refinement tree)"
description: "Data Risk Event (DRE) type codes used in '+ [DRE: ...]' tags."
resource: "tlctc:framework:data-risk-events"
tags:
  - "taxonomy"
  - "dre"
  - "consequence-side"
---
# Data Risk Event type codes

Data Risk Event (DRE) type codes used in '+ [DRE: ...]' tags. Three parent properties — C (Confidentiality), I (Integrity), A (Availability/Accessibility) — with two admitted refinements: I → Ii/If and A → Av/Ac. A parent code stays legal whenever the refinement is unknown or irrelevant. Codes are outcome annotations recorded on the record that changed state: never clusters, never classification inputs (Axiom III), and never appended to unresolved steps (R-UNRES-5).

## Stopping rule

Split a property only where the resulting states differ in the record's present standing — what now holds of the record when it is checked against its referent, its declared scope, its claimed origin or the agents entitled to use it — never by the story of how it came to be in that state (the mechanism, the actor or the intent). On that test the vocabulary is closed, by decision, at two splits (I → Ii/If: does the content fail, or the claimed origin? A → Av/Ac: is the data absent, or present and unusable?); any further split would have to pass the same test. The rule refuses every split of C (accidental versus deliberate disclosure is the story of the disclosure; one party versus public is extent, i.e. severity, not a state), and refuses any split by cause — outcomes never inherit the classification of the step that produced them (Axiom III).

## Codes

| Code | Parent | Name | What fails | Definition |
|---|---|---|---|---|
| `C` | — | Loss of Confidentiality | disclosure | Data has been disclosed to a party not entitled to it. No refinement: disclosed data is disclosed, and the record's standing is identical however it leaked. |
| `I` | — | Loss of Integrity | integrity (parent of Ii and If) | The standing of a record as a faithful and attributable representation has changed other than through its intended, authorised process. Use I when it is unknown or irrelevant whether correspondence (Ii) or provenance (If) failed. |
| `Ii` | `I` | Incorrect state | correspondence, completeness | The record no longer corresponds to what it represents, or is no longer complete; read off the record, the content is wrong. Answered by validation, reconciliation and four-eyes controls. |
| `If` | `I` | Misattributed state | provenance, attribution | The record claims an origin, author or authority it does not have; read off the record, provenance fails while the content may be perfectly accurate. Answered by segregation of duties, provenance logging and behavioural monitoring. |
| `A` | — | Loss of Availability / Accessibility | availability (parent of Av and Ac) | Data can no longer serve its intended use by authorised processes. Use A when it is unknown or irrelevant whether the data is gone (Av) or present but unusable (Ac). |
| `Av` | `A` | Unavailable state | operational presence | Data is gone or unreachable — the resource no longer exists or cannot be technically reached by the infrastructure (deletion, wiper, storage loss, system offline). |
| `Ac` | `A` | Inaccessible state | retrievability | Data is present and reachable but cannot be used for its intended purpose by authorised processes (ransomware encryption, corruption of the container, permission lockout). |

# Schema

- **Parents:** `C`, `I`, `A`
- **Refinements:** `Ii` → `I`, `If` → `I`, `Av` → `A`, `Ac` → `A`
- **Notation:** `+ [DRE: C, Ii, If, Av, Ac]` (any subset; a parent stays legal when the refinement is unknown)
