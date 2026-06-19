---
type: "mapping-set"
title: "ATT&CK techniques → #10 Supply Chain Attack"
description: "5 ATT&CK techniques entries mapped to TLCTC #10 Supply Chain Attack."
resource: "tlctc:mapping:attack:cluster-10"
tags:
  - "mapping"
  - "attack"
  - "cluster-10"
---
# ATT&CK techniques → #10 Supply Chain Attack

> Source: MITRE ATT&CK Enterprise → TLCTC mapping (`mappings/mitre-attack-enterprise/`).

Mapped entries: **5**. Cluster: [#10 Supply Chain Attack](/clusters/cluster-10.md).

| Technique | Name | TLCTC | Rationale |
|---|---|---|---|
| T1195 | Supply Chain Compromise | #10 | Parent for supply-chain compromise. The threat is realized at the **Trust Acceptance Event** — the moment the trust artifact (signed update, package, hardware, vendor binary) becomes authoritative inside @Org. R-SUPPLY: #10 is placed at the TAE, not at the upstream compromise. Sub-techniques specify the vector (.001 development tooling, .002 update channel, .003 hardware). |
| T1195.001 | Supply Chain Compromise: Compromise Software Dependencies and Development Tools | #10.2 → #7 | Compromise of a software dependency or development tool: malicious code is introduced upstream, then enters @Org build/runtime when the dependency is pulled or the dev tool is used. TAE is when @Org's build accepts and integrates the dependency. After integration, attacker code executes — #7 per R-EXEC. Path: `#10.2 \|\|[dev][@Vendor→@Org]\|\| → #7`. |
| T1195.002 | Supply Chain Compromise: Compromise Software Supply Chain | #10.1 → #7 | Compromise of a software update channel: malicious update is signed/distributed through the trusted update mechanism. TAE is when @Org installs the update. Post-install, attacker code executes — #7 per R-EXEC. Path: `#10.1 \|\|[update][@Vendor→@Org]\|\| → #7`. |
| T1195.003 | Supply Chain Compromise: Compromise Hardware Supply Chain | #10.3 → #7 | Compromise of the hardware supply chain: malicious firmware or implants are introduced before the device reaches @Org. TAE is when @Org powers on / accepts the device into its environment. Implant code executes — #7 per R-EXEC. Path: `#10.3 \|\|[physical][@Vendor→@Org]\|\| → #7`. |
| T1199 | Trusted Relationship | #10 → #7 | A trusted partner (MSP, contractor, business partner, federated tenant) is compromised; their access into @Org is honored at the trust boundary. TAE is the moment @Org accepts the partner's connection/session/credential as authoritative — #10 per R-SUPPLY. Follow-on activity is typically execution (#7) of attacker code carried in via the trusted channel. Path: `#10 \|\|[trust][@Vendor→@Org]\|\| → #7`. (The follow-on may be #1 or #4 instead of #7 in cases where the attacker uses partner-granted access purely for function abuse or further auth.) |
