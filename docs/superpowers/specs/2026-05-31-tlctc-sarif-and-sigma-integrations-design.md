# TLCTC SARIF + Sigma Integrations — Design

**Date:** 2026-05-31
**Status:** Approved (design)
**Author:** TLCTC Project (Bernhard Kreinz) with Claude Code

## Summary

Two new low-effort, high-coverage TLCTC integrations, both built by joining
external tool output against mapping tables that already live in this repo:

1. **`integrations/sarif/`** — a generic SARIF 2.1.0 → TLCTC classifier CLI.
   One adapter classifies findings from any SARIF producer (Semgrep, CodeQL,
   Bandit, gosec, Trivy, Grype) by reusing the canonical CWE→TLCTC mapping,
   with a CVE→KEV fallback.
2. **`mappings/sigma/`** — a static Sigma-rules → TLCTC data mapping
   (generator + committed snapshot), derived by joining each rule's ATT&CK
   tags against the 698-technique ATT&CK→TLCTC mapping.

Both reuse existing canonical tables as the single source of truth and add no
runtime third-party dependencies for consumers.

### Design decisions locked during brainstorming

- **SARIF tool is standalone** — it carries its own self-contained copy of the
  classification engine. The shipped `integrations/sonarqube/` pack is NOT
  refactored or touched. (Accepted tradeoff: two copies of the engine that can
  drift; chosen to protect the working SonarQube pack and ship faster.)
- **SARIF identifier scope is CWE + CVE bridge** — CWE-first against
  `tlctc-cwe.json`, then CVE-only findings fall back to the offline
  `tlctc-kev.json` table. No NVD dependency, no network.
- **Sigma deliverable is generator + committed snapshot** — ships both a
  `generate-sigma-mapping.py` and a committed `tlctc-sigma.json` so users get
  data out of the box and can regenerate to refresh.
- **PyYAML is allowed for the Sigma generator only** — a maintainer build-time
  script. The committed output is pure JSON, so consumers need nothing.

---

## Part 1 — `integrations/sarif/` (generic SARIF → TLCTC classifier)

### Purpose

Ingest a SARIF 2.1.0 file produced by any scanner, classify each result to a
TLCTC cluster, and emit JSON / Markdown / TLCTC-enriched SARIF. Standalone,
stdlib-only, self-contained.

### Canonical inputs (never forked)

- `mappings/mitre-cwe/tlctc-cwe.json` — per-CWE `tlctcMapping`,
  `mappingVerdict`, `contextDependent`.
- `mappings/cisa-kev/tlctc-kev.json` — per-CVE `primaryCluster`, `clusterSet`,
  `confidence` (1568 entries, offline). Used as the CVE fallback table.

### Components

```
integrations/sarif/
├── README.md                      # what / why / how, mirrors sonarqube README
├── deploy.md                      # install, run, CI gate, rollback
├── test-cases.md                  # TC-1..TC-n with acceptance criteria
├── pack_metadata.json
├── ReleaseNotes/1_0_0.md
├── cli/
│   ├── __init__.py
│   ├── __main__.py
│   ├── tlctc_sarif.py             # argparse + dispatch
│   ├── sarif_loader.py            # parse runs[].results[], extract CWE/CVE
│   ├── mapping_loader.py          # load + index tlctc-cwe.json and tlctc-kev.json
│   ├── classifier.py              # resolution ladder -> ClassifiedFinding
│   ├── context_resolver.py        # R-ROLE: file-URI globs -> #2 vs #3
│   ├── config.py                  # TOML/JSON config + env precedence
│   └── reporters/
│       ├── __init__.py
│       ├── json_report.py
│       ├── markdown_report.py
│       └── sarif_report.py
├── examples/
│   ├── tlctc-sarif.toml           # documented default config
│   ├── tlctc-sarif.json           # JSON config variant (3.10-friendly)
│   ├── semgrep-input.sarif        # golden fixture: real Semgrep SARIF
│   ├── trivy-input.sarif          # golden fixture: real Trivy SARIF (CVE path)
│   ├── sample-json-report.json    # expected JSON output
│   ├── sample-pr-comment.md       # expected Markdown output
│   └── sample-output.sarif        # expected enriched SARIF
└── tests/
    ├── __init__.py
    ├── fixtures/                  # tiny CWE + KEV slices, minimal SARIF docs
    ├── test_sarif_loader.py
    ├── test_classifier.py
    ├── test_context_resolver.py
    └── test_reporters.py
```

### Data flow

1. **`sarif_loader.py`** parses `runs[].results[]`. For each result it extracts
   identifiers from these sources, in priority order, to absorb producer
   variance in ONE place:
   1. `result.taxa[]` / `run.taxonomies[]` references whose `name`/`id` is a
      `CWE-N` or `CVE-...`.
   2. `run.tool.driver.rules[].relationships[]` → referenced taxa.
   3. `rule.properties.cwe` / `result.properties.cwe` / `.cve` / `.tags[]`
      (Semgrep, Trivy conventions).
   4. `result.ruleId` pattern heuristics (e.g. `external/cwe/cwe-89`).
   Output per finding: `{cwe: [CWE-N,...], cve: [CVE-...,...]}` plus the raw
   `ruleId`, `message`, and `physicalLocation` URI.

2. **`classifier.py`** runs the resolution ladder per finding:
   - **CWE present** → look up `tlctc-cwe.json`. Apply the verdict filter
     (identical semantics to the SonarQube pack):
     - `Allowed` / `Allowed-with-Review` → classify.
     - `Discouraged` → not classified into the main set; surfaced in a
       Markdown low-confidence section.
     - `Prohibited` → skipped (logged at `--verbose`).
   - **else CVE present** → look up `tlctc-kev.json` by `cveID`; use its
     pre-derived `primaryCluster` / `clusterSet` / `confidence`.
   - **else** → `unmapped` bucket.
   Each `ClassifiedFinding` records a `provenance` object: which identifier
   (`cwe`/`cve`), which table (`tlctc-cwe`/`tlctc-kev`), and the source
   verdict/confidence — so every cluster assignment is auditable in the report.

3. **`context_resolver.py`** resolves `#2 | #3` (and `#2 → #7 | #3 → #7`)
   alternations via R-ROLE, globbing the SARIF
   `physicalLocation.artifactLocation.uri` against configurable server / client
   path patterns. The decision and its reason are recorded on the finding.
   This mirrors the SonarQube `context_resolver` but takes a file URI instead
   of `issue.component`.

4. **`reporters/`** emit any combination of:
   - **JSON** — cluster summary + per-finding array + low-confidence + unmapped.
   - **Markdown** — PR-comment body: cluster table + per-cluster sections.
   - **SARIF** — TLCTC taxonomy injected as a `run.taxonomies` entry
     (one taxon per cluster); each result gets `properties.tlctc` carrying the
     cluster, the source CWE/CVE, and the role-resolution reason.

### CLI surface (`tlctc_sarif.py`)

- `classify <file.sarif | ->` — read a SARIF file or stdin, emit reports to
  configured outputs.
- `--fail-on-cluster #N[,#M...]` — CI gate; non-zero exit when any finding
  lands in a nominated cluster.
- `--source-globs <patterns>` — server/client path globs for R-ROLE
  (also settable via config).
- `--format json,markdown,sarif` — select reporters.
- `version` — print pack + TLCTC mapping versions.

### Notation convention

- Human-facing output uses canonical `#N` notation (matches the whitepaper and
  the `tlctcMapping` fields).
- No `tlctc-NN` tag normalization is needed (SARIF has no tag-charset
  restriction); the enriched SARIF uses canonical IDs in `properties.tlctc`.

### Requirements

- Python 3.11+ recommended (`tomllib` for TOML config); 3.10 supported with the
  JSON config variant. No third-party dependencies (`json`, `argparse`,
  `fnmatch`, `pathlib`, `tomllib`).

### Out of scope (v1)

- No live tool invocation — consumes an already-produced `.sarif` (the scanner
  is run by the user / CI).
- No GitHub Action wrapper (CI invokes `python -m cli classify` directly).
- No CVE→CWE NVD enrichment — the only CVE path is the offline KEV table. CVEs
  absent from KEV land in `unmapped`.
- No Layer 3 attack-path emission — SARIF findings are weaknesses, not realised
  attack paths (same rationale as the SonarQube pack).

---

## Part 2 — `mappings/sigma/` (Sigma rules → TLCTC)

### Purpose

A static data mapping deriving each Sigma rule's TLCTC cluster from its ATT&CK
tags joined against `tlctc-enterprise-attack.json`. Mechanical ETL that mirrors
`mappings/cisa-kev/generate-kev-mapping.py`.

### Canonical input (never forked)

- `mappings/mitre-attack-enterprise/tlctc-enterprise-attack.json` — per-technique
  `tlctcMapping`, `tlctcMappingName` (698 techniques).

### External input (pinned, not vendored)

- A local clone of the public SigmaHQ rules directory. Path is a CLI argument;
  the resolved **commit SHA is recorded in output metadata** for reproducibility.

### Components

```
mappings/sigma/
├── README.md                    # what / why / how-to-regenerate, caveats
├── decision-tree.md             # Sigma -> ATT&CK -> TLCTC resolution logic
├── generate-sigma-mapping.py    # deterministic ETL (PyYAML, build-time only)
├── tlctc-sigma.json             # committed snapshot: per-rule records
└── tlctc-sigma-stats.json       # aggregate statistics
```

### Generator behaviour (`generate-sigma-mapping.py`)

Mirrors the KEV generator: pinned in-tree canonical input, a `--rules-dir`
pointing at the SigmaHQ clone, deterministic output, optional `--fetch` for
ad-hoc refresh (never in CI; tagged releases reproduce from pinned inputs).

1. Recursively walk `--rules-dir` for `*.yml` Sigma rules (PyYAML parse).
2. Per rule, read `tags:` and extract `attack.tXXXX[.YYY]` technique IDs.
   Sub-techniques are folded to their parent technique (`T1059.001` → `T1059`)
   because the ATT&CK→TLCTC table is keyed at technique level.
3. Join each technique to `tlctc-enterprise-attack.json` by `techniqueId`;
   pull `tlctcMapping` + `tlctcMappingName`.
4. Compute the rule's cluster set:
   - Collect the union of clusters across all of the rule's techniques.
   - `primaryCluster` = the single most-specific / first-resolved cluster
     (same selection posture as KEV `primaryCluster`).
   - `clusterSet` = the full ordered set.
   - `derivationStatus`:
     - `ok` — all techniques resolved to a concrete single cluster.
     - `ambiguous` — one or more techniques resolve to an alternation
       (`#X | #Y`) or the rule spans multiple clusters.
     - `unmapped` — technique(s) map to `N/A`, or the rule has no `attack.t*`
       tag.
5. Emit per-rule records carrying ONLY: `ruleId` (Sigma GUID), `ruleTitle`,
   `logsource` (category/product/service), `techniques` (the parent technique
   IDs used), `clusterSet`, `primaryCluster`, `derivationStatus`. **No rule
   detection bodies are copied** — titles + GUIDs + our derivation only
   (license-safe).

### Outputs

- **`tlctc-sigma.json`** — `metadata` (TLCTC version, ATT&CK mapping version,
  pinned SigmaHQ commit SHA, total rules, license, caveats) + `mappings` array
  of per-rule records.
- **`tlctc-sigma-stats.json`** — cluster distribution (excluding ambiguous /
  unmapped per the stats convention), `derivationStatus` counts, and a
  `logsource` breakdown.

### Caveats (recorded in metadata + README)

- Mapping is only as good as the rule's `attack.t*` tagging; untagged rules are
  `unmapped`.
- Derived mechanically from the AI-generated, experimental ATT&CK→TLCTC mapping;
  per-rule confidence is not asserted beyond `derivationStatus`.
- Sub-technique folding may coarsen intent where a parent technique's
  `tlctcMapping` is an alternation.

### Build dependency

- `generate-sigma-mapping.py` requires **PyYAML** (build-time only). Consumers
  of `tlctc-sigma.json` need nothing — the output is plain JSON. Documented in
  the README; not added to any consumer-facing dependency surface.

---

## Testing & validation

### Part 1 (SARIF)

- Unit tests (stdlib `unittest`, isolated fixtures — no live API):
  - `sarif_loader`: identifier extraction across Semgrep / CodeQL / Trivy
    shapes, including taxa, relationships, properties, and ruleId-heuristic
    paths.
  - `classifier`: CWE-hit, verdict filtering (Allowed / Discouraged /
    Prohibited), CVE→KEV fallback, unmapped, and `provenance` correctness.
  - `context_resolver`: `#2 | #3` resolution by file-URI globs (server, client,
    no-match).
  - `reporters`: JSON / Markdown / SARIF output matches golden fixtures.
- Golden end-to-end: `examples/semgrep-input.sarif` and `trivy-input.sarif`
  classify to the committed `sample-*` outputs.
- `test-cases.md` enumerates TC-1..TC-n with acceptance criteria (mirrors the
  SonarQube pack).

### Part 2 (Sigma)

- Generator run against a tiny in-tree fixture rules directory (a handful of
  Sigma `.yml` files covering: clean single-technique, sub-technique folding,
  multi-technique ambiguous, alternation mapping, and untagged/unmapped).
- Assert the produced `tlctc-sigma.json` records and the
  `tlctc-sigma-stats.json` counts match expected values.
- Output JSON validates as well-formed and self-consistent (clusters referenced
  exist in the framework; stats counts reconcile with the records array).

---

## Repo touch-points

- `integrations/README.md` — add a `sarif/` row to the table and a short
  description block (mirrors the SonarQube entry).
- `mappings/` — `sigma/` follows the existing mapping-directory convention
  (README + decision-tree + generator + snapshot + stats), like `cisa-kev/`.
- Root `README.md` — add the two new entries where SonarQube / mappings are
  listed.

## Non-goals (both)

- No refactor of the SonarQube pack.
- No new operational `TLCTC-XX.YY` IDs (neither SARIF findings nor Sigma rules
  carry lifecycle state).
- No network access at consume time; no NVD; no vendored Sigma rule bodies.
