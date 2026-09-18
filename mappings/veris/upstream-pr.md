# Upstream pull request — owner runbook

One pull request to [vz-risk/veris](https://github.com/vz-risk/veris), opened by the project
owner from their own GitHub account. Nothing in this repository pushes to Verizon's repositories.

The contribution is the generated CSV `veris-1.4.1_tlctc-2.5.csv`, placed in the upstream
`mappings/` directory next to `veris-1.4.1_attack-19.1-enterprise.csv` and
`cis_csc_v8_veris_mapping_v1.csv`, plus one line in `mappings/readme.md`.

Before the PR: `npm run validate` must pass on the branch (it regenerates the CSV and checks it
byte for byte), and `study/results.json` must be current for the mapping's `updated` date.

## Licence

The VERIS repository is licensed CC BY-SA 4.0 (`LICENSE.txt`). The mapping is CC BY 4.0 in this
repository; CC BY 4.0 material may be offered under CC BY-SA 4.0, so the CSV is contributed
under CC BY-SA 4.0 with attribution to the TLCTC Project. Say so in the PR body (below).

## Steps

```bash
gh repo fork vz-risk/veris --clone
cd veris
git checkout -b tlctc-mapping
cp <tlctc-repo>/mappings/veris/veris-1.4.1_tlctc-2.5.csv mappings/
# append one line to mappings/readme.md (keep the existing line about Mappings Explorer):
cat >> mappings/readme.md <<'EOF'

`veris-1.4.1_tlctc-2.5.csv` maps every VERIS 1.4.1 action variety, vector, result and attribute value to the TLCTC (Top Level Cyber Threat Clusters) v2.5 cause-oriented threat clusters and Data Risk Event codes, with the classification rule per row. Source, classifier and a study over VCDB: https://github.com/Barnes70/TLCTC/tree/main/mappings/veris
EOF
git add mappings/veris-1.4.1_tlctc-2.5.csv mappings/readme.md
git commit -m "mappings: add VERIS 1.4.1 -> TLCTC v2.5 mapping"
git push -u origin tlctc-mapping
```

The VERIS repository has no CI gate for `mappings/` (its unit tests cover the schema tooling), so
there is nothing to run locally beyond checking that the CSV opens as UTF-8 with LF line endings.
On Windows, clone with `git -c core.autocrlf=false clone …` so the CSV keeps its LF bytes; the
Git Bash notes in `integrations/misp/upstream-pr.md` apply if any shell helper is needed.

**STOP here.** The pull request itself is the owner's:

```bash
gh pr create --title "Add VERIS 1.4.1 → TLCTC v2.5 mapping (cause-oriented threat clusters)" --body-file <(cat <<'BODY'
This adds `mappings/veris-1.4.1_tlctc-2.5.csv`: a crosswalk from VERIS 1.4.1 to TLCTC (Top Level Cyber Threat Clusters) v2.5, in the same column layout as the VERIS → ATT&CK file in this directory (Mappings Explorer shape; the three ATT&CK object columns are renamed `tlctc_object_id`, `tlctc_object_name`, `tlctc_version`).

TLCTC is a cause-oriented cyber threat taxonomy: ten non-overlapping clusters, each defined by the generic vulnerability an attack step exploits, with outcomes recorded separately as Data Risk Events and incidents expressed as ordered sequences of cluster steps. Its rules make the companion steps explicit that VERIS records implicitly: malware needs a delivering step before it, credential use needs an acquisition step, social engineering needs a technical follow-on.

What the file contains (346 rows, 337 VERIS values, total coverage of `action.*.variety`, `action.*.vector`, `action.*.result`, `attribute.confidentiality.data_disclosure`, `attribute.integrity.variety`, `attribute.availability.variety`):
- `mapping_type` says what the VERIS value can establish: `direct` (one cluster), `conditional` (one row per alternative with the deciding rule and condition in `comments`, e.g. `Exploit vuln` → #2 | #3 by component role), `chain` (one cluster plus the companion step the rules require), `context` (vectors: boundary context, no cluster), `no-cluster` (errors, environmental events and in-grant misuse: operational risk, off the threat axis), `outcome` (attribute values → Data Risk Event codes C, Ii/If, Av/Ac; results → nothing), `unresolved` (Other/Unknown).
- `comments` carries the rule applied and a one-sentence rationale for every row; `references` links the framework.

A standard-library Python classifier that applies the mapping to VERIS/VCDB records, and a study that runs it over the 10,047 records of the VCDB joined dataset (snapshot 2026-08-04) with an ATT&CK-transitive consistency check, are at https://github.com/Barnes70/TLCTC/tree/main/mappings/veris. The study report: https://github.com/Barnes70/TLCTC/blob/main/documentation/tlctc-veris-vcdb-study.md

Licence: the CSV is contributed under CC BY-SA 4.0 (the repository licence), attribution "TLCTC Project"; the source mapping is CC BY 4.0.
References: https://www.tlctc.net · https://github.com/Barnes70/TLCTC · https://doi.org/10.5281/zenodo.20633176
BODY
)
```

## After the PR

- If the maintainers ask for changes to the CSV, make them in `tlctc-veris.json` here, run
  `npm run build-veris && npm run validate-veris`, re-run `python study/run-study.py` if any
  cluster target changed, copy the regenerated CSV into the fork branch, commit and push; the PR
  updates itself.
- If they ask for a different column layout, change `scripts/build-veris-mapping.js` (the CSV is
  never edited by hand).
- A VERIS 1.4.2 or 1.5 refresh follows `PINNED.md`; the CSV file name carries both versions.
