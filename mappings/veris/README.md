# VERIS → TLCTC Mapping

Maps every enumeration value of **VERIS 1.4.1** (Verizon's Vocabulary for Event Recording
and Incident Sharing) that can say something about cause or outcome to **TLCTC v2.6**: the
cluster whose generic vulnerability the action exploits, the rule that decides where VERIS
cannot, the companion step the rules require but VERIS does not record, the boundary context
a vector implies, the cause-side partition row for actions that are not threats, and the Data
Risk Event code for outcomes. A stdlib classifier applies it to VERIS / VCDB records, and a
reproducible study runs it over the whole VERIS Community Database.

| Piece | Path | Notes |
|---|---|---|
| Canonical mapping | `tlctc-veris.json` | 337 entries, hand-authored, one rationale each |
| Upstream deliverable | `veris-1.4.1_tlctc-2.6.csv` | **generated** by `scripts/build-veris-mapping.js`; the shape of the VERIS → ATT&CK file in [vz-risk/veris `mappings/`](https://github.com/vz-risk/veris/tree/master/mappings) |
| How a value is classified | `decision-tree.md` | the walk-through |
| Classifier | `cli/` | Python 3.10+, standard library only |
| Study | `study/run-study.py`, `study/results.{json,md}` | 10,047 VCDB records, aggregates committed, no records stored |
| Report | `../../documentation/tlctc-veris-vcdb-study.md` | paper-style write-up of the study |
| Pinned upstream files | `pinned/`, `PINNED.md` | VERIS enumerations, labels, ATT&CK mapping; VCDB snapshot hash |
| Owner runbook | `upstream-pr.md` | the pull request to vz-risk/veris |

Cluster names in the CSV come from the v2.6 dictionary at generation time
(`json-schemas/layer-1/tlctc-framework.v2.6.json`); `npm run validate-veris` fails on any drift
between the mapping, the dictionary and the pinned VERIS files.

## What a VERIS value can say: the seven mapping types

| `mapping_type` | Entries | Example |
|---|---|---|
| `direct` — one generic vulnerability, one cluster | 49 | `action.hacking.variety.SQLi` → #2 (R-ROLE, server role) |
| `conditional` — several clusters, a named rule decides | 8 | `action.hacking.variety.Exploit vuln` → #2 \| #3 (R-ROLE); `DoS` → #6 \| #2 \| #3 (R-SPECIFIC, capacity); `Backdoor` → #1 \| #7 (R-EXEC) |
| `chain` — one cluster plus a companion step VERIS does not record | 51 | `Use of stolen creds` → `<acquisition> → #4` (R-CRED); every malware variety → `<enabler> → #7` (R-EXEC); every social variety → `#9 → <follow-on>`; `RFI` → `#2 → #7` |
| `context` — vectors: no cluster, an annotation | 65 | `action.malware.vector.Software update` → `[update]` context, R-SUPPLY; `Partner` → `@Vendor→@Org` crossing |
| `no-cluster` — off the threat axis, partition row named | 58 | `action.error.variety.Misdelivery` → error_in_use (Axiom V); `Privilege abuse` → abuse_of_rights (R-SCOPE); `Extortion` → no IT-system step |
| `outcome` — not a cause (Axiom III) | 87 | `attribute.availability.variety.Obscuration` → DRE `Ac`; `Loss` → `Av`; action results → nothing |
| `unresolved` — `Other` / `Unknown` in a threat-bearing category | 19 | `action.hacking.variety.Unknown` → `?` in notation, excluded from statistics (R-UNRES-3) |

The rules that follow from the framework and shape the table:

- **Ransomware is #7 at execution, the encryption is `Ac`.** `malware.variety.Ransomware` is a
  chain entry (#7 with its enabler before it); the encryption is recorded through
  `attribute.availability.variety.Obscuration` → `Ac`, never as a cluster (Axiom III).
- **Credentials are two steps.** `Use of stolen creds`, `Pass-the-hash`, `Session replay`,
  `Offline cracking` are #4 with an acquisition step before them (R-CRED, Axiom X). `Brute force`
  is #4 on its own: guessing is application.
- **Exploit vuln needs R-ROLE.** VERIS does not record whether the flawed component served the
  attacker or consumed attacker content, so the parent value is conditional; the named children
  are attacks on the victim's service (#2), aligned with the repository's CWE mapping: XSS is
  #2 | #3 by where the encoding flaw sits, CSRF, open-redirect abuse, forced browsing and cache
  poisoning abuse designed functions (#1), session fixation and prediction are #4, entity
  expansion is #6, and RFI and insecure deserialisation are #2 followed by #7.
- **Errors and environmental events carry no cluster.** They sit on the Error in Use or Failure
  row of the cause-side partition (Axiom V, Axiom II).
- **Misuse is Abuse of Rights.** VERIS defines misuse as entrusted resources used contrary to
  their purpose: an entitled actor acting against the grant, which is the dictionary's own
  Abuse of Rights example. Every misuse variety sits on that row with no cluster and no SRE
  (R-SCOPE), except `Password or Session Sharing`, where the borrower authenticates as someone
  else (#4). An insider reaching past the envelope is #1, but VERIS would code that as hacking.
- **Vectors are not clusters.** `Partner` marks a sphere crossing that is #10 only at a Trust
  Acceptance Event (R-SUPPLY), otherwise transit; the mail and phone vectors mark the `[human]`
  context of a #9 step.
- **No attack path is emitted.** VERIS records an unordered set of actions; the classifier
  reports certain clusters, rule-dependent groups and lost companions, and labels any order as
  the hypothesis the companion rules imply.

## The CSV

Same columns as `veris-1.4.1_attack-19.1-enterprise.csv` upstream, with the three ATT&CK object
columns renamed for the target framework:

```
,mapping_framework,mapping_framework_version,capability_group,capability_id,capability_description,
mapping_type,tlctc_object_id,tlctc_object_name,tlctc_version,technology_domain,score_category,
score_value,related_score,references,comments,organization,creation_date,last_update
```

One row per (VERIS value, target): a conditional value has one row per alternative with the
condition in `comments`; a chain value carries its companion in `comments`; values with no
cluster have `tlctc_object_id = none` and the reason in `tlctc_object_name`. 346 rows, LF, no BOM.

## Classifier

```bash
cd mappings/veris
python -m cli classify tests/fixtures/vcdb/0012CC25-9167-40D8-8FE3-3D0DFD8FB6BB.json          # one record → JSON
python -m cli classify tests/fixtures/vcdb --format md                                          # a directory → table
python -m cli classify /path/to/vcdb_1-of-1.json --summary --attack-check --format md           # the joined file → the study tables
```

Per record: `clusters.certain`, `clusters.one_of` (rule-dependent groups), `clusters_upper`,
`chains` (with `missing` = `before`/`after` when the companion is absent), `partition_rows`,
`off_axis_only`, `dre`, `dre_potential`, `context`, `unresolved`, `unmapped`. `--summary`
aggregates into the study's tables; `--attack-check` adds the VERIS → ATT&CK → TLCTC comparison.
Exit codes: 0, 1 usage, 2 unreadable input (the message names the file).

## Study

```bash
python study/run-study.py            # downloads the pinned VCDB zip (sha256 verified), writes study/results.{json,md} and 3 SVG figures
```

Every cell in `results.json` is `{n, denominator}`; strata by incident year and by
`plus.sub_source` (the VCDB README marks `phidbr` and `priority` as non-random). The report in
`documentation/tlctc-veris-vcdb-study.md` reads only from `results.json`.

## Tests and validation

```bash
npm run build-veris && npm run validate-veris     # CSV bytes, coverage of the pinned enum, rule/axiom/DRE ids, results.json consistency
npm run test-veris                                # 39 unittest cases: mapping, classifier, summary, CLI, ATT&CK check, 20 VCDB golden records
```

## Licences

The mapping, the classifier, the study outputs and the report are CC BY 4.0 like the rest of
this repository. The three pinned VERIS files and the twenty VCDB fixture records under
`tests/fixtures/vcdb/` are CC BY-SA 4.0 (Verizon) and carry their own notice.

## Deliberately not included

- No **Layer 3 output** from VERIS records: an unordered record cannot be turned into an ordered path without inventing evidence.
- No **VCDB incident encodings** and no **VCDB schema change** (`plus.tlctc`): separate rounds.
- No mapping of **actor**, **asset**, **victim** or **discovery** enumerations: actors are metadata (Axiom IV), assets are topology, neither classifies.
- No comment on vz-risk/veris issue #127 ("Add Sequencing to VERIS"): the study is the evidence; the owner decides where to cite it.
