# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TLCTC (Top Level Cyber Threat Clusters) v2.0 is a cause-oriented, axiomatic cyber threat taxonomy framework. It classifies threats by **why** compromise happens (the generic vulnerability exploited), not by what happens (outcomes like "ransomware" or "data breach"). Licensed under CC BY 4.0.

## Repository Structure

This is a taxonomy/specification project — no build system, package manager, or test runner. The deliverables are JSON schemas, JSON data files, and PDF documentation.

- **`json-schemas/layer-1/`** — Framework definition (immutable). `tlctc-framework.v2.0.json` contains the 10 cluster definitions, 10 axioms, and 6 classification rules.
- **`json-schemas/layer-2/`** — Reference registry (context). Organization-specific responsibility spheres and boundary contexts.
- **`json-schemas/layer-3/`** — Attack path instances (dynamic). Schema and examples for mapping real incidents.
- **`attack-paths/`** — Community-contributed incident analyses (Layer 3 instances).
- **`examples/agentic-ai/`** — Agentic AI threat analysis with 9 individual attack path files (in `attack-paths/`), consequence chains, tool profiles, and irreversibility matrices.
- **`mappings/mitre-attack-enterprise/`** — Complete MITRE ATT&CK Enterprise → TLCTC mapping (698 techniques) with decision tree and SOC walkthrough.
- **`mappings/mitre-cwe/`** — MITRE CWE → TLCTC mapping (987 weaknesses, AI-generated, experimental) with verdict system, decision tree, and control walkthrough.
- **`tools/`** — Standalone HTML applications (threat modeling, etc.). Single-file, no build system, open in browser.
- **`documentation/`** — PDF white papers and specifications.

## Validation

JSON files validate against their respective schemas (JSON Schema Draft 7). To validate:
```bash
# Using any JSON Schema validator, e.g. ajv-cli
ajv validate -s json-schemas/layer-3/tlctc-attack-path.schema.json -d attack-paths/incident.json
```

## Three-Layer JSON Architecture

- **Layer 1 (Static):** Framework dictionary — clusters, axioms, rules. Rarely changes.
- **Layer 2 (Context):** Reference registries — responsibility spheres (@Org, @Vendor, @External), boundary contexts (human, physical, update, auth, dev, api, cloud). Org-specific.
- **Layer 3 (Dynamic):** Attack path instances — individual incident analyses with step sequences, velocity annotations, and outcomes.

## The 10 Clusters

Exactly 10 non-overlapping clusters: #1 Abuse of Functions, #2 Exploiting Server, #3 Exploiting Client, #4 Identity Theft, #5 Man in the Middle, #6 Flooding Attack, #7 Malware, #8 Physical Attack, #9 Social Engineering, #10 Supply Chain Attack. Clusters #1–#7 are "internal" topology; #8–#10 are "bridge" topology (cross domain boundaries).

## Critical Classification Rules

When creating or reviewing attack path JSON, these rules are non-negotiable:

- **Axiom III:** Threats are causes, not outcomes. "Ransomware" is not a cluster step — the payload execution is #7, the impact is `[DRE: A]`.
- **Axiom VI (Single-Cluster Rule):** One step = one generic vulnerability = one cluster. If a step maps to two clusters, split it.
- **R-EXEC:** If Foreign Executable Content executes, a #7 step with `fec_executed: true` MUST be recorded at the execution moment.
- **Axiom X (Credential Duality):** Credential acquisition maps to the enabling cluster; credential use is always #4. These are separate steps.
- **R-CRED:** Credential acquisition maps to the enabling cluster. Credential application (use of the credential to authenticate) is ALWAYS classified as #4 Identity Theft, regardless of the acquisition method. These are separate attack steps.
- **R-SUPPLY:** #10 is placed at the Trust Acceptance Event — the moment the trust artifact becomes authoritative inside the target domain.
- **R-ROLE:** Classify by the role of the flawed component relative to the attacker: server-role = #2, client-role = #3.
- **Axiom IV:** Actor identity must never determine cluster classification.

## Attack Path Notation

```
#9 ||[human][@External→@Org]|| →[Δt=24h] #7 →[Δt=5m] #4 →[Δt=15m] (#1 + #7) + [DRE: A]
```

- `→` sequential step; `(#X + #Y)` parallel execution
- `→[Δt=value]→` attack velocity between steps
- `||[context][@Source→@Target]||` boundary crossing (required for bridge clusters #8, #9, #10)
- `+ [DRE: C, I, A, Ac]` data risk events (C=Confidentiality, I=Integrity, A=Availability, Ac=Accessibility)
- Velocity classes: VC-1 (days–months), VC-2 (hours), VC-3 (minutes), VC-4 (seconds–ms)

## Contributing Attack Paths

New attack path files go in `attack-paths/`, named `incident-name-year.json`. Must validate against the Layer 3 schema, follow all classification rules above, and include source citations in `metadata.notes`. See `attack-paths/CONTRIBUTING.md` and the SolarWinds example at `json-schemas/layer-3/examples/solarwinds-2020.json` as reference.
