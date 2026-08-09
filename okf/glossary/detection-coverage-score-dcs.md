---
type: "term"
title: "Detection Coverage Score (DCS)"
description: "A strategic Key Performance Indicator (KPI) measuring detection timing adequacy relative to Attack Velocity."
resource: "tlctc:term:detection-coverage-score-dcs"
tags:
  - "glossary"
---
# Detection Coverage Score (DCS)

A strategic Key Performance Indicator (KPI) measuring **detection timing adequacy** relative to Attack Velocity. Formula: `DCS = (Mean Time to Detect) / (Attack Velocity Δt)`. It answers one question: is detection latency shorter than the attacker's progression window between two adjacent steps?

- **Score < 1.0:** Detection is faster than the adversary's progression (the response window exists)
- **Score > 1.0:** Adversary completes the step before detection (no response window)

Example: If a ransomware group moves from #4 to #1 in 10 minutes and your SIEM alerts in 15 minutes, DCS = 15/10 = 1.5, indicating systematic blindness requiring automation rather than analyst intervention.

*Scope note.* Despite the historical name, DCS measures timing adequacy, not coverage: it assumes the relevant activity is detectable at all. A detector with 10-second MTTD but low detection probability does not have good coverage merely because Δt is 60 seconds; detection probability and rule coverage must be assessed separately (see the application paper, Part B).

**Related reading:** [The Commit Is the CVE — silent fixes & the patch-gap collapse](https://www.tlctc.net/silent-fix-window.html)
