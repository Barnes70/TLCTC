---
type: "attack-path"
title: "UBIQUITI-BEC-2015"
description: "Business Email Compromise (BEC) attack on Ubiquiti Networks, June 2015."
resource: "tlctc:attack-path:ubiquiti-bec-2015"
tags:
  - "attack-path"
  - "cluster-9"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.5"
---
# UBIQUITI-BEC-2015

## Attack path

```
||[human][@External→@Ubiquiti]|| #9 + [DRE: I]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-executive-impersonation | [#9](/clusters/cluster-9.md) | \|\|[human][@External→@Ubiquiti]\|\| |  | I |

## Step notes

- **s1-executive-impersonation:** Attacker sent emails impersonating Ubiquiti senior executives and external entities, requesting urgent wire transfers to overseas accounts. Used spoofed email addresses or lookalike domains to create the appearance of legitimate executive communication. #9 Social Engineering: the generic vulnerability is human psychological susceptibility — authority bias (impersonating C-suite executives), urgency (framing requests as time-sensitive), and trust in email as an authentic communication channel. The boundary crossing is via the human context: the attacker manipulates the employees' perception of the communication's source. No technical system was compromised — the attack is entirely against human judgment. V2.5 R-SCOPE: this is the only Attack-row step in the incident. The wire transfer that followed was carried out by entitled employees acting without intent to defraud (Error in Use), which carries no cluster and no SRE, so it is not a step; see metadata notes. [DRE: I] is recorded here because the deception is the proximate cause of the fraudulently authorised transactions — technically valid, wrongly authorised.

# Citations

Business Email Compromise (BEC) attack on Ubiquiti Networks, June 2015. Attackers impersonated Ubiquiti executives and third-party entities via email, tricking finance department employees into making fraudulent wire transfers totaling $46.7M to overseas accounts ($14.9M later recovered). No malware, no system exploitation — purely social engineering combined with abuse of legitimate financial processes. Attack path: #9 ||[human][@External→@Ubiquiti]|| + [DRE: I]. V2.5 R-SCOPE determination (2026-09-09): the record previously carried a second step, #1, for the wire transfer itself. That step has been removed. The transfer was performed by the deceived finance employees, who were entitled to operate the payment system and did not intend the fraudulent outcome; question 2 of the cause-side partition places that action in Error in Use — operational risk, no cluster. It also produced no System Risk Event: the banking systems obeyed and did not fail, so there is no system-altitude event to record as a step. The attacker never touched the payment system, so no Attack-row action occurred there. The deception is the whole of the attack, and [DRE: I] now attaches to it. Sources: Ubiquiti Networks SEC 10-Q filing (August 2015), FBI IC3 BEC advisories, Krebs on Security reporting.
