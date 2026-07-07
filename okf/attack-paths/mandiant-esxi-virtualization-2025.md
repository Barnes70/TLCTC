---
type: "attack-path"
title: "MANDIANT-ESXI-VIRTUALIZATION-2025"
description: "Attack path derived from Mandiant M-Trends 2026 'Adversary Focus on Virtualized Infrastructure' (pp."
resource: "tlctc:attack-path:mandiant-esxi-virtualization-2025"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-1"
  - "cluster-7"
  - "confidence-high"
timestamp: "2026-04-14T00:00:00Z"
tlctc_version: "2.3"
---
# MANDIANT-ESXI-VIRTUALIZATION-2025

## Attack path

```
#4 →[Δt=~2h] #1 + [DRE: C] →[Δt=~10m] #4 →[Δt=~4h] #1 →[Δt=~30m] #4 →[Δt=~15m] #1 →[Δt=~20m] #1 + [DRE: C] →[Δt=~30m] #7 (FEC) + [DRE: Ac]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-initial-access | [#4](/clusters/cluster-4.md) |  | ~2h |  |
| s2a-tier0-credential-acquisition | [#1](/clusters/cluster-1.md) |  | ~10m | C |
| s2b-tier0-credential-use | [#4](/clusters/cluster-4.md) |  | ~4h |  |
| s3-esx-admins-group-manipulation | [#1](/clusters/cluster-1.md) |  | ~30m |  |
| s4-vcenter-auth | [#4](/clusters/cluster-4.md) |  | ~15m |  |
| s5-vmdk-mount | [#1](/clusters/cluster-1.md) |  | ~20m |  |
| s6-ntds-dump | [#1](/clusters/cluster-1.md) |  | ~30m | C |
| s7-esxi-ransomware | [#7](/clusters/cluster-7.md) (FEC) |  |  | Ac |

## Step notes

- **s1-initial-access:** Corporate VPN login via stolen employee credentials. R-CRED / Axiom X: credential application is ALWAYS #4.
- **s2a-tier0-credential-acquisition:** Tier-0 credential acquisition via abuse of legitimate AD/PKI protocols: Kerberoasting (abuse of the Kerberos TGS-REQ function to obtain a service-account hash for offline cracking), DCSync (abuse of the MS-DRSR replication protocol to request credential material from a DC), or ADCS ESC1/ESC4/ESC8 (abuse of legitimate CA enrollment flows to mint a cert for a privileged principal). No exploit, no FEC — designed protocol functions, abused scope → #1. DRE:C on the credential material obtained. Axiom X: credential ACQUISITION maps to the enabling cluster; the subsequent USE is a separate #4 step.
- **s2b-tier0-credential-use:** Authentication as domain admin / Tier-0 principal using the credential material obtained in s2a (cracked service-account password, replicated NT hash, or ADCS-minted certificate via PKINIT). R-CRED / Axiom X: credential application is ALWAYS #4, regardless of how the credential was acquired.
- **s3-esx-admins-group-manipulation:** Abuse of Active Directory group management to add an adversary-controlled account to the ESX Admins AD group. Because vCenter / ESXi honor this group for administrative access (legacy AD integration), group membership change → hypervisor admin. Legitimate AD management function, abused scope. No exploit, no FEC.
- **s4-vcenter-auth:** Authentication to vCenter using the newly-privileged ESX Admins account. R-CRED: credential application is #4. Axiom X: the group-membership change in s3 is the enabling abuse; the credential use here is a separate step.
- **s5-vmdk-mount:** Via vCenter, power off or snapshot the domain controller VM, detach its VMDK, and attach the disk to a new or decommissioned unmanaged VM (one with no EDR agent). All legitimate vCenter administrative operations, abused scope. Intra-system boundary annotation (observational only, does not change classification): |[hypervisor][@vCenter→@UnmanagedVM]|.
- **s6-ntds-dump:** From the unmanaged VM, read NTDS.dit and the SYSTEM registry hive from the mounted disk using standard OS file-read operations (e.g., GoSecretsDump, Impacket). Legitimate OS functions, abused scope. DRE:C — complete Active Directory credential database exfiltrated from outside any managed-endpoint EDR visibility.
- **s7-esxi-ransomware:** Deploy ESXi-only ransomware (FOULFOG.LINUX, INC.LINUX, or similar) to all hypervisors. R-EXEC satisfied: FEC execution on the hypervisor, not on any managed VM. DRE:Ac — VMs present but inaccessible (Accessibility loss). Because no managed endpoint executes the payload, traditional EDR never triggers. Axiom III: ransomware is an outcome class; the #7 classification applies to the payload execution.

# Citations

Attack path derived from Mandiant M-Trends 2026 'Adversary Focus on Virtualized Infrastructure' (pp. 70-73). Illustrates the VMDK-mount credential-dump technique and ESXi-only ransomware (FOULFOG.LINUX, INC.LINUX) that bypasses endpoint EDR entirely. Initial access presumed to be stolen-credential / VPN login consistent with the broader 2025 pattern. Intra-system hypervisor boundary annotated per v2.1 R-INTRA rules — boundaries are observability annotations and do NOT change cluster classification. Sources: M-Trends 2026 pp. 70-73.
