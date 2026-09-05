---
type: "term"
title: "Loss of Control / System Compromise"
description: "The Compromise type of the System Risk Event (SRE) — the central event in the Cyber Bow Tie model — representing the point at which an actor achieves unauthorized control over a system's behavior, privileges, data, or trust relationships."
resource: "tlctc:term:loss-of-control-system-compromise"
tags:
  - "glossary"
---
# Loss of Control / System Compromise

The **Compromise type** of the System Risk Event (SRE) — the central event in the Cyber Bow-Tie model — representing the point at which an actor achieves unauthorized control over a system's behavior, privileges, data, or trust relationships. Since v2.5 the SRE has two types at one altitude: Compromise (this entry; the only type the ten clusters reach) and System Failure (loss of function, no actor). This serves as the pivot point between threat realization (cause) and potential consequences (effect). The SRE is the first event in the consequence chain: **SRE → DRE → BRE\***. Some attacks may have delayed data risk events (creating a detection window), while others lead to immediate data risk events. Examples: A server exploit (#2) enabling remote code execution leading to malware (#7) represents loss of control before any data breach occurs. In contrast, successful SQL injection (#2) can immediately result in Loss of Confidentiality.

**Reference:** §6.3 (Central Event), §6.3.1 (The Consequence Chain)

See also: System Risk Event (SRE), Data Risk Event (DRE), Business Risk Event (BRE)
