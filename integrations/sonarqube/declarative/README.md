# Declarative Starter — Zero-Python Path

For teams who want TLCTC tags inside their SonarQube instance without running
the `tlctc-sonar` CLI in CI. This tier loses the context-aware (R-ROLE) logic
and rich per-issue reports — it gives you a tag namespace, a severity-uplift
quality profile, and a portfolio dashboard.

## Contents

| File | Purpose |
|---|---|
| `tlctc-tags-import.csv` | The 10 cluster tags (`tlctc-01` … `tlctc-10`) with descriptions and links to the TLCTC cluster definitions. |
| `quality-profile-tlctc.xml` | Quality profile overlay that raises severity on the hot rules for R-EXEC (#7), R-CRED (#4), and supply chain (#10). Java-targeted; copy and adapt the `<rule>` entries for your other languages. |
| `tlctc-dashboard.json` | SonarQube portfolio definition that pivots projects by cluster tag. Replace the empty `projects` array with your tenant's project keys before import. |
| `webhook-payload-example.json` | **Reference only** — documents the payload a future webhook receiver would consume. No receiver is shipped in v1. |

## What you can do with these

1. **Tag findings manually.** Sonar's `/api/issues/set_tags` endpoint accepts
   any tag name. Loop the CSV via curl to seed the tags as suggestions in your
   instance, then apply them by hand to specific findings — or via the CLI in
   the parent directory when you're ready to automate.
2. **Pre-elevate severity** on rules that map to high-impact clusters. The
   quality profile sets BLOCKER on SQLi, command injection, deserialization,
   and hardcoded credentials.
3. **Aggregate cluster exposure** across projects via the portfolio definition.

## Seeding the tag namespace (curl one-liner)

SonarQube has no bulk tag-import endpoint, but creating tags on the fly works:

```sh
# Apply the full cluster namespace to one canary issue, then untag it.
ISSUE_KEY="AYZ...your-canary-issue..."
TOKEN="<your sonar token>"
URL="https://sonarqube.example.com"
TAGS=$(awk -F',' 'NR>1 {printf "%s%s", sep, $1; sep=","}' tlctc-tags-import.csv)
curl -u "$TOKEN:" -X POST "$URL/api/issues/set_tags" \
    -d "issue=$ISSUE_KEY" -d "tags=$TAGS"
```

After the request, every cluster tag exists in the tenant's tag suggestion
list. The descriptions in the CSV are reference material for your team — Sonar
itself does not store per-tag descriptions, so paste them into your wiki or
README instead.

## Limitations vs the CLI tier

| Feature | Declarative tier | CLI tier (`../cli/`) |
|---|---|---|
| Tag namespace | ✓ | ✓ |
| Quality profile uplift | ✓ | — (orthogonal; use both) |
| Portfolio dashboard | ✓ | — (orthogonal; use both) |
| Auto-classify findings by CWE | — | ✓ |
| R-ROLE context resolution (#2 vs #3) | — | ✓ |
| Sequence tagging (`#2 → #7`) | — | ✓ |
| SARIF output | — | ✓ |
| PR-comment Markdown | — | ✓ |
| CI gate via `--fail-on-cluster` | — | ✓ |

The two tiers are designed to be used together: import the declarative assets
once at platform setup, then run the CLI in CI for per-PR classification.
