# TLCTC Content Pack — Cortex XSOAR 8.x + Cortex XSIAM

A Marketplace-format Content Pack that operationalizes the TLCTC v2.1 taxonomy
inside **Cortex XSOAR 8.x** and **Cortex XSIAM** from a single artifact.

> **Targets:** XSOAR 8.0+ (`marketplaces: ["xsoar"]`) and XSIAM (`marketplaces: ["marketplacev2"]`).
> Same playbooks, automations, fields, and classifier on both.
> For XSOAR 6.2 see the parallel build under `integrations/cortex-xsoar/`.

---

## What this pack does

Identical functional scope to the 6.2 build:

1. **Tags every incident with its TLCTC cluster at ingestion** via classifier + mapper that read ATT&CK technique IDs from the alert and apply the lookup list.
2. **Routes incidents to ten cluster-scoped master playbooks** — `TLCTC-01-AbuseOfFunctions` through `TLCTC-10-SupplyChain` (Axiom III: classify by cause, not outcome).
3. **Branches response by Velocity Class** — VC-4 record-only (EDR), VC-3 auto-contain, VC-2 human-gated, VC-1 hand off to threat hunting.
4. **Enforces classification splits** — automations apply R-EXEC, R-CRED, R-SUPPLY, R-ROLE so a single ATT&CK technique like T1566.001 fires both #9 and #7 playbooks.
5. **Emits a Layer 3 attack-path JSON on close** that validates against `json-schemas/layer-3/tlctc-attack-path.schema.json`.
6. **Triggers Propagated PR (regulatory) controls** through the RS Container sub-playbook — GDPR Art. 33 fires when DRE includes Confidentiality on PII; NIS2 Art. 23 fires when severity ≥ significant.

---

## Differences from the 6.2 build

| Aspect | 6.2 (`integrations/cortex-xsoar/`) | 8.x + XSIAM (this pack) |
|---|---|---|
| Format | Per-object JSON/YAML uploaded individually | Single Marketplace Content Pack |
| Layout | `layout` object (legacy) | `LayoutsContainer` (8.x format) |
| Incident fields | One combined JSON | One file per field (sdk convention) |
| Scripts | Python embedded in YAML | YAML metadata + sibling `.py` source |
| Docker image | `demisto/python3:3.10` | `demisto/python3:3.11.10` |
| Server min version | 6.2.0 | 8.0.0 |
| Marketplaces | n/a | `["xsoar", "marketplacev2"]` |
| Install | Click-by-click (25 steps) | `demisto-sdk upload` or Marketplace zip |

Behaviour is identical. The same 5 test cases (`test-cases.md`) pass on both.

---

## Repository layout

```
integrations/cortex-xsoar-8/
├── pack_metadata.json
├── README.md
├── deploy.md
├── test-cases.md
├── ReleaseNotes/
│   └── 1_0_0.md
├── IncidentFields/                 # 10 files, one per field
├── IncidentTypes/
├── Layouts/                        # LayoutsContainer
├── Classifiers/                    # classifier + incoming mapper
├── Lists/                          # ATT&CK->TLCTC lookup
├── Scripts/
│   ├── script-TLCTCClassify/       # .yml + .py
│   └── script-TLCTCEmitLayer3/     # .yml + .py
└── Playbooks/                      # dispatch + 2 subs + 10 masters
```

---

## How TLCTC concepts map to pack objects

| TLCTC concept | Object |
|---|---|
| Cluster (#1–#10) | `IncidentFields/incidentfield-tlctccluster.json` + cluster master playbook |
| Operational ID (TLCTC-XX.YY) | `IncidentFields/incidentfield-tlctcoperationalid.json` |
| Δt (Attack Velocity) | `IncidentFields/incidentfield-tlctcdeltat.json` + `Playbooks/playbook-sub-velocity-router.yml` |
| Velocity Class (VC-1…VC-4) | `IncidentFields/incidentfield-tlctcvelocityclass.json` |
| Boundary `||[ctx][@Src→@Tgt]||` | `IncidentFields/incidentfield-tlctcboundary.json` |
| DRE (C/I/A/Ac) | `IncidentFields/incidentfield-tlctcdre.json` |
| RS Container (Direct + Propagated PR) | `Playbooks/playbook-sub-rs-container.yml` |
| Layer 3 Attack Path | `IncidentFields/incidentfield-tlctcattackpath.json` (emitted by `Scripts/script-TLCTCEmitLayer3`) |

---

## References

- Framework: `json-schemas/layer-1/tlctc-framework.v2.3.json`
- Layer 3 schema: `json-schemas/layer-3/tlctc-attack-path.schema.json`
- ATT&CK→TLCTC mapping (lookup source): `mappings/mitre-attack-enterprise/tlctc-enterprise-attack.json`
- Glossary (RS Container, Velocity Class, Operational Notation): `documentation/tlctc-glossary.md`
- Whitepaper: `documentation/tlctc-v2.0-whitepaper.md`
