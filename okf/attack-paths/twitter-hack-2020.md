---
type: "attack-path"
title: "TWITTER-HACK-2020"
description: "Twitter account takeover attack, July 15, 2020."
resource: "tlctc:attack-path:twitter-hack-2020"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-4"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.1"
---
# TWITTER-HACK-2020

## Attack path

```
||[human][@External→@Twitter]|| #9 →[Δt=~10m] #4 →[Δt=~5m] #1 →[Δt=~30m] #4 + [DRE: C] →[Δt=~5m] #1 + [DRE: I]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-employee-vishing | [#9](/clusters/cluster-9.md) | \|\|[human][@External→@Twitter]\|\| | ~10m |  |
| s2-employee-credential-use | [#4](/clusters/cluster-4.md) |  | ~5m |  |
| s3-admin-tool-access | [#1](/clusters/cluster-1.md) |  | ~30m |  |
| s4-account-takeover | [#4](/clusters/cluster-4.md) |  | ~5m | C |
| s5-bitcoin-scam-posting | [#1](/clusters/cluster-1.md) |  |  | I |

## Step notes

- **s1-employee-vishing:** Attackers conducted phone-based social engineering (vishing) targeting Twitter employees, posing as IT department staff. They convinced employees to enter their credentials on a fake internal VPN login page. #9 Social Engineering: the generic vulnerability is human psychological susceptibility — authority impersonation (posing as IT), urgency, and trust in internal-sounding communications. The boundary crossing is via the human context from external attackers into Twitter's employee domain.
- **s2-employee-credential-use:** Attacker used stolen employee credentials to authenticate to Twitter's internal VPN and corporate systems. R-CRED: credential use (VPN authentication) = always #4. Axiom X: credentials were acquired via social engineering (#9); their application to authenticate is a separate #4 step.
- **s3-admin-tool-access:** Attacker navigated Twitter's internal network to access the 'agent tool' — an internal administration panel used by support staff for account management. The tool was accessible to the authenticated employee and functioned as designed. #1 Abuse of Functions: the attacker used legitimate internal navigation and tool access capabilities within the scope of the stolen employee credentials.
- **s4-account-takeover:** Attacker used the admin tool to reset email addresses and disable two-factor authentication on 130 high-profile accounts (Barack Obama, Joe Biden, Elon Musk, Bill Gates, Apple, Uber, etc.), effectively stealing those account identities. #4 Identity Theft: the attacker took control of user accounts by modifying their authentication parameters — this is identity theft at the application level. DRE: C — access to private Direct Messages of compromised accounts. The admin tool's account modification function was used to commit identity theft.
- **s5-bitcoin-scam-posting:** Attacker posted Bitcoin scam tweets from the 130 compromised high-profile accounts ('Send Bitcoin to this address and I'll double it'). The tweet posting API functioned as designed — the attacker had valid session control over the accounts. #1 Abuse of Functions: the legitimate tweet posting function was used to publish fraudulent content. DRE: I — integrity of the accounts' public communications compromised. ~$120K in Bitcoin collected from victims of the scam.

# Citations

Twitter account takeover attack, July 15, 2020. Attackers (led by teenager Graham Ivan Clark) vished Twitter employees to gain access to internal admin tools, then took over 130 high-profile accounts (Obama, Musk, Gates, Apple, etc.) to post Bitcoin scam messages. ~$120K in Bitcoin collected. Attack path: #9 ||[human][@External→@Twitter]|| →[Δt=~10m] #4 →[Δt=~5m] #1 →[Δt=~30m] #4 + [DRE: C] →[Δt=~5m] #1 + [DRE: I]. Sources: Twitter official blog post (July 2020), NYDFS investigation report, DOJ criminal complaint against Graham Ivan Clark, Florida State Attorney indictment.
