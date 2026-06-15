---
type: "mapping-set"
title: "Sigma rules → #3 Exploiting Client"
description: "7 Sigma rules entries mapped to TLCTC #3 Exploiting Client."
resource: "tlctc:mapping:sigma:cluster-3"
tags:
  - "mapping"
  - "sigma"
  - "cluster-3"
---
# Sigma rules → #3 Exploiting Client

> Source: SigmaHQ rules → TLCTC mapping (`mappings/sigma/`). Derived via ATT&CK technique mapping.

Mapped entries: **7**. Cluster: [#3 Exploiting Client](/clusters/cluster-3.md).

| Rule | Techniques | Cluster set | Status |
|---|---|---|---|
| Download From Suspicious TLD - Blacklist | T1203, T1204, T1566 | #3, #7, #9 | ambiguous |
| Download From Suspicious TLD - Whitelist | T1203, T1204, T1566 | #3, #7, #9 | ambiguous |
| Cross Site Scripting Strings | T1189 | #3, #7 | ambiguous |
| Network Connection Initiated By Eqnedt32.EXE | T1203 | #3, #7 | ambiguous |
| Office Application Initiated Network Connection To Non-Local IP | T1203 | #3, #7 | ambiguous |
| Java Running with Remote Debugging | T1203 | #3, #7 | ambiguous |
| Potentially Suspicious Child Process Of WinRAR.EXE | T1203 | #3, #7 | ambiguous |
