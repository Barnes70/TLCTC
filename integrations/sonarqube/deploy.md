# Deploy Runbook

End-to-end deployment of the TLCTC SonarQube sidecar. Sections 0–9 mirror the
shape of the [cortex-xsoar-8 deploy guide](../cortex-xsoar-8/deploy.md).

## 0. Prerequisites

- **Python 3.11+** recommended. Python 3.10 works with the JSON config variant.
- **SonarQube user token** with `Browse` on the projects you intend to scan.
  For `--apply-tags`, the token additionally needs `Administer Issues`.
- The TLCTC repository cloned locally — the CLI reads
  `mappings/mitre-cwe/tlctc-cwe.json` from a relative path by default.
- **Network egress** to the SonarQube base URL (HTTPS, port 443 for SonarCloud
  / your tenant's port for self-hosted).

## 1. Install (no install — just clone)

This integration is stdlib-only. No `pip install`, no virtualenv, no Maven.

```sh
git clone https://github.com/<your-fork>/tlctc.git
cd tlctc/integrations/sonarqube
python -m cli version    # expect: tlctc-sonar 1.0.0
```

If `python` resolves to 3.10 on your machine, that is fine — see step 2 for
the JSON config variant.

## 2. Configure

### Environment variables (preferred for credentials)

```sh
export SONAR_URL="https://sonarqube.example.com"   # or https://sonarcloud.io
export SONAR_TOKEN="<your token>"
```

Never put the token in the TOML / JSON file; the config loader does not read
credentials from it.

### Config file

Copy the documented default to your project root:

```sh
cp examples/tlctc-sonar.toml ../../your-project/tlctc-sonar.toml
# OR, on Python 3.10:
cp examples/tlctc-sonar.json ../../your-project/tlctc-sonar.json
```

Edit `[role.server]` and `[role.client]` glob lists to match your repository
layout. The shipped defaults cover Java / Kotlin / Scala backends and JSX /
TSX / Vue frontends; tune as needed.

## 3. Validate (offline)

```sh
python -m cli validate --config examples/tlctc-sonar.json
```

Expected output (file paths will differ):

```
config OK: examples/tlctc-sonar.json (source=json)
mapping OK: .../mappings/mitre-cwe/tlctc-cwe.json (985 entries, tlctc_version=2.1)
```

If the mapping integrity check fails, stop and re-pull the repo — the CLI
will not classify against a malformed mapping. See exit code 5 in §9.

## 4. Run classify (read-only)

Against a real SonarQube tenant:

```sh
python -m cli classify \
    --sonar-url "$SONAR_URL" \
    --token    "$SONAR_TOKEN" \
    --project-key your.project.key \
    --branch    main \
    --types     VULNERABILITY,SECURITY_HOTSPOT \
    --out-json  tlctc-report.json \
    --out-md    tlctc-report.md \
    --out-sarif tlctc-report.sarif
```

The CLI writes the three artefacts and exits 0. Exit codes are listed in §9.

## 5. Smoke test (offline, against the canned fixture)

The shipped fixture covers all 7 test cases in [`test-cases.md`](test-cases.md):

```sh
python -m cli classify \
    --config       examples/tlctc-sonar.json \
    --sonar-url    "file://$PWD/examples/sample-issues-response.json" \
    --token        x \
    --project-key  demo \
    --out-json     /tmp/smoke.json \
    --out-md       /tmp/smoke.md \
    --out-sarif    /tmp/smoke.sarif
```

The output should match the committed `examples/sample-{json-report.json,
pr-comment.md,output.sarif}` byte-for-byte except for the `generated_at`
timestamp in the JSON.

Unit tests:

```sh
python -m unittest discover tests   # expect: Ran 40 tests; OK
```

## 6. Apply tags (write-back, opt-in)

When you are confident in the classification, opt into write-back:

```sh
python -m cli classify \
    --sonar-url "$SONAR_URL" --token "$SONAR_TOKEN" \
    --project-key your.project.key \
    --out-md tlctc-report.md \
    --apply-tags \
    --dry-run    # remove --dry-run when ready
```

`--dry-run` logs the planned `set_tags` POSTs without issuing them. Without
`--dry-run`, the CLI issues one POST per classified finding, replacing any
existing `tlctc-*` tags while preserving the issue's other tags. The
operation is idempotent — re-running produces no diff.

The `tag` subcommand is an alias for `classify --apply-tags`:

```sh
python -m cli tag --sonar-url ... --token ... --project-key ... --out-md ...
```

## 7. Wire to CI

### GitHub Actions (no Action shipped — invoke directly)

```yaml
- name: TLCTC SAST classification
  env:
    SONAR_URL: ${{ secrets.SONAR_URL }}
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
  run: |
    python -m cli classify \
      --sonar-url "$SONAR_URL" --token "$SONAR_TOKEN" \
      --project-key ${{ github.repository }} \
      --pull-request ${{ github.event.pull_request.number }} \
      --out-md tlctc-pr-comment.md \
      --out-sarif tlctc.sarif \
      --fail-on-cluster '#2,#7,#10'

- name: Upload SARIF to GitHub code scanning
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: tlctc.sarif
```

### GitLab CI

```yaml
tlctc-sast:
  stage: test
  script:
    - python -m cli classify
        --sonar-url "$SONAR_URL" --token "$SONAR_TOKEN"
        --project-key "$CI_PROJECT_PATH"
        --branch "$CI_COMMIT_REF_NAME"
        --out-json tlctc-report.json
        --out-md   tlctc-report.md
        --fail-on-cluster '#7,#10'
  artifacts:
    paths: [tlctc-report.json, tlctc-report.md]
```

## 8. Rollback

The sidecar is stateless. Rollback means:

1. Remove the CI step (delete the workflow block from §7).
2. If `--apply-tags` was used, the `tlctc-*` tag namespace remains on issues.
   Bulk-remove via:
   ```sh
   for k in $(jq -r '.findings[].issue_key' tlctc-report.json); do
     curl -u "$SONAR_TOKEN:" -X POST "$SONAR_URL/api/issues/set_tags" \
       -d "issue=$k" -d "tags="    # empty tag list clears tlctc-* tags
   done
   ```
   Note: this also clears non-TLCTC tags on those issues. Refine the `tags=`
   payload to preserve them if needed.
3. Remove the `declarative/quality-profile-tlctc.xml` profile via SonarQube >
   Quality Profiles > Delete if it was imported.

## 9. Maintenance

- **Mapping refresh.** When `mappings/mitre-cwe/tlctc-cwe.json` is updated
  upstream, the CLI picks it up automatically on the next run — no rebuild
  needed. The CLI logs `tlctc_version=<X>` on every run; if the version drifts
  from `2.1`, audit the changes before promoting.
- **Glob tuning.** Track R-ROLE mis-resolutions reported in the Markdown
  output's "fell back to default_role" lines and add globs accordingly.
- **CI gate evolution.** Start with `--fail-on-cluster '#7'` (Malware blocks
  any merge), expand once the team is comfortable.

### Exit codes

| Code | Meaning |
|---:|---|
| 0 | Clean run |
| 1 | A finding matched `--fail-on-cluster` |
| 2 | Config / usage error |
| 3 | Sonar API auth or other 4xx |
| 4 | Sonar API 5xx or transport failure |
| 5 | Mapping load failure (file missing, malformed, or any path failed to parse) |
| 6 | Partial success — some issues skipped (reserved; not currently emitted) |
