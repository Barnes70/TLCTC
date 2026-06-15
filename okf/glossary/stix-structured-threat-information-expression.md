---
type: "term"
title: "STIX (Structured Threat Information Expression)"
description: "A standardized language for representing cyber threat information."
resource: "tlctc:term:stix-structured-threat-information-expression"
tags:
  - "glossary"
---
# STIX (Structured Threat Information Expression)

A standardized language for representing cyber threat information. TLCTC integrates with STIX at the **classification layer**: cluster identifiers can be carried as custom properties (e.g., `x_tlctc_primary_cluster`) or controlled-vocabulary tags on existing STIX objects such as `attack-pattern` and `indicator`. **Layer 3 attack path instances do not round-trip to STIX 2.1** — Δt annotations, parallel groups, boundary operators (`||...||`, `⇒`, `|...|`), DRE tags, and unresolved operators (`?`, `…`) have no native STIX 2.1 equivalents and cannot be reconstructed from `attack-pattern` + SRO decomposition. Full Layer 3 exchange requires a custom STIX extension or transporting the TLCTC JSON instance as an out-of-band artifact.

**Related reading:** [MITRE ATT&CK & STIX integration with TLCTC](https://www.tlctc.net/mitre-tlctc.html), [MITRE ATT&CK & STIX × TLCTC V2.0 — implementation guide](https://www.tlctc.net/stix-tlctc.html)
