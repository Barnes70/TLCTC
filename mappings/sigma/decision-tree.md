# SigmaHQ → TLCTC Decision Tree

This document specifies the **deterministic algorithm** used by [`generate-sigma-mapping.py`](generate-sigma-mapping.py) to derive a TLCTC cluster for every rule in the SigmaHQ rules corpus.

The algorithm is purely mechanical. Every output is traceable to two inputs:

1. The SigmaHQ rules clone (shallow, commit SHA recorded in output metadata)
2. `mappings/mitre-attack-enterprise/tlctc-enterprise-attack.json` (in-tree, pinned)

There is **no manual per-rule classification**.

---

## Stage 1 — Extract ATT&CK technique tags

For each Sigma rule YAML file:

```
                 Sigma rule YAML
                       │
                       ▼
              Read tags[] list
                       │
        ┌──────────────┴──────────────────┐
        │ No attack.t* tags               │ Has attack.t* tags
        ▼                                 ▼
techniques = []               For each matching tag:
(will → unmapped)               strip sub-technique suffix
                                attack.t1059.001 → T1059
                                attack.t1078.004 → T1078
                                    │
                                    ▼
                              deduplicate + sort
                              → techniques[]
```

**Sub-technique folding rule:** `attack.tXXXX.YYY` is always folded to `TXXXX`. The parent technique's entry in `tlctc-enterprise-attack.json` is used. Two sub-techniques of the same parent (e.g., `t1059.001` and `t1059.003`) produce a single `T1059` entry — no double-counting.

Non-technique tags (`attack.execution`, `attack.defense_evasion`, tactic labels, etc.) are silently skipped — they carry no technique ID.

---

## Stage 2 — Look up each technique in the ATT&CK→TLCTC index

For each technique ID in `techniques[]`:

```
    technique ID (e.g. T1059)
           │
           ▼
    Present in tlctc-enterprise-attack.json?
           │
    ┌──────┴──────┐
    │ No          │ Yes
    ▼             ▼
any_unmapped    Read tlctcMapping expression (e.g. "#1", "#2 | #3", "N/A")
= True                │
                      ▼
             _clusters(expr): extract #N refs, sort numerically
                      │
              ┌───────┴───────┐
              │ clusters = [] │ clusters = [...]
              │ (N/A or empty)│
              ▼               ▼
         any_unmapped     any_alt = True if len > 1
         = True           add clusters to cluster_set
```

`cluster_set` accumulates every cluster referenced across all the rule's techniques (deduplicated, sorted numerically).

---

## Stage 3 — Assign derivationStatus and primaryCluster

```
           cluster_set empty?
                 │
        ┌────────┴────────┐
        │ Yes             │ No
        ▼                 ▼
status = "unmapped"   any_alt OR len(cluster_set) > 1?
primaryCluster = null          │
                    ┌──────────┴──────────┐
                    │ Yes                 │ No
                    ▼                     ▼
           status = "ambiguous"  status = "ok"
```

**Partial resolution rule:** If at least one technique resolved (cluster_set non-empty) but at least one technique was absent from the ATT&CK index (`any_unmapped = True`), the record is `ambiguous` even if `cluster_set` would otherwise have a single entry. A partial result is not a clean result.

**`primaryCluster`** is always the **lowest-numbered cluster** in `cluster_set`:

```
cluster_set = ["#1", "#4", "#7"]  →  primaryCluster = "#1"
cluster_set = ["#7"]              →  primaryCluster = "#7"
cluster_set = []                  →  primaryCluster = null
```

For `ok` records this is unambiguous. For `ambiguous` records it is an auditable default — the full `clusterSet` array is always the authoritative coverage surface.

---

## Stage 4 — Emit the record

```json
{
  "ruleId":          "<Sigma rule GUID>",
  "ruleTitle":       "<Sigma rule title>",
  "logsource":       { <verbatim logsource block> },
  "techniques":      ["T1059", "T1078"],
  "clusterSet":      ["#1", "#4"],
  "primaryCluster":  "#1",
  "derivationStatus": "ambiguous"
}
```

No detection logic, condition blocks, or filter fields are copied. The output is license-safe for distribution.

---

## Status definitions

| Status | Meaning | `primaryCluster` |
|--------|---------|-----------------|
| `ok` | Every tagged technique resolved to a single concrete cluster, and `cluster_set` has exactly one entry | The one cluster |
| `ambiguous` | Multiple clusters in `cluster_set`, or at least one technique maps to an alternation (`#2 \| #3`), or partial resolution (`any_unmapped = True` with a non-empty `cluster_set`) | Lowest-numbered cluster (auditable default) |
| `unmapped` | No `attack.t*` tags present, or all tagged techniques are absent from `tlctc-enterprise-attack.json` | `null` |

---

## Worked Examples

### Example 1 — `ok` status (clean.yml)

**Rule:** `Suspicious PowerShell Download`
**Tags:** `attack.execution`, `attack.t1059`

```
tags → strip non-technique tags → techniques = ["T1059"]

T1059 in tlctc-enterprise-attack.json? → Yes
tlctcMapping = "#1"
clusters("​#1") → ["#1"]

cluster_set = ["#1"]   any_alt = False   any_unmapped = False
→ status = "ok"   primaryCluster = "#1"
```

**Output:**
```json
{
  "techniques": ["T1059"],
  "clusterSet": ["#1"],
  "primaryCluster": "#1",
  "derivationStatus": "ok"
}
```

---

### Example 2 — `ambiguous` status (multi-technique rule)

**Rule:** `Bitbucket Global SSH Settings Changed`
**Tags:** `attack.t1021`, `attack.t1685`

```
techniques = ["T1021", "T1685"]

T1021 → tlctcMapping = "#1 | #4"
clusters("#1 | #4") → ["#1", "#4"]   any_alt = True

T1685 → absent from index   any_unmapped = True

cluster_set = ["#1", "#4"]   any_alt = True
→ status = "ambiguous"   primaryCluster = "#1"
```

**Output:**
```json
{
  "techniques": ["T1021", "T1685"],
  "clusterSet": ["#1", "#4"],
  "primaryCluster": "#1",
  "derivationStatus": "ambiguous"
}
```

The `ambiguous` status here has two independent causes: the alternation in T1021's mapping, and the partial resolution from T1685. Both are expected and auditable.

---

### Example 3 — `unmapped` status (untagged.yml)

**Rule:** `Generic Anomaly`
**Tags:** `attack.defense_evasion`

```
tags → strip non-technique tags (defense_evasion is a tactic label, not t*) → techniques = []

cluster_set = []
→ status = "unmapped"   primaryCluster = null
```

**Output:**
```json
{
  "techniques": [],
  "clusterSet": [],
  "primaryCluster": null,
  "derivationStatus": "unmapped"
}
```

`unmapped` is **not** a classification error — it means the rule author did not tag this rule with a technique ID, or tagged it only with tactic labels. These records are detection coverage blind spots from a TLCTC perspective.

---

## Output guarantees

- **Total records equal rule count** — every parseable `.yml` file in the rules directory produces exactly one record.
- **Status buckets sum to total** — no uncategorised records.
- **`primaryCluster` is always in `clusterSet`** — or both are absent for `unmapped` records.
- **Idempotency** — two consecutive runs against the same rules clone produce byte-identical outputs.

## Why this approach over alternatives

| Alternative | Why not |
|-------------|---------|
| Per-rule manual classification | 3,000+ rules — impractical; tagging is already encoded by rule authors |
| CWE-based derivation | Sigma rules don't carry CWE references; ATT&CK is the natural tag vocabulary |
| Vendor-defined bundles (Splunk/Elastic packs) | Platform-specific; Sigma is vendor-neutral by design |
| Keep sub-technique granularity | Parent-level mapping is the stable surface in `tlctc-enterprise-attack.json`; sub-technique distinctions are not modeled |
