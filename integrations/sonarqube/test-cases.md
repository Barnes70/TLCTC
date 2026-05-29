# Test Cases

Each TC pins one TLCTC classification rule. All cases are runnable offline
against `examples/sample-issues-response.json` using the `file://` URL form:

```sh
python -m cli classify \
    --config       examples/tlctc-sonar.json \
    --sonar-url    "file://$PWD/examples/sample-issues-response.json" \
    --token        x --project-key demo \
    --out-json     /tmp/out.json
```

Then inspect the JSON for the per-issue classification. The unit tests in
`tests/` cover the same logic against `tests/fixtures/tiny-cwe-mapping.json`.

---

## TC-1 — CWE-89 SQL Injection (Axiom VI)

| | |
|---|---|
| Input issue | `ISSUE-001` &middot; `cwe:89` on `demo:src/main/java/com/example/UserRepo.java` |
| Canonical mapping | `#2` (Exploiting Server) — `Allowed`, not context-dependent |
| Expected primary cluster | `#2` |
| Expected tags | `tlctc-02` |
| SARIF result count | 1 (single-cluster mapping; no `relatedLocations`) |
| Role resolution | n/a — single cluster, no alternation |

**Why this matters:** Axiom VI's single-cluster rule. The blog prototype
suggested `#2 → #7` for SQLi, but the canonical mapping classifies CWE-89 as
`#2` only — SQLi exfiltrates data via the server's data layer; it does not by
itself execute foreign code in the server process. If SQLi were chained with
RCE that would be a separate step.

---

## TC-2 — CWE-79 XSS on a server-side template (R-ROLE → server)

| | |
|---|---|
| Input issue | `ISSUE-002` &middot; `cwe:79` on `demo:src/main/java/com/example/render/JspRenderer.java` |
| Canonical mapping | `#2 → #7 \| #3` — `Allowed`, context-dependent |
| Expected primary cluster | `#2` (server branch chosen) |
| Expected tags | `tlctc-02`, `tlctc-07` (sequence) |
| SARIF result count | 1 result on `tlctc-02`, with `#7` chained via `relatedLocations` |
| Role resolution | server glob `**/src/main/java/**` matches |

**Why this matters:** R-ROLE. The same CWE-79 produces a different cluster
depending on where the vulnerable code runs. Server-side rendering reaches
into the response stream from inside the trust boundary, so the server-role
branch (`#2 → #7`) applies.

---

## TC-3 — CWE-79 XSS on a client-side TSX file (R-ROLE inverse → client)

| | |
|---|---|
| Input issue | `ISSUE-003` &middot; `cwe:79` on `demo:src/main/webapp/components/CommentList.tsx` |
| Canonical mapping | `#2 → #7 \| #3` — same entry as TC-2 |
| Expected primary cluster | `#3` (client branch chosen) |
| Expected tags | `tlctc-03` |
| SARIF result count | 1 result on `tlctc-03`, no chained `#7` |
| Role resolution | client glob `**/*.tsx` matches; client checked first because it is more specific |

**Why this matters:** R-ROLE inverse. Same CWE, same rule entry, opposite
cluster — proving the resolver is path-driven, not CWE-driven. Demonstrates
why hand-built CWE→cluster tables in tools (like the blog prototype's tiny
in-memory map) are insufficient.

---

## TC-4 — CWE-798 Hardcoded credentials (R-CRED)

| | |
|---|---|
| Input issue | `ISSUE-004` &middot; `cwe:798` on `demo:src/main/java/com/example/config/AwsClient.java` |
| Canonical mapping | `#4` (Identity Theft) — `Allowed` |
| Expected primary cluster | `#4` |
| Expected tags | `tlctc-04` |
| SARIF result count | 1 |
| Role resolution | n/a — single cluster |

**Why this matters:** R-CRED. Credential *acquisition* maps to the enabling
cluster; credential *application* is always `#4`. Hardcoded credentials are
*both* — the source code contains an attacker-extractable artifact, and any
use of that artifact authenticates as the owner. The canonical mapping
chooses the application side (`#4`) because that is the lasting threat.
Result: no `→ #7` step. Anyone classifying SAST hardcoded-creds findings as
`#7` (Malware) is conflating outcome with cause.

---

## TC-5 — CWE-20 Improper Input Validation (Axiom III, verdict filter)

| | |
|---|---|
| Input issue | `ISSUE-005` &middot; `cwe:20` on `demo:src/main/java/com/example/api/UploadHandler.java` |
| Canonical mapping | `N/A` (Generic Root Cause) — `Discouraged` |
| Expected outcome | No tag applied; issue appears in the Markdown "Low-confidence" collapsible section; exit code 0 |
| `cluster_summary` impact | None — Discouraged CWEs are excluded from the primary summary |
| Role resolution | n/a |

**Why this matters:** Axiom III (cause vs consequence) and the verdict
gating. CWE-20 is an umbrella for "the program didn't validate something."
That is a *root cause* shared by `#1`, `#2`, `#3`, and `#6` depending on the
specific abuse. Classifying it as any single cluster would be misleading;
the responsible action is to surface it as low-confidence and ask the
analyst to drill to a more specific child CWE.

---

## TC-6 — CWE-502 Insecure Deserialization (`#2 → #7 | #3 → #7`)

| | |
|---|---|
| Input issue | `ISSUE-006` &middot; `cwe:502` on `demo:src/main/java/com/example/api/SessionLoader.java` |
| Canonical mapping | `#2 → #7 \| #3 → #7` — `Allowed`, context-dependent |
| Expected primary cluster | `#2` (server branch chosen) |
| Expected tags | `tlctc-02`, `tlctc-07` |
| SARIF result count | 1 result on `tlctc-02`, with `#7` chained via `relatedLocations` |
| Role resolution | server glob `**/api/**` matches |

**Why this matters:** Parser coverage of the "both branches end in `#7`"
shape (7 entries in the canonical mapping use this form). The `→ #7` step
is preserved in both branches; the resolver picks the role, the sequence
parser preserves the chain.

---

## TC-7 — CWE-829 Supply Chain (`#10 → #7`) (R-SUPPLY)

| | |
|---|---|
| Input issue | `ISSUE-007` &middot; `cwe:829` on `demo:pom.xml` |
| Canonical mapping | `#10 → #7` — `Allowed` |
| Expected primary cluster | `#10` (Trust Acceptance Event) |
| Expected tags | `tlctc-10`, `tlctc-07` |
| SARIF result count | 1 result on `tlctc-10`, with `#7` chained via `relatedLocations` |
| Role resolution | n/a — no alternation |

**Why this matters:** R-SUPPLY places `#10` at the *Trust Acceptance Event* —
the moment the trust artifact (here, the dependency declaration) becomes
authoritative inside the target domain. The chained `→ #7` records that the
accepted artifact then runs as code. The blog prototype's tiny CWE map had
no story for supply-chain CWEs at all.

---

## Acceptance criteria for v1

- All seven test cases reproduce the expected primary cluster, tag set, and
  SARIF result count when run offline against
  `examples/sample-issues-response.json`.
- `python -m unittest discover tests` exits 0 with 40 tests.
- Validate run reports the mapping version as `2.1` and at least 985 entries.
- TC-1, TC-2, and TC-4 additionally pass against a live SonarQube smoke
  project before promoting to v1.0.0.
