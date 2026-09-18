# TLCTC for Attack Flow

Brings TLCTC v2.5 into the MITRE Center for Threat-Informed Defense
[Attack Flow](https://github.com/center-for-threat-informed-defense/attack-flow) ecosystem.
Attack Flow says *what* an adversary did, as a graph of ATT&CK techniques; TLCTC says *which
generic vulnerability* each step exploited. The two are complementary, and this directory holds
the pieces that join them.

| Piece | Path | What it is |
|---|---|---|
| TLCTC source bundle | `stix/tlctc-stix-bundle.json` | **Generated.** The framework as a STIX 2.1 bundle in the shape the Builder consumes for ATLAS and F3: the ten clusters as `x-mitre-tactic`, the ten cluster roots (`TLCTC-0N.00`) and the published sub-clusters as `attack-pattern`. Phase 2 makes TLCTC selectable in the Builder. |
| TLCTC extension | `stix/tlctc-attack-flow-extension.json`, `stix/tlctc-attack-flow-extension-schema-1.0.0.json` | A STIX 2.1 `property-extension` (`extension-definition--69b4eaba-45a8-4101-b935-3a7ae2cb3a1a`) that carries cluster, sub-cluster, Δt, boundaries, DRE, FEC and unresolved state on `attack-action`, path metadata on `attack-flow`, and group metadata on `attack-operator`. |
| Converter | `cli/` | Python 3.10+, standard library only. `classify`: an Attack Flow (`.afb` v2 or STIX bundle) → every action through the ATT&CK→TLCTC mapping and a derived TLCTC path. `export`: a TLCTC Layer 3 path → an Attack Flow STIX bundle with the extension, importable into the Builder. |
| Corpus study | `study/run-study.py`, `study/results.{json,md}` | All 41 flows of the Attack Flow corpus classified; aggregates committed, corpus files not. Report: `documentation/tlctc-attack-flow-corpus-study.md`. |
| Examples | `stix/examples/*.attack-flow.json` | Exports of the SolarWinds example, a path with a parallel group and a path with an unresolved step. |
| Pinned upstream | `pinned/`, `PINNED.md`, `study/corpus-sha256.json` | Attack Flow schema 2.0.0, its extension-definition, the OASIS STIX 2.1 common schemas, three corpus fixtures (Apache-2.0), and the sha256 of every corpus file at the pinned commit. |
| Upstream runbook | `upstream-pr.md` | Phase 2 (Builder framework source PR) and Phase 3 (corpus PRs). |

## How the two models meet

Attack Flow's action carries a two-level TTP tuple (tactic, technique). The Builder fills it from
pluggable framework sources (ATT&CK, ATLAS, D3FEND, F3). The TLCTC source bundle fills it with
the two-layer TLCTC model: the **tactic slot holds the strategic cluster** (`[TLC] #7 Malware`)
and the **technique slot holds the operational position** (`[TLC] TLCTC-07.00 Malware (vector
unspecified)`, or a published sub-cluster such as `TLCTC-02.10 Protocol vector`). Every cluster is
selectable today; sub-clusters appear where the operational enumeration has them.

Independently of the Builder, the extension lets any STIX consumer carry the full TLCTC step
record on an action:

```json
"extensions": {
  "extension-definition--fb9c968a-745b-4ade-9b25-c324172197f4": { "extension_type": "new-sdo" },
  "extension-definition--69b4eaba-45a8-4101-b935-3a7ae2cb3a1a": {
    "extension_type": "property-extension",
    "tlctc_step_id": "s1-supply-chain", "tlctc_status": "classified", "tlctc_cluster": "#10",
    "tlctc_delta_t_to_next": "instant",
    "tlctc_boundary": { "context": "update", "source_sphere": "@Vendor", "target_sphere": "@Org" }
  }
}
```

Unresolved steps (`?`, `…`) carry `tlctc_status: unresolved` and no cluster and no DRE (R-UNRES-2,
R-UNRES-5); the schema enforces it. A `parallel_group` becomes an `AND` operator that the members
lead into.

## Classifier

```bash
cd integrations/attack-flow
python -m cli classify tests/fixtures/corpus/SolarWinds.afb --format md      # one flow → table + derived path
python -m cli classify /path/to/corpus --summary --format md                # a directory → the study tables
python -m cli export ../../json-schemas/layer-3/examples/solarwinds-2020.json -o solarwinds.attack-flow.json
```

Per action the result says what the ATT&CK mapping (or, for `AML.` ids, the [ATLAS mapping](../../mappings/mitre-atlas/)) establishes: `resolved` (one cluster, or one
sequence such as `#10 → #7`), `rule_dependent` (alternatives the flow cannot decide, rendered `?`
with candidates), `preparation` (attacker-side, outside the target domain, left out of the path),
`unmapped` (technique unknown to both mappings: ATT&CK for ICS, revoked ids) or `no_technique` (tactic-only action, rendered `?`).
The derived path follows the flow's own order: conditions continue on the true branch (the false
branch is noted), `AND` operators mark parallel actions, `OR` operators list alternatives in order.
The *compressed* form collapses consecutive actions with the same cluster into one step and keeps
the count; Δt is computed only where two adjacent actions both carry `execution_start`.

The derived path is a classification report, not a Layer 3 record: an Attack Flow does not say
whether a technique was performed by the operator or by a running payload (a #7 feature, not a
step), and it records no boundary and no Data Risk Event.

## Tests and validation

```bash
npm run build-attack-flow && npm run validate-attack-flow   # bundle byte-identical; extension schema; examples validate against the pinned Attack Flow schema + extension schema; results.json consistent
npm run test-attack-flow                                     # readers, mapping grammar, classifier, exporter, CLI
python study/run-study.py                                    # re-run the corpus study (downloads the pinned corpus into a cache)
```

## Licences

Everything here is CC BY 4.0 like the rest of the repository, except the pinned upstream files:
the Attack Flow schema and corpus fixtures (Apache-2.0, © The MITRE Corporation) and the OASIS
STIX 2.1 schemas (BSD-3-Clause), each with its notice.

## Deliberately not included

- No `.afb` writer: the Builder imports STIX and saves `.afb`; that is the manual step of Phase 3.
- No change to `tools/stix-exporter` (generic STIX 2.1 with `x_tlctc_*` properties); it stays for consumers that are not Attack Flow aware.
- No reverse conversion into `attack-paths/`: a derived path needs an analyst before it becomes a record.
- No tags, mitigations or D3FEND links on exported actions (Phase 3 material).
