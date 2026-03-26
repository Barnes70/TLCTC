&nbsp;

&nbsp;

# TLCTC JSON Architecture

## Standardized Threat Intelligence Sharing — v2.0

&nbsp;

**Bernhard Kreinz**

&nbsp;

March 2026

&nbsp;

---

&nbsp;

## Abstract

Organizations need a standardized way to share threat intelligence that separates universal framework definitions from specific attack instances. This guide explains the TLCTC JSON architecture that enables worldwide threat intelligence sharing while maintaining consistency and precision.

This document is a **companion** to the *TLCTC v2.0 White Paper*, which defines the normative schemas (Chapter 7). Here we provide:

- A conceptual overview of the layered architecture
- The **Three-Lane Conceptual Model** for attack analysis (Attack Path, Data Risk, Business Risk)
- A **Threat Intelligence Extension Profile** that enriches the minimal v2.0 base schema with software, CVEs, MITRE mappings, evidence, and business impacts
- A fully worked **SolarWinds SUNBURST** example in v2.0 format
- Practical guidance for SOC teams, threat intelligence analysts, and risk managers

> **Normative authority:** The JSON Schema definitions in the white paper (Chapter 7, Sections 7.3–7.5) are normative. This guide is informative and illustrative. Where any conflict exists, the white paper prevails.

---

&nbsp;

## 1. Understanding the Architecture

The TLCTC framework operates on two distinct but interconnected layers:

### Framework Layer (Static)

- Universal threat taxonomy (10 clusters)
- Cluster definitions and axioms
- Generic vulnerabilities
- Framework rules and notation (e.g., R-EXEC)
- Velocity class definitions

**Purpose:** Common language everyone uses.
**Changes:** Rarely (framework evolution).

### Intelligence Layer (Dynamic)

- Specific attack instances
- Software versions and CVEs
- Timeline and actor TTPs
- Domain boundaries (responsibility spheres)
- Impact assessment

**Purpose:** Actual threat intelligence.
**Changes:** Constantly (new incidents).

---

&nbsp;

## 2. The Three-Lane Conceptual Model

TLCTC attack path analysis operates across **three interconnected analytical lanes**. The JSON architecture captures all three lanes and their relationships:

```
┌─────────────────────────────────────────────────────────────┐
│  BUSINESS RISK            [Lane 3]                          │
│  Business impacts linked to steps/DREs                      │
│  JSON: extensions.ti.business_impacts[]                     │
├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤
│  DATA RISK                [Lane 2]                          │
│  DREs (C/I/A) linked to specific steps                      │
│  JSON: outcomes[] + extensions.ti.data_risk_events[]        │
├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤
│  ATTACK PATH              [Lane 1]                          │
│  Clusters, velocity, boundaries, @Spheres                   │
│  JSON: path_sequence[]                                      │
└─────────────────────────────────────────────────────────────┘
```

### Cross-Lane Linkage

- **Attack → Data:** Each step MAY carry `outcomes` tags (`C`, `I`, `A`) recording what data impacts occurred. The TI extension profile adds full `data_risk_events[]` objects with volume, data type, and timestamps.
- **Data → Business:** Each business impact MUST reference either a step (`linked_to_step`) or DRE (`linked_to_dre`).
- **Vertical causality:** The upward arrows represent causal relationships captured through these explicit links.

### Why Three Lanes Matter

A single attack step can simultaneously:
1. Exploit a generic vulnerability (Lane 1 — e.g., `#4` Identity Theft)
2. Cause a data risk event (Lane 2 — e.g., Loss of Confidentiality of credentials)
3. Trigger a business impact (Lane 3 — e.g., regulatory notification obligation)

The three-lane model keeps these dimensions linked but distinct, preventing the conflation of threats with outcomes that Axiom III prohibits.

---

&nbsp;

## 3. File Architecture Overview

The TLCTC JSON architecture is organized into three layers, matching the white paper's Chapter 7 structure:

```
┌─────────────────────────────────────────────────────────────┐
│                     FRAMEWORK LAYER                         │
│                  (Universal and Static)                      │
│                                                             │
│  tlctc-framework.schema.json        Validation schema       │
│  tlctc-framework.v2.0.json          Content package         │
│    ├─ Cluster definitions (#1–#10)                          │
│    ├─ Axioms (I–X)                                          │
│    ├─ Rules (R-EXEC, ...)                                   │
│    └─ Topology types (internal / bridge)                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          ↓ referenced by
┌─────────────────────────────────────────────────────────────┐
│                   REFERENCE DATA LAYER                      │
│              (Semi-Static / Customizable)                    │
│                                                             │
│  tlctc-reference.schema.json        Validation schema       │
│  @Org-registry.v1.0.0.json          Content package         │
│    ├─ Responsibility spheres (@Org, @Vendor, ...)           │
│    └─ Boundary contexts (human, physical, update, ...)      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          ↓ validates
┌─────────────────────────────────────────────────────────────┐
│                    INTELLIGENCE LAYER                        │
│              (Dynamic / Instance-Specific)                   │
│                                                             │
│  tlctc-attack-path.schema.json      Validation schema       │
│  incident-<id>.json                 Content instance         │
│    ├─ Ordered attack path sequence                          │
│    ├─ Boundary annotations per step                         │
│    ├─ Velocity Δt between steps                             │
│    ├─ Outcome tags (C/I/A)                                  │
│    └─ extensions.ti { ... }         TI enrichment data      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### JSON Structure Overview

| JSON File | Purpose | Scope | Update Frequency |
|---|---|---|---|
| `tlctc-framework.v2.0.json` | Core framework definitions | Universal | Rarely (framework updates) |
| `@Org-registry.vX.Y.Z.json` | Domain boundary definitions | Customizable | Occasionally (org changes) |
| `tlctc-attack-path.schema.json` | Validation schema for instances | Universal | Rarely (schema evolution) |
| `incident-<id>.json` | Specific attack instance | Per-incident | Per incident |

---

&nbsp;

## 4. Layer 1 — Framework Definition

> The normative schema is defined in the white paper, Section 7.3. This section provides context.

This is the foundation — the universal taxonomy that everyone references. It contains the threat cluster definitions, axioms, and framework rules.

### Key Purpose

Provides the common language for threat classification. Every organization references the same framework package, ensuring consistency in threat intelligence sharing.

### Cluster Properties (v2.0)

Each cluster in `tlctc-framework.v2.0.json` carries:

| Field | Description |
|---|---|
| `strategic_id` | `#1` through `#10` |
| `operational_root_id` | `TLCTC-XX.00` format |
| `name` | Cluster name |
| `definition` | Canonical definition |
| `attackers_view` | "I abuse..." statement |
| `generic_vulnerability` | The root weakness exploited |
| `topology` | `internal` or `bridge` |
| `operational_sub_threats` | Optional TLCTC-XX.YY refinements |

### Cluster Quick Reference

| # | Name | Topology | Generic Vulnerability |
|---|---|---|---|
| #1 | Abuse of Functions | internal | Trust, scope, and complexity designed into software functionality |
| #2 | Exploiting Server | internal | Server-side implementation flaws |
| #3 | Exploiting Client | internal | Client-side implementation flaws |
| #4 | Identity Theft | internal | Weak binding between identity and authentication artifacts |
| #5 | Man in the Middle | internal | Communication paths observable/alterable by intermediary |
| #6 | Flooding Attack | internal | Finite system capacity |
| #7 | Malware | internal | Environments execute attacker-controlled code/content |
| #8 | Physical Attack | bridge | Physical accessibility of hardware and facilities |
| #9 | Social Engineering | bridge | Humans can be influenced into unsafe actions |
| #10 | Supply Chain Attack | bridge | Trust in third-party components can be subverted |

### Notation Systems

TLCTC v2.0 supports two notation tiers:

| Tier | Format | Use Case |
|---|---|---|
| Strategic | `#X` (e.g., `#1`, `#10`) | Executive communication, risk assessment, governance |
| Operational | `TLCTC-XX.YY` (e.g., `TLCTC-01.00`, `TLCTC-02.02`) | Tool integration, automation, SIEM rules |

Both tiers are valid values for the `cluster` field in attack path instances.

### Attack Path Notation Rules

| Notation | Meaning | Example |
|---|---|---|
| `#X → #Y → #Z` | Sequential progression | `#9 → #4 → #1` |
| `(#X + #Y)` | Parallel/simultaneous execution | `(#1 + #7)` |
| `Δt` value | Velocity between steps | `→ [Δt=15m] →` |
| `\|\|[context][@Source→@Target]\|\|` | Boundary crossing | `\|\|[update][@Vendor→@Org]\|\|` |

### Common Attack Patterns

| Pattern Name | Notation | Description |
|---|---|---|
| Phishing to malware | `#9 → #3 → #7` | Social engineering delivers client exploit leading to FEC execution |
| Phishing to credentials | `#9 → #4` | Social engineering leads to credential misuse |
| Exploit to malware | `#2 → #7` or `#3 → #7` | Implementation flaw enables FEC execution |
| LOLBAS execution | `#1 → #7` | Function abuse enables foreign code execution |
| Supply chain | `#X → ... → #10 → #7` | Third-party trust exploited to deliver malware |

---

&nbsp;

## 5. Layer 2 — Reference Registry (Responsibility Spheres)

> The normative schema is defined in the white paper, Section 7.4. This section provides an expanded reference set.

Defines the domain boundaries where responsibility and control shift during an attack. This layer is semi-static and can be customized per organization.

### Why This Matters

Understanding where an attack crosses domain boundaries is critical for incident response, forensics, and legal responsibility. The "sphere" tells you whose assets, whose controls, and whose responsibility is involved at each step.

### Recommended Responsibility Spheres

The following set provides broad coverage. Organizations should customize based on their environment.

| Sphere ID | Name | Description |
|---|---|---|
| `@External` | External / Attacker Side | Infrastructure controlled by the threat actor or external parties |
| `@Public` | Public Infrastructure | Internet backbone, DNS, public cloud services, public repositories |
| `@Vendor` | Third Party / Vendor | Infrastructure and services provided by trusted third parties |
| `@Org-Perimeter` | Organization Perimeter | Boundary between external and internal (firewalls, DMZ, VPN, email gateways) |
| `@Org` | Organization Internal | Internal corporate network and systems |
| `@Org-Admin` | Privileged / Admin Level | High-privilege administrative systems and accounts |
| `@Customer` | Customer / End User Side | End-user or customer-controlled environment (user devices, home networks) |

> **Note:** When `@Vendor` is compromised, `#10` Supply Chain often marks the boundary transition in the attack path.

### Sphere Transition Patterns

Common patterns of how attacks move between spheres:

| Pattern | Path | Description |
|---|---|---|
| External to Internal | `@External → @Org-Perimeter → @Org` | Classic network breach |
| Supply Chain Compromise | `@External → @Vendor → @Org` | Attack via trusted third party |
| Phishing Entry | `@External → @Customer → @Org` | Social engineering via end user |
| Privilege Escalation | `@Org → @Org-Admin` | Internal movement to admin access |

### Boundary Contexts

Boundary contexts label the *type* of trust or domain crossing:

| Context | Description | Typical Clusters |
|---|---|---|
| `human` | Social engineering vector | `#9` |
| `physical` | Physical security crossing | `#8` |
| `update` | Software updates, patches | `#10` |
| `dev` | CI/CD, software supply chain | `#10` |
| `auth` | Authentication/federation, SSO | `#4`, `#10` |
| `runtime` | Managed services, SaaS control planes | `#10` |
| `admin` | Admin/management plane access | `#1`, `#10` |

### Example Registry: `@Org-registry.v1.0.0.json`

```json
{
  "metadata": {
    "registry_id": "@Org-registry",
    "registry_version": "1.0.0",
    "created_at": "2026-03-01T10:00:00Z",
    "owner": "Security Architecture",
    "notes": "Default registry with recommended sphere set."
  },
  "spheres": [
    { "sphere_id": "@External",       "description": "Attacker-controlled infrastructure",         "typical_domain": "third-party" },
    { "sphere_id": "@Public",          "description": "Public infrastructure (DNS, CDN, repos)",    "typical_domain": "third-party" },
    { "sphere_id": "@Vendor",          "description": "Vendor-managed assets or services",          "typical_domain": "third-party" },
    { "sphere_id": "@Org-Perimeter",   "description": "Organization perimeter (DMZ, gateways)",     "typical_domain": "cyber" },
    { "sphere_id": "@Org",             "description": "Primary organization internal systems",      "typical_domain": "cyber" },
    { "sphere_id": "@Org-Admin",       "description": "Privileged / admin-level systems",           "typical_domain": "cyber" },
    { "sphere_id": "@Customer",        "description": "Customer / end-user environment",            "typical_domain": "human" }
  ],
  "boundary_contexts": [
    { "context": "human",    "description": "Human decision / manipulation boundary (bridge by #9)" },
    { "context": "physical", "description": "Physical domain boundary (bridge by #8)" },
    { "context": "update",   "description": "Third-party update / dependency boundary (bridge by #10)" },
    { "context": "dev",      "description": "Build / CI/CD responsibility boundary" },
    { "context": "auth",     "description": "Identity provider / authentication boundary" },
    { "context": "runtime",  "description": "Managed services / SaaS control plane boundary" },
    { "context": "admin",    "description": "Admin / management plane access boundary" }
  ]
}
```

---

&nbsp;

## 6. Layer 3 — Attack Path Instances

> The normative schema is defined in the white paper, Section 7.5. This section explains practical usage.

Attack path instances are the actual threat intelligence — specific attacks that happened. This is what organizations share with each other.

### Base Schema Recap

The v2.0 base schema (`tlctc-attack-path.schema.json`) keeps each step deliberately minimal:

```json
{
  "step_id": "s1",
  "cluster": "#9",
  "topology_boundary": {
    "context": "human",
    "source_sphere": "@External",
    "target_sphere": "@Org"
  },
  "fec_executed": false,
  "outcomes": ["C"],
  "delta_t_to_next": "2h",
  "evidence_refs": ["TICKET-1234"],
  "notes": "Phishing email delivered to user.",
  "extensions": {}
}
```

This minimal structure ensures:
- Every tool can parse and validate the base fields
- Classification is unambiguous (one cluster per step)
- Boundary crossings are explicit
- R-EXEC compliance is machine-verifiable

### Velocity Notation (Δt)

The `delta_t_to_next` field uses a constrained format:

| Value | Meaning |
|---|---|
| `instant` | No measurable delay |
| `?` | Unknown |
| `15m` | 15 minutes |
| `~2h` | Approximately 2 hours |
| `<5m` | Less than 5 minutes |
| `~6mo` | Approximately 6 months |

### Velocity Classes

Attack velocity determines which defensive modes are structurally viable:

| Class | Name | Typical Δt | Defense Mode |
|---|---|---|---|
| VC-1 | Strategic | Days to months | Log retention, threat hunting, strategic monitoring |
| VC-2 | Tactical | Hours | SIEM alerting, analyst triage, guided response |
| VC-3 | Operational | Minutes | SOAR/EDR automation, rapid containment |
| VC-4 | Real-Time | Seconds to milliseconds | Architecture, circuit breakers, rate limits |

> **Key insight:** If the critical transition is VC-3 or faster, purely human response is structurally insufficient.

### Parallel Groups

When two or more steps execute simultaneously, wrap them in a `parallel_group`:

```json
{
  "mode": "parallel",
  "group_id": "g1",
  "steps": [
    { "step_id": "s4a", "cluster": "#1", "notes": "Abuse of functions." },
    { "step_id": "s4b", "cluster": "#7", "fec_executed": true, "notes": "Parallel malware execution." }
  ],
  "delta_t_to_next": "?",
  "notes": "Represents (#1 + #7)."
}
```

Member steps inside a `parallel_group` MUST NOT define `delta_t_to_next`; the transition time belongs to the group.

### Boundary Annotations

In v2.0, boundary crossings are annotated **on the step where the domain changes** — not as standalone boundary-only entries. Use the `topology_boundary` object:

```json
{
  "step_id": "s3",
  "cluster": "#7",
  "topology_boundary": {
    "context": "update",
    "source_sphere": "@Vendor",
    "target_sphere": "@Org"
  },
  "fec_executed": true,
  "notes": "Malware executes in customer environment via trusted update channel."
}
```

This captures the equivalent of the notation `||[update][@Vendor→@Org]||` directly on the step.

---

&nbsp;

## 7. Threat Intelligence Extension Profile

The v2.0 base schema is intentionally minimal to ensure broad interoperability. For rich threat intelligence sharing, this section defines a **standard extension profile** using the `extensions` object that the base schema reserves at both step and document level.

All enrichment fields live under `extensions.ti` (Threat Intelligence namespace).

### 7.1 Step-Level Extensions

Each `attack_step` may carry the following under `extensions.ti`:

```json
{
  "step_id": "s1",
  "cluster": "#10",
  "delta_t_to_next": "~6mo",
  "outcomes": ["C"],
  "notes": "Build pipeline compromised.",
  "extensions": {
    "ti": {
      "sphere": "@Vendor",
      "stage": "initial",
      "velocity_class": "VC-1",

      "software": [
        {
          "name": "SolarWinds Orion Build Environment",
          "version": "N/A",
          "vendor": "SolarWinds",
          "role": "vulnerability-source",
          "cpe": "cpe:2.3:a:solarwinds:orion_platform:*"
        }
      ],

      "vulnerabilities": {
        "cves": ["CVE-2020-10148"],
        "cwes": ["CWE-506"],
        "description": "Attackers compromised the SolarWinds build environment."
      },

      "mitre_mapping": {
        "tactics": ["TA0001"],
        "techniques": ["T1195.002"]
      },

      "temporal": {
        "date": "2019-09-01",
        "duration_minutes": 525600,
        "detection_date": "2020-12-13",
        "detection_gap_days": 470
      },

      "data_risk_events": [
        {
          "dre_id": "dre-1",
          "type": "C",
          "description": "Build pipeline source code and signing keys exposed.",
          "data_type": "source code",
          "volume": "Entire Orion build system"
        }
      ],

      "evidence": {
        "iocs": [
          { "type": "hash", "value": "b91ce2fa41029f6955bff20079468448" }
        ],
        "artifacts": ["Compromised build server logs", "Modified build scripts"],
        "log_sources": ["SolarWinds build system logs", "Version control system"]
      }
    }
  }
}
```

### Step-Level Extension Field Reference

| Field | Type | Description |
|---|---|---|
| `sphere` | string | Responsibility sphere for this step (e.g., `@Org`, `@Vendor`) |
| `stage` | enum | `initial`, `intermediate`, or `final` |
| `velocity_class` | enum | `VC-1`, `VC-2`, `VC-3`, or `VC-4` |
| `software[]` | array | Software components involved |
| `software[].name` | string | Software name |
| `software[].version` | string | Version number or range |
| `software[].vendor` | string | Software vendor/publisher |
| `software[].role` | enum | `target`, `attack-tool`, `dual-use-tool`, `legitimate-tool-abused`, `malware`, `exploit-delivery`, `vulnerability-source` |
| `software[].cpe` | string | Common Platform Enumeration identifier |
| `vulnerabilities.cves[]` | array | CVE identifiers (pattern: `CVE-YYYY-NNNNN`) |
| `vulnerabilities.cwes[]` | array | CWE identifiers (pattern: `CWE-NNN`) |
| `vulnerabilities.description` | string | Description of the vulnerability |
| `mitre_mapping.tactics[]` | array | MITRE ATT&CK tactic IDs (pattern: `TAXXXX`) |
| `mitre_mapping.techniques[]` | array | MITRE ATT&CK technique IDs (pattern: `TXXXX` or `TXXXX.XXX`) |
| `temporal.date` | date | Date the step occurred |
| `temporal.time` | time | Time the step occurred |
| `temporal.duration_minutes` | integer | Duration of this step |
| `temporal.detection_date` | date | When this step was detected |
| `temporal.detection_gap_days` | integer | Days between occurrence and detection |
| `data_risk_events[]` | array | Full DRE objects (richer than base `outcomes` tags) |
| `data_risk_events[].dre_id` | string | Unique identifier for cross-referencing |
| `data_risk_events[].type` | enum | `C` (Confidentiality), `I` (Integrity), `A` (Availability) |
| `data_risk_events[].description` | string | What data was affected and how |
| `data_risk_events[].data_type` | string | Type of data (PII, credentials, IP, etc.) |
| `data_risk_events[].volume` | string | Estimated volume |
| `data_risk_events[].timestamp` | datetime | When the DRE occurred |
| `evidence.iocs[]` | array | Indicators of Compromise |
| `evidence.iocs[].type` | enum | `ip`, `domain`, `url`, `hash`, `email`, `filename` |
| `evidence.iocs[].value` | string | The indicator value |
| `evidence.artifacts[]` | array | Artifact descriptions |
| `evidence.log_sources[]` | array | Log sources that recorded this step |

### 7.2 Document-Level Extensions

At the root level of the instance document, `extensions.ti` carries:

```json
{
  "metadata": { "..." : "..." },
  "path_sequence": [ "..." ],
  "extensions": {
    "ti": {
      "threat_actor": {
        "name": "APT29",
        "aliases": ["Cozy Bear", "The Dukes", "YTTRIUM", "UNC2452"],
        "type": "nation-state",
        "motivation": "espionage",
        "sophistication": "expert",
        "attribution_confidence": "high"
      },

      "attack_path_notation": "#10 → #7 → #7 ||[update][@Vendor→@Org]|| → #7 → #4 → #1 → #4 ||[auth][@Org→@Cloud]|| → #1 → #1",

      "business_impacts": [
        {
          "impact_id": "bi-1",
          "category": "regulatory",
          "description": "Mandatory breach notifications to government agencies.",
          "severity": "critical",
          "linked_to_step": "s4",
          "linked_to_dre": "dre-1",
          "estimated_cost": {
            "amount": 1000000000,
            "currency": "USD",
            "confidence": "estimated"
          }
        }
      ],

      "summary": {
        "total_duration_days": 470,
        "detection_gap_days": 470,
        "affected_systems": 18000,
        "affected_organizations": 18000,
        "sectors_affected": ["government", "technology", "energy", "healthcare"]
      },

      "references": [
        {
          "title": "SUNBURST Backdoor Analysis",
          "source": "FireEye",
          "date": "2020-12-13"
        }
      ]
    }
  }
}
```

### Document-Level Extension Field Reference

| Field | Type | Description |
|---|---|---|
| `threat_actor.name` | string | Primary name |
| `threat_actor.aliases[]` | array | Known aliases |
| `threat_actor.type` | enum | `nation-state`, `cybercrime`, `hacktivist`, `insider`, `unknown` |
| `threat_actor.motivation` | enum | `espionage`, `financial`, `disruption`, `ideology`, `unknown` |
| `threat_actor.sophistication` | enum | `novice`, `intermediate`, `advanced`, `expert` |
| `threat_actor.attribution_confidence` | enum | `low`, `medium`, `high` |
| `attack_path_notation` | string | Human-readable TLCTC sequence notation |
| `business_impacts[]` | array | Lane 3 impacts with causal linkage |
| `business_impacts[].impact_id` | string | Unique identifier |
| `business_impacts[].category` | enum | `operational`, `financial`, `reputational`, `regulatory`, `strategic` |
| `business_impacts[].severity` | enum | `critical`, `high`, `medium`, `low` |
| `business_impacts[].linked_to_step` | string | `step_id` that caused this impact |
| `business_impacts[].linked_to_dre` | string | `dre_id` that led to this impact |
| `business_impacts[].estimated_cost` | object | `{ amount, currency, confidence }` |
| `summary` | object | Aggregate incident statistics |
| `references[]` | array | External reference documents |

---

&nbsp;

## 8. Worked Example: SolarWinds SUNBURST (v2.0)

When SolarWinds happened, instead of every organization describing it differently, they would all produce an `incident-<id>.json` following the v2.0 schema. Automated tools could ingest it, compare it to other attacks, and update defenses accordingly.

### Attack Path Notation

```
#10 → #7 → #7 ||[update][@SolarWinds→@Org]|| → #7 → #4 → #1 → #4 ||[auth][@Org→@Microsoft]|| → #1 → #1
```

### `incident-APT29-SOLARWINDS-2020.json`

```json
{
  "metadata": {
    "incident_id": "APT29-SOLARWINDS-2020",
    "analyst_confidence": "high",
    "tlctc_version": "2.0",
    "framework_ref": "tlctc-framework.v2.0.json",
    "registry_ref": "@Org-registry.v1.0.0.json",
    "created_at": "2020-12-15T00:00:00Z",
    "notes": "SolarWinds SUNBURST supply chain compromise. Originally documented by FireEye/Mandiant."
  },

  "path_sequence": [
    {
      "step_id": "s1",
      "cluster": "TLCTC-10.02",
      "delta_t_to_next": "~6mo",
      "notes": "Supply chain compromise via development vector: attackers infiltrate SolarWinds build pipeline.",
      "extensions": {
        "ti": {
          "sphere": "@SolarWinds",
          "stage": "initial",
          "velocity_class": "VC-1",
          "software": [
            { "name": "SolarWinds Orion Build Environment", "version": "N/A", "vendor": "SolarWinds", "role": "vulnerability-source" }
          ],
          "vulnerabilities": {
            "cwes": ["CWE-506"],
            "description": "Attackers compromised SolarWinds build environment to inject malicious code during compilation."
          },
          "mitre_mapping": {
            "tactics": ["TA0001"],
            "techniques": ["T1195.002"]
          },
          "temporal": {
            "date": "2019-09-01",
            "duration_minutes": 525600,
            "detection_date": "2020-12-13",
            "detection_gap_days": 470
          },
          "evidence": {
            "iocs": [
              { "type": "hash", "value": "b91ce2fa41029f6955bff20079468448" }
            ],
            "artifacts": ["Compromised build server logs", "Modified build scripts"],
            "log_sources": ["SolarWinds build system logs", "Version control system"]
          }
        }
      }
    },

    {
      "step_id": "s2",
      "cluster": "#7",
      "fec_executed": true,
      "delta_t_to_next": "~2w",
      "notes": "SUNBURST backdoor embedded in signed SolarWinds DLL, packaged for distribution to 18,000+ customers.",
      "extensions": {
        "ti": {
          "sphere": "@SolarWinds",
          "stage": "intermediate",
          "software": [
            { "name": "SUNBURST Backdoor", "version": "Embedded in SolarWinds.Orion.Core.BusinessLayer.dll", "role": "malware" },
            { "name": "SolarWinds Orion Platform", "version": "2019.4 HF 5 through 2020.2.1 HF 1", "vendor": "SolarWinds", "role": "exploit-delivery" }
          ],
          "mitre_mapping": {
            "tactics": ["TA0002", "TA0003", "TA0011"],
            "techniques": ["T1543.003", "T1071.001", "T1132.001"]
          },
          "temporal": { "date": "2020-03-01", "duration_minutes": 20160 },
          "evidence": {
            "iocs": [
              { "type": "hash", "value": "c15abaf51e78ca56c0376522d699c978" },
              { "type": "domain", "value": "avsvmcloud.com" }
            ],
            "artifacts": ["SolarWinds.Orion.Core.BusinessLayer.dll (trojanized)", "C2 communication logs"],
            "log_sources": ["Network traffic logs", "DNS logs", "EDR telemetry"]
          }
        }
      }
    },

    {
      "step_id": "s3",
      "cluster": "#7",
      "fec_executed": true,
      "topology_boundary": {
        "context": "update",
        "source_sphere": "@SolarWinds",
        "target_sphere": "@Org"
      },
      "outcomes": ["C"],
      "delta_t_to_next": "~2w",
      "notes": "SUNBURST executes in customer environment via trusted update channel. C2 communication exposes network topology.",
      "extensions": {
        "ti": {
          "sphere": "@Org",
          "stage": "intermediate",
          "velocity_class": "VC-1",
          "software": [
            { "name": "SUNBURST Backdoor", "role": "malware" }
          ],
          "mitre_mapping": {
            "tactics": ["TA0002", "TA0011"],
            "techniques": ["T1071.001", "T1573.001"]
          },
          "temporal": { "date": "2020-03-15", "duration_minutes": 43200 },
          "data_risk_events": [
            {
              "dre_id": "dre-1",
              "type": "C",
              "description": "Initial C2 communication exposes network topology to attacker.",
              "data_type": "network configuration"
            }
          ],
          "evidence": {
            "iocs": [
              { "type": "domain", "value": "avsvmcloud.com" },
              { "type": "ip", "value": "13.59.205.66" }
            ],
            "artifacts": ["HTTP C2 traffic", "DNS query patterns"],
            "log_sources": ["Firewall logs", "Proxy logs", "DNS logs"]
          }
        }
      }
    },

    {
      "step_id": "s4",
      "cluster": "#7",
      "fec_executed": true,
      "delta_t_to_next": "~2w",
      "notes": "Additional malware stages deployed: TEARDROP, RAINDROP loaders and Cobalt Strike for persistence and lateral movement.",
      "extensions": {
        "ti": {
          "sphere": "@Org",
          "stage": "intermediate",
          "software": [
            { "name": "TEARDROP", "role": "malware" },
            { "name": "RAINDROP", "role": "malware" },
            { "name": "Cobalt Strike", "role": "dual-use-tool" }
          ],
          "mitre_mapping": {
            "tactics": ["TA0002", "TA0005"],
            "techniques": ["T1055", "T1105", "T1027"]
          },
          "temporal": { "date": "2020-04-01" },
          "evidence": {
            "iocs": [
              { "type": "hash", "value": "1835b0e8fc19bca99c4b8e0f7d9fa1b3" }
            ],
            "artifacts": ["TEARDROP loader", "Cobalt Strike beacons"]
          }
        }
      }
    },

    {
      "step_id": "s5",
      "cluster": "#4",
      "outcomes": ["C"],
      "delta_t_to_next": "~2w",
      "notes": "Identity Theft: use of stolen domain/admin credentials to impersonate identities. Acquisition occurred via prior #7 activity.",
      "extensions": {
        "ti": {
          "sphere": "@Org",
          "stage": "intermediate",
          "velocity_class": "VC-1",
          "mitre_mapping": {
            "tactics": ["TA0006"],
            "techniques": ["T1078.002"]
          },
          "temporal": { "date": "2020-04-15" },
          "data_risk_events": [
            {
              "dre_id": "dre-2",
              "type": "C",
              "description": "Domain admin credentials exfiltrated.",
              "data_type": "credentials",
              "volume": "Multiple admin accounts"
            }
          ]
        }
      }
    },

    {
      "step_id": "s6",
      "cluster": "#1",
      "delta_t_to_next": "~2w",
      "notes": "Abuse of Functions: lateral movement via legitimate remote admin/authentication services after #4 impersonation.",
      "extensions": {
        "ti": {
          "sphere": "@Org-Admin",
          "stage": "intermediate",
          "mitre_mapping": {
            "tactics": ["TA0008"],
            "techniques": ["T1021.001"]
          },
          "temporal": { "date": "2020-05-01" }
        }
      }
    },

    {
      "step_id": "s7",
      "cluster": "#4",
      "topology_boundary": {
        "context": "auth",
        "source_sphere": "@Org",
        "target_sphere": "@Microsoft"
      },
      "outcomes": ["C"],
      "delta_t_to_next": "instant",
      "notes": "Identity Theft in cloud: use of credentials/tokens to assume identities in M365/Azure AD across federated trust boundary.",
      "extensions": {
        "ti": {
          "sphere": "@Microsoft",
          "stage": "final",
          "software": [
            { "name": "Azure AD", "role": "target" },
            { "name": "Microsoft 365", "role": "target" }
          ],
          "mitre_mapping": {
            "tactics": ["TA0006"],
            "techniques": ["T1078.004"]
          },
          "temporal": { "date": "2020-06-01" },
          "evidence": {
            "log_sources": ["Azure AD sign-in logs", "Office 365 audit logs"]
          }
        }
      }
    },

    {
      "step_id": "s8",
      "cluster": "#1",
      "outcomes": ["C"],
      "delta_t_to_next": "~2w",
      "notes": "Abuse of Functions: accessing email and cloud data via normal service functions (mailbox access, SharePoint, Azure APIs).",
      "extensions": {
        "ti": {
          "sphere": "@Microsoft",
          "stage": "final",
          "software": [
            { "name": "Microsoft 365", "role": "target" },
            { "name": "Azure", "role": "target" }
          ],
          "mitre_mapping": {
            "tactics": ["TA0009"],
            "techniques": ["T1114.002", "T1213.002"]
          },
          "temporal": { "date": "2020-06-01" },
          "evidence": {
            "log_sources": ["Office 365 audit logs", "Azure activity logs"]
          }
        }
      }
    },

    {
      "step_id": "s9",
      "cluster": "#1",
      "outcomes": ["C"],
      "notes": "Abuse of Functions: data exfiltration through legitimate HTTPS/cloud storage APIs.",
      "extensions": {
        "ti": {
          "sphere": "@Microsoft",
          "stage": "final",
          "mitre_mapping": {
            "tactics": ["TA0010"],
            "techniques": ["T1567.002", "T1048.003"]
          },
          "temporal": { "date": "2020-06-15" }
        }
      }
    }
  ],

  "extensions": {
    "ti": {
      "threat_actor": {
        "name": "APT29",
        "aliases": ["Cozy Bear", "The Dukes", "YTTRIUM", "UNC2452"],
        "type": "nation-state",
        "motivation": "espionage",
        "sophistication": "expert",
        "attribution_confidence": "high"
      },

      "attack_path_notation": "#10 → #7 → #7 ||[update][@SolarWinds→@Org]|| → #7 → #4 → #1 → #4 ||[auth][@Org→@Microsoft]|| → #1 → #1",

      "business_impacts": [
        {
          "impact_id": "bi-1",
          "category": "regulatory",
          "description": "Mandatory breach notifications to multiple government agencies and affected organizations.",
          "severity": "critical",
          "linked_to_step": "s3",
          "linked_to_dre": "dre-1"
        },
        {
          "impact_id": "bi-2",
          "category": "reputational",
          "description": "Significant damage to SolarWinds brand and customer trust.",
          "severity": "critical",
          "linked_to_step": "s1"
        },
        {
          "impact_id": "bi-3",
          "category": "financial",
          "description": "Global incident response, remediation, and legal costs.",
          "severity": "critical",
          "linked_to_step": "s9",
          "estimated_cost": {
            "amount": 1000000000,
            "currency": "USD",
            "confidence": "estimated"
          }
        },
        {
          "impact_id": "bi-4",
          "category": "strategic",
          "description": "Potential exfiltration of sensitive government and corporate intellectual property.",
          "severity": "critical",
          "linked_to_dre": "dre-2"
        },
        {
          "impact_id": "bi-5",
          "category": "operational",
          "description": "Mass emergency patching and system rebuilds across 18,000+ organizations.",
          "severity": "critical",
          "linked_to_step": "s3"
        }
      ],

      "summary": {
        "total_duration_days": 470,
        "detection_gap_days": 470,
        "affected_systems": 18000,
        "affected_organizations": 18000,
        "sectors_affected": [
          "government",
          "technology",
          "telecommunications",
          "consulting",
          "energy",
          "healthcare"
        ],
        "estimated_cost": {
          "amount": 1000000000,
          "currency": "USD",
          "confidence": "estimated"
        }
      },

      "references": [
        {
          "title": "SUNBURST Backdoor Analysis",
          "source": "FireEye",
          "date": "2020-12-13"
        },
        {
          "title": "Microsoft Analysis of Solorigate",
          "source": "Microsoft",
          "date": "2020-12-18"
        },
        {
          "title": "CISA Alert AA20-352A",
          "source": "CISA",
          "date": "2020-12-17"
        }
      ]
    }
  }
}
```

### Key v2.0 Translation Notes

The following changes were made compared to earlier v1.x representations of this attack:

| v1.x Pattern | v2.0 Pattern | Rationale |
|---|---|---|
| `step_number` (integer) | `step_id` (string, e.g., `"s1"`) | Enables stable cross-referencing; survives step insertion/reordering |
| `tlctc_cluster: { strategic, operational }` | `cluster: "#10"` or `"TLCTC-10.02"` | Single field; strategic or operational notation as appropriate |
| Standalone boundary steps | `topology_boundary` on the cluster step | Boundaries annotate steps, not replace them |
| `responsibility_sphere` on step | `extensions.ti.sphere` | Base schema carries boundaries; sphere per step is enrichment |
| `impact.data_risk_events[]` | `outcomes: ["C"]` + `extensions.ti.data_risk_events[]` | Base tags for validation; rich DREs for intelligence sharing |
| `business_impacts[]` at root | `extensions.ti.business_impacts[]` | Keeps base schema minimal; impacts are enrichment |
| `comment` | `notes` | Consistent naming |

---

&nbsp;

## 9. How These JSONs Work Together

```
INCIDENT ANALYSIS WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. FRAMEWORK FOUNDATION
   └─→ Load tlctc-framework.v2.0.json
       ├─ Threat cluster definitions
       ├─ Axioms (I–X)
       └─ Rules (R-EXEC)

2. REFERENCE DATA
   └─→ Load @Org-registry.v1.0.0.json
       ├─ Responsibility spheres
       └─ Boundary contexts

3. CREATE ATTACK INSTANCE
   └─→ New incident-<id>.json following schema
       ├─ Map each step to a TLCTC cluster
       ├─ Add boundary annotations at domain crossings
       ├─ Record Δt between steps
       ├─ Tag outcomes (C/I/A)
       ├─ Assert fec_executed where R-EXEC applies
       └─ Add extensions.ti enrichment (software, CVEs, MITRE, evidence)

4. VALIDATION
   └─→ Validate against tlctc-attack-path.schema.json
       ├─ Pass 1: JSON Schema validation (base fields)
       └─ Pass 2: Referential integrity (fec_recorded_in_step_id, sphere allow-list)

5. SHARING & ANALYSIS
   └─→ Share incident-<id>.json with community
       ├─ All organizations understand the notation
       ├─ Automated tool ingestion via base fields
       ├─ Pattern matching across incidents
       └─ Aggregated threat intelligence via TI extensions
```

---

&nbsp;

## 10. Key Benefits of This Architecture

| Benefit | How It's Achieved |
|---|---|
| Universal Language | Everyone references the same `tlctc-framework.v2.0.json` definitions |
| Machine-Readable | Structured JSON enables automated ingestion and analysis |
| Consistent Validation | Schema ensures all instances follow the same structure |
| Separation of Concerns | Framework (static) vs Intelligence (dynamic) clearly separated |
| Evolution-Friendly | Framework can evolve without breaking historical instances |
| Global Collaboration | Standardized format enables worldwide threat intelligence sharing |
| Tool Integration | SIEM, SOC, TIP tools can parse and correlate automatically |
| Minimal + Extensible | Base schema is lean; `extensions.ti` adds richness without breaking interoperability |

---

&nbsp;

## 11. Usage Examples

### For Security Operations Centers (SOC)

- Load `tlctc-framework.v2.0.json` into your SIEM/TIP
- Configure detection rules mapped to TLCTC clusters
- When incidents occur, create `incident-<id>.json`
- Share with trusted partners / ISACs / threat intelligence communities
- Receive attack paths from others, automatically correlate patterns

### For Threat Intelligence Teams

- Document APT campaigns using `incident-<id>.json` format with full TI extensions
- Compare attack sequences across different threat actors
- Identify common patterns (e.g., all APT29 attacks start with `#10 → #7`)
- Generate Cyber Threat Radars showing cluster distribution

### For Risk Management

- Reference `tlctc-framework.v2.0.json` for threat taxonomy in risk registers
- Map controls to specific TLCTC clusters using NIST CSF functions (see white paper, Chapter 8)
- Analyze historical attack paths to identify control gaps
- Prioritize investments based on cluster frequency in your sector
- Communicate risks to board using strategic notation (`#X`)

---

&nbsp;

## 12. Creating Your Own Attack Path Instance

### Quick Start

To document an attack you have observed:

1. **Copy** the base structure from the schema (or use the SolarWinds example as a template).
2. **For each step** in the attack:
   - Map to the appropriate TLCTC cluster (use `tlctc-framework.v2.0.json` for reference)
   - Choose strategic (`#X`) or operational (`TLCTC-XX.YY`) notation for the `cluster` field
   - Add `topology_boundary` where the attack crosses a domain boundary
   - Set `fec_executed: true` and ensure a `#7` step exists per R-EXEC
   - Tag `outcomes` (`C`, `I`, `A`)
   - Record `delta_t_to_next` between steps
   - Add `extensions.ti` enrichment (software, CVEs, MITRE mappings, evidence)
3. **Generate** the human-readable attack path notation (e.g., `#9 → #3 → #7`)
4. **Add document-level** `extensions.ti` (threat actor, business impacts, summary, references)
5. **Validate** against `tlctc-attack-path.schema.json`
6. **Share** with community!

### Conformance Checklist

An incident record is conformant if (per white paper, Section 7.6):

1. It validates against `tlctc-attack-path.schema.json`
2. `metadata.tlctc_version` matches the referenced framework package version
3. All `step_id` values are unique within the document
4. If `fec_executed=true` appears in any step, either that step is `#7`/`TLCTC-07.xx`, or it includes `fec_recorded_in_step_id` pointing to a `#7` step
5. All boundary annotations use sphere and context identifiers defined in the referenced Layer 2 registry

---

&nbsp;

## 13. Tool Integration

These JSON structures are designed to integrate with:

- **STIX/TAXII** — Enhanced STIX objects with TLCTC cluster mappings
- **MITRE ATT&CK Navigator** — Techniques mapped to clusters
- **SIEM Platforms** — Automated rule generation per cluster
- **Threat Intelligence Platforms** — Standardized ingestion via base schema
- **Risk Management Tools** — Direct mapping to controls (see white paper, Chapter 8)
- **Incident Response Platforms** — Playbook generation per cluster
- **SOAR Systems** — Velocity class determines automation requirements

---

&nbsp;

## 14. Important Notes

- Always reference the framework version in your attack instances (`tlctc_version` field)
- Respect data classification (use `metadata.notes` or a TLP extension for marking)
- Validate against the schema before sharing
- Include sufficient evidence references for verification
- Update `metadata.created_at` or add a `modified_at` extension when editing instances
- The base schema uses `additionalProperties: false`; all custom fields MUST go in `extensions`

---

&nbsp;

## 15. Version Compatibility

| This Guide | White Paper | Framework | Schema |
|---|---|---|---|
| v2.0 | TLCTC v2.0 White Paper, Chapter 7 | `tlctc-framework.v2.0.json` | `tlctc-attack-path.schema.json` v2.0 |

### Changes from v1.x JSON Architecture

| Area | v1.x | v2.0 |
|---|---|---|
| Step identification | `step_number` (integer) | `step_id` (string) |
| Cluster reference | Dual object `{ strategic, operational }` | Single `cluster` field |
| Boundaries | Standalone steps or inline objects | `topology_boundary` on cluster steps |
| Enrichment fields | Mixed into base schema | Isolated in `extensions.ti` |
| Business impacts | Root-level array | `extensions.ti.business_impacts[]` |
| Validation | Informal | `additionalProperties: false` + conformance checklist |
| Parallel execution | Ad-hoc | `parallel_group` with `mode: "parallel"` |
| FEC recording | Implicit | Explicit `fec_executed` + `fec_recorded_in_step_id` |

---

&nbsp;

**Bernhard Kreinz**

Opinions are the author's own. Cite TLCTC properly when re-using definitions.
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
