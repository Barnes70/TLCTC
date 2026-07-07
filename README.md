# Top Level Cyber Threat Clusters (TLCTC)

**Version 2.3** · CC BY 4.0 · [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20633177.svg)](https://doi.org/10.5281/zenodo.20633177) · [tlctc.net](https://www.tlctc.net) · [Core Paper (citable)](documentation/tlctc-v2.3-core.md) · [White Paper](https://www.tlctc.net/tlctc-v2.0-whitepaper.html)

A cause-oriented, axiomatic cyber threat taxonomy. We are aware of no prior framework that classifies threats by the generic vulnerability exploited rather than by outcome or actor.

TLCTC provides the missing semantic foundation for cybersecurity: a stable, non-overlapping classification of cyber threats based on **why** compromise happens — the generic vulnerability exploited — rather than **what** happens afterwards (outcomes like "data breach," "ransomware," or "denial of service").

> *A cyber threat is defined by the generic vulnerability it exploits, not by who performs it and not by what consequence follows.*

---

## Framework Documents

TLCTC v2.3 is a **consolidation freeze** of the finalized v2.1 framework — no new clusters, axioms, or rules (see [`tlctc-v2.3-traceability.md`](documentation/tlctc-v2.3-traceability.md)). The documents form a deliberate hierarchy:

| Document | Role |
|---|---|
| [**Core Paper**](documentation/tlctc-v2.3-core.md) ([PDF](documentation/tlctc-v2.3-core.pdf)) | **The canonical, citable definition** of the framework: derivation, 10 clusters, 10 axioms, 16 classification rules, attack-path notation, glossary, references. Cite this. |
| [**Application Paper**](documentation/tlctc-v2.3-application.md) ([PDF](documentation/tlctc-v2.3-application.pdf)) | Companion for putting the taxonomy to work: classification procedure, worked examples, NIST CSF mapping, controls, KRI/KCI/KPI. Takes the core as given. |
| [**White Paper**](documentation/tlctc-v2.0-whitepaper.md) ([web](https://www.tlctc.net/tlctc-v2.0-whitepaper.html)) | The extended practitioner handbook: full notation grammar (§11), boundary catalogs, decision procedures, anti-patterns, and worked detail beyond the core. Conforms to the core; filename kept for link stability. |
| [**Operational Enumeration**](documentation/tlctc-operational-enumeration.md) ([JSON](json-schemas/operational/tlctc-operational-enumeration.json)) | The *evolving* `TLCTC-XX.YY` sub-cluster catalogue. The strategic layer (10 clusters) is frozen; the operational layer grows by contribution. |

Machine-readable twin of the core: [`json-schemas/layer-1/tlctc-framework.v2.3.json`](json-schemas/layer-1/tlctc-framework.v2.3.json).

---

## The Problem: Semantic Diffusion

Cybersecurity suffers from a persistent language problem. "Threat" is used interchangeably for actors, vulnerabilities, control failures, incidents, and outcomes. Even authoritative sources maintain conflicting definitions — NIST alone carries over 20 different definitions of "cyber threat" across its publications. This semantic blur makes it impossible to compare incidents, aggregate intelligence, design targeted controls, or communicate risk consistently between leadership, risk functions, and technical teams.

TLCTC solves this by anchoring analysis in **causality** and enforcing strict separation through formal axioms.

## Core Architecture

### The Bow-Tie Anchor

TLCTC is structurally anchored in the **Bow-Tie risk model**, which enforces the separation between causes and effects:

```
   CAUSE SIDE                    RISK EVENT                 CONSEQUENCE SIDE
┌──────────────────┐     ┌─────────────────────┐     ┌──────────────────────┐
│  Threat Clusters  │     │  Loss of Control /  │     │   Data Risk Events   │
│  (#1 – #10)      │────▶│  System Compromise  │────▶│   (C, I, A)          │
│  Generic Vulns    │     │     [DETECT]        │     │   Business Impact    │
│                   │     │                     │     │                      │
│  IDENTIFY/PROTECT │     └─────────────────────┘     │  RESPOND/RECOVER     │
└──────────────────┘                                   └──────────────────────┘
```

Threat clusters live **exclusively** on the cause side. Outcomes such as Loss of Confidentiality, Loss of Integrity, or Loss of Availability/Accessibility are recorded separately as **Data Risk Events (DREs)** — never as threat categories.

### The Two-Tiered Approach

TLCTC strictly separates two layers that must align without collapsing into each other:

| Layer | Focus | Stability | Audience |
|---|---|---|---|
| **Strategic Management** | 10 clusters, generic vulnerabilities, risk governance, control mapping | Stable | CISO, Risk, Board |
| **Operational Security** | Specific CVEs, CWEs, MITRE ATT&CK TTPs, detection rules | Dynamic | SOC, Engineering, DevSec |

This separation ensures that strategic risk discussions remain comparable across technologies, environments, and organizations — while operational teams retain full granularity.

---

## The 10 Top Level Cyber Threat Clusters

Each cluster is defined by exactly **one generic vulnerability** (Axiom VI). Each attack step maps to exactly **one** cluster. No overlaps, no gaps.

| # | Cluster | Generic Vulnerability | Topology |
|---|---|---|---|
| **#1** | **Abuse of Functions** | The inherent trust, scope, and complexity designed into software functionality and configuration | Internal |
| **#2** | **Exploiting Server** | Server-side implementation flaws enable unintended behavior | Internal |
| **#3** | **Exploiting Client** | Client-side implementation flaws enable unintended behavior | Internal |
| **#4** | **Identity Theft** | Insufficient binding, at the point of authentication, between a presented credential and the authentic holder of the identity it claims | Internal |
| **#5** | **Man in the Middle** | The lack of sufficient control, integrity protection, or confidentiality over the communication channel/path | Internal |
| **#6** | **Flooding Attack** | Finite capacity limitations inherent in any system component | Internal |
| **#7** | **Malware** | The software environment's designed capability to execute potentially untrusted foreign code | Internal |
| **#8** | **Physical Attack** | Physical accessibility of infrastructure and the exploitability of physical-layer properties | Bridge |
| **#9** | **Social Engineering** | Humans can be influenced into unsafe actions or decisions | Bridge |
| **#10** | **Supply Chain Attack** | Trust in third-party components and update channels can be subverted | Bridge |

### Cluster Scope (operational)

The generic-vulnerability strings above are reproduced verbatim from the canonical framework dictionary (`json-schemas/layer-1/tlctc-framework.v2.3.json`), which also carries the canonical one-line Definition and Attacker's View per cluster. The scope descriptions below are the operational elaborations from the white paper §4.1.

- **#1 Abuse of Functions** — Manipulation of legitimate software capabilities — features, APIs, configurations, administrative settings, workflows — through standard interfaces using built-in input types and valid sequences of actions. The step achieves an attacker advantage **without requiring an implementation flaw**.

- **#2 Exploiting Server** — Triggering an **implementation flaw** in **server-role** software using exploit code, exploiting coding mistakes in how the server processes requests, handles data, enforces logic, or manages resources. This forces an **unintended data→code transition**.

- **#3 Exploiting Client** — Triggering an **implementation flaw** in **client-role** software through crafted content, responses, or state, exploiting coding mistakes in parsing, rendering, state management, or response handling.

- **#4 Identity Theft** — Presentation or use of credentials, tokens, keys, session artifacts, or other identity representations to authenticate and act **as an identity different from the presenter's own**. This cluster focuses on the **use** of credentials — acquisition maps to the enabling cluster (see Credential Dual Nature below).

- **#5 Man in the Middle (MitM)** — Exploitation of a controlled position on a communication path through interception, observation, modification, injection, replay, or protocol downgrade/stripping.

- **#6 Flooding Attack** — Exhaustion of finite system resources (bandwidth, CPU, memory, storage, quotas, pools) through volume or intensity that exceeds capacity limits, causing disruption, degradation, or denial of service.

- **#7 Malware** — Execution of **Foreign Executable Content (FEC)** through the environment's designed execution capabilities (binaries, scripts, macros, modules, or attacker-controlled commands fed into interpreters), including dual-use tooling when it executes attacker-controlled FEC.

- **#8 Physical Attack** — Unauthorized physical interaction with or interference to hardware, facilities, media, interfaces (including removable media), or signals — via direct contact or exploitation of physical phenomena/emanations.

- **#9 Social Engineering** — Psychological manipulation that causes a human to perform an action counter to security interests — disclosing information, granting access, executing content, modifying configuration, or bypassing procedures.

- **#10 Supply Chain Attack** — Exploitation of an organization's **third-party trust link** such that the organization accepts third-party-originating artifacts or decisions as authoritative within its domain, enabling unauthorized action or compromise. Placed at the **Trust Acceptance Event (TAE)**.

---

## Key Concepts

### Data→Code Transitions and R-EXEC

The execution distinction is the sharpest analytical tool in the framework. Four data paths exist:

| Path | Mechanism | Cluster |
|---|---|---|
| Data → Data | Pure data manipulation, no code execution | #1 only |
| Data → Function → Foreign Code | Function abuse enables code execution | #1 → #7 |
| Data → Code via Implementation Flaw | Unintended transition (exploit code triggers bug) | #2 or #3 |
| Data → Code via Designed Capability | Intended execution (malware code uses execution engine) | #7 |

**R-EXEC Rule (Normative):** Whenever Foreign Executable Content (FEC) is executed, a **#7 step MUST be recorded** at the moment of execution, independent of how execution was enabled. Analysts must not "absorb" execution into the enabling cluster.

Common execution patterns: `#1 → #7` · `#2 → #7` · `#3 → #7` · `#8 → #7` · `#9 → #7` · `#10 → #7`

### Credential Dual Nature (Axiom X)

Credentials have two distinct operational phases, and they **must** be classified separately:

| Phase | Classification | Example |
|---|---|---|
| **Acquisition** | Maps to the enabling cluster (the generic vulnerability that exposed the credential) | #2 (SQLi dumps passwords), #5 (MitM intercepts token), #9 (phishing captures password) |
| **Application** | **Always #4** — regardless of how the credential was obtained | Attacker logs in using stolen credentials → #4 |

### Attack Velocity (Δt) and Velocity Classes

Attack Velocity is the time interval between two adjacent attack steps. It is the most accurate predictor of which control types are **structurally viable** — a detection that alerts in hours is structurally insufficient if Δt between steps is minutes.

| Class | Time Range | Defender's Feasible Response Mode |
|---|---|---|
| **VC-1** | Days → Months | Strategic: Log retention, threat hunting, strategic monitoring |
| **VC-2** | Hours | Tactical: SIEM alerting, analyst triage, guided response |
| **VC-3** | Minutes | Operational: Automation (SOAR/EDR), rapid containment, prebuilt playbooks |
| **VC-4** | Seconds → Milliseconds | Real-Time: Architecture & circuit breakers, rate-limits, hardening, automatic isolation |

---

## Attack Path Notation

Complex attacks are not single events — they are **sequences**. TLCTC provides a standardized notation to map multi-step attack paths with full temporal and topological context.

### Notation Elements

| Element | Syntax | Purpose |
|---|---|---|
| Sequential step | `→` | Links cause-side steps in order |
| Parallel steps | `(#X + #Y)` | Concurrent exploitation of distinct generic vulnerabilities |
| Velocity annotation | `→[Δt=value]→` | Time interval between steps (e.g., `→[Δt=15m]→`, `→[Δt=~2h]→`) |
| Domain boundary | `\|\|[context][@Source→@Target]\|\|` | Marks where attack crosses responsibility spheres |
| Transit boundary | `\|\|[context][@Source⇒@Carrier→@Target]\|\|` | Marks intermediate carrier/relay spheres (⇒ = transit) |
| Intra-system boundary | `\|[type][@from→@to]\|` | Within-host boundary crossing (sandbox, privilege, process, hypervisor) |
| Unresolved step | `?` / `…` | Forensic uncertainty — step exists but cluster cannot yet be determined |
| Data Risk Event | `+ [DRE: C, I, A]` | Annotates consequences (never a step itself) |

### Boundary Operators

TLCTC provides three boundary operators — all are **observability annotations** that increase analytical precision without changing cluster classification.

#### Domain Boundary Operator (`||...||`)

Marks where an attack crosses between responsibility spheres (inter-organizational boundaries):
```
||[context][@Source→@Target]||
```

#### Transit Boundary Operator (`⇒`)

Identifies intermediate responsibility spheres that **relay** an attack without being its source or target:

```
||[context][@Source⇒@Carrier→@Target]||          # single transit party
||[context][@Source⇒@CarrierB⇒@CarrierA→@Target]||  # chained transit (right-to-left relay)
```

**Example:** SMS-based phishing where the SMS gateway relays the malicious link:
```
#9 ||[messaging][@Attacker⇒@SMSProvider→@Victim]||
```

> **Transit ≠ Supply Chain (#10).** Transit marks a relay/carrier that passes the attack through. #10 marks a Trust Acceptance Event — the moment a trust artifact becomes authoritative inside the target domain. An SMS provider relaying a phishing link is transit; a compromised npm package installed by the target is #10.

#### Intra-System Boundary Operator (`|[type][@from→@to]|`)

Annotates boundary crossings **within a single host or system** — as opposed to domain boundaries (`||...||`) which cross between responsibility spheres.

| Type | Description | Example |
|---|---|---|
| `sandbox` | Escape from application sandbox to host OS or less-restricted context | Browser renderer sandbox escape, container breakout |
| `privilege` | Elevation from lower to higher privilege level | User-to-root, unprivileged to kernel mode |
| `process` | Crossing from one process's security context to another | Process injection, DLL hijacking |
| `hypervisor` | Escape from VM to hypervisor or another VM | VM escape, hyperjacking |

```
#3 |[sandbox][@renderer→@os]|    # browser exploit escaping renderer sandbox
#2 |[privilege][@user→@root]|    # local privilege escalation via server-side flaw
```

#### Boundary Classification Rules

| Rule | Statement |
|---|---|
| **R-TRANSIT-3** | Vendor code running on the target device is **NOT** transit. Safari on the victim's phone is the attack surface (classify by R-ROLE as #3), not a transit party. |
| **R-INTRA-7** | Intra-system boundaries **never change** cluster classification. They are observability annotations, not classification inputs. |
| **R-INTRA-9** | The `memory` boundary type is explicitly **deferred** and MUST NOT be used. |

#### Boundary Context Vocabulary

The context vocabulary is extensible. The baseline profile defines 16 context types:

`messaging` · `email` · `cdn` · `cloud` · `network` · `signaling` · `auth` · `media` · `browser` · `exploit` · `dev` · `update` · `physical` · `human` · `legal` · `admin`

### Unresolved-Step Operators (`?`, `…`)

Incident analysis is iterative — evidence arrives over time and CTI must flow before classification is complete. Paths support two operators for forensic uncertainty:

| Operator | Name | Meaning |
|---|---|---|
| `?` | Single Unresolved Step | Exactly one step occurred at this position, but its cluster cannot yet be determined |
| `…` | Unresolved Gap | At least one step occurred in this region; both count and clusters are unknown |

**Example:** `#3 →[Δt=0s] #7 →[Δt=4h] ? →[Δt=<10m] #4 → #1`

Key rules:
- `?` and `…` are epistemic annotations, **not** clusters — they have no generic vulnerability (R-UNRES-2)
- DRE tags MUST NOT be appended to `?`/`…` (R-UNRES-5)
- Boundary operators MAY appear adjacent to `?`/`…` — boundaries are independently observable (R-UNRES-6)
- Every `?`/`…` MUST carry a prose `notes` annotation explaining what is unresolved and why (R-UNRES-8)

### Epistemic State Hierarchy

The notation carries four distinct epistemic states for a step:

| State | Syntax | Use when |
|---|---|---|
| Classified | `#X` | Cluster assigned, evidence supports it |
| Low-confidence | `#X [conf=low]` | Best-supported cluster with explicit caveat |
| Inferred | `#X [inferred]` | Not directly observed but logically required |
| Unresolved | `?` or `…` | No cluster can be defended on available evidence |

If *any* cluster can be defended — even weakly — use `#X [conf=low]`, not `?`. Reserve unresolved operators for genuine "we know something happened, we don't know what" situations.

### Example: Deconstructing "Ransomware"

"Ransomware" is not a threat — it's an **outcome label** that obscures the actual attack sequence. Here is what a typical ransomware campaign looks like in TLCTC:

**Scenario:** Phishing email delivers a malicious macro. The malware steals credentials. The attacker uses the credentials to abuse Active Directory while simultaneously deploying an encryption payload.

**TLCTC Attack Path:**
```
#9 ||[human][@External→@Org]|| →[Δt=24h] #7 →[Δt=5m] #4 →[Δt=15m] #1 → #7 + [DRE: Ac]
```

Reading this notation:
1. **#9** — Social engineering (phishing email) crosses from external to organization domain
2. **→[Δt=24h]** — 24 hours until victim opens attachment
3. **#7** — Malware executes (malicious macro runs via designed execution capability)
4. **→[Δt=5m]** — 5 minutes later, credentials are exfiltrated
5. **#4** — Stolen credentials are used (identity theft — credential application)
6. **→[Δt=15m]** — 15 minutes of lateral movement
7. **#1 → #7** — AD function abuse deploys/pushes the encryption payload (#1), then the payload executes (#7); per R-EXEC, #7 is recorded at the execution moment — after its enabler. The order is known, so this is sequential, not parallel (see White Paper §11.2.2)
8. **+ [DRE: Ac]** — Consequence: Loss of Accessibility (data exists but is unusable)

Note: The consequence is Loss of **Accessibility** (data present but encrypted/unusable), not Loss of Availability (data gone or infrastructure unreachable). This distinction matters for incident response.

### More Path Examples

**Supply chain trusted update (SolarWinds-style):**
```
#10 ||[update][@Vendor→@Org]|| →[Δt=0s] #7 →[Δt=hours] #4 →[Δt=days] #1 + [DRE: C]
```

**Physical access to interception:**
```
#8 ||[physical][@Facilities→@IT]|| → #5 → #4
```

**Federated access abuse:**
```
#4 → #10 ||[auth][@Vendor(IdP)→@Org(SP)]|| → #1
```

**SMS phishing with transit carrier:**
```
#9 ||[messaging][@Attacker⇒@SMSProvider→@Victim]|| →[Δt=1h] #7 →[Δt=5m] #4 + [DRE: C]
```

**Browser exploit with sandbox escape:**
```
#3 |[sandbox][@renderer→@os]| →[Δt=0s] #7 |[privilege][@user→@system]| →[Δt=2m] #4 + [DRE: C, I]
```

**Watering hole via compromised CDN with chained transit:**
```
#9 ||[browser][@Attacker⇒@CDN⇒@AdNetwork→@Victim]|| →[Δt=0s] #3 |[sandbox][@renderer→@os]| →[Δt=0s] #7 + [DRE: C]
```

---

## The Rosetta Stone: Translating Other Frameworks

TLCTC acts as the strategic translation layer — a shared semantic backbone that connects operational frameworks without replacing them.

### CVEs and CWEs → TLCTC

Every specific CVE is an instance of a generic vulnerability and maps to a primary TLCTC cluster. The hierarchy flows: **Weakness (CWE) → Specific Vulnerability (CVE) → Generic Vulnerability → Threat Cluster (#1–#10)**.

Example: An RCE vulnerability in Apache Struts (CVE-2017-5638) is a server-side implementation flaw → **#2 Exploiting Server**. If the exploit leads to code execution → **#2 → #7**.

The [`mappings/mitre-cwe/`](mappings/mitre-cwe/) directory contains the **mapping of 985 CWE weaknesses** to TLCTC clusters, including rationale, confidence verdicts, CVE references, and a decision tree methodology. Because CWE defines the *flaw* while TLCTC defines the *exploit vector*, the same CWE can map to different clusters depending on context (e.g., server-side vs. client-side). See the [CWE mapping README](mappings/mitre-cwe/README.md) for notation and the [decision tree](mappings/mitre-cwe/decision-tree.md) for classification methodology.

> **Note:** The CWE mapping was generated with AI assistance and is marked experimental.

### MITRE ATT&CK → TLCTC

Operational techniques map to strategic clusters based on the generic vulnerability exploited. The [`mappings/mitre-attack-enterprise/`](mappings/mitre-attack-enterprise/) directory contains the **complete mapping of 698 ATT&CK Enterprise techniques** to TLCTC clusters, including detailed rationale for each classification and a decision tree methodology.

Quick examples:
- T1566.001 "Spearphishing Attachment" → **#9 Social Engineering** (the phishing step; the payload execution is a separate #7 step)
- T1059 "Command and Scripting Interpreter" → **#7 Malware** (or #1 → #7 when legitimate tools execute attacker-controlled content)
- T1078 "Valid Accounts" → **#4 Identity Theft** (credential application)

See the [mapping README](mappings/mitre-attack-enterprise/README.md) for notation conventions, the [decision tree](mappings/mitre-attack-enterprise/decision-tree.md) for classification methodology, and the [SOC-to-risk walkthrough](mappings/mitre-attack-enterprise/examples/soc-to-risk-walkthrough.md) for a worked example.

### Sigma Detection Rules → TLCTC

Detection rules carry the strategic cluster their logic defends. The [`mappings/sigma/`](mappings/sigma/) directory contains a **per-rule TLCTC derivation of 3,132 SigmaHQ detection rules**, generated mechanically from each rule's `attack.t*` tags joined against the ATT&CK→TLCTC mapping. This lets a SOC cross-walk its detection coverage against the ten clusters — which causes are well-instrumented, and which are blind spots.

Each rule resolves to one of three states: `ok` (a single concrete cluster), `ambiguous` (the rule spans multiple clusters or an alternation), or `unmapped` (no usable ATT&CK technique tag). No rule detection bodies are reproduced — only titles, GUIDs, log sources, and the derived clusters (license-safe). The committed snapshot is rebuilt by a deterministic, dependency-free generator (`primaryCluster` is the lowest-numbered cluster in the resolved set).

See the [mapping README](mappings/sigma/README.md) for the record schema and regeneration recipe, and the [decision tree](mappings/sigma/decision-tree.md) for the resolution algorithm.

> **Note:** Like the ATT&CK and CWE mappings, the Sigma derivation inherits the experimental, AI-generated ATT&CK→TLCTC mapping.

### SARIF Scanner Findings → TLCTC

Any scanner that emits SARIF 2.1.0 (Semgrep, CodeQL, Trivy, Grype, Bandit, gosec) can be cluster-classified without a per-tool adapter. The [`integrations/sarif/`](integrations/sarif/) pack is a standalone, stdlib-only Python CLI that mines CWE/CVE identifiers from any SARIF file, classifies CWE-first against the canonical [CWE→TLCTC mapping](mappings/mitre-cwe/) with a CVE→KEV fallback, resolves ambiguous `#2 | #3` findings by file-path role (R-ROLE), and emits JSON, Markdown, or TLCTC-enriched SARIF. A `--fail-on-cluster` gate turns it into a CI check. See the [pack README](integrations/sarif/README.md) and [deploy guide](integrations/sarif/deploy.md).

### NIST CSF 2.0 → TLCTC

Controls are organized in a cluster × function matrix. NIST CSF 2.0 defines **6 functions**: GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER. GOVERN operates as the overarching strategic governance layer providing assurance controls, while the remaining 5 map directly to Bow-Tie positions:

| Bow-Tie Position | NIST CSF 2.0 Functions | Purpose |
|---|---|---|
| Strategic Oversight | **GOVERN** | Risk appetite, policies, roles — assurance controls |
| Cause Side (Prevention) | **IDENTIFY**, **PROTECT** | Reduce likelihood of cluster steps reaching the central event |
| Central Event | **DETECT** | Recognize when loss of control occurs |
| Consequence Side (Mitigation) | **RESPOND**, **RECOVER** | Contain impact, restore operations after compromise |

---

## JSON Architecture

The TLCTC JSON architecture enables **machine-readable threat intelligence sharing** through a three-layer design that separates stable definitions from dynamic incident data.

### Three-Layer Structure

| Layer | Purpose | Artifact | Scope | Update Frequency |
|---|---|---|---|---|
| **Layer 1 — Framework Definition** | Immutable "dictionary": clusters, axioms, rule IDs, topology types | `tlctc-framework.schema.json` / `tlctc-framework.v2.3.json` | Universal | Rarely (framework evolution) |
| **Layer 2 — Reference Registry** | Reusable reference objects: responsibility spheres, boundary contexts, intra-system boundary types | `tlctc-reference.schema.json` / `@Org-registry.vX.Y.Z.json` | Organization-specific | Occasionally (org changes) |
| **Layer 3 — Attack Path Instances** | Specific incidents: sequences, parallel groups, Δt, boundary annotations, DREs | `tlctc-attack-path.schema.json` / `incident-<id>.json` | Per-incident | Constantly (new incidents) |

> **Layer 4 — Risk Quantification (optional extension, *proposed*):** a FAIR bridge that quantifies financial risk over a Layer 3 attack path (Sequence Complexity Factor, Compound Threat Multipliers, Velocity-Weighted Control Effectiveness, Path Variance Analysis). It sits on top of the three core layers and is not required to use them. Schema: [`json-schemas/layer-4/tlctc-fair-risk.schema.json`](json-schemas/layer-4/tlctc-fair-risk.schema.json); rationale: [`documentation/tlctc-fair-integration-proposal.md`](documentation/tlctc-fair-integration-proposal.md).

### Design Principles

- **Separation of meaning from measurement** — Layer 1 defines *what a cluster is*; Layer 3 records *what happened*. Incident records must not redefine clusters.
- **Strict validation** — Schemas use `additionalProperties: false`. Non-standard fields go in `extensions` objects.
- **Linear + parallel modeling** — Attack paths are ordered sequences of `attack_step` and `parallel_group` entries.
- **R-EXEC enforcement** — Steps carry `fec_executed` and `fec_recorded_in_step_id` fields to ensure FEC execution is always recorded.

---

## Agent-Consumable Knowledge: the OKF Bundle

The [`okf/`](okf/) directory packages the entire taxonomy as an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) bundle (OKF v0.1) — a tree of markdown files with YAML frontmatter, built so LLM agents and RAG pipelines can consume TLCTC directly. It is a **rendered view** generated from the canonical JSON schemas, whitepaper, and tools; those remain the single source of truth.

- **412 concept documents**: clusters (the six-field whitepaper definitions), axioms, rules, Layer-2 spheres/contexts, 247 glossary terms, 51 attack paths (notation + step tables), and ATT&CK/CWE/Sigma mappings grouped by cluster.
- **Governance controls section**: pairs the NIST CSF control objectives with the full **60-cell ISO 27001:2022 Annex A** control matrix (every cluster × function, local + umbrella), the **CDE → COE → ECR** effectiveness model with the Detection Coverage Score, and the KRI/KCI/KPI indicator hierarchy.
- **Regenerate & validate**: `npm run validate` chains `validate-framework` → `build-okf` → `validate-okf` (SPEC conformance). The rebuild is deterministic. See [`okf/README.md`](okf/README.md).

> **Note:** The ISO 27001 Annex A control placements and the CWE mapping carry starter / AI-assisted provenance notes — guidance, not certified control sets.

---

## Axioms

TLCTC relies on 10 non-negotiable axioms organized into four groups. These prevent the category errors that plague cybersecurity language.

| # | Axiom | Group | Core Statement |
|---|---|---|---|
| I | No System-Type Differentiation | Scope | Generic IT assets; sector labels (SCADA, IoT, cloud) don't create new threat classes |
| II | Client–Server Model | Scope | All networked interaction can be modeled as client–server at one or more layers |
| III | Causes, Not Outcomes | Separation | Threats ≠ data risk events. "Data breach" is never a threat category |
| IV | Not Threat Actors | Separation | Threats ≠ actor identity. "APT" is not a cluster |
| V | Not Control Failure | Separation | Control-risk ≠ threat category. A missing patch is not a threat |
| VI | Single-Cluster Rule | Classification | One step = one generic vulnerability = one cluster (non-overlap) |
| VII | Initial-Vulnerability Rule | Classification | Each attack vector is defined by the generic vulnerability it initially targets |
| VIII | Strategic–Operational Layering | Classification | Clusters have sub-threats (strategic → operational decomposition) |
| IX | Sequence + Velocity | Sequences | Clusters chain into attack paths; Δt measures velocity between steps |
| X | Credential Duality | Sequences | Credential acquisition and application are distinct steps with distinct classifications |

---

## Repository Contents

```
tlctc/
├── mappings/
│   ├── mitre-attack-enterprise/              # MITRE ATT&CK Enterprise → TLCTC
│   │   ├── README.md                         # Mapping documentation & notation
│   │   ├── tlctc-enterprise-attack.json      # 698 technique mappings with rationale
│   │   ├── decision-tree.md                  # Classification methodology
│   │   └── examples/
│   │       └── soc-to-risk-walkthrough.md    # Worked example: SOC → risk register
│   ├── mitre-cwe/                            # MITRE CWE → TLCTC (experimental)
│   │   ├── README.md                         # Mapping documentation & verdict system
│   │   ├── tlctc-cwe.json                    # 985 CWE mappings with rationale & CVE refs
│   │   ├── decision-tree.md                  # Classification methodology
│   │   └── examples/
│   │       └── cwe-to-control-walkthrough.md # Worked example: vuln findings → controls
│   ├── npm-supply-chain/                     # npm supply chain patterns → TLCTC
│   │   ├── README.md                         # Pattern documentation & methodology
│   │   ├── tlctc-npm-patterns.json           # Supply chain attack patterns mapping
│   │   └── examples/
│   │       └── incident-to-control-walkthrough.md # Worked example: incident → controls
│   ├── cloudflare-2026-patterns/             # Cloudflare 2026 attack patterns → TLCTC
│   │   ├── README.md                         # Pattern documentation & methodology
│   │   └── tlctc-cloudflare-2026-patterns.json # Cloudflare 2026 threat report pattern mapping
│   ├── cisa-kev/                             # CISA Known Exploited Vulnerabilities → TLCTC
│   │   ├── README.md                         # Mapping documentation & caveats
│   │   ├── generate-kev-mapping.py           # Deterministic ETL generator
│   │   ├── tlctc-kev.json                    # 1,568 per-CVE derivations
│   │   ├── tlctc-kev-stats.json              # Cluster counts, ransomware, vendor & monthly stats
│   │   ├── product-role-heuristic.json       # R-ROLE (#2 | #3) disambiguation rules
│   │   ├── decision-tree.md                  # Derivation algorithm
│   │   ├── input/                            # Pinned KEV snapshot (reproducibility)
│   │   └── examples/
│   │       └── cluster-exposure-walkthrough.md # Worked example: vendor stack → exposure
│   ├── mandiant-2026/                        # Mandiant M-Trends 2026 ATT&CK → TLCTC
│   │   └── tlctc-mandiant-2026-attck-mapping.json # Mandiant 2026 technique mapping
│   ├── splunk-cisco/                         # Splunk/Cisco Top-50 comparison
│   │   └── splunk-top50-tlctc-comparison.html # Interactive Splunk Top-50 vs TLCTC view
│   └── sigma/                                # SigmaHQ detection rules → TLCTC
│       ├── README.md                         # Mapping documentation & caveats
│       ├── generate-sigma-mapping.py         # Deterministic ETL generator (PyYAML)
│       ├── tlctc-sigma.json                  # 3,132 per-rule derivations
│       ├── tlctc-sigma-stats.json            # Cluster distribution & status counts
│       ├── decision-tree.md                  # Derivation algorithm
│       └── tests/                            # Generator unit tests
├── json-schemas/
│   ├── layer-1/                              # Framework Definition (Static)
│   │   ├── tlctc-framework.schema.json       # Schema for framework packages
│   │   └── tlctc-framework.v2.3.json         # V2.3 citable baseline: clusters, axioms, 16 rules
│   ├── layer-2/                              # Reference Registry (Context)
│   │   ├── tlctc-reference.schema.json       # Schema for reference registries
│   │   └── example-registry.json             # Example org-specific registry
│   ├── layer-3/                              # Attack Path Instances (Dynamic)
│   │   ├── tlctc-attack-path.schema.json     # Schema for attack path instances
│   │   └── examples/
│   │       ├── solarwinds-2020.json          # SolarWinds supply chain incident
│   │       ├── chalk-debug-2025.json         # npm phishing campaign incident
│   │       ├── midnight-blizzard-microsoft-2024.json # Midnight Blizzard → Microsoft OAuth pivot
│   │       └── unresolved-step-example-2026.json # Unresolved-step operators (?/…) reference
│   ├── layer-4/                              # FAIR Risk Quantification (Risk)
│   │   ├── tlctc-fair-risk.schema.json       # Schema for FAIR risk assessment instances
│   │   └── examples/
│   │       └── scattered-spider-2024-fair.json # SCATTERED SPIDER FAIR risk assessment
│   └── operational/                          # Operational sub-cluster enumeration (evolving)
│       ├── tlctc-operational-enumeration.schema.json # Schema for the enumeration
│       └── tlctc-operational-enumeration.json # TLCTC-XX.YY catalogue (JSON twin of the md)
├── grammar/                                  # Standalone ABNF grammar for path notation
│   ├── README.md                             # Grammar documentation & tooling notes
│   └── tlctc-attack-path.abnf                # ABNF grammar for TLCTC attack-path syntax
├── scripts/                                  # Build & validation tooling (Node.js)
│   ├── build-pdf.js                          # markdown → text PDF (marked + puppeteer)
│   ├── validate-framework.js                 # ajv JSON Schema validator
│   ├── build-okf.js                          # canonical sources → OKF bundle (okf/)
│   └── validate-okf.js                       # OKF SPEC conformance checker
├── okf/                                      # Open Knowledge Format bundle (agent-consumable; generated by scripts/build-okf.js)
│   ├── README.md                             # Bundle provenance & regeneration recipe
│   ├── index.md / log.md                     # OKF reserved navigation & changelog
│   ├── clusters/ axioms/ rules/              # Framework dictionary (one markdown doc per concept)
│   ├── spheres/ contexts/                    # Layer-2 registry (responsibility spheres, boundary contexts)
│   ├── glossary/                             # 247 term docs
│   ├── attack-paths/                         # 51 incident path docs (notation + step tables)
│   ├── controls/                             # NIST CSF × ISO 27001 matrix, effectiveness model, indicators
│   └── mappings/                             # ATT&CK / CWE / Sigma grouped by cluster
├── documentation/
│   ├── tlctc-v2.3-core.md                    # ⭐ Citable core paper (v2.3) — canonical definition
│   ├── tlctc-v2.3-core.pdf                   # PDF of the core paper (citation target)
│   ├── tlctc-v2.3-application.md             # Application & governance companion (v2.3)
│   ├── tlctc-v2.3-application.pdf            # PDF of the application paper
│   ├── tlctc-v2.3-traceability.md            # v2.1 → v2.3 consolidation traceability
│   ├── tlctc-operational-enumeration.md      # Evolving TLCTC-XX.YY sub-cluster catalogue
│   ├── tlctc-v2.0-whitepaper.md              # Extended practitioner handbook (v2.1 content; filename kept for link stability)
│   ├── tlctc-v2.0-whitepaper.pdf             # PDF export of the white paper
│   ├── tlctc-glossary.md                     # Comprehensive definitions
│   ├── tlctc-glossary.pdf                    # PDF export of the glossary
│   ├── tlctc-ti-sharing-profile.md           # TI Sharing — Extension Profile (companion)
│   ├── tlctc-fair-integration-proposal.md    # FAIR integration proposal (Layer 4 spec)
│   ├── tlctc-cve-extension-proposal.md       # CVE extension proposal
│   ├── tlctc-replication-notation-proposal.md # Replication notation (×N fan-out / ×* self-propagation) — conceptual proposal (v0.1)
│   ├── tlctc-plus-ncsc-proposal.md           # TLCTC+ national reporting extension — policy proposal (v0.1)
│   ├── tlctc-plus-specification.md           # TLCTC+ implementation specification (v0.3) — grammar, conformance, catalogues
│   ├── propagated-controls.md                # Managing controls over event chains — generalizes Propagated PR to BCM, contractual, and policy sources
│   ├── npm-supply-chain-blog-final.md        # npm supply chain threat analysis
│   ├── Why Exactly Ten_ — TLCTC Framework Architecture.pdf # Framework architecture rationale
│   └── images/                               # Diagrams and visual assets
│       ├── tlctc-bowtie-anchor-diagram.svg
│       ├── tlctc-consequence-chain.svg
│       ├── tlctc-cyber-bow-tie.svg
│       ├── tlctc-dual-layer-bowtie-overview.svg
│       └── tlctc-dual-layer-naming.svg
├── tools/
│   ├── README.md                             # Tool index & JSON format reference
│   ├── threat-modeling.html                  # SDLC threat modeling & architecture analysis
│   ├── attack-path-architect.html            # Incident attack path documentation & CTI exchange
│   ├── actor-profile-designer.html           # Threat actor capability profiling & comparison (573 actors: 59 expert-scored + 514 ETDA heuristic-scored)
│   ├── actor-story-designer.html             # Threat intelligence story/narrative builder
│   ├── radar-tlctc-app.html                  # Interactive threat radar visualization & assessment
│   ├── tech-enablers-radar.html              # Technology enabler radar for emerging threat vectors
│   ├── control-matrix.html                   # NIST CSF 2.0 × TLCTC control matrix with maturity scoring
│   ├── attck-explorer.html                   # MITRE ATT&CK technique explorer with TLCTC mapping
│   ├── attck-phase-heatmap.html              # ATT&CK phase heatmap visualization
│   ├── cwe-explorer.html                     # CWE weakness explorer with TLCTC mapping
│   ├── cbp-app.html                          # Cluster-based prioritization application
│   ├── cbp-starter.json                      # Cluster-based prioritization starter dataset
│   ├── control-matrix-starter.json           # NIST CSF control-matrix starter
│   ├── control-matrix-starter-iso27001.json  # ISO 27001 control-matrix starter
│   ├── control-matrix-starter-cloudflare-2026.json # Cloudflare-2026 control-matrix starter
│   ├── score_etda.py                         # ETDA→TLCTC scoring engine: tool arsenal + description mining, calibrated against expert data
│   ├── generate-cs2026-report.js             # CrowdStrike-2026 report generator
│   ├── generate-iso27001-starter.py          # ISO 27001 control-matrix starter generator
│   ├── replace-cdn.sh                        # CDN link rewrite helper
│   └── examples/                             # Starter templates & real-world example datasets
│       ├── template-threat-model.json        # Blank threat model starter
│       ├── template-attack-path.json         # Blank attack path starter
│       ├── template-actor-profile.json       # Blank actor profile starter
│       ├── CTA-CrowdStrike2025.json          # CrowdStrike 2025 Global Threat Report actors
│       ├── CTA-CrowdStrike2026.json          # CrowdStrike 2026 Global Threat Report actors
│       ├── CTA-Cloudflare-2026.json          # Cloudflare 2026 threat actors
│       ├── CTA-Mandiant-2026.json            # Mandiant M-Trends 2026 threat actors
│       ├── CTA-Google-APT-Groups.json        # Google APT group profiles
│       ├── CTA-NCSC-SituationRadar-2024-2025.json  # NCSC Situation Radar threat data
│       ├── CTA-NCSC-TAC-Profiles.json        # NCSC threat actor capability profiles
│       ├── radar-cloudflare-2026.json        # Cloudflare 2026 radar dataset
│       ├── radar-crowdstrike-2026.json       # CrowdStrike 2026 radar dataset
│       ├── radar-mandiant-2026.json          # Mandiant 2026 radar dataset
│       ├── radar-mandiant-2026-industries.json # Mandiant 2026 industry-specific radar
│       ├── stories-cloudflare-2026.json      # Cloudflare 2026 threat narratives
│       ├── stories-crowdstrike-2026.json     # CrowdStrike 2026 threat narratives
│       ├── stories-mandiant-2026.json        # Mandiant 2026 threat narratives
│       ├── control-matrix-cloudflare-2026.json # Cloudflare 2026 control matrix
│       ├── control-matrix-crowdstrike-2026.json # CrowdStrike 2026 control matrix
│       ├── control-matrix-mandiant-2026.json # Mandiant 2026 control matrix
│       ├── tech-enablers-horizon-2026.json   # Technology enablers horizon scan 2026
│       ├── tech-enablers-agentic-focus-2026.json # Agentic AI technology enablers 2026
│       ├── ncsc-google-2024-JB-bericht*.json # NCSC/Google 2024 annual report datasets (5 files)
│       └── npm-*.json                        # npm supply chain incident examples (3 files)
├── integrations/                             # External-tool deployments (operational)
│   ├── README.md                             # Index of available integration packs
│   ├── cortex-xsoar/                         # Cortex XSOAR 6.2.x per-object YAML/JSON pack
│   ├── cortex-xsoar-8/                       # Cortex XSOAR 8.x / XSIAM Marketplace Content Pack
│   ├── sonarqube/                            # SonarQube & SonarCloud sidecar (Python CLI + declarative starter)
│   └── sarif/                                # Generic SARIF 2.1.0 classifier (Python CLI, stdlib only)
├── glossary/
│   ├── tlctc-glossary.schema.json            # Schema for universal cyber security glossary
│   └── tlctc-glossary.json                   # 72 terms: clusters, axioms, rules, notation, architecture, boundary operators
├── agentic-ai/                               # Analysis of AI semantics in Cyber Threats
│   ├── README.md                             # Overview and methodology
│   ├── agentic-consequence-chains.json       # Consequence chain examples
│   ├── agentic-tool-profiles.json            # 5 tool category risk profiles
│   ├── agentic-irreversibility-matrix.json   # Irreversibility windows per consequence type
│   └── attack-paths/                         # 10 individual agentic AI attack paths (A–J)
│       ├── path-A-direct-prompt-injection.json
│       ├── path-B-indirect-prompt-injection.json
│       ├── path-C-social-engineering-operator.json
│       ├── path-D-credential-access.json
│       ├── path-E-agent-as-lolbin.json
│       ├── path-F-runtime-exploit.json
│       ├── path-G-rogue-agent-install.json
│       ├── path-H-supply-chain-marketplace.json
│       ├── path-I-apt-in-a-box.json
│       └── path-J-llm-weaponization-supply-chain.json
├── attack-paths/                             # Community-contributed incident analyses (50 incidents)
│   ├── CONTRIBUTING.md
│   ├── # Canonical pattern reference
│   ├── ad-domain-admin-cascade-2025.json     # Active Directory Domain-Admin → ransomware #1-cascade (composite pattern: Lynx, Storm-2603, Storm-0300/Akira)
│   ├── # Historical incidents (2008–2024)
│   ├── agent-btz-usb-2008.json               # USB worm (2008)
│   ├── watering-hole-iphonedevsdk-2013.json   # Watering hole (2013)
│   ├── darkhotel-wifi-2014.json               # Hotel Wi-Fi (2014)
│   ├── ubiquiti-bec-2015.json                 # BEC wire fraud (2015)
│   ├── ukraine-power-grid-2015.json           # ICS power grid (2015)
│   ├── uber-breach-2016.json                  # Credential stuffing (2016)
│   ├── mirai-botnet-2016.json                 # IoT botnet (2016)
│   ├── capital-one-2019.json                  # SSRF cloud (2019)
│   ├── credential-stuffing-2020.json          # Credential stuffing (2020)
│   ├── twitter-hack-2020.json                 # Social engineering (2020)
│   ├── colonial-pipeline-2021.json            # Ransomware (2021)
│   ├── pegasus-forcedentry-2021.json          # Zero-click exploit (2021)
│   ├── okta-lapsus-2022.json                  # Supply chain (2022)
│   ├── lockbit-byovd-2023.json                # BYOVD ransomware (2023)
│   ├── cloudflare-http-ddos-2023.json         # HTTP/2 DDoS (2023)
│   ├── tesla-insider-2023.json                # Insider threat (2023)
│   ├── tesla-k8s-cryptojacking-2018.json      # K8s cryptojacking (2018)
│   ├── lojax-uefi-2018.json                   # UEFI rootkit (2018)
│   ├── change-healthcare-2024.json            # Healthcare ransomware (2024)
│   ├── # Cloudflare 2026 Threat Report sourced (13 incidents)
│   ├── grub1-saas-pivot-2025.json             # GRUB1 Salesloft/Drift SaaS pivot
│   ├── opencode-exploit-chain-2025.json       # OpenCode AI IDE RCE chain
│   ├── frumpytoad-toughprogress-2025.json     # FrumpyToad ToughProgress phishing
│   ├── nastyshrew-ukraine-2025.json           # NastyShrew Ukraine espionage
│   ├── rottenshrew-signal-2025.json           # RottenShrew Signal device linking
│   ├── clumsytoad-snakedisk-2025.json         # ClumsyToad SnakeDisk USB wiper
│   ├── punytoad-f5-bigip-2025.json            # PunyToad F5 BIG-IP exploitation
│   ├── nk-it-worker-infiltration-2025.json    # DPRK IT worker infiltration scheme
│   ├── infostealer-ransomware-pipeline-2025.json # Infostealer → IAB → ransomware pipeline
│   ├── aisuru-ddos-2025.json                  # Aisuru botnet DDoS-for-hire
│   ├── authorized-insider-extortion-2025.json # Authorized insider extortion
│   ├── bot-chain-lifecycle-2025.json          # Bot chain lifecycle (IoT → proxy)
│   ├── raccoon-phaas-aitm-2025.json          # Raccoon PhaaS AiTM credential theft
│   ├── # Mandiant M-Trends 2026 sourced (6 incidents)
│   ├── mandiant-handoff-ransomware-2025.json  # Infostealer → IAB → ransomware hand-off
│   ├── mandiant-multi-year-espionage-2025.json # Multi-year espionage campaign
│   ├── mandiant-saas-cascade-2025.json        # SaaS token cascade
│   ├── mandiant-edge-device-exploitation-2025.json # Edge device exploitation
│   ├── mandiant-esxi-virtualization-2025.json # ESXi VMDK-mount credential dump
│   ├── mandiant-recovery-denial-2025.json     # Recovery denial ransomware
│   ├── # CrowdStrike 2026 Global Threat Report sourced (8 incidents)
│   ├── scattered-spider-unmanaged-vm-2025.json # SCATTERED SPIDER unmanaged VM credential dump
│   ├── pressure-chollima-bybit-2025.json      # PRESSURE CHOLLIMA Bybit $1.46B supply chain
│   ├── fancy-bear-lamehug-2025.json           # FANCY BEAR LAMEHUG LLM-enabled malware
│   ├── blockade-spider-embargo-2025.json      # BLOCKADE SPIDER cross-domain Embargo ransomware
│   ├── cozy-bear-oauth-ngo-2025.json          # COZY BEAR multi-day OAuth phishing
│   ├── chatty-spider-lawfirm-2025.json        # CHATTY SPIDER 4-minute law firm intrusion
│   ├── punk-spider-smb-encryption-2025.json   # PUNK SPIDER remote SMB encryption via IoT
│   ├── famous-chollima-beavertail-2025.json   # FAMOUS CHOLLIMA fake recruiter npm + BeaverTail
│   ├── # npm ecosystem sourced (3 incidents)
│   ├── s1ngularity-nx-2025.json               # S1ngularity NX npm campaign
│   ├── chalk-debug-phishing-2025.json         # chalk-debug npm phishing
│   └── shai-hulud-worm-2025.json              # ShaiHulud self-propagating npm worm
└── LICENSE                                   # CC BY 4.0
```

## Getting Started

1. **Read the core paper** — [`documentation/tlctc-v2.3-core.md`](documentation/tlctc-v2.3-core.md) is the canonical, citable definition: derivation, clusters, axioms, rules, and notation in one self-contained paper.
2. **Read the axioms** — They are the non-negotiable foundation. If you skip them, you'll misclassify.
3. **Understand the Bow-Tie** — Threats are causes, outcomes are consequences. Never confuse them.
4. **Practice with attack paths** — Take any recent incident report and decompose it into TLCTC notation. The [Application Paper](documentation/tlctc-v2.3-application.md) walks the procedure end-to-end.
5. **Use the JSON schemas** — Validate your attack path instances against Layer 3 schema.
6. **Explore the ATT&CK mapping** — See [`mappings/mitre-attack-enterprise/`](mappings/mitre-attack-enterprise/) to understand how operational techniques translate to strategic clusters.
7. **Explore the CWE mapping** — See [`mappings/mitre-cwe/`](mappings/mitre-cwe/) to connect vulnerability findings to threat clusters.
8. **Track active exploitation** — See [`mappings/cisa-kev/`](mappings/cisa-kev/) for a TLCTC-cluster view of the CISA Known Exploited Vulnerabilities catalog (1,568 CVEs, weekly-refreshable, deterministically derived).
9. **Audit your detection coverage** — See [`mappings/sigma/`](mappings/sigma/) for a per-rule TLCTC cluster derivation of 3,132 SigmaHQ detection rules — cross-walk your SOC ruleset against the strategic cluster model.
10. **Use the glossary** — See [`glossary/`](glossary/) for precise, machine-readable definitions of all TLCTC terms and cyber security vocabulary.
11. **Learn the boundary and epistemic operators** — The [White Paper](https://www.tlctc.net/tlctc-v2.0-whitepaper.html) covers transit boundaries, intra-system boundaries, unresolved-step operators, and the epistemic state hierarchy.
12. **Read the extension proposals** — TLCTC+ has two paired documents: [`tlctc-plus-ncsc-proposal.md`](documentation/tlctc-plus-ncsc-proposal.md) (v0.1 policy proposal — the *why*) and [`tlctc-plus-specification.md`](documentation/tlctc-plus-specification.md) (v0.3 implementation spec — the *how*: grammar, conformance, BRE/PATTERN/IMPACT/REPORT catalogues, JSON formats). For other framework extensions, see [`tlctc-cve-extension-proposal.md`](documentation/tlctc-cve-extension-proposal.md) (CVE enrichment), [`tlctc-fair-integration-proposal.md`](documentation/tlctc-fair-integration-proposal.md) (FAIR risk quantification), and [`tlctc-replication-notation-proposal.md`](documentation/tlctc-replication-notation-proposal.md) (replication notation — ×N fan-out / ×* self-propagation, conceptual).
13. **Deploy an integration** — See [`integrations/`](integrations/) to operationalise TLCTC inside the tools your team already runs. Available packs: Cortex XSOAR 6.2.x and 8.x / XSIAM (incident triage + Layer 3 emission), SonarQube + SonarCloud (SAST findings → cluster tags via a Python sidecar against the canonical CWE→TLCTC mapping), and the generic SARIF classifier (any SARIF 2.1.0 producer → TLCTC clusters; CWE-first with CVE→KEV fallback; stdlib-only).
14. **Feed an LLM agent** — Point a RAG pipeline or agent at the [`okf/`](okf/) Open Knowledge Format bundle (markdown + YAML frontmatter) rendering the whole taxonomy — clusters, axioms, rules, glossary, attack paths, controls, and mappings — for machine consumption. Regenerate with `npm run validate`.

## Contributing

We welcome community contributions, particularly:
- **Attack path mappings** of real-world incidents using TLCTC notation
- **Framework integration examples** (MITRE ATT&CK mappings, NIST CSF control matrices)
- **Tooling** that consumes or produces TLCTC JSON (see [`tools/`](tools/) for existing standalone apps)
- **Integrations** that operationalise TLCTC inside vendor platforms (see [`integrations/`](integrations/) for the Cortex XSOAR and SonarQube packs as reference shapes)
- **Glossary terms** — propose new terms or refine definitions for the universal cyber security glossary

See [`attack-paths/CONTRIBUTING.md`](attack-paths/CONTRIBUTING.md) for guidelines.

## Resources

| Resource | Description |
|---|---|
| [Core Paper v2.3](documentation/tlctc-v2.3-core.md) ([PDF](documentation/tlctc-v2.3-core.pdf)) | The canonical, citable definition of the framework |
| [Application Paper v2.3](documentation/tlctc-v2.3-application.md) ([PDF](documentation/tlctc-v2.3-application.pdf)) | Classification in practice, governance, controls, and indicators |
| [tlctc.net](https://tlctc.net) | Official TLCTC website with documentation, visuals, and tools |
| [White Paper](https://www.tlctc.net/tlctc-v2.0-whitepaper.html) | Extended practitioner handbook: boundary logic, epistemic operators, and complete notation specification |
| [barnes.ch](https://barnes.ch) | Author's site with foundational analysis on cybersecurity's language problem |

## How to Cite

> Kreinz, B. (2026). *A Cause-Oriented Cyber Threat Taxonomy: The Top Level Cyber Threat Clusters Framework* (Version 2.3.0) [Preprint]. Zenodo. https://doi.org/10.5281/zenodo.20633177

```bibtex
@misc{kreinz2026tlctc,
  author    = {Kreinz, Bernhard},
  title     = {A Cause-Oriented Cyber Threat Taxonomy: The Top Level
               Cyber Threat Clusters Framework},
  year      = {2026},
  version   = {2.3.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20633177},
  url       = {https://doi.org/10.5281/zenodo.20633177}
}
```

## License

All TLCTC framework definitions, notations, axioms, and JSON architectures are licensed under **[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**.

You are free to share and adapt this material for any purpose, including commercial use, provided you give appropriate attribution.

---

*TLCTC was created by Bernhard Kreinz to solve cybersecurity's fundamental language problem — because you cannot manage what you cannot consistently name.*
