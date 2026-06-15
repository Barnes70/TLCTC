---
type: "mapping-set"
title: "CWE weaknesses → #9 Social Engineering"
description: "8 CWE weaknesses entries mapped to TLCTC #9 Social Engineering."
resource: "tlctc:mapping:cwe:cluster-9"
tags:
  - "mapping"
  - "cwe"
  - "cluster-9"
---
# CWE weaknesses → #9 Social Engineering

> Source: MITRE CWE → TLCTC mapping (`mappings/mitre-cwe/`). AI-generated, human-reviewed; experimental.

Mapped entries: **8**. Cluster: [#9 Social Engineering](/clusters/cluster-9.md).

| CWE | Name | TLCTC | Verdict | Rationale |
|---|---|---|---|---|
| CWE-356 | Product UI does not Warn User of Unsafe Actions | #9 | Allowed | UI does not warn the user before performing an unsafe action (overwrite, dangerous download, irreversible change). Per ruling-2, this enables user-deception attacks. Decision tree -> #9. |
| CWE-357 | Insufficient UI Warning of Dangerous Operations | #9 | Allowed | UI warning for dangerous operations is missing or insufficient (low-contrast, easily-dismissed, after-the-fact). Per ruling-2 -> #9. |
| CWE-446 | UI Discrepancy for Security Feature | #9 | Allowed | UI presents inconsistent state for a security feature (icon shows secure when it isn't, or vice versa) — enables user deception. Per ruling-2 -> #9. |
| CWE-451 | User Interface (UI) Misrepresentation of Critical Information | #9 | Allowed | UI misrepresents critical security information (URL spoofing in address bar, certificate UI manipulation) — primary phishing/deception vector. Per ruling-2 -> #9. |
| CWE-655 | Insufficient Psychological Acceptability | #9 | Allowed-with-Review | Security mechanisms users find onerous get bypassed or worked around, increasing the surface for user-deception attacks. Per ruling-2 enabling-condition policy → #9. |
| CWE-1007 | Insufficient Visual Distinction of Homoglyphs Presented to User | #9 | Allowed | This weakness facilitates deception and phishing attacks (#9) by making malicious identifiers look legitimate. |
| CWE-1021 | Improper Restriction of Rendered UI Layers or Frames | #9 | Allowed | This vulnerability (Clickjacking) is primarily used to trick the user (#9) into performing actions they did not intend. |
| CWE-1022 | Use of Web Link to Untrusted Target with window.opener Access | #9 | Allowed | Allows a target site to redirect the referring page (Reverse Tabnabbing), mainly used for phishing (#9). |
