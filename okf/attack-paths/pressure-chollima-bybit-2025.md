---
type: "attack-path"
title: "PRESSURE-CHOLLIMA-BYBIT-2025"
description: "PRESSURE CHOLLIMA's supply chain compromise of Safe{Wallet} to steal $1.46 billion USD from Bybit (February 2025), the largest cryptocurrency theft in history."
resource: "tlctc:attack-path:pressure-chollima-bybit-2025"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-7"
  - "cluster-4"
  - "cluster-1"
  - "cluster-10"
  - "confidence-high"
timestamp: "2026-04-16T00:00:00Z"
tlctc_version: "2.1"
---
# PRESSURE-CHOLLIMA-BYBIT-2025

## Attack path

```
||[human][@PressureChollima→@SafeWallet-Dev]|| #9 →[Δt=?] #7 (FEC) + [DRE: C] →[Δt=?] #4 →[Δt=?] #1 + [DRE: I] →[Δt=?] ||[update][@SafeWallet→@Bybit]|| #10 →[Δt=instant] #1 + [DRE: C, I] →[Δt=instant] #1
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-se-developer | [#9](/clusters/cluster-9.md) | \|\|[human][@PressureChollima→@SafeWallet-Dev]\|\| | ? |  |
| s2-trojanized-python-exec | [#7](/clusters/cluster-7.md) (FEC) |  | ? | C |
| s3-cloud-auth | [#4](/clusters/cluster-4.md) |  | ? |  |
| s4-code-injection | [#1](/clusters/cluster-1.md) |  | ? | I |
| s5-supply-chain-tae | [#10](/clusters/cluster-10.md) | \|\|[update][@SafeWallet→@Bybit]\|\| | instant |  |
| s6-fund-redirect | [#1](/clusters/cluster-1.md) |  | instant | C, I |
| s7-anti-forensics | [#1](/clusters/cluster-1.md) |  |  |  |

## Step notes

- **s1-se-developer:** PRESSURE CHOLLIMA delivers a trojanized Python project to a Safe{Wallet} software developer, 'likely delivered using social engineering tactics' (CrowdStrike). DPRK-nexus adversaries routinely use fake job assessments and collaboration requests to target developers. This is #9 Social Engineering: the developer is manipulated into engaging with and executing the malicious project. Boundary crossing: the attack traverses from the external attacker sphere through the human trust boundary into the Safe{Wallet} development environment.
- **s2-trojanized-python-exec:** The trojanized Python project executes on the Safe{Wallet} developer's workstation. R-EXEC: foreign executable content runs — recorded as #7 with fec_executed: true. The malware locates and exfiltrates development-related credentials from the compromised machine. DRE: C — Safe{Wallet} development credentials (cloud infrastructure access) are exposed to an unauthorized party. These credentials enable the subsequent pivot from the developer's machine to Safe{Wallet}'s production cloud environment.
- **s3-cloud-auth:** Attacker authenticates to Safe{Wallet}'s cloud infrastructure using the exfiltrated development credentials. R-CRED: credential application (authentication) is always #4 regardless of acquisition method. Axiom X (Credential Duality): credentials were acquired via #7 (s2, malware execution as enabling cluster); their use to authenticate is a separate #4 step. This pivot from a developer workstation to cloud infrastructure is the critical escalation point — a single compromised developer account yields access to the production frontend.
- **s4-code-injection:** From the authenticated cloud session, PRESSURE CHOLLIMA injects two elements into Safe{Wallet}'s production frontend: (1) malicious JavaScript code that activates during Bybit-specific transactions, and (2) a smart contract containing customized transfer logic that executes exclusively for transactions between Bybit's contract address and an adversary-controlled address. This is #1 Abuse of Functions: the attacker uses legitimate cloud deployment and code management capabilities to modify production code. DRE: I — the integrity of Safe{Wallet}'s trusted frontend codebase is compromised, transforming a legitimate digital asset management platform into an attack delivery mechanism targeting a specific customer.
- **s5-supply-chain-tae:** Trust Acceptance Event: Bybit initiates a routine transaction between its own wallets through Safe{Wallet}'s web interface, loading the compromised frontend. R-SUPPLY: #10 is placed at the moment the trust artifact — Safe{Wallet}'s frontend code containing the injected malicious JavaScript — becomes authoritative inside Bybit's operational context. Bybit trusts Safe{Wallet} as its digital asset management platform; this vendor trust relationship is the supply chain vector. The malicious JavaScript executes within the trusted application context during transaction processing. Boundary crossing: compromised code crosses from the vendor sphere into Bybit's transaction processing context via the trust relationship.
- **s6-fund-redirect:** The adversary's smart contract executes on the blockchain, applying customized transfer logic that redirects cryptocurrency then valued at $1.46 billion USD from Bybit's wallets to an adversary-controlled wallet address. This is #1 Abuse of Functions: the blockchain's smart contract execution mechanism operates exactly as designed — the contract processes the transaction per its programmed logic, but that logic was engineered by the attacker to redirect funds. DRE: I — the integrity of Bybit's financial transaction is compromised (destination modified). DRE: C — Bybit's cryptocurrency holdings are exposed to and captured by an unauthorized party. This constitutes the largest cryptocurrency theft in history and a major DPRK-nexus revenue generation event.
- **s7-anti-forensics:** Immediately following the theft, PRESSURE CHOLLIMA restores the malicious JavaScript hosted on Safe{Wallet}'s cloud instance to its original, legitimate version. This is #1 Abuse of Functions: the attacker again uses legitimate cloud deployment capabilities, this time for anti-forensic cleanup. The rapid restoration demonstrates operational sophistication — the adversary had pre-planned the rollback procedure, minimizing the window during which the compromised frontend was detectable.

# Citations

PRESSURE CHOLLIMA's supply chain compromise of Safe{Wallet} to steal $1.46 billion USD from Bybit (February 2025), the largest cryptocurrency theft in history. The adversary compromised a Safe{Wallet} developer's machine via a trojanized Python project (likely social engineering), exfiltrated development credentials, pivoted to Safe{Wallet}'s cloud infrastructure, and injected malicious JavaScript and a customized smart contract into the frontend. When Bybit performed a routine wallet transaction through Safe{Wallet}, the malicious logic modified the transaction to redirect funds to an attacker-controlled wallet. The adversary immediately restored the original JavaScript post-theft for anti-forensics. Attack path: #9 ||[human][@PressureChollima→@SafeWallet-Dev]|| →[Δt=?] #7 + [DRE: C] →[Δt=?] #4 →[Δt=?] #1 + [DRE: I] →[Δt=?] #10 ||[update][@SafeWallet→@Bybit]|| →[Δt=instant] #1 + [DRE: C, I] →[Δt=instant] #1. Source: CrowdStrike 2026 Global Threat Report, pp. 31-32, Figure 16.
