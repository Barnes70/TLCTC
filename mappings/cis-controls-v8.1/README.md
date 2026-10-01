# CIS Controls v8.1.2 → TLCTC

The 153 Safeguards of the CIS Critical Security Controls v8.1.2 (March 2025), each placed on the TLCTC threat axis: which of the ten cluster rows of the control matrix (application paper §8.1) the Safeguard acts on, in the column of its CIS security function. A `hardening` flag marks the Safeguards that set, restrict or verify configuration.

**Source and licence:** CIS Critical Security Controls® v8.1.2 © Center for Internet Security, Inc., licensed [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). **This mapping contains no CIS text.** It holds Safeguard ids, control numbers, asset classes, security functions and implementation groups (facts), and topics and rationales in TLCTC wording. Read the Safeguards in your own copy of the Controls: [cisecurity.org/controls/v8-1](https://www.cisecurity.org/controls/v8-1). v8.1.1 and v8.1.2 changed glossary definitions only; the Safeguards are those of v8.1.

**Status:** AI-assisted starter guidance; owner review pending. Not a CIS product.

## Relation to the June 2026 mapping

[`cis-v81-mapping.html`](https://www.tlctc.net/cis-v81-mapping.html) (2026-06-06) published a cell-by-cell mapping of v8.1 (153 Safeguards → 74 cell-pure objectives; 48 enablers, 34 umbrellas). Its per-Safeguard data file was never published and could not be recovered, so this file is a **rebuild**: the 34 Safeguards that page names are kept as published; the rest follow the NIST CSF 2.0 mapping's precedents. The rebuild does not reproduce the published counts:

| Measure | June 2026 | Rebuild |
|---|---|---|
| Cause-acting Safeguards | 105 | 88 |
| Enablers / cluster-neutral | 48 | 65 (64 `"all"`, 1 `"none"`) |
| Multi-cluster (umbrella) Safeguards | 34 | 42 |
| Cluster placements, total | 143 fragments | 146 |

| Cluster | June prevention / detection-response | Rebuild (by CIS function: GV·ID·PR / DE·RS·RC) |
|---|---|---|
| #1 | 12 / 8 | 21 / 6 |
| #2 | 19 / 7 | 14 / 6 |
| #3 | 9 / 4 | 15 / 5 |
| #4 | 17 / 4 | 24 / 3 |
| #5 | 5 / 2 | 8 / 0 |
| #6 | 1 / 2 | 0 / 0 |
| #7 | 12 / 11 | 14 / 8 |
| #8 | 8 / 1 | 3 / 1 |
| #9 | 9 / 2 | 7 / 0 |
| #10 | 7 / 3 | 10 / 1 |

Most of the gap comes from two doctrine choices: consequence-side protection (device encryption, remote wipe) placed on the cluster whose step it follows (June, e.g. #8) or on every row (`"all"`, CSF PR.DS-01 precedent, rebuild); and the Bow-Tie side judged per Safeguard (June) or proxied by the CIS security function (rebuild). Owner decision pending.

## Configuration is a cause-side surface

The TLCTC v2.6 dictionary defines the #1 generic vulnerability as *"The inherent trust, scope, and complexity designed into software functionality and configuration."* The `hardening` flag (`true` = the Safeguard sets, restricts or verifies the configuration state of an asset or software) shows where configuration work lands:

| | Safeguards |
|---|---|
| Hardening, total | **58 of 153** (48 PROTECT, 8 DETECT, 2 GOVERN) |
| … cluster-neutral (logging, encryption at rest, firewalls) | 16 |
| … in cluster rows (placements) | #1 17 · #4 16 · #7 12 · #5 6 · #3 5 · #2 3 · #8 3 · #9 3 · #10 0 · #6 0 |

Configuration's home is #1, with #4 second and #7 third; it barely touches #2/#3, whose implementation flaws are closed by patching (Control 7), not by settings. A misconfiguration with no attacker is a System Failure (operational risk, no cluster) and is never a mapping target. The same shape appears in the NIST CCE list; see [CCE Is Not the CWE of Configuration](https://www.tlctc.net/cce-is-not-the-cwe-of-configuration.html).

## The `clusters` field

| Value | Meaning | In the matrix |
|---|---|---|
| `["#4"]`, `["#1", "#7"]`, … | The Safeguard acts on the generic vulnerability of those clusters | **Local** control in each named row of its function column |
| `"all"` | Cluster-neutral: inventories, governance, logging, consequence-side data protection, response and recovery | One **shared Umbrella** control, linked into all ten rows of its function column |
| `"none"` | Outside the threat axis (14.5: accidental exposure without an attacker) | No cell |

Every entry also carries `asset_class`, `function` (GV/ID/PR/DE/RS/RC), `ig` (lowest implementation group), `kind` (`tech`/`org`), `hardening`, a TLCTC `topic` (≤ 60 characters) and a one-line `rationale`.

## Files

| File | Role |
|---|---|
| [`cis-v8.1-tlctc-mapping.json`](cis-v8.1-tlctc-mapping.json) | Single source. Hand-formatted, one Safeguard per line, CRLF. Edit as text. |
| [`tools/extract_skeleton.py`](tools/extract_skeleton.py) | Builds the factual skeleton from the CIS spreadsheet (ids are recovered by position: the release stores them as numbers, so 4.10 reads as 4.1) |
| [`tools/check_no_cis_text.py`](tools/check_no_cis_text.py) | Fails if a topic or rationale shares six consecutive words with CIS text |
| [`../../tools/control-matrix-starter-cis-v8.1.json`](../../tools/control-matrix-starter-cis-v8.1.json) | Generated Control Matrix starter |

```bash
python mappings/cis-controls-v8.1/tools/extract_skeleton.py <CIS xlsx> <out.json>     # only for a new CIS release
python mappings/cis-controls-v8.1/tools/check_no_cis_text.py <CIS xlsx> mappings/cis-controls-v8.1/cis-v8.1-tlctc-mapping.json
npm run build-cis        # validate (153 Safeguards, 18 Controls, fields) + regenerate the starter; chained into npm run validate
npm run test-build-cis   # Node unit tests
npm run test-cis         # Python unit tests (extractor, checker)
```
