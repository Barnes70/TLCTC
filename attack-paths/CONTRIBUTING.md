# Contributing Attack Path Analyses

Thank you for contributing to the TLCTC attack path library. Community-contributed incident analyses are how we build a shared, comparable body of threat intelligence.

## Before You Start

Read these documents first:

1. The **V2.0 White Paper** — particularly Sections 2 (Canonical Cluster Definitions), 3 (Attack Path Notation), and 4 (Attack Velocity)
2. The **Layer 3 schema** at `json-schemas/layer-3/tlctc-attack-path.schema.json`
3. The **SolarWinds example** at `json-schemas/layer-3/examples/solarwinds-2020.json` as a reference implementation

## Submission Requirements

### File Format

Every submission must be a valid JSON file conforming to the Layer 3 attack path schema. Name your file descriptively: `incident-name-year.json` (e.g., `moveit-2023.json`, `log4shell-2021.json`).

### Mandatory Fields

- **`metadata.incident_id`** — Unique identifier for the incident
- **`metadata.analyst_confidence`** — `low`, `medium`, or `high`
- **`metadata.tlctc_version`** — Must be `"2.0"` or `"2.1"`
- **`metadata.framework_ref`** — Must reference `"tlctc-framework.v2.3.json"`
- **`metadata.notes`** — Must include the compact attack path notation and source attribution

### Classification Rules

These are non-negotiable. Submissions that violate them will be rejected.

1. **One step = one cluster** (Axiom VI). If your step maps to two clusters, split it into two steps.
2. **Cause-side only** (Axiom III). Do not use cluster labels for outcomes. "Ransomware" is not a step — the encryption payload execution is #7 or #1, and the impact is `[DRE: A]`.
3. **R-EXEC compliance**. If FEC executes at any point, there must be a #7 step with `fec_executed: true` at the execution moment. Do not absorb execution into the enabling cluster.
4. **Credential dual nature** (Axiom X). Credential acquisition maps to the enabling cluster. Credential use is always #4. These are separate steps.
5. **Actor-agnostic** (Axiom IV). You may mention attribution in notes, but actor identity must never determine cluster classification.

### Recommended Fields

- **Velocity annotations** (`delta_t_to_next`) — Include at least velocity class estimates (VC-1/2/3/4) even if precise timestamps are unavailable. Use `~` for estimates, `?` for unknown.
- **Domain boundary operators** (`topology_boundary`) — Required for bridge cluster steps (#8, #9, #10). Include context and sphere identifiers.
- **Transit boundaries** (`transit_spheres`) — If the attack relays through an intermediate carrier (e.g., SMS provider, CDN), record transit spheres in the boundary. Note: vendor code running on the target device is NOT transit (R-TRANSIT-3).
- **Intra-system boundaries** (`intra_system_boundaries`) — If a step involves within-host boundary crossings (sandbox escape, privilege escalation, process injection, VM escape), annotate with the appropriate type, from, and to fields.
- **Outcome tags** (`outcomes`) — Annotate Data Risk Events (C, I, A) where they occur.
- **Source attribution** — Cite your sources in `metadata.notes` (vendor advisories, CISA alerts, academic papers, threat intel reports).

### Handling Forensic Uncertainty (V2.1)

Incident analysis is iterative — submissions based on live or evolving investigations are welcome. If evidence confirms a step exists but you cannot yet classify it, use the **unresolved-step** variant instead of guessing (see whitepaper §11.5.4):

- Use `"status": "unresolved"` with `"unresolved_type": "single"` for a single unresolved step (maps to the `?` operator).
- Use `"status": "unresolved"` with `"unresolved_type": "gap"` for a region of activity where step count and clusters are unknown (maps to the `…` operator).
- `cluster` and `outcomes` MUST be absent (R-UNRES-2, R-UNRES-5).
- `notes` is **required** and must explain what is unresolved and why (R-UNRES-8).
- `candidates` is informational only — if any candidate can be individually defended on the evidence, classify the step instead and annotate with `[conf=low]` in prose (R-UNRES-9, binary classification).
- Velocity and boundary annotations are permitted on unresolved steps (R-UNRES-4, R-UNRES-6) — timing and boundary crossings are often observable even when cluster classification is not.

See `json-schemas/layer-3/examples/unresolved-step-example-2026.json` for a canonical reference. Unresolved steps SHOULD be replaced with classified steps as evidence matures (R-UNRES-7) — a path is a living artifact, correct now, more correct later.

### Quality Checks

Before submitting:

- [ ] JSON is syntactically valid
- [ ] File validates against `tlctc-attack-path.schema.json`
- [ ] All `step_id` values are unique within the document
- [ ] R-EXEC compliance: every `fec_executed: true` has a corresponding #7 step
- [ ] R-TRANSIT-3 compliance: vendor code on target device is not marked as transit (e.g., Safari on victim's phone is #3, not a transit party)
- [ ] R-INTRA-7 compliance: intra-system boundaries are observability annotations only — they do not change cluster classification
- [ ] R-UNRES compliance (if unresolved steps are present): every unresolved step has a prose `notes` annotation; `cluster` and `outcomes` are absent; `candidates` is informational only and no single candidate can be individually defended
- [ ] Boundary annotations use sphere IDs from the example registry (or clearly document custom spheres)
- [ ] The compact notation in `metadata.notes` matches the JSON path sequence
- [ ] Sources are cited

## How to Submit

1. Fork the repository
2. Create your attack path JSON file in the `attack-paths/` directory
3. Validate against the schema
4. Submit a Pull Request with a brief description of the incident and your analytical reasoning

## What Makes a Good Submission

The best submissions are incidents where TLCTC notation reveals something that traditional classification obscures. For example:

- An attack labeled "ransomware" that actually involves 5 distinct cluster steps with different velocity classes, showing where detection windows exist
- A "supply chain attack" where precise boundary operator placement clarifies which organization was responsible for which failure
- An incident where the credential dual nature distinction changes the control mapping

## Questions?

Open an issue with the "Framework Question" label if you're unsure about a classification decision. The TLCTC framework has tie-breaker rules for ambiguous cases — we'd rather discuss edge cases publicly than have silent misclassification.
