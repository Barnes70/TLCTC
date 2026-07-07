---
type: "attack-path"
title: "BLOCKADE-SPIDER-EMBARGO-2025"
description: "BLOCKADE SPIDER's cross-domain Embargo ransomware campaigns (throughout 2025)."
resource: "tlctc:attack-path:blockade-spider-embargo-2025"
tags:
  - "attack-path"
  - "cluster-2"
  - "cluster-4"
  - "cluster-1"
  - "cluster-7"
  - "confidence-medium"
timestamp: "2026-04-16T00:00:00Z"
tlctc_version: "2.3"
---
# BLOCKADE-SPIDER-EMBARGO-2025

## Attack path

```
#2 + [DRE: C] →[Δt=?] #4 →[Δt=?] #1 + [DRE: C] →[Δt=?] #1 →[Δt=?] #1 →[Δt=?] #7 (FEC) →[Δt=?] #1 + [DRE: C] →[Δt=?] #7 (FEC) + [DRE: Ac]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-edge-device-exploit | [#2](/clusters/cluster-2.md) |  | ? | C |
| s2-sso-auth | [#4](/clusters/cluster-4.md) |  | ? |  |
| s3-sharepoint-recon | [#1](/clusters/cluster-1.md) |  | ? | C |
| s4-edr-rule-modification | [#1](/clusters/cluster-1.md) |  | ? |  |
| s5-identity-persistence | [#1](/clusters/cluster-1.md) |  | ? |  |
| s6-orbit-backdoor | [#7](/clusters/cluster-7.md) (FEC) |  | ? |  |
| s7-unmanaged-vm-exfil | [#1](/clusters/cluster-1.md) |  | ? | C |
| s8-embargo-ransomware | [#7](/clusters/cluster-7.md) (FEC) |  |  | Ac |

## Step notes

- **s1-edge-device-exploit:** Initial access via exploitation of an unmanaged and unpatched edge device (firewall or VPN appliance). R-ROLE: the edge device is in a server role relative to the attacker — classified as #2 Exploiting Server. BLOCKADE SPIDER 'routinely gained initial access via unpatched edge devices.' The compromised edge device yields network access and credential material (stored VPN credentials, session tokens, or configuration data). DRE: C — credential material exposed from the edge device enables subsequent identity-domain operations.
- **s2-sso-auth:** Attacker authenticates using a compromised SSO account. In one documented incident, the account belonged to an information security employee, providing elevated access to security tooling and documentation. R-CRED: credential application is always #4 regardless of acquisition method. Axiom X (Credential Duality): the credential was acquired via the edge device compromise (#2, s1 as enabling cluster); its use to authenticate is a separate #4 step. The compromised SSO account provides access to multiple organizational platforms: SharePoint, EDR console, cloud identity services.
- **s3-sharepoint-recon:** Using the compromised SSO session, the adversary browses Microsoft SharePoint to access two categories of documents: (1) network architecture documentation, which informed subsequent lateral movement decisions, and (2) the victim entity's cyber insurance policies, which may have informed the ransom demand amount. This is #1 Abuse of Functions: SharePoint's document search and access capabilities are functioning exactly as designed — the generic vulnerability is that these functions serve an unauthorized actor. DRE: C — sensitive internal documentation (network architecture, cyber insurance coverage) exposed to the adversary.
- **s4-edr-rule-modification:** The adversary uses the compromised SSO account to access the victim organization's EDR user interface. They identify a legitimate existing rule configured to exclude EDR alerts on activity conducted by specific users in a specific directory. BLOCKADE SPIDER then modifies this rule to apply to all users, effectively converting the specified directory into an unmonitored staging area for malicious binaries. This is #1 Abuse of Functions: the EDR's rule management interface is used exactly as designed — the attacker edits an existing exclusion rule through the legitimate admin console. This technique neutralizes endpoint detection for all subsequent file-based operations in the staging directory.
- **s5-identity-persistence:** BLOCKADE SPIDER establishes persistent identity-domain access through multiple complementary techniques, all using legitimate administrative functions: (1) hijacks the AD agent for on-premises identity control; (2) modifies Entra ID conditional access policies to weaken authentication requirements; (3) registers a federated identity provider in the victim's Entra ID tenant, enabling the adversary to generate trusted identities from their own infrastructure; (4) creates mail forwarding and mail deletion rules in Microsoft 365 to prevent legitimate users from receiving security alerts. This is #1 Abuse of Functions: each technique uses the platform's designed administrative capabilities. Collectively, these modifications give the adversary durable, multi-path access to the victim's identity infrastructure while suppressing security notifications that might trigger investigation.
- **s6-orbit-backdoor:** BLOCKADE SPIDER deploys the OrBit Linux backdoor to VMware vCenter for persistent access to virtualization infrastructure. R-EXEC: foreign executable content runs on the vCenter host — recorded as #7 with fec_executed: true. OrBit provides the adversary with persistent, direct access to the hypervisor management plane, independent of the identity-domain access established in previous steps. This dual-path persistence (identity + hypervisor backdoor) ensures continued access even if one path is discovered and remediated.
- **s7-unmanaged-vm-exfil:** Using vCenter access (via OrBit backdoor or identity-domain credentials), the adversary creates unmanaged virtual machines — VMs with no EDR sensor — to exfiltrate data from key systems without security tooling visibility. Cloud-based SaaS applications are also targeted for data exfiltration. This is #1 Abuse of Functions: VM creation, disk mounting, and SaaS data access all use legitimate platform capabilities. The unmanaged VM technique is structurally identical to SCATTERED SPIDER's approach (see scattered-spider-unmanaged-vm-2025.json): operating from hosts without security tooling creates complete EDR blindness for data staging and exfiltration. DRE: C — sensitive organizational data exfiltrated from both on-premises (via unmanaged VMs) and cloud (via SaaS) sources.
- **s8-embargo-ransomware:** BLOCKADE SPIDER deploys the Linux version of Embargo ransomware on VMware ESXi hypervisors, encrypting virtual machine disk files (VMDKs) at the hypervisor layer. R-EXEC: foreign executable content runs on the hypervisor — recorded as #7 with fec_executed: true. Axiom III: ransomware is an outcome class, not a cluster — the payload execution is #7, the impact is DRE: Ac (data present but unusable). By encrypting at the hypervisor layer rather than within individual VMs, the adversary bypasses all endpoint-level security controls. The preceding steps — EDR rule modification (s4), identity persistence (s5), and data exfiltration (s7) — ensure maximum leverage: the victim's data has already been stolen for double extortion, security monitoring has been degraded, and recovery paths through identity infrastructure have been compromised.

# Citations

BLOCKADE SPIDER's cross-domain Embargo ransomware campaigns (throughout 2025). Composite path derived from CrowdStrike's description of the adversary's progressive tradecraft spanning four operational domains: edge devices, identity/cloud, SaaS applications, and virtualization infrastructure. Techniques are 'conceptually similar to SCATTERED SPIDER, including creating unmanaged VMs in victim networks and subtly modifying existing identity-oriented security policies. No known link exists between the two adversaries.' Analyst confidence is medium because this is a composite from multiple campaigns, not a single incident with exact timestamps. Attack path: #2 + [DRE: C] →[Δt=?] #4 →[Δt=?] #1 + [DRE: C] →[Δt=?] #1 →[Δt=?] #1 →[Δt=?] #7 →[Δt=?] #1 + [DRE: C] →[Δt=?] #7 + [DRE: Ac]. Source: CrowdStrike 2026 Global Threat Report, pp. 24-25, Figure 13.
