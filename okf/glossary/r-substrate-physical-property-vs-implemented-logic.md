---
type: "term"
title: "R-SUBSTRATE (Physical Property vs Implemented Logic)"
description: "Global mapping rule (v2.5): Classify as 8 Physical Attack only where a physical layer property of the substrate — charge, voltage, electromagnetic emission, temperature, emission borne timing, wear, or material state — is itself the exploited generic vulnerability."
resource: "tlctc:term:r-substrate-physical-property-vs-implemented-logic"
tags:
  - "glossary"
---
# R-SUBSTRATE (Physical Property vs Implemented Logic)

Global mapping rule (v2.5): Classify as `#8 Physical Attack` only where a physical-layer property of the substrate — charge, voltage, electromagnetic emission, temperature, emission-borne timing, wear, or material state — is itself the exploited generic vulnerability. Where the physical layer serves only as the readout channel for a defect in implemented logic, classify by that defect (`#2` or `#3` per R-ROLE). Attacker proximity or possession is **not** the test.

The discriminating question is whether the attack is against the *implemented logic* or against the *physical representation* that logic runs on. Rowhammer is `#8` (charge migration between adjacent DRAM cells is the vulnerability; nothing logical fails) even though it can be mounted from JavaScript. Spectre is `#2` (speculation crosses an isolation boundary the design was meant to enforce; cache timing is only the readout). Power side-channel analysis is `#8`, because the cryptography is correct and the emission itself is the vulnerability.

R-SUBSTRATE is the *admission* test — whether a weakness qualifies as `#8` at all. The sequencing principle formerly stated as R-PHYSICAL (now a deprecated alias) still holds — a qualifying physical step is `#8` and subsequent technical steps are classified separately. They are complementary.

**Reference:** §6.1 (R-SUBSTRATE)
