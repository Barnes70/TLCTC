---
type: "term"
title: "Detection Coverage Score (DCS)"
description: "A strategic Key Performance Indicator (KPI) for measuring security effectiveness derived from Attack Velocity."
resource: "tlctc:term:detection-coverage-score-dcs"
tags:
  - "glossary"
---
# Detection Coverage Score (DCS)

A strategic Key Performance Indicator (KPI) for measuring security effectiveness derived from Attack Velocity. Formula: `DCS = (Mean Time to Detect) / (Attack Velocity Δt)`.

- **Score < 1.0:** Organization is faster than the adversary (Winning)
- **Score > 1.0:** Adversary completes the step before detection (Losing)

Example: If a ransomware group moves from #4 to #1 in 10 minutes and your SIEM alerts in 15 minutes, DCS = 15/10 = 1.5, indicating systematic blindness requiring automation rather than analyst intervention.

**Related reading:** [The Commit Is the CVE — silent fixes & the patch-gap collapse](https://www.tlctc.net/silent-fix-window.html)
