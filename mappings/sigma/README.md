# SigmaHQ → TLCTC Mapping

This directory derives a **TLCTC cluster view of SigmaHQ detection rules** — the community-maintained library of Sigma detection rules covering ATT&CK-tagged threats across hundreds of log sources.

> ### Experimental derivation chain — read before using
>
> This artifact is **derived** from [`mitre-attack-enterprise/tlctc-enterprise-attack.json`](../mitre-attack-enterprise/README.md), which classifies 698 ATT&CK Enterprise techniques into TLCTC clusters. That upstream mapping is the source of truth. Mapping quality is bounded by (a) how consistently each Sigma rule's author tagged it with `attack.t*` tags, and (b) the quality of the ATT&CK→TLCTC mapping for those techniques. Untagged rules and rules whose techniques are absent from the ATT&CK mapping surface as `unmapped` or `ambiguous`.

## Purpose

TLCTC's existing mappings ([MITRE ATT&CK](../mitre-attack-enterprise/), [MITRE CWE](../mitre-cwe/)) answer *"which cluster does this technique/weakness belong to?"* from a static, cause-side perspective.

The Sigma mapping answers a different question:

> **Given the detection rules your SOC runs today, which TLCTC clusters are you actually detecting — and how many rules cover each cluster?**

This is a **coverage audit**: it lets you cross-walk your operational detection library against the strategic cluster model. Rules that surface as `unmapped` are detection blind spots from a TLCTC perspective, not classification failures.

## Files

| File | Description |
|------|-------------|
| [`generate-sigma-mapping.py`](generate-sigma-mapping.py) | Deterministic ETL: reads a local SigmaHQ rules clone and writes the two output files |
| [`tlctc-sigma.json`](tlctc-sigma.json) | Derived per-rule mapping (3,132 entries, SigmaHQ commit `994da1665119`) |
| [`tlctc-sigma-stats.json`](tlctc-sigma-stats.json) | Aggregate statistics (cluster distribution, status counts, logsource breakdown) |
| [`decision-tree.md`](decision-tree.md) | Resolution algorithm: ATT&CK tag → TLCTC cluster |

## Data Pipeline

```
SigmaHQ rules clone         tlctc-enterprise-attack.json
(shallow clone,              (698 techniques, in-tree)
 commit SHA recorded)              │
        │                          │
        └──────────┬───────────────┘
                   ▼
       generate-sigma-mapping.py  (deterministic, idempotent)
                   │
       ┌───────────┴────────────┐
       ▼                        ▼
tlctc-sigma.json         tlctc-sigma-stats.json
```

Each rule is classified mechanically: **Sigma rule `attack.t*` tags → parent technique IDs → `tlctc-enterprise-attack.json` → cluster expression → `clusterSet` + `primaryCluster` + `derivationStatus`**. No rule detection bodies are copied. See [`decision-tree.md`](decision-tree.md) for the full traversal algorithm.

## Record Schema (`tlctc-sigma.json` entries)

```json
{
  "ruleId": "195e1b9d-bfc2-4ffa-ab4e-35aef69815f8",
  "ruleTitle": "Bitbucket Full Data Export Triggered",
  "logsource": {
    "product": "bitbucket",
    "service": "audit"
  },
  "techniques": ["T1213"],
  "clusterSet": ["#1"],
  "primaryCluster": "#1",
  "derivationStatus": "ok"
}
```

### Field Reference

| Field | Description |
|-------|-------------|
| `ruleId` | Sigma rule GUID (`id` field verbatim from the rule YAML) |
| `ruleTitle` | Sigma rule title (`title` field verbatim) |
| `logsource` | Sigma `logsource` block verbatim (product, category, service, etc.) |
| `techniques` | Parent ATT&CK technique IDs derived from `attack.t*` tags; sub-techniques are **folded to their parent** (e.g., `attack.t1059.001` → `T1059`) |
| `clusterSet` | Deduplicated flat set of every TLCTC cluster referenced by all resolved techniques — **for stats and coverage queries only**, never the primary surface |
| `primaryCluster` | Canonical cluster: lowest-numbered cluster in `clusterSet`. `null` when `derivationStatus` is `unmapped` |
| `derivationStatus` | See enum below |

### `derivationStatus` enum

| Value | Meaning |
|-------|---------|
| `ok` | All tagged techniques resolved to exactly one concrete cluster — `clusterSet` has a single entry |
| `ambiguous` | Tagged techniques resolve to multiple clusters, or at least one technique maps to an alternation expression (e.g., `#2 \| #3`), or partial resolution — at least one technique resolved while another was absent from the ATT&CK mapping (so `clusterSet` may hold a single entry) — `primaryCluster` is the lowest-numbered fallback |
| `unmapped` | Rule carries no `attack.t*` tags, or every tagged technique is absent from `tlctc-enterprise-attack.json` — `primaryCluster` is `null` |

`primaryCluster` is always the **lowest-numbered** cluster in `clusterSet` (e.g., if `clusterSet` is `["#1","#7"]` then `primaryCluster` is `"#1"`). For `ok` records this is unambiguous; for `ambiguous` records it is an auditable default, not a confident assertion.

## How to Regenerate

**Build dependency:** PyYAML only. The committed JSON output requires no dependencies to consume.

```bash
# 1. Install PyYAML if not present
pip install pyyaml

# 2. Shallow-clone SigmaHQ rules (outside the repo working tree)
git clone --depth 1 https://github.com/SigmaHQ/sigma /tmp/sigma   # Linux/macOS
git clone --depth 1 https://github.com/SigmaHQ/sigma "$env:TEMP\sigma"  # PowerShell

# 3. Capture the commit SHA
git -C /tmp/sigma rev-parse HEAD   # Linux/macOS
git -C "$env:TEMP\sigma" rev-parse HEAD  # PowerShell

# 4. Run the generator from the repo root
python mappings/sigma/generate-sigma-mapping.py \
  --rules-dir /tmp/sigma/rules \
  --sigma-commit <SHA>
```

Outputs are written directly to `mappings/sigma/tlctc-sigma.json` and `mappings/sigma/tlctc-sigma-stats.json`. The generator is deterministic and idempotent — running it twice against the same rules clone produces byte-identical outputs.

The SigmaHQ clone must live **outside the repository working tree** so it is never accidentally staged.

## Statistics (SigmaHQ commit `994da16651194500b607a3007186c29779e1f961`, 2026-05-31)

Full statistics are in [`tlctc-sigma-stats.json`](tlctc-sigma-stats.json).

### Coverage

- **3,132** total rules processed
- **739** (`ok`) — single concrete cluster derived
- **1,834** (`ambiguous`) — multiple or alternating clusters; `primaryCluster` is the lowest-numbered fallback
- **559** (`unmapped`) — no `attack.t*` tags, or all tagged techniques absent from the ATT&CK→TLCTC mapping

### Primary Cluster Distribution (OK records only)

| Cluster | Count |
|---------|-------|
| `#1` Abuse of Functions | 520 |
| `#7` Malware | 53 |
| `#4` Identity Theft | 100 |
| `#2` Exploiting Server | 36 |
| `#9` Social Engineering | 15 |
| `#5` Man in the Middle | 6 |
| `#6` Flooding Attack | 5 |
| `#8` Physical Attack | 2 |
| `#10` Supply Chain Attack | 2 |

The dominance of `#1` (Abuse of Functions) reflects the composition of the SigmaHQ corpus: a large share of rules detect post-exploitation behaviors — LOLBIN execution, administrative-tool abuse, configuration changes — that map to the Abuse of Functions cluster via techniques such as T1059, T1204, T1218, T1569.

## Caveats

- **Tagging quality dependent.** Rules that lack `attack.t*` tags are `unmapped`. The 559 `unmapped` records and 1,834 `ambiguous` records do not indicate classification failures — they reflect the tagging density of the SigmaHQ corpus and the breadth of the upstream ATT&CK→TLCTC mapping.
- **Derived from an experimental AI-generated ATT&CK mapping.** `tlctc-enterprise-attack.json` was produced with AI assistance and is marked experimental. Downstream cluster assignments inherit that uncertainty.
- **Sub-technique folding.** `attack.t1059.001` and `attack.t1059.003` both fold to `T1059`; the parent technique's mapping is used. Sub-technique-level distinctions are not preserved.
- **No rule detection bodies vendored.** Only `id`, `title`, `logsource`, derived `techniques`, and TLCTC derivation fields are committed. Sigma rule detection logic is NOT reproduced — this artifact is license-safe for distribution.
- **Point-in-time snapshot.** The committed JSON reflects SigmaHQ at commit `994da16651194500b607a3007186c29779e1f961`. Regenerate against a fresh clone to pick up new or changed rules.

## License

CC BY 4.0 — see [LICENSE](../../LICENSE). Derived from the [SigmaHQ rules repository](https://github.com/SigmaHQ/sigma) (Detection Rule License / CC BY 4.0) and the [TLCTC ATT&CK mapping](../mitre-attack-enterprise/) (CC BY 4.0).
