---
type: "attack-path"
title: "CHANGE-HEALTHCARE-2024"
description: "ALPHV/BlackCat ransomware attack on Change Healthcare (UnitedHealth Group), February 2024."
resource: "tlctc:attack-path:change-healthcare-2024"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-1"
  - "cluster-7"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.1"
---
# CHANGE-HEALTHCARE-2024

## Attack path

```
#4 →[Δt=~9d] #1 →[Δt=~2d] #1 + [DRE: C] →[Δt=~1d] #7 (FEC) + [DRE: A]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-citrix-credential-use | [#4](/clusters/cluster-4.md) |  | ~9d |  |
| s2-lateral-movement | [#1](/clusters/cluster-1.md) |  | ~2d |  |
| s3-data-exfiltration | [#1](/clusters/cluster-1.md) |  | ~1d | C |
| s4-ransomware-deployment | [#7](/clusters/cluster-7.md) (FEC) |  |  | A |

## Step notes

- **s1-citrix-credential-use:** Attacker authenticated to Change Healthcare's Citrix remote access portal using stolen credentials. The portal did not enforce multi-factor authentication. R-CRED: credential use (authentication) is always #4 regardless of how the credentials were obtained. Per UnitedHealth CEO Andrew Witty's Senate testimony: 'Criminals used compromised credentials to remotely access a Change Healthcare Citrix portal, an application used to enable remote access to desktops. The portal did not have multi-factor authentication.'
- **s2-lateral-movement:** Attacker conducted extensive lateral movement through Change Healthcare's network over approximately 9 days, using legitimate remote access tools, admin utilities, and network protocols. The attacker moved through systems using designed functionality — no exploitation of technical vulnerabilities required after initial access. The generic vulnerability is abuse of legitimate administrative functions.
- **s3-data-exfiltration:** Approximately 6 terabytes of protected health information (PHI) and personally identifiable information (PII) exfiltrated. Data included medical records, insurance claims, payment information, and SSNs of ~100 million individuals. The data transfer used legitimate network functions. DRE: C — massive loss of confidentiality of healthcare data. The exfiltration leveraged designed capabilities, classifying as #1.
- **s4-ransomware-deployment:** ALPHV/BlackCat ransomware deployed, encrypting Change Healthcare systems and disrupting healthcare claims processing nationwide. R-EXEC: ransomware binary is foreign executable content — execution recorded as #7. DRE: A — healthcare payment processing for thousands of providers disrupted for weeks. Axiom III: classify by cause (FEC execution), not by outcome (healthcare disruption). The cascading impact on the US healthcare system was a consequence, not a separate cluster.

# Citations

ALPHV/BlackCat ransomware attack on Change Healthcare (UnitedHealth Group), February 2024. Largest healthcare data breach in US history, affecting ~100 million individuals. Attacker used stolen credentials for a Citrix remote access portal with no MFA. Attack path: #4 →[Δt=~9d] #1 →[Δt=~2d] #1 + [DRE: C] →[Δt=~1d] #7 + [DRE: A]. $22M ransom paid. Sources: UnitedHealth Group CEO testimony to US Senate (May 2024), CISA advisory, HHS breach notification, AHA analysis.
