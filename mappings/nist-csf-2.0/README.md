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
| `"all"` | Cluster-neutral: the outcome serves every cause (governance, asset base, analysis, response, recovery, consequence-side data protection) | One **shared Umbrella** control, linked into all ten rows of its function column |
| `"none"` | Outside the threat axis: no attacker cause (GV.RM-07 positive risks, PR.IR-02 environmental threats) | No cell |

Every entry carries a `kind` (`tech` / `org`) and a one-line `rationale` naming the generic vulnerability it addresses.

Current split: 32 cluster-specific (42 Local placements), 72 cluster-neutral, 2 outside the axis. By function, cluster-specific / neutral: GOVERN 10 / 20 (all ten are GV.SC → #10), IDENTIFY 5 / 16, PROTECT 13 / 8, DETECT 4 / 7, RESPOND 0 / 13, RECOVER 0 / 8. The CSF's response and recovery outcomes are cause-agnostic by design. That is the gap the threat axis fills.

## Files

| File | Role |
|---|---|
| [`csf2-tlctc-mapping.json`](csf2-tlctc-mapping.json) | Single source. Edit this (hand-formatted, one subcategory per line). |
| [`../../tools/control-matrix-starter-nist-csf2.json`](../../tools/control-matrix-starter-nist-csf2.json) | Generated Control Matrix starter |
| [`../../tools/data/csf2-tlctc.js`](../../tools/data/csf2-tlctc.js) | Generated `window.TLCTC_CSF2` for the tlctc.net CSF page |

`node scripts/build-csf2.js` (chained into `npm run validate`) validates the source (6 functions, 22 categories, 106 subcategories, ids, categories, cluster ids, kinds) and regenerates both outputs.
