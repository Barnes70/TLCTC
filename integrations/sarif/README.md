# TLCTC SARIF Classifier

Parses any SARIF 2.1.0 file, extracts CWE and CVE identifiers from findings,
classifies them to TLCTC v2.1 clusters, and emits JSON / Markdown /
TLCTC-SARIF reports. Works with any SARIF producer â€” Semgrep, CodeQL,
Trivy, Grype, Bandit, gosec, OWASP Dependency-Check, and others. The pack
is **standalone and stdlib-only**: no third-party dependencies, no network
calls, no build step.

> **Provenance & validation.** Cluster assignments inherit from the AI-generated, human-reviewed [CWEâ†’TLCTC](../../mappings/mitre-cwe/README.md) and [ATT&CKâ†’TLCTC](../../mappings/mitre-attack-enterprise/README.md) mappings, which are not yet independently validated; classification errors in those bases propagate here. A stratified human-expert validation (Cohen's Îº) of those bases is the planned highest-leverage check.

## What this pack does

- Parses `runs[].results[]` from any SARIF 2.1.0 producer.
- Mines CWE and CVE identifiers from taxa, `properties`, `relationships`,
  and `ruleId` heuristics â€” covering the heterogeneous identifier placement
  across producers.
- CWE-first lookup against the canonical 985-entry CWEâ†’TLCTC mapping
  (`mappings/mitre-cwe/tlctc-cwe.json`) â€” single source of truth, never
  forked.
- CVE-only findings (no CWE present or all CWE lookups skipped) fall back
  to the offline KEVâ†’TLCTC table (`mappings/cisa-kev/tlctc-kev.json`).
- Applies the verdict filter: `Allowed` and `Allowed-with-Review` classify;
  `Discouraged` lands in a low-confidence section; `Prohibited` and `N-A`
  entries are silently skipped (logged at `--verbose`).
- Resolves `#2 | #3` alternations via file-path globs (R-ROLE): server-role
  globs and client-role globs are configured per project; the decision is
  recorded on every finding so reports show *why* a cluster was chosen.
- Emits any combination of three artefacts:
  - **JSON**: cluster summary + per-finding array + low-confidence + unmapped
  - **Markdown**: PR-comment body with a cluster table and per-cluster sections
  - **TLCTC SARIF**: a standalone SARIF 2.1.0 document (driver
    `tlctc-sarif`) containing the classified findings, each tagged with
    `properties.tlctc` and a TLCTC taxonomy node on the run. It is a fresh
    report, not an in-place rewrite of the producer's file â€” the source
    location (`uri` + original `region` line anchors) and the originating
    tool name are preserved on every result.
- `--fail-on-cluster` exits 2 when findings land in nominated clusters,
  enabling a hard CI gate without a separate policy engine.

## Repository layout

```
integrations/sarif/
â”œâ”€â”€ README.md                          # this file
â”œâ”€â”€ deploy.md                          # prerequisites, install, run, CI gate, rollback
â”œâ”€â”€ test-cases.md                      # TC-1..TC-8 with acceptance criteria
â”œâ”€â”€ pack_metadata.json
â”œâ”€â”€ ReleaseNotes/1_0_0.md
â”œâ”€â”€ cli/                               # the Python classifier (stdlib only)
â”‚   â”œâ”€â”€ tlctc_sarif.py                 # argparse + dispatch
â”‚   â”œâ”€â”€ config.py                      # JSON/TOML config + env-var precedence
â”‚   â”œâ”€â”€ sarif_loader.py                # parse SARIF 2.1.0; extract findings
â”‚   â”œâ”€â”€ mapping_loader.py              # loads tlctc-cwe.json + tlctc-kev.json
â”‚   â”œâ”€â”€ context_resolver.py            # R-ROLE: file-path globs â†’ pick #2 vs #3
â”‚   â”œâ”€â”€ classifier.py                  # finding + mapping entry â†’ ClassifiedFinding
â”‚   â””â”€â”€ reporters/                     # json_report, markdown_report, sarif_report
â”œâ”€â”€ examples/
â”‚   â”œâ”€â”€ tlctc-sarif.json               # documented default config (Python 3.10+)
â”‚   â”œâ”€â”€ semgrep-input.sarif            # example Semgrep SARIF for offline tests
â”‚   â””â”€â”€ sample-json-report.json        # expected JSON output for the example input
â””â”€â”€ tests/                             # unit tests (python -m unittest discover tests)
    â””â”€â”€ fixtures/
        â”œâ”€â”€ tiny-cwe.json              # minimal CWE mapping for offline tests
        â”œâ”€â”€ tiny-kev.json              # minimal KEV mapping for offline tests
        â”œâ”€â”€ semgrep-min.sarif          # minimal Semgrep fixture
        â”œâ”€â”€ trivy-min.sarif            # minimal Trivy fixture (CVE-only finding)
        â””â”€â”€ ruleid-cwe-min.sarif       # ruleId CWE heuristic fixture
```

## How TLCTC concepts map to SARIF objects

| TLCTC concept | SARIF object |
|---|---|
| Cluster (`#1` â€¦ `#10`) | `result.properties.tlctc.cluster` (on each result of the standalone TLCTC SARIF report) |
| CWEâ†’TLCTC mapping | Lookup via canonical `tlctc-cwe.json`; never duplicated |
| R-ROLE resolution (#2 vs #3) | Glob match on `result.locations[].physicalLocation.artifactLocation.uri` |
| Provenance (source field) | `result.properties.tlctc.source` (`"cwe"`, `"kev"`, or `"unmapped"`) |
| `--fail-on-cluster #N` | CI gate; exits 2 when any classified finding lands in a nominated cluster |

## Notation convention

- Human-facing output (Markdown, JSON descriptions) uses canonical `#N`
  notation matching the TLCTC whitepaper and `tlctc-cwe.json` `tlctcMapping`
  field.
- SARIF tag normalization is not needed â€” SARIF has no tag charset limit,
  so `#2`, `#7`, and `#10` are valid `properties` values as-is.

This integration intentionally does NOT use a `TLCTC-XX.YY` operational ID â€”
SAST findings do not carry lifecycle state, so the operational-ID rationale
used in the [cortex-xsoar-8](../cortex-xsoar-8/) pack does not apply here.

## Requirements

- **Python 3.10+** (3.11+ recommended for TOML config support via stdlib
  `tomllib`; 3.10 uses the JSON config variant).
- **No third-party dependencies.** `json`, `argparse`, `fnmatch`, `pathlib`
  only â€” matches the [sonarqube](../sonarqube/) pack's no-deps posture.
- A produced `.sarif` file from any SARIF 2.1.0-compatible tool. The
  classifier is read-only and makes no network calls.

## Out of scope for v1

- **No live tool invocation.** The classifier consumes a `.sarif` file
  already produced by a scanner; it does not invoke Semgrep, Trivy, or any
  other tool.
- **No GitHub Action wrapper.** CI invokes `python -m cli classify` directly.
  An Action can wrap this later without breaking changes.
- **No CVEâ†’CWE NVD enrichment.** The CVE path uses the offline KEV table
  only (`mappings/cisa-kev/tlctc-kev.json`). NVD API enrichment would allow
  broader CVE coverage but adds a network dependency; deferred.
- **No Layer 3 attack-path emission.** SARIF findings are weaknesses, not
  realised attack paths. Emitting a Layer 3 path from a static scan would
  manufacture steps that never executed.

## References

- Kreinz, B. *TLCTC v2.1 White Paper* â€” cluster definitions, axioms, and
  classification rules. [Read v2.1](https://www.tlctc.net/tlctc-v2.0-whitepaper.html).
- `mappings/mitre-cwe/tlctc-cwe.json` â€” canonical CWEâ†’TLCTC mapping (985
  entries, audited 2026-05-05).
- `mappings/cisa-kev/tlctc-kev.json` â€” offline KEVâ†’TLCTC derivation (1,568
  CVEs, deterministically derived from the CISA KEV snapshot).
- [sonarqube integration](../sonarqube/) â€” sibling pack whose deploy /
  test-cases conventions this pack mirrors.
- SARIF 2.1.0 specification â€” `https://docs.oasis-open.org/sarif/sarif/v2.1.0/`.
