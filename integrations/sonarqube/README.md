# TLCTC SonarQube

Translates SonarQube SAST findings into TLCTC v2.1 cluster exposure. A Python
CLI sidecar that pulls issues via the SonarQube Web API, joins them against
the canonical 985-entry CWE→TLCTC mapping, applies R-ROLE context-aware logic
to resolve ambiguous mappings, and emits JSON / Markdown / SARIF reports.

The CLI is **read-only by default**. An opt-in `--apply-tags` flag writes
TLCTC cluster tags (`tlctc-01` … `tlctc-10`) back to each issue via
`/api/issues/set_tags`, making the cluster view native to SonarQube's issue
browser, filters, and portfolios.

A small `declarative/` directory ships zero-Python starter assets (tag
descriptions, a quality profile that uplifts severity on R-EXEC / R-CRED /
supply-chain CWEs, and a portfolio dashboard definition) for teams that want
the tag namespace and dashboard without running the CLI.

## What this pack does

- Pulls every `VULNERABILITY` and `SECURITY_HOTSPOT` from `/api/issues/search`
  for one or more project keys, branches, or pull requests. Works on
  self-hosted SonarQube and SonarCloud.
- Extracts CWE references from each issue's `tags` and `securityStandards`.
- Looks them up in the canonical mapping at
  `mappings/mitre-cwe/tlctc-cwe.json` (single source of truth — never forked).
- Applies the verdict filter: `Allowed` and `Allowed-with-Review` classify;
  `Discouraged` lands in a Markdown low-confidence section; `Prohibited` is
  silently skipped (logged at `--verbose`).
- Resolves `#2 | #3` and `#2 → #7 | #3 → #7` alternations by globbing the
  `issue.component` path against server / client patterns (R-ROLE). The
  decision is recorded on every finding so reports show *why* a cluster was
  chosen.
- Emits any combination of three artefacts:
  - **JSON**: cluster summary + per-issue array + low-confidence + unmapped
  - **Markdown**: PR-comment body with a cluster table and per-cluster sections
  - **SARIF 2.1.0**: one rule per cluster, CWE moved into `properties.tlctc`
- Optionally writes `tlctc-NN` tags back to each issue (`--apply-tags`) or
  exits non-zero when findings land in nominated clusters (`--fail-on-cluster`).

## Repository layout

```
integrations/sonarqube/
├── README.md                          # this file
├── deploy.md                          # install, configure, run, rollback
├── test-cases.md                      # TC-1..TC-7 with acceptance criteria
├── pack_metadata.json
├── ReleaseNotes/1_0_0.md
├── cli/                               # the Python sidecar (stdlib only)
│   ├── tlctc_sonar.py                 # argparse + dispatch
│   ├── sonar_client.py                # urllib wrapper, issues/search + set_tags
│   ├── mapping_loader.py              # loads tlctc-cwe.json, indexes by CWE-N
│   ├── path_parser.py                 # parses "#2 → #7 | #3" into a typed AST
│   ├── context_resolver.py            # R-ROLE: path globs → pick #2 vs #3
│   ├── classifier.py                  # issue + entry → ClassifiedFinding
│   ├── tagger.py                      # only module that POSTs (set_tags)
│   ├── config.py                      # TOML or JSON config + env-var precedence
│   └── reporters/                     # json_report, markdown_report, sarif_report
├── examples/
│   ├── tlctc-sonar.toml               # documented default config (Python 3.11+)
│   ├── tlctc-sonar.json               # JSON equivalent (Python 3.10 friendly)
│   ├── sample-issues-response.json    # canned API payload for offline tests
│   ├── sample-json-report.json        # expected JSON output for the canned payload
│   ├── sample-pr-comment.md           # expected Markdown output
│   └── sample-output.sarif            # expected SARIF output
├── declarative/                       # zero-Python starter tier
│   ├── README.md
│   ├── tlctc-tags-import.csv
│   ├── quality-profile-tlctc.xml
│   ├── tlctc-dashboard.json
│   └── webhook-payload-example.json   # reference only — no receiver shipped
└── tests/                             # unit tests (Python -m unittest discover tests)
```

## How TLCTC concepts map to SonarQube objects

| TLCTC concept | SonarQube object |
|---|---|
| Cluster (`#1` … `#10`) | Issue tag (`tlctc-01` … `tlctc-10`) |
| CWE→TLCTC mapping | Lookup via canonical `tlctc-cwe.json`; never duplicated |
| R-ROLE resolution (#2 vs #3) | Glob match on `issue.component` (server vs client patterns) |
| Sequence (`#2 → #7`) | Two tags applied; first step is the "primary" cluster (Axiom VI) |
| Alternation (`#2 | #3`) | Resolved before tagging — only the matching branch tags apply |
| Verdict `Discouraged` | Tag NOT applied; surfaced in Markdown low-confidence section |
| Verdict `Prohibited` | Silently skipped (Category / View / Deprecated nodes) |
| `mappingRationale` | Carried through to SARIF `properties.tlctc.role_resolution.reason` |
| `--fail-on-cluster #N` | CI gate; non-zero exit when findings land in nominated clusters |

## Notation convention

- Human-facing output (Markdown, JSON, SARIF descriptions) uses canonical `#N`
  notation matching the TLCTC whitepaper and `tlctc-cwe.json` `tlctcMapping`
  field.
- SonarQube tags are normalised to `tlctc-NN` (lowercase, zero-padded, no
  `#`) because Sonar tag names cannot contain `#`.

This integration intentionally does NOT use a `TLCTC-XX.YY` operational ID —
SAST findings do not carry lifecycle state, so the operational-ID rationale
used in the [cortex-xsoar-8](../cortex-xsoar-8/) pack does not apply here.

## Requirements

- **Python 3.11+** recommended (uses stdlib `tomllib` for TOML config).
- **Python 3.10** supported with the JSON config variant
  (`examples/tlctc-sonar.json`).
- **No third-party dependencies.** `urllib`, `argparse`, `tomllib`, `fnmatch`
  only — matches the [cortex-xsoar-8](../cortex-xsoar-8/) no-deps posture.
- A SonarQube user token with at least **Browse** permission on the projects
  you scan. `--apply-tags` additionally requires **Administer Issues**.

## Out of scope for v1

- **No Java plugin.** This sidecar supersedes the
  [Engineering the Bridge](https://www.tlctc.net/tlctc-sonar-cwe.html) blog's
  Java `PostProjectAnalysisTask` sketch. The sidecar runs against the Web API
  instead, so it works equally well with SonarCloud (where plugins cannot run).
- **No Layer 3 attack-path emission.** SAST findings are weaknesses, not
  realised attack paths. Emitting a Layer 3 path from a static scan would
  manufacture steps that never executed. Revisit once runtime / EDR signals
  are fused in.
- **No GitHub Action wrapper.** CI invokes `python -m cli classify` directly.
  An Action can wrap this later without breaking changes.
- **No webhook receiver service.** `declarative/webhook-payload-example.json`
  documents the payload shape for teams who want to build their own; no
  receiver ships in v1.

## References

- Kreinz, B. *TLCTC v2.1 White Paper* — cluster definitions, axioms, and
  classification rules. [Read v2.1](https://www.tlctc.net/tlctc-v2.0-whitepaper.html).
- `mappings/mitre-cwe/tlctc-cwe.json` — canonical CWE→TLCTC mapping (985
  entries, audited 2026-05-05).
- [cortex-xsoar-8 integration](../cortex-xsoar-8/) — sibling content pack
  whose deploy / test-cases conventions this pack mirrors.
- SonarQube Web API — `https://next.sonarqube.com/sonarqube/web_api/api/issues`.
- SARIF 2.1.0 specification — `https://docs.oasis-open.org/sarif/sarif/v2.1.0/`.
