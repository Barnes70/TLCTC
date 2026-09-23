---
type: "rule"
title: "R-SPECIFIC"
description: "Where one weakness is describable both as a specific generic vulnerability and as a residual one, classify it under the specific."
resource: "tlctc:rule:R-SPECIFIC"
tags:
  - "taxonomy"
  - "rule"
  - "must"
enforcement_level: "must"
machine_enforceable: false
---
# R-SPECIFIC

Where one weakness is describable both as a specific generic vulnerability and as a residual one, classify it under the specific. The residual tests — designed functionality (#1) and implementation flaw (#2/#3 per R-ROLE) — apply only where no specific generic vulnerability is the one exploited. Three clauses decide the recurring cases: (capacity) if the primary mechanism is volume or intensity exhausting finite resources, #6; an implementation defect causing crash, hang or degradation is #2/#3; (channel) if the defective logic is itself a communication-path control — peer authenticity (certificate validation, chain of trust, hostname matching, expiry or revocation checking), channel encryption, or algorithm negotiation — #5; a defect incidental to that control is #2/#3; (substrate) if a physical-layer property of the substrate — charge, voltage, electromagnetic emission, temperature, emission-borne timing, wear, or material state — is itself the exploited generic vulnerability, #8, whether or not the attacker has physical access; where the physical layer is only the readout channel for a defect in implemented logic, classify by that defect.

> v2.6 consolidation (C2). Folds the v2.5 rules R-FLOOD (capacity), R-CHANNEL (channel) and R-SUBSTRATE (substrate) into one rule; each clause reproduces the retired rule's proposition unchanged, and the retired IDs remain aliases of their clauses with their v2.5 meaning (an ID is never reused). The rule states the derivation principle the three instantiated: the residual clusters — #1 for designed functionality, #2/#3 for implementation flaws — apply only where no specific generic vulnerability is the one exploited. Channel: the test is constitutive versus incidental, not server versus client — a missing or incorrect certificate check IS the absence of control over the communication path, while memory corruption in a TLS parser remains #2/#3; the clause classifies the weakness, R-MITM sequences the path. Substrate: the question is whether the attack is against the implemented logic or against the physical representation it runs on — Rowhammer is #8 (charge migration is the vulnerability, mountable from JavaScript, which is why proximity is not the test), Spectre is #2 (speculation crosses a designed isolation boundary; timing is only the readout), power analysis is #8 (the cryptography is correct; the emission is the vulnerability); the location of a flaw — hardware, firmware, silicon — never determines the cluster, and where foreign code executes to induce the effect the execution is a separate #7 step (#7 -> #8). The substrate clause is the admission test for #8; the sequencing principle once stated as R-PHYSICAL (a retired v2.0 alias) still holds. R-CRED and R-EXEC apply the same principle to #4 and #7 but also split one action into two steps, so they remain separate rules.

# Schema

- **Enforcement level:** must
- **Machine enforceable:** false
