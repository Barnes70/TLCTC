---
type: "term"
title: "SQL Injection"
description: "An implementation flaw where an attacker inserts malicious SQL statements into application queries through unvalidated input, enabling unauthorized database access."
resource: "tlctc:term:sql-injection"
tags:
  - "glossary"
---
# SQL Injection

An implementation flaw where an attacker inserts malicious SQL statements into application queries through unvalidated input, enabling unauthorized database access. In TLCTC: maps to `#2 Exploiting Server` — a coding flaw in server-side query building that creates an unintended data→code transition. SQL injection can lead to immediate Data Risk Events: `[DRE: C]` (data exfiltration), `[DRE: I]` (data modification), or `[DRE: Av]` (data deletion).

**Reference:** V1.9.1 §Definitions (#2), Buzz-Word Refinement

See also: Exploiting Server (#2), Implementation Flaw, Command Injection
