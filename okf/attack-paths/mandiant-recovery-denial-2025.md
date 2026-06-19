---
type: "attack-path"
title: "MANDIANT-RECOVERY-DENIAL-2025"
description: "Composite attack path for the 'recovery denial' ransomware pattern from Mandiant M-Trends 2026 'Ransomware is Now a Resilience Problem' (pp."
resource: "tlctc:attack-path:mandiant-recovery-denial-2025"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-1"
  - "cluster-7"
  - "confidence-high"
timestamp: "2026-04-14T00:00:00Z"
tlctc_version: "2.0"
---
# MANDIANT-RECOVERY-DENIAL-2025

## Attack path

```
#4 →[Δt=~1d] #1 + [DRE: C] →[Δt=~10m] #4 →[Δt=~6h] #1 + [DRE: Av] →[Δt=~4h] #1 →[Δt=~2h] #1 →[Δt=~1h] #7 (FEC) + [DRE: Ac]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-credential-access | [#4](/clusters/cluster-4.md) |  | ~1d |  |
| s2a-tier0-credential-acquisition | [#1](/clusters/cluster-1.md) |  | ~10m | C |
| s2b-tier0-credential-use | [#4](/clusters/cluster-4.md) |  | ~6h |  |
| s3-backup-infrastructure-abuse | [#1](/clusters/cluster-1.md) |  | ~4h | Av |
| s4-fleet-management-abuse | [#1](/clusters/cluster-1.md) |  | ~2h |  |
| s5-virtualization-plane-abuse | [#1](/clusters/cluster-1.md) |  | ~1h |  |
| s6-ransomware-detonation | [#7](/clusters/cluster-7.md) (FEC) |  |  | Ac |

## Step notes

- **s1-credential-access:** Initial access: affiliate logs in to corporate VPN / Citrix / RDP using stolen employee credentials (sourced from a prior infostealer infection or log-market purchase). R-CRED / Axiom X: credential application is ALWAYS #4. MFA bypass typically via stolen session cookie or legacy VPN profile.
- **s2a-tier0-credential-acquisition:** Tier-0 credential acquisition via abuse of legitimate AD/PKI protocols: Kerberoasting (abuse of Kerberos TGS-REQ for a crackable service-ticket hash), DCSync (abuse of MS-DRSR replication to request credential material from a DC), or ADCS ESC1/ESC4/ESC8 (abuse of CA enrollment to mint a cert for a privileged principal). Designed protocol functions, abused scope → #1, not #4. DRE:C — the Tier-0 credential set is the crown jewels. Axiom X: acquisition cluster (#1) is independent of the later credential use (#4).
- **s2b-tier0-credential-use:** Authentication as domain admin / Tier-0 principal using the material obtained in s2a (cracked service password, replicated NT hash, or ADCS-minted certificate via PKINIT). R-CRED / Axiom X: credential application is ALWAYS #4.
- **s3-backup-infrastructure-abuse:** Abuse of legitimate backup-management functions: delete backup catalogs, expire retention, destroy cloud-backup tenants (Veeam, Rubrik, Commvault). Legitimate management APIs, abused scope. No exploit, no FEC. DRE:Av — backups made unavailable. This step is the strategic core of recovery denial.
- **s4-fleet-management-abuse:** Abuse of fleet-management tooling (Intune, SCCM, GPO): stage a scheduled task / software package that will push the ransomware payload to every managed endpoint. Using trusted deployment plumbing ensures delivery without tripping EDR prevention. Legitimate function, abused scope.
- **s5-virtualization-plane-abuse:** vCenter access and VM power-off / VMDK manipulation in preparation for hypervisor-level ransomware. Legitimate vCenter administrative functions, abused scope. Modeled in this path to show that AD-integrated hypervisors share the same Tier-0 identity compromise as backup and fleet management — this is why the 'single compromise, three-pillar blast radius' pattern exists.
- **s6-ransomware-detonation:** Coordinated ransomware detonation across endpoints (via s4), file servers, backup appliances (via s3), and ESXi hypervisors (via s5). R-EXEC satisfied: FEC execution recorded at every encryption event. DRE:Ac — data present but inaccessible (Accessibility loss, not Availability — the bytes are on disk, but the decryption key is held by the attacker). Axiom III: ransomware is an outcome class; the #7 classification applies to the payload execution, not to the word 'ransomware'.

# Citations

Composite attack path for the 'recovery denial' ransomware pattern from Mandiant M-Trends 2026 'Ransomware is Now a Resilience Problem' (pp. 60-65). Operators systematically target the three pillars that enable recovery — backup infrastructure, identity services (AD/ADCS), and virtualization management (vCenter) — before detonation. Objective: deny the victim any non-ransom path back to operations. Initial access via stolen credentials (infostealer-sourced or prior compromise) is most common; this path models that variant. Sources: M-Trends 2026 pp. 60-65.
