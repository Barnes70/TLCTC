---
type: "attack-path"
title: "DARKHOTEL-WIFI-2014"
description: "DarkHotel APT campaign targeting business executives via luxury hotel WiFi networks, documented by Kaspersky in November 2014 (active since ~2007)."
resource: "tlctc:attack-path:darkhotel-wifi-2014"
tags:
  - "attack-path"
  - "cluster-8"
  - "cluster-9"
  - "cluster-5"
  - "cluster-7"
  - "cluster-4"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.5"
---
# DARKHOTEL-WIFI-2014

## Attack path

```
(#8 + #9) →[Δt=instant] #5 →[Δt=~5m] #7 (FEC) + [DRE: C] →[Δt=~1h] #4 →[Δt=~2h] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| g1-hotel-access | [#8](/clusters/cluster-8.md) + [#9](/clusters/cluster-9.md) | | instant | |
| s2-traffic-interception | [#5](/clusters/cluster-5.md) |  | ~5m |  |
| s3-fake-update-execution | [#7](/clusters/cluster-7.md) (FEC) |  | ~1h | C |
| s4-credential-capture | [#4](/clusters/cluster-4.md) |  | ~2h |  |
| s5-corporate-data-exfiltration | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **g1-hotel-access:** Parallel exploitation: physical compromise of hotel infrastructure (#8) combined with the guest's trust in the hotel environment (#9). Both are required for the attack — the physical access enables network control, and the social trust brings the victim onto the compromised network.
- **s2-traffic-interception:** Man-in-the-middle position established on the hotel network. Attacker intercepts the victim's HTTP traffic and injects fake software update prompts (e.g., Adobe Flash Player, Google Toolbar) into web pages the executive visits. #5 MitM: the generic vulnerability is the ability to intercept and modify communications between two parties. The attacker is positioned between the victim and the internet, actively manipulating traffic content.
- **s3-fake-update-execution:** Victim accepts the fake software update prompt; a digitally signed trojan (keylogger + backdoor) downloads and executes. The malware was signed with stolen or fraudulent code-signing certificates to appear legitimate. R-EXEC: foreign executable content executed — recorded as #7 with fec_executed: true. The victim believed they were installing a legitimate software update due to the MitM-injected prompt. [DRE: C] is recorded here: the keylogger component captures the executive's credentials for corporate email, VPN and other services. Per Axiom X the acquisition of credential material maps to the enabling cluster, which is this #7 step, so the confidentiality event belongs here and not on the #4 step that later presents those credentials.
- **s4-credential-capture:** The attacker uses the captured credentials to authenticate to corporate resources. R-CRED: credential use (authentication with captured credentials) = always #4. Axiom X: the credentials were acquired via the malware's keylogger function during s3 (enabling cluster #7), where their confidentiality event is recorded; their application to authenticate is this separate #4 step and carries no DRE of its own. The corporate data disclosure that this access enables is recorded on s5, where the data is actually taken.
- **s5-corporate-data-exfiltration:** Attacker uses compromised credentials and backdoor access to exfiltrate corporate documents, emails, strategic plans, and sensitive business data from the executive's accounts and corporate network. The access uses legitimate APIs and file transfer functions. DRE: C — proprietary business intelligence and corporate secrets exfiltrated. #1 Abuse of Functions: all accessed systems function as designed; the attacker operates with stolen but technically valid credentials.

# Citations

DarkHotel APT campaign targeting business executives via luxury hotel WiFi networks, documented by Kaspersky in November 2014 (active since ~2007). Attackers compromised hotel WiFi infrastructure to MitM executive guests, injecting fake software update prompts that delivered digitally signed malware (keylogger/backdoor). Targeted luxury hotels in Asia. Attack path: (#8 + #9) →[Δt=instant] #5 →[Δt=~5m] #7 + [DRE: C] →[Δt=~1h] #4 →[Δt=~2h] #1 + [DRE: C]. Sources: Kaspersky Lab 'DarkHotel' report (November 2014), Kaspersky SecureList APT analysis, ESET DarkHotel follow-up research.
