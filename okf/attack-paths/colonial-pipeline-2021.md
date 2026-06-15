---
type: "attack-path"
title: "COLONIAL-PIPELINE-2021"
description: "DarkSide ransomware attack on Colonial Pipeline, May 2021."
resource: "tlctc:attack-path:colonial-pipeline-2021"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-1"
  - "cluster-7"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.1"
---
# COLONIAL-PIPELINE-2021

## Attack path

```
#4 →[Δt=~7d] #1 →[Δt=~2h] #1 + [DRE: C] →[Δt=~4h] #7 (FEC) + [DRE: A]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-vpn-credential-use | [#4](/clusters/cluster-4.md) |  | ~7d |  |
| s2-lateral-movement | [#1](/clusters/cluster-1.md) |  | ~2h |  |
| s3-data-exfiltration | [#1](/clusters/cluster-1.md) |  | ~4h | C |
| s4-ransomware-deployment | [#7](/clusters/cluster-7.md) (FEC) |  |  | A |

## Step notes

- **s1-vpn-credential-use:** Attacker authenticated to Colonial Pipeline's legacy VPN using a compromised password. The VPN account was not protected by multi-factor authentication. The password was likely obtained from a prior breach or dark web credential dump (password reuse). R-CRED: credential application (use to authenticate) is always #4 regardless of acquisition method. The credential acquisition occurred outside this incident's scope (prior breach); this step records the use.
- **s2-lateral-movement:** Attacker used legitimate administrative tools and remote management capabilities to move laterally through Colonial Pipeline's IT network over approximately 7 days. Living-off-the-land techniques — the tools and protocols functioned as designed. The generic vulnerability is abuse of legitimate functionality: remote desktop, file shares, and management consoles all operated within their designed parameters.
- **s3-data-exfiltration:** Approximately 100GB of data exfiltrated from Colonial Pipeline's network using legitimate data transfer tools and protocols. The exfiltration leveraged designed network capabilities — no exploitation of a technical vulnerability. DRE: C — confidential business data stolen for double-extortion leverage. Axiom III: the cause is abuse of designed data transfer functions, not the outcome (extortion).
- **s4-ransomware-deployment:** DarkSide ransomware deployed and executed across Colonial Pipeline's IT systems, encrypting critical data and rendering systems inoperable. R-EXEC: foreign executable content (ransomware binary) executed — recorded as #7 with fec_executed: true. DRE: A — pipeline operations shut down for 6 days. Axiom III: 'ransomware' is an outcome label; the generic vulnerability is execution of foreign executable content (#7). The business decision to shut down OT systems was a consequence of the IT encryption, not a separate attack step.

# Citations

DarkSide ransomware attack on Colonial Pipeline, May 2021. Largest fuel pipeline in the US shut down for 6 days, causing fuel shortages across the US East Coast. Attacker used a compromised VPN password (no MFA, likely from a prior breach). Attack path: #4 →[Δt=~7d] #1 →[Δt=~2h] #1 + [DRE: C] →[Δt=~4h] #7 + [DRE: A]. $4.4M ransom paid (DOJ later recovered $2.3M). Sources: Mandiant incident report, CISA Alert AA21-131A, Bloomberg reporting, DOJ Bitcoin recovery announcement.
