---
type: "mapping-set"
title: "Sigma rules → #5 Man in the Middle"
description: "9 Sigma rules entries mapped to TLCTC #5 Man in the Middle."
resource: "tlctc:mapping:sigma:cluster-5"
tags:
  - "mapping"
  - "sigma"
  - "cluster-5"
---
# Sigma rules → #5 Man in the Middle

> Source: SigmaHQ rules → TLCTC mapping (`mappings/sigma/`). Derived via ATT&CK technique mapping.

Mapped entries: **9**. Cluster: [#5 Man in the Middle](/clusters/cluster-5.md).

| Rule | Techniques | Cluster set | Status |
|---|---|---|---|
| RottenPotato Like Attack Pattern | T1557 | #5 | ok |
| Potential Kerberos Coercion by Spoofing SPNs via DNS Manipulation | T1557 | #5 | ok |
| Local Privilege Escalation Indicator TabTip | T1557 | #5 | ok |
| Notepad++ Updater DNS Query to Uncommon Domains | T1195, T1557 | #5, #10 | ambiguous |
| Uncommon File Created by Notepad++ Updater Gup.EXE | T1195, T1557 | #5, #10 | ambiguous |
| Suspicious Child Process of Notepad++ Updater - GUP.Exe | T1195, T1557 | #5, #10 | ambiguous |
| HackTool - ADCSPwn Execution | T1557 | #5 | ok |
| HackTool - Impacket Tools Execution | T1557 | #5 | ok |
| Potential SMB Relay Attack Tool Execution | T1557 | #5 | ok |
