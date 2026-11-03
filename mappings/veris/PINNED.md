# Pinned upstream files

The mapping, the classifier tests and the study are reproducible against these exact
upstream states. Nothing here is edited by hand.

| File | Source | Commit | sha256 | Licence |
|---|---|---|---|---|
| `pinned/verisc-enum.json` | [vz-risk/veris](https://github.com/vz-risk/veris) `verisc-enum.json` (VERIS 1.4.2 enumerations) | `dba30b035039f3d002c6eb06dc149dbed7476059` (master, 2026-10-14) | `6f227ee1dfa2b9f2ec56407510d702cf61271a8ad6f0ff06115eae4e0a54b3e6` | CC BY-SA 4.0 (repository licence) |
| `pinned/verisc-labels.json` | vz-risk/veris `verisc-labels.json` (enumeration descriptions) | same | `2ee3adb91c28133f5be2dc8d57106302a9f4d1d235df73e9dfeb4b4c57337eb8` | CC BY-SA 4.0 |
| `pinned/veris-1.4.1_attack-19.1-enterprise.csv` | vz-risk/veris `mappings/veris-1.4.1_attack-19.1-enterprise.csv` (VERIS → ATT&CK, used only for the transitive consistency check; unchanged in 1.4.2) | `45d9d7a` (2026-06-12), identical at `dba30b0` | `65dfd6022bb5fd6e1ae6ef18271effe53652b72179eacc7fbeb5190430ddbc42` | CC BY-SA 4.0 |
| VCDB joined dataset (**not stored** in this repository) | [vz-risk/VCDB](https://github.com/vz-risk/VCDB) `data/joined/vcdb.json.zip` (10,047 records; the web-skimmer batch is excluded by VCDB's own packaging) | `230cf22b56a481dd1a994b21e4d94c59e2bccea9` (master, 2026-08-04) | `e4be5dd432ccfad16520a6b60dd83e9d47c63b0f3352c26c4d43a5dd774c32c0` | CC BY-SA 4.0 |

Download URL used by `study/run-study.py`:
`https://raw.githubusercontent.com/vz-risk/VCDB/230cf22b56a481dd1a994b21e4d94c59e2bccea9/data/joined/vcdb.json.zip`

## Refreshing

1. Download the three VERIS files from the new commit into `pinned/` and update the commit and hashes above.
2. Run `npm run validate-veris`: it fails on every enumeration value that gained or lost an entry in `tlctc-veris.json`, and on every description that drifted.
3. Fix the mapping, bump `metadata.updated`, regenerate the CSV (`npm run build-veris`).
4. For a new VCDB snapshot, update the commit, URL and hash here, re-run `python study/run-study.py`, and commit the new `study/results.json`, `study/results.md` and figures.
