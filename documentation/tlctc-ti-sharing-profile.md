&nbsp;

&nbsp;

# TLCTC Threat-Intelligence Sharing — Extension Profile

## An enrichment & sharing companion to the TLCTC White Paper

&nbsp;

**Bernhard Kreinz**

&nbsp;

March 2026 · revised August 2026 · aligned to TLCTC v2.5

&nbsp;

---

&nbsp;

## Abstract

This guide defines the **Threat Intelligence Extension Profile** for TLCTC Layer 3 attack-path instances: a standard convention (`extensions.ti`) for enriching the minimal base schema with software, CVEs, MITRE mappings, evidence, and business impacts, so that incidents can be shared and correlated across organizations. It also presents the **Three-Lane Conceptual Model** (Attack Path / Data Risk / Business Risk) that these enrichment fields are organized around.

This is an **informative companion**, not a normative definition. The layered JSON architecture and the attack-path notation are defined normatively in the TLCTC White Paper; this guide only adds the sharing/enrichment convention layered on top.

**Implements:** TLCTC framework specification **v2.5**. The normative authority for cluster definitions, axioms, and classification rules is the canonical dictionary `json-schemas/layer-1/tlctc-framework.v2.5.json`, reproduced and derived in the v2.5 core paper (`documentation/tlctc-v2.5-core.md`); this profile introduces no normative content of its own.

> **Where the normative definitions live:**
>
> - **Layered JSON architecture & schemas** → White Paper §14 (*The JSON Architecture*)
> - **Attack-path notation & operators** → White Paper §11 (*Attack Path Notation*); core paper §7
> - **Framework dictionary** → `json-schemas/layer-1/tlctc-framework.v2.5.json`
> - **Layer 1–3 schemas & canonical examples** → `json-schemas/layer-1…3/` (e.g. `layer-3/examples/solarwinds-2020.json`)
>
> Where any conflict exists, the White Paper and the schemas prevail.

---

&nbsp;

## 1. Architecture at a Glance

TLCTC threat intelligence is organized in layers (full definitions: White Paper §14):

- **Layer 1 — Framework (static):** the universal taxonomy — 10 clusters, axioms, rules. `tlctc-framework.v2.5.json`.
- **Layer 2 — Reference (semi-static):** responsibility spheres (`@Org`, `@Vendor`, …) and boundary contexts, customizable per organization.
- **Layer 3 — Attack-path instances (dynamic):** individual incidents as ordered cluster steps with velocity, boundaries, and outcomes — the objects shared as threat intelligence.
- **Layer 4 — Risk quantification (optional extension, *proposed*):** a FAIR bridge for financial risk modeling. See `documentation/tlctc-fair-integration-proposal.md` and `json-schemas/layer-4/`.

The **Threat Intelligence Extension Profile** defined below enriches Layer 3 instances through the schema's reserved `extensions` object, without changing the base fields every tool relies on.

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

## 3. Threat Intelligence Extension Profile

The v2.0 base schema is intentionally minimal to ensure broad interoperability. For rich threat intelligence sharing, this section defines a **standard extension profile** using the `extensions` object that the base schema reserves at both step and document level.

All enrichment fields live under `extensions.ti` (Threat Intelligence namespace).

### 3.1 Step-Level Extensions

Each `attack_step` may carry the following under `extensions.ti`:

```json
{
  "step_id": "s1",
  "cluster": "#10",
  "topology_boundary": {
    "context": "update",
    "source_sphere": "@Vendor",
    "target_sphere": "@Org"
  },
  "delta_t_to_next": "~14d",
  "notes": "Trust Acceptance Event (R-SUPPLY): signed vendor update accepted by target via legitimate update channel; trojanized artifact passes signature/trust verification. Upstream build-pipeline compromise is recorded as causal TI context (CVE/CWE/MITRE), not as a separate #10 step on the vendor side.",
  "extensions": {
    "ti": {
      "sphere": "@Org",
      "stage": "initial",
      "velocity_class": "VC-1",

      "software": [
        {
          "name": "SolarWinds Orion Platform",
          "version": "2019.4 HF 5 through 2020.2.1 HF 1",
          "vendor": "SolarWinds",
          "role": "exploit-delivery",
          "cpe": "cpe:2.3:a:solarwinds:orion_platform:*"
        }
      ],

      "vulnerabilities": {
        "cves": ["CVE-2020-10148"],
        "cwes": ["CWE-506"],
        "description": "Trojanized signed build artifact distributed via legitimate update channel; upstream build environment compromise enabled injection at compile time."
      },

      "mitre_mapping": {
        "tactics": ["TA0001"],
        "techniques": ["T1195.002"]
      },

      "temporal": {
        "date": "2020-03-26",
        "detection_date": "2020-12-13",
        "detection_gap_days": 262
      },

      "evidence": {
        "iocs": [
          { "type": "hash", "value": "b91ce2fa41029f6955bff20079468448" }
        ],
        "artifacts": ["SolarWinds.Orion.Core.BusinessLayer.dll (trojanized)", "Update server logs"],
        "log_sources": ["Update server logs", "Endpoint install logs"]
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
| `identity_relation` | enum | Relation between the identity claimed by a presented credential and the presenter: `impersonated` (identity belongs to someone other than the presenter — the normal #4 case), `self-issued` (credential was issued to the presenter by the target system through a designed enrolment function; the presenter is its authentic holder), `unknown` (issuance provenance not yet established). Optional; add only where provenance was examined. Absence asserts nothing. |
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

**Consistency check (`identity_relation`).** The field records an assertion whose classification consequences follow from **R-CRED** (self-issued proviso), not from this profile. A step with `"cluster": "#4"` and `"identity_relation": "self-issued"` is mechanically contradictory: authentication as the credential's authentic holder exploits no #4 binding gap. Validators SHOULD flag this combination; resolution is either re-classifying the step (usually to `#1` at the enrolment step) or correcting the relation to `impersonated`/`unknown`. `unknown` marks an open analytical task (the step's classification stands, but provenance has not been checked) — useful when re-checking records against the self-issued proviso (R-CRED). On an enrolment step (`#1`), `self-issued` marks the head of an expected `#1 → #4` (enrolment as an existing identity) or `#1`-only (fictitious registration) continuation.

### 3.2 Document-Level Extensions

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

      "attack_path_notation": "#10 ||[update][@Vendor→@Org]|| →[Δt=~14d] #7 →[Δt=~2w] #7 →[Δt=~2w] #4 →[Δt=~2w] #1 →[Δt=~2w] #4 ||[auth][@Org→@Cloud]|| →[Δt=instant] #1 →[Δt=~2w] #1 + [DRE: C]",

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

## 4. Worked Example: SolarWinds SUNBURST

> The canonical **base-schema** instance lives at [`json-schemas/layer-3/examples/solarwinds-2020.json`](../json-schemas/layer-3/examples/solarwinds-2020.json). The version below is the same incident enriched with the full TI Extension Profile.

When SolarWinds happened, instead of every organization describing it differently, they would all produce an `incident-<id>.json` following the v2.0 schema. Automated tools could ingest it, compare it to other attacks, and update defenses accordingly.

### Attack Path Notation

```
#10 ||[update][@SolarWinds→@Org]|| →[Δt=~14d] #7 →[Δt=~2w] #7 →[Δt=~2w] #4 →[Δt=~2w] #1 →[Δt=~2w] #4 ||[auth][@Org→@Microsoft]|| →[Δt=instant] #1 →[Δt=~2w] #1 + [DRE: C]
```

Per **R-SUPPLY**, `#10` is placed at the **Trust Acceptance Event** — the moment the signed Orion update becomes authoritative inside `@Org`. The upstream build-pipeline compromise on `@SolarWinds` is recorded as causal context in the step's TI extension, not as a separate `#10` step on the vendor side.

### `incident-APT29-SOLARWINDS-2020.json`

```json
{
  "metadata": {
    "incident_id": "APT29-SOLARWINDS-2020",
    "analyst_confidence": "high",
    "tlctc_version": "2.5",
    "framework_ref": "tlctc-framework.v2.5.json",
    "registry_ref": "@Org-registry.v1.0.0.json",
    "created_at": "2020-12-15T00:00:00Z",
    "notes": "SolarWinds SUNBURST supply chain compromise. Originally documented by FireEye/Mandiant."
  },

  "path_sequence": [
    {
      "step_id": "s1",
      "cluster": "#10",
      "topology_boundary": {
        "context": "update",
        "source_sphere": "@SolarWinds",
        "target_sphere": "@Org"
      },
      "delta_t_to_next": "~14d",
      "notes": "Trust Acceptance Event (R-SUPPLY): the signed SolarWinds Orion update (v2019.4 HF 5 through 2020.2.1 HF 1) — containing the SUNBURST backdoor inside SolarWinds.Orion.Core.BusinessLayer.dll — is accepted and installed by the target via the legitimate vendor update channel and passes signature/trust verification. Upstream cause (recorded as TI context, not as a separate step): attackers compromised the SolarWinds build environment ~6 months earlier (Sep 2019) and injected SUNBURST during compilation. Per R-SUPPLY, #10 is placed here at the TAE inside @Org, not at the upstream build-pipeline event on @SolarWinds.",
      "extensions": {
        "ti": {
          "sphere": "@Org",
          "stage": "initial",
          "velocity_class": "VC-1",
          "software": [
            { "name": "SolarWinds Orion Platform", "version": "2019.4 HF 5 through 2020.2.1 HF 1", "vendor": "SolarWinds", "role": "exploit-delivery" },
            { "name": "SolarWinds Orion Build Environment", "version": "N/A", "vendor": "SolarWinds", "role": "vulnerability-source" }
          ],
          "vulnerabilities": {
            "cves": ["CVE-2020-10148"],
            "cwes": ["CWE-506"],
            "description": "Trojanized signed build artifact distributed via legitimate update channel; upstream build environment compromise enabled injection at compile time."
          },
          "mitre_mapping": {
            "tactics": ["TA0001"],
            "techniques": ["T1195.002"]
          },
          "temporal": {
            "date": "2020-03-26",
            "detection_date": "2020-12-13",
            "detection_gap_days": 262
          },
          "evidence": {
            "iocs": [
              { "type": "hash", "value": "b91ce2fa41029f6955bff20079468448" },
              { "type": "hash", "value": "c15abaf51e78ca56c0376522d699c978" }
            ],
            "artifacts": ["SolarWinds.Orion.Core.BusinessLayer.dll (trojanized)", "Compromised build server logs", "Modified build scripts"],
            "log_sources": ["Update server logs", "SolarWinds build system logs", "Version control system"]
          }
        }
      }
    },

    {
      "step_id": "s2",
      "cluster": "#7",
      "fec_executed": true,
      "outcomes": ["C"],
      "delta_t_to_next": "~2w",
      "notes": "FEC execution via designed capability (R-EXEC): SUNBURST loads inside the legitimate solarwinds.businesslayerhost.exe service using the platform's intended DLL loading mechanism — an intended data→code transition, not an exploit. After a ~14-day dormancy SUNBURST initiates C2 over DNS (avsvmcloud.com), exposing internal network topology to the attacker.",
      "extensions": {
        "ti": {
          "sphere": "@Org",
          "stage": "intermediate",
          "velocity_class": "VC-1",
          "software": [
            { "name": "SUNBURST Backdoor", "version": "Embedded in SolarWinds.Orion.Core.BusinessLayer.dll", "role": "malware" }
          ],
          "mitre_mapping": {
            "tactics": ["TA0002", "TA0011"],
            "techniques": ["T1543.003", "T1071.001", "T1573.001", "T1132.001"]
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
      "step_id": "s3",
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
      "step_id": "s4",
      "cluster": "#4",
      "outcomes": ["C"],
      "delta_t_to_next": "~2w",
      "notes": "Identity Theft (R-CRED, Axiom X): use of stolen domain/admin credentials to authenticate. Credential acquisition occurred during prior #7 activity (consequence of malware access — recorded as DRE:C on s2/s3); credential application is always #4 regardless of acquisition method.",
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
      "step_id": "s5",
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
      "step_id": "s6",
      "cluster": "#4",
      "topology_boundary": {
        "context": "auth",
        "source_sphere": "@Org",
        "target_sphere": "@Microsoft"
      },
      "outcomes": ["C"],
      "delta_t_to_next": "instant",
      "notes": "Identity Theft in cloud (R-CRED): use of forged SAML tokens (signed with stolen ADFS signing key) to assume identities in M365/Azure AD across the federated trust boundary.",
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
      "step_id": "s7",
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
      "step_id": "s8",
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

      "attack_path_notation": "#10 ||[update][@SolarWinds→@Org]|| →[Δt=~14d] #7 →[Δt=~2w] #7 →[Δt=~2w] #4 →[Δt=~2w] #1 →[Δt=~2w] #4 ||[auth][@Org→@Microsoft]|| →[Δt=instant] #1 →[Δt=~2w] #1 + [DRE: C]",

      "business_impacts": [
        {
          "impact_id": "bi-1",
          "category": "regulatory",
          "description": "Mandatory breach notifications to multiple government agencies and affected organizations.",
          "severity": "critical",
          "linked_to_step": "s2",
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
          "linked_to_step": "s8",
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
          "linked_to_step": "s2"
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

---

&nbsp;

## 5. Interoperability & Conformance

**Conformance.** An instance is conformant when it validates against the Layer 3 schema (`json-schemas/layer-3/tlctc-attack-path.schema.json`) and follows the classification rules; the full conformance checklist is in White Paper §14. Every enrichment field defined here lives under the schema's reserved `extensions.ti` namespace, so the base document stays interoperable and validates unchanged.

**STIX/TAXII.** Cluster tags carried on STIX objects via custom properties (e.g., `x_tlctc_primary_cluster`). **Layer 3 attack path instances do not round-trip to STIX 2.1**: Δt velocity annotations, parallel groups (`#X + #Y`), boundary operators (`||...||`, `⇒`, `|...|`), DRE tags, and unresolved operators (`?`, `…`) have no native STIX 2.1 equivalents. Full Layer 3 exchange requires either a custom STIX extension or transporting the TLCTC JSON instance alongside STIX as an out-of-band artifact.

---

&nbsp;

**Bernhard Kreinz**

Opinions are the author's own. Cite TLCTC properly when re-using definitions.
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
