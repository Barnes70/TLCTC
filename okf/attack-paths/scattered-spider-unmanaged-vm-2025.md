---
type: "attack-path"
title: "SCATTERED-SPIDER-UNMANAGED-VM-2025"
description: "SCATTERED SPIDER's abuse of unmanaged virtual machines to dump Active Directory credentials, as documented in the CrowdStrike 2026 Global Threat Report (pp."
resource: "tlctc:attack-path:scattered-spider-unmanaged-vm-2025"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-4"
  - "cluster-7"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-04-16T00:00:00Z"
tlctc_version: "2.3"
---
# SCATTERED-SPIDER-UNMANAGED-VM-2025

## Attack path

```
||[human][@Attacker→@Org-HelpDesk]|| #9 →[Δt=~15m] #4 →[Δt=~45m] #7 (FEC) →[Δt=~15m] ||[human][@Attacker→@Org-HelpDesk]|| #9 →[Δt=~15m] #4 →[Δt=~5m] #1 + [DRE: C] →[Δt=~5m] #4 →[Δt=~30m] #1 →[Δt=~30m] #7 (FEC) + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-vishing-helpdesk-first | [#9](/clusters/cluster-9.md) | \|\|[human][@Attacker→@Org-HelpDesk]\|\| | ~15m |  |
| s2-first-entra-auth | [#4](/clusters/cluster-4.md) |  | ~45m |  |
| s3-ad-explorer-fec | [#7](/clusters/cluster-7.md) (FEC) |  | ~15m |  |
| s4-vishing-helpdesk-second | [#9](/clusters/cluster-9.md) | \|\|[human][@Attacker→@Org-HelpDesk]\|\| | ~15m |  |
| s5-second-account-auth | [#4](/clusters/cluster-4.md) |  | ~5m |  |
| s6-pam-credential-retrieval | [#1](/clusters/cluster-1.md) |  | ~5m | C |
| s7-vcenter-auth | [#4](/clusters/cluster-4.md) |  | ~30m |  |
| s8-unmanaged-vm-setup | [#1](/clusters/cluster-1.md) |  | ~30m |  |
| s9-ntds-dump | [#7](/clusters/cluster-7.md) (FEC) |  |  | C |

## Step notes

- **s1-vishing-helpdesk-first:** SCATTERED SPIDER calls the victim organization's help desk, persuading personnel to initiate a self-service password reset for a targeted Entra ID / SSO account. This is #9 Social Engineering: a human is manipulated into performing an action that serves the attacker. Boundary crossing: the attack traverses from the external attacker sphere into the organizational human trust boundary. SCATTERED SPIDER 'almost exclusively relied on social engineering techniques to persuade help desk personnel to perform self-service password resets' for initial access in 2025.
- **s2-first-entra-auth:** Attacker authenticates to the compromised Entra ID account using the reset credentials. R-CRED: credential application (authentication) is always #4 regardless of acquisition method. The credential was obtained via social engineering in s1 (#9 as enabling cluster); its use to authenticate is a separate #4 step per Axiom X (Credential Duality). From this session the attacker searches Microsoft SharePoint for network architecture documentation and pivots to a Citrix VDI system — both are legitimate platform features used as designed (reconnaissance, not a separate classification event).
- **s3-ad-explorer-fec:** On the Citrix VDI system, the attacker downloads and executes AD Explorer (a Sysinternals tool) to enumerate Active Directory users and computers. R-EXEC: foreign executable content is downloaded and run on the managed endpoint — the only managed host the attacker touches during the entire three-hour intrusion. This is #7 with fec_executed: true. AD Explorer is a legitimate tool, but it is foreign to the target system and brought in by the attacker for offensive reconnaissance.
- **s4-vishing-helpdesk-second:** SCATTERED SPIDER makes a second vishing call to the help desk, this time targeting a more privileged account that has access to the privileged access management (PAM) application. Same technique as s1: social engineering to trigger a self-service password reset. The two vishing calls are separated by approximately one hour and target different accounts with different privilege levels, making them structurally distinct #9 steps.
- **s5-second-account-auth:** Attacker authenticates to the second compromised account (obtained via s4 vishing). R-CRED: credential application is always #4. This privileged account provides access to the organization's PAM application via web browser.
- **s6-pam-credential-retrieval:** Using the authenticated PAM session, the attacker retrieves the target user's VMware vCenter password. This is #1 Abuse of Functions: the PAM application is functioning exactly as designed — providing stored credentials to authenticated users. The attacker abuses this legitimate capability because they hold a stolen identity. DRE: C — the vCenter administrative credential is exposed to an unauthorized party. The PAM becomes a single point of credential exposure: one compromised identity yields the keys to virtualization infrastructure.
- **s7-vcenter-auth:** Attacker authenticates to VMware vCenter using the credentials retrieved from the PAM in s6. R-CRED: credential application is always #4 regardless of acquisition method (here: PAM abuse in s6, #1 as enabling cluster). Axiom X (Credential Duality): the credential was acquired via #1; its use to authenticate to vCenter is a separate #4 step.
- **s8-unmanaged-vm-setup:** Core defense evasion technique (Figure 10). The attacker uses vCenter's legitimate VM management functions to: (1) download a Windows Server ISO and create a new VM, or identify an existing decommissioned VM — this VM has no EDR sensor (unmanaged); (2) identify and shut down the VM hosting the domain controller; (3) detach the DC's VMDK from the host VM; (4) mount the DC VMDK as a secondary drive to the unmanaged VM. All operations use vCenter's designed functionality — this is #1 Abuse of Functions. The unmanaged VM is the critical pivot: by operating from a host with no security tooling, the attacker achieves complete EDR blindness for the credential extraction that follows.
- **s9-ntds-dump:** On the unmanaged VM, the attacker executes GoSecretsDump to extract the NTDS.dit Active Directory database and the SYSTEM registry hive from the mounted DC VMDK. R-EXEC: foreign executable content (GoSecretsDump) runs on the unmanaged VM — recorded as #7 with fec_executed: true. DRE: C — the NTDS.dit contains all domain password hashes, Kerberos keys, and account metadata. This is the culmination of the defense evasion chain: the credential dump executes entirely outside EDR visibility. CrowdStrike notes that vCenter log ingestion via Falcon Next-Gen SIEM can detect this activity, and CrowdStrike Services maintains a public tool to detect adversary-controlled VMs in VMware environments.

# Citations

SCATTERED SPIDER's abuse of unmanaged virtual machines to dump Active Directory credentials, as documented in the CrowdStrike 2026 Global Threat Report (pp. 22-23, Figures 10-11). In mid-2025, the adversary completed this full chain in under three hours, interacting with only one managed endpoint. Initial access relied exclusively on vishing help desk personnel for self-service password resets. The core defense evasion technique: mount a domain controller's VMDK to a new or decommissioned VM (unmanaged — no EDR sensor) and copy the NTDS.dit database from that unmanaged host. SCATTERED SPIDER deployed ransomware only on VMware ESXi systems (not modeled here — the case highlight covers the credential-dump chain). Attack path: #9 ||[human][@External→@Org]|| →[Δt=15m] #4 →[Δt=45m] #7 →[Δt=15m] #9 ||[human][@External→@Org]|| →[Δt=15m] #4 →[Δt=5m] #1 →[Δt=5m] #4 →[Δt=30m] #1 →[Δt=30m] #7 + [DRE: C]. Source: CrowdStrike 2026 Global Threat Report, Case Highlight: SCATTERED SPIDER's Abuse of Unmanaged Systems.
