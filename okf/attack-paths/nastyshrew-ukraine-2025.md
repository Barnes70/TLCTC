---
type: "attack-path"
title: "NASTYSHREW-UKRAINE-2025"
description: "NastyShrew (Gamaredon/Primitive Bear/UAC-0010/Aqua Blizzard) persistent campaigns targeting Ukrainian government and critical infrastructure, 2025."
resource: "tlctc:attack-path:nastyshrew-ukraine-2025"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-7"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-04-09T00:00:00Z"
tlctc_version: "2.3"
---
# NASTYSHREW-UKRAINE-2025

## Attack path

```
||[email][@NastyShrew→@UkrainianGov]|| #9 →[Δt=~1h] #7 (FEC) →[Δt=~5m] #1 →[Δt=~30m] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-phishing-delivery | [#9](/clusters/cluster-9.md) | \|\|[email][@NastyShrew→@UkrainianGov]\|\| | ~1h |  |
| s2-vbscript-chain-execution | [#7](/clusters/cluster-7.md) (FEC) |  | ~5m |  |
| s3-dead-drop-c2-resolution | [#1](/clusters/cluster-1.md) |  | ~30m |  |
| s4-persistent-access-exfil | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-phishing-delivery:** High-frequency phishing campaigns targeting Ukrainian government agencies and critical infrastructure operators. Emails deliver .lnk shortcut files and .ps1 PowerShell scripts as initial access vectors. NastyShrew casts a wide net — volume over precision. The human boundary crossing is the #9 step: the victim must interact with the malicious attachment.
- **s2-vbscript-chain-execution:** The .lnk/.ps1 file triggers a multi-stage VBScript chain from the Pteranodon malware family. R-EXEC: foreign executable content executes — recorded as #7 with fec_executed: true. The VBScript stages are progressively decoded and executed, establishing the initial foothold.
- **s3-dead-drop-c2-resolution:** Infected host polls legitimate paste sites (teletype.in, rentry.co) to retrieve the current C2 tunnel address. NastyShrew uses these dead drop resolvers (DDR) to rotate backend infrastructure in minutes. This is #1 Abuse of Functions: the paste sites' read APIs function exactly as designed — intended for text sharing, abused for C2 address distribution. The traffic resolves to benign-looking domains, complicating detection. The VPS infrastructure behind the C2 is configured with strict firewall rules permitting only inbound traffic from Ukrainian IP ranges (geofencing).
- **s4-persistent-access-exfil:** NastyShrew maintains persistent access on thousands of Ukrainian endpoints. Data collection and exfiltration uses legitimate system tools and network capabilities — standard API calls, file reads, and data transfer protocols. This is #1: the tools and protocols function as designed; the scope is abused. DRE: C — intelligence collection from Ukrainian government systems supporting battlefield operations. The persistence model is maintain-and-rotate: infrastructure is expected to be disrupted, so NastyShrew purchases new domains and hosting quickly, using cryptocurrency for anonymity.

# Citations

NastyShrew (Gamaredon/Primitive Bear/UAC-0010/Aqua Blizzard) persistent campaigns targeting Ukrainian government and critical infrastructure, 2025. One of the most active and persistent Russian threats. Characterized by high-frequency campaigns maintaining persistence on thousands of endpoints. Infrastructure: dead drop resolvers on paste sites (teletype.in, rentry.co) for C2 tunnel rotation, geofencing to Ukrainian IP ranges, VPS purchased with cryptocurrency. Delivery: high-frequency phishing with .lnk and .ps1 files triggering multi-stage VBScript chains (Pteranodon family). Members arrested in Thailand (Phuket) in February and November 2025 in joint US/Thai operations. Attack path: #9 ||[email][@External->@Org]|| -> #7 -> #1 -> #1 + [DRE: C]. Sources: Cloudflare 2026 Threat Report (pp. 16), CERT-UA, Cloudforce One.
