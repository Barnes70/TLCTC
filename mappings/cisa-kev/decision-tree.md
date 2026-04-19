# CISA KEV → TLCTC Decision Tree

This document specifies the **deterministic algorithm** used by [`generate-kev-mapping.py`](generate-kev-mapping.py) to derive a TLCTC cluster for every CVE in the CISA Known Exploited Vulnerabilities catalog.

The algorithm is purely mechanical. Every output is traceable to one of three inputs:

1. The pinned KEV snapshot (CISA)
2. `mappings/mitre-cwe/tlctc-cwe.json` (classification source of truth)
3. `mappings/cisa-kev/product-role-heuristic.json` (R-ROLE tie-breaking)

There is **no manual per-CVE classification**.

---

## Stage 1 — Per-CWE derivation

For each CWE listed in the KEV entry's `cwes[]`:

```
                     KEV entry
                        │
                        ▼
               Extract cwes[] list
                        │
        ┌───────────────┴──────────────┐
        │ cwes[] is empty              │ cwes[] has entries
        ▼                              ▼
status = cwe-missing         For each CWE:
                                  │
                                  ▼
                       CWE in tlctc-cwe.json?
                                  │
                 ┌────────────────┴────────────────┐
                 │ No                              │ Yes
                 ▼                                 ▼
     status = cwe-unmapped-in-tlctc      Read tlctcMapping + mappingVerdict
                                                  │
                                ┌─────────────────┼─────────────────────┐
                                ▼                 ▼                     ▼
                  tlctcMapping == "N/A"   verdict in                 otherwise
                                         (Discouraged, Prohibited)      │
                                ▼                 ▼                     ▼
                     status = cwe-too-abstract (both branches)      status = ok
```

**Why `Discouraged`/`Prohibited` are treated as `cwe-too-abstract`:** CWE-20 (the largest KEV CWE bucket) is `Discouraged` in the CWE→TLCTC mapping because it spans #1/#2/#3/#6. A per-CVE derivation through CWE-20 yields no actionable cluster — it must be flagged, not silently assigned.

## Stage 2 — Collapse across multiple CWEs

KEV entries can reference multiple CWEs. The collapse rule:

- If all per-CWE statuses are identical → that status wins.
- Otherwise → `mixed`.

The primary expression for the output record is taken from the **first CWE with status `ok`** (if any exist). All OK CWEs contribute to `clusterSet` (deduplicated, stats-only).

## Stage 3 — Primary cluster extraction

Given a `tlctcMapping` expression, the primary cluster is derived by parsing the notation grammar from [`tlctc-cwe.json`](../mitre-cwe/tlctc-cwe.json):

| Notation | Rule | Example |
|----------|------|---------|
| `A → B` | `A` enables/leads to `B`. Primary = `A` (the cause). | `#2 → #7` → primary `#2` |
| `A \| B` | Either `A` or `B` depending on context. Primary = `A` (left-most). | `#2 \| #3` → primary `#2` |
| Composite | Arrow binds tighter than `\|`. Parse prefix before `→`, then first alternative. | `#2 → #7 \| #3` → prefix `#2` → primary `#2` |

**The full expression is preserved in `derivedMappingExpression` verbatim.** `clusterSet` flattens the expression for stats queries but is never the primary surface.

## Stage 4 — R-ROLE disambiguation

The CWE mapping bucket `#2 | #3` (219 CWEs, the largest single bucket after role-collapse) is **not a classification failure** — it's a deliberate reflection of [R-ROLE](../../CLAUDE.md): the same memory-corruption weakness is `#2` in server-side code, `#3` in client-side code.

KEV already encodes the context in `vendorProject` + `product`. The heuristic recovers it.

```
derivedMappingExpression contains "#2 | #3" (either order)?
                    │
          ┌─────────┴─────────┐
          │ No                │ Yes
          ▼                   ▼
contextResolvedBy =   Apply product-role-heuristic.json rules,
  "cwe-unambiguous"   first-match-wins, on
                      "<vendorProject> :: <product>" (case-insensitive)
                                       │
                        ┌──────────────┴──────────────┐
                        │ Rule matched                 │ No rule matched
                        ▼                              ▼
        primaryCluster = rule.role         primaryCluster = left-most alt (#2)
        contextResolvedBy =                contextResolvedBy = "unresolved"
          "product-heuristic"
        contextHeuristicNotes = rule.notes
```

### Heuristic rule structure

Rules are ordered top-to-bottom; the first match wins. Two rule forms:

```json
{ "pattern": "Exchange Server", "role": "#2", "notes": "Mail server." }
{ "pattern_vendor": "Apple",    "role": "#3", "notes": "Apple's KEV-listed products are overwhelmingly client-side." }
```

- `pattern` — substring match anywhere in `"<vendor> :: <product>"`.
- `pattern_vendor` — exact (case-insensitive) match against `vendorProject`.

**Narrow patterns always precede vendor-wide defaults.** A vendor-wide default is the fallback when none of the specific product rules fire for that vendor. See [`product-role-heuristic.json`](product-role-heuristic.json) for the full rule set.

### Why `unresolved` is a valid outcome

When no rule fires for a `#2 | #3` entry, the record carries `contextResolvedBy: "unresolved"` with `primaryCluster` defaulting to the left-most alternative (`#2`). This is an auditable state — a reviewer can grep for unresolved records and decide whether to add new rules. It is **never silently assigned**.

## Stage 5 — Confidence inheritance

Per-row `confidence` is the source CWE's `mappingVerdict`. For multi-CWE KEV entries, the **weakest verdict** across all contributing CWEs is chosen (conservative strategy):

```
Prohibited < Discouraged < Unreviewed < Allowed-with-Review < Allowed
```

**Never use a uniform confidence.** Rolling all rows into a single "Allowed" would hide the fact that CWE-20-class derivations (`cwe-too-abstract`) and ambiguous `Allowed-with-Review` CWEs mix with high-confidence ones. Downstream stats **must** segment by `confidence` before publishing aggregate cluster counts.

## Output guarantees

- **Total records equal catalog count** (1,568 for v2026.04.14).
- **Status buckets sum to total** — no uncategorised records.
- **Ransomware count is preserved** from source (313 in v2026.04.14).
- **Idempotency** — two consecutive runs produce byte-identical outputs.

## Why this approach over alternatives

| Alternative | Why not |
|-------------|---------|
| Merge into `tlctc-cwe.json` | CWE mapping is a stable release; KEV refreshes weekly. Would force either stale KEV data or weekly CWE-mapping revisions. |
| Per-CVE manual classification | Compounds review burden by 1,500+ entries for marginal gain over mechanical derivation. |
| Attack-path integration only | Misses the strategic "which cluster is under active weaponization?" question. |
| Skip R-ROLE heuristic | Every ASA/Fortinet/Ivanti CVE would claim client-side exposure — unreadable. Every Chrome/Safari CVE would claim server-side — wrong. |
