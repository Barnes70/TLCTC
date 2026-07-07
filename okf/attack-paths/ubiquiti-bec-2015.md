---
type: "attack-path"
title: "UBIQUITI-BEC-2015"
description: "Business Email Compromise (BEC) attack on Ubiquiti Networks, June 2015."
resource: "tlctc:attack-path:ubiquiti-bec-2015"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.3"
---
# UBIQUITI-BEC-2015

## Attack path

```
||[human][@External→@Ubiquiti]|| #9 →[Δt=~2h] #1 + [DRE: I]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-executive-impersonation | [#9](/clusters/cluster-9.md) | \|\|[human][@External→@Ubiquiti]\|\| | ~2h |  |
| s2-fraudulent-wire-transfer | [#1](/clusters/cluster-1.md) |  |  | I |

## Step notes

- **s1-executive-impersonation:** Attacker sent emails impersonating Ubiquiti senior executives and external entities, requesting urgent wire transfers to overseas accounts. Used spoofed email addresses or lookalike domains to create the appearance of legitimate executive communication. #9 Social Engineering: the generic vulnerability is human psychological susceptibility — authority bias (impersonating C-suite executives), urgency (framing requests as time-sensitive), and trust in email as an authentic communication channel. The boundary crossing is via the human context: the attacker manipulates the employees' perception of the communication's source. No technical system was compromised — the attack is entirely against human judgment.
- **s2-fraudulent-wire-transfer:** Finance department employees initiated wire transfers totaling $46.7M to attacker-controlled overseas bank accounts using the company's legitimate banking and payment systems. The wire transfer systems, banking APIs, and financial authorization processes all functioned exactly as designed — no technical vulnerability was exploited. #1 Abuse of Functions: the legitimate financial transfer capability was used for unauthorized payments. DRE: I — integrity of financial transactions compromised; the transactions were technically valid but fraudulently authorized. This demonstrates that BEC attacks require no technical sophistication — the entire attack exploits human trust and legitimate business processes.

# Citations

Business Email Compromise (BEC) attack on Ubiquiti Networks, June 2015. Attackers impersonated Ubiquiti executives and third-party entities via email, tricking finance department employees into making fraudulent wire transfers totaling $46.7M to overseas accounts ($14.9M later recovered). No malware, no system exploitation — purely social engineering combined with abuse of legitimate financial processes. Attack path: #9 ||[human][@External→@Ubiquiti]|| →[Δt=~2h] #1 + [DRE: I]. Sources: Ubiquiti Networks SEC 10-Q filing (August 2015), FBI IC3 BEC advisories, Krebs on Security reporting.
