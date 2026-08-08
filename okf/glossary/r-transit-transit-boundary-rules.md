---
type: "term"
title: "R-TRANSIT (Transit Boundary Rules)"
description: "The complete transit boundary rule set governing use of the transit operator ( ⇒ ): | Rule | Name | Summary | | | | | | R TRANSIT 3 | Vendor Code on Target Device | Vendor code running on the target device is NOT transit — it is the attack surface and MUST be classified by R ROLE | Only R TRANSIT 3 is part of the v2.5 normative registry."
resource: "tlctc:term:r-transit-transit-boundary-rules"
tags:
  - "glossary"
---
# R-TRANSIT (Transit Boundary Rules)

The complete transit boundary rule set governing use of the transit operator (`⇒`):

| Rule | Name | Summary |
|---|---|---|
| **R-TRANSIT-3** | Vendor Code on Target Device | Vendor code running on the target device is NOT transit — it is the attack surface and MUST be classified by R-ROLE |

Only **R-TRANSIT-3** is part of the v2.5 normative registry. The remaining v2.1 drafting guidance is non-normative notation practice: a transit party must be distinct from source and target and actually sit between them in the delivery path; the annotation is optional (recommended where the intermediary has meaningful control responsibility, omittable for pure conduits); compromise or coercion of the intermediary must be modeled as its own preceding cluster step; transit annotations never change cluster classification (see SG-2); and chained transit may be used when each party has independent analytical relevance. The withdrawn draft IDs R-TRANSIT-1, -2, -4, -5, -6, -7, -8 are not to be cited.

**Reference:** core paper §6.2 (R-TRANSIT-3), §11.3.5 (Transit Boundary Operator)
