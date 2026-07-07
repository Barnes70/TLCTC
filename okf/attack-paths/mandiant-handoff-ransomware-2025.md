---
type: "attack-path"
title: "MANDIANT-HANDOFF-RANSOMWARE-2025"
description: "Composite attack path representing the infostealer → initial access broker (IAB) → ransomware-affiliate pipeline described in Mandiant M-Trends 2026 'A Minor Infection Today Can Be a Ransomware Attack Tomorrow' (pp."
resource: "tlctc:attack-path:mandiant-handoff-ransomware-2025"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-7"
  - "cluster-4"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-04-14T00:00:00Z"
tlctc_version: "2.3"
---
# MANDIANT-HANDOFF-RANSOMWARE-2025

## Attack path

```
||[human][@External→@Victim]|| #9 →[Δt=~1h] #7 (FEC) + [DRE: C] →[Δt=<30s] #4 →[Δt=~hours] (#1 + #7)
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-clickfix-lure | [#9](/clusters/cluster-9.md) | \|\|[human][@External→@Victim]\|\| | ~1h |  |
| s2-infostealer-execution | [#7](/clusters/cluster-7.md) (FEC) |  | <30s | C |
| s3-credential-use-vpn | [#4](/clusters/cluster-4.md) |  | ~hours |  |
| g4-recon-and-deploy | [#1](/clusters/cluster-1.md) + [#7](/clusters/cluster-7.md) | |  | |

## Step notes

- **s1-clickfix-lure:** ClickFix / fake-CAPTCHA / fake-software-download lure presented to the victim. Generic vulnerability: human psychological susceptibility. The victim runs an attacker-supplied command or downloads a fake installer. Axiom X note: the credentials harvested downstream belong to the victim; their acquisition is enabled by this social-engineering step.
- **s2-infostealer-execution:** Infostealer (Lumma, RedLine, StealC, or similar) executes on the host. R-EXEC satisfied: FEC execution recorded. The stealer harvests browser-stored credentials, session cookies, VPN profiles, and cryptocurrency wallets within seconds. DRE:C — credential database exfiltrated to a log-market. The stealer is typically short-lived; the host may appear 'clean' minutes later.
- **s3-credential-use-vpn:** After a marketplace hand-off (IAB buys from distributor, ransomware affiliate buys from IAB), a ransomware affiliate authenticates to the victim organization's corporate VPN or remote access gateway using stolen credentials. R-CRED / Axiom X: credential application is ALWAYS #4, regardless of how the credential was acquired. The <30s metric is the time between credential landing in the log market and first interactive login. No MFA challenge because the stolen session cookie or VPN profile bypassed it.
- **g4-recon-and-deploy:** Parallel group: the affiliate typically runs abuse-of-functions recon (#1) concurrently with or immediately before the ransomware detonation (#7). Modeled as parallel because the two capabilities execute in overlapping minutes, not as strict sequence.

# Citations

Composite attack path representing the infostealer → initial access broker (IAB) → ransomware-affiliate pipeline described in Mandiant M-Trends 2026 'A Minor Infection Today Can Be a Ransomware Attack Tomorrow' (pp. 55-59). Three distinct actors: (1) the stealer distributor, (2) the IAB credential aggregator, (3) the ransomware affiliate. Hand-off time between credential harvest and affiliate login observed at <30 seconds in 2025 cases. Prior compromise / stolen-credential pathways were the #1 ransomware initial access vector (30%). Sources: M-Trends 2026 pp. 29-37 (ransomware chapter), pp. 55-59 (hand-off article).
