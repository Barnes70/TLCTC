---
type: "attack-path"
title: "CLUMSYTOAD-SNAKEDISK-2025"
description: "ClumsyToad (Mustang Panda/BASIN/Earth Preta) SnakeDisk USB worm campaign targeting Thailand, September 2025."
resource: "tlctc:attack-path:clumsytoad-snakedisk-2025"
tags:
  - "attack-path"
  - "cluster-8"
  - "cluster-7"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-04-09T00:00:00Z"
tlctc_version: "2.1"
---
# CLUMSYTOAD-SNAKEDISK-2025

## Attack path

```
||[physical][@ClumsyToad→@ThaiGov]|| #8 →[Δt=?] #7 (FEC) →[Δt=instant] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-usb-introduction | [#8](/clusters/cluster-8.md) | \|\|[physical][@ClumsyToad→@ThaiGov]\|\| | ? |  |
| s2-snakedisk-execution | [#7](/clusters/cluster-7.md) (FEC) |  | instant |  |
| s3-yokai-backdoor-operations | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-usb-introduction:** Infected USB removable drive is introduced into a Thai government or police facility. The physical boundary crossing is the #8 step — the attack vector crosses from the external physical domain into the target organization's physical infrastructure. The USB drive carries the SnakeDisk worm. The mechanism of initial USB introduction (dropped, planted, shared) is not specified in the report. Bridge cluster: #8 crosses the physical domain boundary.
- **s2-snakedisk-execution:** SnakeDisk USB worm executes on the target system. The worm includes a geofence check — it only executes on Thailand-based IP addresses, ensuring operational targeting discipline. R-EXEC: foreign executable content executes — recorded as #7 with fec_executed: true. Upon execution, SnakeDisk deploys the Yokai backdoor and begins propagation to other removable drives connected to the host.
- **s3-yokai-backdoor-operations:** The Yokai backdoor establishes persistence and uses legitimate system tools and protocols for C2, data collection, and exfiltration. ClumsyToad's broader tradecraft in 2025 moved to Windows Management Console (.msc) files to exploit inherent trust in system-signed management files, bypassing EDR LotL detections. The C2, lateral movement, and data collection all leverage designed system capabilities. This is #1 Abuse of Functions: legitimate administrative tools and OS capabilities used within designed parameters but abused scope. DRE: C — intelligence collection from Thai government and police infrastructure.

# Citations

ClumsyToad (Mustang Panda/BASIN/Earth Preta) SnakeDisk USB worm campaign targeting Thailand, September 2025. Cloudforce One identified a novel USB worm geofenced to execute exclusively on Thailand-based IP addresses. SnakeDisk propagates via infected removable drives to deploy the Yokai backdoor, specifically targeting Thai government and police infrastructure. ClumsyToad also moved from standard .lnk files to Windows Management Console (.msc) files to bypass EDR LotL detections. Attack path: #8 ||[physical][@External->@ThaiGov]|| -> #7 -> #1 + [DRE: C]. Sources: Cloudflare 2026 Threat Report (pp. 20), Cloudforce One.
