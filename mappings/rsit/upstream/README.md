# RSIT and TLCTC

Create a relation between the classifications in [RSIT](https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force) and [TLCTC](https://github.com/Barnes70/TLCTC) (Top Level Cyber Threat Clusters).

RSIT classifies the state of an incident: what the data record shows. TLCTC classifies the cause: the generic vulnerability an attacker exploited, in ten non-overlapping clusters (#1 Abuse of Functions … #10 Supply Chain Attack). The two answer different questions, so the link is one-way and changes neither taxonomy: for each RSIT value it states what the value already proves about the cause, and which question decides where it does not.

This follows the pattern of [rsit2attck](../rsit2attck/README.md): one extra field per value in the RSIT machine tag file, and a generated human-readable table.

## Files

| File | Content |
|---|---|
| `machinetag.json` | RSIT `machinev1` (version 1003) with an extra field **tlctc** on every value |
| `rsit_2_tlctc.md` | the human-readable table, generated from `machinetag.json` |
| `machinetag2tlctc.py` | regenerates the table (Python 3, standard library) |

## The `tlctc` field

The field is a list with one element. MISP taxonomy processing ignores it, as it ignores `attck`, so the file can be used in a MISP environment unchanged.

Where the RSIT value proves that the step happened, the element carries the TLCTC machine tag and the UUID of that entry in the TLCTC MISP taxonomy:

```json
"tlctc": [
  { "machinetag": "tlctc:cluster=\"07-malware\"", "uuid": "b553d3b4-c6d9-507d-9c77-1a23c8ac73cd",
    "mapping_type": "chain", "note": "<enabler> → #7 (R-EXEC); RSIT does not record the preceding step. Ask: How did the code arrive and start?",
    "timestamp": 20261103 }
]
```

Every other value carries the candidate clusters as plain text and the deciding question, with no machine tag:

```json
"tlctc": [
  { "candidates": ["#6", "#2", "#3"], "mapping_type": "conditional",
    "note": "One of: #6 (R-SPECIFIC) if volume or intensity exhausts finite resources; … Ask: Flaw or capacity?",
    "timestamp": 20261103 }
]
```

Seven values carry a machine tag: Scanning (#1), Information Gathering / Social Engineering (#9), Burglary (#8), Distributed Denial of Service (#6), Infected System (#7), Unprivileged Account Compromise (#4) and Phishing (#9). The others are left untagged on purpose. In TLCTC a cluster tag asserts that the step succeeded, so a tag on an attempt, an exposure, an indicator or a data state would count something that did not happen as an attack.

| `mapping_type` | Meaning | Values |
|---|---|---|
| `direct` | one cluster | 4 |
| `chain` | one cluster; the rules require a step before or after that RSIT does not record | 3 |
| `conditional` | several clusters; the condition decides | 7 |
| `attempt` | an attempted step; when blocked, a near miss, not an incident | 3 |
| `exposure` | a state of the target that enables a cluster; no step | 5 |
| `indicator` | attacker infrastructure, not a victim event | 4 |
| `outcome` | a data state (confidentiality, integrity, availability), not a cause | 4 |
| `no-cluster` | not an attack on an IT system: failure, abuse of a genuine entitlement, content harm, test | 7 |
| `unresolved` | the value does not say what happened | 2 |

## Regenerate the table

```
python3 machinetag2tlctc.py machinetag.json rsit_2_tlctc.md
```

The `tlctc` fields themselves are maintained in the TLCTC repository (`mappings/rsit/tlctc-rsit.json`, with one rationale per value) and regenerated when `machinev1` changes.

## References

- TLCTC v2.7 core specification: <https://doi.org/10.5281/zenodo.23437984> (the classifications used here are those of v2.6, unchanged in v2.7)
- TLCTC MISP taxonomy (proposed): <https://github.com/MISP/misp-taxonomies/pull/348>
- Mapping source with rationales: <https://github.com/Barnes70/TLCTC/tree/main/mappings/rsit>

## Licence

The files in this directory are dedicated to the public domain under CC0 1.0 Universal, like the rest of this repository.
