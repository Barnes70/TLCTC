---
type: "term"
title: "Attack Path Notation"
description: "The standardized format for describing cyber attack sequences using TLCTC clusters."
resource: "tlctc:term:attack-path-notation"
tags:
  - "glossary"
---
# Attack Path Notation

The standardized format for describing cyber attack sequences using TLCTC clusters. Format uses: `→` for sequential steps, `+` for parallel execution, `[time]` for temporal intervals, and `||[context][@Source→@Target]||` for domain boundaries. Example: `#9→[24h]#4→[12m]#1 ||[dev][@Vendor→@Org]|| →[weeks]#10.2→[0s]#7`.

**Related reading:** [CVE-2020-17103 — patch closed an effect, not a cluster](https://www.tlctc.net/cve-2020-17103.html), [20 annotated attack paths (Ransomware, BEC, OT, ...)](https://www.tlctc.net/tlctc-attack-path-examples.html), [Dual-layer notation — TLCTC-XX.YY enumeration](https://www.tlctc.net/tlctc-enumeration.html), [TLCTC v2.1 monster prompt — CTI & Forensic](https://www.tlctc.net/tlctc-prompt-cti.html)
