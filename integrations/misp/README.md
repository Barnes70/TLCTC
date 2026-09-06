# TLCTC for MISP

Brings TLCTC v2.5 into MISP as three pieces that work together:

| Piece | Path | Upstream target |
|---|---|---|
| Taxonomy `tlctc` | `taxonomies/tlctc/machinetag.json` (generated) | [MISP/misp-taxonomies](https://github.com/MISP/misp-taxonomies) |
| Object templates `tlctc-attack-path`, `tlctc-attack-step` | `objects/*/definition.json` | [MISP/misp-objects](https://github.com/MISP/misp-objects) |
| Converter Layer 3 → MISP event | `cli/` (Python 3.10+, stdlib only) | this repository |

The taxonomy is the index (two tags per event answer "which causes, and which
first?"); the objects carry the content — the ordered path with attack velocity,
boundary crossings, Data Risk Events and unresolved steps — so a MISP event
graph shows the attack path itself. The converter turns any file in
`attack-paths/` into an importable event that uses both.

Cluster definitions and generic vulnerabilities in the taxonomy are copied
verbatim from the v2.5 dictionary (`json-schemas/layer-1/tlctc-framework.v2.5.json`);
`npm run validate-misp` fails on any drift.

## Tags

```
tlctc:cluster="07-malware"                  one per distinct cluster observed (not exclusive)
tlctc:entry-cluster="09-social-engineering" the cluster of the first step (exclusive, at most one)
```

Values are `01-abuse-of-functions` … `10-supply-chain-attack`. Colours follow
the TLCTC tool palette; the three bridge clusters (#8, #9, #10) share amber.

Tagging rules that follow from the framework:

- **Credentials.** A stolen-credential intrusion carries the acquiring cluster
  *and* `04-identity-theft`: acquisition maps to the enabling cluster,
  application is always #4 (Axiom X, R-CRED). They are separate steps.
- **Ransomware is not a tag.** The payload execution is `07-malware`; the
  encryption is recorded as Data Risk Event `Ac` (present but unusable) on the
  step objects, never as a cluster (Axiom III).
- **Unresolved steps** (`?`, `…`) carry no cluster tag and no DRE (R-UNRES-2,
  R-UNRES-5). They are step objects with `status=unresolved`.
- **Boundary operators are not taxonomy content.** `||[human][@External→@Org]||`
  lives on the step object (`boundary-context/-source/-target/-transit`), not in a tag.
- **No cluster for Abuse of Rights.** An intended in-grant action is operational
  risk (R-SCOPE): it produces no `tlctc:` tag; record the DRE only.

## Objects

`tlctc-attack-path` (one per event, `required: notation`): `notation`,
`incident-id`, `tlctc-version`, `framework-ref`, `entry-cluster`,
`analyst-confidence`, `data-risk-event` (multiple), `reference` (link, multiple),
`notes`, `layer3-json` (attachment: the source Layer 3 file).

`tlctc-attack-step` (one per step, `required: step-id`): `step-id`, `status`,
`cluster`, `unresolved-type`, `candidates`, `fec-executed`, `delta-t-to-next`,
`boundary-context`, `boundary-source`, `boundary-target`, `boundary-transit`,
`intra-system-boundary`, `data-risk-event`, `evidence`, `notes`.

References: the path object `includes` every step; each step is `followed-by`
its successor, and the reference comment carries `Δt=<delta_t_to_next>` so the
event graph labels the edge with the attack velocity. A parallel group fans out:
the predecessor references every member, every member references the successor.
Each step's `cluster` attribute additionally carries its `tlctc:cluster` tag.

## Install in a private MISP instance

Taxonomy:

```bash
sudo -u www-data mkdir -p /var/www/MISP/app/files/taxonomies/tlctc
sudo -u www-data cp taxonomies/tlctc/machinetag.json /var/www/MISP/app/files/taxonomies/tlctc/
# MISP UI: Event Actions → List Taxonomies → Update Taxonomies → enable "tlctc" → enable all tags
```

Object templates:

```bash
sudo -u www-data cp -r objects/tlctc-attack-path objects/tlctc-attack-step /var/www/MISP/app/files/misp-objects/objects/
# MISP UI: Event Actions → List Object Templates → Update Objects
```

Once the upstream pull requests are merged (see `upstream-pr.md`), both arrive
with the regular `misp-taxonomies` / `misp-objects` submodule updates.

## Converter

```bash
cd integrations/misp
python -m cli convert ../../attack-paths/colonial-pipeline-2021.json -o colonial.misp.json
python -m cli convert ../../attack-paths/*.json --out-dir out/
python -m cli validate colonial.misp.json
```

Options: `--distribution 0-3` (default 0, your organisation only), `--threat-level 1-4`
(default 4), `--analysis 0-2` (default 2), `--orgc NAME` (omitted by default;
the importing instance assigns its own), `--no-attachment`.

Import the result with **Event Actions → Import from… → MISP JSON**, or via
PyMISP: `misp.add_event(json.load(open("colonial.misp.json")))`.

Every uuid is version 5 over the incident id, so re-importing a regenerated file
updates the same event instead of creating a duplicate. A Layer 3 file that is
structurally unusable exits with code 2 and a message naming the file and item;
full schema validation stays with `npm run validate-attack-paths`.

## Worked example: SolarWinds SUNBURST

`examples/solarwinds-2020.misp.json` is the converter output for
`json-schemas/layer-3/examples/solarwinds-2020.json`.

Event tags:

```
tlctc:cluster="10-supply-chain-attack"   tlctc:cluster="07-malware"
tlctc:cluster="04-identity-theft"        tlctc:cluster="01-abuse-of-functions"
tlctc:entry-cluster="10-supply-chain-attack"
```

Path object `notation`:

```
#10 ||[update][@Vendor→@Org]|| →[Δt=instant] #7 →[Δt=~14d] #4 + [DRE: C] →[Δt=~2h] #1 + [DRE: C]
```

Objects and references:

```
tlctc-attack-path ──includes──▶ s1-supply-chain        cluster=#10  boundary update @Vendor→@Org
                  ──includes──▶ s2-sunburst-execution  cluster=#7   fec-executed=1
                  ──includes──▶ s3-credential-forgery  cluster=#4   data-risk-event=C
                  ──includes──▶ s4-cloud-abuse         cluster=#1   data-risk-event=C
s1 ──followed-by (Δt=instant)──▶ s2 ──followed-by (Δt=~14d)──▶ s3 ──followed-by (Δt=~2h)──▶ s4
```

## Deliberately not included

- No MISP **galaxy**: TLCTC has ten fixed clusters, not a growing catalogue; a
  taxonomy is the right shape.
- No **OpenCTI**, **Attack Flow** or **VERIS** work (separate integrations).
- No **back-conversion** MISP → Layer 3; the `layer3-json` attachment keeps the source.
- No sub-cluster, velocity-class or DRE **taxonomy predicates**: velocity and DRE
  live on the objects where they belong to a step.

For STIX 2.1 output of the same attack paths see `tools/stix-exporter/`.

## Tests

```bash
cd integrations/misp && python -m unittest discover tests      # converts every attack path in the repo
npm run validate-misp                                          # taxonomy, templates, example (from repo root)
```

## Licence

The taxonomy and object template JSON files are contributed upstream under
CC0 1.0 (MISP's convention); the rest of this directory is CC BY 4.0 like the
repository.
