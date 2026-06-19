---
type: "attack-path"
title: "ROTTENSHREW-SIGNAL-2025"
description: "RottenShrew (UAC-0185/Lost Potential/UNC4221) Signal device-linking campaign, 2025."
resource: "tlctc:attack-path:rottenshrew-signal-2025"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-4"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-04-09T00:00:00Z"
tlctc_version: "2.1"
---
# ROTTENSHREW-SIGNAL-2025

## Attack path

```
||[human][@RottenShrew→@UkrainianMilitary]|| #9 →[Δt=~5m] #4 →[Δt=~1m] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-kropyva-impersonation | [#9](/clusters/cluster-9.md) | \|\|[human][@RottenShrew→@UkrainianMilitary]\|\| | ~5m |  |
| s2-signal-device-linking | [#4](/clusters/cluster-4.md) |  | ~1m |  |
| s3-geolocation-and-collection | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-kropyva-impersonation:** RottenShrew impersonates the Kropyva application (Ukrainian artillery guidance system) through phishing campaigns targeting Ukrainian military personnel. The lure exploits operational trust — military users expect to interact with Kropyva-related resources. Additional impersonated targets include the Delta military app, Teneta tactical modem sites, Diia government services, and e-Cherha border crossing service. The human boundary crossing is the #9 step: psychological manipulation through brand impersonation of trusted military tools.
- **s2-signal-device-linking:** Victims are enticed to link their Signal accounts to RottenShrew-controlled instances using a custom Signal Phish Kit. The device-linking mechanism is a legitimate Signal feature — it functions as designed. R-CRED: the victim's Signal session/identity is the credential being captured and applied. The linking gives RottenShrew full access to communications and metadata. Axiom X: the credential acquisition occurred through #9 (social engineering); the credential application (session linking) is #4.
- **s3-geolocation-and-collection:** RottenShrew deploys PINPOINT, a lightweight JavaScript payload using the browser's Geolocation API to extract high-accuracy coordinates of victims. MESHAGENT (legitimate RMM tool) provides persistence and live screen monitoring. Signal metadata and communications are collected. This is #1 Abuse of Functions: the browser Geolocation API, MESHAGENT's remote management capabilities, and Signal's message retrieval all operate within designed parameters. DRE: C — geolocation data, communications content, and device metadata collected. The geolocation capability indicates potential overlap with kinetic targeting — reconnaissance for physical military operations. This temporal correlation between digital espionage and conventional military action is a defining characteristic of RottenShrew operations.

# Citations

RottenShrew (UAC-0185/Lost Potential/UNC4221) Signal device-linking campaign, 2025. Specialized reconnaissance unit focused on geolocation of Ukrainian military personnel, likely followed by kinetic action. The campaign mimicked the Kropyva application (a proprietary Ukrainian artillery guidance system) to entice military users to link their Signal accounts to RottenShrew-controlled instances. Also targeted Delta (military app), Teneta-related sites (tactical modem/blue force tracking), Diia (digital government), and e-Cherha (border crossing service). Tools: PINPOINT (JS geolocation payload using browser Geolocation API), MESHAGENT (RMM for persistence), custom Signal Phish Kit. Attack path: #9 ||[human][@External->@UkrainianMilitary]|| -> #4 -> #1 + [DRE: C]. Sources: Cloudflare 2026 Threat Report (pp. 18), CERT-UA.
