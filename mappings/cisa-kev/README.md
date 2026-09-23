# CISA KEV → TLCTC Mapping

This directory derives a **TLCTC cluster view of the CISA Known Exploited Vulnerabilities (KEV) catalog** — the authoritative list of CVEs currently being exploited in the wild.

> ### ⚠ Compounded experimental signal — read before using
>
> This artifact is **derived** from the [`mitre-cwe/tlctc-cwe.json`](../mitre-cwe/README.md) mapping, which is AI-generated and marked experimental. Every row here carries a **per-row `confidence`** inherited from the source CWE's `mappingVerdict` (weakest across multiple CWEs). Do not treat aggregate counts as authoritative without reading the segmented-by-confidence numbers in `tlctc-kev-stats.json`.

## Purpose

TLCTC's existing mappings ([MITRE ATT&CK](../mitre-attack-enterprise/), [MITRE CWE](../mitre-cwe/)) are **static and cause-side** — they answer *"which cluster does this technique/weakness belong to?"*. Neither carries an **actively-exploited signal**.

CISA KEV is updated weekly. Cross-walked through TLCTC, it answers a question the static mappings cannot:

> **Which TLCTC clusters are under active weaponization this month — and which are ransomware-linked?**

That is the question this artifact is built to answer.

## Files

| File | Description |
|------|-------------|
| [`input/known_exploited_vulnerabilities.v2026.04.14.json`](input/known_exploited_vulnerabilities.v2026.04.14.json) | Pinned CISA KEV snapshot (for reproducibility) |
| [`product-role-heuristic.json`](product-role-heuristic.json) | Vendor/product rules that resolve the `#2 \| #3` R-ROLE ambiguity |
| [`generate-kev-mapping.py`](generate-kev-mapping.py) | Deterministic ETL: regenerates outputs from pinned inputs |
| [`tlctc-kev.json`](tlctc-kev.json) | Derived per-CVE mapping (1,568 entries) |
| [`tlctc-kev-stats.json`](tlctc-kev-stats.json) | Aggregate statistics (cluster counts, ransomware, top vendors, monthly histograms) |
| [`decision-tree.md`](decision-tree.md) | CVE → CWE → TLCTC traversal algorithm |
| [`examples/cluster-exposure-walkthrough.md`](examples/cluster-exposure-walkthrough.md) | Worked example: vendor-stack → exposure profile |

## Data Pipeline

```
CISA KEV snapshot          tlctc-cwe.json             product-role-heuristic.json
(pinned)                   (AI-generated)             (reviewed rules)
     │                           │                            │
     └───────────┬───────────────┴──────────────┬─────────────┘
                 ▼                              ▼
         generate-kev-mapping.py  (deterministic, idempotent)
                 │
     ┌───────────┴────────────┐
     ▼                        ▼
tlctc-kev.json         tlctc-kev-stats.json
```

Each CVE is classified mechanically: **CVE → CWE(s) → TLCTC cluster expression**. R-ROLE `#2 | #3` ambiguities are disambiguated via a small, versioned vendor/product heuristic (e.g., "Exchange Server → #2", "Chrome → #3"). See [`decision-tree.md`](decision-tree.md).

## Record Schema (`tlctc-kev.json` entries)

```json
{
  "cveID": "CVE-2026-20131",
  "vendorProject": "Cisco",
  "product": "Secure Firewall Management Center (FMC)",
  "vulnerabilityName": "... Deserialization of Untrusted Data Vulnerability",
  "dateAdded": "2026-03-19",
  "dueDate": "2026-03-22",
  "knownRansomwareCampaignUse": "Known",
  "shortDescription": "...",
  "sourceCwes": ["CWE-502"],
  "derivedMappingExpression": "#2 | #3",
  "primaryCluster": "#2",
  "clusterSet": ["#2", "#3"],
  "confidence": "Allowed",
  "derivationStatus": "ok",
  "contextResolvedBy": "product-heuristic",
  "contextHeuristicNotes": "FMC is a management server — server role.",
  "sourceCweTrace": [ ... ]
}
```

### Field Reference

| Field | Description |
|-------|-------------|
| `sourceCwes` | Raw CWE list from the KEV entry (verbatim) |
| `derivedMappingExpression` | The source CWE's `tlctcMapping` **verbatim** (e.g., `#2 → #7 \| #3`). Preserves the notation grammar — never union-collapsed. |
| `primaryCluster` | Canonical cluster: prefix before `→` and first alternative before `\|`, then R-ROLE-resolved if applicable |
| `clusterSet` | Deduplicated flat set of every cluster referenced — **for stats only**, never the primary surface |
| `confidence` | Inherited from source CWE's `mappingVerdict`; weakest across multiple CWEs |
| `derivationStatus` | See enum below |
| `contextResolvedBy` | See enum below |

### `derivationStatus` enum

Four orthogonal failure modes — **do not collapse**:

| Value | Meaning |
|-------|---------|
| `ok` | Primary cluster derived from at least one mapped CWE with verdict `Allowed` or `Allowed-with-Review` |
| `cwe-missing` | KEV entry has no `cwes[]` array (disproportionately hits recent high-profile CVEs) |
| `cwe-too-abstract` | Source CWE's `tlctcMapping` is `N/A`, OR verdict is `Discouraged`/`Prohibited` (CWE-20 class — the single largest KEV bucket) |
| `cwe-unmapped-in-tlctc` | CWE not present in `tlctc-cwe.json` |
| `mixed` | Multiple source CWEs with heterogeneous statuses |

### `contextResolvedBy` enum

| Value | Meaning |
|-------|---------|
| `cwe-unambiguous` | Source CWE has no `#2 \| #3` alternation |
| `product-heuristic` | `#2 \| #3` ambiguity resolved by a rule in `product-role-heuristic.json` |
| `unresolved` | `#2 \| #3` present but no heuristic rule matched (or no CWE at all); `primaryCluster` falls back to the left-most alternative |

## Statistics (catalog version 2026.04.14; TLCTC v2.6 CWE mapping)

### Coverage

- **1,568** total entries
- **313** ransomware-linked (`knownRansomwareCampaignUse: "Known"`) — 19.96% of catalog
- **976** (`ok`) derivation-complete records
- **167** (`cwe-missing`) — KEV entry carries no CWE reference
- **291** (`cwe-too-abstract`) — dominated by CWE-20 (Improper Input Validation)
- **94** (`cwe-unmapped-in-tlctc`)
- **40** (`mixed`)

### Primary Cluster Distribution (OK records only)

| Cluster | Count | Ransomware |
|---------|-------|------------|
| `#2` Exploiting Server | 547 | 129 |
| `#3` Exploiting Client | 210 | 10 |
| `#1` Abuse of Functions | 166 | 47 |
| `#10` Supply Chain Attack | 15 | 1 |
| `#5` Man in the Middle | 12 | 0 |
| `#4` Identity Theft | 11 | 1 |
| `#6` Flooding Attack | 8 | 5 |
| `#9` Social Engineering | 3 | 0 |

### R-ROLE Disambiguation

- **400** entries — `cwe-unambiguous` (source CWE not context-dependent)
- **365** entries — `product-heuristic` fired (350 of them in `ok` status)
- **803** entries — `unresolved` (includes all `cwe-missing`, `cwe-too-abstract`, `cwe-unmapped-in-tlctc`; plus 241 `ok`-status `#2 | #3` entries where no rule matched)

The v2.6 regeneration (2026-09-23) moved `#10` from 20 to 15 and `#5` from 2 to 12: the snapshot had last been derived from an earlier CWE mapping, before the 2026-08 re-audit and the v2.6 subversion test (a flaw in a legitimately supplied component is classified where it is exploited, not `#10`). The same regeneration fixed R-ROLE detection: path-form expressions such as `#2 → #7 | #3 → #7` (CWE-94, CWE-502) are now routed through the product-role heuristic like `#2 | #3`, so a document-borne Office exploit resolves to `#3` instead of defaulting to the left-most `#2`.
## Refresh Procedure

```bash
# Regenerate from pinned snapshot (deterministic, CI-safe):
python mappings/cisa-kev/generate-kev-mapping.py

# Rebuild ad-hoc against the live CISA feed (for investigation only,
# NEVER in CI — tagged releases must be reproducible from in-tree inputs):
python mappings/cisa-kev/generate-kev-mapping.py --fetch
```

To pin a new KEV snapshot:

1. Download from <https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json>.
2. Save as `input/known_exploited_vulnerabilities.v<YYYY.MM.DD>.json` (use the `catalogVersion` as the date suffix).
3. Update `DEFAULT_KEV_INPUT` in `generate-kev-mapping.py`.
4. Regenerate. Commit all four files in one changeset.

## Verification

Run the generator twice; outputs are byte-identical. The generator also:

- Preserves the KEV input order (no re-sort) so diffs between snapshots are minimal.
- Enumerates every KEV entry — `len(entries) == catalog.count`.
- Sums `by_derivation_status` buckets to `total_records` (no uncategorised records).

## License

CC BY 4.0 — see [LICENSE](../../LICENSE). Derived from the [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) (public domain) and the [TLCTC CWE mapping](../mitre-cwe/) (CC BY 4.0).
