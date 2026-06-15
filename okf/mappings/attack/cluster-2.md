---
type: "mapping-set"
title: "ATT&CK techniques → #2 Exploiting Server"
description: "7 ATT&CK techniques entries mapped to TLCTC #2 Exploiting Server."
resource: "tlctc:mapping:attack:cluster-2"
tags:
  - "mapping"
  - "attack"
  - "cluster-2"
---
# ATT&CK techniques → #2 Exploiting Server

> Source: MITRE ATT&CK Enterprise → TLCTC mapping (`mappings/mitre-attack-enterprise/`).

Mapped entries: **7**. Cluster: [#2 Exploiting Server](/clusters/cluster-2.md).

| Technique | Name | TLCTC | Rationale |
|---|---|---|---|
| T1068 | Exploitation for Privilege Escalation | (#2 \| #3) → #7 | Exploitation for Privilege Escalation: trigger an implementation flaw in a higher-privileged component to gain elevated execution. Server-role flaw (kernel processing user-mode input, hypervisor processing guest input, privileged daemon) → `#2`; client-role flaw (privileged user-mode component processing crafted input) → `#3`. Successful exploitation results in attacker-controlled code running at higher privilege — `#7` per R-EXEC. Path: `(#2 \| #3) → #7`. Cluster corrected from prior `#2 \| #3` (which omitted the `#7` step that is the entire point of PrivEsc exploitation). |
| T1190 | Exploit Public-Facing Application | #2 | Internet-facing application (web server, API gateway, network service) processes attacker-crafted input that triggers a server-side implementation flaw (injection, deserialization, auth bypass, RCE). Server-role component is the flawed party — #2 per R-ROLE. Path: `#2 \|\|[api][@External→@Org]\|\|`. When the exploit drops or executes attacker code, append `→ #7` per R-EXEC. |
| T1210 | Exploitation of Remote Services | #2 | Exploiting an implementation flaw in a remote service (SMB, RDP, SSH daemon, database server, container runtime, hypervisor management plane) for lateral movement. The flawed component is in server role — `#2` per R-ROLE. Path: `#2`. When successful exploitation drops or executes attacker code, append `→ #7` per R-EXEC. |
| T1211 | Exploitation for Defense Evasion | (#2 \| #3) → #7 | Exploitation for Defense Evasion: trigger an implementation flaw in a defensive component (EDR agent, AV engine, kernel security feature, sandbox) to disable or bypass it. Server-role flaw → `#2`; client-role → `#3`. Successful exploitation runs attacker code at the privilege of the defensive component or its kernel hooks — `#7` per R-EXEC. Cluster corrected from prior `#2 \| #3` (which omitted the `→ #7` chain). |
| T1212 | Exploitation for Credential Access | (#2 \| #3) → #4 | Exploiting an implementation flaw to obtain credentials: server-role flaw (`#2` per R-ROLE — auth service, KDC, IAM service) or client-role flaw (`#3` — browser, agent, IdP client). Flaw exploitation yields credentials/tokens, which are then applied — `#4` per R-CRED. Path: `(#2 \| #3) → #4`. |
| T1499.004 | Endpoint Denial of Service: Application or System Exploitation | #2 \| #6 | App/system exploitation for DoS straddles two clusters: (#2) triggering a server-side flaw that crashes or hangs the service, vs (#6) overwhelming application logic through volume of requests against an expensive operation. Path: `#2 + [DRE: A]` or `#6 + [DRE: A]` per mode. |
| T1669 | Wi-Fi Networks | #2 \| #4 | Initial access via Wi-Fi has two cluster modes: (#2) exploit an implementation flaw in the access point or wireless protocol stack (KRACK-class WPA flaws, vendor firmware vulns); or (#4) authenticate using stolen, cracked, or default Wi-Fi credentials. Cluster corrected from prior `#8 \| #2`: physical-attack (#8) was a poor fit — RF medium proximity is not equivalent to physical tampering with hardware in the TLCTC sense. Path: `#2 \| #4 \|\|[network][@External→@Org]\|\|`. Evil-twin / rogue-AP variants where the attacker impersonates the legitimate SSID to capture handshakes are credential-acquisition for a later #4, classified per their own technique. |
