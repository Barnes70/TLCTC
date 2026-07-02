# Test Cases

Each TC pins one TLCTC classification rule. All cases are runnable offline
against the bundled fixtures using:

```sh
python -m unittest discover tests -v
```

The unit tests in `tests/` cover the same logic against
`tests/fixtures/tiny-cwe.json` and `tests/fixtures/tiny-kev.json`.

---

## TC-1 â€” CWEâ†’cluster (CWE-89 SQL Injection)

| | |
|---|---|
| Input finding | `cwe=["CWE-89"]`, path `src/api/u.py`, producer Semgrep |
| Canonical mapping | `#2` (Exploiting Server) â€” `Allowed`, not context-dependent |
| Expected `primary_cluster` | `#2` |
| Expected `status` | `classified` |
| Expected provenance | `table=tlctc-cwe`, `identifier=CWE-89` |
| Test method | `test_classifier.TestClassifier.test_allowed_cwe_classifies` |

**Why this matters:** Validates the core CWE-first lookup path. CWE-89 maps
to `#2` in the canonical 985-entry mapping â€” the classifier must resolve it
directly without context-dependent logic.

---

## TC-2 â€” #2|#3 R-ROLE resolution

| | |
|---|---|
| Input finding | `cwe=["CWE-79"]`, path `src/api/u.py`, producer Semgrep |
| Canonical mapping | `#2 \| #3` â€” `Allowed`, context-dependent |
| Expected `primary_cluster` | `#2` (server branch â€” `**/api/**` glob matches) |
| Expected `role_reason` | contains `"server-role"` |
| Test method | `test_classifier.TestClassifier.test_alternation_resolved_by_rrole` |

**Why this matters:** R-ROLE. The same CWE produces a different cluster
depending on where the vulnerable code runs. File-path globs drive the
resolution; the decision is recorded on the finding so reports show *why*.

---

## TC-3 â€” Discouraged verdict â†’ low_confidence

| | |
|---|---|
| Input finding | `cwe=["CWE-20"]`, any path, any producer |
| Canonical mapping | `Discouraged` (generic root-cause umbrella) |
| Expected `status` | `low_confidence` |
| Expected behaviour | No cluster assigned; surfaced in Markdown low-confidence section |
| Test method | `test_classifier.TestClassifier.test_discouraged_is_low_confidence` |

**Why this matters:** The verdict filter. CWE-20 (Improper Input Validation)
is an umbrella shared by `#1`, `#2`, `#3`, and `#6` depending on context.
The responsible action is to surface it as low-confidence rather than
forcing a misleading single-cluster label.

---

## TC-4 â€” Prohibited verdict â†’ skipped

| | |
|---|---|
| Input finding | `cwe=["CWE-0"]` (Prohibited/N-A entry), any path |
| Canonical mapping | `Prohibited` |
| Expected `status` | `skipped` |
| Expected behaviour | Not counted in cluster summary; no report entry |
| Test method | `test_classifier.TestClassifier.test_prohibited_is_skipped` |

**Why this matters:** Ensures Prohibited/N-A mapping nodes (Category, View,
and Deprecated CWEs) are cleanly excluded without causing a crash or a
misleading classification.

---

## TC-5 â€” CVEâ†’KEV fallback

| | |
|---|---|
| Input finding | `cve=["CVE-2021-44228"]`, no CWE, path `pom.xml`, producer Trivy |
| KEV table | CVE-2021-44228 â†’ `#2` (Log4Shell) |
| Expected `primary_cluster` | `#2` |
| Expected `status` | `classified` |
| Expected provenance | `table=tlctc-kev` |
| Test method | `test_classifier.TestClassifier.test_cve_fallback_via_kev` |

**Why this matters:** Validates the offline KEV fallback path. Trivy and
Grype often emit CVE identifiers without CWE; the KEV table provides
TLCTC cluster coverage for the 1,568 actively-exploited CVEs without
requiring a network call to NVD.

---

## TC-6 â€” Unmapped finding

| | |
|---|---|
| Input finding | `cve=["CVE-0000-0000"]` (not in KEV), no CWE |
| Expected `status` | `unmapped` |
| Expected behaviour | Appears in the JSON `unmapped` bucket; no cluster |
| Test method | `test_classifier.TestClassifier.test_unmapped` |

**Why this matters:** The classifier must handle findings with no
classifiable identifier gracefully â€” unmapped does not mean error.

---

## TC-7 â€” Multi-CWE: skippable CWE then valid CWE classifies

| | |
|---|---|
| Input finding | `cwe=["CWE-0", "CWE-89"]`, path `src/api/u.py`, producer CodeQL |
| Expected `primary_cluster` | `#2` (CWE-89 used; CWE-0 skipped) |
| Expected `status` | `classified` |
| Expected `provenance.identifier` | `CWE-89` |
| Test method | `test_classifier.TestClassifier.test_skippable_cwe_then_valid_cwe_classifies` |

**Why this matters:** A finding may carry multiple CWEs. A Prohibited/N-A
entry in position 0 must not short-circuit the search â€” the classifier must
continue to the next CWE and classify on the first usable hit.

---

## TC-8 â€” `--fail-on-cluster` exits 2

| | |
|---|---|
| Input | `semgrep-min.sarif` (contains a `#2` finding), `--fail-on-cluster "#2"` |
| Expected exit code | `2` |
| Test method | `test_cli.TestCli.test_fail_on_cluster_exits_nonzero` |

**Why this matters:** The CI gate. `--fail-on-cluster` must cause a non-zero
exit so the pipeline fails when nominated clusters appear. Exit code 2
distinguishes a gate trigger from a usage or config error.

---

## Acceptance criteria for v1

- All eight test cases reproduce the expected cluster, status, and provenance
  when run offline against the bundled fixtures.
- `python -m unittest discover tests` exits 0 with 28 tests.
- TC-1 and TC-5 additionally pass against a real Semgrep / Trivy scan
  before promoting to v1.0.0.
