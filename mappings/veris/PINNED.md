# Pinned upstream files

The mapping, the classifier tests and the study are reproducible against these exact
upstream states. Nothing here is edited by hand.

| File | Source | Commit | sha256 | Licence |
|---|---|---|---|---|
| `pinned/verisc-enum.json` | [vz-risk/veris](https://github.com/vz-risk/veris) `verisc-enum.json` (VERIS 1.4.1 enumerations) | `45d9d7ace489b9b7bc4f1cee1daa4bf4872dfcaf` (master, 2026-06-12) | `8fff722d7efb8911a4437be608dca665b5fb5d29b4117cbeb2493892dcef700e` | CC BY-SA 4.0 (repository licence) |
| `pinned/verisc-labels.json` | vz-risk/veris `verisc-labels.json` (enumeration descriptions) | same | `8678e95d773e181bf5d8809f3dcef2dc0cce1252b68088e503e06766fafe2247` | CC BY-SA 4.0 |
| `pinned/veris-1.4.1_attack-19.1-enterprise.csv` | vz-risk/veris `mappings/veris-1.4.1_attack-19.1-enterprise.csv` (VERIS → ATT&CK, used only for the transitive consistency check) | same | `65dfd6022bb5fd6e1ae6ef18271effe53652b72179eacc7fbeb5190430ddbc42` | CC BY-SA 4.0 |
| VCDB joined dataset (**not stored** in this repository) | [vz-risk/VCDB](https://github.com/vz-risk/VCDB) `data/joined/vcdb.json.zip` (10,047 records; the web-skimmer batch is excluded by VCDB's own packaging) | `230cf22b56a481dd1a994b21e4d94c59e2bccea9` (master, 2026-08-04) | `e4be5dd432ccfad16520a6b60dd83e9d47c63b0f3352c26c4d43a5dd774c32c0` | CC BY-SA 4.0 |

Download URL used by `study/run-study.py`:
`https://raw.githubusercontent.com/vz-risk/VCDB/230cf22b56a481dd1a994b21e4d94c59e2bccea9/data/joined/vcdb.json.zip`

## Refreshing

1. Download the three VERIS files from the new commit into `pinned/` and update the commit and hashes above.
2. Run `npm run validate-veris`: it fails on every enumeration value that gained or lost an entry in `tlctc-veris.json`, and on every description that drifted.
3. Fix the mapping, bump `metadata.updated`, regenerate the CSV (`npm run build-veris`).
4. For a new VCDB snapshot, update the commit, URL and hash here, re-run `python study/run-study.py`, and commit the new `study/results.json`, `study/results.md` and figures.
