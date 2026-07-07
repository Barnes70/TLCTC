---
type: "attack-path"
title: "LOCKBIT-BYOVD-2023"
description: "LockBit affiliate attack using Bring Your Own Vulnerable Driver (BYOVD) technique, representative of multiple 2023 incidents."
resource: "tlctc:attack-path:lockbit-byovd-2023"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-1"
  - "cluster-3"
  - "cluster-7"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.3"
---
# LOCKBIT-BYOVD-2023

## Attack path

```
#4 →[Δt=~30m] (#1 + #3) →[Δt=~2h] #1 + [DRE: C] →[Δt=~4h] #7 (FEC) + [DRE: C, A]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-rdp-credential-use | [#4](/clusters/cluster-4.md) |  | ~30m |  |
| g1-byovd | [#1](/clusters/cluster-1.md) + [#3](/clusters/cluster-3.md) | | ~2h | |
| s3-data-exfiltration | [#1](/clusters/cluster-1.md) |  | ~4h | C |
| s4-ransomware-deployment | [#7](/clusters/cluster-7.md) (FEC) |  |  | C, A |

## Step notes

- **s1-rdp-credential-use:** LockBit affiliate authenticates via RDP using credentials purchased from an initial access broker (IAB) on dark web marketplaces. R-CRED: credential application (authenticating to RDP) is always #4 regardless of acquisition method. The credential acquisition (by the IAB, via prior compromise) is a separate incident chain. Axiom X: this step records the use of the credential, not its acquisition.
- **g1-byovd:** BYOVD technique: loading and exploiting the vulnerable driver are tightly coupled actions. The #1 step (loading via legitimate mechanism) enables the #3 step (exploiting the driver's vulnerability). Modeled as parallel because they form a single tactical action from the attacker's perspective.
- **s3-data-exfiltration:** With EDR disabled, attacker exfiltrates sensitive data using legitimate file transfer tools (e.g., rclone, MEGAsync, or native SMB/FTP). The tools and protocols function as designed. DRE: C — confidential data stolen for double-extortion. The generic vulnerability is abuse of designed data transfer functionality.
- **s4-ransomware-deployment:** LockBit 3.0 ransomware deployed and executed. R-EXEC: foreign executable content execution recorded as #7 with fec_executed: true. DRE: C (encrypted data may be irrecoverable without key), A (systems rendered inoperable). The BYOVD technique in the prior step ensured no security software would intercept the ransomware deployment.

# Citations

LockBit affiliate attack using Bring Your Own Vulnerable Driver (BYOVD) technique, representative of multiple 2023 incidents. Affiliate purchased RDP credentials from initial access broker, loaded a vulnerable signed driver (e.g., Dell dbutil_2_3.sys or Process Explorer driver) to disable EDR/AV, exfiltrated data, and deployed LockBit ransomware. Attack path: #4 →[Δt=~30m] (#1 + #3) →[Δt=~2h] #1 + [DRE: C] →[Δt=~4h] #7 + [DRE: C, A]. Sources: Sophos X-Ops BYOVD research (2023), Sentinel Labs driver vulnerability reports, CISA #StopRansomware: LockBit 3.0 advisory (AA23-165A).
