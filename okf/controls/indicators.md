---
type: "indicator-framework"
title: "Indicators: KRI, KCI, KPI, DCS"
description: "Strategic indicator hierarchy (KRI / KCI / KPI / DCS) for measuring the TLCTC × CSF control matrix."
resource: "tlctc:controls:indicators"
tags:
  - "controls"
  - "indicators"
  - "kri"
  - "kci"
  - "kpi"
  - "dcs"
---
# Indicators: KRI, KCI, KPI, DCS

The cluster × function matrix becomes measurable through a small hierarchy of strategic
indicators, each anchored to the organization's risk appetite. Source: application paper §10.

## KRI — Key Risk Indicators
Sit at the risk-event layer; measure *exposure to threat pressure* per cluster (incidents and
**near-misses**, where the threat materialized but a control held). Bounded directly by risk
appetite. Example: credential-stuffing volume (#4), malware execution attempts (#7), split
into blocked (near-miss) vs successful (incident).

## KCI — Key Control Indicators
Sit at the control-objectives layer; measure whether each matrix objective is achieved against
a risk-appetite-derived target.
- **Technical KCI** — state/coverage ("what *is* the posture?"): % privileged accounts with
  hardware MFA (#4), % endpoints with application allowlisting (#7).
- **Procedural KCI** — process performance ("how fast/well?"): mean time to patch critical CVEs
  (#1/#2), mean time to revoke compromised tokens (#4).

## KPI — Key Performance Indicators
The procedural KCIs viewed as process-performance measures; KPI is the performance facet of KCI,
not a separate fourth type. The strategic three-way split is: risk exposure (KRI), control state
(technical KCI), control performance (procedural KCI/KPI).

## DCS — Detection Coverage Score
`DCS = MTTD / Δt`. A control's performance is only sufficient *relative to attacker speed*. See
[/controls/effectiveness-model.md](/controls/effectiveness-model.md).
