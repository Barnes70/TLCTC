# CIS Controls v8.1.2 → TLCTC

The 153 Safeguards of the CIS Critical Security Controls v8.1.2 (March 2025), each placed on one of two TLCTC layers:

- **System-risk layer** — Safeguards that act on a cluster step, up to the System Risk Event. They go in the 10 × 6 control matrix (application paper §8.1): the cluster row(s) whose generic vulnerability they act on, in the column of their CIS security function.
- **Data-risk layer** — Safeguards that act after the System Risk Event, at the Data Risk Event. The cluster matrix does not hold them; they go in a separate matrix with one row per DRE leaf code (`C`, `Ii`, `If`, `Av`, `Ac`) and the same six function columns (owner ruling, 2026-10-01).

A `hardening` flag marks the Safeguards that set, restrict or verify configuration.

**Source and licence:** CIS Critical Security Controls® v8.1.2 © Center for Internet Security, Inc., licensed [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). **This mapping contains no CIS text.** It holds Safeguard ids, control numbers, asset classes, security functions and implementation groups (facts), and topics and rationales in TLCTC wording. Read the Safeguards in your own copy of the Controls: [cisecurity.org/controls/v8-1](https://www.cisecurity.org/controls/v8-1). v8.1.1 and v8.1.2 changed glossary definitions only; the Safeguards are those of v8.1.

**Status:** AI-assisted starter guidance; owner review pending. Not a CIS product.

## Why two matrices

Like most control standards, the CIS Controls mix two kinds of control without saying so. Application patching (7.4) stops a cluster step: an implementation flaw is no longer there to exploit. Disk encryption (3.6) stops nothing of the kind — the laptop is still stolen, the System Risk Event still happens. It acts one layer later, keeping that event from becoming a `[DRE: C]`. Placing it in a cluster row (or in every row) claims a cause-side effect it does not have. So it goes in the DRE matrix, row `C`, column PROTECT.

### The DRE matrix (data-risk layer, 18 Safeguards)

| DRE | GOVERN | IDENTIFY | PROTECT | DETECT | RESPOND | RECOVER |
|---|---|---|---|---|---|---|
| **C** confidentiality | 3.1 | 3.2, 3.7, 3.8 | 3.4, 3.5, 3.6, 3.9, 3.11, 3.13, 4.11, 11.3, 14.4 | 3.14 | — | — |
| **Ii** incorrect state | 3.1, 11.1 | 3.2, 3.7, 3.8 | 11.3 | — | — | 11.2, 11.4, 11.5 |
| **If** misattributed state | 3.1 | 3.2, 3.7, 3.8 | — | — | — | — |
| **Av** unavailable | 3.1, 11.1 | 3.2, 3.7, 3.8 | — | — | — | 11.2, 11.4, 11.5 |
| **Ac** inaccessible | 3.1, 11.1 | 3.2, 3.7, 3.8 | — | — | — | 11.2, 11.4, 11.5 |

3.1, 3.2, 3.7 and 3.8 are data-layer enablers (`"dre": "all"`). Two gaps show at once: **`If` has no Safeguard of its own** — nothing in the CIS Controls protects or verifies provenance and attribution — and **detection and response barely exist at the data layer**: one Safeguard detects a disclosure (3.14), none responds to a Data Risk Event. Transit encryption (3.10) is not here: it denies the man-in-the-middle step itself, so it stays on `#5`.

### The cluster matrix (system-risk layer, 135 Safeguards)

89 act on specific clusters (151 Local placements, 43 of them on more than one cluster), 45 are cluster-neutral (inventories, governance, logging, network reach, response and recovery processes) and one is outside the threat axis (14.5: accidental exposure without an attacker).

| Cluster | Local placements (GV·ID·PR / DE·RS·RC) | of which hardening |
|---|---|---|
| #1 Abuse of Functions | 22 / 6 | 17 |
| #2 Exploiting Server | 14 / 6 | 3 |
| #3 Exploiting Client | 15 / 5 | 5 |
| #4 Identity Theft | 24 / 3 | 16 |
| #5 Man in the Middle | 8 / 0 | 6 |
| #6 Flooding Attack | 3 / 1 | 1 |
| #7 Malware | 14 / 8 | 12 |
| #8 Physical Attack | 3 / 1 | 3 |
| #9 Social Engineering | 7 / 0 | 3 |
| #10 Supply Chain Attack | 10 / 1 | 0 |

No Safeguard is written for `#6`: "denial of service", "rate limiting", "capacity" and "bandwidth" appear nowhere in the 153 Safeguards, and only 12.2 asks for availability. Flooding coverage is incidental — four Safeguards act on finite capacity as a side effect: availability in the network architecture (12.2), intrusion prevention and application-layer filtering (13.8, 13.10), and intrusion detection (13.3). The cause-neutral network controls (segmentation, flow logs, host firewalls) reach the `#6` row only as Umbrella controls.

## Configuration is a cause-side surface

The TLCTC v2.6 dictionary defines the #1 generic vulnerability as *"The inherent trust, scope, and complexity designed into software functionality and configuration."* 58 of 153 Safeguards are hardening (48 PROTECT, 8 DETECT, 2 GOVERN): 42 sit in cluster rows (placements: #1 17 · #4 16 · #7 12 · #5 6 · #3 5 · #2 3 · #8 3 · #9 3 · #6 1 · #10 0), 11 are cluster-neutral system configuration (logging, firewalls, time sync) and 5 are data-layer configuration (encryption at rest, sensitive-data access logging, backup protection). Configuration's home is #1, with #4 second and #7 third; it barely touches #2/#3, whose implementation flaws are closed by patching (Control 7), not by settings. A misconfiguration with no attacker is a System Failure (operational risk, no cluster) and is never a mapping target. The same shape appears in the NIST CCE list; see [CCE Is Not the CWE of Configuration](https://www.tlctc.net/cce-is-not-the-cwe-of-configuration.html).

## Relation to the June 2026 mapping

[`cis-v81-mapping.html`](https://www.tlctc.net/cis-v81-mapping.html) (2026-06-06) published a cell-by-cell mapping of v8.1 (153 Safeguards → 74 cell-pure objectives; 48 enablers, 34 umbrellas). Its per-Safeguard data file was never published and could not be recovered, so this file is a **rebuild**: the 34 Safeguards that page names are kept as published, the rest follow the NIST CSF 2.0 mapping's precedents. Three differences are structural, not disagreements over single rows:

- **Two layers.** June placed data-layer protection in cluster rows (its `#8` prevention count of 8 is reproduced exactly when the five post-`#8` protections — 3.5, 3.6, 3.9, 3.11, 4.11 — are put there). Under the two-matrix ruling they move to the DRE matrix, so the cluster matrix here is smaller (135 Safeguards, 151 placements against June's 143 fragments).
- **The Bow-Tie side** is judged per Safeguard in June and proxied by the CIS security function here (GV·ID·PR / DE·RS·RC), which explains most of the smaller detection-response column (30 against 44).
- **`#6`:** no Safeguard is written for flooding; both mappings place Safeguards there by their effect on capacity (June 1 / 2, rebuild 3 / 1: 12.2, 13.8, 13.10 / 13.3).

| Cluster | June prevention / detection-response | Rebuild, cluster matrix |
|---|---|---|
| #1 | 12 / 8 | 22 / 6 |
| #2 | 19 / 7 | 14 / 6 |
| #3 | 9 / 4 | 15 / 5 |
| #4 | 17 / 4 | 24 / 3 |
| #5 | 5 / 2 | 8 / 0 |
| #6 | 1 / 2 | 3 / 1 |
| #7 | 12 / 11 | 14 / 8 |
| #8 | 8 / 1 | 3 / 1 |
| #9 | 9 / 2 | 7 / 0 |
| #10 | 7 / 3 | 10 / 1 |

## Fields

| Field | Meaning |
|---|---|
| `clusters` | System-risk layer. `["#4"]`, `["#1", "#7"]`, … = Local control in each named row of its function column; `"all"` = cluster-neutral, one shared Umbrella control in all ten rows; `"none"` = outside the threat axis, no cell. `null` on data-layer entries. |
| `dre` | Data-risk layer only. `["C"]`, `["Ii", "Av", "Ac"]`, … = DRE matrix rows; `"all"` = data-layer enabler in all five rows. |
| `function` | CIS security function, the matrix column (GV/ID/PR/DE/RS/RC). |
| `asset_class`, `ig` | CIS asset class and lowest implementation group. |
| `kind`, `hardening` | `tech`/`org`; configuration flag. |
| `topic`, `rationale` | TLCTC wording (topic ≤ 60 characters). |

## Files

| File | Role |
|---|---|
| [`cis-v8.1-tlctc-mapping.json`](cis-v8.1-tlctc-mapping.json) | Single source. Hand-formatted, one Safeguard per line, CRLF. Edit as text. |
| [`cis-v8.1-dre-matrix.json`](cis-v8.1-dre-matrix.json) | Generated DRE matrix (rows C·Ii·If·Av·Ac × six functions → Safeguard ids) |
| [`../../tools/control-matrix-starter-cis-v8.1.json`](../../tools/control-matrix-starter-cis-v8.1.json) | Generated Control Matrix starter (system-risk layer only) |
| [`tools/extract_skeleton.py`](tools/extract_skeleton.py) | Builds the factual skeleton from the CIS spreadsheet (ids are recovered by position: the release stores them as numbers, so 4.10 reads as 4.1) |
| [`tools/check_no_cis_text.py`](tools/check_no_cis_text.py) | Fails if a topic or rationale shares six consecutive words with CIS text |

```bash
python mappings/cis-controls-v8.1/tools/extract_skeleton.py <CIS xlsx> <out.json>     # only for a new CIS release
python mappings/cis-controls-v8.1/tools/check_no_cis_text.py <CIS xlsx> mappings/cis-controls-v8.1/cis-v8.1-tlctc-mapping.json
npm run build-cis        # validate + regenerate the starter and the DRE matrix; chained into npm run validate
npm run test-build-cis   # Node unit tests
npm run test-cis         # Python unit tests (extractor, checker)
```
