# Integrations

External-tool integrations for the TLCTC framework. Pick the build that matches
your platform; behaviour is identical across builds.

| Directory | Target | Format | Install |
|---|---|---|---|
| [`cortex-xsoar/`](cortex-xsoar/) | Cortex XSOAR **6.2.x** | Per-object YAML/JSON | Click-by-click via Settings UI (25 steps) |
| [`cortex-xsoar-8/`](cortex-xsoar-8/) | Cortex XSOAR **8.x** + Cortex **XSIAM** | Marketplace Content Pack (`marketplaces: ["xsoar","marketplacev2"]`) | `demisto-sdk validate / lint / zip-packs / upload` |

Both builds:

- Tag incidents with TLCTC cluster at ingestion via an ATT&CK→TLCTC classifier.
- Route to 10 cluster-scoped master playbooks (Axiom III: classify by cause, not outcome).
- Branch response by Velocity Class (VC-1…VC-4).
- Enforce Axiom VI / R-EXEC / R-CRED / R-SUPPLY / R-ROLE classification splits.
- Emit a Layer 3 attack-path JSON on close that validates against `json-schemas/layer-3/tlctc-attack-path.schema.json`.
- Trigger Propagated PR controls (GDPR Art. 33, NIS2 Art. 23) through the RS Container sub-playbook.

The 6.2 build will not import on 8.x without conversion; the 8.x build will not
import on 6.2 (different object schemas, LayoutsContainer, content-pack format).
Each directory has its own README, deploy runbook, and test cases.
