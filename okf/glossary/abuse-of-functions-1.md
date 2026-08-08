---
type: "term"
title: "Abuse of Functions (#1)"
description: "A threat cluster where an attacker misuses the logic, scope, or configuration of existing, legitimate software functions for malicious purposes."
resource: "tlctc:term:abuse-of-functions-1"
tags:
  - "glossary"
---
# Abuse of Functions (#1)

A threat cluster where an attacker misuses the logic, scope, or configuration of existing, legitimate software functions for malicious purposes. This manipulation occurs through standard interfaces using expected input types (data, parameters, configurations, sequence of actions), but in a way that subverts the intended purpose or security controls. Crucially, inputs remain data; no foreign code is introduced or executed. The generic vulnerability is the scope, complexity, or inherent trust placed in legitimate software functions. Classification is governed by the #1 boundary tests in the core paper: if the attacker's success does not require any implementation flaw and instead abuses intended functionality, scope, or configuration via standard interfaces using expected input types, the step MUST be classified as `#1 Abuse of Functions`. (This test was stated as mapping rule R-ABUSE in the v2.0 whitepaper; the ID is a deprecated alias in v2.5.)

**Reference:** Core paper §4 (#1 boundary tests); formerly R-ABUSE (whitepaper §4.2.5)

**Related reading:** [AD → Domain Admin → Ransomware cascade](https://www.tlctc.net/ad-ransomware-tlctc-cascade.html), [CVE-2026-44578: Next.js WebSocket SSRF](https://www.tlctc.net/cve-2026-44578.html), [CVE-2020-17103 — patch closed an effect, not a cluster](https://www.tlctc.net/cve-2020-17103.html), [CrowdStrike 2025 Threat Hunting Report — TLCTC](https://www.tlctc.net/tlctc-crowdstrike-2025-analysis.html), [CrowdStrike 2025 Global Threat Report — TLCTC](https://www.tlctc.net/tlctc-crowdstrike-2025-report.html), [The Adoboli Paradox — Cyber vs Operational Risk](https://www.tlctc.net/tlctc-adoboli-paradox.html)
