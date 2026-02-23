# Top Level Cyber Threat Clusters (TLCTC)

**Version 2.0** · CC BY 4.0 · [tlctc.net](https://tlctc.net) · [White Paper](https://tlctc.net/whitepaper)

The first cause-oriented, axiomatic cyber threat taxonomy.

TLCTC provides the missing semantic foundation for cybersecurity: a stable, non-overlapping classification of cyber threats based on **why** compromise happens — the generic vulnerability exploited — rather than **what** happens afterwards (outcomes like "data breach," "ransomware," or "denial of service").

> *A cyber threat is defined by the generic vulnerability it exploits, not by who performs it and not by what consequence follows.*

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
| **#2** | **Exploiting Server** | Server-side implementation flaws that enable unintended behavior | Internal |
| **#3** | **Exploiting Client** | Client-side implementation flaws that enable unintended behavior | Internal |
| **#4** | **Identity Theft** | Weak identity management processes and/or inadequate credential protection mechanisms | Internal |
| **#5** | **Man in the Middle** | Lack of sufficient control, integrity protection, or confidentiality over the communication path | Internal |
| **#6** | **Flooding Attack** | Finite capacity limitations inherent in any system component | Internal |
| **#7** | **Malware** | The software environment's designed capability to execute potentially untrusted foreign code | Internal |
| **#8** | **Physical Attack** | Physical accessibility of infrastructure and exploitability of physical-layer properties | Bridge |
| **#9** | **Social Engineering** | Human psychological factors (trust, fear, urgency, authority bias, curiosity, fatigue) | Bridge |
| **#10** | **Supply Chain Attack** | Trust in third-party components, services, and update channels can be subverted | Bridge |

### Canonical Definitions

- **#1 Abuse of Functions** — An attacker abuses the logic or scope of existing, legitimate software functions for malicious purposes without exploiting a code flaw. Inputs remain data; no foreign code is introduced or executed.

- **#2 Exploiting Server** — An attacker targets flaws within the server-side application's source code implementation (e.g., SQL injection, buffer overflows), forcing an **unintended data→code transition**. The execution path was never designed to exist.

- **#3 Exploiting Client** — An attacker targets flaws within the source code implementation of any software acting in a client role (e.g., browser, PDF reader, email client), forcing an **unintended data→code transition**.

- **#4 Identity Theft** — An attacker misuses authentication credentials (passwords, tokens, keys, session identifiers) to impersonate a legitimate identity. This cluster focuses on the **use** of credentials — acquisition maps to the enabling cluster (see Credential Dual Nature below).

- **#5 Man in the Middle (MitM)** — An attacker intercepts, modifies, or relays communication between two parties by exploiting a privileged position on the communication path.

- **#6 Flooding Attack** — An attacker intentionally overwhelms system resources or exceeds capacity limits (network, CPU, memory, API quotas) through volume or intensity, causing denial of service.

- **#7 Malware** — An attacker abuses the inherent ability of a software environment to execute foreign executable content (malicious code, scripts, commands, or illegitimate introduction of dual-use tools executing attacker-controlled content). Uses **intended** execution capabilities.

- **#8 Physical Attack** — An attacker gains unauthorized physical interaction with or causes physical interference to hardware, facilities, data media, interfaces, or signals.

- **#9 Social Engineering** — An attacker psychologically manipulates individuals into performing actions counter to their security interests. This is exclusively about human manipulation.

- **#10 Supply Chain Attack** — An attacker compromises systems by targeting vulnerabilities within third-party software, hardware, services, or update mechanisms that are trusted and integrated by the target. Placed at the **Trust Acceptance Event (TAE)**.

---

## Key V2.0 Concepts

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
| Data Risk Event | `+ [DRE: C, I, A]` | Annotates consequences (never a step itself) |

### Example: Deconstructing "Ransomware"

"Ransomware" is not a threat — it's an **outcome label** that obscures the actual attack sequence. Here is what a typical ransomware campaign looks like in TLCTC:

**Scenario:** Phishing email delivers a malicious macro. The malware steals credentials. The attacker uses the credentials to abuse Active Directory while simultaneously deploying an encryption payload.

**TLCTC Attack Path:**
```
#9 ||[human][@External→@Org]|| →[Δt=24h] #7 →[Δt=5m] #4 →[Δt=15m] (#1 + #7) + [DRE: A]
```

Reading this notation:
1. **#9** — Social engineering (phishing email) crosses from external to organization domain
2. **→[Δt=24h]** — 24 hours until victim opens attachment
3. **#7** — Malware executes (malicious macro runs via designed execution capability)
4. **→[Δt=5m]** — 5 minutes later, credentials are exfiltrated
5. **#4** — Stolen credentials are used (identity theft — credential application)
6. **→[Δt=15m]** — 15 minutes of lateral movement
7. **(#1 + #7)** — Simultaneous abuse of AD functions (#1) and encryption payload execution (#7)
8. **+ [DRE: A]** — Consequence: Loss of Accessibility (data exists but is unusable)

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

---

## The Rosetta Stone: Translating Other Frameworks

TLCTC acts as the strategic translation layer — a shared semantic backbone that connects operational frameworks without replacing them.

### CVEs → TLCTC

Every specific CVE is an instance of a generic vulnerability and maps to a primary TLCTC cluster. The hierarchy flows: **Weakness (CWE) → Specific Vulnerability (CVE) → Generic Vulnerability → Threat Cluster (#1–#10)**.

Example: An RCE vulnerability in Apache Struts (CVE-2017-5638) is a server-side implementation flaw → **#2 Exploiting Server**. If the exploit leads to code execution → **#2 → #7**.

### MITRE ATT&CK → TLCTC

Operational techniques map to strategic clusters based on the generic vulnerability exploited. Examples:
- T1566.001 "Spearphishing Attachment" → **#9 Social Engineering** (the phishing step; the payload execution is a separate #7 step)
- T1059 "Command and Scripting Interpreter" → **#7 Malware** (or #1 → #7 when legitimate tools execute attacker-controlled content)
- T1078 "Valid Accounts" → **#4 Identity Theft** (credential application)

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
| **Layer 1 — Framework Definition** | Immutable "dictionary": clusters, axioms, rule IDs, topology types | `tlctc-framework.schema.json` / `tlctc-framework.v2.0.json` | Universal | Rarely (framework evolution) |
| **Layer 2 — Reference Registry** | Reusable reference objects: responsibility spheres, boundary contexts | `tlctc-reference.schema.json` / `@Org-registry.vX.Y.Z.json` | Organization-specific | Occasionally (org changes) |
| **Layer 3 — Attack Path Instances** | Specific incidents: sequences, parallel groups, Δt, boundary annotations, DREs | `tlctc-attack-path.schema.json` / `incident-<id>.json` | Per-incident | Constantly (new incidents) |

### Design Principles

- **Separation of meaning from measurement** — Layer 1 defines *what a cluster is*; Layer 3 records *what happened*. Incident records must not redefine clusters.
- **Strict validation** — Schemas use `additionalProperties: false`. Non-standard fields go in `extensions` objects.
- **Linear + parallel modeling** — Attack paths are ordered sequences of `attack_step` and `parallel_group` entries.
- **R-EXEC enforcement** — Steps carry `fec_executed` and `fec_recorded_in_step_id` fields to ensure FEC execution is always recorded.

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
├── json-schemas/
│   ├── layer-1/                          # Framework Definition (Static)
│   │   ├── tlctc-framework.schema.json   # Schema for framework packages
│   │   └── tlctc-framework.v2.0.json     # V2.0 content: clusters, axioms, rules
│   ├── layer-2/                          # Reference Registry (Context)
│   │   ├── tlctc-reference.schema.json   # Schema for reference registries
│   │   └── example-registry.json         # Example org-specific registry
│   └── layer-3/                          # Attack Path Instances (Dynamic)
│       ├── tlctc-attack-path.schema.json # Schema for attack path instances
│       └── examples/                     # Example incident mappings
│           └── solarwinds-2020.json
├── documentation/
│   ├── TLCTC-v2.0-whitepaper.pdf         # Canonical V2.0 White Paper
│   ├── TLCTC-glossary-v2.0.pdf           # Comprehensive Definitions
│   ├── json-architecture.pdf             # JSON Architecture Specification
│   └── why-exactly-ten.pdf               # Framework Architecture Rationale
├── attack-paths/                         # Community-contributed incident analyses
│   └── CONTRIBUTING.md
└── LICENSE                               # CC BY 4.0
```

## Getting Started

1. **Read the axioms** — They are the non-negotiable foundation. If you skip them, you'll misclassify.
2. **Understand the Bow-Tie** — Threats are causes, outcomes are consequences. Never confuse them.
3. **Practice with attack paths** — Take any recent incident report and decompose it into TLCTC notation.
4. **Use the JSON schemas** — Validate your attack path instances against Layer 3 schema.

## Contributing

We welcome community contributions, particularly:
- **Attack path mappings** of real-world incidents using TLCTC notation
- **Framework integration examples** (MITRE ATT&CK mappings, NIST CSF control matrices)
- **Tooling** that consumes or produces TLCTC JSON

See [`attack-paths/CONTRIBUTING.md`](attack-paths/CONTRIBUTING.md) for guidelines.

## Resources

| Resource | Description |
|---|---|
| [tlctc.net](https://tlctc.net) | Official TLCTC website with documentation, visuals, and tools |
| [V2.0 White Paper](https://tlctc.net/whitepaper) | Canonical definitions, boundary logic, and complete specification |
| [barnes.ch](https://barnes.ch) | Author's site with foundational analysis on cybersecurity's language problem |

## License

All TLCTC framework definitions, notations, axioms, and JSON architectures are licensed under **[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**.

You are free to share and adapt this material for any purpose, including commercial use, provided you give appropriate attribution.

---

*TLCTC was created by Bernhard Kreinz to solve cybersecurity's fundamental language problem — because you cannot manage what you cannot consistently name.*
