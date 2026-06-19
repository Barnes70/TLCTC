---
type: "term"
title: "R-TRANSIT (Transit Boundary Rules)"
description: "The complete transit boundary rule set governing use of the transit operator ( ⇒ ): | Rule | Name | Summary | | | | | | R TRANSIT 1 | Distinct Parties | @Transit MUST be distinct from both @Source and @Target | | R TRANSIT 2 | True Intermediary Topology | Operator MUST be used only when the intermediary sits between source and target in the delivery path | | R TRANSIT 3 | Vendor Code on Target Device | Vendor code running on the target device is NOT transit — it is the attack surface and MUST be classified by R ROLE | | R TRANSIT 4 | Control Relevance | Operator SHOULD be used when the intermediary has meaningful control responsibility; MAY be omitted when analytically incidental | | R TRANSIT 5 | Pure Conduit Fallback | If the intermediary adds no useful control surface, the analyst MAY use the binary v2.0 boundary or omit the transit annotation | | R TRANSIT 6 | Compromise or Coercion Is Separate | If transit is enabled by compromise or coercion of the intermediary, that enabling condition MUST be modeled as a preceding cluster step | | R TRANSIT 7 | Cluster Independence | Transit annotation MUST NOT change cluster classification | | R TRANSIT 8 | Multiple Transit Parties | Chained transit MAY be used when each intermediary has independent analytical relevance | Reference: §4.2.4 (R TRANSIT), §11.3.5 (Transit Boundary Operator)"
resource: "tlctc:term:r-transit-transit-boundary-rules"
tags:
  - "glossary"
---
# R-TRANSIT (Transit Boundary Rules)

The complete transit boundary rule set governing use of the transit operator (`⇒`):

| Rule | Name | Summary |
|---|---|---|
| **R-TRANSIT-1** | Distinct Parties | `@Transit` MUST be distinct from both `@Source` and `@Target` |
| **R-TRANSIT-2** | True Intermediary Topology | Operator MUST be used only when the intermediary sits between source and target in the delivery path |
| **R-TRANSIT-3** | Vendor Code on Target Device | Vendor code running on the target device is NOT transit — it is the attack surface and MUST be classified by R-ROLE |
| **R-TRANSIT-4** | Control Relevance | Operator SHOULD be used when the intermediary has meaningful control responsibility; MAY be omitted when analytically incidental |
| **R-TRANSIT-5** | Pure Conduit Fallback | If the intermediary adds no useful control surface, the analyst MAY use the binary v2.0 boundary or omit the transit annotation |
| **R-TRANSIT-6** | Compromise or Coercion Is Separate | If transit is enabled by compromise or coercion of the intermediary, that enabling condition MUST be modeled as a preceding cluster step |
| **R-TRANSIT-7** | Cluster Independence | Transit annotation MUST NOT change cluster classification |
| **R-TRANSIT-8** | Multiple Transit Parties | Chained transit MAY be used when each intermediary has independent analytical relevance |

**Reference:** §4.2.4 (R-TRANSIT), §11.3.5 (Transit Boundary Operator)
