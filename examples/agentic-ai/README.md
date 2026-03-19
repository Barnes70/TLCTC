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
| `attack-paths/path-A-direct-prompt-injection.json` | Path A — Direct Prompt Injection (#1→#1) | Layer 3 (Instance) |
| `attack-paths/path-B-indirect-prompt-injection.json` | Path B — Indirect Prompt Injection (#1→#1→#1) | Layer 3 (Instance) |
| `attack-paths/path-C-social-engineering-operator.json` | Path C — Social Engineering of Operator (#9→#1) | Layer 3 (Instance) |
| `attack-paths/path-D-credential-access.json` | Path D — Credential Access (#4→#1→#1) | Layer 3 (Instance) |
| `attack-paths/path-E-agent-as-lolbin.json` | Path E — Agent as LOLBin (#1→#7) | Layer 3 (Instance) |
| `attack-paths/path-F-runtime-exploit.json` | Path F — Runtime Exploit (#3→#7→#1) | Layer 3 (Instance) |
| `attack-paths/path-G-rogue-agent-install.json` | Path G — Rogue Agent Install (#9→#7→#1) | Layer 3 (Instance) |
| `attack-paths/path-H-supply-chain-marketplace.json` | Path H — Supply Chain Marketplace (#10→#7→#1) | Layer 3 (Instance) |
| `attack-paths/path-I-apt-in-a-box.json` | Path I — APT-in-a-Box (#7→#4→#1) | Layer 3 (Instance) |
| `attack-paths/path-J-llm-weaponization-supply-chain.json` | Path J — LLM Weaponization via Supply Chain (#10→#1→#7→#1→#7→#1) | Layer 3 (Instance) |
| `agentic-consequence-chains.json` | Consequence chain examples from Paper 2 | Extension (consequence-side) |
| `agentic-tool-profiles.json` | 5 tool category risk profiles | Layer 2 (Reference) |
| `agentic-irreversibility-matrix.json` | Irreversibility windows per consequence type | Layer 2 (Reference) |

## Scenarios

The 10 attack paths cover two primary scenarios:

- **LegitimateAgentCompromised** (Paths A–F): The AI agent is authorised software with designed capabilities. The primary cluster is #1 Abuse of Functions: the generic vulnerability is the inherent trust, scope, and complexity designed into the agent's functionality. Control strategy: constrain the functional domain (least privilege, capability boundaries, instruction hierarchy, context isolation).

- **MaliciousAgentIntroduced** (Paths G–I): The AI agent itself IS the Foreign Executable Content. The primary cluster is #7 Malware: the generic vulnerability is the environment's designed capability to execute untrusted content. Control strategy: prevent unauthorised execution (allow-listing, code signing, sandboxing, marketplace governance).

- **AgentWeaponizedByMalware** (Path J): The AI agent is legitimate software discovered and co-opted post-compromise by external malware. The agent serves as a LOLBin — its designed code execution capabilities become an attacker force multiplier. Unlike Paths A–F (direct compromise) and G–I (malicious introduction), the agent is a secondary tool in a broader supply chain campaign. Based on the S1ngularity/Nx real-world precedent (August 2025). Control strategy: capability restrictions on agent execution (sandboxing, output filtering, invocation authentication).

## Attack Surface Layers

- **Layer 1 (Generic Software):** The agent runtime as generic software: file parsing, HTTP handling, deserialisation, memory management, network connections. Subject to every generic vulnerability that applies to any software asset (Axiom I: no system-type differentiation). Applicable clusters: #2, #3, #4, #5, #6.

- **Layer 2 (AI-Specific):** Attack vectors that exist because the software asset is an LLM-based agent: prompt injection, training data poisoning, model extraction, hallucination exploitation. Novel manifestations of existing generic vulnerabilities — not novel clusters. All map to #1 (function abuse), potentially combined with #10 (supply chain) for third-party training data. Applicable clusters: #1, #10.

## DRE Short Forms

Data Risk Event (DRE) canonical short forms used in attack path outcomes:

- **C** = Confidentiality
- **I** = Integrity
- **A** = Availability
- **Ac** = Accessibility

## Relationship to TLCTC JSON Architecture

These files follow the three-layer architecture defined in §7 of the TLCTC v2.0 specification:

- **Layer 1 (Framework Definition):** Referenced via `framework_ref`, not duplicated. All files point to `tlctc-framework.v2.0.json` as the authoritative cluster definitions.
- **Layer 2 (Reference Registry):** `agentic-tool-profiles.json` and `agentic-irreversibility-matrix.json` extend the reference registry with agentic AI-specific context data.
- **Layer 3 (Attack Path Instances):** The 9 individual attack path files in `attack-paths/` are instance-level records following the canonical schema.

The consequence chain file (`agentic-consequence-chains.json`) is a **proposed extension** to the TLCTC JSON architecture for recording effect-side event sequences. It maintains strict Axiom III discipline: consequence chains are notated separately from attack paths, using the `C:` prefix to mark consequence-side notation. This extension is under development and may evolve.

## Validation

Attack path instances validate against the canonical Layer 3 schema:

```bash
# Validate individual attack path
ajv validate -s json-schemas/layer-3/tlctc-attack-path.schema.json -d examples/agentic-ai/attack-paths/path-A-direct-prompt-injection.json

# Validate all attack paths
for f in examples/agentic-ai/attack-paths/*.json; do
  ajv validate -s json-schemas/layer-3/tlctc-attack-path.schema.json -d "$f"
done
```

## Usage

These examples serve three purposes:

1. **Educational:** Demonstrate how the TLCTC framework applies to agentic AI scenarios.
2. **Template:** Provide starting points for organisations performing their own agentic AI threat analysis.
3. **Machine-readable:** Enable automated ingestion by SIEMs, risk registers, and threat intelligence platforms.

## License

CC BY 4.0 — Bernhard Kreinz / [tlctc.net](https://tlctc.net)
