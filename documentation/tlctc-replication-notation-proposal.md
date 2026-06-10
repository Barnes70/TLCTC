# Expressing Replication in TLCTC Attack Paths: A Conceptual Extension Proposal

**Author:** Bernhard Kreinz
**Framework version:** TLCTC v2.1 (notation baseline)
**Document version:** v0.1 — conceptual proposal, draft for peer review
**Status:** Idea-stage. Nothing in this document is normative. No grammar, schema, or whitepaper change is made by this proposal.
**Intended audience:** Standards and framework bodies (NIST, MITRE, CISA, ENISA, NCSCs/CERTs) and the TLCTC community
**License:** CC BY 4.0
**Core thesis:** Keep the operator inventory small. Real-world attacks replicate; the notation should eventually be able to say so — with at most one new structural concept.

---

## 0. One-Sentence Proposal

**TLCTC attack path notation should gain a single structural concept — the replicated subpath — written as `(subpath)×N` for fan-out and `(subpath)×*` for self-propagation, so that mass deployment and worm behavior become first-class, parseable, comparable path structure instead of prose.**

---

## 1. Executive Summary

TLCTC attack path notation today expresses two compositional relationships:

- `→` — *this step enabled that step* (sequence)
- `+` — *these steps happened concurrently, order not meaningful* (parallelism, inside parentheses)

Real-world attacks exhibit a third structural behavior that neither operator can express: **replication** — the same step or subpath instantiated many times across many targets.

- A ransomware operator pushes the encryptor to 2,000 hosts via GPO. The notation writes `#1 → #7` once; reality executed it 2,000 times.
- A wormable exploit (WannaCry, NotPetya) repeats `#2 → #7` from every newly infected host. The path does not fan out from one origin — it *re-enters itself*, generation after generation.
- A mass-exploitation campaign runs one CVE against ~1,800 organizations. Each victim's path is structurally identical; the scale is the story.

The TLCTC project has already met this gap in practice. The Shai-Hulud npm worm analysis (`attack-paths/shai-hulud-worm-2025.json`) is forced to record its defining structural property — recursion — *in prose*:

> "The attack path loops back to s4-install-processing for each new victim, creating a cyclic/fractal propagation pattern. […] each recursion generates a new #10 boundary crossing — supply chain trust is renewed at every propagation step."

That sentence is correct, important, and invisible to every parser, statistic, and comparison tool in the ecosystem. This proposal sketches how to make it visible — and explicitly invites standards bodies to refine, restructure, or replace the sketch.

---

## 2. The Gap

### 2.1 What the notation can and cannot say

| Structural relationship | Operator | Status |
| --- | --- | --- |
| B happened after A, enabled by A | `A → B` | ✅ v2.0 core |
| A and B happened concurrently, order not meaningful | `(A + B)` | ✅ v2.0 core |
| The attack crossed a responsibility boundary | `\|\|[ctx][@A→@B]\|\|` | ✅ v2.0 core / v2.1 transit |
| A step occurred but cannot yet be classified | `?` / `…` | ✅ v2.1 extension |
| **This subpath instantiated N times across N targets** | — | ❌ no syntax |
| **This subpath re-enters itself from each new victim** | — | ❌ no syntax |

Whitepaper §11.0.1 already acknowledges the phenomenon — a cluster "MAY appear multiple times in a single path (retries, re-entry, multiple systems, repeated actions)" — but offers no way to distinguish *one step on one system* from *one step pattern on two thousand systems*.

### 2.2 Why it matters

1. **Comparability.** Two incidents with the path `#9 → #7 → #4 → #1 → #7` are not comparable if one encrypted a single laptop and the other an entire hospital group. Scale is structure, not color commentary.
2. **Velocity.** The whitepaper's velocity model already singles out wormable propagation as the defining VC-4 case ("Realtime — seconds/ms — #6 Flooding, #2 Wormable — architectural controls; human response too slow"). But the *per-generation* spread rate — the single most decision-relevant number for a worm — has no home in the notation. `Δt` annotates the gap between two steps; a worm's tempo is the gap between two *generations* of the same steps.
3. **Statistics integrity.** Without a defined convention, one analyst writes the spreading subpath once, another writes it five times, a third writes one path per victim. Cluster-frequency statistics silently diverge.
4. **Control selection.** Fan-out and self-propagation call for different controls. Fan-out via a management plane (`#1` via GPO, SCCM, MDM) points at tiering and change control on the deployment mechanism. Self-propagation points at architectural segmentation, because each victim becomes an attacker. A notation that cannot distinguish them cannot drive that decision.

### 2.3 What this is *not* about

Scoping discipline matters more than expressiveness. Three adjacent phenomena are **deliberately excluded**:

- **Retry/iteration against the same target** (password spraying, repeated exploit attempts). The existing open annotation mechanism already covers this with zero grammar cost: `#4 [attempts=10000]` parses today under §11.5.1. Repetition against *one* target does not change path shape.
- **OR-branching / alternative vectors.** Whitepaper §11.1.2 already rules: "or" is expressed as multiple alternative paths *outside* the notation. Campaign-level variation belongs in composite pattern studies, not in path syntax.
- **Heterogeneous spread.** If victims experienced *different* cluster sequences, that is not replication of one subpath — it is several paths, and existing mechanisms (separate Layer 3 instances, pattern studies) apply.

What remains — and what this proposal addresses — are the two genuinely *structural* gaps: **fan-out (1→N)** and **self-propagation (recursion)**. They change the shape of the path from a chain into a tree; annotations cannot honestly fake a tree.

---

## 3. Design Constraints

Any future replication syntax should be evaluated against these constraints, which generalize from TLCTC's existing design decisions:

1. **Operator tax.** The notation's value comes from its tiny operator inventory — an analyst learns `→`, `+`, `||...||`, and a few annotations, and can read any path. Every added operator taxes every future reader. The budget for this entire problem space is **one structural concept**.
2. **Cause-side purity (Axiom III).** Replication count is cause-side structure (how the attack propagated), not an outcome. "2,000 hosts encrypted" as an *impact* belongs in DRE/Impact reporting layers; "the attacker instantiated this subpath ~2,000 times" is attack structure and belongs in the path.
3. **Classification neutrality.** Replication must never change cluster classification — mirroring R-INTRA-7 for intra-system boundaries. A `#7` step inside a replicated group is exactly the `#7` it would be outside one.
4. **Additive and backward compatible.** All existing paths must remain valid, exactly as the v2.1 unresolved-step extension (`?`, `…`) preserved every v2.0 path.
5. **The escape ladder.** TLCTC has three tiers of expressiveness: prose/metadata → open annotation `[key=val]` → first-class operator. A phenomenon earns operator status only when it must survive parsing, statistics, and cross-incident comparison. Fan-out and recursion clear that bar; retries do not.
6. **Epistemic honesty.** Victim counts are usually estimates. The syntax must carry approximate and unknown multiplicities without forcing false precision — the same philosophy that produced `[conf=low]` and `?`.

---

## 4. Recommended Concept (Strawman)

This section is a concrete recommendation offered *so that reviewers have something specific to react to*. Section 7 lists alternatives; Section 9 lists the open questions a working group would need to settle.

### 4.1 The replicated subpath

Introduce a **replication group**: a parenthesized subpath followed by a multiplier.

```
(subpath)×N        fan-out:    N independent instantiations from one origin
(subpath)×*        recursion:  each instantiation's terminal step becomes a
                               new origin that re-enters the group
```

- The multiplier sign is `×` (U+00D7), with ASCII alias `x` (e.g., `(...)x2000`) following the precedent of `→`/`->`.
- `N` may be **exact** (`×2000`), **approximate** (`×~2000`), or **unknown-many** (`×?`).
- `×*` is the Kleene-star-flavored recursion marker: unbounded self-application, generation count unknown or growing. An optional generation bound or estimate may annotate it: `×*[gen≈5]`.

**Prerequisite implication (the real grammar cost):** today, parentheses only group `+` (parallel) steps. A replication group must permit a *sequential* subpath inside parentheses — `(#1 → #7)×N`. This is the largest single change implied by this proposal, and it is called out honestly: it touches the ABNF, every parser, and the serialization profile. It is also the reason replication should be designed *once, properly* rather than bolted on.

### 4.2 Semantics of `×N` (fan-out)

`(S)×N` asserts:

1. The subpath `S` was instantiated `N` times.
2. All instantiations share the **same origin** — the step immediately preceding the group enabled every instance.
3. Instances are **homogeneous**: each one followed the cluster sequence written in `S`. (If they differ, this is not replication — see §2.3.)
4. Ordering **among instances** is not meaningful (parallel-flavored); ordering **inside each instance** follows `S` as written.
5. Trailing annotations and DRE tags on the group apply **per instance**: `(#1 → #7)×~2000 + [DRE: Ac]` means each of ~2,000 instances ended in an accessibility loss.

### 4.3 Semantics of `×*` (self-propagation)

`(S)×*` asserts everything `×N` does, plus:

6. The terminal state of each instance **creates a new origin** that re-enters `S` — the tree grows by generations.
7. A `Δt` attached to the recursion describes the **per-generation tempo**: `(S)×*[Δt≈12h/gen]`. This is the worm's defining velocity metric and maps directly onto the whitepaper's VC-4/"wormable" architectural-control argument.
8. Boundary operators inside `S` **re-apply at every generation**. This is the Shai-Hulud invariant, promoted from prose to structure: a `#10` trust-acceptance boundary inside a `×*` group *is* the statement "supply chain trust is renewed at every propagation step."

### 4.4 Draft rule family (R-REPL, conceptual)

Mirroring the structure of the v2.1 R-UNRES and R-INTRA rule families:

| Rule | Statement |
| --- | --- |
| **R-REPL-1** | The multiplier is cause-side structure. It records how the attack propagated, never an impact measurement. |
| **R-REPL-2** | A replication group requires homogeneous instances — one cluster sequence, many targets. Heterogeneous spread MUST be expressed as separate paths or a pattern study. |
| **R-REPL-3** | For cluster-frequency statistics, a replicated subpath counts **once**; the multiplier is reported as a separate scale dimension. (A 300,000-node worm must not swamp cluster statistics — the same reasoning that excludes `?`/`…` from statistics in R-UNRES-3.) |
| **R-REPL-4** | Replication never changes cluster classification (mirrors R-INTRA-7). |
| **R-REPL-5** | Multiplicity MUST be honest: exact `×N` only with evidentiary support; otherwise `×~N` or `×?`. |
| **R-REPL-6** | Boundary operators inside a replication group re-apply per instance (and per generation under `×*`). |
| **R-REPL-7** | `×*` MUST only be used when each instance genuinely creates a new attacker origin (self-propagation). Operator-driven repeated deployment is `×N`, however large N is. |
| **R-REPL-8** | Any path containing a replication group SHOULD carry a prose annotation explaining the propagation mechanism and the basis for the multiplicity estimate (mirrors R-UNRES-8). |

---

## 5. Worked Examples (Informative)

### 5.1 Mass ransomware deployment (fan-out)

Operator phishes in, stages, steals credentials, takes the domain, then pushes the encryptor fleet-wide via GPO:

```
#9 ||[human][@External→@Org]|| →[Δt=24h] #7 →[Δt=5m] #4 →[Δt=15m] #1
   → (#1 → #7)×~2000 + [DRE: Ac]
```

Today this is written `… → #1 → #7 + [DRE: Ac]`, and "2,000 hosts" lives in the notes. The replicated form preserves the corrected sequential reading (`#1 → #7`, per R-EXEC: the GPO push enables the execution) *and* states that this enabler→execution pair instantiated ~2,000 times. `×~2000`, not `×2000`: host counts in IR reports are estimates (R-REPL-5).

### 5.2 Wormable exploit (self-propagation) — WannaCry pattern

```
#2 →[Δt=0s] #7 → (#2 → #7)×*[Δt≈minutes/gen] + [DRE: Ac]
```

The initial exploit-and-execute pair is written once as the patient-zero entry; the replication group states that every infected host re-ran the same `#2 → #7` pair against new targets, with a per-generation tempo in minutes — the structural signature that makes "wormable" a VC-4 architectural-control problem rather than a response-playbook problem.

### 5.3 Shai-Hulud npm worm (recursion across a trust boundary)

The 2025 analysis records, in prose, that the path "loops back" and that "each recursion generates a new #10 boundary crossing." As a replication group, the propagation phase becomes:

```
… → #4 → (#1 → #10 ||[update][@VictimN⇒@npm→@VictimN+1]|| → #7 → #1 → #4)×*[Δt≈12h/gen]
```

Read: each generation publishes poisoned packages (`#1`), a downstream victim accepts the trust artifact (`#10` at the TAE, transiting the registry), the payload executes (`#7`), harvests (`#1`), and the stolen tokens authenticate as the next victim (`#4`) — which is the new origin. The `#10` boundary sits *inside* the group, so R-REPL-6 makes "supply chain trust is renewed at every propagation step" a property of the syntax, not a sentence in the notes.

### 5.4 Mass-exploitation campaign (fan-out across organizations)

One internet-facing CVE, ~1,800 victim organizations:

```
(#2 ||[api][@External→@VictimOrg]|| → #7)×~1800
```

This is the CISA-KEV-shaped case: the unit of replication is the victim *organization*, and the path states that the same exploit→execute pair instantiated across ~1,800 of them. Campaign-level statistics can then distinguish "one incident, internal fan-out" (§5.1) from "one campaign, inter-organizational fan-out" — structurally, not editorially.

---

## 6. What This Proposal Deliberately Does Not Do

- It does **not** modify the ABNF (`grammar/tlctc-attack-path.abnf`), the Layer 3 JSON schema, or whitepaper §11. The notation above is illustrative pseudo-syntax until a working group adopts and specifies it.
- It does **not** introduce syntax for retries (existing annotations suffice) or OR-branching (excluded by §11.1.2; handled by pattern studies).
- It does **not** propose per-victim path explosion. The replication group is precisely the device that avoids writing 2,000 paths or one 2,000-step path.
- It does **not** claim the multiplier is an impact metric. Victim-count-as-impact belongs to consequence-side layers (DRE, and in TLCTC+ contexts, Impact records).

### 6.1 Adoption cost ledger (if a working group proceeds)

Honest accounting of what first-class adoption would touch:

| Artifact | Change |
| --- | --- |
| ABNF grammar | New production: sequential subpath inside parentheses + multiplier suffix. The single largest cost. |
| Whitepaper §11 | New subsection (operators, semantics, R-REPL rules), symbol-table rows for `×`, `×*` |
| Layer 3 JSON schema | A `replication_group` sequence-item variant (sibling of `attack_step`, `parallel_group`, unresolved steps) with `multiplicity`, `multiplicity_basis`, `recursive`, `generation_tempo` fields |
| Parsers/validators | Grouping is structural — every consumer must update |
| Statistics guidance | R-REPL-3 counting convention |
| Visualization | Tree/fractal rendering for `×*` paths |

---

## 7. Alternatives Considered

1. **Annotation-only** — `#7 [targets=2000]`, `#7 [recursive]`. Parses today with zero grammar cost. Rejected as the *end state* because annotations are defined as metadata that "MUST NOT change the meaning of the underlying cluster sequence" (§11.5) — and replication *is* path shape, not metadata. Smuggling structure into annotations would betray the notation's own discipline. (As an *interim* convention while the concept matures, however, annotations are the legitimate tier of the escape ladder — see §8.)
2. **Dedicated recursion symbol** (e.g., `↻`). Visually evocative, but adds a third arrow-like Unicode glyph to a grammar that already documents Unicode burden as a known limitation, and splits fan-out and recursion into two unrelated syntaxes when they are one concept with a closed/open multiplicity.
3. **One path per victim / per generation.** Already the implicit status quo for campaigns. Does not scale, destroys readability, and hides the structural identity of the instances — the very thing worth expressing.
4. **Do nothing.** Defensible — prose and metadata work today, and §8 below is the operational answer for now. But Shai-Hulud demonstrates the cost: the most analytically important property of the most structurally complex npm attack to date is currently invisible to every tool in the ecosystem.

---

## 8. Interim Convention (Usable Today, Zero Grammar Cost)

Until any standards body takes this up, analysts who need to record replication NOW can stay fully conformant with v2.1:

1. Write the replicated subpath **once**, in correct sequential form (e.g., `#1 → #7`).
2. Attach open annotations on the first step of the replicated region: `[fanout=~2000]` or `[propagation=recursive] [gen_tempo=~12h]`. These parse under §11.5.1 today.
3. Record mechanism and multiplicity basis in prose (Layer 3 `notes`), as Shai-Hulud already does.

This three-line convention is deliberately aligned with the strawman semantics so that, if `×N`/`×*` is ever adopted, annotated paths can be migrated mechanically.

---

## 9. Open Questions for NIST / MITRE / CISA and the Community

This proposal is published in the explicit hope that standards bodies adopt the problem, not necessarily the strawman. Concrete questions a working group would need to settle:

1. **Multiplicity vocabulary.** Are `×N` / `×~N` / `×?` / `×*` the right four states? Should generation-bounded recursion (`×*[gen=3]`) be first-class or an annotation?
2. **Statistics counting.** Is R-REPL-3 (count once, scale separately) the right convention for national/sectoral statistics, or do some use cases (e.g., CISA KEV exploitation prevalence) need instance-weighted counts as a defined alternative view?
3. **Unit of replication.** §5.1 replicates across *hosts*, §5.4 across *organizations*. Should the unit be explicit in the syntax (e.g., via the boundary operator inside the group) or remain contextual?
4. **Interaction with ATT&CK.** MITRE ATT&CK models lateral movement and software-deployment-tool abuse as techniques (e.g., T1570, T1072) but has no campaign-scale path structure either. Is there a joint opportunity: TLCTC path structure × ATT&CK technique granularity for describing wormable and mass-deployment behavior?
5. **Interaction with CVE/KEV enrichment.** The TLCTC CVE extension proposal already suggests attack-path context on CVE records. A `wormable` CVE is precisely one whose canonical path ends in `(#2 → #7)×*`. Should "replicated-path potential" become a structured CVE/KEV enrichment field?
6. **Sequential grouping.** The prerequisite change (sequential subpaths inside parentheses) has uses beyond replication — e.g., scoping a DRE or boundary to a subpath. Should it be specified independently first?
7. **Convergence (N→1).** Many origins collapsing onto one target (e.g., distributed contributors to one poisoned artifact) is the structural inverse of fan-out. Real phenomenon or YAGNI? The authors lean YAGNI until a concrete incident demands it.

---

## 10. Status and Relationship to Other TLCTC Documents

| Document | Relationship |
| --- | --- |
| `documentation/tlctc-v2.0-whitepaper.md` §11 | Normative notation this proposal extends conceptually; unchanged by this proposal |
| `grammar/tlctc-attack-path.abnf` | Machine-readable grammar; unchanged by this proposal |
| `documentation/tlctc-cve-extension-proposal.md` | Sibling proposal; intersects at "wormable" CVE enrichment (§9, Q5) |
| `documentation/tlctc-plus-ncsc-proposal.md` | Consequence-side reporting layer; victim-count-as-impact belongs there, multiplier-as-structure belongs here |
| `attack-paths/shai-hulud-worm-2025.json` | Motivating evidence: recursion currently expressible only in prose |

**Status:** v0.1 conceptual draft. Feedback, counter-proposals, and adoption by any standards body are explicitly welcome — that is the point of this document.
