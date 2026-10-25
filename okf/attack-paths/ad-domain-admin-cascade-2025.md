---
type: "attack-path"
title: "AD-DOMAIN-ADMIN-CASCADE-2025"
description: "Reference path for the Active Directory Domain-Admin → ransomware cascade, modelled on the Lynx intrusion (The DFIR Report, 'Cat's Got Your Files: Lynx Ransomware', 17 December 2025; intrusion of early March 2025; time to ransomware just under 178 hours across nine calendar days)."
resource: "tlctc:attack-path:ad-domain-admin-cascade-2025"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-7"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-04-19T00:00:00Z"
tlctc_version: "2.6"
---
# AD-DOMAIN-ADMIN-CASCADE-2025

## Attack path

```
… →[Δt=?] #4 →[Δt=~minutes] #7 (FEC) →[Δt=~minutes] #4 →[Δt=~minutes] #1 →[Δt=~minutes] #1 →[Δt=~minutes] #7 (FEC) →[Δt=~5d] #4 →[Δt=~minutes] #1 →[Δt=~minutes] #7 (FEC) →[Δt=~minutes] #1 →[Δt=~minutes] #1 + [DRE: C] →[Δt=~3d] #4 →[Δt=~minutes] #1 + [DRE: Av] →[Δt=~minutes] #1 →[Δt=~minutes] #7 (FEC) + [DRE: Ac]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s0-acquisition-prefix | … (unresolved) |  | ? | |
| s1-rdp-beachhead | [#4](/clusters/cluster-4.md) |  | ~minutes |  |
| s2-netscan | [#7](/clusters/cluster-7.md) (FEC) |  | ~minutes |  |
| s3-rdp-to-dc | [#4](/clusters/cluster-4.md) |  | ~minutes |  |
| s4-create-lookalike-accounts | [#1](/clusters/cluster-1.md) |  | ~minutes |  |
| s5-elevate-accounts | [#1](/clusters/cluster-1.md) |  | ~minutes |  |
| s6-anydesk-install | [#7](/clusters/cluster-7.md) (FEC) |  | ~5d |  |
| s7-rdp-beachhead-day6 | [#4](/clusters/cluster-4.md) |  | ~minutes |  |
| s8-netexec-download | [#1](/clusters/cluster-1.md) |  | ~minutes |  |
| s9-netexec-run | [#7](/clusters/cluster-7.md) (FEC) |  | ~minutes |  |
| s10-collect-archive | [#1](/clusters/cluster-1.md) |  | ~minutes |  |
| s11-upload-temp-sh | [#1](/clusters/cluster-1.md) |  | ~3d | C |
| s12-rdp-day9 | [#4](/clusters/cluster-4.md) |  | ~minutes |  |
| s13-veeam-backup-deletion | [#1](/clusters/cluster-1.md) |  | ~minutes | Av |
| s14-stage-payload | [#1](/clusters/cluster-1.md) |  | ~minutes |  |
| s15-encrypt-per-host | [#7](/clusters/cluster-7.md) (FEC) |  |  | Ac |

## Step notes

- **s0-acquisition-prefix:** Acquisition of the two domain credentials used in s1 and s3. The DFIR Report found no brute force, no spraying, no on-host privilege escalation and no credential dumping. It assesses that both credentials were compromised before the intrusion: infostealer logs, reuse from a breach, or an initial-access broker. No acquisition telemetry survived on the target estate, so no cluster can be defended (R-UNRES-8, R-UNRES-9). Each candidate route would be its own chain, for example #9 → #7 + [DRE: C] for a stealer infection.
- **s1-rdp-beachhead:** Day 1. Successful RDP logon to an internet-exposed beachhead host with valid credentials and an elevated token. No failed authentications precede it, which is the forensic signature of pre-acquired credentials. Credential application is #4 (R-CRED, Axiom X).
- **s2-netscan:** SoftPerfect Network Scanner (netscan.exe 7.2.7, with config and license file) dropped onto the beachhead desktop over the RDP session and run against the internal range, with share write checks. A legitimate product brought in by the attacker is a foreign-introduced tool, so its execution is #7 (R-EXEC). Native discovery commands run in the same session (ipconfig, route print, systeminfo) are designed functions and are not recorded separately.
- **s3-rdp-to-dc:** About ten minutes after the first logon, RDP from the beachhead to a domain controller with a DIFFERENT domain-admin account, also compromised beforehand. This is the decisive compromise, where a Tier-0 identity is under attacker control and reach becomes domain-wide. It is one SRE among many, since every cluster step records its own. Credential application is #4.
- **s4-create-lookalike-accounts:** Accounts 'administratr' and a look-alike of an existing user are created with dsa.msc and set to never expire. A third look-alike is created on day 1 or day 2; the report is inconsistent on this. The enrolment function is used outside any grant, so this is #1 (R-SCOPE, R-CRED). Because the directory issued these identities to the attacker, later logons with them claim no one else's identity and are NOT #4 (R-CRED, self-issued identity). The day-2 hypervisor logons with them are #1. Axiom IV: the typosquat naming is a tell, not a classification input.
- **s5-elevate-accounts:** 'administratr' and the first look-alike are added to Domain Admins, and 'administratr' also to Group Policy Creator Owners. The third account goes into a domain-specific privileged group. These are designed group-membership functions used outside any grant.
- **s6-anydesk-install:** AnyDesk installed as a service on the domain controller, then never used. The installer and service are foreign-introduced code executing (R-EXEC). The step succeeded as persistence, so it is recorded even though the channel stayed idle. Day 1 ends with a registry query for hypervisor hostnames.
- **s7-rdp-beachhead-day6:** Day 6. RDP back to the beachhead from the same source IP and workstation name. Re-applying a stolen credential is #4 each time.
- **s8-netexec-download:** NetExec (nxc.exe) downloaded through Microsoft Edge. Ingress transfer uses a designed client function and moves a file without running it, so it is #1 (ATT&CK T1105 mapping). R-EXEC fires at s9.
- **s9-netexec-run:** NetExec run for about two minutes against the /24 over SMB (445) with domain-admin credentials. The report's detail section describes live-host enumeration; its summary calls it a password spray. Either way the attacker-introduced tool executes, so this is #7 (R-EXEC). The SMB authentications it makes with the stolen credential are folded into this step.
- **s10-collect-archive:** File shares on two file servers browsed and archived with 7-Zip's Explorer 'Add to archive' (7zG.exe), with the archives saved to the desktop. These are designed file-access and archive functions (ATT&CK T1560.001 → #1). The report does not say whether 7-Zip was already installed. The disclosure is recorded at s11, where the data leaves the organization's control.
- **s11-upload-temp-sh:** The archives are uploaded one by one to the temporary file-sharing service temp.sh; browser history shows its /upload URI. A browser's upload form is a designed client function and no attacker code runs, so this is #1 + [DRE: C]. The April 2026 edition recorded a #7 'exfil tool' here, which Lynx does not evidence. Contrast Storm-2603 (Talos), where a PowerShell script did the upload: #7 + [DRE: C].
- **s12-rdp-day9:** Day 9. RDP to the beachhead from a new source IP (a day-8 session from the same IP did the reconnaissance omitted here), then RDP to a backup server with the stolen domain-admin credential. #4 at each authentication.
- **s13-veeam-backup-deletion:** In the Veeam Backup & Replication console, backup jobs are deleted and backups are removed from the configuration database. This is a designed administrative function used outside any grant. [DRE: Av]: the backup data is gone, not merely unusable. Contrast: the backup administrator doing the same inside their grant would be Abuse of Rights (no cluster, no SRE, the chain starts at the DRE), with an identical log entry.
- **s14-stage-payload:** The Lynx payload w.exe is copied to the desktop of the compromised domain-admin account, and on one server to the root of E:. A designed file-copy function moves a file without running it, so this is #1. The run is s15.
- **s15-encrypt-per-host:** w.exe is run manually via cmd (e.g. --dir E:\ --mode fast --verbose --noprint) on several backup and file servers, each reached over RDP. Foreign executable content runs, so this is #7 with fec_executed (R-EXEC). [DRE: Ac]: the data is present but unusable. Axiom III: 'ransomware' is the outcome label, not a cluster. This one step stands for the per-host s14 → s15 pair repeated on each server, and a forensic record would enumerate each pair.

# Citations

Reference path for the Active Directory Domain-Admin → ransomware cascade, modelled on the Lynx intrusion (The DFIR Report, 'Cat's Got Your Files: Lynx Ransomware', 17 December 2025; intrusion of early March 2025; time to ransomware just under 178 hours across nine calendar days). Evidenced steps only. Shape: a variable prefix, the decisive compromise (a Tier-0 identity under attacker control, s3), and a near-invariant tail that is structurally #1 Abuse of Functions, with #7 wherever foreign executable content runs. Every cluster step records its own SRE (core §3.4). 'Decisive' marks where reach becomes domain-wide, not where loss of control begins. Attack path: … → #4 →[Δt=~minutes] #7 →[Δt=~minutes] #4 →[Δt=~minutes] #1 →[Δt=~minutes] #1 →[Δt=~minutes] #7 →[Δt=~5d] #4 →[Δt=~minutes] #1 →[Δt=~minutes] #7 →[Δt=~minutes] #1 →[Δt=~minutes] #1 + [DRE: C] →[Δt=~3d] #4 →[Δt=~minutes] #1 + [DRE: Av] →[Δt=~minutes] #1 →[Δt=~minutes] #7 + [DRE: Ac]. Compressions: the day-2 logons to hypervisors with the look-alike accounts (#1, since these accounts were self-enrolled; R-CRED) and the day-8 reconnaissance of domain controllers and Hyper-V hosts are omitted. Only session-opening logons are recorded, although every RDP hop with the stolen domain-admin credential is its own #4. The report does not mention credential dumping, shadow-copy deletion or log clearing, so none is recorded. Velocity is per transition: VC-3 (minutes) inside each session, VC-1 (days) between sessions. The ~10-minute beachhead→DC edge needs automated containment (DCS_c = TTC_P90/Δt < 1). Other prefix variants, as classified in the companion post: (B) Akira, Microsoft case study of 9 April 2025, no threat actor named: #4 [conf=low] VPN entry → … → #4 RDP to DC1 with a domain-admin credential → #1 recon → #1 GPO AV tampering → #1 two accounts created and added to Domain Admins → #1 logon as one of them. The encryption was blocked by attack disruption, so no #7/Ac is recorded (successes only). (C) Storm-2603, Cisco Talos 9 October 2025, incident of August 2025, moderate-confidence attribution, initial access not observed: #2 [conf=low] ToolShell → … → #1 admin accounts synced to Entra ID → #1 vSphere console → #1 GPO Defender off → #7 + [DRE: C] PowerShell exfil script → #7 + [DRE: Ac] fileless PowerShell encryptor / Warlock / Babuk on ESXi; Velociraptor 0.73.4.0 installs are #7, untimed. (D) Kerberoasting: #4 → #1 + [DRE: C] TGS requests → #4 cracked service account → #1 (ATT&CK T1558.003). (E) ZeroLogon CVE-2020-1472: #2 + [DRE: I] machine-account password reset → #4 logon as the DC account → #1 + [DRE: C] DCSync. Sources: DFIR Report (Lynx); Microsoft Security Blog 'How cyberattackers exploit domain controllers using ransomware' (9 April 2025; >78% of human-operated cyberattacks breach a DC, DC is the primary spreader in >35%); Cisco Talos 'Velociraptor leveraged in ransomware attacks' (9 October 2025); CISA AA24-109A (Akira, updated 13 November 2025); Secura Zerologon whitepaper (2020). Companion analysis: https://www.tlctc.net/ad-ransomware-tlctc-cascade.html (The #1-Cascade). Revision 2026-10-25: rebuilt as an evidence-only Lynx path. The earlier composite carried an actor label ('Storm-0300') that Microsoft's case study does not support. It also had an exfiltration #7 that Lynx does not evidence (the upload went through a browser), DCSync, shadow-copy and log-clearing steps that Lynx does not document, a non-registry boundary context, per-incident velocity classes, and ZeroLogon's [DRE: C] on the exploit step. Classified against the v2.6 dictionary; v2.7 is classification-preserving.
