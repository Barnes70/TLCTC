---
type: "attack-path"
title: "INFOSTEALER-RANSOMWARE-PIPELINE-2025"
description: "Canonical infostealer-to-ransomware pipeline as described in the Cloudflare 2026 Threat Report."
resource: "tlctc:attack-path:infostealer-ransomware-pipeline-2025"
tags:
  - "attack-path"
  - "cluster-7"
  - "cluster-1"
  - "cluster-4"
  - "confidence-high"
timestamp: "2026-04-09T00:00:00Z"
tlctc_version: "2.3"
---
# INFOSTEALER-RANSOMWARE-PIPELINE-2025

## Attack path

```
#7 (FEC) →[Δt=instant] #1 + [DRE: C] →[Δt=~1d] #4 →[Δt=~2h] #1 + [DRE: C] →[Δt=~2h] #7 (FEC) + [DRE: Ac] →[Δt=~hours] #1
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-infostealer-infection | [#7](/clusters/cluster-7.md) (FEC) |  | instant |  |
| s2-credential-and-token-harvest | [#1](/clusters/cluster-1.md) |  | ~1d | C |
| s3-credential-use-by-ransomware-affiliate | [#4](/clusters/cluster-4.md) |  | ~2h |  |
| s4-lateral-movement-exfil | [#1](/clusters/cluster-1.md) |  | ~2h | C |
| s5a-ransomware-execution | [#7](/clusters/cluster-7.md) (FEC) |  | ~hours | Ac |
| s5b-extortion-demand | [#1](/clusters/cluster-1.md) |  |  |  |

## Step notes

- **s1-infostealer-infection:** Victim system infected with an infostealer (e.g., LummaC2, the premier MaaS example disrupted in May 2025). Initial infection vector varies — drive-by download, malicious email attachment, trojanized software. R-EXEC: foreign executable content executes — recorded as #7 with fec_executed: true. LummaC2 represents the industrialization of data theft: customized malware builds, professional-grade dashboards for managing stolen data.
- **s2-credential-and-token-harvest:** The infostealer harvests credentials for Citrix, Microsoft RDWeb, browser-based VPNs, and critically, active session tokens and cookies. The token theft is the key evolution: it neutralizes standard MFA by capturing already-authenticated session state. The credential sweep uses legitimate browser APIs and filesystem reads — designed functions, abused scope. This is #1 Abuse of Functions. DRE: C — credentials and session tokens exfiltrated. The stolen logs are sold to initial access brokers (IABs) who validate and auction high-value corporate access.
- **s3-credential-use-by-ransomware-affiliate:** Ransomware affiliate purchases validated credentials/tokens from the IAB marketplace and authenticates to the target organization's infrastructure. R-CRED: credential application is always #4. The session tokens bypass MFA entirely — the attacker captures the already-authenticated state and 'logs in rather than breaks in'. This represents the handoff from the infostealer supply chain to the ransomware execution chain. Axiom X: credential acquisition (#1 in s2, enabled by #7 in s1) and credential use (#4 here) are separate steps with separate control surfaces.
- **s4-lateral-movement-exfil:** Ransomware affiliate uses legitimate tools for lateral movement and data exfiltration. GenAI is used in real time to rewrite code that bypasses EDR and map complex network topologies for rapid lateral movement. All tools and protocols function as designed. This is #1 Abuse of Functions. DRE: C — sensitive data exfiltrated for double-extortion leverage. In a majority of observed cases, exfiltrated data is used as ransom leverage while bypassing traditional backup-and-restore defenses.
- **s5a-ransomware-execution:** Ransomware payload deployed and executed across the target network, encrypting critical data. R-EXEC: foreign executable content — #7 with fec_executed: true. DRE: Ac — data present but unusable (encrypted). Axiom III: 'ransomware' is an outcome label; the cause is FEC execution (#7).
- **s5b-extortion-demand:** Extortion demand issued leveraging both the encryption and the exfiltrated data — recorded after the encryption event (the demand presupposes completed encryption / exfil leverage), so #7 → #1 sequential, not a parallel group (§11.2.2 and R-EXEC). The communication channels and payment infrastructure (cryptocurrency) all function as designed — legitimate functionality abused for criminal purposes. Pure extortion (data theft leverage) has become the new standard, often more effective than encryption alone. Manufacturing and critical infrastructure represent over 50% of targets due to the immense cost of operational downtime creating desperate incentive for high-value payouts.

# Citations

Canonical infostealer-to-ransomware pipeline as described in the Cloudflare 2026 Threat Report. This represents the standard operational baseline for the 2026 ransomware ecosystem. The pipeline: (1) Infostealers like LummaC2 harvest credentials for Citrix, Microsoft RDWeb, browser-based VPNs, and live session tokens that bypass MFA. (2) Initial access brokers (IABs) purchase logs from infostealer operators, validate credentials, and auction high-value corporate access. (3) Ransomware affiliates purchase access and execute data theft and direct extortion. Per Verizon DBIR 2025, 54% of all ransomware attacks traced back to infostealer-enabled credential theft. GenAI has compressed attack timelines from days to minutes. Manufacturing and critical infrastructure represent over 50% of targeted attacks. Attack path: #7 -> #4 -> #1 + [DRE: C] -> #7 + [DRE: Ac] -> #1. Sources: Cloudflare 2026 Threat Report (pp. 39-41), Verizon 2025 DBIR, HellCat ransomware breaches (Jaguar Land Rover, Telefonica). AI-GENERATED EXAMPLE: This is a composite/canonical pattern derived from multiple incidents described in the report.
