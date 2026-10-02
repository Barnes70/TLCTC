# NIST CSF 2.0 Core → TLCTC

The 106 subcategories of the NIST Cybersecurity Framework 2.0 Core, each placed on the TLCTC threat axis: which of the ten cluster rows of the CSF × TLCTC control matrix (application paper §8.1) the outcome addresses.

**Source:** *The NIST Cybersecurity Framework (CSF) 2.0*, NIST CSWP 29, 26 February 2024, Appendix A — [doi.org/10.6028/NIST.CSWP.29](https://doi.org/10.6028/NIST.CSWP.29). Function, category and subcategory text is verbatim (a U.S. Government work).

**Status:** AI-assisted starter guidance, pending owner review. Not a NIST product, and not an official crosswalk.

## Outcomes, not controls

CSF subcategories are outcomes. The CSF "does not prescribe how outcomes should be achieved". Each one sits in its own function column; the mapping only decides the row.

## The `clusters` field

| Value | Meaning | In the matrix |
|---|---|---|
| `["#4"]`, `["#2", "#3"]`, … | The outcome addresses the generic vulnerability of those clusters | **Local** control in each named row of its function column |
| `"all"` | Cluster-neutral: the outcome serves every cause (governance, asset base, analysis, response, recovery) | One **shared Umbrella** control, linked into all ten rows of its function column |
| `"none"` | Outside the threat axis: no attacker cause (GV.RM-07 positive risks, PR.IR-02 environmental threats) | No cell |
| `null` + `dre` | Data-risk layer: the outcome acts after the System Risk Event, at the Data Risk Event (`dre`: `C`, `Ii`, `If`, `Av`, `Ac` or `"all"`) | Not in the cluster matrix: the separate [DRE Control Matrix](../../tools/dre-matrix.html) |

Every entry carries a `kind` (`tech` / `org`) and a one-line `rationale` naming the generic vulnerability it addresses.

Current split: 32 cluster-specific (42 Local placements), 67 cluster-neutral, 2 outside the axis, 5 on the data-risk layer. By function, cluster-specific / neutral / data layer: GOVERN 10 / 20 / 0 (all ten cluster-specific ones are GV.SC → #10), IDENTIFY 5 / 15 / 1, PROTECT 13 / 5 / 3, DETECT 4 / 7 / 0, RESPOND 0 / 13 / 0, RECOVER 0 / 7 / 1. The CSF's response and recovery outcomes are cause-agnostic by design. That is the gap the threat axis fills.

## Two layers

The cluster matrix is the system-risk layer: it holds outcomes that act on a cluster step, up to the System Risk Event. Five outcomes act one layer later, at the Data Risk Event, and go to the separate DRE matrix instead (owner ruling, 2026-10-01; the same rule as the [CIS Controls mapping](../cis-controls-v8.1/)): PR.DS-01 data-at-rest and PR.DS-10 data-in-use protection (every DRE row: the CSF names confidentiality, integrity and availability), PR.DS-11 backups and RC.RP-03 backup verification (`Ii`, `Av`, `Ac`), and ID.AM-07 data inventories (enabler for every row). PR.DS-02 (data in transit) stays on `#5`: it denies the man-in-the-middle step itself. RC.RP-05 restores systems, not data, and stays cluster-neutral. As with the CIS Controls, no CSF outcome detects or responds at the data layer, and misattribution (`If`) is covered only by the two broad data-protection outcomes.

## Files

| File | Role |
|---|---|
| [`csf2-tlctc-mapping.json`](csf2-tlctc-mapping.json) | Single source. Edit this (hand-formatted, one subcategory per line). |
| [`../../tools/control-matrix-starter-nist-csf2.json`](../../tools/control-matrix-starter-nist-csf2.json) | Generated Control Matrix starter |
| [`../../tools/data/csf2-tlctc.js`](../../tools/data/csf2-tlctc.js) | Generated `window.TLCTC_CSF2` for the tlctc.net CSF page |
| [`../../tools/dre-matrix-starter-nist-csf2.json`](../../tools/dre-matrix-starter-nist-csf2.json) | Generated DRE Matrix starter (the five data-layer outcomes) |

`node scripts/build-csf2.js` (chained into `npm run validate`) validates the source (6 functions, 22 categories, 106 subcategories, ids, categories, cluster ids, kinds) and regenerates all three outputs.
