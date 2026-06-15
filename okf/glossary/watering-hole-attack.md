---
type: "term"
title: "Watering Hole Attack"
description: "An attack where an adversary compromises a website frequently visited by the target group, then uses the compromised site to deliver exploits or malware to visitors."
resource: "tlctc:term:watering-hole-attack"
tags:
  - "glossary"
---
# Watering Hole Attack

An attack where an adversary compromises a website frequently visited by the target group, then uses the compromised site to deliver exploits or malware to visitors. In TLCTC: the attack decomposes into multiple steps depending on the method:

- Compromising the website: maps to its own cluster (e.g., `#2 Exploiting Server`, `#4 Identity Theft`)
- Luring users to visit: `#9 Social Engineering` (if actively lured) or implicit via the site's normal traffic
- Exploiting visitor's browser: `#3 Exploiting Client`
- Delivering malware: `#7 Malware`

Typical sequence: `#3 → #7` (for the victim's perspective) or the full chain from attacker's perspective.

**Reference:** V1.9.1 Buzz-Word Refinement (#3)

See also: Exploiting Client (#3), Drive-By Download, Malvertising
