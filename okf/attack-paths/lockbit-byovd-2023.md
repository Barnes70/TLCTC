---
type: "attack-path"
title: "LOCKBIT-BYOVD-2023"
description: "LockBit affiliate attack using Bring Your Own Vulnerable Driver (BYOVD) technique, representative of multiple 2023 incidents."
resource: "tlctc:attack-path:lockbit-byovd-2023"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-1"
  - "cluster-7"
  - "cluster-2"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.6"
---
# LOCKBIT-BYOVD-2023

## Attack path

```
#4 →[Δt=~30m] #1 →[Δt=instant] #7 (FEC) →[Δt=instant] #2 →[Δt=~2h] #1 + [DRE: C] →[Δt=~4h] #7 (FEC) + [DRE: Ac]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-rdp-credential-use | [#4](/clusters/cluster-4.md) |  | ~30m |  |
| s2a-driver-load | [#1](/clusters/cluster-1.md) |  | instant |  |
| s2b-edr-killer-exec | [#7](/clusters/cluster-7.md) (FEC) |  | instant |  |
| s2c-driver-exploit | [#2](/clusters/cluster-2.md) |  | ~2h |  |
| s3-data-exfiltration | [#1](/clusters/cluster-1.md) |  | ~4h | C |
| s4-ransomware-deployment | [#7](/clusters/cluster-7.md) (FEC) |  |  | Ac |

## Step notes

- **s1-rdp-credential-use:** LockBit affiliate authenticates via RDP using credentials purchased from an initial access broker (IAB) on dark web marketplaces. R-CRED: credential application (authenticating to RDP) is always #4 regardless of acquisition method. The credential acquisition (by the IAB, via prior compromise) is a separate incident chain. Axiom X: this step records the use of the credential, not its acquisition.
- **s2a-driver-load:** With the administrative session from s1, the attacker installs a legitimately signed but vulnerable kernel driver (e.g., Dell dbutil_2_3.sys, Process Explorer's PROCEXP152.sys) through the standard Windows service/driver-loading mechanism. The loader works as designed - it accepts the driver because it carries a valid signature - so the generic vulnerability is abuse of a designed function (#1). No flaw is exploited in this step. Loading and exploiting are ordered (load, then exploit), so they are sequential steps, not a parallel group.
- **s2b-edr-killer-exec:** The attacker's EDR-killer tool (e.g., AuKill or Terminator-style tooling) executes and opens the driver's device interface. R-EXEC: attacker-supplied executable content runs, so a #7 step is recorded at the execution moment. The tool is the client that sends the malicious IOCTLs in s2c.
- **s2c-driver-exploit:** The killer sends crafted IOCTLs that the vulnerable driver mis-processes (arbitrary memory read/write or unrestricted process termination), terminating EDR/AV processes from kernel mode. R-ROLE: the driver services requests from a user-mode process, so it holds the SERVER role -> #2 (same reasoning as the CVE-2025-21333 ruling; corrected from #3 on 2026-10-04). A code flaw in the driver is exploited, which distinguishes this step from the #1 load in s2a. R-INTRA-7: the admin->kernel privilege crossing is an observability annotation, not a classification input.
- **s3-data-exfiltration:** With EDR disabled, attacker exfiltrates sensitive data using legitimate file transfer tools (e.g., rclone, MEGAsync, or native SMB/FTP). The tools and protocols function as designed. DRE: C — confidential data stolen for double-extortion. The generic vulnerability is abuse of designed data transfer functionality.
- **s4-ransomware-deployment:** LockBit 3.0 ransomware deployed and executed. R-EXEC: foreign executable content execution recorded as #7 with fec_executed: true. DRE: Ac - the encrypted data is still present but unusable (Axiom III: "ransomware" is the outcome label, the cluster is the FEC execution). The confidentiality loss belongs to the exfiltration in s3, not to the encryption. The BYOVD segment (s2a-s2c) ensured no security software would intercept the ransomware deployment.

# Citations

LockBit affiliate attack using Bring Your Own Vulnerable Driver (BYOVD) technique, representative of multiple 2023 incidents. Affiliate purchased RDP credentials from initial access broker, loaded a vulnerable signed driver (e.g., Dell dbutil_2_3.sys or Process Explorer driver) to disable EDR/AV, exfiltrated data, and deployed LockBit ransomware. Attack path: #4 →[Δt=~30m] #1 →[Δt=instant] #7 →[Δt=instant] #2 |[privilege][@admin→@kernel]| →[Δt=~2h] #1 + [DRE: C] →[Δt=~4h] #7 + [DRE: Ac]. Sources: Sophos X-Ops BYOVD research (2023), Sentinel Labs driver vulnerability reports, CISA #StopRansomware: LockBit 3.0 advisory (AA23-165A). v2.6 requalification (2026-09-23): checked against the v2.6 changes - #10 subversion test (planting counts as subversion), federation (#4 unless the identity provider was subverted), successes only, the data-vs-code boundary and the R-SPECIFIC consolidation - classification unchanged. Correction (2026-10-04): the BYOVD segment was previously modelled as a parallel group (#1 + #3). Three fixes: (1) a kernel driver that services IOCTLs from a user-mode process holds the SERVER role (R-ROLE; same reasoning as the CVE-2025-21333 ruling), so exploiting it is #2, not #3; (2) the order is known - the driver is loaded first, then exploited - so the steps are sequential, never parallel; (3) the IOCTLs are sent by an attacker-supplied EDR-killer tool, whose execution is FEC and must be recorded as #7 (R-EXEC). The ransomware step's DRE was [DRE: C, A]; encrypted data is present but unusable, so it is [DRE: Ac] (the confidentiality loss is the exfiltration step's DRE).
