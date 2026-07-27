---
type: "attack-path"
title: "UKRAINE-POWER-GRID-2015"
description: "Ukraine power grid cyberattack (December 23, 2015)."
resource: "tlctc:attack-path:ukraine-power-grid-2015"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-7"
  - "cluster-4"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.3"
---
# UKRAINE-POWER-GRID-2015

## Attack path

```
||[human][@External→@PowerCompany]|| #9 →[Δt=instant] #7 (FEC) →[Δt=~180d] #4 →[Δt=~2h] #1 →[Δt=~4h] #1 + [DRE: A] →[Δt=instant] #7 (FEC) + [DRE: A]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-spear-phishing | [#9](/clusters/cluster-9.md) | \|\|[human][@External→@PowerCompany]\|\| | instant |  |
| s2-blackenergy-execution | [#7](/clusters/cluster-7.md) (FEC) |  | ~180d |  |
| s3-credential-harvest-use | [#4](/clusters/cluster-4.md) |  | ~2h |  |
| s4-scada-lateral-movement | [#1](/clusters/cluster-1.md) |  | ~4h |  |
| s5-breaker-disconnect | [#1](/clusters/cluster-1.md) |  | instant | A |
| s6-killdisk-wipe | [#7](/clusters/cluster-7.md) (FEC) |  |  | A |

## Step notes

- **s1-spear-phishing:** Targeted spear-phishing emails sent to employees at three Ukrainian power distribution companies. The emails contained Microsoft Word document attachments with embedded malicious macros that dropped the BlackEnergy 3 trojan. The emails were crafted to appear as legitimate communications relevant to the energy sector, exploiting the recipients' trust and professional context. Generic vulnerability: human psychological susceptibility to social engineering — the employees were deceived into opening the attachment and enabling macros. The topology boundary crossing is from the external attacker sphere into the power company's organizational sphere, mediated through the human context (the employee's decision to open the attachment). The 'instant' delta reflects that macro execution occurs immediately upon the victim enabling macros — the social engineering step and malware execution are causally linked but represent different generic vulnerabilities (human deception vs. foreign code execution).
- **s2-blackenergy-execution:** BlackEnergy 3 trojan macro payload executed when the victim opened the Word attachment and clicked 'Enable Content' to run the embedded VBA macro. The macro dropped and executed the BlackEnergy backdoor, which established command-and-control (C2) communication with attacker infrastructure. The malware provided persistent remote access, keylogging, screenshot capture, and the ability to download additional tools. R-EXEC: this is the FEC execution moment — foreign executable content (BlackEnergy 3 trojan) executes on the victim's workstation, recorded as #7 with fec_executed: true. The ~180d (approximately 6 months) delta represents the extensive reconnaissance period during which the attackers mapped the IT and OT networks, identified SCADA systems, studied HMI interfaces, and harvested credentials. This prolonged dwell time (VC-1: months) is characteristic of state-sponsored ICS-targeted operations and represents a significant detection window that was not exploited.
- **s3-credential-harvest-use:** Attackers leveraged their BlackEnergy foothold to harvest VPN credentials for the operational technology (OT) / SCADA network, then used those credentials to authenticate to the industrial control network via the corporate VPN. The credential acquisition occurred through the malware's keylogging and credential-dumping capabilities (part of the #7 step's consequences), but the application of those credentials to authenticate as a legitimate user is a separate attack step. Axiom X (Credential Duality): the acquisition of VPN credentials was enabled by the malware (#7), but the use of those credentials to impersonate a legitimate operator and authenticate to the SCADA VPN is always classified as #4 Identity Theft, regardless of the acquisition method. R-CRED: credential application = #4. The ~2h delta represents the time between gaining authenticated SCADA network access and completing lateral movement to the HMI stations.
- **s4-scada-lateral-movement:** Using the stolen VPN credentials (now authenticated as a legitimate user), the attackers navigated from the IT network into the OT/SCADA network and accessed Human-Machine Interface (HMI) stations used to control power distribution equipment. The attackers used legitimate remote desktop tools (including native Windows RDP and VNC software already installed on operator workstations) to connect to the HMI stations. Classification rationale: this is Abuse of Functions (#1) — all tools and capabilities used in this step functioned exactly as designed. The VPN provided authorized remote access, the remote desktop software provided authorized screen sharing, and the network routing between IT and OT segments was configured to allow this traffic. No exploit was used; no software vulnerability was triggered. The generic vulnerability is the excessive capability of legitimately accessible functions — the VPN and remote desktop tools provided more access than the security architecture intended. The ~4h delta represents the time the attackers spent on the HMI stations preparing and executing the breaker operations across all three power companies simultaneously.
- **s5-breaker-disconnect:** The attackers used the legitimate HMI interface to send SCADA commands that remotely opened circuit breakers at approximately 30 substations across three power distribution companies, disconnecting approximately 230,000 customers from the electrical grid. The operators' own HMI software was used against them — the attackers literally clicked the same buttons that operators would use, issuing valid SCADA commands through the designed control interface. Classification rationale: this is unambiguously Abuse of Functions (#1). The HMI worked exactly as designed. The circuit breakers responded correctly to valid commands. No software vulnerability was exploited. The generic vulnerability is that the SCADA system's legitimate control functions — designed to allow operators to open and close breakers — were exercised by an unauthorized party who had obtained legitimate access. DRE: A (Loss of Availability) — approximately 230,000 customers lost electrical power for 1 to 6 hours. This was the first publicly confirmed cyberattack to cause a power outage, demonstrating that cyber operations can produce kinetic-equivalent effects on critical infrastructure.
- **s6-killdisk-wipe:** Simultaneously with or immediately after the breaker operations, the attackers deployed KillDisk destructive malware to operator workstations and SCADA servers. KillDisk overwrote the Master Boot Record (MBR) and selectively destroyed files on the targeted systems, rendering them unbootable and inoperable. Additionally, the attackers reprogrammed the UPS (Uninterruptible Power Supply) systems to fail, and launched a telephone denial-of-service (TDoS) attack against the power companies' call centers to prevent customers from reporting outages and to delay the utilities' situational awareness. R-EXEC: KillDisk is a distinct foreign executable — a separate FEC execution event from the initial BlackEnergy infection. This is the second #7 step in the path, recording the execution of destructive malware. fec_executed: true. DRE: A (Loss of Availability) — the destruction of operator workstations and SCADA servers prevented remote recovery of the power grid, forcing utility operators to manually travel to substations and physically close circuit breakers by hand. This anti-forensic and anti-recovery action extended the outage duration from what could have been minutes (if operators could simply re-close breakers via HMI) to hours. The combination of grid disconnection, system destruction, UPS sabotage, and call center flooding demonstrates a highly coordinated, multi-vector attack designed to maximize impact and delay recovery.

# Citations

Ukraine power grid cyberattack (December 23, 2015). Russian-attributed attack (Sandworm/Voodoo Bear group, also known as TeleBots) against three Ukrainian power distribution companies: Kyivoblenergo, Prykarpattyaoblenergo, and Chernivtsioblenergo. The attack caused a blackout affecting approximately 230,000 customers for 1-6 hours — the first confirmed cyberattack to take down a power grid. Attack chain: spear-phishing with BlackEnergy 3 trojan macro dropper, ~6 months of reconnaissance and lateral movement, VPN credential theft, SCADA/ICS network access, legitimate HMI commands to open circuit breakers, KillDisk wiper deployment for anti-recovery. Attack path: #9 ||[human][@External→@PowerCompany]|| →[Δt=instant] #7 →[Δt=~6mo] #4 →[Δt=~2h] #1 →[Δt=~4h] #1 + [DRE: A] →[Δt=instant] #7 + [DRE: A]. Axiom IV: attribution to Sandworm/Russia does not affect cluster classification. Sources: CISA ICS-CERT Alert IR-ALERT-H-16-056-01, SANS ICS report 'Analysis of the Cyber Attack on the Ukrainian Power Grid' by Robert M. Lee, Michael J. Assante, and Tim Conway (E-ISAC, March 2016), Symantec BlackEnergy/Sandworm research, Dragos Inc. CRASHOVERRIDE/ELECTRUM analysis.
