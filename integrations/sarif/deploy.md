# Deploy Runbook

End-to-end deployment of the TLCTC SARIF Classifier. Sections mirror the
shape of the [sonarqube deploy guide](../sonarqube/deploy.md).

## 0. Prerequisites

- **Python 3.10+** required. Python 3.11+ recommended (enables TOML config
  via stdlib `tomllib`; 3.10 uses the JSON config variant).
- A produced `.sarif` file from any SARIF 2.1.0-compatible scanner
  (Semgrep, CodeQL, Trivy, Grype, Bandit, gosec, or another).
- The TLCTC repository cloned locally — the CLI reads
  `mappings/mitre-cwe/tlctc-cwe.json` and
  `mappings/cisa-kev/tlctc-kev.json` from relative paths by default.

## 1. Install (no install — just clone)

This integration is stdlib-only. No `pip install`, no virtualenv, no build step.

```sh
git clone https://github.com/<your-fork>/tlctc.git
cd tlctc/integrations/sarif
python -m cli classify --help
```

## 2. Produce a SARIF file

The classifier consumes a `.sarif` file you produce from your scanner of
choice. Two common examples:

**Semgrep**

```sh
semgrep --sarif --output scan.sarif .
```

**Trivy**

```sh
trivy fs --format sarif -o scan.sarif .
```

Any SARIF 2.1.0 producer works. The loader mines CWE/CVE identifiers from
taxa, `properties`, `relationships`, and `ruleId` heuristics — no
producer-specific configuration required.

## 3. Configure

Copy the documented default config to your project root and edit the
`source_globs` to match your repository layout:

```sh
cp examples/tlctc-sarif.json ../../your-project/tlctc-sarif.json
```

Edit `server` and `client` glob lists to match your layout. The shipped
defaults cover common Java / Kotlin backends and JSX / TSX frontends.

## 4. Run classify

```sh
python -m cli classify scan.sarif --config examples/tlctc-sarif.json
```

The CLI writes to stdout in the configured format (default: JSON) and exits 0.
To emit multiple formats, pass a comma-separated list:

```sh
python -m cli classify scan.sarif \
    --config examples/tlctc-sarif.json \
    --format json,markdown,sarif
```

## 5. CI gate

Use `--fail-on-cluster` to block a pipeline when findings land in nominated
clusters. The CLI exits 2 if any classified finding matches:

```sh
python -m cli classify scan.sarif \
    --config examples/tlctc-sarif.json \
    --format markdown \
    --fail-on-cluster "#2,#7"
```

### GitHub Actions example

```yaml
- name: Produce SARIF
  run: semgrep --sarif --output semgrep.sarif .

- name: TLCTC SARIF classification
  run: |
    python -m cli classify semgrep.sarif \
      --config tlctc-sarif.json \
      --format markdown,sarif \
      --fail-on-cluster '#2,#7,#10'
```

### GitLab CI example

```yaml
tlctc-sarif:
  stage: test
  script:
    - trivy fs --format sarif -o scan.sarif .
    - python -m cli classify scan.sarif
        --config tlctc-sarif.json
        --format json
        --fail-on-cluster '#7,#10'
  artifacts:
    paths: [scan.sarif]
```

## 6. Smoke test (offline)

Run the unit test suite against the bundled fixtures:

```sh
python -m unittest discover tests   # expect: Ran 28 tests; OK
```

## 7. Rollback

The classifier is **read-only**. It writes report files but does not modify
your scanner output, your repository, or any external service.

To roll back:

1. Remove the CI step (delete the pipeline block from §5).
2. Delete the generated report files (e.g., `tlctc-report.json`,
   `tlctc-report.md`, `tlctc.sarif`).
3. Nothing else to undo — no tags written, no API calls made.

## 8. Maintenance

- **Mapping refresh.** When `mappings/mitre-cwe/tlctc-cwe.json` or
  `mappings/cisa-kev/tlctc-kev.json` are updated upstream, the CLI picks
  them up automatically on the next run — no rebuild needed.
- **Glob tuning.** Track R-ROLE mis-resolutions reported in the JSON output's
  `role_resolution` fields and add globs accordingly.
- **CI gate evolution.** Start with `--fail-on-cluster '#7'` (Malware blocks
  any merge), expand to `#2,#7,#10` once the team is comfortable.

### Exit codes

| Code | Meaning |
|---:|---|
| 0 | Clean run — all findings classified or skipped by verdict |
| 2 | `--fail-on-cluster` triggered — one or more findings matched a nominated cluster |
