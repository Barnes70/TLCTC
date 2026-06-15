---
type: "effectiveness-model"
title: "Control Effectiveness Model (CDE → COE → ECR, DCS)"
description: "Three-layer control effectiveness model: CDE_max, CDE_fitness, COE, ECR, and the Detection Coverage Score."
resource: "tlctc:controls:effectiveness-model"
tags:
  - "controls"
  - "effectiveness"
  - "dcs"
  - "metrics"
---
# Control Effectiveness Model

The TLCTC Control Matrix assesses each control in three layers and combines them into a
single **Effective Control Rating (ECR)**. The model lives in the Control Matrix tool
(`tools/control-matrix.html`); this document summarizes it for agent consumption.

## Three layers

- **CDE_max** — *Design effectiveness ceiling* (0.00–0.99, never 1.0): the theoretical
  prevention/detection limit of the control by design. No control is perfect.
- **CDE_fitness** — *Velocity fitness* (factor 1.0 / 0.5 / 0.0): whether the control can
  structurally act within the cell's attack-velocity (Δt) window.
- **COE** — *Operational effectiveness*: measured performance from typed metrics
  (coverage, currency, mode, configuration, performance).

```
ECR = COE × CDE_max × fitness_factor
```

## Cell aggregation

- **Essential** controls set a **worst-of floor**.
- **Complementary** controls add a probabilistic **ceiling raise**.
- **Cell ECR = floor + raise.**
- **Residual ceiling gap = 1.0 − cell CDE_max composite** — risk that operations cannot
  close, only new control *types* or explicit acceptance can.

## Detection Coverage Score (DETECT cells)

```
DCS = MTTD / Δt
```

| DCS | Verdict |
|---|---|
| < 0.5 | effective |
| 0.5–0.8 | adequate |
| 0.8–1.0 | marginal |
| 1.0–2.0 | ineffective |
| > 2.0 | structurally failed |

The same MTTD can be effective or ineffective depending on the Δt of the transition being
defended — see [/controls/indicators.md](/controls/indicators.md) and
[velocity classes](/glossary/velocity-class.md).

## Worked example (DETECT × #7 Malware)

EDR (behavioral): CDE_max 0.85 (misses novel fileless techniques), fitness 1.0 (acts within
seconds, VC-3), COE 0.97 (active-agent coverage) → **ECR ≈ 0.82**. Combined in the DE×#7 cell
with SIEM correlation and sandbox detonation as complementary controls to raise the ceiling.
Source: `tools/control-matrix-starter.json`.
