---
type: "term"
title: "Loss of Control / System Compromise"
description: "The System Risk Event (SRE) the framework defines — the central event in the Cyber Bow Tie model — representing the point at which an actor achieves unauthorized control over a system's behavior, privileges, data, or trust relationships."
resource: "tlctc:term:loss-of-control-system-compromise"
tags:
  - "glossary"
---
# Loss of Control / System Compromise

The System Risk Event (SRE) the framework defines — the central event in the Cyber Bow-Tie model — representing the point at which an actor achieves unauthorized control over a system's behavior, privileges, data, or trust relationships. It is the only event the ten clusters reach; other events at the same altitude with no actor holding capability (System Failure foremost) are operational risk. This serves as the pivot point between threat realization (cause) and potential consequences (effect); one is recorded per cluster step, so a multi-step path chains them. The SRE is the first event in the consequence chain: **SRE → DRE → BRE\***. Some attacks may have delayed data risk events (creating a detection window), while others lead to immediate data risk events. Examples: A server exploit (#2) enabling remote code execution leading to malware (#7) represents loss of control before any data breach occurs. In contrast, successful SQL injection (#2) can immediately result in Loss of Confidentiality.

**Reference:** Handbook §6.3 (Central Event), §6.3.1 (The Consequence Chain); Core paper §3.4

See also: System Risk Event (SRE), Data Risk Event (DRE), Business Risk Event (BRE)
