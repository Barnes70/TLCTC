---
type: "mapping-set"
title: "ATT&CK techniques → #5 Man in the Middle"
description: "3 ATT&CK techniques entries mapped to TLCTC #5 Man in the Middle."
resource: "tlctc:mapping:attack:cluster-5"
tags:
  - "mapping"
  - "attack"
  - "cluster-5"
---
# ATT&CK techniques → #5 Man in the Middle

> Source: MITRE ATT&CK Enterprise → TLCTC mapping (`mappings/mitre-attack-enterprise/`).

Mapped entries: **3**. Cluster: [#5 Man in the Middle](/clusters/cluster-5.md).

| Technique | Name | TLCTC | Rationale |
|---|---|---|---|
| T1557 | Adversary-in-the-Middle | #5 | Adversary-in-the-Middle positioning to intercept, relay, or modify traffic. Generic vulnerability is trust placed in network-path integrity — `#5`. In Collection context, intercepted traffic that contains data yields `[DRE: C]` at the interception step. |
| T1557.004 | Adversary-in-the-Middle: Evil Twin | #5 | Evil Twin: rogue Wi-Fi AP impersonates a legitimate SSID; clients associate to the attacker AP — direct AiTM (`#5`). `[DRE: C]` for intercepted traffic. |
| T1659 | Content Injection | #5 → #7 | Attacker injects malicious content into network traffic between @Org clients and legitimate destinations — typically from a Man-in-the-Middle position (compromised intermediate device, ISP-level interception, hostile transit network, malicious Wi-Fi). The injection step is `#5`; the injected content executing on the @Org client is `#7` per R-EXEC. Path: `#5 \|\|[network][@External→@Org]\|\| → #7`. (When the injection exploits a client-side flaw to gain execution, insert `→ #3` between `#5` and `#7`.) |
