# MITRE ATLAS → TLCTC Mapping

Maps every technique of **MITRE ATLAS** (Adversarial Threat Landscape for AI Systems: adversary
tactics and techniques against AI-enabled systems) to **TLCTC v2.5** threat clusters, in the same
record shape and notation as the [ATT&CK Enterprise mapping](../mitre-attack-enterprise/). ATLAS
answers "what did the adversary do to the AI system?"; TLCTC answers "which generic vulnerability
did that step exploit?", which is what decides the control.

> **Provenance.** Authored 2026-09-18 from the ATLAS technique descriptions, the repository's
> agentic-AI attack paths (`agentic-ai/attack-paths/`, paths A–J) and the agent theses; AI-drafted
> and human-reviewed, not independently validated. Techniques that mirror an ATT&CK technique
> (Valid Accounts, Phishing, Drive-by Compromise, Exploit Public-Facing Application, …) carry the
> ATT&CK mapping over and say so in the rationale, so the two mappings cannot disagree on them.

## Files

| File | Description |
|---|---|
| [`tlctc-atlas.json`](tlctc-atlas.json) | 211 technique mappings: all 208 techniques and sub-techniques of ATLAS v2026.09 plus the 3 ids that release retired but the STIX distribution still carries (`atlasStatus`, `supersededBy`), with rationale, tactics and the ATLAS description |
| [`decision-tree.md`](decision-tree.md) | How an ATLAS technique is classified: the AI-specific questions in front of the ATT&CK decision tree |
| [`pinned/ATLAS-2026.09.yaml`](pinned/ATLAS-2026.09.yaml) | The current ATLAS release (`mitre-atlas/atlas-data` tag `v2026.09`, `dist/v6/ATLAS-2026.09.yaml`, format 6.0.0, Apache-2.0) |
| [`pinned/stix-atlas.json`](pinned/stix-atlas.json) | The ATLAS STIX 2.1 distribution the Attack Flow Builder reads (`mitre-atlas/atlas-navigator-data` `dist/stix-atlas.json`, commit in the mapping metadata, Apache-2.0); 170 techniques of ATLAS 5.6 |

Validation: `npm run validate-atlas-mapping` checks total coverage of both pinned sources,
verbatim technique names, tactic ids, `atlasStatus` against the v2026.09 release, the notation
grammar, cluster ids against the dictionary, and the rationale on every row. It runs inside
`npm run validate`.

## Source

ATLAS content is authored in [`mitre-atlas/atlas-data`](https://github.com/mitre-atlas/atlas-data)
(YAML, monthly releases such as `v2026.09`, 208 techniques) and distributed as STIX 2.1 and
Navigator layers by [`mitre-atlas/atlas-navigator-data`](https://github.com/mitre-atlas/atlas-navigator-data),
which at the pinned commit still carries the 170 techniques of ATLAS 5.6: none of the 41
techniques v2026.09 added (autonomous-agent operations, tool-poisoning sub-techniques, multimodal
triggers, crafted assistant links, exposed AI services, …) and three ids that release retired
(`AML.T0019`, `AML.T0058`, `AML.T0104`, folded into `AML.T0115`). The mapping covers the union and
labels each row, so it serves both the current release and the STIX consumers, and the validator
reports drift against either pin when one is refreshed.

The `tactics` of every current technique are the v2026.09 `achieves` relationships of the YAML
(the validator enforces this); the three retired ids keep the STIX tactic set. Five techniques
carry tactics the STIX distribution does not: `AML.T0012` and `AML.T0053` gained Lateral Movement,
`AML.T0020` dropped Resource Development, and `AML.T0065` / `AML.T0066` moved from Resource
Development to `AML.TA0001`, which v2026.09 renamed from *AI Attack Staging* to *AI Attack
Adaptation* (the STIX bundle still uses the old name).

## Notation

Same as the ATT&CK mapping: `#N` a cluster, `A → B` a sequence (A enables B), `A | B` alternatives
that the technique alone cannot decide, parentheses for grouping, `#10.3` an operational
sub-cluster hint, `N/A` threat potential outside the target domain (reconnaissance, resource
development, AI attack staging on the attacker's side, and business-side harms).

| Form | Techniques |
|---|---|
| single cluster | 104 |
| sequence | 14 |
| alternatives | 23 |
| N/A | 70 |

## The doctrine the rows follow

- **Prompt injection, jailbreaks, RAG and context poisoning, agent tool abuse are #1.** The model
  or agent does what it is designed to do with input it was designed to accept; no implementation
  flaw and no foreign executable content are involved. The agent is the capability vector, not the
  actor (Axiom IV). This is the reading of agentic paths A, B and E and of the agent theses.
- **Attacker-side work is N/A.** Reconnaissance, resource development (including publishing
  poisoned datasets, models, hallucinated entities and agent tools) and AI attack staging (proxy
  models, adversarial data, deepfakes, generated commands) touch no victim system; the step is
  recorded when the artefact meets one.
- **Supply chain is #10 at the Trust Acceptance Event** (R-SUPPLY): a dataset, model, package,
  container image or agent tool honoured as trusted. Code that then executes adds #7 (R-EXEC);
  instructions that an agent then follows add #1.
- **Degradation is an outcome.** Poisoned models, eroded datasets, corrupted context and leaked
  training data are Data Risk Events (`Ii`, `If`, `Av`, `C`) produced by a #1 or #10 step, never
  clusters (Axiom III). ATLAS's *External Harms* are Business Risk Events and map to N/A.
- **Denial and cost follow R-FLOOD.** Volume or resource-intensive inputs that exhaust finite
  capacity are #6; a metered or expensive function driven against its purpose below that point
  is #1.
- **Physical inputs to sensors are #1, not #8**, unless the attacker manipulates the system's own
  hardware (R-SUBSTRATE): a sticker on a sign exploits the designed perception function.

## Examples

| ATLAS | TLCTC | Why |
|---|---|---|
| AML.T0051.001 LLM Prompt Injection: Indirect | `#1` | instructions placed where the agent's designed reading function executes them (path B) |
| AML.T0010.003 AI Supply Chain Compromise: Model | `#10 \| (#10 → #7)` | trusted model artefact; #7 follows if the serialised object executes on load |
| AML.T0024.002 Extract AI Model | `#1` | the inference API queried as designed; the copy is a DRE C on the model |
| AML.T0112.000 Machine Compromise: Local AI Agent | `#1 → #7` | the agent's code-execution tool driven through its interface (path E) |
| AML.T0034.001 Resource-Intensive Queries | `#6 \| #1` | intensity exhausting capacity, or cost abuse below that point |
| AML.T0048 External Harms | `N/A` | Business Risk Events, not causes |
| AML.T0110.001 AI Agent Tool Poisoning: Implementation | `(#10 → #7) \| (#1 → #7)` | a poisoned tool adopted from a registry (TAE) or modified in place, then its code runs on invocation |
| AML.T0117 Autonomous Attack-Path Adaptation | `N/A` | the attacker's planning loop; each step the agent takes classifies by its own technique |
| AML.T0131 Crafted AI Assistant Links | `#9 → #1` | a person follows the link, the assistant executes the prefilled prompt as designed |

## Used by

`integrations/attack-flow/` classifies Attack Flow actions through this mapping when the action
carries an ATLAS technique id (the two OpenClaw corpus flows), and through the ATT&CK mapping
otherwise.
