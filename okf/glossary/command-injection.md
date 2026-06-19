---
type: "term"
title: "Command Injection"
description: "An attack where an attacker injects operating system commands into an application that passes user input to a system shell."
resource: "tlctc:term:command-injection"
tags:
  - "glossary"
---
# Command Injection

An attack where an attacker injects operating system commands into an application that passes user input to a system shell. In TLCTC: maps to `#2 Exploiting Server` or `#3 Exploiting Client` per R-ROLE — this is an implementation flaw (failure to sanitize input) that creates an unintended data→code transition. The execution of the injected commands constitutes Foreign Executable Content, so the full sequence is typically `#2 → #7` or `#3 → #7`.

See also: Exploiting Server (#2), SQL Injection, Foreign Executable Content (FEC)
