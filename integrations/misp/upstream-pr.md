# Upstream pull requests — owner runbook

Two pull requests, opened by the project owner from their own GitHub account.
Nothing in this repository pushes to MISP repositories.

Before either PR: `npm run validate` must pass on `main` and the taxonomy
`version` in `machinetag.json` must be the value the PR introduces (1 for the
first submission; bump on every later change).

## 1. MISP/misp-taxonomies

```bash
gh repo fork MISP/misp-taxonomies --clone
cd misp-taxonomies
git checkout -b tlctc
mkdir tlctc
cp <tlctc-repo>/integrations/misp/taxonomies/tlctc/machinetag.json tlctc/
sudo apt install jq moreutils python3-jsonschema     # sponge comes from moreutils
./jq_all_the_things.sh                               # must produce NO diff in tlctc/machinetag.json
python3 validate_all.py                              # schema check of every taxonomy
python3 gen_uuid.py                                  # must be a no-op for tlctc (uuids already match its scheme)
(cd tools && python3 gen_manifest.py)                # regenerates MANIFEST.json — commit it
./validate_all.sh                                    # the CI gate; expects a clean tree afterwards
git add tlctc/machinetag.json MANIFEST.json
git commit -m "add: tlctc — TLCTC (Top Level Cyber Threat Clusters) v2.5 cause-oriented threat taxonomy"
git push -u origin tlctc
gh pr create --title "Add tlctc taxonomy (Top Level Cyber Threat Clusters v2.5)" --body-file <(cat <<'BODY'
This adds the `tlctc` taxonomy: TLCTC (Top Level Cyber Threat Clusters) v2.5, a cause-oriented cyber threat taxonomy with exactly ten non-overlapping clusters, each defined by the generic vulnerability exploited rather than by the outcome.

Two predicates:
- `cluster` (non-exclusive): every cluster whose generic vulnerability was exploited at some step of the attack path.
- `entry-cluster` (exclusive): the cluster of the first step.

Ten values under each (`01-abuse-of-functions` … `10-supply-chain-attack`), with `numerical_value`, colours and descriptions taken verbatim from the framework dictionary. UUIDs follow this repository's `gen_uuid.py` scheme.

Companion object templates (`tlctc-attack-path`, `tlctc-attack-step`) are proposed in MISP/misp-objects.

Licence: the contributed JSON is released under CC0 1.0.
References: https://www.tlctc.net · https://github.com/Barnes70/TLCTC · https://doi.org/10.5281/zenodo.20633176
BODY
)
```

## 2. MISP/misp-objects

```bash
gh repo fork MISP/misp-objects --clone
cd misp-objects
git checkout -b tlctc-objects
cp -r <tlctc-repo>/integrations/misp/objects/tlctc-attack-path objects/
cp -r <tlctc-repo>/integrations/misp/objects/tlctc-attack-step objects/
./jq_all_the_things.sh                               # jq -S -j; must produce NO diff in the two definition.json files
find objects/tlctc-* -name "*.json" -exec chmod -x {} \;
./validate_all.sh                                    # schema, opposites, unique uuids — the CI gate
git add objects/tlctc-attack-path objects/tlctc-attack-step
git commit -m "add: tlctc-attack-path and tlctc-attack-step objects (TLCTC v2.5)"
git push -u origin tlctc-objects
gh pr create --title "Add tlctc-attack-path and tlctc-attack-step object templates" --body-file <(cat <<'BODY'
Two object templates for TLCTC (Top Level Cyber Threat Clusters) v2.5 attack paths, the companion to the `tlctc` taxonomy proposed in MISP/misp-taxonomies.

- `tlctc-attack-path` (meta-category misc): one per incident — full notation string, incident id, entry cluster, analyst confidence, Data Risk Events, source links, and the Layer 3 source JSON as an attachment. References each step with `includes`.
- `tlctc-attack-step` (meta-category misc): one per step — exactly one cause cluster (or `status=unresolved` for forensically open steps), foreign-code execution flag, attack velocity to the next step, responsibility-sphere boundary crossing (source, target, transit carriers), intra-system boundaries, Data Risk Events, evidence. Steps reference their successor with `followed-by`; the reference comment carries the Δt so the event graph shows attack velocity.

Both use existing relationships (`includes`, `followed-by`) and existing attribute types only. A converter that emits events with these templates from TLCTC Layer 3 JSON lives at https://github.com/Barnes70/TLCTC/tree/main/integrations/misp (example event included).

Licence: the contributed JSON is released under CC0 1.0.
References: https://www.tlctc.net · https://github.com/Barnes70/TLCTC · https://doi.org/10.5281/zenodo.20633176
BODY
)
```

## Running the upstream checks on Windows (Git Bash)

The two `validate_all.sh` scripts assume a Linux box. What made them run here
(set up 2026-09-16; the shims live in `~/bin`, which Git Bash puts on PATH):

- `jq` installed via `winget install jqlang.jq`; the `~/bin/jq` shim adds `-b`
  (binary) because the native jq.exe otherwise writes CRLF.
- `~/bin/sponge`, `~/bin/uuidparse`, `~/bin/jsonschema`, `~/bin/pytaxonomies`:
  small bash shims standing in for moreutils, util-linux and the two Python CLIs
  (`pip install jsonschema pytaxonomies`).
- Run every Python helper with `PYTHONUTF8=1` exported. Without it Python opens
  the taxonomy files as cp1252 and `validate_all.py`, `gen_uuid.py` and
  `unique_uuid.py` crash (and `gen_uuid.py` half-rewrites the tree before it does).
- `gen_uuid.py` also rewrites ~30 upstream taxonomies whose uuids do not follow
  its scheme. That is upstream drift, not ours: check that `tlctc/machinetag.json`
  is byte-identical afterwards, then `git checkout -- .` the rest.
- `tools/gen_manifest.py` sorts paths case-insensitively on Windows and writes
  CRLF. Regenerate MANIFEST.json with a byte-order sort
  (`sorted(..., key=lambda p: p.parent.name)`) and pipe it through
  `jq . | sponge` so the diff is only the new entry and the version date.
  After `validate_all.sh` the tree is dirty on Windows for the same two reasons;
  `git diff --ignore-cr-at-eol --stat` plus an order check is the real signal.
- misp-taxonomies CI additionally runs `pytaxonomies -l MANIFEST.json -a`.

## After merge

- Note the upstream merge commits in this file.
- When a cluster string changes in a future dictionary version: regenerate
  (`npm run build-misp`), bump `TAXONOMY_VERSION` in `scripts/build-misp-taxonomy.js`,
  and open a follow-up PR. UUIDs do not change (they hash the value slugs, not the text).
- When an object template changes: bump its `version` and open a follow-up PR;
  the template `uuid` never changes.
