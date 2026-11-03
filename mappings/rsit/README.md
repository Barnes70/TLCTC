# RSIT → TLCTC Mapping

Maps every value of the **Reference Security Incident Taxonomy** (RSIT, `machinev1` version 1003),
the incident taxonomy of the TF-CSIRT working group hosted by ENISA and used by European CSIRTs and
their tools (IntelMQ, MISP), to **TLCTC v2.6**. RSIT records the state of an incident; TLCTC
classifies its cause. For each RSIT value the mapping says what the value already proves about the
cause, which question completes the path where it cannot, and which values are not successful
attacks at all.

| Piece | Path | Notes |
|---|---|---|
| Canonical mapping | `tlctc-rsit.json` | 39 entries, hand-authored, one rationale each |
| Upstream contribution | `upstream/` | **generated** by `scripts/build-rsit-mapping.js`: `machinetag.json` (RSIT `machinev1` + a `tlctc` field per value, the [`rsit2attck`](https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/tree/master/working_copy/rsit2attck) shape), `rsit_2_tlctc.md` (table), `machinetag2tlctc.py` (renderer), `README.md` |
| How a ticket is read | `decision-tree.md` | the analyst walk, by RSIT class |
| Pinned upstream file | `pinned/machinev1`, `PINNED.md` | RSIT master b9ad1f8, sha256 |
| Owner runbook | `upstream-pr.md` | the issue and pull request to the RSIT repository |

## What an RSIT value can say: the mapping types

| `mapping_type` | Entries | Example |
|---|---|---|
| `direct` — one cluster | 4 | `information-gathering/scanner` → #1 (as ATT&CK T1595); `availability/ddos` → #6 |
| `chain` — one cluster plus a step RSIT does not record | 3 | `malicious-code/infected-system` → `<enabler> → #7` (R-EXEC); `fraud/phishing` → `#9 → #4` (R-CRED) |
| `conditional` — several clusters, a condition decides | 7 | `availability/dos` → #6 \| #2 \| #3 (R-SPECIFIC); `availability/sabotage` → #8 \| #1 \| Abuse of Rights |
| `attempt` — an attempted step; a blocked one is a near miss | 3 | `intrusion-attempts/brute-force` → #4; `intrusion-attempts/ids-alert` → #2 \| #3 |
| `exposure` — a state that enables a cluster; no step, no SRE | 5 | `vulnerable/weak-crypto` → enables #5 |
| `indicator` — attacker infrastructure, not a victim event | 4 | `malicious-code/c2-server` → serves #7 on the infected clients |
| `outcome` — a data state, not a cause (Axiom III) | 4 | `information-content-security/unauthorised-information-access` → DRE C; causes RSIT names: #4, #5, #8 |
| `no-cluster` — not an attack on an IT system | 7 | `availability/outage` → Failure row; `fraud/unauthorised-use-of-resources` → Abuse of Rights (R-SCOPE); `abusive-content/harmful-speech` → out of scope |
| `unresolved` — the value does not say what happened | 2 | `other/undetermined` → `?` (R-UNRES-3) |
| `context` | 0 | reserved for parity with the VERIS mapping; RSIT has no vector field |

The rules that shape the table:

- **Successes only carry a tag.** In `upstream/machinetag.json` only the 7 `direct` and `chain`
  values carry a TLCTC MISP machine tag and UUID, because only there does the RSIT state prove the
  step happened. Every other value lists candidate clusters as plain text with the deciding question.
  A cluster tag on an attempt, an exposure or a data state would count a non-attack as an attack.
- **Attempts are near misses.** Intrusion Attempts values assert no successful step. Blocked, they
  are near misses (TLCTC+ v0.9 `near_miss_record`; application paper §10, near misses per cluster
  as a KRI); successful, they belong under the matching Intrusions value.
- **Exposures have no SRE.** The Vulnerable class describes a state of the target. It names the
  cluster the state enables (weak cryptography → #5, as CWE-326/327/757), never a step.
- **Credentials are two steps.** Unprivileged Account Compromise is #4 with the acquisition step
  before it (R-CRED, Axiom X); Phishing is #9 with #4 after it when the credentials are used.
- **Not every RSIT value is a threat.** Outage and Misconfiguration have no attacker (Failure row,
  as VERIS `error.variety.Misconfiguration`). Unauthorised Use of Resources, RSIT's example being
  chain letters on the organisation's email, is an entitled user acting against the purpose of a
  genuine grant: Abuse of Rights (R-SCOPE). Harmful speech, illegal content and copyright
  infringement involve no step against an IT system.
- **Consistency with the other mappings.** Scanning #1 and Sniffing #1 \| #5 follow ATT&CK
  T1595/T1046/T1040; Login Attempts #4 follows T1110; DoS #6 \| #2 \| #3 follows VERIS
  `hacking.variety.DoS`; defacement as a cause hint #7 follows T1491; XSS with #7 follows CWE-79.

## What the mapping cannot do: the terms

Several RSIT values use words that other frameworks, reports and communities define differently,
and the RSIT descriptions do not always draw the line where TLCTC draws it:

- **Phishing** is an indicator (a URL) in RSIT's description, a social-engineering step in TLCTC,
  and a fraud or attack category in other reports.
- **Masquerade** covers both deceiving people and authenticating to a system as someone else.
- **Sabotage** spans physical damage, logical damage by an attacker and damage by an entitled
  administrator, and includes bomb threats.
- **Fraud** and **Information Content Security** group infrastructure, content, misuse and data
  states rather than causes.
- **System Compromise** and **Intrusion Attempts** name a state or an attempt, not how it came about.

The mapping does not settle what these words mean. It maps each value by its description in
`machinev1` version 1003, as written; where one word covers several causes, the entry is
`conditional` and names the question that decides. Two records with the same RSIT tag can therefore
have different causes, and the same cause can appear under different tags. Clearing up the
terms is a question for the RSIT community and for whoever uses them; the TLCTC definitions are in
the [core specification](../../documentation/tlctc-v2.7-core.md).

## Build and validate

```bash
npm run build-rsit       # regenerate upstream/ from tlctc-rsit.json + pinned/machinev1 + the TLCTC MISP taxonomy
npm run validate-rsit    # coverage of machinev1, field pairing, dictionary ids, pinned sha256, tag rule, generated bytes
npm run test-rsit        # node:test (builder, validator) + Python unittest (renderer)
```

## Licences

The mapping and this documentation are CC BY 4.0 like the rest of this repository. The files in
`upstream/` are dedicated to the public domain under CC0 1.0 for contribution to the RSIT repository,
which is CC0. `pinned/machinev1` is RSIT's own file (CC0).

## Deliberately not included

- No empirical study and no classifier: there is no public RSIT-tagged dataset comparable to VCDB.
- No TLCTC MISP galaxy and no change to the TLCTC MISP taxonomy ([MISP/misp-taxonomies#348](https://github.com/MISP/misp-taxonomies/pull/348) is open).
- No new RSIT classes and no edits to RSIT descriptions.
- No attack path is emitted from a single RSIT tag: a tag cannot order steps it does not record.
