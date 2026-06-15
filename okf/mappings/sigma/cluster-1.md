---
type: "mapping-set"
title: "Sigma rules → #1 Abuse of Functions"
description: "2294 Sigma rules entries mapped to TLCTC #1 Abuse of Functions."
resource: "tlctc:mapping:sigma:cluster-1"
tags:
  - "mapping"
  - "sigma"
  - "cluster-1"
---
# Sigma rules → #1 Abuse of Functions

> Source: SigmaHQ rules → TLCTC mapping (`mappings/sigma/`). Derived via ATT&CK technique mapping.

Mapped entries: **2294**. Cluster: [#1 Abuse of Functions](/clusters/cluster-1.md).

| Rule | Techniques | Cluster set | Status |
|---|---|---|---|
| Bitbucket Full Data Export Triggered | T1213 | #1 | ok |
| Bitbucket Global Permission Changed | T1098 | #1 | ok |
| Bitbucket Global SSH Settings Changed | T1021, T1685 | #1, #4 | ambiguous |
| Bitbucket Unauthorized Full Data Export Triggered | T1213, T1586 | #1 | ambiguous |
| Bitbucket User Details Export Attempt Detected | T1082, T1213, T1591 | #1 | ambiguous |
| Bitbucket User Login Failure Via SSH | T1021, T1110 | #1, #4 | ambiguous |
| Bitbucket User Permissions Export Attempt | T1082, T1213, T1591 | #1 | ambiguous |
| Github Delete Action Invoked | T1213 | #1 | ok |
| Github High Risk Configuration Disabled | T1556 | #1, #7 | ambiguous |
| Github Fork Private Repositories Setting Enabled/Cleared | T1020, T1537 | #1, #7 | ambiguous |
| New Github Organization Member Added | T1136 | #1 | ok |
| Github Outside Collaborator Detected | T1098, T1213 | #1 | ok |
| GitHub Repository Pages Site Changed to Public | T1567 | #1, #7 | ambiguous |
| Github Repository/Organization Transferred | T1020, T1537 | #1, #7 | ambiguous |
| Github Self Hosted Runner Changes Detected | T1078, T1213, T1526 | #1, #4 | ambiguous |
| Kubernetes Admission Controller Modification | T1078, T1552 | #1, #4 | ambiguous |
| Kubernetes Events Deleted | T1070 | #1 | ok |
| Potential Remote Command Execution In Pod Container | T1609 | #1, #7 | ambiguous |
| Container With A hostPath Mount Created | T1611 | #1, #2 | ambiguous |
| Creation Of Pod In System Namespace | T1036 | #1, #7 | ambiguous |
| Kubernetes Potential Enumeration Activity | T1609, T1613 | #1, #7 | ambiguous |
| Privileged Container Deployed | T1611 | #1, #2 | ambiguous |
| RBAC Permission Enumeration Attempt | T1069, T1087 | #1 | ok |
| Kubernetes Secrets Enumeration | T1552 | #1, #4 | ambiguous |
| New Kubernetes Service Account Created | T1136 | #1 | ok |
| Potential Sidecar Injection Into Running Deployment | T1609 | #1, #7 | ambiguous |
| OpenCanary - FTP Login Attempt | T1021, T1190 | #1, #2, #4 | ambiguous |
| OpenCanary - GIT Clone Request | T1213 | #1 | ok |
| OpenCanary - HTTPPROXY Login Attempt | T1090 | #1, #7 | ambiguous |
| OpenCanary - MSSQL Login Attempt Via SQLAuth | T1003, T1213 | #1, #7 | ambiguous |
| OpenCanary - MSSQL Login Attempt Via Windows Authentication | T1003, T1213 | #1, #7 | ambiguous |
| OpenCanary - MySQL Login Attempt | T1003, T1213 | #1, #7 | ambiguous |
| OpenCanary - NMAP FIN Scan | T1046 | #1 | ok |
| OpenCanary - NMAP NULL Scan | T1046 | #1 | ok |
| OpenCanary - NMAP OS Scan | T1046 | #1 | ok |
| OpenCanary - NMAP XMAS Scan | T1046 | #1 | ok |
| OpenCanary - Host Port Scan (SYN Scan) | T1046 | #1 | ok |
| OpenCanary - RDP New Connection Attempt | T1021, T1133 | #1, #4 | ambiguous |
| OpenCanary - REDIS Action Command Attempt | T1003, T1213 | #1, #7 | ambiguous |
| OpenCanary - SIP Request | T1123 | #1 | ok |
| OpenCanary - SMB File Open Request | T1005, T1021 | #1, #4 | ambiguous |
| OpenCanary - SNMP OID Request | T1016, T1021 | #1, #4 | ambiguous |
| OpenCanary - SSH Login Attempt | T1021, T1078, T1133 | #1, #4 | ambiguous |
| OpenCanary - SSH New Connection Attempt | T1021, T1078, T1133 | #1, #4 | ambiguous |
| OpenCanary - TFTP Request | T1041 | #1, #7 | ambiguous |
| OpenCanary - VNC Connection Attempt | T1021 | #1, #4 | ambiguous |
| Remote Schedule Task Lateral Movement via ATSvc | T1053 | #1, #7 | ambiguous |
| Possible DCSync Attack | T1033 | #1 | ok |
| Remote Schedule Task Lateral Movement via ITaskSchedulerService | T1053 | #1, #7 | ambiguous |
| Remote DCOM/WMI Lateral Movement | T1021, T1047 | #1, #4, #7 | ambiguous |
| Remote Registry Lateral Movement | T1112 | #1 | ok |
| Remote Server Service Abuse for Lateral Movement | T1569 | #1, #7 | ambiguous |
| Remote Schedule Task Lateral Movement via SASec | T1053 | #1, #7 | ambiguous |
| SharpHound Recon Account Discovery | T1087 | #1 | ok |
| SharpHound Recon Sessions | T1033 | #1 | ok |
| Antivirus Exploitation Framework Detection | T1203, T1219 | #1, #3, #7 | ambiguous |
| Antivirus Password Dumper Detection | T1003, T1558 | #1, #4, #7 | ambiguous |
| Antivirus Web Shell Detection | T1505 | #1, #7 | ambiguous |
| Suspicious SQL Query | T1190, T1505 | #1, #2, #7 | ambiguous |
| PUA - AWS TruffleHog Execution | T1003, T1555 | #1, #4, #7 | ambiguous |
| AWS Console GetSigninToken Potential Abuse | T1021, T1550 | #1, #4 | ambiguous |
| SES Identity Has Been Deleted | T1070 | #1 | ok |
| AWS SAML Provider Deletion Activity | T1078, T1531 | #1, #4, #7 | ambiguous |
| AWS S3 Bucket Versioning Disable | T1490 | #1 | ok |
| AWS EC2 Disable EBS Encryption | T1486, T1565 | #1, #7 | ambiguous |
| AWS EC2 Startup Shell Script Change | T1059 | #1, #7 | ambiguous |
| AWS EC2 VM Export Failure | T1005, T1537 | #1, #7 | ambiguous |
| AWS ECS Task Definition That Queries The Credential Endpoint | T1525 | #1, #7 | ambiguous |
| AWS ElastiCache Security Group Created | T1136 | #1 | ok |
| AWS ElastiCache Security Group Modified or Deleted | T1531 | #1, #7 | ambiguous |
| Potential Bucket Enumeration on AWS | T1580, T1619 | #1 | ok |
| AWS IAM Backdoor Users Keys | T1098 | #1 | ok |
| AWS IAM S3Browser LoginProfile Creation | T1059, T1078 | #1, #4, #7 | ambiguous |
| AWS IAM S3Browser Templated S3 Bucket Policy Creation | T1059, T1078 | #1, #4, #7 | ambiguous |
| AWS IAM S3Browser User or AccessKey Creation | T1059, T1078 | #1, #4, #7 | ambiguous |
| AWS RDS Master Password Change | T1020 | #1 | ok |
| Modification or Deletion of an AWS RDS Cluster | T1020 | #1 | ok |
| Restore Public AWS RDS Instance | T1020 | #1 | ok |
| AWS Route 53 Domain Transfer Lock Disabled | T1098 | #1 | ok |
| AWS Route 53 Domain Transferred to Another Account | T1098 | #1 | ok |
| AWS S3 Data Management Tampering | T1537 | #1, #7 | ambiguous |
| AWS Snapshot Backup Exfiltration | T1537 | #1, #7 | ambiguous |
| AWS Identity Center Identity Provider Change | T1556 | #1, #7 | ambiguous |
| AWS STS AssumeRole Misuse | T1548, T1550 | #1, #4, #7 | ambiguous |
| AWS STS GetCallerIdentity Enumeration Via TruffleHog | T1087 | #1 | ok |
| AWS STS GetSessionToken Misuse | T1548, T1550 | #1, #4, #7 | ambiguous |
| AWS Suspicious SAML Activity | T1078, T1548, T1550 | #1, #4, #7 | ambiguous |
| AWS User Login Profile Was Modified | T1098 | #1 | ok |
| Azure Active Directory Hybrid Health AD FS New Server | T1578 | #1 | ok |
| Azure Active Directory Hybrid Health AD FS Service Delete | T1578 | #1 | ok |
| User Added to an Administrator's Azure AD Role | T1078, T1098 | #1, #4 | ambiguous |
| Azure Application Deleted | T1489 | #1 | ok |
| Azure Container Registry Created or Deleted | T1485, T1489, T1496 | #1, #7 | ambiguous |
| Number Of Resource Creation Or Deployment Activities | T1098 | #1 | ok |
| Azure Device or Configuration Modified or Deleted | T1485, T1565 | #1, #7 | ambiguous |
| Azure DNS Zone Modified or Deleted | T1565 | #1 | ok |
| Granting Of Permissions To An Account | T1098 | #1 | ok |
| Azure Keyvault Key Modified or Deleted | T1552 | #1, #4 | ambiguous |
| Azure Key Vault Modified or Deleted | T1552 | #1, #4 | ambiguous |
| Azure Keyvault Secrets Modified or Deleted | T1552 | #1, #4 | ambiguous |
| Azure Kubernetes Admission Controller | T1078, T1552 | #1, #4 | ambiguous |
| Azure Kubernetes Cluster Created or Deleted | T1485, T1489, T1496 | #1, #7 | ambiguous |
| Azure Kubernetes CronJob | T1053 | #1, #7 | ambiguous |
| Azure Kubernetes Network Policy Change | T1485, T1489, T1496 | #1, #7 | ambiguous |
| Azure Kubernetes Sensitive Role Access | T1485, T1489, T1496 | #1, #7 | ambiguous |
| Azure Kubernetes RoleBinding/ClusterRoleBinding Modified and Deleted | T1485, T1489, T1496 | #1, #7 | ambiguous |
| Azure Kubernetes Secret or Config Object Access | T1485, T1489, T1496 | #1, #7 | ambiguous |
| Azure Kubernetes Service Account Modified or Deleted | T1485, T1489, T1496, T1531 | #1, #7 | ambiguous |
| Disabled MFA to Bypass Authentication Mechanisms | T1556 | #1, #7 | ambiguous |
| Azure New CloudShell Created | T1059 | #1, #7 | ambiguous |
| Rare Subscription-level Operations In Azure | T1003 | #1, #7 | ambiguous |
| CA Policy Removed by Non Approved Actor | T1548, T1556 | #1, #7 | ambiguous |
| CA Policy Updated by Non Approved Actor | T1548, T1556 | #1, #7 | ambiguous |
| New CA Policy by Non-approved Actor | T1548 | #1, #7 | ambiguous |
| Certificate-Based Authentication Enabled | T1556 | #1, #7 | ambiguous |
| Changes to Device Registration Policy | T1484 | #1 | ok |
| New Root Certificate Authority Added | T1556 | #1, #7 | ambiguous |
| Application AppID Uri Configuration Changes | T1078, T1552 | #1, #4 | ambiguous |
| Added Credentials to Existing Application | T1098 | #1 | ok |
| Delegated Permissions Granted For All Users | T1528 | #1, #4, #9 | ambiguous |
| End User Consent | T1528 | #1, #4, #9 | ambiguous |
| End User Consent Blocked | T1528 | #1, #4, #9 | ambiguous |
| Added Owner To Application | T1552 | #1, #4 | ambiguous |
| App Granted Microsoft Permissions | T1528 | #1, #4, #9 | ambiguous |
| App Granted Privileged Delegated Or App Permissions | T1098 | #1 | ok |
| App Assigned To Azure RBAC/Microsoft Entra Role | T1098 | #1 | ok |
| Application URI Configuration Changes | T1078, T1528 | #1, #4, #9 | ambiguous |
| Windows LAPS Credential Dump From Entra ID | T1098 | #1 | ok |
| Change to Authentication Method | T1098, T1556 | #1, #7 | ambiguous |
| User Added To Group With CA Policy Modification Access | T1548, T1556 | #1, #7 | ambiguous |
| User Removed From Group With CA Policy Modification Access | T1548, T1556 | #1, #7 | ambiguous |
| Bulk Deletion Changes To Privileged Account Permissions | T1098 | #1 | ok |
| Anomalous Token | T1528 | #1, #4, #9 | ambiguous |
| Anomalous User Activity | T1098 | #1 | ok |
| Anonymous IP Address | T1528 | #1, #4, #9 | ambiguous |
| Suspicious Inbox Forwarding Identity Protection | T1114 | #1, #4 | ambiguous |
| Malicious IP Address Sign-In Failure Rate | T1090 | #1, #7 | ambiguous |
| Malicious IP Address Sign-In Suspicious | T1090 | #1, #7 | ambiguous |
| Sign-In From Malware Infected IP | T1090 | #1, #7 | ambiguous |
| Primary Refresh Token Access Attempt | T1528 | #1, #4, #9 | ambiguous |
| SAML Token Issuer Anomaly | T1606 | #1, #4 | ambiguous |
| Discovery Using AzureHound | T1087, T1526 | #1 | ok |
| Azure AD Only Single Factor Authentication Required | T1078, T1556 | #1, #4, #7 | ambiguous |
| Multifactor Authentication Denied | T1078, T1110, T1621 | #1, #4, #9 | ambiguous |
| Multifactor Authentication Interrupted | T1078, T1110, T1621 | #1, #4, #9 | ambiguous |
| GCP Access Policy Deleted | T1098 | #1 | ok |
| GCP Break-glass Container Workload Deployed | T1548 | #1, #7 | ambiguous |
| Google Cloud Re-identifies Sensitive Information | T1565 | #1 | ok |
| Google Full Network Traffic Packet Capture | T1074 | #1 | ok |
| Google Cloud Kubernetes Admission Controller | T1078, T1552 | #1, #4 | ambiguous |
| Google Cloud Service Account Disabled or Deleted | T1531 | #1, #7 | ambiguous |
| Google Workspace Application Access Level Modified | T1098 | #1 | ok |
| Google Workspace Granted Domain API Access | T1098 | #1 | ok |
| Google Workspace User Granted Admin Privileges | T1098 | #1 | ok |
| Google Workspace Out Of Domain Email Forwarding | T1114 | #1, #4 | ambiguous |
| Disabling Multi Factor Authentication | T1556 | #1, #7 | ambiguous |
| New Federated Domain Added | T1484 | #1 | ok |
| New Federated Domain Added - Exchange | T1136 | #1 | ok |
| Activity from Suspicious IP Addresses | T1573 | #1, #7 | ambiguous |
| Activity from Anonymous IP Addresses | T1573 | #1, #7 | ambiguous |
| Activity from Infrequent Country | T1573 | #1, #7 | ambiguous |
| Data Exfiltration to Unsanctioned Apps | T1537 | #1, #7 | ambiguous |
| PST Export Alert Using eDiscovery Alert | T1114 | #1, #4 | ambiguous |
| PST Export Alert Using New-ComplianceSearchAction | T1114 | #1, #4 | ambiguous |
| Suspicious Inbox Forwarding | T1020 | #1 | ok |
| Okta Admin Role Assigned to an User or Group | T1098 | #1 | ok |
| Okta Identity Provider Created | T1098 | #1 | ok |
| Okta MFA Reset or Deactivated | T1556 | #1, #7 | ambiguous |
| Potential Okta Password in AlternateID Field | T1552 | #1, #4 | ambiguous |
| Okta User Account Locked Out | T1531 | #1, #7 | ambiguous |
| Binary Padding - Linux | T1027 | #1, #7 | ambiguous |
| Linux Capabilities Discovery | T1083, T1548 | #1, #7 | ambiguous |
| File Time Attribute Change - Linux | T1070 | #1 | ok |
| Remove Immutable File Attribute - Auditd | T1222 | #1 | ok |
| Clipboard Collection with Xclip Tool - Auditd | T1115 | #1 | ok |
| Clipboard Collection of Image Data with Xclip Tool | T1115 | #1 | ok |
| Data Compressed | T1560 | #1 | ok |
| Data Exfiltration with Wget | T1048 | #1, #7 | ambiguous |
| File or Folder Permissions Change | T1222 | #1 | ok |
| Credentials In Files - Linux | T1552 | #1, #4 | ambiguous |
| Hidden Files and Directories | T1564 | #1 | ok |
| Steganography Hide Zip Information in Picture File | T1027 | #1, #7 | ambiguous |
| Masquerading as Linux Crond Process | T1036 | #1, #7 | ambiguous |
| Network Sniffing - Linux | T1040 | #1, #5 | ambiguous |
| Screen Capture with Import Tool | T1113 | #1 | ok |
| Screen Capture with Xwd | T1113 | #1 | ok |
| Steganography Hide Files with Steghide | T1027 | #1, #7 | ambiguous |
| Steganography Extract Files with Steghide | T1027 | #1, #7 | ambiguous |
| Suspicious Commands Linux | T1059 | #1, #7 | ambiguous |
| Suspicious History File Operations - Linux | T1552 | #1, #4 | ambiguous |
| Service Reload or Start - Linux | T1543 | #1, #7 | ambiguous |
| System Shutdown/Reboot - Linux | T1529 | #1, #7 | ambiguous |
| Steganography Unzip Hidden Information From Picture File | T1027 | #1, #7 | ambiguous |
| System Owner or User Discovery - Linux | T1033 | #1 | ok |
| Audio Capture | T1123 | #1 | ok |
| ASLR Disabled Via Sysctl or Direct Syscall - Linux | T1055, T1685 | #1, #7 | ambiguous |
| Linux Keylogging with Pam.d | T1003, T1056 | #1, #7 | ambiguous |
| Password Policy Discovery - Linux | T1201 | #1 | ok |
| System Information Discovery - Auditd | T1082 | #1 | ok |
| BPFDoor Abnormal Process ID or Lock File Accessed | T1059, T1106 | #1, #7 | ambiguous |
| Use Of Hidden Paths Or Files | T1574 | #1, #7 | ambiguous |
| Modification of ld.so.preload | T1574 | #1, #7 | ambiguous |
| Potential Abuse of Linux Magic System Request Key | T1059, T1489, T1499, T1529 | #1, #6, #7 | ambiguous |
| System and Hardware Information Discovery | T1082 | #1 | ok |
| Systemd Service Creation | T1543 | #1, #7 | ambiguous |
| Unix Shell Configuration Modification | T1546 | #1, #7 | ambiguous |
| Creation Of An User Account | T1136 | #1 | ok |
| Loading of Kernel Module via Insmod | T1547 | #1, #7 | ambiguous |
| Linux Network Service Scanning - Auditd | T1046 | #1 | ok |
| Split A File Into Pieces - Linux | T1030 | #1 | ok |
| System Info Discovery via Sysinfo Syscall | T1057, T1082 | #1 | ok |
| Special File Creation via Mknod Syscall | T1543 | #1, #7 | ambiguous |
| Webshell Remote Command Execution | T1505 | #1, #7 | ambiguous |
| Modifying Crontab | T1053 | #1, #7 | ambiguous |
| Equation Group Indicators | T1059 | #1, #7 | ambiguous |
| Commands to Clear or Remove the Syslog - Builtin | T1565 | #1 | ok |
| Remote File Copy | T1105 | #1 | ok |
| Code Injection by ld.so Preload | T1574 | #1, #7 | ambiguous |
| Privileged User Has Been Created | T1098, T1136 | #1 | ok |
| Linux Command History Tampering | T1070 | #1 | ok |
| Suspicious Activity in Shell Commands | T1059 | #1, #7 | ambiguous |
| Suspicious Reverse Shell Command Line | T1059 | #1, #7 | ambiguous |
| Shellshock Expression | T1505 | #1, #7 | ambiguous |
| JexBoss Command Sequence | T1059 | #1, #7 | ambiguous |
| Linux Doas Conf File Creation | T1548 | #1, #7 | ambiguous |
| Persistence Via Sudoers.d Files | T1548 | #1, #7 | ambiguous |
| New Cron File Created | T1053 | #1, #7 | ambiguous |
| Suspicious Filename with Embedded Base64 Commands | T1027, T1059 | #1, #7 | ambiguous |
| Triple Cross eBPF Rootkit Default Persistence | T1053 | #1, #7 | ambiguous |
| Wget Creating Files in Tmp Directory | T1105 | #1 | ok |
| Linux Reverse Shell Indicator | T1059 | #1, #7 | ambiguous |
| Linux Crypto Mining Pool Connections | T1496 | #1, #7 | ambiguous |
| Communication To LocaltoNet Tunneling Service Initiated - Linux | T1090, T1102, T1572 | #1, #7 | ambiguous |
| Communication To Ngrok Tunneling Service - Linux | T1090, T1102, T1567, T1568, T1572 | #1, #7 | ambiguous |
| Potentially Suspicious Malware Callback Communication - Linux | T1571 | #1, #7 | ambiguous |
| Shell Invocation via Apt - Linux | T1083 | #1 | ok |
| Scheduled Task/Job At | T1053 | #1, #7 | ambiguous |
| Suspicious Invocation of Shell via AWK - Linux | T1059 | #1, #7 | ambiguous |
| Decode Base64 Encoded Text | T1027 | #1, #7 | ambiguous |
| BPFtrace Unsafe Option Usage | T1059 | #1, #7 | ambiguous |
| Linux Setgid Capability Set on a Binary via Setcap Utility | T1548, T1554 | #1, #7 | ambiguous |
| Linux Setuid Capability Set on a Binary via Setcap Utility | T1548, T1554 | #1, #7 | ambiguous |
| Capabilities Discovery - Linux | T1083 | #1 | ok |
| Capsh Shell Invocation - Linux | T1059 | #1, #7 | ambiguous |
| Remove Immutable File Attribute | T1222 | #1 | ok |
| Chmod Targeting Sensitive Directories | T1222 | #1 | ok |
| Clipboard Collection with Xclip Tool | T1115 | #1 | ok |
| Copy Passwd Or Shadow From TMP Path | T1552 | #1, #4 | ambiguous |
| Crontab Enumeration | T1007 | #1 | ok |
| Linux Crypto Mining Indicators | T1496 | #1, #7 | ambiguous |
| Curl Usage on Linux | T1105 | #1 | ok |
| Suspicious Download and Execute Pattern via Curl/Wget | T1059, T1203 | #1, #3, #7 | ambiguous |
| Potential Linux Process Code Injection Via DD Utility | T1055 | #1, #7 | ambiguous |
| Linux Doas Tool Execution | T1548 | #1, #7 | ambiguous |
| Shell Invocation via Env Command - Linux | T1059 | #1, #7 | ambiguous |
| ESXi Network Configuration Discovery Via ESXCLI | T1007, T1033, T1059 | #1, #7 | ambiguous |
| ESXi Admin Permission Assigned To Account Via ESXCLI | T1059, T1098 | #1, #7 | ambiguous |
| ESXi Storage Information Discovery Via ESXCLI | T1007, T1033, T1059 | #1, #7 | ambiguous |
| ESXi Syslog Configuration Change Via ESXCLI | T1059, T1685, T1690 | #1, #7 | ambiguous |
| ESXi System Information Discovery Via ESXCLI | T1007, T1033, T1059 | #1, #7 | ambiguous |
| ESXi Account Creation Via ESXCLI | T1059, T1136 | #1, #7 | ambiguous |
| ESXi VM List Discovery Via ESXCLI | T1007, T1033, T1059 | #1, #7 | ambiguous |
| ESXi VM Kill Via ESXCLI | T1059, T1529 | #1, #7 | ambiguous |
| ESXi VSAN Information Discovery Via ESXCLI | T1007, T1033, T1059 | #1, #7 | ambiguous |
| File and Directory Discovery - Linux | T1083 | #1 | ok |
| File Deletion | T1070 | #1 | ok |
| Shell Execution via Find - Linux | T1083 | #1 | ok |
| Shell Execution via Flock - Linux | T1083 | #1 | ok |
| Shell Execution GCC  - Linux | T1083 | #1 | ok |
| Shell Execution via Git - Linux | T1059 | #1, #7 | ambiguous |
| OS Architecture Discovery Via Grep | T1082 | #1 | ok |
| Group Has Been Deleted Via Groupdel | T1531 | #1, #7 | ambiguous |
| Install Root Certificate | T1553 | #1, #10 | ambiguous |
| Suspicious Package Installed - Linux | T1553 | #1, #10 | ambiguous |
| Local System Accounts Discovery - Linux | T1087 | #1 | ok |
| Local Groups Discovery - Linux | T1069 | #1 | ok |
| Potential GobRAT File Discovery Via Grep | T1082 | #1 | ok |
| Mount Execution With Hidepid Parameter | T1564 | #1 | ok |
| Potential Netcat Reverse Shell Execution | T1059 | #1, #7 | ambiguous |
| Shell Execution via Nice - Linux | T1083 | #1 | ok |
| Nohup Execution | T1059 | #1, #7 | ambiguous |
| Pnscan Binary Data Transmission Activity | T1046 | #1 | ok |
| Connection Proxy | T1090 | #1, #7 | ambiguous |
| PUA - TruffleHog Execution - Linux | T1083, T1552 | #1, #4 | ambiguous |
| Python One-Liners with Base64 Decoding - Linux | T1027, T1059 | #1, #7 | ambiguous |
| Python WebServer Execution - Linux | T1048 | #1, #7 | ambiguous |
| Python Spawning Pretty TTY Via PTY Module | T1059 | #1, #7 | ambiguous |
| Inline Python Execution - Spawn Shell Via OS System Library | T1059 | #1, #7 | ambiguous |
| Linux Remote System Discovery | T1018 | #1 | ok |
| Linux Package Uninstall | T1070 | #1 | ok |
| Shell Execution via Rsync - Linux | T1059 | #1, #7 | ambiguous |
| Suspicious Invocation of Shell via Rsync | T1059, T1203 | #1, #3, #7 | ambiguous |
| Scheduled Cron Task/Job - Linux | T1053 | #1, #7 | ambiguous |
| Security Software Discovery - Linux | T1518 | #1 | ok |
| Disable Or Stop Services | T1489, T1685 | #1 | ambiguous |
| Setuid and Setgid | T1548 | #1, #7 | ambiguous |
| Shell Invocation Via Ssh - Linux | T1059 | #1, #7 | ambiguous |
| Potential Linux Amazon SSM Agent Hijacking | T1219 | #1, #7 | ambiguous |
| Container Residence Discovery Via Proc Virtual FS | T1082 | #1 | ok |
| Suspicious Curl File Upload - Linux | T1105, T1567 | #1, #7 | ambiguous |
| Docker Container Discovery Via Dockerenv Listing | T1082 | #1 | ok |
| Potentially Suspicious Execution From Tmp Folder | T1036 | #1, #7 | ambiguous |
| Potential Discovery Activity Using Find - Linux | T1083 | #1 | ok |
| History File Deletion | T1565 | #1 | ok |
| Potential Container Discovery Via Inodes Listing | T1082 | #1 | ok |
| Interactive Bash Suspicious Children | T1036, T1059 | #1, #7 | ambiguous |
| Suspicious Java Children Processes | T1059 | #1, #7 | ambiguous |
| Linux Network Service Scanning Tools Execution | T1046 | #1 | ok |
| Linux Recon Indicators | T1552, T1592 | #1, #4 | ambiguous |
| Script Interpreter Spawning Credential Scanner - Linux | T1005, T1059, T1552 | #1, #4, #7 | ambiguous |
| Potential Suspicious Change To Sensitive/Critical Files | T1565 | #1 | ok |
| System Information Discovery | T1082 | #1 | ok |
| System Network Connections Discovery - Linux | T1049 | #1 | ok |
| System Network Discovery - Linux | T1016 | #1 | ok |
| Mask System Power Settings Via Systemctl | T1653 | #1, #7 | ambiguous |
| Touch Suspicious Service File | T1070 | #1 | ok |
| User Has Been Deleted Via Userdel | T1531 | #1, #7 | ambiguous |
| Vim GTFOBin Abuse - Linux | T1083 | #1 | ok |
| Linux Webshell Indicators | T1505 | #1, #7 | ambiguous |
| Download File To Potentially Suspicious Directory Via Wget | T1105 | #1 | ok |
| Potential Xterm Reverse Shell | T1059 | #1, #7 | ambiguous |
| MacOS Emond Launch Daemon | T1546 | #1, #7 | ambiguous |
| Startup Item File Created - MacOS | T1037 | #1, #7 | ambiguous |
| MacOS Scripting Interpreter AppleScript | T1059 | #1, #7 | ambiguous |
| Decode Base64 Encoded Text -MacOs | T1027 | #1, #7 | ambiguous |
| Binary Padding - MacOS | T1027 | #1, #7 | ambiguous |
| File Time Attribute Change | T1070 | #1 | ok |
| Hidden Flag Set On File/Directory Via Chflags - MacOS | T1105, T1218, T1552, T1564 | #1, #4, #7 | ambiguous |
| Clipboard Data Collection Via OSAScript | T1059, T1115 | #1, #7 | ambiguous |
| Creation Of A Local User Account | T1136 | #1 | ok |
| Hidden User Creation | T1564 | #1 | ok |
| Credentials from Password Stores - Keychain | T1555 | #1, #4, #7 | ambiguous |
| System Integrity Protection (SIP) Disabled | T1518 | #1 | ok |
| System Integrity Protection (SIP) Enumeration | T1518 | #1 | ok |
| File and Directory Discovery - MacOS | T1083 | #1 | ok |
| Credentials In Files | T1552 | #1, #4 | ambiguous |
| GUI Input Capture - macOS | T1056 | #1, #7 | ambiguous |
| Disk Image Mounting Via Hdiutil - MacOS | T1560, T1566 | #1, #9 | ambiguous |
| Suspicious Installer Package Child Process | T1059, T1071 | #1, #7 | ambiguous |
| System Information Discovery Using Ioreg | T1082 | #1 | ok |
| JXA In-memory Execution Via OSAScript | T1059 | #1, #7 | ambiguous |
| Launch Agent/Daemon Execution Via Launchctl | T1543, T1569 | #1, #7 | ambiguous |
| Local System Accounts Discovery - MacOs | T1087 | #1 | ok |
| Local Groups Discovery - MacOs | T1069 | #1 | ok |
| MacOS Network Service Scanning | T1046 | #1 | ok |
| Network Sniffing - MacOs | T1040 | #1, #5 | ambiguous |
| File Download Via Nscurl - MacOS | T1105 | #1 | ok |
| Suspicious Microsoft Office Child Process - MacOS | T1059, T1137, T1204 | #1, #7, #9 | ambiguous |
| OSACompile Run-Only Execution | T1059 | #1, #7 | ambiguous |
| Payload Decoded and Decrypted via Built-in Utilities | T1059, T1140, T1204 | #1, #7, #9 | ambiguous |
| Potential Persistence Via PlistBuddy | T1543 | #1, #7 | ambiguous |
| Remote Access Tool - Potential MeshAgent Execution - MacOS | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - Renamed MeshAgent Execution - MacOS | T1036, T1219 | #1, #7 | ambiguous |
| Macos Remote System Discovery | T1018 | #1 | ok |
| Scheduled Cron Task/Job - MacOs | T1053 | #1, #7 | ambiguous |
| Screen Capture - macOS | T1113 | #1 | ok |
| Security Software Discovery - MacOs | T1518 | #1 | ok |
| Space After Filename - macOS | T1036 | #1, #7 | ambiguous |
| Split A File Into Pieces | T1030 | #1 | ok |
| Suspicious Browser Child Process - MacOS | T1059, T1189, T1203 | #1, #3, #7 | ambiguous |
| Suspicious Execution via macOS Script Editor | T1059, T1204, T1553, T1566 | #1, #7, #9, #10 | ambiguous |
| Potential Discovery Activity Using Find - MacOS | T1083 | #1 | ok |
| Suspicious History File Operations | T1552 | #1, #4 | ambiguous |
| Potential In-Memory Download And Compile Of Payloads | T1059, T1105 | #1, #7 | ambiguous |
| System Network Discovery - macOS | T1016 | #1 | ok |
| Osacompile Execution By Potentially Suspicious Applet/Osascript | T1059 | #1, #7 | ambiguous |
| System Information Discovery Using sw_vers | T1082 | #1 | ok |
| System Information Discovery Via Sysctl - MacOS | T1082, T1497 | #1, #7 | ambiguous |
| System Network Connections Discovery - MacOs | T1049 | #1 | ok |
| System Information Discovery Using System_Profiler | T1082, T1497 | #1, #7 | ambiguous |
| System Shutdown/Reboot - MacOs | T1529 | #1, #7 | ambiguous |
| Time Machine Backup Deletion Attempt Via Tmutil - MacOS | T1490 | #1 | ok |
| Time Machine Backup Disabled Via Tmutil - MacOS | T1490 | #1 | ok |
| New File Exclusion Added To Time Machine Via Tmutil - MacOS | T1490 | #1 | ok |
| Gatekeeper Bypass via Xattr | T1553 | #1, #10 | ambiguous |
| Cisco Clear Logs | T1070 | #1 | ok |
| Cisco Collect Data | T1005, T1087, T1552 | #1, #4 | ambiguous |
| Cisco Crypto Commands | T1552, T1553 | #1, #4, #10 | ambiguous |
| Cisco Discovery | T1016, T1018, T1033, T1049, T1057, T1082, T1083, T1124, T1201 | #1 | ok |
| Cisco Denial of Service | T1495, T1529, T1565 | #1, #7 | ambiguous |
| Cisco Dot1x Disabled | T1556, T1685 | #1, #7 | ambiguous |
| Cisco File Deletion | T1070, T1561 | #1, #7 | ambiguous |
| Cisco Show Commands Input | T1552 | #1, #4 | ambiguous |
| Cisco Local Accounts | T1098, T1136 | #1 | ok |
| Cisco Modify Configuration | T1053, T1490, T1505, T1565 | #1, #7 | ambiguous |
| Cisco Stage Data | T1074, T1105, T1560 | #1 | ok |
| Cisco Sniffing | T1040 | #1, #5 | ambiguous |
| DNS Query to External Service Interaction Domains | T1190, T1595 | #1, #2 | ambiguous |
| Monero Crypto Coin Mining Pool Lookup | T1496, T1567 | #1, #7 | ambiguous |
| Suspicious DNS Query with B64 Encoded String | T1048, T1071 | #1, #7 | ambiguous |
| Telegram Bot API Request | T1102 | #1 | ok |
| FortiGate - New Administrator Account Created | T1136 | #1 | ok |
| FortiGate - New Local User Created | T1136 | #1 | ok |
| MITRE BZAR Indicators for Execution | T1047, T1053, T1569 | #1, #7 | ambiguous |
| MITRE BZAR Indicators for Persistence | T1547 | #1, #7 | ambiguous |
| Potential PetitPotam Attack Via EFS RPC Calls | T1187, T1557 | #1, #4, #5 | ambiguous |
| SMB Spoolss Name Piped Usage | T1021 | #1, #4 | ambiguous |
| Suspicious DNS Query Indicating Kerberos Coercion via DNS Object SPN Spoofing - Network | T1187, T1557 | #1, #4, #5 | ambiguous |
| DNS Events Related To Mining Pools | T1496, T1569 | #1, #7 | ambiguous |
| Suspicious DNS Z Flag Bit Set | T1095, T1571 | #1, #7 | ambiguous |
| DNS TOR Proxies | T1048 | #1, #7 | ambiguous |
| Executable from Webdav | T1105 | #1 | ok |
| WebDav Put Request | T1048 | #1, #7 | ambiguous |
| Publicly Accessible RDP Service | T1021 | #1, #4 | ambiguous |
| Remote Task Creation via ATSVC Named Pipe - Zeek | T1053 | #1, #7 | ambiguous |
| Possible Impacket SecretDump Remote Activity - Zeek | T1003 | #1, #7 | ambiguous |
| First Time Seen Remote Named Pipe - Zeek | T1021 | #1, #4 | ambiguous |
| Suspicious PsExec Execution - Zeek | T1021 | #1, #4 | ambiguous |
| Transferring Files with Credential Data via Network Shares - Zeek | T1003 | #1, #7 | ambiguous |
| Kerberos Network Traffic RC4 Ticket Encryption | T1558 | #1, #4 | ambiguous |
| Download from Suspicious Dyndns Hosts | T1105, T1568 | #1, #7 | ambiguous |
| Potential Hello-World Scraper Botnet Activity | T1595 | #1 | ok |
| PwnDrp Access | T1071, T1102 | #1, #7 | ambiguous |
| Raw Paste Service Access | T1071, T1102 | #1, #7 | ambiguous |
| Flash Player Update from Suspicious Location | T1036, T1189, T1204 | #1, #3, #7, #9 | ambiguous |
| Suspicious Network Communication With IPFS | T1056 | #1, #7 | ambiguous |
| Telegram API Access | T1071, T1102 | #1, #7 | ambiguous |
| Bitsadmin to Uncommon IP Server Address | T1071, T1197 | #1, #7 | ambiguous |
| Bitsadmin to Uncommon TLD | T1071, T1197 | #1, #7 | ambiguous |
| Rclone Activity via Proxy | T1567 | #1, #7 | ambiguous |
| Source Code Enumeration Detection by Keyword | T1083 | #1 | ok |
| Server Side Template Injection Strings | T1221 | #1 | ok |
| Suspicious Windows Strings In URI | T1505 | #1, #7 | ambiguous |
| Webshell ReGeorg Detection Via Web Logs | T1505 | #1, #7 | ambiguous |
| Windows Webshell Strings | T1505 | #1, #7 | ambiguous |
| LSASS Process Crashed - Application | T1003 | #1, #7 | ambiguous |
| Ntdsutil Abuse | T1003 | #1, #7 | ambiguous |
| Backup Catalog Deleted | T1070 | #1 | ok |
| Restricted Software Access By SRP | T1072 | #1, #7 | ambiguous |
| Application Uninstalled | T1489 | #1 | ok |
| MSI Installation From Web | T1218 | #1, #7 | ambiguous |
| Atera Agent Installation | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - ScreenConnect Command Execution | T1059 | #1, #7 | ambiguous |
| Remote Access Tool - ScreenConnect File Transfer | T1059 | #1, #7 | ambiguous |
| AppLocker Prevented Application or Script from Running | T1059, T1204 | #1, #7, #9 | ambiguous |
| Windows AppX Deployment Full Trust Package Installation | T1204, T1553 | #1, #7, #9, #10 | ambiguous |
| Windows AppX Deployment Unsigned Package Installation | T1204, T1553 | #1, #7, #9, #10 | ambiguous |
| New BITS Job Created Via Bitsadmin | T1197 | #1, #7 | ambiguous |
| New BITS Job Created Via PowerShell | T1197 | #1, #7 | ambiguous |
| BITS Transfer Job Downloading File Potential Suspicious Extension | T1197 | #1, #7 | ambiguous |
| BITS Transfer Job Download From File Sharing Domains | T1197 | #1, #7 | ambiguous |
| BITS Transfer Job Download From Direct IP | T1197 | #1, #7 | ambiguous |
| BITS Transfer Job With Uncommon Or Suspicious Remote TLD | T1197 | #1, #7 | ambiguous |
| BITS Transfer Job Download To Potential Suspicious Folder | T1197 | #1, #7 | ambiguous |
| Certificate Private Key Acquired | T1649 | #1, #4 | ambiguous |
| Certificate Exported From Local Certificate Store | T1649 | #1, #4 | ambiguous |
| CodeIntegrity - Blocked Image/Driver Load For Policy Violation | T1543 | #1, #7 | ambiguous |
| CodeIntegrity - Blocked Driver Load With Revoked Certificate | T1543 | #1, #7 | ambiguous |
| DNS Query for Anonfiles.com Domain - DNS Client | T1567 | #1, #7 | ambiguous |
| DNS Query To MEGA Hosting Website - DNS Client | T1567 | #1, #7 | ambiguous |
| Query Tor Onion Address - DNS Client | T1090 | #1, #7 | ambiguous |
| DNS Query To Ufile.io - DNS Client | T1567 | #1, #7 | ambiguous |
| DNS Server Error Failed Loading the ServerLevelPluginDLL | T1574 | #1, #7 | ambiguous |
| ETW Logging/Processing Option Disabled On IIS Server | T1505, T1685 | #1, #7 | ambiguous |
| HTTP Logging Disabled On IIS Server | T1505, T1685 | #1, #7 | ambiguous |
| New Module Module Added To IIS Server | T1505, T1685 | #1, #7 | ambiguous |
| Previously Installed IIS Module Was Removed | T1505, T1685 | #1, #7 | ambiguous |
| Potential Active Directory Reconnaissance/Enumeration Via LDAP | T1069, T1087, T1482 | #1 | ok |
| Certificate Request Export to Exchange Webserver | T1505 | #1, #7 | ambiguous |
| Mailbox Export to Exchange Webserver | T1505 | #1, #7 | ambiguous |
| Remove Exported Mailbox from Exchange Webserver | T1070 | #1 | ok |
| Exchange Set OabVirtualDirectory ExternalUrl Property | T1505 | #1, #7 | ambiguous |
| MSExchange Transport Agent Installation - Builtin | T1505 | #1, #7 | ambiguous |
| Failed MSExchange Transport Agent Installation | T1505 | #1, #7 | ambiguous |
| Potential Remote Desktop Connection to Non-Domain Host | T1219 | #1, #7 | ambiguous |
| OpenSSH Server Listening On Socket | T1021 | #1, #4 | ambiguous |
| Potential Access Token Abuse | T1134 | #1, #4 | ambiguous |
| A Member Was Added to a Security-Enabled Global Group | T1098 | #1 | ok |
| A Member Was Removed From a Security-Enabled Global Group | T1098 | #1 | ok |
| RDP Login from Localhost | T1021 | #1, #4 | ambiguous |
| A Security-Enabled Global Group Was Deleted | T1098 | #1 | ok |
| Potential Privilege Escalation via Local Kerberos Relay over LDAP | T1548 | #1, #7 | ambiguous |
| Successful Account Login Via WMI | T1047 | #1, #7 | ambiguous |
| Azure AD Health Monitoring Agent Registry Keys Access | T1012 | #1 | ok |
| Azure AD Health Service Agents Registry Keys Access | T1012 | #1 | ok |
| Powerview Add-DomainObjectAcl DCSync AD Extend Right | T1098 | #1 | ok |
| AD Privileged Users or Groups Reconnaissance | T1087 | #1 | ok |
| AD Object WriteDAC Access | T1222 | #1 | ok |
| Active Directory Replication from Non Machine Account | T1003 | #1, #7 | ambiguous |
| Potential AD User Enumeration From Non-Machine Account | T1087 | #1 | ok |
| Add or Remove Computer from DC | T1207 | #1, #4 | ambiguous |
| Access To ADMIN$ Network Share | T1021 | #1, #4 | ambiguous |
| Enabled User Right in AD to Control User Objects | T1098 | #1 | ok |
| Active Directory User Backdoors | T1098 | #1 | ok |
| Hacktool Ruler | T1059, T1087, T1114, T1550 | #1, #4, #7 | ambiguous |
| Remote Task Creation via ATSVC Named Pipe | T1053 | #1, #7 | ambiguous |
| Processes Accessing the Microphone and Webcam | T1123 | #1 | ok |
| CobaltStrike Service Installations - Security | T1021, T1543, T1569 | #1, #4, #7 | ambiguous |
| Failed Code Integrity Checks | T1027 | #1, #7 | ambiguous |
| DCERPC SMB Spoolss Named Pipe | T1021 | #1, #4 | ambiguous |
| DCOM InternetExplorer.Application Iertutil DLL Hijack - Security | T1021 | #1, #4 | ambiguous |
| Mimikatz DC Sync | T1003 | #1, #7 | ambiguous |
| Windows Default Domain GPO Modification | T1484 | #1 | ok |
| ETW Logging Disabled In .NET Processes - Registry | T1112, T1685 | #1 | ambiguous |
| DPAPI Domain Backup Key Extraction | T1003 | #1, #7 | ambiguous |
| DPAPI Domain Master Key Backup Attempt | T1003 | #1, #7 | ambiguous |
| Persistence and Execution at Scale via GPO Scheduled Task | T1053 | #1, #7 | ambiguous |
| Hidden Local User Creation | T1136 | #1 | ok |
| HackTool - NoFilter Execution | T1134 | #1, #4 | ambiguous |
| HybridConnectionManager Service Installation | T1554 | #1, #7 | ambiguous |
| Impacket PsExec Execution | T1021 | #1, #4 | ambiguous |
| Possible Impacket SecretDump Remote Activity | T1003 | #1, #7 | ambiguous |
| Invoke-Obfuscation CLIP+ Launcher - Security | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Obfuscated IEX Invocation - Security | T1027 | #1, #7 | ambiguous |
| Invoke-Obfuscation STDIN+ Launcher - Security | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation VAR+ Launcher - Security | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation COMPRESS OBFUSCATION - Security | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation RUNDLL LAUNCHER - Security | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Stdin - Security | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use Clip - Security | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use MSHTA - Security | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use Rundll32 - Security | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation VAR++ LAUNCHER OBFUSCATION - Security | T1027, T1059 | #1, #7 | ambiguous |
| Kerberoasting Activity - Initial Query | T1558 | #1, #4 | ambiguous |
| First Time Seen Remote Named Pipe | T1021 | #1, #4 | ambiguous |
| LSASS Access From Non System Account | T1003 | #1, #7 | ambiguous |
| Credential Dumping Tools Service Execution - Security | T1003, T1569 | #1, #7 | ambiguous |
| WCE wceaux.dll Access | T1003 | #1, #7 | ambiguous |
| Metasploit SMB Authentication | T1021 | #1, #4 | ambiguous |
| Metasploit Or Impacket Service Installation Via SMB PsExec | T1021, T1569, T1570 | #1, #4, #7 | ambiguous |
| Meterpreter or Cobalt Strike Getsystem Service Installation - Security | T1134 | #1, #4 | ambiguous |
| NetNTLM Downgrade Attack | T1112, T1685 | #1 | ambiguous |
| Windows Network Access Suspicious desktop.ini Action | T1547 | #1, #7 | ambiguous |
| New or Renamed User Account with '$' Character | T1036 | #1, #7 | ambiguous |
| Denied Access To Remote Desktop | T1021 | #1, #4 | ambiguous |
| Password Policy Enumerated | T1201 | #1 | ok |
| Windows Pcap Drivers | T1040 | #1, #5 | ambiguous |
| Possible PetitPotam Coerce Authentication Attempt | T1187 | #1, #4 | ambiguous |
| PetitPotam Suspicious Kerberos TGT Request | T1187 | #1, #4 | ambiguous |
| Possible DC Shadow Attack | T1207 | #1, #4 | ambiguous |
| PowerShell Scripts Installed as Services - Security | T1569 | #1, #7 | ambiguous |
| Protected Storage Service Access | T1021 | #1, #4 | ambiguous |
| RDP over Reverse SSH Tunnel WFP | T1021, T1090 | #1, #4, #7 | ambiguous |
| Register new Logon Process by Rubeus | T1558 | #1, #4 | ambiguous |
| Service Registry Key Read Access Request | T1574 | #1, #7 | ambiguous |
| Remote PowerShell Sessions Network Connections (WinRM) | T1059 | #1, #7 | ambiguous |
| Replay Attack Detected | T1558 | #1, #4 | ambiguous |
| SAM Registry Hive Handle Request | T1012, T1552 | #1, #4 | ambiguous |
| SCM Database Handle Failure | T1010 | #1 | ok |
| SCM Database Privileged Operation | T1548 | #1, #7 | ambiguous |
| Potential Secure Deletion with SDelete | T1027, T1070, T1485, T1553 | #1, #7, #10 | ambiguous |
| Remote Access Tool Services Have Been Installed - Security | T1543, T1569 | #1, #7 | ambiguous |
| Service Installed By Unusual Client - Security | T1543 | #1, #7 | ambiguous |
| File Access Of Signal Desktop Sensitive Data | T1003 | #1, #7 | ambiguous |
| SMB Create Remote File Admin Share | T1021 | #1, #4 | ambiguous |
| A New Trust Was Created To A Domain | T1098 | #1 | ok |
| Addition of SID History to Active Directory Object | T1134 | #1, #4 | ambiguous |
| Password Change on Directory Service Restore Mode (DSRM) Account | T1098 | #1 | ok |
| Group Policy Abuse for Privilege Addition | T1484 | #1 | ok |
| Startup/Logon Script Added to Group Policy Object | T1484, T1547 | #1, #7 | ambiguous |
| Suspicious LDAP-Attributes Used | T1001 | #1, #7 | ambiguous |
| Suspicious Windows ANONYMOUS LOGON Local Account Created | T1136 | #1 | ok |
| Password Dumper Activity on LSASS | T1003 | #1, #7 | ambiguous |
| Potentially Suspicious AccessMask Requested From LSASS | T1003 | #1, #7 | ambiguous |
| Reconnaissance Activity | T1069, T1087 | #1 | ok |
| Password Protected ZIP File Opened | T1027 | #1, #7 | ambiguous |
| Password Protected ZIP File Opened (Suspicious Filenames) | T1027, T1036, T1105 | #1, #7 | ambiguous |
| Password Protected ZIP File Opened (Email Attachment) | T1027, T1566 | #1, #7, #9 | ambiguous |
| Uncommon Outbound Kerberos Connection - Security | T1558 | #1, #4 | ambiguous |
| Possible Shadow Credentials Added | T1556 | #1, #7 | ambiguous |
| Suspicious PsExec Execution | T1021 | #1, #4 | ambiguous |
| Suspicious Access to Sensitive File Extensions | T1039 | #1 | ok |
| Suspicious Kerberos RC4 Ticket Encryption | T1558 | #1, #4 | ambiguous |
| Suspicious Scheduled Task Creation | T1053 | #1, #7 | ambiguous |
| Important Scheduled Task Deleted/Disabled | T1053 | #1, #7 | ambiguous |
| Suspicious Scheduled Task Update | T1053 | #1, #7 | ambiguous |
| Unauthorized System Time Modification | T1070 | #1 | ok |
| Remote Service Activity via SVCCTL Named Pipe | T1021 | #1, #4 | ambiguous |
| SysKey Registry Keys Access | T1012 | #1 | ok |
| Sysmon Channel Reference Deletion | T1112 | #1 | ok |
| Tap Driver Installation - Security | T1048 | #1, #7 | ambiguous |
| Suspicious Teams Application Related ObjectAcess Event | T1528 | #1, #4, #9 | ambiguous |
| Transferring Files with Credential Data via Network Shares | T1003 | #1, #7 | ambiguous |
| User Added to Local Administrator Group | T1078, T1098 | #1, #4 | ambiguous |
| User Couldn't Call a Privileged Service 'LsaRegisterLogonProcess' | T1558 | #1, #4 | ambiguous |
| Local User Creation | T1136 | #1 | ok |
| User Logoff Event | T1531 | #1, #7 | ambiguous |
| VSSAudit Security Event Source Registration | T1003 | #1, #7 | ambiguous |
| WMI Persistence - Security | T1546 | #1, #7 | ambiguous |
| T1047 Wmiprvse Wbemcomn DLL Hijack | T1021, T1047 | #1, #4, #7 | ambiguous |
| Microsoft Defender Blocked from Loading Unsigned DLL | T1574 | #1, #7 | ambiguous |
| Unsigned Binary Loaded From Suspicious Location | T1574 | #1, #7 | ambiguous |
| HybridConnectionManager Service Running | T1554 | #1, #7 | ambiguous |
| Unsigned or Unencrypted SMB Connection to Share Established | T1021 | #1, #4 | ambiguous |
| Active Directory Certificate Services Denied Certificate Enrollment Request | T1553 | #1, #10 | ambiguous |
| DHCP Server Loaded the CallOut DLL | T1574 | #1, #7 | ambiguous |
| DHCP Server Error Failed Loading the CallOut DLL | T1574 | #1, #7 | ambiguous |
| ISATAP Router Address Was Set | T1557, T1565 | #1, #5 | ambiguous |
| No Suitable Encryption Key Found For Generating Kerberos Ticket | T1558 | #1, #4 | ambiguous |
| Critical Hive In Suspicious Location Access Bits Cleared | T1003 | #1, #7 | ambiguous |
| Volume Shadow Copy Mount | T1003 | #1, #7 | ambiguous |
| Crash Dump Created By Operating System | T1003, T1005 | #1, #7 | ambiguous |
| Vulnerable Netlogon Secure Channel Connection Allowed | T1548 | #1, #7 | ambiguous |
| CobaltStrike Service Installations - System | T1021, T1543, T1569 | #1, #4, #7 | ambiguous |
| smbexec.py Service Installation | T1021, T1569 | #1, #4, #7 | ambiguous |
| Invoke-Obfuscation CLIP+ Launcher - System | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Obfuscated IEX Invocation - System | T1027 | #1, #7 | ambiguous |
| Invoke-Obfuscation STDIN+ Launcher - System | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation VAR+ Launcher - System | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation COMPRESS OBFUSCATION - System | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation RUNDLL LAUNCHER - System | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Stdin - System | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use Clip - System | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use MSHTA - System | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use Rundll32 - System | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation VAR++ LAUNCHER OBFUSCATION - System | T1027, T1059 | #1, #7 | ambiguous |
| KrbRelayUp Service Installation | T1543 | #1, #7 | ambiguous |
| Credential Dumping Tools Service Execution - System | T1003, T1569 | #1, #7 | ambiguous |
| Meterpreter or Cobalt Strike Getsystem Service Installation - System | T1134 | #1, #4 | ambiguous |
| Moriya Rootkit - System | T1543 | #1, #7 | ambiguous |
| PowerShell Scripts Installed as Services | T1569 | #1, #7 | ambiguous |
| CSExec Service Installation | T1569 | #1, #7 | ambiguous |
| HackTool Service Registration or Execution | T1569 | #1, #7 | ambiguous |
| Mesh Agent Service Installation | T1219 | #1, #7 | ambiguous |
| PAExec Service Installation | T1569 | #1, #7 | ambiguous |
| New PDQDeploy Service - Server Side | T1543 | #1, #7 | ambiguous |
| New PDQDeploy Service - Client Side | T1543 | #1, #7 | ambiguous |
| ProcessHacker Privilege Elevation | T1543, T1569 | #1, #7 | ambiguous |
| RemCom Service Installation | T1569 | #1, #7 | ambiguous |
| Remote Access Tool Services Have Been Installed - System | T1543, T1569 | #1, #7 | ambiguous |
| Sliver C2 Default Service Installation | T1543, T1569 | #1, #7 | ambiguous |
| Service Installed By Unusual Client - System | T1543 | #1, #7 | ambiguous |
| Suspicious Service Installation | T1543 | #1, #7 | ambiguous |
| PsExec Service Installation | T1569 | #1, #7 | ambiguous |
| TacticalRMM Service Installation | T1219 | #1, #7 | ambiguous |
| Tap Driver Installation | T1048 | #1, #7 | ambiguous |
| Uncommon Service Installation Image Path | T1543 | #1, #7 | ambiguous |
| Service Installation in Suspicious Folder | T1543 | #1, #7 | ambiguous |
| Service Installation with Suspicious Folder Pattern | T1543 | #1, #7 | ambiguous |
| Suspicious Service Installation Script | T1543 | #1, #7 | ambiguous |
| Scheduled Task Executed From A Suspicious Location | T1053 | #1, #7 | ambiguous |
| Scheduled Task Executed Uncommon LOLBIN | T1053 | #1, #7 | ambiguous |
| Important Scheduled Task Deleted or Disabled | T1489 | #1 | ok |
| Ngrok Usage with Remote Desktop Service | T1090 | #1, #7 | ambiguous |
| Mimikatz Use | T1003 | #1, #7 | ambiguous |
| LSASS Access Detected via Attack Surface Reduction | T1003 | #1, #7 | ambiguous |
| PSExec and WMI Process Creations Block | T1047, T1569 | #1, #7 | ambiguous |
| Windows Defender AMSI Trigger Detected | T1059 | #1, #7 | ambiguous |
| Windows Defender Threat Detected | T1059 | #1, #7 | ambiguous |
| WMI Persistence | T1546 | #1, #7 | ambiguous |
| HackTool - CACTUSTORCH Remote Thread Creation | T1055, T1059, T1218 | #1, #7 | ambiguous |
| HackTool - Potential CobaltStrike Process Injection | T1055 | #1, #7 | ambiguous |
| Remote Thread Created In KeePass.EXE | T1555 | #1, #4, #7 | ambiguous |
| Potential Credential Dumping Attempt Via PowerShell Remote Thread | T1003 | #1, #7 | ambiguous |
| Remote Thread Creation Via PowerShell In Uncommon Target | T1059, T1218 | #1, #7 | ambiguous |
| Password Dumper Remote Thread in LSASS | T1003 | #1, #7 | ambiguous |
| Rare Remote Thread Creation By Uncommon Source Image | T1055 | #1, #7 | ambiguous |
| Remote Thread Creation By Uncommon Source Image | T1055 | #1, #7 | ambiguous |
| Remote Thread Creation In Uncommon Target Image | T1055 | #1, #7 | ambiguous |
| Remote Thread Creation Ttdinject.exe Proxy | T1127 | #1, #7 | ambiguous |
| Hidden Executable In NTFS Alternate Data Stream | T1564 | #1 | ok |
| Suspicious File Download From File Sharing Websites -  File Stream | T1564 | #1 | ok |
| Unusual File Download From File Sharing Websites - File Stream | T1564 | #1 | ok |
| HackTool Named File Stream Created | T1564 | #1 | ok |
| Exports Registry Key To an Alternate Data Stream | T1564 | #1 | ok |
| Unusual File Download from Direct IP Address | T1564 | #1 | ok |
| DNS Query for Anonfiles.com Domain - Sysmon | T1567 | #1, #7 | ambiguous |
| AppX Package Installation Attempts Via AppInstaller.EXE | T1105 | #1 | ok |
| Cloudflared Tunnels Related DNS Requests | T1071, T1572 | #1, #7 | ambiguous |
| DNS Query To Devtunnels Domain | T1071, T1572 | #1, #7 | ambiguous |
| DNS Server Discovery Via LDAP Query | T1482 | #1 | ok |
| DNS Query To AzureWebsites.NET By Non-Browser Process | T1219 | #1, #7 | ambiguous |
| DNS Query by Finger Utility | T1059, T1071 | #1, #7 | ambiguous |
| DNS HybridConnectionManager Service Bus | T1554 | #1, #7 | ambiguous |
| Suspicious DNS Query Indicating Kerberos Coercion via DNS Object SPN Spoofing | T1187, T1557 | #1, #4, #5 | ambiguous |
| DNS Query To MEGA Hosting Website | T1567 | #1, #7 | ambiguous |
| DNS Query Request To OneLaunch Update Service | T1056 | #1, #7 | ambiguous |
| DNS Query Request By Regsvr32.EXE | T1218, T1559 | #1, #7 | ambiguous |
| DNS Query To Remote Access Software Domain From Non-Browser App | T1219 | #1, #7 | ambiguous |
| TeamViewer Domain Query By Non-TeamViewer Application | T1219 | #1, #7 | ambiguous |
| DNS Query Tor .Onion Address - Sysmon | T1090 | #1, #7 | ambiguous |
| DNS Query To Ufile.io | T1567 | #1, #7 | ambiguous |
| Malicious Driver Load | T1068, T1543 | #1, #2, #3, #7 | ambiguous |
| Malicious Driver Load By Name | T1068, T1543 | #1, #2, #3, #7 | ambiguous |
| PUA - Process Hacker Driver Load | T1543 | #1, #7 | ambiguous |
| PUA - System Informer Driver Load | T1543 | #1, #7 | ambiguous |
| Driver Load From A Temporary Directory | T1543 | #1, #7 | ambiguous |
| Vulnerable Driver Load | T1068, T1543 | #1, #2, #3, #7 | ambiguous |
| Vulnerable Driver Load By Name | T1068, T1543 | #1, #2, #3, #7 | ambiguous |
| Vulnerable HackSys Extreme Vulnerable Driver Load | T1543 | #1, #7 | ambiguous |
| Vulnerable WinRing0 Driver Load | T1543 | #1, #7 | ambiguous |
| WinDivert Driver Load | T1557, T1599 | #1, #2, #5 | ambiguous |
| Credential Manager Access By Uncommon Applications | T1003 | #1, #7 | ambiguous |
| Access To Windows Credential History File By Uncommon Applications | T1555 | #1, #4, #7 | ambiguous |
| Access To Crypto Currency Wallets By Uncommon Applications | T1003 | #1, #7 | ambiguous |
| Access To Windows DPAPI Master Keys By Uncommon Applications | T1555 | #1, #4, #7 | ambiguous |
| Access To Potentially Sensitive Sysvol Files By Uncommon Applications | T1552 | #1, #4 | ambiguous |
| Suspicious File Access to Browser Credential Storage | T1217, T1555 | #1, #4, #7 | ambiguous |
| Microsoft Teams Sensitive File Access By Uncommon Applications | T1528 | #1, #4, #9 | ambiguous |
| Backup Files Deleted | T1490 | #1 | ok |
| EventLog EVTX File Deleted | T1070 | #1 | ok |
| Exchange PowerShell Cmdlet History Deleted | T1070 | #1 | ok |
| IIS WebServer Access Logs Deleted | T1070 | #1 | ok |
| PowerShell Console History Logs Deleted | T1070 | #1 | ok |
| Prefetch File Deleted | T1070 | #1 | ok |
| TeamViewer Log File Deleted | T1070 | #1 | ok |
| Tomcat WebServer Logs Deleted | T1070 | #1 | ok |
| File Deleted Via Sysinternals SDelete | T1070 | #1 | ok |
| ADS Zone.Identifier Deleted By Uncommon Application | T1070 | #1 | ok |
| ADSI-Cache File Creation By Uncommon Tool | T1001 | #1, #7 | ambiguous |
| Advanced IP Scanner - File Event | T1046 | #1 | ok |
| Anydesk Temporary Artefact | T1219 | #1, #7 | ambiguous |
| Suspicious Binary Writes Via AnyDesk | T1219 | #1, #7 | ambiguous |
| Suspicious File Created by ArcSOC.exe | T1105, T1127, T1133 | #1, #4, #7 | ambiguous |
| BloodHound Collection Files | T1059, T1069, T1087, T1482 | #1, #7 | ambiguous |
| Potentially Suspicious File Creation by OpenEDR's ITSMService | T1105, T1219, T1570 | #1, #4, #7 | ambiguous |
| Creation Of Non-Existent System DLL | T1574 | #1, #7 | ambiguous |
| Suspicious Deno File Written from Remote Source | T1059, T1105, T1204 | #1, #7, #9 | ambiguous |
| New Custom Shim Database Created | T1547 | #1, #7 | ambiguous |
| Suspicious Screensaver Binary File Creation | T1546 | #1, #7 | ambiguous |
| Files With System DLL Name In Unsuspected Locations | T1036 | #1, #7 | ambiguous |
| Files With System Process Name In Unsuspected Locations | T1036 | #1, #7 | ambiguous |
| Creation Exe for Service with Unquoted Path | T1547 | #1, #7 | ambiguous |
| Cred Dump Tools Dropped Files | T1003 | #1, #7 | ambiguous |
| WScript or CScript Dropper - File | T1059 | #1, #7 | ambiguous |
| CSExec Service File Creation | T1569 | #1, #7 | ambiguous |
| Dynamic CSharp Compile Artefact | T1027 | #1, #7 | ambiguous |
| Potential DCOM InternetExplorer.Application DLL Hijack | T1021 | #1, #4 | ambiguous |
| Desktop.INI Created by Uncommon Process | T1547 | #1, #7 | ambiguous |
| DLL Search Order Hijackig Via Additional Space in Path | T1574 | #1, #7 | ambiguous |
| Suspicious ASPX File Drop by Exchange | T1505 | #1, #7 | ambiguous |
| Suspicious File Drop by Exchange | T1190, T1505 | #1, #2, #7 | ambiguous |
| GoToAssist Temporary Installation Artefact | T1219 | #1, #7 | ambiguous |
| HackTool - CrackMapExec File Indicators | T1003 | #1, #7 | ambiguous |
| HackTool - Dumpert Process Dumper Default File | T1003 | #1, #7 | ambiguous |
| HackTool - Typical HiveNightmare SAM File Export | T1552 | #1, #4 | ambiguous |
| HackTool - Inveigh Execution Artefacts | T1219 | #1, #7 | ambiguous |
| HackTool - RemoteKrbRelay SMB Relay Secrets Dump Module Indicators | T1219 | #1, #7 | ambiguous |
| HackTool - Mimikatz Kirbi File Creation | T1558 | #1, #4 | ambiguous |
| HackTool - NetExec File Indicators | T1021, T1059 | #1, #4, #7 | ambiguous |
| HackTool - Powerup Write Hijack DLL | T1574 | #1, #7 | ambiguous |
| HackTool - QuarksPwDump Dump File | T1003 | #1, #7 | ambiguous |
| HackTool - Potential Remote Credential Dumping Activity Via CrackMapExec Or Impacket-Secretsdump | T1003 | #1, #7 | ambiguous |
| HackTool - SafetyKatz Dump Indicator | T1003 | #1, #7 | ambiguous |
| HackTool - Impacket File Indicators | T1003 | #1, #7 | ambiguous |
| Potential Initial Access via DLL Search Order Hijacking | T1566, T1574 | #1, #7, #9 | ambiguous |
| Installation of TeamViewer Desktop | T1219 | #1, #7 | ambiguous |
| Malicious DLL File Dropped in the Teams or OneDrive Folder | T1574 | #1, #7 | ambiguous |
| LSASS Process Memory Dump Files | T1003 | #1, #7 | ambiguous |
| LSASS Process Dump Artefact In CrashDumps Folder | T1003 | #1, #7 | ambiguous |
| WerFault LSASS Process Memory Dump | T1003 | #1, #7 | ambiguous |
| Adwind RAT / JRAT File Artifact | T1059 | #1, #7 | ambiguous |
| File Creation In Suspicious Directory By Msdt.EXE | T1547 | #1, #7 | ambiguous |
| Suspicious DotNET CLR Usage Log Artifact | T1218 | #1, #7 | ambiguous |
| SCR File Write Event | T1218 | #1, #7 | ambiguous |
| NTDS.DIT Created | T1003 | #1, #7 | ambiguous |
| NTDS.DIT Creation By Uncommon Parent Process | T1003 | #1, #7 | ambiguous |
| NTDS.DIT Creation By Uncommon Process | T1003 | #1, #7 | ambiguous |
| NTDS Exfiltration Filename Patterns | T1003 | #1, #7 | ambiguous |
| Potential Persistence Via Microsoft Office Add-In | T1137 | #1, #7 | ambiguous |
| New Outlook Macro Created | T1008, T1137, T1546 | #1, #7 | ambiguous |
| Potential Persistence Via Outlook Form | T1137 | #1, #7 | ambiguous |
| Suspicious Outlook Macro Created | T1008, T1137, T1546 | #1, #7 | ambiguous |
| Potential Persistence Via Microsoft Office Startup Folder | T1137 | #1, #7 | ambiguous |
| PCRE.NET Package Temp Files | T1059 | #1, #7 | ambiguous |
| Suspicious File Created In PerfLogs | T1059 | #1, #7 | ambiguous |
| Malicious PowerShell Scripts - FileCreation | T1059 | #1, #7 | ambiguous |
| Potential Startup Shortcut Persistence Via PowerShell.EXE | T1547 | #1, #7 | ambiguous |
| Rclone Config File Creation | T1567 | #1, #7 | ambiguous |
| Potential Winnti Dropper Activity | T1027 | #1, #7 | ambiguous |
| RemCom Service File Creation | T1569 | #1, #7 | ambiguous |
| ScreenConnect Temporary Installation Artefact | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - ScreenConnect Temporary File | T1059 | #1, #7 | ambiguous |
| Potential RipZip Attack on Startup Folder | T1547 | #1, #7 | ambiguous |
| Potential SAM Database Dump | T1003 | #1, #7 | ambiguous |
| Self Extraction Directive File Created In Potentially Suspicious Location | T1218 | #1, #7 | ambiguous |
| Windows Shell/Scripting Application File Write to Suspicious Folder | T1059 | #1, #7 | ambiguous |
| Windows Binaries Write Suspicious Extensions | T1036 | #1, #7 | ambiguous |
| Startup Folder File Write | T1547 | #1, #7 | ambiguous |
| Suspicious Creation with Colorcpl | T1564 | #1 | ok |
| Created Files by Microsoft Sync Center | T1055, T1218 | #1, #7 | ambiguous |
| Suspicious Files in Default GPO Folder | T1036 | #1, #7 | ambiguous |
| Suspicious Desktopimgdownldr Target File | T1105 | #1 | ok |
| Suspicious Double Extension Files | T1036 | #1, #7 | ambiguous |
| DPAPI Backup Keys And Certificate Export Activity IOC | T1552, T1555 | #1, #4, #7 | ambiguous |
| Suspicious MSExchangeMailboxReplication ASPX Write | T1190, T1505 | #1, #2, #7 | ambiguous |
| Suspicious Executable File Creation | T1564 | #1 | ok |
| Suspicious File Write to Webapps Root Directory | T1190, T1505 | #1, #2, #7 | ambiguous |
| Suspicious File Write to SharePoint Layouts Directory | T1190, T1505 | #1, #2, #7 | ambiguous |
| Suspicious Get-Variable.exe Creation | T1027, T1546 | #1, #7 | ambiguous |
| Potential Hidden Directory Creation Via NTFS INDEX_ALLOCATION Stream | T1564 | #1 | ok |
| Potential Homoglyph Attack Using Lookalike Characters in Filename | T1036 | #1, #7 | ambiguous |
| Legitimate Application Dropped Archive | T1218 | #1, #7 | ambiguous |
| Legitimate Application Dropped Executable | T1218 | #1, #7 | ambiguous |
| Legitimate Application Writing Files In Uncommon Location | T1105, T1218 | #1, #7 | ambiguous |
| Legitimate Application Dropped Script | T1218 | #1, #7 | ambiguous |
| Suspicious LNK Double Extension File Created | T1036 | #1, #7 | ambiguous |
| PowerShell Profile Modification | T1546 | #1, #7 | ambiguous |
| Potential File Extension Spoofing Using Right-to-Left Override | T1036 | #1, #7 | ambiguous |
| Suspicious Startup Folder Persistence | T1204, T1547 | #1, #7, #9 | ambiguous |
| Suspicious Interactive PowerShell as SYSTEM | T1059 | #1, #7 | ambiguous |
| Suspicious Scheduled Task Write to System32 Tasks | T1053 | #1, #7 | ambiguous |
| TeamViewer Remote Session | T1219 | #1, #7 | ambiguous |
| VsCode Powershell Profile Modification | T1546 | #1, #7 | ambiguous |
| Windows Terminal Profile Settings Modification By Uncommon Process | T1547 | #1, #7 | ambiguous |
| ADExplorer Writing Complete AD Snapshot Into .dat File | T1069, T1087, T1482 | #1 | ok |
| PsExec Service File Creation | T1569 | #1, #7 | ambiguous |
| PSEXEC Remote Execution File Artefact | T1136, T1543, T1570 | #1, #4, #7 | ambiguous |
| LSASS Process Memory Dump Creation Via Taskmgr.EXE | T1003 | #1, #7 | ambiguous |
| Hijack Legit RDP Session to Move Laterally | T1219 | #1, #7 | ambiguous |
| UAC Bypass Using Consent and Comctl32 - File | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using .NET Code Profiler on MMC | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using IDiagnostic Profile - File | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using IEInstal - File | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using MSConfig Token Modification - File | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using NTFS Reparse Point - File | T1548 | #1, #7 | ambiguous |
| UAC Bypass Abusing Winsat Path Parsing - File | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using Windows Media Player - File | T1548 | #1, #7 | ambiguous |
| Potential Webshell Creation On Static Website | T1505 | #1, #7 | ambiguous |
| Creation of WerFault.exe/Wer.dll in Unusual Folder | T1574 | #1, #7 | ambiguous |
| WinRAR Creating Files in Startup Locations | T1547 | #1, #7 | ambiguous |
| AWL Bypass with Winrm.vbs and Malicious WsmPty.xsl/WsmTxt.xsl - File | T1216 | #1, #7 | ambiguous |
| WMI Persistence - Script Event Consumer File Write | T1546 | #1, #7 | ambiguous |
| Wmiexec Default Output File | T1047 | #1, #7 | ambiguous |
| Wmiprvse Wbemcomn DLL Hijack - File | T1021, T1047 | #1, #4, #7 | ambiguous |
| UEFI Persistence Via Wpbbin - FileCreation | T1542 | #1, #7 | ambiguous |
| Writing Local Admin Share | T1546 | #1, #7 | ambiguous |
| Potentially Suspicious Self Extraction Directive File Created | T1218 | #1, #7 | ambiguous |
| Clfs.SYS Loaded By Process Located In a Potential Suspicious Location | T1059 | #1, #7 | ambiguous |
| DLL Loaded From Suspicious Location Via Cmspt.EXE | T1218 | #1, #7 | ambiguous |
| Potential Azure Browser SSO Abuse | T1574 | #1, #7 | ambiguous |
| Suspicious Renamed Comsvcs DLL Loaded By Rundll32 | T1003 | #1, #7 | ambiguous |
| CredUI.DLL Loaded By Uncommon Process | T1056 | #1, #7 | ambiguous |
| Suspicious Unsigned Dbghelp/Dbgcore DLL Loaded | T1003 | #1, #7 | ambiguous |
| PCRE.NET Package Image Load | T1059 | #1, #7 | ambiguous |
| Diagnostic Library Sdiageng.DLL Loaded By Msdt.EXE | T1202 | #1 | ok |
| PowerShell Core DLL Loaded By Non PowerShell Process | T1059 | #1, #7 | ambiguous |
| Time Travel Debugging Utility Usage - Image | T1003, T1218 | #1, #7 | ambiguous |
| Unsigned .node File Loaded | T1036, T1129, T1574 | #1, #7 | ambiguous |
| Suspicious Volume Shadow Copy VSS_PS.dll Load | T1490 | #1 | ok |
| Suspicious Volume Shadow Copy Vssapi.dll Load | T1490 | #1 | ok |
| Potentially Suspicious Volume Shadow Copy Vsstrace.dll Load | T1490 | #1 | ok |
| Potential DCOM InternetExplorer.Application DLL Hijack - Image Load | T1021 | #1, #4 | ambiguous |
| Unsigned Image Loaded Into LSASS Process | T1003 | #1, #7 | ambiguous |
| WMI ActiveScriptEventConsumers Activity Via Scrcons.EXE DLL Load | T1546 | #1, #7 | ambiguous |
| Potential 7za.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Abusable DLL Potential Sideloading From Suspicious Location | T1059 | #1, #7 | ambiguous |
| Potential Antivirus Software DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential appverifUI.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Aruba Network Service Potential DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential AVKkid.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential CCleanerDU.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential CCleanerReactivator.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential Chrome Frame Helper DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Via ClassicExplorer32.dll | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Via comctl32.dll | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Using Coregen.exe | T1055, T1218 | #1, #7 | ambiguous |
| System Control Panel Item Loaded From Uncommon Location | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Of DBGCORE.DLL | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Of DBGHELP.DLL | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Of DbgModel.DLL | T1574 | #1, #7 | ambiguous |
| Potential EACore.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential Edputil.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential System DLL Sideloading From Non System Locations | T1574 | #1, #7 | ambiguous |
| Potential Goopdate.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Of Libcurl.DLL Via GUP.EXE | T1574 | #1, #7 | ambiguous |
| Potential Iviewers.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential JLI.dll Side-Loading | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Via JsSchHlp | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Of KeyScramblerIE.DLL Via KeyScrambler.EXE | T1574 | #1, #7 | ambiguous |
| Potential Libvlc.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential Mfdetours.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Unsigned Mfdetours.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Of MpSvc.DLL | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Of MsCorSvc.DLL | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Of Non-Existent DLLs From System Folders | T1574 | #1, #7 | ambiguous |
| Microsoft Office DLL Sideload | T1574 | #1, #7 | ambiguous |
| Potential Python DLL SideLoading | T1574 | #1, #7 | ambiguous |
| Potential Rcdll.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential RjvPlatform.DLL Sideloading From Default Location | T1574 | #1, #7 | ambiguous |
| Potential RjvPlatform.DLL Sideloading From Non-Default Location | T1574 | #1, #7 | ambiguous |
| Potential RoboForm.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| DLL Sideloading Of ShellChromeAPI.DLL | T1574 | #1, #7 | ambiguous |
| Potential ShellDispatch.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential SmadHook.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential SolidPDFCreator.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Third Party Software DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Fax Service DLL Search Order Hijack | T1574 | #1, #7 | ambiguous |
| Potential Vcruntime140 DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential Vivaldi_elf.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| VMGuestLib DLL Sideload | T1574 | #1, #7 | ambiguous |
| VMMap Signed Dbghelp.DLL Potential Sideloading | T1574 | #1, #7 | ambiguous |
| VMMap Unsigned Dbghelp.DLL Potential Sideloading | T1574 | #1, #7 | ambiguous |
| Potential DLL Sideloading Via VMware Xfer | T1574 | #1, #7 | ambiguous |
| Potential Waveedit.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential Wazuh Security Platform DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential Mpclient.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| Potential WWlib.DLL Sideloading | T1574 | #1, #7 | ambiguous |
| BaaUpdate.exe Suspicious DLL Load | T1021, T1218 | #1, #4, #7 | ambiguous |
| Unsigned Module Loaded by ClickOnce Application | T1574 | #1, #7 | ambiguous |
| DLL Load By System Process From Suspicious Locations | T1070 | #1 | ok |
| Python Image Load By Non-Python Process | T1027 | #1, #7 | ambiguous |
| DotNet CLR DLL Loaded By Scripting Applications | T1055 | #1, #7 | ambiguous |
| Unsigned DLL Loaded by Windows Utility | T1218 | #1, #7 | ambiguous |
| Suspicious Unsigned Thor Scanner Execution | T1574 | #1, #7 | ambiguous |
| UAC Bypass Using Iscsicpl - ImageLoad | T1548 | #1, #7 | ambiguous |
| UAC Bypass With Fake DLL | T1548, T1574 | #1, #7 | ambiguous |
| MMC Loading Script Engines DLLs | T1059, T1218 | #1, #7 | ambiguous |
| Suspicious Loading of Dbgcore/Dbghelp DLLs from Uncommon Location | T1003, T1685 | #1, #7 | ambiguous |
| Trusted Path Bypass via Windows Directory Spoofing | T1548, T1574 | #1, #7 | ambiguous |
| WMI Persistence - Command Line Event Consumer | T1546 | #1, #7 | ambiguous |
| WMIC Loading Scripting Libraries | T1220 | #1, #7 | ambiguous |
| Wmiprvse Wbemcomn DLL Hijack | T1021, T1047 | #1, #4, #7 | ambiguous |
| Suspicious WSMAN Provider Image Loads | T1021, T1059 | #1, #4, #7 | ambiguous |
| Network Connection Initiated By AddinUtil.EXE | T1218 | #1, #7 | ambiguous |
| Uncommon Connection to Active Directory Web Services | T1087 | #1 | ok |
| Uncommon Network Connection Initiated By Certutil.EXE | T1105 | #1 | ok |
| Outbound Network Connection Initiated By Cmstp.EXE | T1218 | #1, #7 | ambiguous |
| Network Connection Initiated To AzureWebsites.NET By Non-Browser Process | T1102 | #1 | ok |
| Network Connection Initiated To BTunnels Domains | T1567, T1572 | #1, #7 | ambiguous |
| Network Connection Initiated To Cloudflared Tunnels Domains | T1567, T1572 | #1, #7 | ambiguous |
| Network Communication With Crypto Mining Pool | T1496 | #1, #7 | ambiguous |
| New Connection Initiated To Potential Dead Drop Resolver Domain | T1102 | #1 | ok |
| Network Connection Initiated To DevTunnels Domain | T1567, T1572 | #1, #7 | ambiguous |
| Suspicious Dropbox API Usage | T1105, T1567 | #1, #7 | ambiguous |
| Suspicious Network Connection to IP Lookup Service APIs | T1016 | #1 | ok |
| Suspicious Non-Browser Network Communication With Google API | T1102 | #1 | ok |
| Communication To LocaltoNet Tunneling Service Initiated | T1090, T1102, T1572 | #1, #7 | ambiguous |
| Network Connection Initiated To Mega.nz | T1567 | #1, #7 | ambiguous |
| Process Initiated Network Connection To Ngrok Domain | T1102, T1567, T1572 | #1, #7 | ambiguous |
| Communication To Ngrok Tunneling Service Initiated | T1090, T1102, T1567, T1568, T1572 | #1, #7 | ambiguous |
| Potentially Suspicious Network Connection To Notion API | T1102 | #1 | ok |
| Network Communication Initiated To Portmap.IO Domain | T1041, T1090 | #1, #7 | ambiguous |
| Suspicious Non-Browser Network Communication With Telegram API | T1102, T1105, T1567 | #1, #7 | ambiguous |
| Network Connection Initiated To Visual Studio Code Tunnels Domain | T1567, T1572 | #1, #7 | ambiguous |
| Network Connection Initiated via Finger.EXE | T1059, T1071 | #1, #7 | ambiguous |
| Network Connection Initiated By IMEWDBLD.EXE | T1105 | #1 | ok |
| Network Connection Initiated Via Notepad.EXE | T1055 | #1, #7 | ambiguous |
| Python Initiated Connection | T1046 | #1 | ok |
| Outbound RDP Connections Over Non-Standard Tools | T1021 | #1, #4 | ambiguous |
| RDP Over Reverse SSH Tunnel | T1021, T1572 | #1, #4, #7 | ambiguous |
| RDP to HTTP or HTTPS Target Ports | T1021, T1572 | #1, #4, #7 | ambiguous |
| RegAsm.EXE Initiating Network Connection To Public IP | T1218 | #1, #7 | ambiguous |
| Network Connection Initiated By Regsvr32.EXE | T1218, T1559 | #1, #7 | ambiguous |
| Remote Access Tool - AnyDesk Incoming Connection | T1219 | #1, #7 | ambiguous |
| Rundll32 Internet Connection | T1218 | #1, #7 | ambiguous |
| Silenttrinity Stager Msbuild Activity | T1127 | #1, #7 | ambiguous |
| Network Communication Initiated To File Sharing Domains From Process Located In Suspicious Folder | T1105 | #1 | ok |
| Network Connection Initiated From Process Located In Potentially Suspicious Or Uncommon Location | T1105 | #1 | ok |
| Potentially Suspicious Malware Callback Communication | T1571 | #1, #7 | ambiguous |
| Communication To Uncommon Destination Ports | T1571 | #1, #7 | ambiguous |
| Uncommon Outbound Kerberos Connection | T1550, T1558 | #1, #4 | ambiguous |
| Microsoft Sync Center Suspicious Network Connections | T1055, T1218 | #1, #7 | ambiguous |
| Suspicious Outbound SMTP Connections | T1048 | #1, #7 | ambiguous |
| Potential Remote PowerShell Session Initiated | T1021, T1059 | #1, #4, #7 | ambiguous |
| Outbound Network Connection To Public IP Via Winlogon | T1218 | #1, #7 | ambiguous |
| Local Network Connection Initiated By Script Interpreter | T1105 | #1 | ok |
| Outbound Network Connection Initiated By Script Interpreter | T1105 | #1 | ok |
| Potentially Suspicious Wuauclt Network Connection | T1218 | #1, #7 | ambiguous |
| ADFS Database Named Pipe Connection By Uncommon Tool | T1005 | #1 | ok |
| CobaltStrike Named Pipe | T1055 | #1, #7 | ambiguous |
| CobaltStrike Named Pipe Pattern Regex | T1055 | #1, #7 | ambiguous |
| CobaltStrike Named Pipe Patterns | T1055 | #1, #7 | ambiguous |
| HackTool - CoercedPotato Named Pipe Creation | T1055 | #1, #7 | ambiguous |
| HackTool - EfsPotato Named Pipe Creation | T1055 | #1, #7 | ambiguous |
| HackTool - Credential Dumping Tools Named Pipe Created | T1003 | #1, #7 | ambiguous |
| HackTool - Koh Default Named Pipe | T1134, T1528 | #1, #4, #9 | ambiguous |
| Alternate PowerShell Hosts Pipe | T1059 | #1, #7 | ambiguous |
| New PowerShell Instance Created | T1059 | #1, #7 | ambiguous |
| PUA - CSExec Default Named Pipe | T1021, T1569 | #1, #4, #7 | ambiguous |
| PUA - PAExec Default Named Pipe | T1569 | #1, #7 | ambiguous |
| PUA - RemCom Default Named Pipe | T1021, T1569 | #1, #4, #7 | ambiguous |
| WMI Event Consumer Created Named Pipe | T1047 | #1, #7 | ambiguous |
| Malicious Named Pipe Created | T1055 | #1, #7 | ambiguous |
| PsExec Tool Execution From Suspicious Locations - PipeName | T1569 | #1, #7 | ambiguous |
| Nslookup PowerShell Download Cradle | T1059 | #1, #7 | ambiguous |
| Delete Volume Shadow Copies Via WMI With PowerShell | T1490 | #1 | ok |
| PowerShell Downgrade Attack - PowerShell | T1059 | #1, #7 | ambiguous |
| PowerShell Download Via Net.WebClient - PowerShell Classic | T1059, T1105 | #1, #7 | ambiguous |
| PowerShell Called from an Executable Version Mismatch | T1059 | #1, #7 | ambiguous |
| Netcat The Powershell Version | T1059, T1095 | #1, #7 | ambiguous |
| Remote PowerShell Session (PS Classic) | T1021, T1059 | #1, #4, #7 | ambiguous |
| Potential RemoteFXvGPUDisablement.EXE Abuse | T1218 | #1, #7 | ambiguous |
| Renamed Powershell Under Powershell Channel | T1036, T1059 | #1, #7 | ambiguous |
| Use Get-NetTCPConnection | T1049 | #1 | ok |
| Zip A Folder With PowerShell For Staging In Temp - PowerShell | T1074 | #1 | ok |
| Suspicious Non PowerShell WSMAN COM Provider | T1021, T1059 | #1, #4, #7 | ambiguous |
| Alternate PowerShell Hosts - PowerShell Module | T1059 | #1, #7 | ambiguous |
| Bad Opsec Powershell Code Artifacts | T1059 | #1, #7 | ambiguous |
| Clear PowerShell History - PowerShell Module | T1070 | #1 | ok |
| Malicious PowerShell Scripts - PoshModule | T1059 | #1, #7 | ambiguous |
| Suspicious Get-ADDBAccount Usage | T1003 | #1, #7 | ambiguous |
| PowerShell Get Clipboard | T1115 | #1 | ok |
| Invoke-Obfuscation CLIP+ Launcher - PowerShell Module | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Obfuscated IEX Invocation - PowerShell Module | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation STDIN+ Launcher - PowerShell Module | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation VAR+ Launcher - PowerShell Module | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation COMPRESS OBFUSCATION - PowerShell Module | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation RUNDLL LAUNCHER - PowerShell Module | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Stdin - PowerShell Module | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use Clip - PowerShell Module | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use MSHTA - PowerShell Module | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use Rundll32 - PowerShell Module | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation VAR++ LAUNCHER OBFUSCATION - PowerShell Module | T1027, T1059 | #1, #7 | ambiguous |
| Malicious PowerShell Commandlets - PoshModule | T1059, T1069, T1087, T1482 | #1, #7 | ambiguous |
| Remote PowerShell Session (PS Module) | T1021, T1059 | #1, #4, #7 | ambiguous |
| Potential RemoteFXvGPUDisablement.EXE Abuse - PowerShell Module | T1218 | #1, #7 | ambiguous |
| AD Groups Or Users Enumeration Using PowerShell - PoshModule | T1069 | #1 | ok |
| Suspicious PowerShell Download - PoshModule | T1059 | #1, #7 | ambiguous |
| Use Get-NetTCPConnection - PowerShell Module | T1049 | #1 | ok |
| Suspicious PowerShell Invocations - Generic - PowerShell Module | T1059 | #1, #7 | ambiguous |
| Suspicious PowerShell Invocations - Specific - PowerShell Module | T1059 | #1, #7 | ambiguous |
| Suspicious Get Local Groups Information | T1069 | #1 | ok |
| Suspicious Get Information for SMB Share - PowerShell Module | T1069 | #1 | ok |
| Zip A Folder With PowerShell For Staging In Temp  - PowerShell Module | T1074 | #1 | ok |
| SyncAppvPublishingServer Bypass Powershell Restriction - PS Module | T1218 | #1, #7 | ambiguous |
| Access to Browser Login Data | T1555 | #1, #4, #7 | ambiguous |
| Powershell Add Name Resolution Policy Table Rule | T1565 | #1 | ok |
| PowerShell ADRecon Execution | T1059 | #1, #7 | ambiguous |
| Silence.EDA Detection | T1059, T1071, T1529, T1572 | #1, #7 | ambiguous |
| Get-ADUser Enumeration Using UserAccountControl Flags | T1033 | #1 | ok |
| Automated Collection Command PowerShell | T1119 | #1 | ok |
| Windows Screen Capture with CopyFromScreen | T1113 | #1 | ok |
| Clear PowerShell History - PowerShell | T1070 | #1 | ok |
| Clearing Windows Console History | T1070 | #1 | ok |
| Powershell Create Scheduled Task | T1053 | #1, #7 | ambiguous |
| Computer Discovery And Export Via Get-ADComputer Cmdlet - PowerShell | T1033 | #1 | ok |
| Powershell Install a DLL in System Directory | T1556 | #1, #7 | ambiguous |
| Registry-Free Process Scope COR_PROFILER | T1574 | #1, #7 | ambiguous |
| PowerShell Create Local User | T1059, T1136 | #1, #7 | ambiguous |
| DMSA Service Account Created in Specific OUs - PowerShell | T1078, T1098 | #1, #4 | ambiguous |
| Create Volume Shadow Copy with Powershell | T1003 | #1, #7 | ambiguous |
| DirectorySearcher Powershell Exploitation | T1018 | #1 | ok |
| Manipulation of User Computer or Group Security Principals Across AD | T1136 | #1 | ok |
| Disable Powershell Command History | T1070 | #1 | ok |
| Potential In-Memory Execution Using Reflection.Assembly | T1620 | #1, #7 | ambiguous |
| Potential COM Objects Download Cradles Usage - PS Script | T1105 | #1 | ok |
| DSInternals Suspicious PowerShell Cmdlets - ScriptBlock | T1059 | #1, #7 | ambiguous |
| Dump Credentials from Windows Credential Manager With PowerShell | T1555 | #1, #4, #7 | ambiguous |
| Enable Windows Remote Management | T1021 | #1, #4 | ambiguous |
| Enumerate Credentials from Windows Credential Manager With PowerShell | T1555 | #1, #4, #7 | ambiguous |
| Disable of ETW Trace - Powershell | T1070, T1685 | #1 | ambiguous |
| Certificate Exported Via PowerShell - ScriptBlock | T1552 | #1, #4 | ambiguous |
| Suspicious FromBase64String Usage On Gzip Archive - Ps Script | T1132 | #1, #7 | ambiguous |
| Service Registry Permissions Weakness Check | T1574 | #1, #7 | ambiguous |
| Active Directory Computers Enumeration With Get-AdComputer | T1018, T1087 | #1 | ok |
| Active Directory Group Enumeration With Get-AdGroup | T1069 | #1 | ok |
| Suspicious Get-ADReplAccount | T1003 | #1, #7 | ambiguous |
| Automated Collection Bookmarks Using Get-ChildItem PowerShell | T1217 | #1 | ok |
| Security Software Discovery Via Powershell Script | T1518 | #1 | ok |
| HackTool - Rubeus Execution - ScriptBlock | T1003, T1550, T1558 | #1, #4, #7 | ambiguous |
| HackTool - WinPwn Execution - ScriptBlock | T1046, T1082, T1106, T1518, T1548, T1552, T1555 | #1, #4, #7 | ambiguous |
| PowerShell ICMP Exfiltration | T1048 | #1, #7 | ambiguous |
| Import PowerShell Modules From Suspicious Directories | T1059 | #1, #7 | ambiguous |
| Execute Invoke-command on Remote Host | T1021 | #1, #4 | ambiguous |
| Powershell DNSExfiltration | T1048 | #1, #7 | ambiguous |
| Invoke-Obfuscation CLIP+ Launcher - PowerShell | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Obfuscated IEX Invocation - PowerShell | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation STDIN+ Launcher - Powershell | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation VAR+ Launcher - PowerShell | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation COMPRESS OBFUSCATION - PowerShell | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation RUNDLL LAUNCHER - PowerShell | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Stdin - Powershell | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use Clip - Powershell | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use MSHTA - PowerShell | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use Rundll32 - PowerShell | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation VAR++ LAUNCHER OBFUSCATION - PowerShell | T1027, T1059 | #1, #7 | ambiguous |
| Powershell Keylogging | T1056 | #1, #7 | ambiguous |
| Powershell LocalAccount Manipulation | T1098 | #1 | ok |
| Malicious PowerShell Commandlets - ScriptBlock | T1059, T1069, T1087, T1482 | #1, #7 | ambiguous |
| Malicious PowerShell Keywords | T1059 | #1, #7 | ambiguous |
| Live Memory Dump Using Powershell | T1003 | #1, #7 | ambiguous |
| DMSA Link Attributes Modified | T1078, T1098 | #1, #4 | ambiguous |
| Modify Group Policy Settings - ScriptBlockLogging | T1484 | #1 | ok |
| Powershell MsXml COM Object | T1059 | #1, #7 | ambiguous |
| Malicious Nishang PowerShell Commandlets | T1059 | #1, #7 | ambiguous |
| NTFS Alternate Data Stream | T1059, T1564 | #1, #7 | ambiguous |
| Code Executed Via Office Add-in XLL File | T1137 | #1, #7 | ambiguous |
| Potential Packet Capture Activity Via Start-NetEventSession - ScriptBlock | T1040 | #1, #5 | ambiguous |
| Potential Invoke-Mimikatz PowerShell Script | T1003 | #1, #7 | ambiguous |
| Potential Unconstrained Delegation Discovery Via Get-ADComputer - ScriptBlock | T1018, T1558, T1589 | #1, #4 | ambiguous |
| PowerShell Web Access Installation - PsScript | T1059 | #1, #7 | ambiguous |
| PowerView PowerShell Cmdlets - ScriptBlock | T1059 | #1, #7 | ambiguous |
| PowerShell Credential Prompt | T1059 | #1, #7 | ambiguous |
| PSAsyncShell - Asynchronous TCP Reverse Shell | T1059 | #1, #7 | ambiguous |
| PowerShell PSAttack | T1059 | #1, #7 | ambiguous |
| PowerShell Remote Session Creation | T1059 | #1, #7 | ambiguous |
| Potential RemoteFXvGPUDisablement.EXE Abuse - PowerShell ScriptBlock | T1218 | #1, #7 | ambiguous |
| Suspicious Kerberos Ticket Request via PowerShell Script - ScriptBlock | T1558 | #1, #4 | ambiguous |
| PowerShell Script With File Hostname Resolving Capabilities | T1020 | #1 | ok |
| Root Certificate Installed - PowerShell | T1553 | #1, #10 | ambiguous |
| Suspicious Invoke-Item From Mount-DiskImage | T1553 | #1, #10 | ambiguous |
| PowerShell Script With File Upload Capabilities | T1020 | #1 | ok |
| Powershell Sensitive File Discovery | T1083 | #1 | ok |
| PowerShell Script Change Permission Via Set-Acl - PsScript | T1222 | #1 | ok |
| PowerShell Set-Acl On Windows Folder - PsScript | T1222 | #1 | ok |
| Change PowerShell Policies to an Insecure Level - PowerShell | T1059 | #1, #7 | ambiguous |
| PowerShell ShellCode | T1055, T1059 | #1, #7 | ambiguous |
| Malicious ShellIntel PowerShell Commandlets | T1059 | #1, #7 | ambiguous |
| Detected Windows Software Discovery - PowerShell | T1518 | #1 | ok |
| Powershell Store File In Alternate Data Stream | T1564 | #1 | ok |
| AD Groups Or Users Enumeration Using PowerShell - ScriptBlock | T1069 | #1 | ok |
| Potential PowerShell Obfuscation Using Character Join | T1027, T1059 | #1, #7 | ambiguous |
| Powershell Directory Enumeration | T1083 | #1 | ok |
| Suspicious PowerShell Download - Powershell Script | T1059 | #1, #7 | ambiguous |
| Powershell Execute Batch Script | T1059 | #1, #7 | ambiguous |
| Extracting Information with PowerShell | T1552 | #1, #4 | ambiguous |
| Troubleshooting Pack Cmdlet Execution | T1202 | #1 | ok |
| Password Policy Discovery With Get-AdDefaultDomainPasswordPolicy | T1201 | #1 | ok |
| Suspicious PowerShell Get Current User | T1033 | #1 | ok |
| Suspicious GPO Discovery With Get-GPO | T1615 | #1 | ok |
| Suspicious Process Discovery With Get-Process | T1057 | #1 | ok |
| PowerShell Get-Process LSASS in ScriptBlock | T1003 | #1, #7 | ambiguous |
| Suspicious GetTypeFromCLSID ShellExecute | T1546 | #1, #7 | ambiguous |
| Suspicious Hyper-V Cmdlets | T1564 | #1 | ok |
| Suspicious PowerShell Invocations - Generic | T1059 | #1, #7 | ambiguous |
| Suspicious PowerShell Invocations - Specific | T1059 | #1, #7 | ambiguous |
| Suspicious IO.FileStream | T1070 | #1 | ok |
| Potential Keylogger Activity | T1056 | #1, #7 | ambiguous |
| Potential Suspicious PowerShell Keywords | T1059 | #1, #7 | ambiguous |
| Suspicious Get Local Groups Information - PowerShell | T1069 | #1 | ok |
| Powershell Local Email Collection | T1114 | #1, #4 | ambiguous |
| Suspicious Mount-DiskImage | T1553 | #1, #10 | ambiguous |
| PowerShell Deleted Mounted Share | T1070 | #1 | ok |
| Suspicious New-PSDrive to Admin Share | T1021 | #1, #4 | ambiguous |
| Suspicious TCP Tunnel Via PowerShell Script | T1090 | #1, #7 | ambiguous |
| Recon Information for Export with PowerShell | T1119 | #1 | ok |
| Remove Account From Domain Admin Group | T1531 | #1, #7 | ambiguous |
| Suspicious Service DACL Modification Via Set-Service Cmdlet - PS | T1574 | #1, #7 | ambiguous |
| Potential PowerShell Obfuscation Using Alias Cmdlets | T1027, T1059 | #1, #7 | ambiguous |
| Suspicious Get Information for SMB Share | T1069 | #1 | ok |
| Suspicious SSL Connection | T1573 | #1, #7 | ambiguous |
| Suspicious Start-Process PassThru | T1036 | #1, #7 | ambiguous |
| Suspicious Unblock-File | T1553 | #1, #10 | ambiguous |
| Powershell Suspicious Win32_PnPEntity | T1120 | #1 | ok |
| Deletion of Volume Shadow Copies via WMI with PowerShell - PS Script | T1490 | #1 | ok |
| Suspicious PowerShell WindowStyle Option | T1564 | #1 | ok |
| Zip A Folder With PowerShell For Staging In Temp - PowerShell Script | T1074 | #1 | ok |
| SyncAppvPublishingServer Execution to Bypass Powershell Restriction | T1218 | #1, #7 | ambiguous |
| Testing Usage of Uncommonly Used Port | T1571 | #1, #7 | ambiguous |
| Powershell Timestomp | T1070 | #1 | ok |
| User Discovery And Export Via Get-ADUser Cmdlet - PowerShell | T1033 | #1 | ok |
| Potential Persistence Via PowerShell User Profile Using Add-Content | T1546 | #1, #7 | ambiguous |
| Abuse of Service Permissions to Hide Services Via Set-Service - PS | T1574 | #1, #7 | ambiguous |
| Registry Modification Attempt Via VBScript - PowerShell | T1059, T1112 | #1, #7 | ambiguous |
| Usage Of Web Request Commands And Cmdlets - ScriptBlock | T1059 | #1, #7 | ambiguous |
| PowerShell WMI Win32_Product Install MSI | T1218 | #1, #7 | ambiguous |
| Potential WinAPI Calls Via PowerShell Scripts | T1059, T1106 | #1, #7 | ambiguous |
| Windows Defender Exclusions Added - PowerShell | T1059, T1685 | #1, #7 | ambiguous |
| Winlogon Helper DLL | T1547 | #1, #7 | ambiguous |
| Powershell WMI Persistence | T1546 | #1, #7 | ambiguous |
| WMIC Unquoted Services Path Lookup - PowerShell | T1047 | #1, #7 | ambiguous |
| WMImplant Hack Tool | T1047, T1059 | #1, #7 | ambiguous |
| Suspicious X509Enrollment - Ps Script | T1553 | #1, #10 | ambiguous |
| Powershell XML Execute Command | T1059 | #1, #7 | ambiguous |
| CMSTP Execution Process Access | T1218, T1559 | #1, #7 | ambiguous |
| HackTool - CobaltStrike BOF Injection Pattern | T1106, T1685 | #1, #7 | ambiguous |
| HackTool - Generic Process Access | T1003 | #1, #7 | ambiguous |
| HackTool - HandleKatz Duplicating LSASS Handle | T1003, T1106 | #1, #7 | ambiguous |
| HackTool - LittleCorporal Generated Maldoc Injection | T1055, T1204 | #1, #7, #9 | ambiguous |
| Lsass Memory Dump via Comsvcs DLL | T1003 | #1, #7 | ambiguous |
| LSASS Memory Access by Tool With Dump Keyword In Name | T1003 | #1, #7 | ambiguous |
| Potential Credential Dumping Activity Via LSASS | T1003 | #1, #7 | ambiguous |
| Credential Dumping Activity By Python Based Tool | T1003 | #1, #7 | ambiguous |
| Remote LSASS Process Access Through Windows Remote Management | T1003, T1021, T1059 | #1, #4, #7 | ambiguous |
| Suspicious LSASS Access Via MalSecLogon | T1003 | #1, #7 | ambiguous |
| Potentially Suspicious GrantedAccess Flags On LSASS | T1003 | #1, #7 | ambiguous |
| Credential Dumping Attempt Via WerFault | T1003 | #1, #7 | ambiguous |
| LSASS Access From Potentially White-Listed Processes | T1003 | #1, #7 | ambiguous |
| Uncommon Process Access Rights For Target Image | T1055 | #1, #7 | ambiguous |
| Suspicious Process Access to LSASS with Dbgcore/Dbghelp DLLs | T1003, T1685 | #1, #7 | ambiguous |
| Potential Direct Syscall of NtOpenProcess | T1106 | #1, #7 | ambiguous |
| Credential Dumping Attempt Via Svchost | T1548 | #1, #7 | ambiguous |
| Function Call From Undocumented COM Interface EditionUpgradeManager | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using WOW64 Logger DLL Hijack | T1548 | #1, #7 | ambiguous |
| 7Zip Compressing Dump Files | T1560 | #1 | ok |
| Compress Data and Lock With Password for Exfiltration With 7-ZIP | T1560 | #1 | ok |
| Suspicious AddinUtil.EXE CommandLine Execution | T1218 | #1, #7 | ambiguous |
| Uncommon Child Process Of AddinUtil.EXE | T1218 | #1, #7 | ambiguous |
| Uncommon AddinUtil.EXE CommandLine Execution | T1218 | #1, #7 | ambiguous |
| AddinUtil.EXE Execution From Uncommon Directory | T1218 | #1, #7 | ambiguous |
| Potential Adplus.EXE Abuse | T1003 | #1, #7 | ambiguous |
| AgentExecutor PowerShell Execution | T1218 | #1, #7 | ambiguous |
| Suspicious AgentExecutor PowerShell Execution | T1218 | #1, #7 | ambiguous |
| Uncommon Child Process Of Appvlp.EXE | T1218 | #1, #7 | ambiguous |
| Suspicious ArcSOC.exe Child Process | T1059, T1203 | #1, #3, #7 | ambiguous |
| AspNetCompiler Execution | T1127 | #1, #7 | ambiguous |
| Suspicious Child Process of AspNetCompiler | T1127 | #1, #7 | ambiguous |
| Potentially Suspicious ASP.NET Compilation Via AspNetCompiler | T1127 | #1, #7 | ambiguous |
| Interactive AT Job | T1053 | #1, #7 | ambiguous |
| Uncommon  Assistive Technology Applications Execution Via AtBroker.EXE | T1218 | #1, #7 | ambiguous |
| Hiding Files with Attrib.exe | T1564 | #1 | ok |
| Set Suspicious Files as System Files Using Attrib.EXE | T1564 | #1 | ok |
| Suspicious Autorun Registry Modified via WMI | T1047, T1547 | #1, #7 | ambiguous |
| Suspicious BitLocker Access Agent Update Utility Execution | T1021, T1218 | #1, #4, #7 | ambiguous |
| Indirect Inline Command Execution Via Bash.EXE | T1202 | #1 | ok |
| Indirect Command Execution From Script File Via Bash.EXE | T1202 | #1 | ok |
| Boot Configuration Tampering Via Bcdedit.EXE | T1490 | #1 | ok |
| Potential Ransomware or Unauthorized MBR Tampering Via Bcdedit.EXE | T1070, T1542 | #1, #7 | ambiguous |
| Data Export From MSSQL Table Via BCP.EXE | T1048 | #1, #7 | ambiguous |
| Suspicious Child Process Of BgInfo.EXE | T1059, T1202, T1218 | #1, #7 | ambiguous |
| Uncommon Child Process Of BgInfo.EXE | T1059, T1202, T1218 | #1, #7 | ambiguous |
| BitLockerTogo.EXE Execution | T1218 | #1, #7 | ambiguous |
| File Download Via Bitsadmin | T1036, T1105, T1197 | #1, #7 | ambiguous |
| Suspicious Download From Direct IP Via Bitsadmin | T1036, T1197 | #1, #7 | ambiguous |
| Suspicious Download From File-Sharing Website Via Bitsadmin | T1036, T1105, T1197 | #1, #7 | ambiguous |
| File With Suspicious Extension Downloaded Via Bitsadmin | T1036, T1105, T1197 | #1, #7 | ambiguous |
| File Download Via Bitsadmin To A Suspicious Target Folder | T1036, T1105, T1197 | #1, #7 | ambiguous |
| Monitoring For Persistence Via BITS | T1197 | #1, #7 | ambiguous |
| Potential Data Stealing Via Chromium Headless Debugging | T1185, T1564 | #1, #4 | ambiguous |
| Browser Execution In Headless Mode | T1105, T1564 | #1 | ok |
| File Download with Headless Browser | T1105, T1564 | #1 | ok |
| Chromium Browser Instance Executed With Custom Extension | T1176 | #1, #7 | ambiguous |
| Suspicious Chromium Browser Instance Executed With Custom Extension | T1176 | #1, #7 | ambiguous |
| File Download From Browser Process Via Inline URL | T1105 | #1 | ok |
| Browser Started with Remote Debugging | T1185 | #1, #4 | ambiguous |
| Tor Client/Browser Execution | T1090 | #1, #7 | ambiguous |
| Suspicious Calculator Usage | T1036 | #1, #7 | ambiguous |
| Potential Binary Proxy Execution Via Cdb.EXE | T1106, T1127, T1218 | #1, #7 | ambiguous |
| New Root Certificate Installed Via CertMgr.EXE | T1553 | #1, #10 | ambiguous |
| File Download via CertOC.EXE | T1105 | #1 | ok |
| File Download From IP Based URL Via CertOC.EXE | T1105 | #1 | ok |
| DLL Loaded via CertOC.EXE | T1218 | #1, #7 | ambiguous |
| Suspicious DLL Loaded via CertOC.EXE | T1218 | #1, #7 | ambiguous |
| Suspicious CertReq Command to Download | T1105 | #1 | ok |
| New Root Certificate Installed Via Certutil.EXE | T1553 | #1, #10 | ambiguous |
| File Decoded From Base64/Hex Via Certutil.EXE | T1027 | #1, #7 | ambiguous |
| Suspicious Download Via Certutil.EXE | T1027, T1105 | #1, #7 | ambiguous |
| Suspicious File Downloaded From Direct IP Via Certutil.EXE | T1027, T1105 | #1, #7 | ambiguous |
| Suspicious File Downloaded From File-Sharing Website Via Certutil.EXE | T1027, T1105 | #1, #7 | ambiguous |
| File Encoded To Base64 Via Certutil.EXE | T1027 | #1, #7 | ambiguous |
| Suspicious File Encoded To Base64 Via Certutil.EXE | T1027 | #1, #7 | ambiguous |
| File In Suspicious Location Encoded To Base64 Via Certutil.EXE | T1027 | #1, #7 | ambiguous |
| Certificate Exported Via Certutil.EXE | T1027 | #1, #7 | ambiguous |
| Potential NTLM Coercion Via Certutil.EXE | T1218 | #1, #7 | ambiguous |
| Console CodePage Lookup Via CHCP | T1614 | #1 | ok |
| Suspicious CodePage Switch Via CHCP | T1036 | #1, #7 | ambiguous |
| Process Access via TrolleyExpress Exclusion | T1003, T1218 | #1, #7 | ambiguous |
| Data Copied To Clipboard Via Clip.EXE | T1115 | #1 | ok |
| Cloudflared Portable Execution | T1090 | #1, #7 | ambiguous |
| Cloudflared Quick Tunnel Execution | T1090 | #1, #7 | ambiguous |
| Cloudflared Tunnel Connections Cleanup | T1090, T1102, T1572 | #1, #7 | ambiguous |
| Cloudflared Tunnel Execution | T1090, T1102, T1572 | #1, #7 | ambiguous |
| Change Default File Association Via Assoc | T1546 | #1, #7 | ambiguous |
| Change Default File Association To Executable Via Assoc | T1546 | #1, #7 | ambiguous |
| Curl Download And Execute Combination | T1105, T1218 | #1, #7 | ambiguous |
| File Deletion Via Del | T1070 | #1 | ok |
| Greedy File Deletion Using Del | T1070 | #1 | ok |
| File And SubFolder Enumeration Via Dir Command | T1217 | #1 | ok |
| Potential Dosfuscation Activity | T1059 | #1, #7 | ambiguous |
| Command Line Execution with Suspicious URL and AppData Strings | T1059, T1105 | #1, #7 | ambiguous |
| Cmd Launched with Hidden Start Flags to Suspicious Targets | T1564 | #1 | ok |
| Potential Privilege Escalation Using Symlink Between Osk and Cmd | T1546 | #1, #7 | ambiguous |
| VolumeShadowCopy Symlink Creation Via Mklink | T1003 | #1, #7 | ambiguous |
| Suspicious File Execution From Internet Hosted WebDav Share | T1059 | #1, #7 | ambiguous |
| Cmd.EXE Missing Space Characters Execution Anomaly | T1059 | #1, #7 | ambiguous |
| Potential CommandLine Path Traversal Via Cmd.EXE | T1059 | #1, #7 | ambiguous |
| Potentially Suspicious Ping/Copy Command Combination | T1070 | #1 | ok |
| Suspicious Ping/Del Command Combination | T1070 | #1 | ok |
| Potentially Suspicious CMD Shell Output Redirect | T1218 | #1, #7 | ambiguous |
| Directory Removal Via Rmdir | T1070 | #1 | ok |
| Copy From VolumeShadowCopy Via Cmd.EXE | T1490 | #1 | ok |
| Read Contents From Stdin Via Cmd.EXE | T1059 | #1, #7 | ambiguous |
| Sticky Key Like Backdoor Execution | T1546 | #1, #7 | ambiguous |
| Persistence Via Sticky Key Backdoor | T1546 | #1, #7 | ambiguous |
| Potential Download/Upload Activity Using Type Command | T1105 | #1 | ok |
| Unusual Parent Process For Cmd.EXE | T1059 | #1, #7 | ambiguous |
| New Generic Credentials Added Via Cmdkey.EXE | T1003 | #1, #7 | ambiguous |
| Potential Reconnaissance For Cached Credentials Via Cmdkey.EXE | T1003 | #1, #7 | ambiguous |
| Potential Arbitrary File Download Via Cmdl32.EXE | T1202, T1218 | #1, #7 | ambiguous |
| CMSTP Execution Process Creation | T1218 | #1, #7 | ambiguous |
| OpenEDR Spawning Command Shell | T1021, T1059, T1219 | #1, #4, #7 | ambiguous |
| Arbitrary File Download Via ConfigSecurityPolicy.EXE | T1567 | #1, #7 | ambiguous |
| Powershell Executed From Headless ConHost Process | T1059, T1564 | #1, #7 | ambiguous |
| Suspicious High IntegrityLevel Conhost Legacy Option | T1202 | #1 | ok |
| Conhost.exe CommandLine Path Traversal | T1059 | #1, #7 | ambiguous |
| Uncommon Child Process Of Conhost.EXE | T1202 | #1 | ok |
| Potentially Suspicious Child Processes Spawned by ConHost | T1202, T1218 | #1, #7 | ambiguous |
| Conhost Spawned By Uncommon Parent Process | T1059 | #1, #7 | ambiguous |
| Control Panel Items | T1218, T1546 | #1, #7 | ambiguous |
| New DMSA Service Account Created in Specific OUs | T1078, T1098 | #1, #4 | ambiguous |
| CreateDump Process Dump | T1003, T1036 | #1, #7 | ambiguous |
| Dynamic .NET Compilation Via Csc.EXE | T1027 | #1, #7 | ambiguous |
| Csc.EXE Execution Form Potentially Suspicious Parent | T1027, T1059, T1218 | #1, #7 | ambiguous |
| Suspicious Csi.exe Usage | T1072, T1218 | #1, #7 | ambiguous |
| Suspicious Use of CSharp Interactive Console | T1127 | #1, #7 | ambiguous |
| Active Directory Structure Export Via Csvde.EXE | T1087 | #1 | ok |
| Suspicious Curl.EXE Download | T1105 | #1 | ok |
| Suspicious CustomShellHost Execution | T1216 | #1, #7 | ambiguous |
| ManageEngine Endpoint Central Dctask64.EXE Potential Abuse | T1055 | #1, #7 | ambiguous |
| Uncommon Child Process Of Defaultpack.EXE | T1218 | #1, #7 | ambiguous |
| Remote File Download Via Desktopimgdownldr Utility | T1105 | #1 | ok |
| Suspicious Desktopimgdownldr Command | T1105 | #1 | ok |
| Devcon Execution Disabling VMware VMCI Device | T1543, T1685 | #1, #7 | ambiguous |
| DeviceCredentialDeployment Execution | T1218 | #1, #7 | ambiguous |
| Potential DLL Sideloading Via DeviceEnroller.EXE | T1574 | #1, #7 | ambiguous |
| Arbitrary MSI Download Via Devinit.EXE | T1218 | #1, #7 | ambiguous |
| DirLister Execution | T1083 | #1 | ok |
| System Information Discovery via Registry Queries | T1082 | #1 | ok |
| Potentially Suspicious Child Process Of DiskShadow.EXE | T1218 | #1, #7 | ambiguous |
| Diskshadow Script Mode - Uncommon Script Extension Execution | T1218 | #1, #7 | ambiguous |
| Diskshadow Script Mode - Execution From Potential Suspicious Location | T1218 | #1, #7 | ambiguous |
| PowerShell Web Access Feature Enabled Via DISM | T1548 | #1, #7 | ambiguous |
| DLL Sideloading by VMware Xfer Utility | T1574 | #1, #7 | ambiguous |
| Dllhost.EXE Execution Anomaly | T1055 | #1, #7 | ambiguous |
| DNS Exfiltration and Tunneling Tools Execution | T1048, T1071, T1132 | #1, #7 | ambiguous |
| New DNS ServerLevelPluginDll Installed Via Dnscmd.EXE | T1112, T1574 | #1, #7 | ambiguous |
| Potential Application Whitelisting Bypass via Dnx.EXE | T1027, T1218 | #1, #7 | ambiguous |
| Arbitrary DLL or Csproj Code Execution Via Dotnet.EXE | T1218 | #1, #7 | ambiguous |
| Binary Proxy Execution Via Dotnet-Trace.EXE | T1218 | #1, #7 | ambiguous |
| Process Memory Dump Via Dotnet-Dump | T1218 | #1, #7 | ambiguous |
| Potentially Over Permissive Permissions Granted Using Dsacls.EXE | T1218 | #1, #7 | ambiguous |
| Potential Password Spraying Attempt Using Dsacls.EXE | T1218 | #1, #7 | ambiguous |
| Domain Trust Discovery Via Dsquery | T1482 | #1 | ok |
| Suspicious Kernel Dump Using Dtrace | T1082 | #1 | ok |
| Potential Windows Defender AV Bypass Via Dump64.EXE Rename | T1003 | #1, #7 | ambiguous |
| DumpMinitool Execution | T1003, T1036 | #1, #7 | ambiguous |
| Suspicious DumpMinitool Execution | T1003, T1036 | #1, #7 | ambiguous |
| New Capture Session Launched Via DXCap.EXE | T1218 | #1, #7 | ambiguous |
| Esentutl Gather Credentials | T1003 | #1, #7 | ambiguous |
| Copying Sensitive Files with Credential Data | T1003 | #1, #7 | ambiguous |
| Esentutl Steals Browser Information | T1005 | #1 | ok |
| Security Event Logging Disabled via MiniNt Registry Key - Process | T1112, T1685 | #1 | ambiguous |
| Potentially Suspicious Event Viewer Child Process | T1548 | #1, #7 | ambiguous |
| Potentially Suspicious Cabinet File Expansion | T1218 | #1, #7 | ambiguous |
| Explorer Process Tree Break | T1036 | #1, #7 | ambiguous |
| File Explorer Folder Opened Using Explorer Folder Shortcut Via Shell | T1135 | #1 | ok |
| Explorer NOUACCHECK Flag | T1548 | #1, #7 | ambiguous |
| Remote File Download Via Findstr.EXE | T1105, T1218, T1552, T1564 | #1, #4, #7 | ambiguous |
| Findstr GPP Passwords | T1552 | #1, #4 | ambiguous |
| Findstr Launching .lnk File | T1027, T1036, T1202 | #1, #7 | ambiguous |
| LSASS Process Reconnaissance Via Findstr.EXE | T1552 | #1, #4 | ambiguous |
| Permission Misconfiguration Reconnaissance Via Findstr.EXE | T1552 | #1, #4 | ambiguous |
| Recon Command Output Piped To Findstr.EXE | T1057 | #1 | ok |
| Security Tools Keyword Lookup Via Findstr.EXE | T1518 | #1 | ok |
| Insensitive Subfolder Search Via Findstr.EXE | T1105, T1218, T1552, T1564 | #1, #4, #7 | ambiguous |
| Sysmon Discovery Via Default Driver Altitude Using Findstr.EXE | T1518 | #1 | ok |
| Finger.EXE Execution | T1105 | #1 | ok |
| Filter Driver Unloaded Via Fltmc.EXE | T1070, T1685 | #1 | ambiguous |
| Sysmon Driver Unloaded Via Fltmc.EXE | T1070, T1685 | #1 | ambiguous |
| Forfiles.EXE Child Process Masquerading | T1036 | #1, #7 | ambiguous |
| Forfiles Command Execution | T1059 | #1, #7 | ambiguous |
| Use of FSharp Interpreters | T1059 | #1, #7 | ambiguous |
| Fsutil Drive Enumeration | T1120 | #1 | ok |
| Potentially Suspicious NTFS Symlink Behavior Modification | T1059, T1222 | #1, #7 | ambiguous |
| Fsutil Suspicious Invocation | T1070, T1485 | #1, #7 | ambiguous |
| Potential Arbitrary Command Execution Via FTP.EXE | T1059, T1202 | #1, #7 | ambiguous |
| Arbitrary File Download Via GfxDownloadWrapper.EXE | T1105 | #1 | ok |
| Github Self-Hosted Runner Execution | T1071, T1102 | #1, #7 | ambiguous |
| Gpresult Display Group Policy Information | T1615 | #1 | ok |
| File Download Using Notepad++ GUP Utility | T1105 | #1 | ok |
| Suspicious GUP Usage | T1574 | #1, #7 | ambiguous |
| HH.EXE Execution | T1218 | #1, #7 | ambiguous |
| Remote CHM File Download/Execution Via HH.EXE | T1218 | #1, #7 | ambiguous |
| HTML Help HH.EXE Suspicious Child Process | T1047, T1059, T1218, T1566 | #1, #7, #9 | ambiguous |
| Suspicious HH.EXE Execution | T1047, T1059, T1218, T1566 | #1, #7, #9 | ambiguous |
| HackTool - Bloodhound/Sharphound Execution | T1059, T1069, T1087, T1482 | #1, #7 | ambiguous |
| HackTool - F-Secure C3 Load by Rundll32 | T1218 | #1, #7 | ambiguous |
| HackTool - Certify Execution | T1649 | #1, #4 | ambiguous |
| HackTool - Certipy Execution | T1649 | #1, #4 | ambiguous |
| Operator Bloopers Cobalt Strike Commands | T1059 | #1, #7 | ambiguous |
| Operator Bloopers Cobalt Strike Modules | T1059 | #1, #7 | ambiguous |
| CobaltStrike Load by Rundll32 | T1218 | #1, #7 | ambiguous |
| Potential CobaltStrike Process Patterns | T1059 | #1, #7 | ambiguous |
| HackTool - CoercedPotato Execution | T1055 | #1, #7 | ambiguous |
| HackTool - Covenant PowerShell Launcher | T1059, T1564 | #1, #7 | ambiguous |
| HackTool - CrackMapExec Execution | T1047, T1053, T1059, T1110, T1201 | #1, #4, #7 | ambiguous |
| HackTool - CrackMapExec Execution Patterns | T1047, T1053, T1059 | #1, #7 | ambiguous |
| HackTool - CrackMapExec Process Patterns | T1003 | #1, #7 | ambiguous |
| HackTool - CrackMapExec PowerShell Obfuscation | T1027, T1059 | #1, #7 | ambiguous |
| HackTool - CreateMiniDump Execution | T1003 | #1, #7 | ambiguous |
| HackTool - DInjector PowerShell Cradle Execution | T1055 | #1, #7 | ambiguous |
| HackTool - Doppelanger LSASS Dumper Execution | T1003 | #1, #7 | ambiguous |
| HackTool - Dumpert Process Dumper Execution | T1003 | #1, #7 | ambiguous |
| HackTool - Empire PowerShell Launch Parameters | T1059 | #1, #7 | ambiguous |
| HackTool - Empire PowerShell UAC Bypass | T1548 | #1, #7 | ambiguous |
| HackTool - WinRM Access Via Evil-WinRM | T1021 | #1, #4 | ambiguous |
| Hacktool Execution - Imphash | T1003, T1588 | #1, #7 | ambiguous |
| Hacktool Execution - PE Metadata | T1003, T1588 | #1, #7 | ambiguous |
| HackTool - HandleKatz LSASS Dumper Execution | T1003 | #1, #7 | ambiguous |
| HackTool - HollowReaper Execution | T1055 | #1, #7 | ambiguous |
| HackTool - Htran/NATBypass Execution | T1090 | #1, #7 | ambiguous |
| HackTool - Potential Impacket Lateral Movement Activity | T1021, T1047 | #1, #4, #7 | ambiguous |
| HackTool - Impersonate Execution | T1134 | #1, #4 | ambiguous |
| HackTool - Inveigh Execution | T1003 | #1, #7 | ambiguous |
| Invoke-Obfuscation CLIP+ Launcher | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Obfuscated IEX Invocation | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation STDIN+ Launcher | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation VAR+ Launcher | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation COMPRESS OBFUSCATION | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Stdin | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use Clip | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation Via Use MSHTA | T1027, T1059 | #1, #7 | ambiguous |
| Invoke-Obfuscation VAR++ LAUNCHER OBFUSCATION | T1027, T1059 | #1, #7 | ambiguous |
| HackTool - Jlaive In-Memory Assembly Execution | T1059 | #1, #7 | ambiguous |
| HackTool - Koadic Execution | T1059 | #1, #7 | ambiguous |
| HackTool - KrbRelay Execution | T1558 | #1, #4 | ambiguous |
| HackTool - RemoteKrbRelay Execution | T1558 | #1, #4 | ambiguous |
| HackTool - KrbRelayUp Execution | T1550, T1558 | #1, #4 | ambiguous |
| Potential Meterpreter/CobaltStrike Activity | T1134 | #1, #4 | ambiguous |
| HackTool - Mimikatz Execution | T1003 | #1, #7 | ambiguous |
| HackTool - NetExec Execution | T1018, T1021 | #1, #4 | ambiguous |
| HackTool - PCHunter Execution | T1007, T1012, T1057, T1082, T1083 | #1 | ok |
| HackTool - Default PowerSploit/Empire Scheduled Task Creation | T1053, T1059 | #1, #7 | ambiguous |
| HackTool - Pypykatz Credentials Dumping Activity | T1003 | #1, #7 | ambiguous |
| HackTool - Quarks PwDump Execution | T1003 | #1, #7 | ambiguous |
| HackTool - RedMimicry Winnti Playbook Execution | T1059, T1106, T1218 | #1, #7 | ambiguous |
| HackTool - Rubeus Execution | T1003, T1550, T1558 | #1, #4, #7 | ambiguous |
| HackTool - SafetyKatz Execution | T1003 | #1, #7 | ambiguous |
| HackTool - SecurityXploded Execution | T1555 | #1, #4, #7 | ambiguous |
| HackTool - PPID Spoofing SelectMyParent Tool Execution | T1134 | #1, #4 | ambiguous |
| HackTool - SharpChisel Execution | T1090 | #1, #7 | ambiguous |
| HackTool - SharpDPAPI Execution | T1134 | #1, #4 | ambiguous |
| HackTool - SharpImpersonation Execution | T1134 | #1, #4 | ambiguous |
| HackTool - SharPersist Execution | T1053 | #1, #7 | ambiguous |
| HackTool - SharpLdapWhoami Execution | T1033 | #1 | ok |
| HackTool - SharpMove Tool Execution | T1021 | #1, #4 | ambiguous |
| HackTool - SharpUp PrivEsc Tool Execution | T1569, T1574, T1615 | #1, #7 | ambiguous |
| HackTool - SharpView Execution | T1033, T1049, T1069, T1135, T1482 | #1 | ok |
| HackTool - Sliver C2 Implant Activity Pattern | T1059 | #1, #7 | ambiguous |
| HackTool - SOAPHound Execution | T1087 | #1 | ok |
| HackTool - Stracciatella Execution | T1059, T1685 | #1, #7 | ambiguous |
| HackTool - TruffleSnout Execution | T1482 | #1 | ok |
| HackTool - UACMe Akagi Execution | T1548 | #1, #7 | ambiguous |
| HackTool - Windows Credential Editor (WCE) Execution | T1003 | #1, #7 | ambiguous |
| HackTool - winPEAS Execution | T1046, T1082, T1087 | #1 | ok |
| HackTool - WinPwn Execution | T1046, T1082, T1106, T1518, T1548, T1552, T1555 | #1, #4, #7 | ambiguous |
| HackTool - WSASS Execution | T1003 | #1, #7 | ambiguous |
| HackTool - XORDump Execution | T1003, T1036 | #1, #7 | ambiguous |
| Suspicious ZipExec Execution | T1202, T1218 | #1, #7 | ambiguous |
| Suspicious Execution of Hostname | T1082 | #1 | ok |
| Suspicious HWP Sub Processes | T1059, T1203, T1566 | #1, #3, #7, #9 | ambiguous |
| Potential Fake Instance Of Hxtsr.EXE Executed | T1036 | #1, #7 | ambiguous |
| Use Icacls to Hide File to Everyone | T1564 | #1 | ok |
| File Download And Execution Via IEExec.EXE | T1105 | #1 | ok |
| Self Extracting Package Creation Via Iexpress.EXE From Potentially Suspicious Location | T1218 | #1, #7 | ambiguous |
| Microsoft IIS Service Account Password Dumped | T1003 | #1, #7 | ambiguous |
| IIS Native-Code Module Command Line Installation | T1505 | #1, #7 | ambiguous |
| Microsoft IIS Connection Strings Decryption | T1003 | #1, #7 | ambiguous |
| IIS WebServer Log Deletion via CommandLine Utilities | T1070 | #1 | ok |
| Suspicious IIS Module Registration | T1505 | #1, #7 | ambiguous |
| C# IL Code Compilation Via Ilasm.EXE | T1127 | #1, #7 | ambiguous |
| Arbitrary File Download Via IMEWDBLD.EXE | T1218 | #1, #7 | ambiguous |
| InfDefaultInstall.exe .inf Execution | T1218 | #1, #7 | ambiguous |
| File Download Via InstallUtil.EXE | T1218 | #1, #7 | ambiguous |
| Suspicious Child Process Of Manage Engine ServiceDesk | T1102 | #1 | ok |
| JScript Compiler Execution | T1127 | #1, #7 | ambiguous |
| Kavremover Dropped Binary LOLBIN Usage | T1127 | #1, #7 | ambiguous |
| Attempts of Kerberos Coercion Via DNS SPN Spoofing | T1187, T1557 | #1, #4, #5 | ambiguous |
| Potentially Suspicious Child Process of KeyScrambler.exe | T1203, T1574 | #1, #3, #7 | ambiguous |
| Import LDAP Data Interchange Format File Via Ldifde.EXE | T1105, T1218 | #1, #7 | ambiguous |
| Uncommon Link.EXE Parent Process | T1218 | #1, #7 | ambiguous |
| LOLBAS Data Exfiltration by DataSvcUtil.exe | T1567 | #1, #7 | ambiguous |
| Devtoolslauncher.exe Executes Specified Binary | T1218 | #1, #7 | ambiguous |
| Suspicious Diantz Alternate Data Stream Execution | T1564 | #1 | ok |
| Suspicious Diantz Download and Compress Into a CAB File | T1105 | #1 | ok |
| Suspicious Extrac32 Execution | T1105 | #1 | ok |
| Suspicious Extrac32 Alternate Data Stream Execution | T1564 | #1 | ok |
| Potential Reconnaissance Activity Via GatherNetworkInfo.VBS | T1059, T1615 | #1, #7 | ambiguous |
| Gpscript Execution | T1218 | #1, #7 | ambiguous |
| Ie4uinit Lolbin Use From Invalid Path | T1218 | #1, #7 | ambiguous |
| Launch-VsDevShell.PS1 Proxy Execution | T1216 | #1, #7 | ambiguous |
| Potential Manage-bde.wsf Abuse To Proxy Execution | T1216 | #1, #7 | ambiguous |
| Mavinject Inject DLL Into Running Process | T1055, T1218 | #1, #7 | ambiguous |
| MpiExec Lolbin | T1218 | #1, #7 | ambiguous |
| Execute Files with Msdeploy.exe | T1218 | #1, #7 | ambiguous |
| Use of OpenConsole | T1059 | #1, #7 | ambiguous |
| OpenWith.exe Executes Specified Binary | T1218 | #1, #7 | ambiguous |
| Use of Pcalua For Execution | T1059 | #1, #7 | ambiguous |
| Indirect Command Execution By Program Compatibility Wizard | T1218 | #1, #7 | ambiguous |
| Execute Pcwrun.EXE To Leverage Follina | T1218 | #1, #7 | ambiguous |
| Code Execution via Pcwutl.dll | T1218 | #1, #7 | ambiguous |
| Execute Code with Pester.bat as Parent | T1059, T1216 | #1, #7 | ambiguous |
| Execute Code with Pester.bat | T1059, T1216 | #1, #7 | ambiguous |
| PrintBrm ZIP Creation of Extraction | T1105, T1564 | #1 | ok |
| Pubprn.vbs Proxy Execution | T1216 | #1, #7 | ambiguous |
| DLL Execution via Rasautou.exe | T1218 | #1, #7 | ambiguous |
| REGISTER_APP.VBS Proxy Execution | T1218 | #1, #7 | ambiguous |
| Use of Remote.exe | T1127 | #1, #7 | ambiguous |
| Replace.exe Usage | T1105 | #1 | ok |
| Lolbin Runexehelper Use As Proxy | T1218 | #1, #7 | ambiguous |
| Suspicious Runscripthelper.exe | T1059, T1202 | #1, #7 | ambiguous |
| Use of Scriptrunner.exe | T1218 | #1, #7 | ambiguous |
| Using SettingSyncHost.exe as LOLBin | T1574 | #1, #7 | ambiguous |
| Use Of The SFTP.EXE Binary As A LOLBIN | T1218 | #1, #7 | ambiguous |
| Suspicious Driver Install by pnputil.exe | T1547 | #1, #7 | ambiguous |
| Suspicious GrpConv Execution | T1547 | #1, #7 | ambiguous |
| Dumping Process via Sqldumper.exe | T1003 | #1, #7 | ambiguous |
| SyncAppvPublishingServer Execute Arbitrary PowerShell Code | T1218 | #1, #7 | ambiguous |
| SyncAppvPublishingServer VBS Execute Arbitrary PowerShell Code | T1216, T1218 | #1, #7 | ambiguous |
| Potential DLL Injection Or Execution Using Tracker.exe | T1055 | #1, #7 | ambiguous |
| Use of TTDInject.exe | T1127 | #1, #7 | ambiguous |
| Time Travel Debugging Utility Usage | T1003, T1218 | #1, #7 | ambiguous |
| Lolbin Unregmp2.exe Use As Proxy | T1218 | #1, #7 | ambiguous |
| UtilityFunctions.ps1 Proxy Dll | T1216 | #1, #7 | ambiguous |
| Visual Basic Command Line Compiler Usage | T1027 | #1, #7 | ambiguous |
| Use of VisualUiaVerifyNative.exe | T1218 | #1, #7 | ambiguous |
| Use of VSIISExeLauncher.exe | T1127 | #1, #7 | ambiguous |
| Use of Wfc.exe | T1127 | #1, #7 | ambiguous |
| Potential Register_App.Vbs LOLScript Abuse | T1218 | #1, #7 | ambiguous |
| Potential Credential Dumping Via LSASS Process Clone | T1003 | #1, #7 | ambiguous |
| Potential Mftrace.EXE Abuse | T1127 | #1, #7 | ambiguous |
| Windows Default Domain GPO Modification via GPME | T1484 | #1 | ok |
| MMC20 Lateral Movement | T1021 | #1, #4 | ambiguous |
| MMC Executing Files with Reversed Extensions Using RTLO Abuse | T1036, T1204, T1218 | #1, #7, #9 | ambiguous |
| MMC Spawning Windows Shell | T1021 | #1, #4 | ambiguous |
| CodePage Modification Via MODE.COM To Russian Language | T1036 | #1, #7 | ambiguous |
| Potential Suspicious Mofcomp Execution | T1218 | #1, #7 | ambiguous |
| Potential Mpclient.DLL Sideloading Via Defender Binaries | T1574 | #1, #7 | ambiguous |
| File Download Via Windows Defender MpCmpRun.EXE | T1105, T1218 | #1, #7 | ambiguous |
| MSDT Execution Via Answer File | T1218 | #1, #7 | ambiguous |
| Potential Arbitrary Command Execution Using Msdt.EXE | T1202 | #1 | ok |
| Suspicious Cabinet File Execution Via Msdt.EXE | T1202 | #1 | ok |
| Suspicious MSDT Parent Process | T1036, T1218 | #1, #7 | ambiguous |
| Arbitrary File Download Via MSEDGE_PROXY.EXE | T1218 | #1, #7 | ambiguous |
| Remotely Hosted HTA File Executed Via Mshta.EXE | T1218 | #1, #7 | ambiguous |
| Wscript Shell Run In CommandLine | T1059 | #1, #7 | ambiguous |
| Suspicious JavaScript Execution Via Mshta.EXE | T1218 | #1, #7 | ambiguous |
| Potential LethalHTA Technique Execution | T1218 | #1, #7 | ambiguous |
| Suspicious MSHTA Child Process | T1218 | #1, #7 | ambiguous |
| MSHTA Execution with Suspicious File Extensions | T1059, T1140, T1218 | #1, #7 | ambiguous |
| Suspicious Mshta.EXE Execution Patterns | T1106 | #1, #7 | ambiguous |
| DllUnregisterServer Function Call Via Msiexec.EXE | T1218 | #1, #7 | ambiguous |
| Suspicious MsiExec Embedding Parent | T1218 | #1, #7 | ambiguous |
| Suspicious Msiexec Execute Arbitrary DLL | T1218 | #1, #7 | ambiguous |
| Msiexec Quiet Installation | T1218 | #1, #7 | ambiguous |
| Suspicious Msiexec Quiet Install From Remote Location | T1218 | #1, #7 | ambiguous |
| Potential MsiExec Masquerading | T1036 | #1, #7 | ambiguous |
| MsiExec Web Install | T1105, T1218 | #1, #7 | ambiguous |
| Windows MSIX Package Support Framework AI_STUBS Execution | T1204, T1218, T1553 | #1, #7, #9, #10 | ambiguous |
| Arbitrary File Download Via MSOHTMED.EXE | T1218 | #1, #7 | ambiguous |
| Arbitrary File Download Via MSPUB.EXE | T1218 | #1, #7 | ambiguous |
| Potential Process Injection Via Msra.EXE | T1055 | #1, #7 | ambiguous |
| Detection of PowerShell Execution via Sqlps.exe | T1059, T1127 | #1, #7 | ambiguous |
| SQL Client Tools PowerShell Session Detection | T1059, T1127 | #1, #7 | ambiguous |
| Suspicious Child Process Of SQL Server | T1190, T1505 | #1, #2, #7 | ambiguous |
| Potential MSTSC Shadowing Activity | T1563 | #1, #4 | ambiguous |
| New Remote Desktop Connection Initiated Via Mstsc.EXE | T1021 | #1, #4 | ambiguous |
| Mstsc.EXE Execution With Local RDP File | T1219 | #1, #7 | ambiguous |
| Suspicious Mstsc.EXE Execution With Local RDP File | T1219 | #1, #7 | ambiguous |
| Msxsl.EXE Execution | T1220 | #1, #7 | ambiguous |
| Remote XSL Execution Via Msxsl.EXE | T1220 | #1, #7 | ambiguous |
| Suspicious Group And Account Reconnaissance Activity Using Net.EXE | T1087 | #1 | ok |
| Unmount Share Via Net.EXE | T1070 | #1 | ok |
| Start Windows Service Via Net.EXE | T1569 | #1, #7 | ambiguous |
| Stop Windows Service Via Net.EXE | T1489 | #1 | ok |
| Windows Admin Share Mount Via Net.EXE | T1021 | #1, #4 | ambiguous |
| Windows Internet Hosted WebDav Share Mount Via Net.EXE | T1021 | #1, #4 | ambiguous |
| Windows Share Mount Via Net.EXE | T1021 | #1, #4 | ambiguous |
| System Network Connections Discovery Via Net.EXE | T1049 | #1 | ok |
| Password Provided In Command Line Of Net.EXE | T1021, T1078 | #1, #4 | ambiguous |
| New User Created Via Net.EXE | T1136 | #1 | ok |
| New User Created Via Net.EXE With Never Expire Option | T1136 | #1 | ok |
| Suspicious Manipulation Of Default Accounts Via Net.EXE | T1560 | #1 | ok |
| Share And Session Enumeration Using Net.EXE | T1018 | #1 | ok |
| Firewall Configuration Discovery Via Netsh.EXE | T1016 | #1 | ok |
| Potential Persistence Via Netsh Helper DLL | T1546 | #1, #7 | ambiguous |
| New Network Trace Capture Started Via Netsh.EXE | T1040 | #1, #5 | ambiguous |
| New Port Forwarding Rule Added Via Netsh.EXE | T1090 | #1, #7 | ambiguous |
| RDP Port Forwarding Rule Added Via Netsh.EXE | T1090 | #1, #7 | ambiguous |
| Harvesting Of Wifi Credentials Via Netsh.EXE | T1040 | #1, #5 | ambiguous |
| Nltest.EXE Execution | T1016, T1018, T1482 | #1 | ok |
| Potential Recon Activity Via Nltest.EXE | T1016, T1482 | #1 | ok |
| Potential Arbitrary Code Execution Via Node.EXE | T1127 | #1, #7 | ambiguous |
| Node Process Executions | T1059, T1127 | #1, #7 | ambiguous |
| Notepad Password Files Discovery | T1083 | #1 | ok |
| Network Reconnaissance Activity | T1082, T1087 | #1 | ok |
| Suspicious Usage Of Active Directory Diagnostic Tool (ntdsutil.exe) | T1003 | #1, #7 | ambiguous |
| Invocation of Active Directory Diagnostic Tool (ntdsutil.exe) | T1003 | #1, #7 | ambiguous |
| Driver/DLL Installation Via Odbcconf.EXE | T1218 | #1, #7 | ambiguous |
| Suspicious Driver/DLL Installation Via Odbcconf.EXE | T1218 | #1, #7 | ambiguous |
| Odbcconf.EXE Suspicious DLL Location | T1218 | #1, #7 | ambiguous |
| New DLL Registered Via Odbcconf.EXE | T1218 | #1, #7 | ambiguous |
| Potentially Suspicious DLL Registered Via Odbcconf.EXE | T1218 | #1, #7 | ambiguous |
| Response File Execution Via Odbcconf.EXE | T1218 | #1, #7 | ambiguous |
| Suspicious Response File Execution Via Odbcconf.EXE | T1218 | #1, #7 | ambiguous |
| Uncommon Child Process Spawned By Odbcconf.EXE | T1218 | #1, #7 | ambiguous |
| Potential Arbitrary File Download Using Office Application | T1202 | #1 | ok |
| Potential Excel.EXE DCOM Lateral Movement Via ActivateMicrosoftApp | T1021 | #1, #4 | ambiguous |
| Potentially Suspicious Office Document Executed From Trusted Location | T1202 | #1 | ok |
| OneNote.EXE Execution of Malicious Embedded Scripts | T1218 | #1, #7 | ambiguous |
| Outlook EnableUnsafeClientMailRules Setting Enabled | T1059, T1202 | #1, #7 | ambiguous |
| Suspicious Remote Child Process From Outlook | T1059, T1202 | #1, #7 | ambiguous |
| Suspicious Microsoft Office Child Process | T1047, T1204, T1218 | #1, #7, #9 | ambiguous |
| Potential Arbitrary DLL Load Using Winword | T1202 | #1 | ok |
| Potential Mpclient.DLL Sideloading Via OfflineScannerShell.EXE Execution | T1218 | #1, #7 | ambiguous |
| PDQ Deploy Remote Adminstartion Tool Execution | T1072 | #1, #7 | ambiguous |
| Perl Inline Command Execution | T1059 | #1, #7 | ambiguous |
| Php Inline Command Execution | T1059 | #1, #7 | ambiguous |
| Ping Hex IP | T1027, T1140 | #1, #7 | ambiguous |
| PktMon.EXE Execution | T1040 | #1, #5 | ambiguous |
| Suspicious Plink Port Forwarding | T1021, T1572 | #1, #4, #7 | ambiguous |
| Potential RDP Tunneling Via Plink | T1572 | #1, #7 | ambiguous |
| Audio Capture via PowerShell | T1123 | #1 | ok |
| Suspicious Encoded PowerShell Command Line | T1059 | #1, #7 | ambiguous |
| Suspicious PowerShell Encoded Command Patterns | T1059 | #1, #7 | ambiguous |
| PowerShell Base64 Encoded FromBase64String Cmdlet | T1059, T1140 | #1, #7 | ambiguous |
| Malicious Base64 Encoded PowerShell Keywords in Command Lines | T1059 | #1, #7 | ambiguous |
| PowerShell Base64 Encoded IEX Cmdlet | T1059 | #1, #7 | ambiguous |
| PowerShell Base64 Encoded Invoke Keyword | T1027, T1059 | #1, #7 | ambiguous |
| PowerShell Base64 Encoded Reflective Assembly Load | T1027, T1059, T1620 | #1, #7 | ambiguous |
| Suspicious Encoded And Obfuscated Reflection Assembly Load Function Call | T1027, T1059 | #1, #7 | ambiguous |
| PowerShell Base64 Encoded WMI Classes | T1027, T1059 | #1, #7 | ambiguous |
| Potential Process Execution Proxy Via CL_Invocation.ps1 | T1216 | #1, #7 | ambiguous |
| Assembly Loading Via CL_LoadAssembly.ps1 | T1216 | #1, #7 | ambiguous |
| Potential Script Proxy Execution Via CL_Mutexverifiers.ps1 | T1216 | #1, #7 | ambiguous |
| ConvertTo-SecureString Cmdlet Usage Via CommandLine | T1027, T1059 | #1, #7 | ambiguous |
| Potential PowerShell Obfuscation Via Reversed Commands | T1027, T1059 | #1, #7 | ambiguous |
| Potential PowerShell Command Line Obfuscation | T1027, T1059 | #1, #7 | ambiguous |
| Obfuscated PowerShell MSI Install via WindowsInstaller COM | T1027, T1059, T1218 | #1, #7 | ambiguous |
| PowerShell MSI Install via WindowsInstaller COM From Remote Location | T1059, T1105, T1218 | #1, #7 | ambiguous |
| Computer Discovery And Export Via Get-ADComputer Cmdlet | T1033 | #1 | ok |
| Potential PowerShell Console History Access Attempt via History File | T1552 | #1, #4 | ambiguous |
| New Service Creation Using PowerShell | T1543 | #1, #7 | ambiguous |
| Gzip Archive Decode Via PowerShell | T1132 | #1, #7 | ambiguous |
| Potential PowerShell Downgrade Attack | T1059 | #1, #7 | ambiguous |
| Potential COM Objects Download Cradles Usage - Process Creation | T1105 | #1 | ok |
| Obfuscated PowerShell OneLiner Execution | T1059, T1685 | #1, #7 | ambiguous |
| Potential DLL File Download Via PowerShell Invoke-WebRequest | T1059, T1105 | #1, #7 | ambiguous |
| PowerShell Download and Execution Cradles | T1059 | #1, #7 | ambiguous |
| PowerShell Download Pattern | T1059 | #1, #7 | ambiguous |
| DSInternals Suspicious PowerShell Cmdlets | T1059 | #1, #7 | ambiguous |
| Suspicious Execution of Powershell with Base64 | T1059 | #1, #7 | ambiguous |
| Potential Encoded PowerShell Patterns In CommandLine | T1027, T1059 | #1, #7 | ambiguous |
| Powershell Inline Execution From A File | T1059 | #1, #7 | ambiguous |
| Certificate Exported Via PowerShell | T1059, T1552 | #1, #4, #7 | ambiguous |
| Base64 Encoded PowerShell Command Detected | T1027, T1059, T1140 | #1, #7 | ambiguous |
| Suspicious FromBase64String Usage On Gzip Archive - Process Creation | T1132 | #1, #7 | ambiguous |
| PowerShell Get-Clipboard Cmdlet Via CLI | T1115 | #1 | ok |
| Suspicious Reconnaissance Activity Using Get-LocalGroupMember Cmdlet | T1087 | #1 | ok |
| PowerShell Get-Process LSASS | T1552 | #1, #4 | ambiguous |
| Abuse of Service Permissions to Hide Services Via Set-Service | T1574 | #1, #7 | ambiguous |
| Suspicious PowerShell IEX Execution Patterns | T1059 | #1, #7 | ambiguous |
| Root Certificate Installed From Susp Locations | T1553 | #1, #10 | ambiguous |
| Import PowerShell Modules From Suspicious Directories - ProcCreation | T1059 | #1, #7 | ambiguous |
| Suspicious Invoke-WebRequest Execution With DirectIP | T1105 | #1 | ok |
| Suspicious Invoke-WebRequest Execution | T1105 | #1 | ok |
| Suspicious Kerberos Ticket Request via CLI | T1558 | #1, #4 | ambiguous |
| Malicious PowerShell Commandlets - ProcessCreation | T1059, T1069, T1087, T1482 | #1, #7 | ambiguous |
| MSExchange Transport Agent Installation | T1505 | #1, #7 | ambiguous |
| Non Interactive PowerShell Process Spawned | T1059 | #1, #7 | ambiguous |
| Potential PowerShell Obfuscation Via WCHAR/CHAR | T1027, T1059 | #1, #7 | ambiguous |
| Execution of Powershell Script in Public Folder | T1059 | #1, #7 | ambiguous |
| RemoteFXvGPUDisablement Abuse Via AtomicTestHarnesses | T1218 | #1, #7 | ambiguous |
| Potential Powershell ReverseShell Connection | T1059 | #1, #7 | ambiguous |
| Run PowerShell Script from ADS | T1564 | #1 | ok |
| Run PowerShell Script from Redirected Input Stream | T1059 | #1, #7 | ambiguous |
| PowerShell SAM Copy | T1003 | #1, #7 | ambiguous |
| Suspicious PowerShell Invocation From Script Engines | T1059 | #1, #7 | ambiguous |
| Potentially Suspicious Powershell Script Execution From Temp Folder | T1059 | #1, #7 | ambiguous |
| Suspicious Service DACL Modification Via Set-Service Cmdlet | T1543 | #1, #7 | ambiguous |
| Change PowerShell Policies to an Insecure Level | T1059 | #1, #7 | ambiguous |
| Deletion of Volume Shadow Copies via WMI with PowerShell | T1490 | #1 | ok |
| Exchange PowerShell Snap-Ins Usage | T1059, T1114 | #1, #4, #7 | ambiguous |
| Stop Windows Service Via PowerShell Stop-Service | T1489 | #1 | ok |
| Suspicious PowerShell Download and Execute Pattern | T1059 | #1, #7 | ambiguous |
| Suspicious PowerShell Parameter Substring | T1059 | #1, #7 | ambiguous |
| Suspicious PowerShell Parent Process | T1059 | #1, #7 | ambiguous |
| PowerShell Script Run in AppData | T1059 | #1, #7 | ambiguous |
| Powershell Token Obfuscation - Process Creation | T1027 | #1, #7 | ambiguous |
| User Discovery And Export Via Get-ADUser Cmdlet | T1033 | #1 | ok |
| Net WebClient Casing Anomalies | T1059 | #1, #7 | ambiguous |
| Suspicious X509Enrollment - Process Creation | T1553 | #1, #10 | ambiguous |
| Suspicious XOR Encoded PowerShell Command | T1027, T1059, T1140 | #1, #7 | ambiguous |
| Folder Compress To Potentially Suspicious Output Via Compress-Archive Cmdlet | T1074 | #1 | ok |
| Arbitrary File Download Via PresentationHost.EXE | T1218 | #1, #7 | ambiguous |
| XBAP Execution From Uncommon Locations Via PresentationHost.EXE | T1218 | #1, #7 | ambiguous |
| Visual Studio NodejsTools PressAnyKey Arbitrary Binary Execution | T1218 | #1, #7 | ambiguous |
| Sensitive File Dump Via Print.EXE | T1003, T1218 | #1, #7 | ambiguous |
| Abusing Print Executable | T1218 | #1, #7 | ambiguous |
| File Download Using ProtocolHandler.exe | T1218 | #1, #7 | ambiguous |
| Potential Provlaunch.EXE Binary Proxy Execution Abuse | T1218 | #1, #7 | ambiguous |
| Suspicious Provlaunch.EXE Child Process | T1218 | #1, #7 | ambiguous |
| Screen Capture Activity Via Psr.EXE | T1113 | #1 | ok |
| PUA - 3Proxy Execution | T1572 | #1, #7 | ambiguous |
| PUA - Suspicious ActiveDirectory Enumeration Via AdFind.EXE | T1087 | #1 | ok |
| PUA - AdFind.EXE Execution | T1087 | #1 | ok |
| PUA - AdFind Suspicious Execution | T1018, T1069, T1087, T1482 | #1 | ok |
| PUA - Advanced IP Scanner Execution | T1046, T1135 | #1 | ok |
| PUA - Advanced Port Scanner Execution | T1046, T1135 | #1 | ok |
| PUA - AdvancedRun Execution | T1059, T1134, T1564 | #1, #4, #7 | ambiguous |
| PUA - AdvancedRun Suspicious Execution | T1134 | #1, #4 | ambiguous |
| PUA - Chisel Tunneling Tool Execution | T1090 | #1, #7 | ambiguous |
| PUA - CsExec Execution | T1569, T1587 | #1, #7 | ambiguous |
| PUA - DefenderCheck Execution | T1027 | #1, #7 | ambiguous |
| PUA - DIT Snapshot Viewer | T1003 | #1, #7 | ambiguous |
| PUA - Fast Reverse Proxy (FRP) Execution | T1090 | #1, #7 | ambiguous |
| PUA- IOX Tunneling Tool Execution | T1090 | #1, #7 | ambiguous |
| PUA - Kernel Driver Utility (KDU) Execution | T1543 | #1, #7 | ambiguous |
| PUA - Memory Dump Mount Via MemProcFS | T1003 | #1, #7 | ambiguous |
| PUA - Mouse Lock Execution | T1056 | #1, #7 | ambiguous |
| PUA - Netcat Suspicious Execution | T1095 | #1, #7 | ambiguous |
| PUA - SoftPerfect Netscan Execution | T1046 | #1 | ok |
| PUA - Ngrok Execution | T1572 | #1, #7 | ambiguous |
| PUA - Nimgrab Execution | T1105 | #1 | ok |
| PUA - NimScan Execution | T1046 | #1 | ok |
| PUA - NirCmd Execution | T1569 | #1, #7 | ambiguous |
| PUA - NirCmd Execution As LOCAL SYSTEM | T1569 | #1, #7 | ambiguous |
| PUA - Nmap/Zenmap Execution | T1046 | #1 | ok |
| PUA - NPS Tunneling Tool Execution | T1090 | #1, #7 | ambiguous |
| PUA - NSudo Execution | T1569 | #1, #7 | ambiguous |
| PUA - PingCastle Execution | T1595 | #1 | ok |
| PUA - PingCastle Execution From Potentially Suspicious Parent | T1595 | #1 | ok |
| PUA - Process Hacker Execution | T1543, T1564, T1622 | #1, #7 | ambiguous |
| PUA - Radmin Viewer Utility Execution | T1072 | #1, #7 | ambiguous |
| PUA - Potential PE Metadata Tamper Using Rcedit | T1027, T1036 | #1, #7 | ambiguous |
| PUA - Rclone Execution | T1567 | #1, #7 | ambiguous |
| PUA - Restic Backup Tool Execution | T1048, T1567 | #1, #7 | ambiguous |
| PUA - RunXCmd Execution | T1569 | #1, #7 | ambiguous |
| PUA - Seatbelt Execution | T1083, T1087, T1526 | #1 | ok |
| PUA - System Informer Execution | T1082, T1543, T1564 | #1, #7 | ambiguous |
| PUA - TruffleHog Execution | T1083, T1552 | #1, #4 | ambiguous |
| PUA - WebBrowserPassView Execution | T1555 | #1, #4, #7 | ambiguous |
| PUA - Wsudo Suspicious Execution | T1059 | #1, #7 | ambiguous |
| PUA - Adidnsdump Execution | T1018 | #1 | ok |
| Python One-Liners with Base64 Decoding | T1027, T1059 | #1, #7 | ambiguous |
| Python Inline Command Execution | T1059 | #1, #7 | ambiguous |
| Python Spawning Pretty TTY on Windows | T1059 | #1, #7 | ambiguous |
| Potentially Suspicious Usage Of Qemu | T1090, T1572 | #1, #7 | ambiguous |
| QuickAssist Execution | T1219 | #1, #7 | ambiguous |
| Files Added To An Archive Using Rar.EXE | T1560 | #1 | ok |
| Rar Usage with Password and Compression Level | T1560 | #1 | ok |
| Suspicious Greedy Compression Using Rar.EXE | T1059 | #1, #7 | ambiguous |
| Suspicious RASdial Activity | T1059 | #1, #7 | ambiguous |
| RDP Enable or Disable via Win32_TerminalServiceSetting WMI Class | T1021, T1047 | #1, #4, #7 | ambiguous |
| Process Memory Dump via RdrLeakDiag.EXE | T1003 | #1, #7 | ambiguous |
| Windows Recovery Environment Disabled Via Reagentc | T1490 | #1 | ok |
| Potential Persistence Attempt Via Run Keys Using Reg.EXE | T1547 | #1, #7 | ambiguous |
| Dropping Of Password Filter DLL | T1556 | #1, #7 | ambiguous |
| RunMRU Registry Key Deletion | T1070 | #1 | ok |
| Potentially Suspicious Desktop Background Change Using Reg.EXE | T1112, T1491 | #1, #7 | ambiguous |
| Direct Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| Dumping of Sensitive Hives Via Reg.EXE | T1003 | #1, #7 | ambiguous |
| Windows Recall Feature Enabled Via Reg.EXE | T1113 | #1 | ok |
| Enumeration for Credentials in Registry | T1552 | #1, #4 | ambiguous |
| Potential Suspicious Registry File Imported Via Reg.EXE | T1112 | #1 | ok |
| RestrictedAdminMode Registry Value Tampering - ProcCreation | T1112 | #1 | ok |
| Suspicious Query of MachineGUID | T1082 | #1 | ok |
| Modify Group Policy Settings | T1484 | #1 | ok |
| Enable LM Hash Storage - ProcCreation | T1112 | #1 | ok |
| Potential Configuration And Service Reconnaissance Via Reg.EXE | T1007, T1012 | #1 | ok |
| Potential Tampering With RDP Related Registry Keys Via Reg.EXE | T1021, T1112 | #1, #4 | ambiguous |
| Suspicious ScreenSave Change by Reg.exe | T1546 | #1, #7 | ambiguous |
| Changing Existing Service ImagePath Value Via Reg.EXE | T1574 | #1, #7 | ambiguous |
| Detected Windows Software Discovery | T1518 | #1 | ok |
| Reg Add Suspicious Paths | T1112, T1685 | #1 | ambiguous |
| System Language Discovery via Reg.Exe | T1614 | #1 | ok |
| System Restore Registry Modification via CommandLine | T1490 | #1 | ok |
| RegAsm.EXE Execution Without CommandLine Flags or Files | T1218 | #1, #7 | ambiguous |
| Potentially Suspicious Execution Of Regasm/Regsvcs With Uncommon Extension | T1218 | #1, #7 | ambiguous |
| Potentially Suspicious Execution Of Regasm/Regsvcs From Uncommon Location | T1218 | #1, #7 | ambiguous |
| Exports Critical Registry Keys To a File | T1012 | #1 | ok |
| Exports Registry Key To a File | T1012 | #1 | ok |
| Imports Registry Key From a File | T1112 | #1 | ok |
| Imports Registry Key From an ADS | T1112 | #1 | ok |
| Regedit as Trusted Installer | T1548 | #1, #7 | ambiguous |
| Suspicious Registry Modification From ADS Via Regini.EXE | T1112 | #1 | ok |
| Registry Modification Via Regini.EXE | T1112 | #1 | ok |
| DLL Execution Via Register-cimprovider.exe | T1574 | #1, #7 | ambiguous |
| Enumeration for 3rd Party Creds From CLI | T1552 | #1, #4 | ambiguous |
| Registry Export of Third-Party Credentials | T1552 | #1, #4 | ambiguous |
| Suspicious Debugger Registration Cmdline | T1546 | #1, #7 | ambiguous |
| Potential Persistence Via Logon Scripts - CommandLine | T1037 | #1, #7 | ambiguous |
| Potential Credential Dumping Attempt Using New NetworkProvider - CLI | T1003 | #1, #7 | ambiguous |
| Potential Privilege Escalation via Service Permissions Weakness | T1574 | #1, #7 | ambiguous |
| Potential Provisioning Registry Key Abuse For Binary Proxy Execution | T1218 | #1, #7 | ambiguous |
| Hiding User Account Via SpecialAccounts Registry Key - CommandLine | T1564 | #1 | ok |
| Potential Regsvr32 Commandline Flag Anomaly | T1218 | #1, #7 | ambiguous |
| Potentially Suspicious Regsvr32 HTTP IP Pattern | T1218 | #1, #7 | ambiguous |
| Potentially Suspicious Regsvr32 HTTP/FTP Pattern | T1218 | #1, #7 | ambiguous |
| Suspicious Regsvr32 Execution From Remote Share | T1218 | #1, #7 | ambiguous |
| Potentially Suspicious Child Process Of Regsvr32 | T1218 | #1, #7 | ambiguous |
| Regsvr32 Execution From Potential Suspicious Location | T1218 | #1, #7 | ambiguous |
| Regsvr32 Execution From Highly Suspicious Location | T1218 | #1, #7 | ambiguous |
| Regsvr32 DLL Execution With Suspicious File Extension | T1218 | #1, #7 | ambiguous |
| Scripting/CommandLine Process Spawned Regsvr32 | T1218 | #1, #7 | ambiguous |
| Regsvr32 DLL Execution With Uncommon Extension | T1574 | #1, #7 | ambiguous |
| Remote Access Tool - AnyDesk Execution | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - AnyDesk Piped Password Via CLI | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - AnyDesk Silent Installation | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - Anydesk Execution From Suspicious Folder | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - GoToAssist Execution | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - LogMeIn Execution | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - Potential MeshAgent Execution - Windows | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - MeshAgent Command Execution via MeshCentral | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - NetSupport Execution | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - Renamed MeshAgent Execution - Windows | T1036, T1219 | #1, #7 | ambiguous |
| Remote Access Tool - ScreenConnect Execution | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - ScreenConnect Remote Command Execution | T1059 | #1, #7 | ambiguous |
| Remote Access Tool - ScreenConnect Potential Suspicious Remote Command Execution | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - Simple Help Execution | T1219 | #1, #7 | ambiguous |
| Remote Access Tool - TacticalRMM Agent Registration to Potentially Attacker-Controlled Server | T1105, T1219 | #1, #7 | ambiguous |
| Remote Access Tool - UltraViewer Execution | T1219 | #1, #7 | ambiguous |
| Discovery of a System Time | T1124 | #1 | ok |
| Renamed AdFind Execution | T1018, T1069, T1087, T1482 | #1 | ok |
| Renamed AutoIt Execution | T1027 | #1, #7 | ambiguous |
| Potential Defense Evasion Via Binary Rename | T1036 | #1, #7 | ambiguous |
| Potential Defense Evasion Via Rename Of Highly Relevant Binaries | T1036 | #1, #7 | ambiguous |
| Renamed BOINC Client Execution | T1553 | #1, #10 | ambiguous |
| Renamed BrowserCore.EXE Execution | T1036, T1528 | #1, #4, #7, #9 | ambiguous |
| Renamed Cloudflared.EXE Execution | T1090 | #1, #7 | ambiguous |
| Renamed CreateDump Utility Execution | T1003, T1036 | #1, #7 | ambiguous |
| Renamed CURL.EXE Execution | T1059, T1202 | #1, #7 | ambiguous |
| Renamed ZOHO Dctask64 Execution | T1036, T1055, T1202, T1218 | #1, #7 | ambiguous |
| Renamed FTP.EXE Execution | T1059, T1202 | #1, #7 | ambiguous |
| Renamed Jusched.EXE Execution | T1036 | #1, #7 | ambiguous |
| Renamed Mavinject.EXE Execution | T1055, T1218 | #1, #7 | ambiguous |
| Renamed MegaSync Execution | T1218 | #1, #7 | ambiguous |
| Renamed Msdt.EXE Execution | T1036 | #1, #7 | ambiguous |
| Renamed NirCmd.EXE Execution | T1059, T1202 | #1, #7 | ambiguous |
| Renamed Office Binary Execution | T1036 | #1, #7 | ambiguous |
| Renamed PAExec Execution | T1202 | #1 | ok |
| Renamed PingCastle Binary Execution | T1059, T1202 | #1, #7 | ambiguous |
| Renamed Plink Execution | T1036 | #1, #7 | ambiguous |
| Visual Studio NodejsTools PressAnyKey Renamed Execution | T1218 | #1, #7 | ambiguous |
| Renamed Schtasks Execution | T1036, T1053 | #1, #7 | ambiguous |
| Renamed ProcDump Execution | T1036 | #1, #7 | ambiguous |
| Renamed Vmnat.exe Execution | T1574 | #1, #7 | ambiguous |
| Renamed Whoami Execution | T1033 | #1 | ok |
| Capture Credentials with Rpcping.exe | T1003 | #1, #7 | ambiguous |
| Ruby Inline Command Execution | T1059 | #1, #7 | ambiguous |
| Potential Rundll32 Execution With DLL Stored In ADS | T1564 | #1 | ok |
| Suspicious Rundll32 Invoking Inline VBScript | T1055 | #1, #7 | ambiguous |
| Rundll32 InstallScreenSaver Execution | T1218 | #1, #7 | ambiguous |
| Suspicious Key Manager Access | T1555 | #1, #4, #7 | ambiguous |
| Rundll32 Execution Without CommandLine Parameters | T1202 | #1 | ok |
| Potential Obfuscated Ordinal Call Via Rundll32 | T1027 | #1, #7 | ambiguous |
| Process Memory Dump Via Comsvcs.DLL | T1003, T1036 | #1, #7 | ambiguous |
| Rundll32 Registered COM Objects | T1546 | #1, #7 | ambiguous |
| Suspicious Process Start Locations | T1036 | #1, #7 | ambiguous |
| Suspicious Rundll32 Setupapi.dll Activity | T1218 | #1, #7 | ambiguous |
| Shell32 DLL Execution in Suspicious Directory | T1218 | #1, #7 | ambiguous |
| RunDLL32 Spawning Explorer | T1218 | #1, #7 | ambiguous |
| Potentially Suspicious Rundll32 Activity | T1218 | #1, #7 | ambiguous |
| Suspicious Control Panel DLL Load | T1218 | #1, #7 | ambiguous |
| Suspicious Rundll32 Execution With Image Extension | T1218 | #1, #7 | ambiguous |
| Suspicious ShellExec_RunDLL Call Via Ordinal | T1218 | #1, #7 | ambiguous |
| ShimCache Flush | T1112 | #1 | ok |
| Suspicious Rundll32 Activity Invoking Sys File | T1218 | #1, #7 | ambiguous |
| Potentially Suspicious Rundll32.EXE Execution of UDL File | T1071, T1218 | #1, #7 | ambiguous |
| Rundll32 UNC Path Execution | T1021, T1218 | #1, #4, #7 | ambiguous |
| Rundll32 Execution With Uncommon DLL Extension | T1218 | #1, #7 | ambiguous |
| WebDav Client Execution Via Rundll32.EXE | T1048 | #1, #7 | ambiguous |
| Suspicious WebDav Client Execution Via Rundll32.EXE | T1048 | #1, #7 | ambiguous |
| Rundll32 Execution Without Parameters | T1021, T1569, T1570 | #1, #4, #7 | ambiguous |
| Run Once Task Execution as Configured in Registry | T1112 | #1 | ok |
| Possible Privilege Escalation via Weak Service Permissions | T1574 | #1, #7 | ambiguous |
| New Service Creation Using Sc.EXE | T1543 | #1, #7 | ambiguous |
| New Kernel Driver Via SC.EXE | T1543 | #1, #7 | ambiguous |
| Interesting Service Enumeration Via Sc.EXE | T1003 | #1, #7 | ambiguous |
| Allow Service Access Using Security Descriptor Tampering Via Sc.EXE | T1543 | #1, #7 | ambiguous |
| Deny Service Access Using Security Descriptor Tampering Via Sc.EXE | T1543 | #1, #7 | ambiguous |
| Service DACL Abuse To Hide Services Via Sc.EXE | T1574 | #1, #7 | ambiguous |
| Service Security Descriptor Tampering Via Sc.EXE | T1574 | #1, #7 | ambiguous |
| Suspicious Service Path Modification | T1543 | #1, #7 | ambiguous |
| Potential Persistence Attempt Via Existing Service Tampering | T1543, T1574 | #1, #7 | ambiguous |
| Stop Windows Service Via Sc.EXE | T1489 | #1 | ok |
| Suspicious Schtasks Execution AppData Folder | T1053, T1059 | #1, #7 | ambiguous |
| Suspicious Modification Of Scheduled Tasks | T1053 | #1, #7 | ambiguous |
| Scheduled Task Creation Via Schtasks.EXE | T1053 | #1, #7 | ambiguous |
| Suspicious Scheduled Task Creation Involving Temp Folder | T1053 | #1, #7 | ambiguous |
| Scheduled Task Creation with Curl and PowerShell Execution Combo | T1053, T1105, T1218 | #1, #7 | ambiguous |
| Delete Important Scheduled Task | T1489 | #1 | ok |
| Delete All Scheduled Tasks | T1489 | #1 | ok |
| Disable Important Scheduled Task | T1489 | #1 | ok |
| Schedule Task Creation From Env Variable Or Potentially Suspicious Path Via Schtasks.EXE | T1053 | #1, #7 | ambiguous |
| Schtasks From Suspicious Folders | T1053 | #1, #7 | ambiguous |
| Suspicious Scheduled Task Name As GUID | T1053 | #1, #7 | ambiguous |
| Uncommon One Time Only Scheduled Task At 00:00 | T1053 | #1, #7 | ambiguous |
| Potential SSH Tunnel Persistence Install Using A Scheduled Task | T1053 | #1, #7 | ambiguous |
| Potential Persistence Via Microsoft Compatibility Appraiser | T1053 | #1, #7 | ambiguous |
| Potential Persistence Via Powershell Search Order Hijacking - Task | T1053, T1059 | #1, #7 | ambiguous |
| Scheduled Task Executing Payload from Registry | T1053, T1059 | #1, #7 | ambiguous |
| Scheduled Task Executing Encoded Payload from Registry | T1053, T1059 | #1, #7 | ambiguous |
| Suspicious Schtasks Schedule Types | T1053 | #1, #7 | ambiguous |
| Suspicious Schtasks Schedule Type With High Privileges | T1053 | #1, #7 | ambiguous |
| Suspicious Scheduled Task Creation via Masqueraded XML File | T1036, T1053 | #1, #7 | ambiguous |
| Suspicious Command Patterns In Scheduled Task Creation | T1053 | #1, #7 | ambiguous |
| Schtasks Creation Or Modification With SYSTEM Privileges | T1053 | #1, #7 | ambiguous |
| Scheduled Task Creation Masquerading as System Processes | T1036, T1053 | #1, #7 | ambiguous |
| Script Event Consumer Spawning Process | T1047 | #1, #7 | ambiguous |
| Potential Shim Database Persistence via Sdbinst.EXE | T1546 | #1, #7 | ambiguous |
| Uncommon Extension Shim Database Installation Via Sdbinst.EXE | T1546 | #1, #7 | ambiguous |
| Sdclt Child Processes | T1548 | #1, #7 | ambiguous |
| Sdiagnhost Calling Suspicious Child Process | T1036, T1218 | #1, #7 | ambiguous |
| Potential Suspicious Activity Using SeCEdit | T1082, T1505, T1546, T1547, T1556, T1557, T1564, T1574, T1685 | #1, #5, #7 | ambiguous |
| NodeJS Execution of JavaScript File | T1059 | #1, #7 | ambiguous |
| Suspicious Serv-U Process Pattern | T1555 | #1, #4, #7 | ambiguous |
| Uncommon Child Process Of Setres.EXE | T1202, T1218 | #1, #7 | ambiguous |
| Potential SPN Enumeration Via Setspn.EXE | T1558 | #1, #4 | ambiguous |
| Setup16.EXE Execution With Custom .Lst File | T1574 | #1, #7 | ambiguous |
| Indirect Command Execution via SFTP ProxyCommand | T1202 | #1 | ok |
| Suspicious Execution of Shutdown | T1529 | #1, #7 | ambiguous |
| Suspicious Execution of Shutdown to Log Out | T1529 | #1, #7 | ambiguous |
| Uncommon Sigverif.EXE Child Process | T1216 | #1, #7 | ambiguous |
| Audio Capture via SoundRecorder | T1123 | #1 | ok |
| Suspicious Speech Runtime Binary Child Process | T1021, T1218 | #1, #4, #7 | ambiguous |
| Suspicious Splwow64 Without Params | T1202 | #1 | ok |
| Veeam Backup Database Suspicious Query | T1005 | #1 | ok |
| VeeamBackup Database Credentials Dump Via Sqlcmd.EXE | T1005 | #1 | ok |
| SQLite Chromium Profile Data DB Access | T1005, T1539, T1555 | #1, #4, #7 | ambiguous |
| SQLite Firefox Profile Data DB Access | T1005, T1539 | #1, #7 | ambiguous |
| Arbitrary File Download Via Squirrel.EXE | T1218 | #1, #7 | ambiguous |
| Process Proxy Execution Via Squirrel.EXE | T1218 | #1, #7 | ambiguous |
| Port Forwarding Activity Via SSH.EXE | T1021, T1572 | #1, #4, #7 | ambiguous |
| Program Executed Using Proxy/Local Command Via SSH.EXE | T1218 | #1, #7 | ambiguous |
| Potential RDP Tunneling Via SSH | T1572 | #1, #7 | ambiguous |
| Potential Amazon SSM Agent Hijacking | T1219 | #1, #7 | ambiguous |
| Execution via stordiag.exe | T1218 | #1, #7 | ambiguous |
| Abused Debug Privilege by Arbitrary Parent Processes | T1548 | #1, #7 | ambiguous |
| User Added to Local Administrators Group | T1098 | #1 | ok |
| User Added To Highly Privileged Group | T1098 | #1 | ok |
| User Added to Remote Desktop Users Group | T1021, T1133, T1136 | #1, #4 | ambiguous |
| Execute From Alternate Data Streams | T1564 | #1 | ok |
| Always Install Elevated Windows Installer | T1548 | #1, #7 | ambiguous |
| Automated Collection Command Prompt | T1119, T1552 | #1, #4 | ambiguous |
| Bad Opsec Defaults Sacrificial Processes With Improper Arguments | T1218 | #1, #7 | ambiguous |
| Suspicious Child Process Created as System | T1134 | #1, #4 | ambiguous |
| Potential CommandLine Obfuscation Using Unicode Characters From Suspicious Image | T1027 | #1, #7 | ambiguous |
| Suspicious Explorer Process with Whitespace Padding - ClickFix/FileFix | T1027, T1204 | #1, #7, #9 | ambiguous |
| Suspicious Usage of For Loop with Recursive Directory Search in CMD | T1027, T1059 | #1, #7 | ambiguous |
| Potential Command Line Path Traversal Evasion Attempt | T1036 | #1, #7 | ambiguous |
| Potential Browser Data Stealing | T1555 | #1, #4, #7 | ambiguous |
| Copy From Or To Admin Share Or Sysvol Folder | T1021, T1039, T1048 | #1, #4, #7 | ambiguous |
| Suspicious Copy From or To System Directory | T1036 | #1, #7 | ambiguous |
| LOL-Binary Copied From System Directory | T1036 | #1, #7 | ambiguous |
| Potential Crypto Mining Activity | T1496 | #1, #7 | ambiguous |
| Potential Data Exfiltration Activity Via CommandLine Tools | T1059 | #1, #7 | ambiguous |
| Suspicious Parent Double Extension File Execution | T1036 | #1, #7 | ambiguous |
| Suspicious Download from Office Domain | T1105, T1608 | #1 | ambiguous |
| Always Install Elevated MSI Spawned Cmd And Powershell | T1548 | #1, #7 | ambiguous |
| Elevated System Shell Spawned From Uncommon Parent Location | T1059 | #1, #7 | ambiguous |
| Hidden Powershell in Link File Pattern | T1059 | #1, #7 | ambiguous |
| ETW Trace Evasion Activity | T1070, T1685 | #1 | ambiguous |
| Potentially Suspicious EventLog Recon Activity Using Log Query Utilities | T1087, T1552 | #1, #4 | ambiguous |
| Potentially Suspicious Execution From Parent Process In Public Folder | T1059, T1564 | #1, #7 | ambiguous |
| Process Execution From A Potentially Suspicious Folder | T1036 | #1, #7 | ambiguous |
| Suspicious File Characteristics Due to Missing Fields | T1059 | #1, #7 | ambiguous |
| Suspicious Reconnaissance Activity Via GatherNetworkInfo.VBS | T1059, T1615 | #1, #7 | ambiguous |
| Potential Hidden Directory Creation Via NTFS INDEX_ALLOCATION Stream - CLI | T1564 | #1 | ok |
| Writing Of Malicious Files To The Fonts Folder | T1059, T1211 | #1, #2, #3, #7 | ambiguous |
| Potential Homoglyph Attack Using Lookalike Characters | T1036 | #1, #7 | ambiguous |
| Potentially Suspicious Inline JavaScript Execution via NodeJS Binary | T1059 | #1, #7 | ambiguous |
| Potential WinAPI Calls Via CommandLine | T1106 | #1, #7 | ambiguous |
| Potentially Suspicious JWT Token Search Via CLI | T1528, T1552 | #1, #4, #9 | ambiguous |
| Local Accounts Discovery | T1033, T1087 | #1 | ok |
| LSASS Dump Keyword In CommandLine | T1003 | #1, #7 | ambiguous |
| Potential File Download Via MS-AppInstaller Protocol Handler | T1218 | #1, #7 | ambiguous |
| Suspicious Network Command | T1016 | #1 | ok |
| Suspicious Scan Loop Network | T1018, T1059 | #1, #7 | ambiguous |
| Potential Network Sniffing Activity Using Network Tools | T1040 | #1, #5 | ambiguous |
| Non-privileged Usage of Reg or Powershell | T1112 | #1 | ok |
| Suspicious Process Patterns NTDS.DIT Exfil | T1003 | #1, #7 | ambiguous |
| Use Short Name Path in Image | T1564 | #1 | ok |
| Use NTFS Short Name in Command Line | T1564 | #1 | ok |
| Use NTFS Short Name in Image | T1564 | #1 | ok |
| Suspicious Process Parents | T1036 | #1, #7 | ambiguous |
| Potential PowerShell Execution Via DLL | T1218 | #1, #7 | ambiguous |
| Privilege Escalation via Named Pipe Impersonation | T1021 | #1, #4 | ambiguous |
| Private Keys Reconnaissance Via CommandLine Tools | T1552 | #1, #4 | ambiguous |
| Windows Processes Suspicious Parent Directory | T1036 | #1, #7 | ambiguous |
| Suspicious Program Names | T1059 | #1, #7 | ambiguous |
| Recon Information for Export with Command Prompt | T1119 | #1 | ok |
| Suspicious Redirection to Local Admin Share | T1048 | #1, #7 | ambiguous |
| Registry Modification of MS-settings Protocol Handler | T1112, T1546, T1548 | #1, #7 | ambiguous |
| Potential Remote Desktop Tunneling | T1021 | #1, #4 | ambiguous |
| Potential Defense Evasion Via Right-to-Left Override | T1036 | #1, #7 | ambiguous |
| Script Interpreter Execution From Suspicious Folder | T1059 | #1, #7 | ambiguous |
| Script Interpreter Spawning Credential Scanner - Windows | T1005, T1059, T1552 | #1, #4, #7 | ambiguous |
| Sensitive File Access Via Volume Shadow Copy Backup | T1490 | #1 | ok |
| Suspicious New Service Creation | T1543 | #1, #7 | ambiguous |
| Suspicious Service Binary Directory | T1202 | #1 | ok |
| Suspicious Windows Service Tampering | T1489, T1685 | #1 | ambiguous |
| Shadow Copies Creation Using Operating Systems Utilities | T1003 | #1, #7 | ambiguous |
| Shadow Copies Deletion Using Operating Systems Utilities | T1070, T1490 | #1 | ok |
| Windows Shell/Scripting Processes Spawning Suspicious Programs | T1059, T1218 | #1, #7 | ambiguous |
| Process Creation Using Sysnative Folder | T1055 | #1, #7 | ambiguous |
| System File Execution Location Anomaly | T1036 | #1, #7 | ambiguous |
| Suspicious SYSTEM User Process Creation | T1003, T1027, T1134 | #1, #4, #7 | ambiguous |
| Suspicious SYSVOL Domain Group Policy Access | T1552 | #1, #4 | ambiguous |
| Tasks Folder Evasion | T1574 | #1, #7 | ambiguous |
| Malicious Windows Script Components File Execution by TAEF Detection | T1218 | #1, #7 | ambiguous |
| Malicious PE Execution by Microsoft Visual Studio Debugger | T1218 | #1, #7 | ambiguous |
| Suspicious Userinit Child Process | T1055 | #1, #7 | ambiguous |
| Suspicious Velociraptor Child Process | T1219 | #1, #7 | ambiguous |
| Usage Of Web Request Commands And Cmdlets | T1059 | #1, #7 | ambiguous |
| WhoAmI as Parameter | T1033 | #1 | ok |
| Execution via WorkFolders.exe | T1218 | #1, #7 | ambiguous |
| Suspect Svchost Activity | T1055 | #1, #7 | ambiguous |
| Suspicious Process Masquerading As SvcHost.EXE | T1036 | #1, #7 | ambiguous |
| Uncommon Svchost Command Line Parameter | T1036, T1055 | #1, #7 | ambiguous |
| Uncommon Svchost Parent Process | T1036 | #1, #7 | ambiguous |
| Permission Check Via Accesschk.EXE | T1069 | #1 | ok |
| Active Directory Database Snapshot Via ADExplorer | T1069, T1087, T1482 | #1 | ok |
| Suspicious Active Directory Database Snapshot Via ADExplorer | T1069, T1087, T1482 | #1 | ok |
| Procdump Execution | T1003, T1036 | #1, #7 | ambiguous |
| Potential SysInternals ProcDump Evasion | T1003, T1036 | #1, #7 | ambiguous |
| Potential LSASS Process Dump Via Procdump | T1003, T1036 | #1, #7 | ambiguous |
| Psexec Execution | T1021, T1569 | #1, #4, #7 | ambiguous |
| Suspicious Use of PsLogList | T1087 | #1 | ok |
| Sysinternals PsService Execution | T1543 | #1, #7 | ambiguous |
| Sysinternals PsSuspend Execution | T1543 | #1, #7 | ambiguous |
| Potential Binary Impersonating Sysinternals Tools | T1036, T1202, T1218 | #1, #7 | ambiguous |
| Sysprep on AppData Folder | T1059 | #1, #7 | ambiguous |
| Suspicious Execution of Systeminfo | T1082 | #1 | ok |
| Suspicious Recursive Takeown | T1222 | #1 | ok |
| Tap Installer Execution | T1048 | #1, #7 | ambiguous |
| Compressed File Creation Via Tar.EXE | T1560 | #1 | ok |
| Compressed File Extraction Via Tar.EXE | T1560 | #1 | ok |
| Loaded Module Enumeration Via Tasklist.EXE | T1003 | #1, #7 | ambiguous |
| Taskmgr as LOCAL_SYSTEM | T1036 | #1, #7 | ambiguous |
| New Process Created Via Taskmgr.EXE | T1036 | #1, #7 | ambiguous |
| Potentially Suspicious Command Targeting Teams Sensitive Files | T1528 | #1, #4, #9 | ambiguous |
| Suspicious TSCON Start as SYSTEM | T1219 | #1, #7 | ambiguous |
| Suspicious RDP Redirect Using TSCON | T1021, T1563 | #1, #4 | ambiguous |
| UAC Bypass Using ChangePK and SLUI | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using Disk Cleanup | T1548 | #1, #7 | ambiguous |
| Bypass UAC via CMSTP | T1218, T1548 | #1, #7 | ambiguous |
| CMSTP UAC Bypass via COM Object Access | T1218, T1548 | #1, #7 | ambiguous |
| UAC Bypass Tools Using ComputerDefaults | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using Consent and Comctl32 - Process | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using DismHost | T1548 | #1, #7 | ambiguous |
| Bypass UAC via Fodhelper.exe | T1548 | #1, #7 | ambiguous |
| UAC Bypass via Windows Firewall Snap-In Hijack | T1548 | #1, #7 | ambiguous |
| UAC Bypass via ICMLuaUtil | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using IDiagnostic Profile | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using IEInstal - Process | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using MSConfig Token Modification - Process | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using NTFS Reparse Point - Process | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using PkgMgr and DISM | T1548 | #1, #7 | ambiguous |
| Potential UAC Bypass Via Sdclt.EXE | T1548 | #1, #7 | ambiguous |
| TrustedPath UAC Bypass Pattern | T1548 | #1, #7 | ambiguous |
| UAC Bypass Abusing Winsat Path Parsing - Process | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using Windows Media Player - Process | T1548 | #1, #7 | ambiguous |
| Bypass UAC via WSReset.exe | T1548 | #1, #7 | ambiguous |
| UAC Bypass WSReset | T1548 | #1, #7 | ambiguous |
| Use of UltraVNC Remote Access Software | T1219 | #1, #7 | ambiguous |
| Suspicious UltraVNC Execution | T1021 | #1, #4 | ambiguous |
| User Shell Folders Registry Modification via CommandLine | T1112, T1547 | #1, #7 | ambiguous |
| Uncommon Userinit Child Process | T1037 | #1, #7 | ambiguous |
| Windows Credential Manager Access via VaultCmd | T1555 | #1, #4, #7 | ambiguous |
| Registry Modification Attempt Via VBScript | T1059, T1112 | #1, #7 | ambiguous |
| Verclsid.exe Runs COM Object | T1218 | #1, #7 | ambiguous |
| Virtualbox Driver Installation or Starting of VMs | T1564 | #1 | ok |
| Suspicious VBoxDrvInst.exe Parameters | T1112 | #1 | ok |
| Potential Persistence Via VMwareToolBoxCmd.EXE VM State Change Script | T1059 | #1, #7 | ambiguous |
| Suspicious Persistence Via VMwareToolBoxCmd.EXE VM State Change Script | T1059 | #1, #7 | ambiguous |
| VMToolsd Suspicious Child Process | T1059 | #1, #7 | ambiguous |
| Potentially Suspicious Child Process Of VsCode | T1202, T1218 | #1, #7 | ambiguous |
| Visual Studio Code Tunnel Execution | T1071, T1219 | #1, #7 | ambiguous |
| Renamed Visual Studio Code Tunnel Execution | T1071, T1219 | #1, #7 | ambiguous |
| Potential Binary Proxy Execution Via VSDiagnostics.EXE | T1218 | #1, #7 | ambiguous |
| Proxy Execution via Vshadow | T1202 | #1 | ok |
| Suspicious Vsls-Agent Command With AgentExtensionPath Load | T1218 | #1, #7 | ambiguous |
| Use of W32tm as Timer | T1124 | #1 | ok |
| All Backups Deleted Via Wbadmin.EXE | T1490 | #1 | ok |
| Windows Backup Deleted Via Wbadmin.EXE | T1490 | #1 | ok |
| Sensitive File Dump Via Wbadmin.EXE | T1003 | #1, #7 | ambiguous |
| File Recovery From Backup Via Wbadmin.EXE | T1490 | #1 | ok |
| Sensitive File Recovery From Backup Via Wbadmin.EXE | T1003 | #1, #7 | ambiguous |
| Potentially Suspicious WebDAV LNK Execution | T1059, T1204 | #1, #7, #9 | ambiguous |
| Chopper Webshell Process Pattern | T1018, T1033, T1087, T1505 | #1, #7 | ambiguous |
| Webshell Hacking Activity Patterns | T1018, T1033, T1087, T1505 | #1, #7 | ambiguous |
| Webshell Detection With Command Line Keywords | T1018, T1033, T1087, T1505 | #1, #7 | ambiguous |
| Suspicious Process By Web Server Process | T1190, T1505 | #1, #2, #7 | ambiguous |
| Webshell Tool Reconnaissance Activity | T1505 | #1, #7 | ambiguous |
| Potential Credential Dumping Via WER | T1003 | #1, #7 | ambiguous |
| Potential ReflectDebugger Content Execution Via WerFault.EXE | T1036 | #1, #7 | ambiguous |
| PPL Tampering Via WerFaultSecure | T1003, T1685 | #1, #7 | ambiguous |
| Suspicious Child Process Of Wermgr.EXE | T1036, T1055 | #1, #7 | ambiguous |
| Suspicious Where Execution | T1217 | #1 | ok |
| Enumerate All Information With Whoami.EXE | T1033 | #1 | ok |
| Whoami.EXE Execution From Privileged Process | T1033 | #1 | ok |
| Group Membership Reconnaissance Via Whoami.EXE | T1033 | #1 | ok |
| Whoami.EXE Execution With Output Option | T1033 | #1 | ok |
| Whoami.EXE Execution Anomaly | T1033 | #1 | ok |
| Security Privileges Enumeration Via Whoami.EXE | T1033 | #1 | ok |
| Add New Download Source To Winget | T1059 | #1, #7 | ambiguous |
| Add Insecure Download Source To Winget | T1059 | #1, #7 | ambiguous |
| Add Potential Suspicious New Download Source To Winget | T1059 | #1, #7 | ambiguous |
| Install New Package Via Winget Local Manifest | T1059 | #1, #7 | ambiguous |
| Winrar Compressing Dump Files | T1560 | #1 | ok |
| WinRAR Execution in Non-Standard Folder | T1560 | #1 | ok |
| AWL Bypass with Winrm.vbs and Malicious WsmPty.xsl/WsmTxt.xsl | T1216 | #1, #7 | ambiguous |
| Remote Code Execute via Winrm.vbs | T1216 | #1, #7 | ambiguous |
| Remote PowerShell Session Host Process (WinRM) | T1021, T1059 | #1, #4, #7 | ambiguous |
| Winrs Local Command Execution | T1021, T1218 | #1, #4, #7 | ambiguous |
| Potential Lateral Movement via Windows Remote Shell | T1021 | #1, #4 | ambiguous |
| Compress Data and Lock With Password for Exfiltration With WINZIP | T1560 | #1 | ok |
| Wlrmdr.EXE Uncommon Argument Or Child Process | T1218 | #1, #7 | ambiguous |
| WMI Backdoor Exchange Transport Agent | T1546 | #1, #7 | ambiguous |
| Password Set to Never Expire via WMI | T1047, T1098 | #1, #7 | ambiguous |
| WMI Persistence - Script Event Consumer | T1546 | #1, #7 | ambiguous |
| New ActiveScriptEventConsumer Created Via Wmic.EXE | T1546 | #1, #7 | ambiguous |
| Potential Windows Defender Tampering Via Wmic.EXE | T1047, T1685 | #1, #7 | ambiguous |
| New Process Created Via Wmic.EXE | T1047 | #1, #7 | ambiguous |
| Computer System Reconnaissance Via Wmic.EXE | T1047 | #1, #7 | ambiguous |
| Hardware Model Reconnaissance Via Wmic.EXE | T1047 | #1, #7 | ambiguous |
| Local Groups Reconnaissance Via Wmic.EXE | T1069 | #1 | ok |
| Windows Hotfix Updates Reconnaissance Via Wmic.EXE | T1047 | #1, #7 | ambiguous |
| Process Reconnaissance Via Wmic.EXE | T1047 | #1, #7 | ambiguous |
| Potential Product Reconnaissance Via Wmic.EXE | T1047 | #1, #7 | ambiguous |
| Potential Product Class Reconnaissance Via Wmic.EXE | T1047, T1082 | #1, #7 | ambiguous |
| Service Reconnaissance Via Wmic.EXE | T1047 | #1, #7 | ambiguous |
| Uncommon System Information Discovery Via Wmic.EXE | T1082 | #1 | ok |
| Potential Unquoted Service Path Reconnaissance Via Wmic.EXE | T1047 | #1, #7 | ambiguous |
| System Disk And Volume Reconnaissance Via Wmic.EXE | T1047, T1082 | #1, #7 | ambiguous |
| WMIC Remote Command Execution | T1047 | #1, #7 | ambiguous |
| Service Started/Stopped Via Wmic.EXE | T1047 | #1, #7 | ambiguous |
| Service Startup Type Change Via Wmic.EXE | T1047, T1685 | #1, #7 | ambiguous |
| Potential Remote SquiblyTwo Technique Execution | T1047, T1059, T1220 | #1, #7 | ambiguous |
| Registry Manipulation via WMI Stdregprov | T1012, T1047, T1112 | #1, #7 | ambiguous |
| Suspicious WMIC Execution Via Office Process | T1047, T1204, T1218 | #1, #7, #9 | ambiguous |
| Suspicious Process Created Via Wmic.EXE | T1047 | #1, #7 | ambiguous |
| Application Terminated Via Wmic.EXE | T1047 | #1, #7 | ambiguous |
| Application Removed Via Wmic.EXE | T1047 | #1, #7 | ambiguous |
| XSL Script Execution Via WMIC.EXE | T1047, T1059, T1220 | #1, #7 | ambiguous |
| WmiPrvSE Spawned A Process | T1047 | #1, #7 | ambiguous |
| Potential WMI Lateral Movement WmiPrvSE Spawned PowerShell | T1047, T1059 | #1, #7 | ambiguous |
| Suspicious WmiPrvSE Child Process | T1047, T1204, T1218 | #1, #7, #9 | ambiguous |
| UEFI Persistence Via Wpbbin - ProcessCreation | T1542 | #1, #7 | ambiguous |
| Potential Dropper Script Execution Via WScript/CScript/MSHTA | T1059 | #1, #7 | ambiguous |
| Cscript/Wscript Uncommon Script Extension Execution | T1059 | #1, #7 | ambiguous |
| WSL Child Process Anomaly | T1202, T1218 | #1, #7 | ambiguous |
| Installation of WSL Kali-Linux | T1059 | #1, #7 | ambiguous |
| WSL Kali-Linux Usage | T1202 | #1 | ok |
| Windows Binary Executed From WSL | T1202 | #1 | ok |
| Proxy Execution Via Wuauclt.EXE | T1218 | #1, #7 | ambiguous |
| Suspicious Windows Update Agent Empty Cmdline | T1036 | #1, #7 | ambiguous |
| Xwizard.EXE Execution From Non-Default Location | T1574 | #1, #7 | ambiguous |
| COM Object Execution via Xwizard.EXE | T1218 | #1, #7 | ambiguous |
| Potential Process Hollowing Activity | T1055 | #1, #7 | ambiguous |
| Potential Defense Evasion Via Raw Disk Access By Uncommon Tools | T1006 | #1 | ok |
| Windows Recall Feature Enabled - DisableAIDataAnalysis Value Deleted | T1113 | #1 | ok |
| Terminal Server Client Connection History Cleared - Registry | T1070, T1112 | #1 | ok |
| Removal of Potential COM Hijacking Registry Keys | T1112 | #1 | ok |
| RunMRU Registry Key Deletion - Registry | T1070 | #1 | ok |
| Creation of a Local Hidden User Account by Registry | T1136 | #1 | ok |
| UAC Bypass Via Wsreset | T1548 | #1, #7 | ambiguous |
| CMSTP Execution Registry Event | T1218 | #1, #7 | ambiguous |
| Disable Security Events Logging Adding Reg Key MiniNt | T1112, T1685 | #1 | ambiguous |
| Wdigest CredGuard Registry Modification | T1112 | #1 | ok |
| Esentutl Volume Shadow Copy Service Keys | T1003 | #1, #7 | ambiguous |
| Windows Credential Editor Registry | T1003 | #1, #7 | ambiguous |
| Registry Entries For Azorult Malware | T1112 | #1 | ok |
| Potential Qakbot Registry Activity | T1112 | #1 | ok |
| Path To Screensaver Binary Modified | T1546 | #1, #7 | ambiguous |
| Narrator's Feedback-Hub Persistence | T1547 | #1, #7 | ambiguous |
| NetNTLM Downgrade Attack - Registry | T1112, T1685 | #1 | ambiguous |
| New DLL Added to AppCertDlls Registry Key | T1546 | #1, #7 | ambiguous |
| New DLL Added to AppInit_DLLs Registry Key | T1546 | #1, #7 | ambiguous |
| Office Application Startup - Office Test | T1137 | #1, #7 | ambiguous |
| Registry Persistence Mechanisms in Recycle Bin | T1547 | #1, #7 | ambiguous |
| New PortProxy Registry Entry Added | T1090 | #1, #7 | ambiguous |
| RedMimicry Winnti Playbook Registry Manipulation | T1112 | #1 | ok |
| WINEKEY Registry Modification | T1547 | #1, #7 | ambiguous |
| Run Once Task Configuration in Registry | T1112 | #1 | ok |
| Shell Open Registry Keys Manipulation | T1546, T1548 | #1, #7 | ambiguous |
| Potential Credential Dumping Via LSASS SilentProcessExit Technique | T1003 | #1, #7 | ambiguous |
| Security Support Provider (SSP) Added to LSA Configuration | T1547 | #1, #7 | ambiguous |
| Sticky Key Like Backdoor Usage - Registry | T1546 | #1, #7 | ambiguous |
| Atbroker Registry Change | T1218, T1547 | #1, #7 | ambiguous |
| Suspicious Run Key from Download | T1547 | #1, #7 | ambiguous |
| DLL Load via LSASS | T1547 | #1, #7 | ambiguous |
| Suspicious Camera and Microphone Access | T1123, T1125 | #1 | ok |
| Registry Tampering by Potentially Suspicious Processes | T1059, T1112 | #1, #7 | ambiguous |
| Registry Persistence via Service in Safe Mode | T1564 | #1 | ok |
| Add Port Monitor Persistence in Registry | T1547 | #1, #7 | ambiguous |
| Allow RDP Remote Assistance Feature | T1112 | #1 | ok |
| Classes Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| Common Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| CurrentControlSet Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| CurrentVersion Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| CurrentVersion NT Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| Internet Explorer Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| Office Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| Session Manager Autorun Keys Modification | T1546, T1547 | #1, #7 | ambiguous |
| System Scripts Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| WinSock2 Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| Wow6432Node CurrentVersion Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| Wow6432Node Classes Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| Wow6432Node Windows NT CurrentVersion Autorun Keys Modification | T1547 | #1, #7 | ambiguous |
| New BgInfo.EXE Custom DB Path Registry Configuration | T1112 | #1 | ok |
| New BgInfo.EXE Custom VBScript Registry Configuration | T1112 | #1 | ok |
| New BgInfo.EXE Custom WMI Query Registry Configuration | T1112 | #1 | ok |
| Bypass UAC Using DelegateExecute | T1548 | #1, #7 | ambiguous |
| Bypass UAC Using Event Viewer | T1547 | #1, #7 | ambiguous |
| Bypass UAC Using SilentCleanup Task | T1548 | #1, #7 | ambiguous |
| Default RDP Port Changed to Non Standard Port | T1547 | #1, #7 | ambiguous |
| IE Change Domain Zone | T1137 | #1, #7 | ambiguous |
| ClickOnce Trust Prompt Tampering | T1112 | #1 | ok |
| Potential CobaltStrike Service Installations - Registry | T1021, T1543, T1569 | #1, #4, #7 | ambiguous |
| COM Hijack via Sdclt | T1546, T1548 | #1, #7 | ambiguous |
| CrashControl CrashDump Disabled | T1112, T1564 | #1 | ok |
| Security Event Logging Disabled via MiniNt Registry Key - Registry Set | T1112, T1685 | #1 | ambiguous |
| Service Binary in Suspicious Folder | T1112 | #1 | ok |
| Custom File Open Handler Executes PowerShell | T1202 | #1 | ok |
| Potential Registry Persistence Attempt Via DbgManagedDebugger | T1574 | #1, #7 | ambiguous |
| Potentially Suspicious Desktop Background Change Via Registry | T1112, T1491 | #1, #7 | ambiguous |
| DHCP Callout DLL Installation | T1112, T1574 | #1, #7 | ambiguous |
| Disable Administrative Share Creation at Startup | T1070 | #1 | ok |
| Disable Internal Tools or Feature in Registry | T1112 | #1 | ok |
| Disable Windows Security Center Notifications | T1112 | #1 | ok |
| Registry Disable System Restore | T1490 | #1 | ok |
| Windows Event Log Access Tampering Via Registry | T1112, T1547 | #1, #7 | ambiguous |
| Add DisallowRun Execution to Registry | T1112 | #1 | ok |
| DNS-over-HTTPS Enabled by Registry | T1112, T1140 | #1, #7 | ambiguous |
| New DNS ServerLevelPluginDll Installed | T1112, T1574 | #1, #7 | ambiguous |
| ETW Logging Disabled In .NET Processes - Sysmon Registry | T1112, T1685 | #1 | ambiguous |
| Directory Service Restore Mode(DSRM) Registry Value Tampering | T1556 | #1, #7 | ambiguous |
| Periodic Backup For System Registry Hives Enabled | T1113 | #1 | ok |
| Windows Recall Feature Enabled - Registry | T1113 | #1 | ok |
| Enabling COR Profiler Environment Variables | T1574 | #1, #7 | ambiguous |
| Change User Account Associated with the FAX Service | T1112 | #1 | ok |
| Change the Fax Dll | T1112 | #1 | ok |
| Registry Modification to Hidden File Extension | T1137 | #1, #7 | ambiguous |
| Displaying Hidden Files Feature Disabled | T1564 | #1 | ok |
| Registry Hide Function from User | T1112 | #1 | ok |
| New Root or CA or AuthRoot Certificate to Store | T1490 | #1 | ok |
| Lolbas OneDriveStandaloneUpdater.exe Proxy Download | T1105 | #1 | ok |
| RestrictedAdminMode Registry Value Tampering | T1112 | #1 | ok |
| Lsass Full Dump Request Via DumpType Registry Settings | T1003 | #1, #7 | ambiguous |
| NET NGenAssemblyUsageLog Registry Key Tamper | T1112 | #1 | ok |
| New Netsh Helper DLL Registered From A Suspicious Location | T1546 | #1, #7 | ambiguous |
| Potential Persistence Via Netsh Helper DLL - Registry | T1546 | #1, #7 | ambiguous |
| Potential Credential Dumping Attempt Using New NetworkProvider - REG | T1003 | #1, #7 | ambiguous |
| Potentially Suspicious ODBC Driver Registered | T1003 | #1, #7 | ambiguous |
| Trust Access Disable For VBApplications | T1112 | #1 | ok |
| Enable Microsoft Dynamic Data Exchange | T1559 | #1, #7 | ambiguous |
| Potential Persistence Via Outlook LoadMacroProviderOnBoot Setting | T1008, T1137, T1546 | #1, #7 | ambiguous |
| Outlook Macro Execution Without Warning Setting Enabled | T1008, T1137, T1546 | #1, #7 | ambiguous |
| Outlook EnableUnsafeClientMailRules Setting Enabled - Registry | T1112 | #1 | ok |
| Outlook Security Settings Updated - Registry | T1137 | #1, #7 | ambiguous |
| Macro Enabled In A Potentially Suspicious Document | T1112 | #1 | ok |
| Uncommon Microsoft Office Trusted Location Added | T1112 | #1 | ok |
| Office Macros Warning Disabled | T1112 | #1 | ok |
| MaxMpxCt Registry Value Changed | T1070 | #1 | ok |
| Potential Persistence Via AppCompat RegisterAppRestart Layer | T1546 | #1, #7 | ambiguous |
| Potential Persistence Via App Paths Default Property | T1546 | #1, #7 | ambiguous |
| Potential Persistence Using DebugPath | T1546 | #1, #7 | ambiguous |
| COM Object Hijacking Via Modification Of Default System CLSID Default Value | T1546 | #1, #7 | ambiguous |
| Potential COM Object Hijacking Via TreatAs Subkey - Registry | T1546 | #1, #7 | ambiguous |
| Potential PSFactoryBuffer COM Hijacking | T1546 | #1, #7 | ambiguous |
| Potential Persistence Via Custom Protocol Handler | T1112 | #1 | ok |
| Potential Persistence Via Event Viewer Events.asp | T1112 | #1 | ok |
| Potential Persistence Via GlobalFlags | T1546 | #1, #7 | ambiguous |
| Modification of IE Registry Settings | T1112 | #1 | ok |
| Potential Persistence Via Logon Scripts - Registry | T1037 | #1, #7 | ambiguous |
| Potential Persistence Via Visual Studio Tools for Office | T1137 | #1, #7 | ambiguous |
| Potential Persistence Via Outlook Home Page | T1112 | #1 | ok |
| Potential Persistence Via Outlook Today Page | T1112 | #1 | ok |
| Potential WerFault ReflectDebugger Registry Value Abuse | T1036 | #1, #7 | ambiguous |
| Potential Persistence Via Scrobj.dll COM Hijacking | T1546 | #1, #7 | ambiguous |
| Potential Persistence Via Shim Database Modification | T1546 | #1, #7 | ambiguous |
| Suspicious Shim Database Patching Activity | T1546 | #1, #7 | ambiguous |
| Potential Persistence Via Shim Database In Uncommon Location | T1546 | #1, #7 | ambiguous |
| Potential Persistence Via Excel Add-in - Registry | T1137 | #1, #7 | ambiguous |
| Registry Modification for OCI DLL Redirection | T1112, T1574 | #1, #7 | ambiguous |
| PowerShell as a Service in Registry | T1569 | #1, #7 | ambiguous |
| Suspicious PowerShell In Registry Run Keys | T1547 | #1, #7 | ambiguous |
| PowerShell Logging Disabled Via Registry Key Tampering | T1112, T1564 | #1 | ok |
| Potential Provisioning Registry Key Abuse For Binary Proxy Execution - REG | T1218 | #1, #7 | ambiguous |
| ETW Logging Disabled For rpcrt4.dll | T1112, T1685 | #1 | ambiguous |
| Potentially Suspicious Command Executed Via Run Dialog Box - Registry | T1059 | #1, #7 | ambiguous |
| ScreenSaver Registry Key Set | T1218 | #1, #7 | ambiguous |
| ServiceDll Hijack | T1543 | #1, #7 | ambiguous |
| ETW Logging Disabled For SCM | T1112, T1685 | #1 | ambiguous |
| Registry Explorer Policy Modification | T1112 | #1 | ok |
| Persistence Via New SIP Provider | T1553 | #1, #10 | ambiguous |
| Hiding User Account Via SpecialAccounts Registry Key | T1564 | #1 | ok |
| Activate Suppression of Windows Security Center Notifications | T1112 | #1 | ok |
| Potential PendingFileRenameOperations Tampering | T1036 | #1, #7 | ambiguous |
| Suspicious Printer Driver Empty Manufacturer | T1574 | #1, #7 | ambiguous |
| Registry Persistence via Explorer Run Key | T1547 | #1, #7 | ambiguous |
| New RUN Key Pointing to Suspicious Folder | T1547 | #1, #7 | ambiguous |
| Suspicious Space Characters in RunMRU Registry Path - ClickFix | T1027, T1204 | #1, #7, #9 | ambiguous |
| Suspicious Shell Open Command Registry Modification | T1546, T1548 | #1, #7 | ambiguous |
| Suspicious Space Characters in TypedPaths Registry Path - FileFix | T1027, T1204 | #1, #7, #9 | ambiguous |
| Modify User Shell Folders Startup Value | T1547 | #1, #7 | ambiguous |
| WFP Filter Added via Registry | T1569, T1685 | #1, #7 | ambiguous |
| Enable LM Hash Storage | T1112 | #1 | ok |
| Scheduled TaskCache Change by Uncommon Program | T1053 | #1, #7 | ambiguous |
| Potential Registry Persistence Attempt Via Windows Telemetry | T1053 | #1, #7 | ambiguous |
| RDP Sensitive Settings Changed to Zero | T1112 | #1 | ok |
| RDP Sensitive Settings Changed | T1112 | #1 | ok |
| New TimeProviders Registered With Uncommon DLL Name | T1547 | #1, #7 | ambiguous |
| COM Hijacking via TreatAs | T1546 | #1, #7 | ambiguous |
| UAC Bypass via Event Viewer | T1548 | #1, #7 | ambiguous |
| UAC Bypass via Sdclt | T1548 | #1, #7 | ambiguous |
| UAC Bypass Abusing Winsat Path Parsing - Registry | T1548 | #1, #7 | ambiguous |
| UAC Bypass Using Windows Media Player - Registry | T1548 | #1, #7 | ambiguous |
| UAC Disabled | T1548 | #1, #7 | ambiguous |
| UAC Notification Disabled | T1548 | #1, #7 | ambiguous |
| UAC Secure Desktop Prompt Disabled | T1548 | #1, #7 | ambiguous |
| VBScript Payload Stored in Registry | T1547 | #1, #7 | ambiguous |
| Execution DLL of Choice Using WAB.EXE | T1218 | #1, #7 | ambiguous |
| Wdigest Enable UseLogonCredential | T1112 | #1 | ok |
| Winlogon AllowMultipleTSSessions Enable | T1112 | #1 | ok |
| Winlogon Notify Key Logon Persistence | T1547 | #1, #7 | ambiguous |
| Sysmon Configuration Error | T1564 | #1 | ok |
| Sysmon Configuration Modification | T1564 | #1 | ok |
| WMI Event Subscription | T1546 | #1, #7 | ambiguous |
| Suspicious Encoded Scripts in a WMI Consumer | T1047, T1546 | #1, #7 | ambiguous |
| Suspicious Scripting in a WMI Consumer | T1059 | #1, #7 | ambiguous |
