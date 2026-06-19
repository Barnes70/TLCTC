---
type: "mapping-set"
title: "Sigma rules → #7 Malware"
description: "79 Sigma rules entries mapped to TLCTC #7 Malware."
resource: "tlctc:mapping:sigma:cluster-7"
tags:
  - "mapping"
  - "sigma"
  - "cluster-7"
---
# Sigma rules → #7 Malware

> Source: SigmaHQ rules → TLCTC mapping (`mappings/sigma/`). Derived via ATT&CK technique mapping.

Mapped entries: **79**. Cluster: [#7 Malware](/clusters/cluster-7.md).

| Rule | Techniques | Cluster set | Status |
|---|---|---|---|
| Antivirus Hacktool Detection | T1204 | #7, #9 | ambiguous |
| Antivirus Ransomware Detection | T1486 | #7 | ok |
| AWS EFS Fileshare Mount Modified or Deleted | T1485 | #7 | ok |
| AWS EKS Cluster Created or Deleted | T1485 | #7 | ok |
| AWS KMS Imported Key Material Usage | T1486, T1608 | #7 | ambiguous |
| Suspicious Inbox Manipulation Rules | T1140 | #7 | ok |
| Microsoft 365 - Potential Ransomware Activity | T1486 | #7 | ok |
| Microsoft 365 - Unusual Volume of File Deletion | T1485 | #7 | ok |
| Microsoft 365 - User Restricted from Sending Email | T1199 | #7, #10 | ambiguous |
| Overwriting the File with Dev Zero or Null | T1485 | #7 | ok |
| Symlink Etc Passwd | T1204 | #7, #9 | ambiguous |
| Linux Base64 Encoded Pipe to Shell | T1140 | #7 | ok |
| Linux Base64 Encoded Shebang In CLI | T1140 | #7 | ok |
| DD File Overwrite | T1485 | #7 | ok |
| Suspicious Curl Change User Agents - Linux | T1071 | #7 | ok |
| Linux Shell Pipe to Shell | T1140 | #7 | ok |
| Triple Cross eBPF Rootkit Install Commands | T1014 | #7 | ok |
| Potential Base64 Decoded From Images | T1140 | #7 | ok |
| Cobalt Strike DNS Beaconing | T1071 | #7 | ok |
| DNS TXT Answer with Possible Execution Strings | T1071 | #7 | ok |
| Wannacry Killswitch Domain | T1071 | #7 | ok |
| Windows WebDAV User Agent | T1071 | #7 | ok |
| HackTool - BabyShark Agent Default URL Pattern | T1071 | #7 | ok |
| HackTool - CobaltStrike Malleable Profile Patterns - Proxy | T1071 | #7 | ok |
| HackTool - Empire UserAgent URI Combo | T1071 | #7 | ok |
| APT User Agent | T1071 | #7 | ok |
| Suspicious Base64 Encoded User-Agent | T1071 | #7 | ok |
| Crypto Miner User Agent | T1071 | #7 | ok |
| HTTP Request With Empty User Agent | T1071 | #7 | ok |
| Exploit Framework User Agent | T1071 | #7 | ok |
| Malware User Agent | T1071 | #7 | ok |
| Windows PowerShell User Agent | T1071 | #7 | ok |
| Suspicious User Agent | T1071 | #7 | ok |
| Potential Base64 Encoded User-Agent | T1071 | #7 | ok |
| MSSQL Destructive Query | T1485 | #7 | ok |
| Suspicious Cobalt Strike DNS Beaconing - DNS Client | T1071 | #7 | ok |
| External Disk Drive Or USB Storage Device Was Recognized By The System | T1091, T1200 | #7, #8 | ambiguous |
| DNS Query To Common Malware Hosting and Shortener Services | T1071 | #7 | ok |
| Suspicious Cobalt Strike DNS Beaconing - Sysmon | T1071 | #7 | ok |
| DNS Query To Visual Studio Code Tunnels Domain | T1071 | #7 | ok |
| File With Uncommon Extension Created By An Office Application | T1204 | #7, #9 | ambiguous |
| Suspicious Binaries and Scripts in Public Folder | T1204 | #7, #9 | ambiguous |
| Suspicious Appended Extension | T1486 | #7 | ok |
| Load Of RstrtMgr.DLL By A Suspicious Process | T1486, T1685 | #7 | ambiguous |
| Load Of RstrtMgr.DLL By An Uncommon Process | T1486, T1685 | #7 | ambiguous |
| HackTool - SILENTTRINITY Stager DLL Load | T1071 | #7 | ok |
| DotNET Assembly DLL Loaded Via Office Application | T1204 | #7, #9 | ambiguous |
| CLR DLL Loaded Via Office Applications | T1204 | #7, #9 | ambiguous |
| GAC DLL Loaded Via Office Applications | T1204 | #7, #9 | ambiguous |
| Microsoft Excel Add-In Loaded From Uncommon Location | T1204 | #7, #9 | ambiguous |
| Microsoft VBA For Outlook Addin Loaded Via Outlook | T1204 | #7, #9 | ambiguous |
| VBA DLL Loaded Via Office Application | T1204 | #7, #9 | ambiguous |
| Remote DLL Load Via Rundll32.EXE | T1204 | #7, #9 | ambiguous |
| Outbound Network Connection Initiated By Microsoft Dialer | T1071 | #7 | ok |
| PowerShell Decompress Commands | T1140 | #7 | ok |
| Powershell Detect Virtualization Environment | T1497 | #7 | ok |
| Change User Agents with WebRequest | T1071 | #7 | ok |
| Replace Desktop Wallpaper by Powershell | T1491 | #7 | ok |
| Deleted Data Overwritten Via Cipher.EXE | T1485 | #7 | ok |
| Portable Gpg.EXE Execution | T1486 | #7 | ok |
| HackTool - SILENTTRINITY Stager Execution | T1071 | #7 | ok |
| Suspicious Outlook Child Process | T1204 | #7, #9 | ambiguous |
| Suspicious Binary In User Directory Spawned From Office Application | T1204 | #7, #9 | ambiguous |
| Suspicious Reg Add BitLocker | T1486 | #7 | ok |
| Renamed Gpg.EXE Execution | T1486 | #7 | ok |
| Renamed Sysinternals Sdelete Execution | T1485 | #7 | ok |
| Arbitrary Shell Command Execution Via Settingcontent-Ms | T1204, T1566 | #7, #9 | ambiguous |
| Potential Suspicious Browser Launch From Document Reader Process | T1204 | #7, #9 | ambiguous |
| Potential Commandline Obfuscation Using Escape Characters | T1140 | #7 | ok |
| Suspicious ClickFix/FileFix Execution Pattern | T1204 | #7, #9 | ambiguous |
| Suspicious FileFix Execution Pattern | T1204 | #7, #9 | ambiguous |
| Suspicious LNK Command-Line Padding with Whitespace Characters | T1204 | #7, #9 | ambiguous |
| Potential File Overwrite Via Sysinternals SDelete | T1485 | #7 | ok |
| Visual Studio Code Tunnel Shell Execution | T1071 | #7 | ok |
| Visual Studio Code Tunnel Service Installation | T1071 | #7 | ok |
| FileFix - Command Evidence in TypedPaths | T1204 | #7, #9 | ambiguous |
| Potential Ransomware Activity Using LegalNotice Message | T1491 | #7 | ok |
| New Application in AppCompat | T1204 | #7, #9 | ambiguous |
| Potential ClickFix Execution Pattern - Registry | T1204 | #7, #9 | ambiguous |
