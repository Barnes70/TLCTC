# TLCTC npm Supply Chain Attack Patterns

Canonical attack path patterns for npm supply chain incidents, decomposed into TLCTC threat cluster sequences.

## Purpose

The npm ecosystem is structurally revealing for supply chain analysis. Developers and CI pipelines delegate trust to package names, version ranges, lockfile state, registry metadata, maintainer accounts, and provenance signals. When that trust is abused, the industry labels the result a "supply chain attack" — a label that names the boundary crossed but says nothing about the mechanisms that made the crossing possible.

This mapping decomposes common npm attack archetypes into their constituent TLCTC clusters, making each mechanism — and its corresponding control surface — explicit.

## Files

| File | Contents |
|------|----------|
| `tlctc-npm-patterns.json` | 5 canonical attack path patterns with cluster decompositions and control mappings |
| `examples/incident-to-control-walkthrough.md` | Worked example: Chalk/Debug 2025 incident decomposed to actionable controls |

## The 5 Patterns

| ID | Pattern | Notation | Vector |
|----|---------|----------|--------|
| NPM-PAT-001 | Canonical Install-Time Compromise | `#10 → #1 → #7` | Development |
| NPM-PAT-002 | Maintainer Account Compromise via Phishing | `#9 → #4 → #1 → #10 → #1 → #7` | Update |
| NPM-PAT-003 | Typosquatting | `#9 → #10 → #1 → #7` | Development |
| NPM-PAT-004 | Build-to-Secret-Theft (Full Chain) | `#10 → #1 → #7 → #1 → #4 → #1` | Development |
| NPM-PAT-005 | Self-Replicating Worm | `#10 → #1 → #7 → #1 → #7 → #1 → #4 → #1 → #10 → [RECURSIVE]` | Update |

## Key Structural Findings

**#10 is a trust boundary, not a mechanism.** In every pattern, #10 marks the Trust Acceptance Event — once per propagation hop. The mechanisms are #9, #1, #4, and #7.

**The #1 between #10 and #7 is the most undertapped control surface.** The package manager's processing step (resolve, download, unpack) has its own controls — namespace policies, install sandboxing, `--ignore-scripts` — structurally distinct from trust governance (#10) and execution control (#7).

**R-CRED exposes a universal kill chain.** Every pattern with credential theft follows: acquisition via one cluster, then use via #4. Controls at the #4 boundary (hardware MFA, token scoping, publish approval) break every campaign regardless of acquisition method.

**#1 is the silent majority.** Across all five patterns, #1 steps outnumber every other cluster. Modern npm attacks work overwhelmingly by using legitimate functions for unintended purposes.

## Attack Vectors

- **Update Vector (#10.1):** Poisoned versions pushed through an existing package's update channel. Consumers with permissive semver ranges (`^x.y.z`, `~x.y.z`) are affected. Controls: lockfile pinning, staged updates.
- **Development Vector (#10.2):** Malicious dependency pulled during pre-deployment dependency resolution. Controls: dependency review, provenance checking, namespace policies.

## Relationship to Attack Path Instances

These patterns are abstract templates. Concrete incident analyses (Layer 3 instances) based on these patterns are available in:

- `attack-paths/s1ngularity-nx-2025.json` — NPM-PAT-001 + NPM-PAT-004
- `attack-paths/chalk-debug-phishing-2025.json` — NPM-PAT-002
- `attack-paths/shai-hulud-worm-2025.json` — NPM-PAT-005
- `json-schemas/layer-3/examples/chalk-debug-2025.json` — NPM-PAT-002 (reference example)

## Notation

| Operator | Meaning |
|----------|---------|
| `#X → #Y` | Sequential: X enables Y |
| `||[ctx][@A→@B]||` | Inter-organizational domain boundary |
| `||[ctx][@A⇒@T→@B]||` | Transit boundary: T is carrier infrastructure |
| `+ [DRE: X]` | Data Risk Event (C/I/A/Ac) |
| `[RECURSIVE]` | Cyclic propagation — path loops back |

## License

CC BY 4.0 — Bernhard Kreinz / [tlctc.net](https://tlctc.net)
