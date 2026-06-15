---
type: "mapping-set"
title: "Sigma rules → #2 Exploiting Server"
description: "55 Sigma rules entries mapped to TLCTC #2 Exploiting Server."
resource: "tlctc:mapping:sigma:cluster-2"
tags:
  - "mapping"
  - "sigma"
  - "cluster-2"
---
# Sigma rules → #2 Exploiting Server

> Source: SigmaHQ rules → TLCTC mapping (`mappings/sigma/`). Derived via ATT&CK technique mapping.

Mapped entries: **55**. Cluster: [#2 Exploiting Server](/clusters/cluster-2.md).

| Rule | Techniques | Cluster set | Status |
|---|---|---|---|
| Django Framework Exceptions | T1190 | #2 | ok |
| Potential JNDI Injection Exploitation In JVM Based Application | T1190 | #2 | ok |
| Potential Local File Read Vulnerability In JVM Based Application | T1190 | #2 | ok |
| Potential OGNL Injection Exploitation In JVM Based Application | T1190 | #2 | ok |
| Process Execution Error In JVM Based Application | T1190 | #2 | ok |
| Potential XXE Exploitation Attempt In JVM Based Application | T1190 | #2 | ok |
| Potential RCE Exploitation Attempt In NodeJS | T1190 | #2 | ok |
| OpenCanary - HTTP GET Request | T1190 | #2 | ok |
| OpenCanary - HTTP POST Login Attempt | T1190 | #2 | ok |
| Python SQL Exceptions | T1190 | #2 | ok |
| Ruby on Rails Framework Exceptions | T1190 | #2 | ok |
| Spring Framework Exceptions | T1190 | #2 | ok |
| Potential SpEL Injection In Spring Framework | T1190 | #2 | ok |
| Suspicious SQL Error Messages | T1190 | #2 | ok |
| Potential Server Side Template Injection In Velocity | T1190 | #2 | ok |
| Ingress/Egress Security Group Modification | T1190 | #2 | ok |
| LoadBalancer Security Group Modification | T1190 | #2 | ok |
| RDS Database Security Group Modification | T1190 | #2 | ok |
| Possible Coin Miner CPU Priority Param | T1068 | #2, #3, #7 | ambiguous |
| Guacamole Two Users Sharing Session Anomaly | T1212 | #2, #3, #4 | ambiguous |
| Buffer Overflow Attempts | T1068 | #2, #3, #7 | ambiguous |
| Suspicious OpenSSH Daemon Error | T1190 | #2 | ok |
| Suspicious Named Error | T1190 | #2 | ok |
| Suspicious VSFTPD Error Messages | T1190 | #2 | ok |
| Linux Sudo Chroot Execution | T1068 | #2, #3, #7 | ambiguous |
| OMIGOD SCX RunAsProvider ExecuteScript | T1068, T1190, T1203 | #2, #3, #7 | ambiguous |
| OMIGOD SCX RunAsProvider ExecuteShellCommand | T1068, T1190, T1203 | #2, #3, #7 | ambiguous |
| Apache Threading Error | T1190, T1210 | #2 | ok |
| F5 BIG-IP iControl Rest API Command Execution - Proxy | T1190 | #2 | ok |
| Hack Tool User Agent | T1110, T1190 | #2, #4 | ambiguous |
| F5 BIG-IP iControl Rest API Command Execution - Webserver | T1190 | #2 | ok |
| Successful IIS Shortname Fuzzing Scan | T1190 | #2 | ok |
| Java Payload Strings | T1190 | #2 | ok |
| JNDIExploit Pattern | T1190 | #2 | ok |
| Path Traversal Exploitation Attempts | T1190 | #2 | ok |
| SQL Injection Strings In URI | T1190 | #2 | ok |
| Suspicious User-Agents Related To Recon Tools | T1190 | #2 | ok |
| Microsoft Malware Protection Engine Crash | T1211, T1685 | #2, #3, #7 | ambiguous |
| Audit CVE Event | T1068, T1203, T1210, T1211, T1212, T1499 | #2, #3, #4, #6, #7 | ambiguous |
| Microsoft Malware Protection Engine Crash - WER | T1211, T1685 | #2, #3, #7 | ambiguous |
| Failed Logon From Public IP | T1078, T1133, T1190 | #2, #4 | ambiguous |
| Kerberos Manipulation | T1212 | #2, #3, #4 | ambiguous |
| Zerologon Exploitation Using Well-known Tools | T1210 | #2 | ok |
| DNS Query Request By QuickAssist.EXE | T1071, T1210 | #2, #7 | ambiguous |
| Process Explorer Driver Creation By Non-Sysinternals Binary | T1068 | #2, #3, #7 | ambiguous |
| Process Monitor Driver Creation By Non-Sysinternals Binary | T1068 | #2, #3, #7 | ambiguous |
| HKTL - SharpSuccessor Privilege Escalation Tool Execution | T1068 | #2, #3, #7 | ambiguous |
| HackTool - SharpWSUS/WSUSpendu Execution | T1210 | #2 | ok |
| HackTool - SysmonEOP Execution | T1068 | #2, #3, #7 | ambiguous |
| Suspicious SysAidServer Child | T1210 | #2 | ok |
| Remote Access Tool - ScreenConnect Server Web Shell Execution | T1190 | #2 | ok |
| Suspicious NTLM Authentication on the Printer Spooler Service | T1212 | #2, #3, #4 | ambiguous |
| Suspicious Spool Service Child Process | T1068, T1203 | #2, #3, #7 | ambiguous |
| Terminal Service Process Spawn | T1190, T1210 | #2 | ok |
| Suspicious Processes Spawned by WinRM | T1190 | #2 | ok |
