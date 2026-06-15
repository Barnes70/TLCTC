---
type: "attack-path"
title: "PEGASUS-FORCEDENTRY-2021"
description: "NSO Group Pegasus spyware delivered via FORCEDENTRY zero-click exploit, 2021."
resource: "tlctc:attack-path:pegasus-forcedentry-2021"
tags:
  - "attack-path"
  - "cluster-3"
  - "cluster-7"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.1"
---
# PEGASUS-FORCEDENTRY-2021

## Attack path

```
#3 →[Δt=instant] #7 (FEC) →[Δt=instant] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-imessage-exploit | [#3](/clusters/cluster-3.md) |  | instant |  |
| s2-pegasus-install | [#7](/clusters/cluster-7.md) (FEC) |  | instant |  |
| s3-surveillance-exfiltration | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-imessage-exploit:** Zero-click exploit of CoreGraphics integer overflow vulnerability (CVE-2021-30860) in iOS iMessage attachment processing. A malicious PDF file (disguised with .gif extension) was sent via iMessage and automatically processed by the IMTranscoderAgent sandboxed process. The exploit used a novel JBIG2-based Turing-complete computational oracle to escape the BlastDoor sandbox. R-ROLE: iMessage/CoreGraphics is client-side software that receives and processes attacker-controlled content = #3. Intra-system boundary annotation: sandbox escape from IMTranscoderAgent to OS context. R-INTRA-7: the sandbox escape does not change the cluster classification — it remains #3. The zero-click nature means no social engineering (#9) is involved — the vulnerability is purely technical.
- **s2-pegasus-install:** Pegasus spyware installed and executed on the device following sandbox escape. The spyware establishes persistence and begins its surveillance module initialization. R-EXEC: foreign executable content (Pegasus implant) executed — recorded as #7 with fec_executed: true. The spyware is a distinct piece of foreign code, separate from the exploit that delivered it.
- **s3-surveillance-exfiltration:** Pegasus abuses legitimate iOS APIs and device capabilities for comprehensive surveillance: microphone recording, camera access, GPS location tracking, message reading (iMessage, WhatsApp, Signal), email access, call logs, and keychain data. All accessed through designed OS interfaces — the spyware operates as a privileged application abusing legitimate device functions. DRE: C — total loss of confidentiality of device data and communications. The surveillance capabilities are abuse of designed functions (#1), not exploitation of additional vulnerabilities.

# Citations

NSO Group Pegasus spyware delivered via FORCEDENTRY zero-click exploit, 2021. Targeted iMessage on iOS. Malicious PDF disguised as GIF exploited integer overflow in CoreGraphics (CVE-2021-30860) within the sandboxed IMTranscoderAgent process, escaped BlastDoor sandbox, and installed Pegasus spyware. Zero user interaction required. Attack path: #3 |[sandbox][@IMTranscoderAgent→@os]| →[Δt=instant] #7 →[Δt=instant] #1 + [DRE: C]. Sources: Citizen Lab FORCEDENTRY report (September 2021), Apple security update for CVE-2021-30860, Google Project Zero JBIG2 exploit analysis.
