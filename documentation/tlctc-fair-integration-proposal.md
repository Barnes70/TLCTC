# FAIR Integration with TLCTC v2.3: Layer 4 Risk Quantification Proposal

**Author:** Bernhard Kreinz
**Framework Version:** TLCTC v2.3 / FAIR Model v3.0
**License:** CC BY 4.0

---

## Abstract

The FAIR (Factor Analysis of Information Risk) framework provides the industry's most rigorous methodology for quantifying information security risk in financial terms. However, FAIR lacks a structured cyber threat taxonomy and has no mechanism for modeling multi-step attack sequences, temporal dynamics, or domain boundary crossings. Conversely, TLCTC v2.3 provides precise cause-oriented threat classification with velocity annotations and boundary modeling, but does not extend into financial risk quantification.

This proposal defines **Layer 4** of the TLCTC JSON architecture: a machine-readable schema that bridges TLCTC attack path analysis (Layer 3) with FAIR risk quantification. Layer 4 introduces four TLCTC-specific enhancement factors — Sequence Complexity Factor (SCF), Compound Threat Multipliers (CTM), Velocity-Weighted Control Effectiveness (VWCE), and Path Variance Analysis (PVA) — and maps control effectiveness through the NIST Cybersecurity Framework 2.0 functions into FAIR-CAM's Controls Analytics Model.

The full JSON schema is available in the repository at [`json-schemas/layer-4/tlctc-fair-risk.schema.json`](../json-schemas/layer-4/tlctc-fair-risk.schema.json).

---

## 1. Motivation

### 1.1 FAIR's Strengths

FAIR (standardized as The Open Group O-RT 3.1 / O-RA 2.1, and extended by the FAIR Institute's FAIR Model v3.0, FAIR-CAM v1.0, and FAIR-MAM v1.0) provides:

- A decomposable risk ontology with well-defined mathematical relationships
- Calibrated estimation using probability distributions (Beta-PERT, lognormal)
- Monte Carlo simulation for loss exceedance curves and annualized loss exposure (ALE)
- Six Forms of Loss for structured financial impact assessment
- A Controls Analytics Model (FAIR-CAM) that maps controls to specific risk factors

### 1.2 FAIR's Limitations in Cyber Threat Modeling

- **No standardized threat taxonomy.** FAIR defines *Threat Event Frequency* and *Threat Capability* but does not prescribe how to categorize or decompose threat types. Analysts must bring their own taxonomy, leading to inconsistent scenario definitions across analyses.
- **Single-event model.** The FAIR ontology models a single loss event. Multi-step attack sequences — where an attacker chains phishing (#9) into credential theft (#4) into lateral movement (#1) — cannot be natively represented. Each step has different threat capability, resistance strength, and velocity characteristics.
- **No temporal dimension.** FAIR's Contact Frequency captures *how often* a threat agent encounters an asset, but not *how fast* an attack progresses between steps. A control that is highly effective when defenders have hours to respond may be structurally irrelevant when the transition happens in milliseconds.
- **No boundary modeling.** FAIR does not represent domain boundary crossings or responsibility sphere handoffs — critical for understanding where controls must be placed and who is accountable.
- **No cause-consequence separation.** FAIR's Loss Magnitude mixes the threat event with its outcome. TLCTC's axiom that threats are causes (clusters) and impacts are consequences (DREs) enables cleaner analysis.

### 1.3 The Integration Opportunity

TLCTC v2.3 addresses each of these gaps:

| FAIR Gap | TLCTC v2.3 Capability |
|---|---|
| No threat taxonomy | 10 non-overlapping clusters based on generic vulnerabilities |
| Single-event model | Multi-step attack path sequences with parallel execution |
| No temporal dimension | Attack Velocity (Δt) annotations, four Velocity Classes (VC-1 to VC-4) |
| No boundary modeling | Domain Boundary Operators, responsibility sphere mapping |
| Cause-consequence conflation | DRE tags separate outcomes from classification |

Layer 4 formalizes this integration as a JSON schema that references Layer 3 attack paths and enriches them with FAIR quantification data.

---

## 2. FAIR Ontology Reference

The complete FAIR risk decomposition tree, as defined by the Open Group O-RT 3.1 and the FAIR Institute's FAIR Model v3.0:

```
Risk
├── Loss Event Frequency (LEF)
│   ├── Threat Event Frequency (TEF)
│   │   ├── Contact Frequency (CF)
│   │   └── Probability of Action (PoA)
│   └── Susceptibility (Vuln)
│       ├── Threat Capability (TCap)
│       └── Resistance Strength (RS)
└── Loss Magnitude (LM)
    ├── Primary Loss Magnitude (PLM)
    │   └── [evaluated across 6 Forms of Loss]
    └── Secondary Loss (SL)
        ├── Secondary Loss Event Frequency (SLEF)
        └── Secondary Loss Magnitude (SLM)
            └── [evaluated across 6 Forms of Loss]
```

### 2.1 Factor Definitions

| Factor | Definition | Relationship |
|---|---|---|
| **Risk** | Probable frequency and magnitude of future loss | `LEF × LM` |
| **Loss Event Frequency (LEF)** | Probable frequency that a threat agent inflicts harm within a timeframe | `TEF × Susceptibility` |
| **Threat Event Frequency (TEF)** | Probable frequency that a threat agent acts against an asset | `CF × PoA` |
| **Contact Frequency (CF)** | Frequency of threat agent contact with the asset (physical or logical) | Input estimate |
| **Probability of Action (PoA)** | Probability the threat agent acts once contact occurs | Input estimate |
| **Susceptibility** | Probability a threat event becomes a loss event (0–1) | `P(TCap > RS)` |
| **Threat Capability (TCap)** | Level of force a threat agent can apply (0–100 percentile) | Input estimate |
| **Resistance Strength (RS)** | Control strength against a baseline unit of force (0–100 percentile) | Input estimate |
| **Loss Magnitude (LM)** | Total economic impact of a loss event | `PLM + SL` |
| **Primary Loss Magnitude (PLM)** | Direct costs from the loss event | Sum across Forms of Loss |
| **Secondary Loss (SL)** | Costs from secondary stakeholder reactions | `SLEF × SLM` |
| **Secondary Loss Event Frequency (SLEF)** | Probability secondary stakeholders react negatively | Input estimate |
| **Secondary Loss Magnitude (SLM)** | Economic cost of secondary reactions | Sum across Forms of Loss |

> **Terminology note:** FAIR Model v3.0 (January 2025) renamed "Vulnerability" to **"Susceptibility"** to avoid confusion with the narrower cybersecurity definition (CVEs, software flaws). The Open Group O-RT 3.1 retains "Vulnerability" as normative but acknowledges "Susceptibility" as a synonym. This proposal uses "Susceptibility" throughout.

### 2.2 Six Forms of Loss

Both Primary and Secondary Loss Magnitude are evaluated across these six forms, originally defined in O-RT and refined by FAIR-MAM:

| Form of Loss | Typical Classification | Definition |
|---|---|---|
| **Productivity** | Primary | Operational inability to deliver products or services |
| **Response** | Primary & Secondary | Costs of managing the event (investigation, legal, notification) |
| **Replacement** | Primary | Costs to repair or substitute affected assets |
| **Competitive Advantage** | Secondary | Losses from compromised IP or market differentiators |
| **Fines & Judgments** | Secondary | Civil, criminal, or contractual penalties |
| **Reputation** | Secondary | Diminished stakeholder perception and trust |

### 2.3 Distribution Specifications

FAIR uses calibrated estimation with Monte Carlo simulation. All inputs are probability ranges:

| Component | Distribution | Parameters | Notes |
|---|---|---|---|
| Frequency estimates | **Beta-PERT** | `minimum`, `most_likely` (mode), `maximum`, `confidence` (kurtosis, default=4) | Higher confidence = sharper peak around mode |
| Magnitude estimates | **Lognormal** | `low` (5th percentile), `high` (95th percentile) | Never below zero; long right tail for blowout losses |
| Event occurrence | **Poisson** | Mean derived from frequency estimate | Models event count per time period |
| TCap / RS | **Beta-PERT** | `minimum`, `most_likely`, `maximum`, `confidence` | Measured as percentiles (0–100) against full threat community |

The Layer 4 schema adopts these distribution specifications directly to ensure compatibility with existing FAIR tooling (RiskLens/Safe Security, Netflix riskquant, Open Group Risk Analysis Tool).

---

## 3. FAIR-Related Standards Landscape

The FAIR ecosystem now comprises several interrelated standards. Layer 4 integrates with the following:

| Standard | Version | Relevance to Layer 4 |
|---|---|---|
| **FAIR Model** (FAIR Institute) | v3.0 (Jan 2025) | Core risk decomposition ontology; Layer 4 implements this tree |
| **Open FAIR O-RT** (Open Group) | v3.1 (2025) | Normative risk taxonomy standard; aligned with NIST CSF 2.0 |
| **Open FAIR O-RA** (Open Group) | v2.1 (2025) | Risk analysis process guidance |
| **FAIR-CAM** (Controls Analytics Model) | v1.0 (Jan 2025) | Control effect classification; Layer 4 maps VWCE through FAIR-CAM |
| **FAIR-MAM** (Materiality Assessment Model) | v1.0 | 10-module loss magnitude expansion; Layer 4 references MAM modules |
| **FAIR-CRS** (Cyber Risk Scenario Taxonomy) | v1.0 (Feb 2025) | Scenario definition: Threat × Asset × Method × Effect |
| **NIST CSF** | v2.0 (Feb 2024) | 6 functions as top-level control objectives in Layer 4 |

---

## 4. Layer 4 Architecture

### 4.1 Position in the Three-Layer Architecture

Layer 4 extends the existing TLCTC JSON architecture:

```
Layer 1 (Static)     Framework dictionary — clusters, axioms, rules
Layer 2 (Context)    Reference registries — spheres, boundary contexts
Layer 3 (Dynamic)    Attack path instances — incident analyses
Layer 4 (Risk)       FAIR risk quantification — financial risk modeling   ← NEW
```

Layer 4 instances **reference** Layer 3 attack path instances (via `attack_path_ref` and optional SHA256 integrity hash) and enrich them with FAIR risk quantification data. A single Layer 3 attack path may have multiple Layer 4 risk assessments (e.g., different analysts, different threat communities, different asset valuations).

### 4.2 Schema Overview

The Layer 4 schema defines these top-level objects:

```json
{
  "metadata": { },
  "scenario": { },
  "fair_factors": { },
  "tlctc_enhancements": { },
  "control_analysis": { },
  "results": { },
  "extensions": { }
}
```

| Object | Purpose |
|---|---|
| `metadata` | Assessment identity, analyst, versioning, attack path reference |
| `scenario` | FAIR-CRS scenario definition (threat, asset, method, effect) |
| `fair_factors` | Full FAIR decomposition tree with distribution estimates |
| `tlctc_enhancements` | SCF, CTM, PVA — the TLCTC-specific risk factors |
| `control_analysis` | NIST CSF → FAIR-CAM → VWCE per-transition control effectiveness |
| `results` | Computed outputs: ALE, loss exceedance, enhanced risk score |
| `extensions` | Forward-compatibility |

---

## 5. Schema Specification

### 5.1 Metadata

```json
{
  "metadata": {
    "assessment_id": "FAIR-SCATTERED-SPIDER-2025-001",
    "analyst": "Security Risk Team",
    "analyst_confidence": "medium",
    "tlctc_version": "2.3",
    "fair_version": "3.0",
    "attack_path_ref": "scattered-spider-2024.json",
    "attack_path_sha256": "a1b2c3...",
    "framework_ref": "tlctc-framework.v2.3.json",
    "assessment_date": "2025-12-14T10:00:00Z",
    "time_horizon": "1y",
    "currency": "USD",
    "notes": "Risk assessment for identity-driven attack scenario",
    "extensions": {}
  }
}
```

**Required fields:** `assessment_id`, `analyst_confidence`, `tlctc_version`, `fair_version`, `attack_path_ref`, `assessment_date`, `time_horizon`, `currency`.

The `time_horizon` field specifies the period over which frequency estimates apply (ISO 8601 duration). The `currency` field uses ISO 4217 codes.

### 5.2 Scenario (FAIR-CRS)

Aligns with the FAIR Cyber Risk Scenario Taxonomy (February 2025):

```json
{
  "scenario": {
    "scenario_id": "SCATTERED-SPIDER-IDENTITY",
    "title": "Identity-driven attack via help desk social engineering",
    "threat_community": "Organized cybercriminal group (SCATTERED SPIDER)",
    "asset_at_risk": "Enterprise identity infrastructure and production data",
    "method": "Social engineering → credential theft → lateral movement → ransomware",
    "effect": "Data exfiltration and business interruption via ransomware",
    "attack_path_notation": "#9 ||[human][@External→@Org(HelpDesk)]|| →[Δt<1m] #4 →[Δt=2-5m] #1 →[Δt=hours] #4 →[Δt<24h] #7 + [DRE: C, A]",
    "notes": ""
  }
}
```

The `attack_path_notation` field captures the full TLCTC v2.3 notation string from the referenced Layer 3 instance for human readability. It is informational — the authoritative path data lives in the Layer 3 JSON.

### 5.3 FAIR Factors

The complete FAIR decomposition tree with calibrated distribution estimates:

```json
{
  "fair_factors": {
    "loss_event_frequency": {
      "threat_event_frequency": {
        "contact_frequency": {
          "distribution": "pert",
          "minimum": 1,
          "most_likely": 4,
          "maximum": 12,
          "confidence": 4,
          "unit": "events_per_year",
          "notes": "Help desk contact attempts by threat actors"
        },
        "probability_of_action": {
          "distribution": "pert",
          "minimum": 0.6,
          "most_likely": 0.85,
          "maximum": 0.95,
          "confidence": 4,
          "notes": "High motivation: organized crime with financial motive"
        }
      },
      "susceptibility": {
        "threat_capability": {
          "distribution": "pert",
          "minimum": 60,
          "most_likely": 80,
          "maximum": 95,
          "confidence": 3,
          "unit": "percentile",
          "notes": "Sophisticated threat actor with demonstrated social engineering expertise"
        },
        "resistance_strength": {
          "distribution": "pert",
          "minimum": 30,
          "most_likely": 50,
          "maximum": 70,
          "confidence": 3,
          "unit": "percentile",
          "notes": "Standard identity controls; help desk verification procedures in place but bypassable"
        }
      }
    },
    "loss_magnitude": {
      "primary_loss": {
        "distribution": "lognormal",
        "low": 500000,
        "high": 25000000,
        "unit": "USD",
        "forms_of_loss": {
          "productivity": {
            "distribution": "lognormal",
            "low": 200000,
            "high": 10000000,
            "notes": "Business interruption from ransomware deployment"
          },
          "response": {
            "distribution": "lognormal",
            "low": 150000,
            "high": 5000000,
            "notes": "Incident response, forensics, legal counsel"
          },
          "replacement": {
            "distribution": "lognormal",
            "low": 50000,
            "high": 2000000,
            "notes": "System rebuild and reimage costs"
          }
        }
      },
      "secondary_loss": {
        "secondary_loss_event_frequency": {
          "distribution": "pert",
          "minimum": 0.5,
          "most_likely": 0.8,
          "maximum": 1.0,
          "confidence": 4,
          "notes": "High probability of regulatory and media attention for ransomware event"
        },
        "secondary_loss_magnitude": {
          "distribution": "lognormal",
          "low": 1000000,
          "high": 50000000,
          "unit": "USD",
          "forms_of_loss": {
            "fines_and_judgments": {
              "distribution": "lognormal",
              "low": 500000,
              "high": 20000000,
              "notes": "GDPR, state breach notification penalties"
            },
            "reputation": {
              "distribution": "lognormal",
              "low": 200000,
              "high": 15000000,
              "notes": "Customer churn, brand damage"
            },
            "competitive_advantage": {
              "distribution": "lognormal",
              "low": 100000,
              "high": 10000000,
              "notes": "Exfiltrated proprietary data"
            }
          }
        }
      }
    }
  }
}
```

**Distribution objects** follow a consistent shape:

- **PERT distribution:** `{ "distribution": "pert", "minimum": N, "most_likely": N, "maximum": N, "confidence": N }`
- **Lognormal distribution:** `{ "distribution": "lognormal", "low": N, "high": N }` (5th and 95th percentiles)

All distributions include optional `unit` and `notes` fields.

### 5.4 TLCTC Enhancement Factors

These are the novel factors introduced by the TLCTC-FAIR integration. They derive from the Layer 3 attack path structure and modify the base FAIR calculation.

#### 5.4.1 Sequence Complexity Factor (SCF)

The SCF accounts for the fact that multi-step attack paths are harder to execute than single-step attacks. Longer sequences with diverse velocity classes require different attacker capabilities at each transition.

```json
{
  "tlctc_enhancements": {
    "sequence_complexity_factor": {
      "path_length": 5,
      "parallel_group_count": 0,
      "velocity_classes_observed": ["VC-2", "VC-3", "VC-4"],
      "velocity_variance": "high",
      "scf_value": 0.72,
      "notes": "Mixed VC-4/VC-3/VC-2 path. VC variance increases defender optionality but also indicates attacker must operate across multiple tempos."
    }
  }
}
```

**SCF interpretation:** Values < 1.0 reduce effective LEF (longer, more complex paths are less likely to complete). Values > 1.0 would indicate an amplification effect (e.g., well-rehearsed attack playbooks where sequence length adds no friction).

**Derivation:**

```
SCF = base_factor × (1 + log(path_length)) × velocity_variance_penalty
```

Where:
- `base_factor` — analyst-calibrated baseline (typically 0.8–1.0)
- `path_length` — number of sequential steps from the Layer 3 instance
- `velocity_variance_penalty` — adjustment for mixed velocity classes (higher variance = lower SCF, as the attacker must succeed across multiple tempo domains)

#### 5.4.2 Compound Threat Multipliers (CTM)

When TLCTC parallel groups `(#X + #Y)` appear in the attack path, the combined effect may differ from independent execution. CTM captures synergy or interference between parallel clusters.

```json
{
  "compound_threat_multipliers": [
    {
      "group_ref": "parallel-1",
      "clusters": ["#1", "#7"],
      "synergy_factor": 1.3,
      "rationale": "Function abuse (#1) combined with malware execution (#7) bypasses controls tuned to either threat independently. SIEM rules for #1 anomalies may not correlate with #7 FEC indicators.",
      "notes": ""
    }
  ]
}
```

**CTM interpretation:** `synergy_factor` of 1.0 = independent (no interaction). > 1.0 = synergistic (combined effect exceeds sum of parts). < 1.0 = interference (parallel execution creates noise that aids detection).

#### 5.4.3 Path Variance Analysis (PVA)

Multiple attack paths may achieve the same objective. PVA documents alternative paths with relative probabilities, enabling weighted risk aggregation.

```json
{
  "path_variance_analysis": [
    {
      "path_id": "primary",
      "attack_path_ref": "scattered-spider-2024.json",
      "notation": "#9 ||[human][@External→@Org(HelpDesk)]|| →[Δt<1m] #4 →[Δt=2-5m] #1 →[Δt=hours] #4 →[Δt<24h] #7 + [DRE: C, A]",
      "path_probability": 0.6,
      "notes": "Primary observed attack path"
    },
    {
      "path_id": "alternative-1",
      "attack_path_ref": null,
      "notation": "#9 ||[human][@External→@Org(IT)]|| →[Δt=1h] #4 →[Δt=30m] #1 →[Δt=2d] #7 + [DRE: C, A]",
      "path_probability": 0.25,
      "notes": "Alternative: targeting IT staff directly (slower, bypasses help desk controls)"
    },
    {
      "path_id": "alternative-2",
      "attack_path_ref": null,
      "notation": "#3 →[Δt=instant] #7 →[Δt=5m] #4 →[Δt=1h] #1 + [DRE: C, A]",
      "path_probability": 0.15,
      "notes": "Alternative: exploit-driven initial access without social engineering"
    }
  ]
}
```

**Weighted risk calculation:**

```
Total_Risk = Σ(Path_Risk_i × path_probability_i)
```

Path probabilities must sum to ≤ 1.0 (the remainder represents unknown/unmodeled paths).

### 5.5 Control Analysis: NIST CSF → FAIR-CAM → VWCE

This is the most novel aspect of the Layer 4 schema. Control effectiveness is organized in a three-tier hierarchy:

```
NIST CSF 2.0 Function          (strategic objective — what the control aims to achieve)
  └── FAIR-CAM Domain           (analytical category — how the control affects risk factors)
       └── FAIR-CAM Sub-domain  (mechanism — specific control mechanism)
            └── VWCE per VC     (velocity-weighted effectiveness — per-transition viability)
```

#### 5.5.1 NIST CSF 2.0 Functions as Control Objectives

The six NIST CSF 2.0 functions provide universally recognized strategic control objectives:

| NIST Function | Purpose | FAIR-CAM Mapping |
|---|---|---|
| **Govern (GV)** | Establish and monitor cybersecurity risk management strategy | Decision Support Controls, Variance Management Controls |
| **Identify (ID)** | Understand assets, risks, and improvement opportunities | Feeds FAIR scenario definition (asset/threat scoping) |
| **Protect (PR)** | Implement safeguards to manage risk | Loss Event Controls → Prevention (Avoidance, Deterrence, Resistance) |
| **Detect (DE)** | Find and analyze anomalous activity | Loss Event Controls → Detection (Visibility, Monitoring, Recognition) |
| **Respond (RS)** | Act regarding detected incidents | Loss Event Controls → Response (Containment) |
| **Recover (RC)** | Restore capabilities impaired by incidents | Loss Event Controls → Response (Recovery, Remediation) |

#### 5.5.2 FAIR-CAM Control Domains

Within each NIST function, FAIR-CAM v1.0 provides the analytical framework for understanding *how* controls affect risk factors:

**Loss Event Controls** (directly affect FAIR risk factors):

| Domain | Sub-domain | FAIR Factor Affected | NIST Function |
|---|---|---|---|
| **Prevention** | Avoidance | Reduces Contact Frequency (CF) | Protect |
| | Deterrence | Reduces Probability of Action (PoA) | Protect |
| | Resistance | Increases Resistance Strength (RS) | Protect |
| **Detection** | Visibility | Enables awareness of threat events | Detect |
| | Monitoring | Continuous observation capability | Detect |
| | Recognition | Identification of anomalies | Detect |
| **Response** | Containment | Limits loss spread (reduces LM) | Respond |
| | Recovery | Restores normal operations (reduces LM) | Recover |
| | Remediation | Addresses root causes (reduces future LEF) | Recover |

**Variance Management Controls** (indirectly affect risk via control reliability):

| Sub-domain | Purpose | NIST Function |
|---|---|---|
| Prevention of variance | Ensures controls operate as designed | Govern |
| Identification of variance | Detects when controls deviate from spec | Govern |
| Correction of variance | Remediates control drift | Govern |

**Decision Support Controls** (indirectly affect risk via decision quality):

| Purpose | NIST Function |
|---|---|
| Align organizational decisions with risk management objectives | Govern, Identify |

#### 5.5.3 Velocity-Weighted Control Effectiveness (VWCE)

The central insight of this integration: control effectiveness is not absolute — it varies by Velocity Class. A control that is highly effective when the attack transition takes days may be structurally irrelevant when the transition happens in milliseconds.

VWCE is captured **per transition** in the attack path, then rolled up to path-level and scenario-level effectiveness.

```json
{
  "control_analysis": {
    "transition_controls": [
      {
        "from_step": "s1-vishing",
        "to_step": "s2-account-takeover",
        "delta_t": "<1m",
        "velocity_class": "VC-4",
        "controls": [
          {
            "control_id": "ctrl-sat-01",
            "control_name": "Security Awareness Training",
            "nist_function": "PR",
            "fair_cam_domain": "prevention",
            "fair_cam_subdomain": "resistance",
            "fair_factor_affected": "resistance_strength",
            "base_effectiveness": 0.70,
            "vc_applicability": 0.10,
            "vwce": 0.07,
            "rationale": "Awareness training has high base effectiveness against #9, but at VC-4 velocity the human has <1 second to recognize and resist the social engineering attempt in a real-time phone call. The attack leverages urgency and authority cues that bypass trained responses.",
            "notes": ""
          },
          {
            "control_id": "ctrl-mfa-01",
            "control_name": "Multi-Factor Authentication",
            "nist_function": "PR",
            "fair_cam_domain": "prevention",
            "fair_cam_subdomain": "resistance",
            "fair_factor_affected": "resistance_strength",
            "base_effectiveness": 0.85,
            "vc_applicability": 0.30,
            "vwce": 0.255,
            "rationale": "MFA provides high resistance but the help desk reset process creates a bypass path. At VC-4, the attacker socially engineers the MFA reset before the legitimate user can respond.",
            "notes": ""
          },
          {
            "control_id": "ctrl-siem-01",
            "control_name": "SIEM Identity Anomaly Detection",
            "nist_function": "DE",
            "fair_cam_domain": "detection",
            "fair_cam_subdomain": "recognition",
            "fair_factor_affected": "detection_effectiveness",
            "base_effectiveness": 0.60,
            "vc_applicability": 0.05,
            "vwce": 0.03,
            "rationale": "SIEM detection at VC-4 is effectively zero — the transition completes before an alert can fire, be triaged, and trigger response.",
            "notes": ""
          }
        ]
      },
      {
        "from_step": "s2-account-takeover",
        "to_step": "s3-mfa-registration",
        "delta_t": "2-5m",
        "velocity_class": "VC-3",
        "controls": [
          {
            "control_id": "ctrl-edr-01",
            "control_name": "EDR / Endpoint Automation",
            "nist_function": "DE",
            "fair_cam_domain": "detection",
            "fair_cam_subdomain": "monitoring",
            "fair_factor_affected": "detection_effectiveness",
            "base_effectiveness": 0.80,
            "vc_applicability": 0.75,
            "vwce": 0.60,
            "rationale": "EDR/SOAR automation can detect and respond to suspicious MFA registration within minutes. VC-3 is within operational response window.",
            "notes": ""
          }
        ]
      }
    ],
    "scenario_level_summary": {
      "highest_risk_transition": {
        "from_step": "s1-vishing",
        "to_step": "s2-account-takeover",
        "velocity_class": "VC-4",
        "max_vwce": 0.255,
        "notes": "The #9→#4 transition at VC-4 is the critical vulnerability in this path. Only architectural controls (e.g., eliminating help desk password reset capability) are structurally effective."
      },
      "control_coverage_by_nist_function": {
        "GV": { "controls_count": 0, "avg_vwce": null },
        "ID": { "controls_count": 0, "avg_vwce": null },
        "PR": { "controls_count": 2, "avg_vwce": 0.163 },
        "DE": { "controls_count": 2, "avg_vwce": 0.315 },
        "RS": { "controls_count": 0, "avg_vwce": null },
        "RC": { "controls_count": 0, "avg_vwce": null }
      }
    }
  }
}
```

**VWCE calculation:**

```
VWCE(control, transition) = base_effectiveness × vc_applicability
```

Where:
- `base_effectiveness` — Control's inherent effectiveness irrespective of attack speed (0.0–1.0)
- `vc_applicability` — Factor reflecting whether the control can structurally operate at this Velocity Class (0.0–1.0)
- `vwce` — The velocity-weighted effective value (0.0–1.0)

**VWCE reference matrix** (general guidance for calibration):

| Control Type | VC-1 (Days+) | VC-2 (Hours) | VC-3 (Minutes) | VC-4 (Seconds) |
|---|---|---|---|---|
| Security Awareness Training | High (0.7–0.9) | Medium (0.4–0.6) | Low (0.1–0.3) | None (0.0–0.1) |
| SIEM Alerting / Analyst Triage | High (0.7–0.9) | High (0.7–0.9) | Low (0.1–0.3) | None (0.0–0.1) |
| EDR / SOAR Automation | High (0.8–1.0) | High (0.8–1.0) | High (0.7–0.9) | Medium (0.3–0.6) |
| Architectural Hardening | High (0.8–1.0) | High (0.8–1.0) | High (0.8–1.0) | High (0.7–0.9) |
| Supply Chain Verification | High (0.7–0.9) | Medium (0.4–0.6) | Low (0.1–0.3) | None (0.0–0.1) |

### 5.6 Results

Computed outputs from the FAIR+TLCTC analysis:

```json
{
  "results": {
    "annualized_loss_exposure": {
      "distribution": "lognormal",
      "low": 750000,
      "high": 35000000,
      "unit": "USD",
      "notes": "ALE incorporating SCF, CTM, and VWCE adjustments"
    },
    "enhanced_fair_risk_score": {
      "base_fair_ale": { "low": 1200000, "high": 45000000 },
      "scf_adjusted_ale": { "low": 864000, "high": 32400000 },
      "ctm_adjustment": null,
      "vwce_adjustment_factor": 0.82,
      "final_ale": { "low": 750000, "high": 35000000 },
      "notes": "SCF reduces LEF (5-step path). VWCE reveals that VC-4 transition at entry point degrades Protect controls significantly, partially offsetting SCF reduction."
    },
    "loss_exceedance_curve": [
      { "threshold": 1000000, "probability": 0.78 },
      { "threshold": 5000000, "probability": 0.52 },
      { "threshold": 10000000, "probability": 0.31 },
      { "threshold": 25000000, "probability": 0.12 },
      { "threshold": 50000000, "probability": 0.04 }
    ],
    "monte_carlo_iterations": 100000,
    "notes": ""
  }
}
```

**Final risk formula:**

```
Enhanced_FAIR_Risk = f(Base_FAIR_Risk, SCF, CTM, PVA, VWCE)
```

Specifically:

```
Adjusted_LEF = Base_LEF × SCF × Σ(CTM_i for all parallel groups)
Adjusted_LM  = Base_LM × VWCE_impact_factor
Total_Risk   = Σ(Adjusted_LEF_path_j × Adjusted_LM_path_j × path_probability_j)  for all PVA paths
```

---

## 6. VWCE Reference Matrix: Control Types by Velocity Class

This matrix provides calibration guidance for VWCE values. It maps control types to their structural viability at each Velocity Class. The mapping flows through the NIST CSF → FAIR-CAM hierarchy:

### 6.1 Protect (PR) → Prevention Controls

| Control | FAIR-CAM Sub-domain | FAIR Factor | VC-1 | VC-2 | VC-3 | VC-4 |
|---|---|---|---|---|---|---|
| Security Awareness Training | Resistance | RS | High | Medium | Low | None |
| Email/URL Filtering | Avoidance | CF | High | High | High | High |
| Network Segmentation | Avoidance | CF | High | High | High | High |
| MFA (standard) | Resistance | RS | High | High | Medium | Low |
| MFA (phishing-resistant / FIDO2) | Resistance | RS | High | High | High | High |
| Hardened Identity Verification | Resistance | RS | High | High | Medium | Low |
| Architecture / Zero Trust | Resistance | RS | High | High | High | High |

### 6.2 Detect (DE) → Detection Controls

| Control | FAIR-CAM Sub-domain | FAIR Factor | VC-1 | VC-2 | VC-3 | VC-4 |
|---|---|---|---|---|---|---|
| Threat Hunting | Recognition | Detection | High | Low | None | None |
| SIEM Alerting + Analyst | Recognition | Detection | High | High | Low | None |
| EDR Behavioral Detection | Monitoring | Detection | High | High | High | Medium |
| SOAR Automated Playbooks | Recognition | Detection | High | High | High | Medium |
| Canary Tokens / Honeypots | Visibility | Detection | High | High | High | High |

### 6.3 Respond (RS) → Response Controls

| Control | FAIR-CAM Sub-domain | FAIR Factor | VC-1 | VC-2 | VC-3 | VC-4 |
|---|---|---|---|---|---|---|
| Manual IR Procedures | Containment | LM | High | Medium | Low | None |
| Automated Containment (SOAR) | Containment | LM | High | High | High | Medium |
| Network Isolation / Kill Switch | Containment | LM | High | High | High | High |

### 6.4 Recover (RC) → Recovery Controls

| Control | FAIR-CAM Sub-domain | FAIR Factor | VC-1 | VC-2 | VC-3 | VC-4 |
|---|---|---|---|---|---|---|
| Backup & Restore | Recovery | LM | High | High | High | High |
| Disaster Recovery Plan | Recovery | LM | High | High | Medium | Low |
| Post-Incident Remediation | Remediation | Future LEF | High | High | High | High |

### 6.5 Govern (GV) → Variance & Decision Controls

| Control | FAIR-CAM Domain | FAIR Factor | VC-1 | VC-2 | VC-3 | VC-4 |
|---|---|---|---|---|---|---|
| Policy Compliance Monitoring | Variance Management | Control Reliability | High | High | Medium | Low |
| Risk-Informed Decision Making | Decision Support | All (indirect) | High | High | High | High |
| Control Testing & Validation | Variance Management | Control Reliability | High | High | High | High |

### 6.6 Identify (ID) — Scenario Inputs

Identify function controls do not directly map to FAIR-CAM's Loss Event Controls. Instead, they feed the FAIR scenario definition:

- **Asset Inventory** → defines `asset_at_risk` in the FAIR-CRS scenario
- **Risk Assessment Process** → calibrates FAIR factor estimates
- **Threat Intelligence** → informs Contact Frequency and Threat Capability estimates
- **Vulnerability Management** → informs Resistance Strength estimates

These are not rated on the VWCE matrix because they operate at the assessment level, not the transition level.

---

## 7. Worked Example: SCATTERED SPIDER

### 7.1 Attack Path (Layer 3 Reference)

```
#9 ||[human][@External→@Org(HelpDesk)]|| →[Δt<1m] #4 →[Δt=2-5m] #1 →[Δt=hours] #4 →[Δt<24h] #7 + [DRE: C, A]
```

| Step | Cluster | Δt to Next | VC | Description |
|---|---|---|---|---|
| 1 | #9 Social Engineering | <1m | VC-4 | Help desk vishing attack |
| 2 | #4 Identity Theft | 2–5m | VC-3 | Account takeover (credential use) |
| 3 | #1 Abuse of Functions | hours | VC-2 | MFA device registration, log deletion |
| 4 | #4 Identity Theft | <24h | VC-2 | Lateral credential theft (ntds.dit) |
| 5 | #7 Malware | — | — | Ransomware deployment + [DRE: C, A] |

### 7.2 Key VWCE Insight

The critical transition is **Step 1 → Step 2** (#9 → #4) at **VC-4 velocity**:

- Security Awareness Training: `VWCE = 0.70 × 0.10 = 0.07` — **structurally ineffective**
- MFA (standard): `VWCE = 0.85 × 0.30 = 0.255` — **degraded** (help desk bypass)
- MFA (phishing-resistant FIDO2): `VWCE = 0.90 × 0.90 = 0.81` — **structurally effective** (cannot be socially engineered)
- SIEM alerting: `VWCE = 0.60 × 0.05 = 0.03` — **structurally ineffective** at this speed

**Conclusion:** Only architectural controls (phishing-resistant MFA, eliminating help desk password reset, zero trust architecture) are structurally viable at the entry point. This directly informs FAIR's Resistance Strength estimate and investment prioritization.

### 7.3 SCF Application

```
path_length = 5
velocity_classes = [VC-4, VC-3, VC-2, VC-2]
velocity_variance = high (3 distinct VCs)
SCF = 0.85 × (1 + log(5)) × 0.65 ≈ 0.72
```

Interpretation: The 5-step path with high velocity variance reduces effective LEF by ~28%. The attacker must operate across real-time, operational, and tactical tempos — each requiring different capabilities.

### 7.4 Enhanced Risk Calculation

```
Base LEF (FAIR):     ~3.4 events/year
SCF-adjusted LEF:    3.4 × 0.72 ≈ 2.45 events/year
Base LM (FAIR):      $500K–$25M primary + $1M–$50M secondary
VWCE impact:         VC-4 entry degrades Protect controls → higher effective susceptibility
Enhanced ALE:        $750K–$35M (90% confidence interval)
```

---

## 8. Schema File

The complete JSON Schema (Draft 7) for Layer 4 is maintained at:

```
json-schemas/layer-4/tlctc-fair-risk.schema.json
```

It follows the same conventions as Layers 1–3:
- JSON Schema Draft 7 (`http://json-schema.org/draft-07/schema#`)
- `additionalProperties: false` throughout
- Explicit `required` arrays
- `extensions` fields for forward-compatibility
- Internal `$ref` pointers to `#/definitions`

---

## 9. Integration with Existing FAIR Tooling

Layer 4 is designed for compatibility with the FAIR tool ecosystem:

| Tool | Integration Path |
|---|---|
| **Netflix riskquant** (Python) | Extract `fair_factors` distributions → feed to `simpleloss.py` or `pertloss.py` |
| **Open Group Risk Analysis Tool** (Excel) | Map `fair_factors` to spreadsheet inputs; `results` match output format |
| **RiskLens / Safe Security** (SaaS) | Export Layer 4 `scenario` + `fair_factors` as scenario inputs |
| **evaluator** (R) | Map Layer 4 distributions to evaluator's OpenFAIR-compliant data frames |
| **Monte Carlo engines** | `fair_factors` distributions are directly simulable (PERT → frequency, lognormal → magnitude, Poisson → event count) |

---

## 10. Future Work

- **FAIR-MAM integration:** Expand `forms_of_loss` to align with FAIR-MAM's 10 modules / 26 subcategories for more granular loss estimation.
- **Automated SCF/VWCE derivation:** Tooling to automatically compute SCF from Layer 3 path structure and suggest VWCE calibration ranges from the reference matrix.
- **Control portfolio optimization:** Use VWCE data across multiple scenarios to identify the control investment portfolio that maximizes risk reduction per dollar at observed velocity classes.
- **FAIR-TAM integration:** Extend Layer 4 to support third-party risk scenarios, mapping vendor-crossing boundaries (Layer 3 transit operators) to FAIR-TAM's third-party assessment factors.

---

## References

- The Open Group. *Open FAIR Risk Taxonomy (O-RT)*, v3.1 (2025).
- The Open Group. *Open FAIR Risk Analysis (O-RA)*, v2.1 (2025).
- FAIR Institute. *FAIR Model Standard Artifact*, v3.0, January 2025.
- FAIR Institute. *FAIR Controls Analytics Model (FAIR-CAM)*, v1.0, January 2025.
- FAIR Institute. *FAIR Materiality Assessment Model (FAIR-MAM)*, v1.0.
- FAIR Institute. *Cyber Risk Scenario Taxonomy (FAIR-CRS)*, February 2025.
- NIST. *Cybersecurity Framework (CSF)*, v2.0, February 2024.
- TLCTC Framework. *TLCTC v2.0 Whitepaper*. tlctc.net.
- CrowdStrike. *2025 Global Threat Report* (attack velocity benchmarks).
