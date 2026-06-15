---
type: "term"
title: "Living Off the Land / LOLBAS (Living Off the Land Binaries and Scripts)"
description: "An attack technique using only software functions and binaries already present on a (potentially compromised) system, invoked with legitimate inputs/parameters, without introducing foreign code initially."
resource: "tlctc:term:living-off-the-land-lolbas-living-off-the-land-binaries-and-scripts"
tags:
  - "glossary"
---
# Living Off the Land / LOLBAS (Living Off the Land Binaries and Scripts)

An attack technique using only software functions and binaries already present on a (potentially compromised) system, invoked with legitimate inputs/parameters, without introducing foreign code initially. Legitimate system binaries are used to execute attacker-controlled content. In TLCTC: the invocation of the legitimate binary may be `#1` (if no implementation flaw is exploited), while the execution of attacker-controlled content through it is `#7`. The sequence `#1 → #7` applies. Examples: Using cmd.exe, PowerShell, WMI, or Task Scheduler to execute attacker-controlled scripts.

**Reference:** §4.2.5 (R-EXEC, LOLBAS Clarification)
