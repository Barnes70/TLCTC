---
type: "term"
title: "Lateral Movement"
description: "The techniques an attacker uses to progressively move through a network after initial compromise, seeking higher value targets and expanded access."
resource: "tlctc:term:lateral-movement"
tags:
  - "glossary"
---
# Lateral Movement

The techniques an attacker uses to progressively move through a network after initial compromise, seeking higher-value targets and expanded access. In TLCTC: lateral movement is not a single cluster — it is an attack path composed of multiple sequential steps. Typical lateral movement sequences include: `#4 → #1` (using stolen credentials to access another system's functions), `#4 → #7` (deploying malware on additional systems using stolen credentials), or `#1 → #7` (abusing legitimate remote tools to execute code on other systems). Each step in lateral movement maps to its own cluster based on the generic vulnerability exploited.

**Reference:** V1.9.1 §Bridging Strategy and Operations, §E (Real World Examples)




**Related reading:** [AD → Domain Admin → Ransomware cascade](https://www.tlctc.net/ad-ransomware-tlctc-cascade.html)

See also: Attack Path, Sequence, Identity Theft (#4)
