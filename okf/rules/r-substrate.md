---
type: "rule"
title: "R-SUBSTRATE"
description: "Classify as #8 only where a physical-layer property of the substrate — charge, voltage, electromagnetic emission, temperature, emission-borne timing, wear, or material state — is itself the exploited generic vulnerability."
resource: "tlctc:rule:R-SUBSTRATE"
tags:
  - "taxonomy"
  - "rule"
  - "must"
enforcement_level: "must"
machine_enforceable: false
---
# R-SUBSTRATE

Classify as #8 only where a physical-layer property of the substrate — charge, voltage, electromagnetic emission, temperature, emission-borne timing, wear, or material state — is itself the exploited generic vulnerability. Where the physical layer serves only as the readout channel for a defect in implemented logic, classify by that defect (#2 or #3 per R-ROLE). Attacker proximity or possession is NOT the test: #8 covers exploitation of physical phenomena whether or not the attacker has physical access.

> v2.4 addition, completing the family with R-FLOOD (#6) and R-CHANNEL (#5): each resolves a weakness describable either as a specific generic vulnerability or as a generic code defect, in favour of the specific one, with R-ROLE as the residual test. The discriminating question is whether the attack is against the implemented logic or against the physical representation that logic runs on. Rowhammer is #8: charge migration between adjacent DRAM cells IS the vulnerability, no logical control fails, and removing the physics removes the flaw entirely — yet it can be mounted from JavaScript, which is why proximity cannot be the test. Spectre is #2: speculation crosses an isolation boundary the design was meant to enforce, and cache timing is only how the residue is read out — remove the physics and a boundary-crossing design remains. Power side-channel analysis is #8: the cryptography is correct and the emission itself is the vulnerability. Corollary: the location of a flaw — hardware, firmware, silicon — never determines the cluster. Substrate is not cause; per Axiom VI, where foreign code executes to induce the physical effect the execution is a separate #7 step (e.g. #7 → #8). Relationship to the legacy R-PHYSICAL (v2.0 §4.2.5, glossary): the two are complementary and non-conflicting. R-SUBSTRATE is the ADMISSION test — it decides whether a weakness qualifies as #8 at all. R-PHYSICAL is the SEQUENCING rule — given a qualifying physical step, it requires that step to be #8 and subsequent technical steps to be classified separately. R-SUBSTRATE also settles a latent ambiguity in R-PHYSICAL's phrasing ("the attacker's advantage comes from unauthorized physical interaction"), which can be misread as requiring attacker physical access; it does not.

# Schema

- **Enforcement level:** must
- **Machine enforceable:** false
