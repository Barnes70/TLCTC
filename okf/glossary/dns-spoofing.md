---
type: "term"
title: "DNS Spoofing"
description: "A technique where an attacker corrupts DNS resolution to redirect traffic to attacker controlled infrastructure."
resource: "tlctc:term:dns-spoofing"
tags:
  - "glossary"
---
# DNS Spoofing

A technique where an attacker corrupts DNS resolution to redirect traffic to attacker-controlled infrastructure. In TLCTC: the DNS spoofing itself is `#1 Abuse of Functions` (abusing legitimate DNS protocol functionality without exploiting a code flaw). DNS spoofing typically leads to a Man in the Middle position, making the full sequence `#1 → #5`. Note: if the attacker exploits an implementation flaw in a DNS server (e.g., cache poisoning via a code bug), the initial step maps to `#2 Exploiting Server` instead.

**Reference:** V1.9.1 Buzz-Word Refinement (#1)

See also: ARP Spoofing, BGP Hijacking, Man in the Middle (#5)
