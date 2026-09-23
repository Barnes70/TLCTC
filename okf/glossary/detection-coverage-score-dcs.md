---
type: "term"
title: "Detection Coverage Score (DCS)"
description: "A strategic indicator measuring the defender's timing adequacy relative to Attack Velocity, in two forms read on distributions rather than means (v2.6) : detection DCS d = TTD P90 / Δt and containment DCS c = TTC P90 / Δt , where TTD and TTC are the defender's time to detect and time to contain distributions at an edge, read at the 90th percentile."
resource: "tlctc:term:detection-coverage-score-dcs"
tags:
  - "glossary"
---
# Detection Coverage Score (DCS)

A strategic indicator measuring the defender's **timing adequacy** relative to Attack Velocity, in two forms read on distributions rather than means *(v2.6)*: detection `DCS_d = TTD_P90 / Δt` and containment `DCS_c = TTC_P90 / Δt`, where TTD and TTC are the defender's time-to-detect and time-to-contain distributions at an edge, read at the 90th percentile. Where Δt is itself a distribution it is read at a fast percentile (P10). It answers one question: does the defender act before the attacker completes the transition between two adjacent steps?

- **Score < 1.0:** the defender acts first (for `DCS_c`, the transition is stopped)
- **Score > 1.0:** the adversary completes the step first
- **`DCS_d < 1` with `DCS_c > 1`:** the step was seen but not stopped

The v2.0–v2.5 formula `DCS = MTTD / Δt` (mean time to detect) is the mean-based special case of `DCS_d` and remains valid where only means are available.

Example: If a ransomware group moves from #4 to #1 in 10 minutes and your SIEM alerts in 15 minutes at P90, DCS_d = 15/10 = 1.5, indicating systematic blindness requiring automation rather than analyst intervention.

*Scope note.* Despite the historical name, DCS measures timing adequacy, not coverage: it assumes the relevant activity is detectable at all. A detector with 10-second MTTD but low detection probability does not have good coverage merely because Δt is 60 seconds; detection probability and rule coverage must be assessed separately (see the application paper, Part B).

**Related reading:** [The Commit Is the CVE — silent fixes & the patch-gap collapse](https://www.tlctc.net/silent-fix-window.html)
