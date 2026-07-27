---
type: "attack-path"
title: "RACCOON-PHAAS-AITM-2025"
description: "RaccoonO365 Phishing-as-a-Service (PhaaS) adversary-in-the-middle (AitM) campaign, disrupted by Cloudforce One in 2025."
resource: "tlctc:attack-path:raccoon-phaas-aitm-2025"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-5"
  - "cluster-4"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-04-09T00:00:00Z"
tlctc_version: "2.3"
---
# RACCOON-PHAAS-AITM-2025

## Attack path

```
||[email][@PhaaS-Operator→@Victim]|| #9 →[Δt=~5m] #5 →[Δt=instant] #4 →[Δt=~1h] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-phaas-phishing-delivery | [#9](/clusters/cluster-9.md) | \|\|[email][@PhaaS-Operator→@Victim]\|\| | ~5m |  |
| s2-aitm-session-interception | [#5](/clusters/cluster-5.md) |  | instant |  |
| s3-token-replay-authentication | [#4](/clusters/cluster-4.md) |  | ~1h |  |
| s4-data-harvesting | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-phaas-phishing-delivery:** Industrialized phishing email delivery via RaccoonO365 mailer bots. The PhaaS infrastructure provides: automated rotation of clean residential proxies and warm IP addresses to bypass reputation-based filters; high-fidelity real-time brand impersonation templates (Microsoft 365, Google, Kraken, Gemini) virtually indistinguishable from legitimate logins; CAPTCHA-based human verification gates; browser fingerprinting and anti-analysis scripts that disable browser consoles. This is #9 Social Engineering: the victim must navigate to the phishing page and enter credentials — human psychological susceptibility to brand trust. The PhaaS infrastructure industrializes the delivery but doesn't change the generic vulnerability.
- **s2-aitm-session-interception:** The PhaaS kit deploys an adversary-in-the-middle (AitM) proxy that sits transparently between the victim and the legitimate service (e.g., Microsoft 365). As the victim authenticates through the proxy, it captures the live session token — the already-authenticated session state — in real time. This is #5 Man in the Middle: the attacker intercepts the communication between the victim and the legitimate service by positioning the phishing infrastructure as an intermediary. The generic vulnerability is the interception of data in transit between two parties. The MFA challenge is passed through to the real service and completed normally; the proxy captures the resulting session token.
- **s3-token-replay-authentication:** Attacker replays the captured session token to authenticate as the victim to Microsoft 365, OneDrive, SharePoint, or other services. R-CRED: the use of stolen session tokens to authenticate is always #4 Identity Theft. Axiom X: token acquisition (#5 MitM in s2) and token use (#4 here) are separate steps. This effectively neutralizes standard MFA — the attacker has the already-authenticated session. The shift from 'attacking the box' to 'attacking the session' makes ransomware deployment 'a simple login event'.
- **s4-data-harvesting:** Using the authenticated session, the attacker harvests credentials, cookies, and data from Microsoft 365, OneDrive, and SharePoint. All data access uses legitimate API endpoints and designed functionality. This is #1 Abuse of Functions: the Microsoft 365 APIs operate within their designed parameters; the scope is abused by an unauthorized session. DRE: C — exfiltration of corporate data, enabling wide-scale financial fraud and extortion. The PhaaS operators often abuse legitimate cloud infrastructure to shield backend servers, making the attack appear to originate from a trusted network.

# Citations

RaccoonO365 Phishing-as-a-Service (PhaaS) adversary-in-the-middle (AitM) campaign, disrupted by Cloudforce One in 2025. Industrialized phishing pipeline marketed as no-downtime Telegram-based mailer bots with tiered subscriptions ($355/30 days). Features: 100% inbox delivery via automated rotation of clean residential proxies, turnkey brand impersonation (Google, Microsoft 365, Kraken, Gemini), CAPTCHA-based human verification, browser fingerprinting, and anti-analysis scripts. Critical capability: AitM integration that acts as transparent proxy between victim and legitimate service, harvesting live session tokens to bypass MFA. The captured already-authenticated session state turns ransomware into 'a simple login event'. Attack path: #9 ||[email][@External->@Org]|| -> #5 -> #4 -> #1 + [DRE: C]. Sources: Cloudflare 2026 Threat Report (pp. 35-36), Cloudforce One RaccoonO365 disruption.
