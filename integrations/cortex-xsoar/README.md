# TLCTC Integration for Cortex XSOAR 6.2

Operationalizes the TLCTC v2.1 taxonomy inside Cortex XSOAR 6.2.
Playbooks, classifier, custom fields, automations, and a Layer 3 emitter
sufficient to ship a working integration.

> **Target version:** Cortex XSOAR **6.2.x** (on-prem and cloud).
> Object exports use the 6.2 native YAML/JSON formats. Will not import on 8.x / XSIAM without conversion.
>
> **For XSOAR 8.x or Cortex XSIAM, use the sibling build:** [`../cortex-xsoar-8/`](../cortex-xsoar-8/) — same functional scope, packaged as a Marketplace Content Pack.

---

## What this integration does

1. **Tags every incident with its TLCTC cluster at ingestion** — using a classifier + mapper that reads ATT&CK technique IDs from the alert and looks up the TLCTC cluster.
2. **Routes incidents to ten cluster-scoped master playbooks**, not outcome-scoped ones — `TLCTC-01-AbuseOfFunctions` through `TLCTC-10-SupplyChain`. (Axiom III: classify by cause, not outcome.)
3. **Branches response by Velocity Class** — VC-4 records-only (EDR enforces), VC-3 auto-contains, VC-2 human-gated, VC-1 hands off to threat hunting.
4. **Enforces classification splits** — automations apply R-EXEC, R-CRED, R-SUPPLY, R-ROLE so a single ATT&CK technique like T1566.001 fires both #9 and #7 playbooks in sequence.
5. **Emits a Layer 3 attack-path JSON on close** that validates against `json-schemas/layer-3/tlctc-attack-path.schema.json` — for archival, learning, and cross-incident pattern analysis.
6. **Triggers Propagated PR (regulatory) controls** through the RS Container sub-playbook — GDPR Art. 33 fires only when DRE includes Confidentiality on PII; NIS2 Art. 23 fires when E1 (System Compromise) is reached.

---

## Repository layout

```
integrations/cortex-xsoar/
├── README.md                       # this file
├── deploy.md                       # step-by-step install runbook
├── test-cases.md                   # validation scenarios with expected behavior
├── incident-fields/                # custom incident fields (TLCTC fields)
├── incident-types/                 # "TLCTC Threat" incident type
├── layouts/                        # incident layout exposing TLCTC fields
├── classifiers/                    # ATT&CK→TLCTC classifier + mapper
├── lists/                          # ATT&CK→TLCTC lookup list
├── automations/                    # Python helpers (classification, Layer 3 emitter)
└── playbooks/                      # 10 master playbooks + 2 sub-playbooks
```

---

## Install order

Strict order — later objects reference earlier ones.

1. `lists/attck-tlctc-lookup.json`
2. `incident-fields/*.json`
3. `incident-types/tlctc-threat.json`
4. `layouts/tlctc-threat-layout.json`
5. `automations/TLCTCClassify.yml`
6. `automations/TLCTCEmitLayer3.yml`
7. `classifiers/attck-tlctc-classifier.json` + `classifiers/attck-tlctc-mapper.json`
8. `playbooks/sub-velocity-router.yml`
9. `playbooks/sub-rs-container.yml`
10. `playbooks/TLCTC-01-AbuseOfFunctions.yml` … `playbooks/TLCTC-10-SupplyChain.yml`

See `deploy.md` for the click-by-click runbook (XSOAR 6.2 paths and required RBAC).

---

## How it maps to TLCTC concepts

| TLCTC concept | XSOAR object |
|---|---|
| Cluster (#1–#10) | Custom incident field `tlctc_cluster` + one master playbook per cluster |
| Operational ID (TLCTC-XX.YY) | Custom incident field `tlctc_operational_id` (machine-readable correlation key) |
| Δt (Attack Velocity) | Custom incident field `tlctc_delta_t` + Velocity-Class router sub-playbook |
| Velocity Class (VC-1…VC-4) | Custom incident field `tlctc_velocity_class` — drives auto vs human-gated tasks |
| Boundary `||[context][@Source→@Target]||` | Custom incident field `tlctc_boundary` (JSON object matching Layer 3 schema) |
| DRE (C/I/A/Av/Ac) | Custom incident field `tlctc_dre` (multi-select) |
| RS Container (Direct + Propagated PR) | `sub-rs-container.yml` sub-playbook |
| Layer 3 Attack Path | Custom incident field `tlctc_attack_path` (JSON) — emitted on close |

---

## Non-goals

- Not a content pack for the XSOAR Marketplace. Ship as a private content pack (`Settings → Configurations → Custom Content`).
- Does not replace ATT&CK content; it sits *above* it and forces cluster-level reasoning.
- Does not implement detection — assumes alerts arrive from EDR/SIEM with ATT&CK technique IDs already attached.

---

## References (in this repo)

- Framework: `json-schemas/layer-1/tlctc-framework.v2.0.json`
- Layer 3 schema: `json-schemas/layer-3/tlctc-attack-path.schema.json`
- ATT&CK→TLCTC mapping (source for the lookup list): `mappings/mitre-attack-enterprise/`
- Glossary (RS Container, Velocity Class, Operational Notation): `documentation/tlctc-glossary.md`
- Whitepaper: `documentation/tlctc-v2.0-whitepaper.md`
