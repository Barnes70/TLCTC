---
type: "term"
title: "Time to Detect (TTD) / Time to Contain (TTC)"
description: "The distributions of elapsed time from an attack step to its detection (TTD) and to its containment (TTC) at a given edge of an attack path."
resource: "tlctc:term:time-to-detect-ttd-time-to-contain-ttc"
tags:
  - "glossary"
---
# Time to Detect (TTD) / Time to Contain (TTC)

The distributions of elapsed time from an attack step to its detection (TTD) and to its containment (TTC) at a given edge of an attack path. The Detection Coverage Score reads them at the 90th percentile — `DCS_d = TTD_P90 / Δt`, `DCS_c = TTC_P90 / Δt` — so that the score describes the slow tail an attacker can count on rather than an average that hides it. MTTD is the mean of TTD.

**Reference:** Core paper §7.2; application paper §10

See also: Detection Coverage Score (DCS), Attack Velocity (Δt), KCI (Key Control Indicator)
