---
type: "attack-path"
title: "AISURU-DDOS-2025"
description: "Aisuru botnet hyper-volumetric DDoS attacks, 2025."
resource: "tlctc:attack-path:aisuru-ddos-2025"
tags:
  - "attack-path"
  - "cluster-7"
  - "cluster-6"
  - "confidence-high"
timestamp: "2026-04-09T00:00:00Z"
tlctc_version: "2.1"
---
# AISURU-DDOS-2025

## Attack path

```
#7 (FEC) →[Δt=?] #6 + [DRE: A]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-botnet-propagation | [#7](/clusters/cluster-7.md) (FEC) |  | ? |  |
| s2-hyper-volumetric-ddos | [#6](/clusters/cluster-6.md) |  |  | A |

## Step notes

- **s1-botnet-propagation:** Aisuru botnet malware propagates to and executes on 1-4 million hosts (estimated), comprising IoT devices, compromised servers, and residential systems. R-EXEC: foreign executable content executes on each infected host — recorded as #7 with fec_executed: true. The botnet infrastructure masks attack sources by tunneling through residential proxy services, making malicious traffic appear to originate from legitimate users. The successor Kimwolf network continues the botnet's infrastructure after disruption efforts. Botnet propagation is itself a complex multi-step process (scanning, exploitation, payload delivery), but modeled here as a single #7 step representing the aggregate FEC execution across the botnet fleet.
- **s2-hyper-volumetric-ddos:** The Aisuru botnet launches hyper-volumetric DDoS attacks, peaking at 31.4 Tbps (November 2025 record — massive UDP flood). The attack physically exhausts target organizations' network capacity. This is #6 Flooding Attack: the generic vulnerability is the finite capacity of network resources overwhelmed by volume. DRE: A — availability destroyed. Most attacks peak in seconds and conclude within 10 minutes, effectively closing the window for human intervention. The sheer scale represents a democratization of massive attack capability — even mid-tier actors can now launch hyper-volumetric attacks that were once nation-state exclusive. Beyond volumetric floods, modern bots also target specific high-cost application functions (complex search queries) to exhaust CPU/memory with minimal traffic.

# Citations

Aisuru botnet hyper-volumetric DDoS attacks, 2025. Record-breaking 31.4 Tbps UDP flood in November 2025, nearly six times the peak volume of 2024's largest attack. Cloudflare observed 47.1 million DDoS attacks in 2025 (more than doubled from 2024), mitigating 5,376 attacks per hour. Aisuru and its successor Kimwolf control an estimated 1-4 million infected hosts. 19 new world records in 2025. Most attacks lasted less than 10 minutes, closing the window for human intervention. Successor network Kimwolf saw 550+ C2 nodes null-routed in early 2026. Botnets tunnel through residential proxy services to make traffic appear legitimate. Attack path: #7 -> #6 + [DRE: A]. Sources: Cloudflare 2026 Threat Report (pp. 42-45), Cloudflare DDoS quarterly reports.
