---
type: "term"
title: "SSL Stripping"
description: "A MitM technique where an attacker downgrades HTTPS connections to HTTP by intercepting and modifying communication between client and server."
resource: "tlctc:term:ssl-stripping"
tags:
  - "glossary"
---
# SSL Stripping

A MitM technique where an attacker downgrades HTTPS connections to HTTP by intercepting and modifying communication between client and server. In TLCTC: SSL stripping is an action performed from a MitM position and maps to `#5 Man in the Middle` (exploiting the controlled communication path to perform a protocol downgrade). The attacker must already have the MitM position (gained via `#1` ARP spoofing, `#8` physical access, etc.), making the full sequence e.g., `#1 → #5`.

**Reference:** V1.9.1 Buzz-Word Refinement (#1)

See also: Man in the Middle (#5), ARP Spoofing, Position Acquisition vs Position Exploitation
