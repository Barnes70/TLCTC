# TLCTC → STIX 2.1 Exporter

One-way exporter that converts a TLCTC Layer 3 attack-path JSON into a STIX 2.1 `bundle`. The bundle is importable by STIX-aware tools such as MITRE D3FEND CAD; cluster classification, velocity, boundaries, and DRE outcomes are preserved as `x_tlctc_*` custom properties.

## Usage

```
node export-stix.js <input.json> [--out <output.json>]
node export-stix.js --pilot     # SolarWinds + AD cascade
node export-stix.js --all       # every file in attack-paths/*.json
```

Default output location: `attack-paths/stix/<input-basename>.stix.json`.

## Tests

```
node export-stix.test.js
```

Round-trips the SolarWinds and AD-cascade fixtures and asserts cluster IDs, Δt edges, boundary fields, DRE outcomes, FEC flags, and unresolved-step semantics survive in the bundle.

## STIX object mapping

| TLCTC element | STIX object | Notes |
|---|---|---|
| `metadata` | `report` SDO | top-level report; `object_refs` covers all bundle objects |
| `attack_step` | `attack-pattern` SDO | classified step; cluster ID surfaces in `external_references[source_name=tlctc]` |
| `parallel_group` | `grouping` SDO with `context: "tlctc-parallel"` | members listed in `object_refs` |
| `unresolved_step` (`?` / `…`) | `attack-pattern` with `x_tlctc_status: "unresolved"` | no `x_tlctc_cluster`, no `x_tlctc_dre` (R-UNRES-2/5) |
| Sequence edge | `relationship` SDO with `relationship_type: "related-to"`, `x_tlctc_relation: "precedes"` | `x_tlctc_delta_t` carries the Δt of the *transition*, not of either step |
| ATT&CK enrichment | `attack-pattern` SDO + `derived-from` `relationship` | best-effort: only emitted when a `Txxxx` / `Txxxx.NNN` ID is found in `evidence_refs` or `notes` |

## Custom property reference

All custom properties are prefixed `x_tlctc_` per STIX 2.1 §3.4.

| Property | Where it appears | Source field |
|---|---|---|
| `x_tlctc_step_id` | step SDOs | `step_id` |
| `x_tlctc_cluster` | classified step SDOs | `cluster` (e.g., `#7`, `TLCTC-07.03`) |
| `x_tlctc_strategic_cluster` | classified step SDOs | `#1`–`#10` derived from `cluster` |
| `x_tlctc_dre` | classified step SDOs | `outcomes` (subset of `C`/`I`/`A`/`Ac`) |
| `x_tlctc_fec` | classified step SDOs | `fec_executed` |
| `x_tlctc_fec_recorded_in_step_id` | classified step SDOs | `fec_recorded_in_step_id` |
| `x_tlctc_boundary` | step SDOs | `topology_boundary` (object: `context`, `source_sphere`, `target_sphere`, `transit_spheres`) |
| `x_tlctc_intra_boundaries` | step SDOs | `intra_system_boundaries` |
| `x_tlctc_evidence_refs` | step SDOs | `evidence_refs` |
| `x_tlctc_status` | unresolved step SDOs | always `"unresolved"` |
| `x_tlctc_unresolved_type` | unresolved step SDOs | `unresolved_type` (`single` or `gap`) |
| `x_tlctc_estimated_count` | unresolved step SDOs | `estimated_count` |
| `x_tlctc_candidates` | unresolved step SDOs | `candidates` (informational only per R-UNRES-9) |
| `x_tlctc_relation` | relationship / grouping SDOs | `"precedes"` or `"parallel"` |
| `x_tlctc_delta_t` | relationship SDOs | `delta_t_to_next` of the predecessor step |
| `x_tlctc_group_id` | grouping SDOs | `group_id` |
| `x_tlctc_attck_technique` | enrichment SDOs | matched ATT&CK ID |
| `x_tlctc_enrichment_basis` | enrichment SDOs | string describing how the link was derived |
| `x_tlctc_incident_id` / `x_tlctc_version` / `x_tlctc_analyst_confidence` / `x_tlctc_framework_ref` / `x_tlctc_framework_sha256` / `x_tlctc_registry_ref` / `x_tlctc_registry_sha256` | report SDO | from `metadata` |

## Known limitations

- **One-way.** STIX → TLCTC is out of scope for v1; CAD-edited graphs would not produce valid Layer 3 paths back without analyst review.
- **ATT&CK enrichment is best-effort.** Techniques are only attached when a `Txxxx` ID is mentioned in `evidence_refs` or `notes`. We do not auto-explode cluster→technique using the full 698-row mapping (would create noise; cluster is many-to-one with techniques, so reverse-mapping has low signal).
- **No `extension-definition` SDO.** Custom properties use the `x_*` form allowed by STIX 2.1. A future v1.1 may publish a hosted `extension-definition` for stricter consumers.
- **Spheres are opaque to STIX-only consumers.** Layer 2 sphere identifiers (`@Org`, `@Vendor`, etc.) are preserved verbatim inside `x_tlctc_boundary` but have no STIX-native equivalent. Consumers without TLCTC awareness will see them as labels.
- **Δt is on the edge, not the step.** Matches the notation (`→[Δt=…]→` is a *transition* between steps). Tools that visualize node-level dwell time will need to read the relationship SDO.
