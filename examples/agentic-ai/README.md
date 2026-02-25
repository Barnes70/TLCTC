# TLCTC v2.0 — Agentic AI Examples

Machine-readable implementation artefacts for the TLCTC Agentic AI analysis.

## Source Papers

These examples accompany two papers that apply the TLCTC v2.0 framework to agentic AI:

1. **"Agentic AI Under the Microscope"** — Cause-side analysis (left side of the Bow-Tie).  
   Demonstrates that all agentic AI threats decompose into the established 10 clusters, with two primary scenarios: #1 Abuse of Functions (legitimate agent compromised) and #7 Malware (malicious agent introduced). Introduces the two-layer attack surface model (Layer 1: generic software vulnerabilities; Layer 2: AI-specific manifestations of #1).

2. **"The Consequence Amplifier"** — Consequence-side analysis (right side of the Bow-Tie).  
   Analyses how agentic AI's tool access, autonomous decision-making, and multi-system integration amplify consequence patterns through three structural properties: Velocity Amplification, Scope Amplification, and Autonomy Amplification. Introduces consequence chain notation and the irreversibility problem.

Both papers are available at [tlctc.net](https://tlctc.net).

## File Structure

| File | Contents | TLCTC Layer |
|------|----------|-------------|
| `agentic-attack-paths.json` | 9 attack paths (Paths A–I) from Paper 1 | Layer 3 (Instance) |
| `agentic-consequence-chains.json` | Consequence chain examples from Paper 2 | Extension (consequence-side) |
| `agentic-tool-profiles.json` | 5 tool category risk profiles | Layer 2 (Reference) |
| `agentic-irreversibility-matrix.json` | Irreversibility windows per consequence type | Layer 2 (Reference) |

## Relationship to TLCTC JSON Architecture

These files follow the three-layer architecture defined in §7 of the TLCTC v2.0 specification:

- **Layer 1 (Framework Definition):** Referenced via `framework_ref`, not duplicated. All files point to `tlctc-framework.v2.0.json` as the authoritative cluster definitions.
- **Layer 2 (Reference Registry):** `agentic-tool-profiles.json` and `agentic-irreversibility-matrix.json` extend the reference registry with agentic AI-specific context data.
- **Layer 3 (Attack Path Instances):** `agentic-attack-paths.json` contains instance-level attack path records following the canonical schema.

The consequence chain file (`agentic-consequence-chains.json`) is a **proposed extension** to the TLCTC JSON architecture for recording effect-side event sequences. It maintains strict Axiom III discipline: consequence chains are notated separately from attack paths, using the `C:` prefix to mark consequence-side notation. This extension is under development and may evolve.

## Validation

Attack path instances can be validated against the canonical schema:

```bash
# Validate against tlctc-attack-sequence-schema.json
python scripts/validate_attack_path.py agentic-attack-paths.json
```

## Usage

These examples serve three purposes:

1. **Educational:** Demonstrate how the TLCTC framework applies to agentic AI scenarios.
2. **Template:** Provide starting points for organisations performing their own agentic AI threat analysis.
3. **Machine-readable:** Enable automated ingestion by SIEMs, risk registers, and threat intelligence platforms.

## License

CC BY 4.0 — Bernhard Kreinz / [tlctc.net](https://tlctc.net)
