---
type: "attack-path"
title: "BOT-CHAIN-LIFECYCLE-2025"
description: "Triple-threat bot chain lifecycle as described by Cloudforce One (Cloudflare 2026 Threat Report)."
resource: "tlctc:attack-path:bot-chain-lifecycle-2025"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-1"
  - "cluster-7"
  - "cluster-6"
  - "confidence-medium"
timestamp: "2026-04-09T00:00:00Z"
tlctc_version: "2.1"
---
# BOT-CHAIN-LIFECYCLE-2025

## Attack path

```
#4 →[Δt=instant] #1 + [DRE: C] →[Δt=~1h] #7 (FEC) →[Δt=~1d] #6 + [DRE: A]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-automated-credential-stuffing | [#4](/clusters/cluster-4.md) |  | instant |  |
| s2-account-takeover-exploitation | [#1](/clusters/cluster-1.md) |  | ~1h | C |
| s3-host-compromise-botnet-enrollment | [#7](/clusters/cluster-7.md) (FEC) |  | ~1d |  |
| s4-ddos-infrastructure-disruption | [#6](/clusters/cluster-6.md) |  |  | A |

## Step notes

- **s1-automated-credential-stuffing:** Bots weaponize compromised credentials at industrial scale — automated account takeover (ATO). Credential databases are fed by a circular ecosystem of harvesting sites and infostealers (Qakbot, Emotet). Bots test stolen username/password pairs across thousands of sites per second. Cloudflare data: 94% of all login attempts originate from bots; 63% of human logins use previously compromised credentials. R-CRED: the use of stolen credentials to authenticate is always #4. Attack tools (Selenium, Puppeteer) mimic human mouse movements and realistic scrolling to bypass session intelligence during credential stuffing. Botnets tunnel through residential proxy services (Aisuru, Kimwolf) to make traffic appear legitimate.
- **s2-account-takeover-exploitation:** Once credentials are validated, bots exploit the compromised accounts to extract data systematically. This includes targeting LLM interfaces — bots interact with LLMs to exploit input handling vulnerabilities or extract proprietary training data and generated content. Standard API calls, data export functions, and search queries all function as designed. This is #1 Abuse of Functions. DRE: C — systematic extraction of account data, proprietary information, and LLM-stored content. This novel LLM interface targeting bypasses traditional network security by leveraging public-facing AI endpoints.
- **s3-host-compromise-botnet-enrollment:** Compromised hosts are enrolled into botnets through malware deployment. Infrastructure provided by massive distributed botnets (911 S5, Mantis using hijacked VMs, Aisuru with 1-4M infected hosts). R-EXEC: foreign executable content executes — #7 with fec_executed: true. The botnet agent provides the attacker with persistent control and the ability to redirect the host's resources for the final phase.
- **s4-ddos-infrastructure-disruption:** The botnet power used for access is turned into a weapon of destruction. Denial-of-service attacks represent the final link — the transition from stealthy exploitation to massive infrastructure bombardment. Aisuru reached 31.4 Tbps peaks; Kimwolf operated 550+ C2 nodes. Beyond volumetric floods, bots target specific high-cost application functions (complex search queries) to exhaust CPU/memory with minimal traffic. DRE: A — availability destroyed. This pivot marks the shift in the threat actor's endgame: when access is no longer enough, they weaponize the entire bot chain for total operational blackout.

# Citations

Triple-threat bot chain lifecycle as described by Cloudforce One (Cloudflare 2026 Threat Report). Three phases: (1) Identity exploitation — automated credential stuffing using compromised credential databases, with 94% of all login attempts originating from bots and 63% of human logins involving previously compromised credentials. Tools like Selenium and Puppeteer mimic human behavior to bypass detection. (2) Host compromise — secured footholds escalated to systematic data extraction, including targeting LLM interfaces for proprietary data theft. Infrastructure: botnets like 911 S5 (dismantled) and Mantis (hijacked VMs). (3) Infrastructure disruption — botnet power turned into DDoS weapons (Aisuru, Kimwolf). ~30% of all HTTP traffic observed by Cloudflare originates from bots. Attack path: #4 -> #1 + [DRE: C] -> #7 -> #6 + [DRE: A]. Sources: Cloudflare 2026 Threat Report (pp. 42-43). AI-GENERATED EXAMPLE: This is a composite/canonical pattern derived from the report's bot chain lifecycle description.
