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
- **`metadata.tlctc_version`** — Must be `"2.0"`
- **`metadata.framework_ref`** — Must reference `"tlctc-framework.v2.0.json"`
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
- **Outcome tags** (`outcomes`) — Annotate Data Risk Events (C, I, A) where they occur.
- **Source attribution** — Cite your sources in `metadata.notes` (vendor advisories, CISA alerts, academic papers, threat intel reports).

### Quality Checks

Before submitting:

- [ ] JSON is syntactically valid
- [ ] File validates against `tlctc-attack-path.schema.json`
- [ ] All `step_id` values are unique within the document
- [ ] R-EXEC compliance: every `fec_executed: true` has a corresponding #7 step
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
