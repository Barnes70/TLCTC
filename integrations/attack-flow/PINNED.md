# Pinned upstream files

Upstream: [center-for-threat-informed-defense/attack-flow](https://github.com/center-for-threat-informed-defense/attack-flow) at commit `0bd4a2d45dceacce499d7e94b85f7966e70f5399` (main, 2026-08-13; Builder 4.0 in development). Licence Apache-2.0.

| File | Upstream path | sha256 |
|---|---|---|
| `pinned/attack-flow-schema-2.0.0.json` | `stix/attack-flow-schema-2.0.0.json` | `fff896f5e1bdc39d9b387c0d3571307037cf9be1059de9cd94d066d1da2997cc` |
| `pinned/attack-flow-extension-2.0.0.json` | `stix/attack-flow-extension-2.0.0.json` | `afdbac65edc9805ea2f3b2b84b4ae4908644e7f4190f28e8e836659d74d87e70` |
| `tests/fixtures/corpus/SolarWinds.afb` | `corpus/SolarWinds.afb` | `d88a2396e8da0a95a4a25d115d00d7553686e082f80341987a5f1bee9b31008d` |
| `tests/fixtures/corpus/Tesla Kubernetes Breach.afb` | `corpus/Tesla Kubernetes Breach.afb` | `0c725aeaff17e441a061b2228680bfedb8646edb0ad5157bcea721b767a772f5` |
| `tests/fixtures/corpus/Equifax Breach.afb` | `corpus/Equifax Breach.afb` | `85e7b4a9f008e2f917b19de1566628c511796f67eef37fc7b747c5cdd3ba487a` |

The full corpus (41 `.afb` files) is **not stored** here; `study/run-study.py` downloads it from the pinned commit into a cache and verifies every file against the hashes in `study/corpus-sha256.json`.

## Refreshing

1. Update the commit above, re-download the two schema files and the three fixtures, update the hashes.
2. Run `npm run validate-attack-flow` (pinned schema drift shows up in the example export check).
3. Re-run `python study/run-study.py` (it refreshes `study/corpus-sha256.json` for a new commit only with `--accept-new-corpus`) and commit the new results.
