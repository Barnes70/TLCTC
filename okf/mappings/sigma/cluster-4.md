---
type: "mapping-set"
title: "Sigma rules → #4 Identity Theft"
description: "104 Sigma rules entries mapped to TLCTC #4 Identity Theft."
resource: "tlctc:mapping:sigma:cluster-4"
tags:
  - "mapping"
  - "sigma"
  - "cluster-4"
---
# Sigma rules → #4 Identity Theft

> Source: SigmaHQ rules → TLCTC mapping (`mappings/sigma/`). Derived via ATT&CK technique mapping.

Mapped entries: **104**. Cluster: [#4 Identity Theft](/clusters/cluster-4.md).

| Rule | Techniques | Cluster set | Status |
|---|---|---|---|
| Bitbucket User Login Failure | T1078, T1110 | #4 | ok |
| Github New Secret Created | T1078 | #4 | ok |
| Github SSH Certificate Configuration Changed | T1078 | #4 | ok |
| OpenCanary - Telnet Login Attempt | T1078, T1133 | #4 | ok |
| AWS ConsoleLogin Failed Authentication | T1110 | #4 | ok |
| AWS Successful Console Login Without MFA | T1078 | #4 | ok |
| Malicious Usage Of IMDS Credentials Outside Of AWS Infrastructure | T1078 | #4 | ok |
| AWS Key Pair Import Activity | T1078 | #4 | ok |
| AWS Root Credentials | T1078 | #4 | ok |
| Azure Subscription Permission Elevation Via ActivityLogs | T1078 | #4 | ok |
| Account Created And Deleted Within A Close Time Frame | T1078 | #4 | ok |
| Bitlocker Key Retrieval | T1078 | #4 | ok |
| Guest Users Invited To Tenant By Non Approved Inviters | T1078 | #4 | ok |
| Users Added to Global or Device Admin Roles | T1078 | #4 | ok |
| Azure Domain Federation Settings Modified | T1078 | #4 | ok |
| Guest User Invited By Non Approved Inviters | T1078 | #4 | ok |
| User State Changed From Guest To Member | T1078 | #4 | ok |
| PIM Approvals And Deny Elevation | T1078 | #4 | ok |
| PIM Alert Setting Changes To Disabled | T1078 | #4 | ok |
| Changes To PIM Settings | T1078 | #4 | ok |
| User Added To Privilege Role | T1078 | #4 | ok |
| Privileged Account Creation | T1078 | #4 | ok |
| Azure Subscription Permission Elevation Via AuditLogs | T1078 | #4 | ok |
| Temporary Access Pass Added To An Account | T1078 | #4 | ok |
| Password Reset By User Account | T1078 | #4 | ok |
| Activity From Anonymous IP Address | T1078 | #4 | ok |
| Atypical Travel | T1078 | #4 | ok |
| Impossible Travel | T1078 | #4 | ok |
| New Country | T1078 | #4 | ok |
| Password Spray Activity | T1110 | #4 | ok |
| Suspicious Browser Activity | T1078 | #4 | ok |
| Azure AD Threat Intelligence | T1078 | #4 | ok |
| Unfamiliar Sign-In Properties | T1078 | #4 | ok |
| Stale Accounts In A Privileged Role | T1078 | #4 | ok |
| Invalid PIM License | T1078 | #4 | ok |
| Roles Assigned Outside PIM | T1078 | #4 | ok |
| Roles Activated Too Frequently | T1078 | #4 | ok |
| Roles Activation Doesn't Require MFA | T1078 | #4 | ok |
| Roles Are Not Being Used | T1078 | #4 | ok |
| Too Many Global Admins | T1078 | #4 | ok |
| Account Lockout | T1110 | #4 | ok |
| Increased Failed Authentications Of Any Type | T1078 | #4 | ok |
| Measurable Increase Of Successful Authentications | T1078 | #4 | ok |
| Authentications To Important Apps Using Single Factor Authentication | T1078 | #4 | ok |
| Successful Authentications From Countries You Do Not Operate Out Of | T1078, T1110 | #4 | ok |
| Device Registration or Join Without MFA | T1078 | #4 | ok |
| Failed Authentications From Countries You Do Not Operate Out Of | T1078, T1110 | #4 | ok |
| Suspicious SignIns From A Non Registered Device | T1078 | #4 | ok |
| Sign-ins from Non-Compliant Devices | T1078 | #4 | ok |
| Sign-ins by Unknown Devices | T1078 | #4 | ok |
| Potential MFA Bypass Using Legacy Client Authentication | T1078, T1110 | #4 | ok |
| Application Using Device Code Authentication Flow | T1078 | #4 | ok |
| Applications That Are Using ROPC Authentication Flow | T1078 | #4 | ok |
| Account Disabled or Blocked for Sign in Attempts | T1078 | #4 | ok |
| Sign-in Failure Due to Conditional Access Requirements Not Met | T1078, T1110 | #4 | ok |
| Use of Legacy Authentication Protocols | T1078, T1110 | #4 | ok |
| Login to Disabled Account | T1078 | #4 | ok |
| Azure Unusual Authentication Interruption | T1078 | #4 | ok |
| User Access Blocked by Azure Conditional Access | T1078, T1110 | #4 | ok |
| Users Authenticating To Other Azure AD Tenants | T1078 | #4 | ok |
| Google Workspace Government Attack Warning | T1078 | #4 | ok |
| Suspicious Login Activity Classified By Google | T1078 | #4 | ok |
| Azure Login Bypassing Conditional Access Policies | T1078 | #4 | ok |
| Microsoft 365 - Impossible Travel Activity | T1078 | #4 | ok |
| Logon from a Risky IP Address | T1078 | #4 | ok |
| Okta New Admin Console Behaviours | T1078 | #4 | ok |
| Remote Access Tool - Team Viewer Session Started On Linux Host | T1133 | #4 | ok |
| User Added To Admin Group Via Dscl | T1078 | #4 | ok |
| User Added To Admin Group Via DseditGroup | T1078 | #4 | ok |
| Root Account Enable Via Dsenableroot | T1078 | #4 | ok |
| Remote Access Tool - Team Viewer Session Started On MacOS Host | T1133 | #4 | ok |
| User Added To Admin Group Via Sysadminctl | T1078 | #4 | ok |
| Guest Account Enabled Via Sysadminctl | T1078 | #4 | ok |
| Cisco BGP Authentication Failures | T1078, T1110, T1557 | #4, #5 | ambiguous |
| Cisco LDP Authentication Failures | T1078, T1110, T1557 | #4, #5 | ambiguous |
| FortiGate - New VPN SSL Web Portal Added | T1133 | #4 | ok |
| FortiGate - VPN SSL Settings Modified | T1133 | #4 | ok |
| Huawei BGP Authentication Failures | T1078, T1110, T1557 | #4, #5 | ambiguous |
| Juniper BGP Missing MD5 | T1078, T1110, T1557 | #4, #5 | ambiguous |
| MSSQL Server Failed Logon | T1110 | #4 | ok |
| MSSQL Server Failed Logon From External Network | T1110 | #4 | ok |
| NTLM Logon | T1550 | #4 | ok |
| NTLM Brute Force | T1110 | #4 | ok |
| Admin User Remote Logon | T1078 | #4 | ok |
| Successful Overpass the Hash Attempt | T1550 | #4 | ok |
| Pass the Hash Activity 2 | T1550 | #4 | ok |
| External Remote RDP Logon from Public IP | T1078, T1110, T1133 | #4 | ok |
| External Remote SMB Logon from Public IP | T1078, T1110, T1133 | #4 | ok |
| Outgoing Logon with New Credentials | T1550 | #4 | ok |
| Win Susp Computer Name Containing Samtheadmin | T1078 | #4 | ok |
| Account Tampering - Suspicious Failed Logon Reasons | T1078 | #4 | ok |
| Suspicious Remote Logon with Explicit Credentials | T1078 | #4 | ok |
| Suspicious Rejected SMB Guest Logon From IP | T1110 | #4 | ok |
| NTLMv1 Logon Between Client and Server | T1550 | #4 | ok |
| Unusual File Modification by dns.exe | T1133 | #4 | ok |
| Unusual File Deletion by Dns.exe | T1133 | #4 | ok |
| Suspicious Computer Machine Password by PowerShell | T1078 | #4 | ok |
| Suspicious Connection to Remote Account | T1110 | #4 | ok |
| Unusual Child Process of dns.exe | T1133 | #4 | ok |
| HackTool - Hashcat Password Cracker Execution | T1110 | #4 | ok |
| HackTool - Hydra Password Bruteforce Execution | T1110 | #4 | ok |
| Remote Access Tool - ScreenConnect Installation Execution | T1133 | #4 | ok |
| Remote Access Tool - Team Viewer Session Started On Windows Host | T1133 | #4 | ok |
| Running Chrome VPN Extensions via the Registry 2 VPN Extension | T1133 | #4 | ok |
