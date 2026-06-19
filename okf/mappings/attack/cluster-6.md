---
type: "mapping-set"
title: "ATT&CK techniques → #6 Flooding Attack"
description: "8 ATT&CK techniques entries mapped to TLCTC #6 Flooding Attack."
resource: "tlctc:mapping:attack:cluster-6"
tags:
  - "mapping"
  - "attack"
  - "cluster-6"
---
# ATT&CK techniques → #6 Flooding Attack

> Source: MITRE ATT&CK Enterprise → TLCTC mapping (`mappings/mitre-attack-enterprise/`).

Mapped entries: **8**. Cluster: [#6 Flooding Attack](/clusters/cluster-6.md).

| Technique | Name | TLCTC | Rationale |
|---|---|---|---|
| T1498 | Network Denial of Service | #6 | Network DoS exhausts @Org network bandwidth or upstream capacity through high-volume traffic. Generic vulnerability is finite capacity overwhelmed by volume — #6 Flooding Attack. Outcome `[DRE: A]` — legitimate traffic cannot reach @Org services. Path: `#6 + [DRE: A]`. |
| T1498.001 | Network Denial of Service: Direct Network Flood | #6 | Direct flood: attacker (or botnet) sends traffic from `@External` toward `@Org` capacity. #6 Flooding Attack. Path: `#6 \|\|[network][@External→@Org]\|\| + [DRE: A]`. |
| T1498.002 | Reflection Amplification | #6 | Reflection/amplification: attacker spoofs source IP to direct response traffic from third-party reflectors (DNS, NTP, memcached) to `@Org`. The reflectors are transit/carriers, not the source or target — use the transit operator. #6 Flooding Attack. Path: `#6 \|\|[network][@External⇒@Reflectors→@Org]\|\| + [DRE: A]`. |
| T1499 | Endpoint Denial of Service | #6 | Endpoint DoS exhausts host-level resources (sockets, threads, memory, application worker pools) through high request volume. #6 Flooding Attack. Outcome `[DRE: A]`. Path: `#6 + [DRE: A]`. |
| T1499.001 | OS Exhaustion Flood | #6 | OS exhaustion (TCP connection table, conntrack, ephemeral ports, kernel buffers) via volume. #6 Flooding Attack. Path: `#6 + [DRE: A]`. |
| T1499.002 | Endpoint Denial of Service: Service Exhaustion Flood | #6 | Service-layer exhaustion (worker thread pools, connection limits, service-specific resources) via volume. #6 Flooding Attack. Path: `#6 + [DRE: A]`. |
| T1499.003 | Endpoint Denial of Service: Application Exhaustion Flood | #6 | Application-logic exhaustion (expensive endpoints, search/aggregation, cryptographic operations triggered by requests) via volume. #6 Flooding Attack. Path: `#6 + [DRE: A]`. |
| T1667 | Email Bombing | #6 | Email bombing overwhelms a recipient mailbox or upstream mail processing through high-volume messages, typically to bury security alerts or deny legitimate use. Generic vulnerability is finite capacity overwhelmed by volume — #6 Flooding Attack. Cluster corrected from prior `#1 \| #7`: the threat is volumetric, not function-abuse or malware-execution at the receive side (the send side may use abused mail APIs, but that is a separate upstream step). Outcome `[DRE: A]` — mailbox or mail processing unavailable for legitimate use. Path: `#6 \|\|[email][@External→@Org]\|\| + [DRE: A]`. |
