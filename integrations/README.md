# Integrations

External-tool integrations for the TLCTC framework. Pick the build that matches
your platform; behaviour is identical across builds.

| Directory | Target | Format | Install |
|---|---|---|---|
| [`cortex-xsoar/`](cortex-xsoar/) | Cortex XSOAR **6.2.x** | Per-object YAML/JSON | Click-by-click via Settings UI (25 steps) |
| [`cortex-xsoar-8/`](cortex-xsoar-8/) | Cortex XSOAR **8.x** + Cortex **XSIAM** | Marketplace Content Pack (`marketplaces: ["xsoar","marketplacev2"]`) | `demisto-sdk validate / lint / zip-packs / upload` |
| [`sonarqube/`](sonarqube/) | SonarQube **self-hosted** + **SonarCloud** | Python 3.11+ CLI (stdlib only) + declarative starter assets | `git clone` then `python -m cli classify` (see [`sonarqube/deploy.md`](sonarqube/deploy.md)) |
| [`sarif/`](sarif/) | Any **SARIF 2.1.0** producer (Semgrep, CodeQL, Trivy, Grype, Bandit, gosec) | Python 3.10+ CLI (stdlib only) | `git clone` then `python -m cli classify scan.sarif` |

The two Cortex builds:

- Tag incidents with TLCTC cluster at ingestion via an ATT&CK→TLCTC classifier.
- Route to 10 cluster-scoped master playbooks (Axiom III: classify by cause, not outcome).
- Branch response by Velocity Class (VC-1…VC-4).
- Enforce Axiom VI / R-EXEC / R-CRED / R-SUPPLY / R-ROLE classification splits.
- Emit a Layer 3 attack-path JSON on close that validates against `json-schemas/layer-3/tlctc-attack-path.schema.json`.
- Trigger Propagated PR controls (GDPR Art. 33, NIS2 Art. 23) through the RS Container sub-playbook.

The 6.2 build will not import on 8.x without conversion; the 8.x build will not
import on 6.2 (different object schemas, LayoutsContainer, content-pack format).

The SonarQube build:

- Translates SAST findings to TLCTC clusters via the canonical 985-entry CWE→TLCTC mapping (`mappings/mitre-cwe/tlctc-cwe.json`).
- Applies R-ROLE context-aware logic (file-path globs) for ambiguous `#2 | #3` mappings.
- Read-only by default (emits JSON / Markdown / SARIF); opt-in `--apply-tags` writes `tlctc-NN` tags back via `/api/issues/set_tags`.
- Works equally on self-hosted SonarQube and SonarCloud (Web-API based).
- Does NOT emit Layer 3 — SAST findings are weaknesses, not realised attack paths.

The SARIF build:

- Classifies findings from any SARIF 2.1.0 producer to TLCTC clusters.
- CWE-first via the canonical 985-entry CWE→TLCTC mapping; CVE-only findings fall back to the offline KEV→TLCTC table (`mappings/cisa-kev/tlctc-kev.json`).
- Applies R-ROLE (file-path globs) for ambiguous `#2 | #3` mappings.
- Emits JSON / Markdown / TLCTC-enriched SARIF; `--fail-on-cluster` gates CI.
- Does NOT emit Layer 3 — SARIF findings are weaknesses, not realised attack paths.

Each directory has its own README, deploy runbook, and test cases.
