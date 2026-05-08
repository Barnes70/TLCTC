# TLCTC+ Specification v0.3

## TLCTC-Anchored Digital-Harm Reporting Extension for NCSCs, CERTs, and Regulators

**Author:** Bernhard Kreinz  
**Base framework:** TLCTC v2.1  
**Extension version:** TLCTC+ v0.3  
**Status:** Released  
**License:** CC BY 4.0  
**Core thesis:** Keep TLCTC pure. Extend the reporting layer.  

> **Companion document:** This is the **implementation specification** — grammar, conformance, catalogues, JSON record formats. For the **policy proposal** (why NCSCs/CERTs need TLCTC+, why anchor on #9, governance, adoption path, risks/benefits), see [`tlctc-plus-ncsc-proposal.md`](tlctc-plus-ncsc-proposal.md). The proposal makes the case; this spec defines how to build it.

---

## 0. Executive Summary

TLCTC+ is a reporting extension for cases that have a TLCTC anchor.

It covers exactly what the name implies:

1. **TLCTC cause space** — the ten TLCTC threat clusters and their attack-path grammar.
2. **Consequence-side reporting grammar** — explicit SRE, DRE, BRE, Impact, Pattern, and Report notation built on top of TLCTC.
3. **NCSC/CERT digital-harm intake** — cyber incidents, cyber-enabled harm, and pure #9-anchored digital crimes.

TLCTC+ is **not** a complete operational-risk taxonomy. It does not classify non-cyber operational failures. It does not introduce an ORE notation. It does not duplicate or replace TLSFC.

The long-term target architecture is:

```text
TLCTC  ─┐
        ├─→ shared BRE / Impact / Report catalogue
TLSFC  ─┘
```

The shared consequence catalogues are embedded in this specification because TLCTC+ is their first consumer. The catalogue codes (PATTERN, BRE, IMPACT, REPORT) are versioned independently from the specification document — see §0.1. Once TLSFC reaches publication readiness, the BRE / Impact / Report catalogues SHOULD be extracted into a neutral consequence-side specification shared by TLCTC and TLSFC.

### 0.1 Document and Catalogue Versions

```text
Specification document version:   TLCTC+ v0.3
PATTERN catalogue version:        v0.2
BRE catalogue version:            v0.2
IMPACT catalogue version:         v0.2
REPORT catalogue version:         v0.2
```

The catalogue version intentionally lags the document version: v0.3 is a grammar and conformance refinement that adds, removes, or renumbers no catalogue codes. The next catalogue revision will bump alongside the document version that introduces it.

---

## 1. Scope

TLCTC+ covers three sub-cases, and only three.

### 1.1 Core Cyber Incidents

A full TLCTC attack path leads to a System Risk Event, may lead to one or more Data Risk Events, and may lead to Business Risk Events.

```text
#9 → #7 + [SRE] + [DRE: Ac] + [BRE: BRE-SVC.11]
```

Canonical chain:

```text
TLCTC path → SRE → DRE → BRE*
```

### 1.2 Hybrid Cyber-Enabled Harm

A TLCTC attack path exists, but the nationally or regulatorily dominant interest is the consequence side.

Examples:

- Business Email Compromise
- Account takeover
- Ransomware-driven outage
- Payment diversion after credential theft
- Malware-assisted fraud
- Supply-chain incident causing regulatory reporting

Example:

```text
#9 + [DRE: C] → #4 + [SRE] 
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 80,000]
```

### 1.3 Pure #9-Anchored Digital Crimes

No IT system is compromised, so no SRE occurs. The digital harm is anchored on #9 Social Engineering. A DRE MAY be recorded only when the #9 step itself directly causes data disclosure, modification, or loss of accessibility/availability **without** system compromise — typically `+ [DRE: C]` for credential or PII handover during phishing.

If the disclosed artifact is later **used** to operate as an identity or to perform a privileged action, the case transitions out of the pure-#9 class into hybrid cyber-enabled harm:

```text
#9 ... + [DRE: C]                    pure-#9 with DRE (no use observed yet)
#9 ... + [DRE: C] → #4 + [SRE]       hybrid: credential use causes SRE
```

Examples that remain pure-#9 (with or without DRE):

- Romance scam without credential theft or malware (no DRE)
- Investment scam without account takeover (no DRE)
- Fake support scam without code execution or credential use (no DRE)
- Authority impersonation inducing payment (no DRE)
- Sextortion payment without system compromise (no DRE)
- Phishing that captured credentials but where credential use is not yet confirmed (`+ [DRE: C]`, no SRE)

Example (no DRE):

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

Example (DRE without SRE — credentials disclosed but credential use not yet observed):

```text
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-ID.11 Phishing for Credentials]
+ [DRE: C]
```

The `||...||` boundary operator is REQUIRED on the #9 anchor: #9 is a TLCTC v2.1 bridge cluster, and the TLCTC+ profile strengthens the v2.1 boundary requirement to MUST for all bridge-cluster steps in TLCTC+ records (see §7 R-9-BOUNDARY).

---

## 2. Explicit Non-Scope

The following are outside TLCTC+ v0.3.

### 2.1 Non-Cyber Operational Failure

The following case is **not** a TLCTC+ case:

```text
[Batch failure] → payment outage → customer churn
```

It has no TLCTC anchor by construction. It belongs in TLSFC or another non-adversarial operational-risk framework.

### 2.2 ORE Notation

TLCTC+ v0.3 does **not** define:

```text
[ORE: ...]
```

and does not contain an ORE catalogue.

### 2.3 Complete OpRisk Taxonomy

TLCTC+ is not a full OpRisk taxonomy. OpRisk functions may consume TLCTC+ output for the cyber-and-digital-crime portion of their portfolio, but non-cyber operational failure must be classified elsewhere.

### 2.4 New Threat Clusters

TLCTC+ does not add an eleventh TLCTC cluster. Labels such as "ransomware", "data breach", "romance scam", "BEC", "payment outage", or "external fraud" are not TLCTC threat clusters.

---

## 3. Design Principles

### 3.1 Preserve TLCTC Core

TLCTC+ SHALL preserve TLCTC semantics unchanged.

That means:

```text
Threats remain causes.
SRE is the central Bow-Tie event.
DREs remain data/resource risk events.
BREs remain business consequence events.
Patterns remain narrative/operational descriptors.
Impacts remain measurements.
Reports remain procedural artefacts or workflow states.
Controls remain barriers, not threats.
```

### 3.2 Cause First

Every TLCTC+ record MUST begin with a TLCTC cause path or a #9 anchor.

Correct:

```text
#9 → #4 + [SRE] + [BRE: BRE-FIN.11]
```

Incorrect:

```text
[BRE: Romance Scam] → #4
```

### 3.3 Explicit SRE

SRE is first-class in TLCTC+.

An SRE records the cyber Bow-Tie central event: **Loss of Control / System Compromise**.

Cyber incidents use:

```text
<TLCTC path> + [SRE]
```

Cyber incidents with data/resource consequences use:

```text
<TLCTC path> + [SRE] + [DRE: C|I|Ac|Av]
```

### 3.4 Optional SRE for Pure #9 Digital Crimes; DRE Permitted for Direct Disclosure

If no IT system is compromised, the SRE node is omitted.

Pure human-target digital crimes may proceed directly from #9 to BRE:

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11] + [BRE: BRE-FIN.11]
```

A DRE MAY be recorded on a pure-#9 step when the social-engineering act itself directly causes data disclosure, modification, inaccessibility, or unavailability — without system compromise. The most common case is credential or PII handover during phishing:

```text
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-ID.11] + [DRE: C]
```

If the disclosed artifact is later **used** (credential application, account takeover, privileged action), the case is no longer pure-#9: it transitions to hybrid cyber-enabled harm with `→ #4 + [SRE]` per Axiom X / R-CRED.

This does not weaken the SRE. It states that no cyber central event has occurred (yet) for cases recorded as pure-#9.

The TLCTC v2.1 boundary operator `||...||` remains REQUIRED on #9 anchors regardless of whether an SRE or DRE follows. #9 is a bridge cluster in core TLCTC, and the TLCTC+ profile strengthens the v2.1 bridge-cluster boundary requirement from SHOULD to MUST for all TLCTC+ records. See §7 R-9-BOUNDARY.

### 3.5 Pattern/Event Separation

Scam names and fraud playbooks are **patterns**, not BREs.

Correct:

```text
#9 [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
```

Incorrect:

```text
#9 + [BRE: Romance Scam]
```

The phrase "romance scam" describes the attacker's manipulation narrative. The BRE is the observable business or citizen consequence.

### 3.6 BRE/Event and Impact/Measurement Separation

A BRE is what happened.  
An Impact is how much it hurt.

Correct:

```text
[BRE: BRE-CUS.11 Customer Account Closure]
+ [Impact: IMPACT-FIN.16 Customer Churn Loss = EUR 1.2m]
```

Incorrect:

```text
[BRE: Financial Loss]
```

### 3.7 REPORT/BRE-REG Separation

BRE-REG codes describe regulatory events.

REPORT codes describe procedural artefacts or reporting workflow states produced in response to those events.

Example:

```text
+ [BRE: BRE-REG.11 Mandatory Notification Obligation]
+ [Report: REPORT-NIS2.11 24h Early Warning Filed]
```

REPORT codes do not appear inside BRE chains.

### 3.8 Pattern Annotation Position (Cause-Side, Non-Additive)

Pattern is the only TLCTC+ annotation that attaches to a TLCTC step in **bracket-only** form, without the leading `+`:

```text
#9 ||[ctx][@A→@B]|| [Pattern: PATTERN-FIN.11]
```

The asymmetry is intentional. SRE, DRE, BRE, Impact, and Report are **consequence-side** annotations: they sit to the right of the Bow-Tie centre and are joined to the path with the additive `+ [...]` form already used by core TLCTC for `+ [DRE: ...]`.

Pattern is **cause-side metadata**: it qualifies the realized step (what manipulation narrative or playbook this step instantiates) rather than recording a downstream event. Bracket-only attachment aligns Pattern with other v2.1 step-level annotations such as `[conf=low]`, `[inferred]`, and `[Δt=...]`, which are also bracket-only and step-scoped.

Mnemonic:

```text
[X = ...]      step-level metadata (cause-side; qualifies the step)
+ [X: ...]     consequence-side event (right of the Bow-Tie centre)
```

A Pattern annotation MUST NOT be written with `+`, and a SRE/DRE/BRE/Impact/Report annotation MUST NOT be written without `+`. See §7 R-PATTERN-POSITION.

### 3.9 Cause/Consequence Independence

A TLCTC cluster on the cause side does NOT determine the BRE family on the consequence side.

The cluster classifies the generic vulnerability that was exploited; the BRE family classifies the kind of business, citizen, service, regulatory, or organizational consequence that resulted. These are independent dimensions, and a record may use any combination supported by the case.

```text
#4 → BRE-ID.*     human-identity takeover (e.g., personal email account)
#4 → BRE-SVC.*    technical-identity takeover (e.g., service-account → payment outage; no BRE-ID)
#7 → BRE-FIN.*    malware-driven fraud
#7 → BRE-SVC.*    malware-driven service outage
#9 → BRE-FIN.*    pure-#9 induced payment (no SRE, no BRE-ID)
#9 → BRE-CUS.*    pure-#9 citizen harm without financial event
#10 → BRE-REG.*   compromised supplier triggering regulatory notification
```

The same #4 step may produce a BRE-ID, BRE-SVC, BRE-FIN, BRE-DATA, BRE-ORG, or none of these depending on whose identity was stolen and what the attacker did with it. Cause-side classification of credential use remains #4 (per R-CRED); consequence-side BRE follows the actual harm. See §7 R-CAUSE-CONSEQUENCE-INDEPENDENCE, §11.4 note, and §17.8 worked example.

---

## 4. Tracks, Not Layers

TLCTC+ avoids the term "Layer N" to prevent collision with TLCTC core layering and control-effectiveness models.

TLCTC+ uses six tracks.

```text
Cause Track       TLCTC path or #9 anchor (Pattern attaches here)
SRE Track         System Risk Event (Loss of Control / System Compromise)
DRE Track         Data Risk Event(s)
BRE Track         Business Risk Event chain
Impact Track      Quantified or qualified impact
Report Track      Reporting workflow and procedural artefacts
```

SRE and DRE are separated because they are independently observable consequence events with distinct linkage semantics in the data model (§15.4 vs §15.5). A record may carry an SRE without any DRE (post-compromise, pre-data-impact) and may carry a DRE without an SRE (pure-#9 cases where confidentiality is lost through disclosure but no system is compromised).

---

## 5. Core Chain Models

### 5.1 Core Cyber Incident

```text
TLCTC path + [SRE] + [DRE: X] + [BRE: BRE₁ → BRE₂] + [Impact: IMPACT₁]
```

Example:

```text
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: Ac]
+ [BRE: BRE-SVC.11 Payment Function Unavailable → BRE-CUS.11 Customer Account Closure]
+ [Impact: IMPACT-FIN.16 Customer Churn Loss = EUR 2.4m]
```

### 5.2 Cyber Compromise Without DRE

This is a critical detection-window scenario.

```text
#2 → #7 + [SRE]
```

Meaning:

- the attacker achieved system compromise / loss of control;
- no DRE has yet been observed;
- dwell time and containment controls operate between SRE and any later DRE.

### 5.3 Hybrid Cyber-Enabled Harm

```text
#9 ||[email][@External→@Org]|| + [DRE: C] → #4 + [SRE]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 50,000]
```

### 5.4 Pure #9-Anchored Digital Crime

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

There is no SRE because no IT system was compromised.

### 5.5 Transitioning Case

A case can begin as pure #9 digital crime and later become a cyber incident.

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
→[case evolution] #9 ||[email][@External→@Citizen]|| + [DRE: C] → #4 + [SRE]
+ [BRE: BRE-ID.13 Email Account Takeover Harm]
```

The same incident file may contain both chains, but each chain records its own semantics.

---

## 6. Notation

### 6.1 TLCTC Attack Path

Unchanged from TLCTC core.

```text
#9 → #4 → #7
```

**Editorial convention.** Short syntax snippets in §3, §6, §7, §8, and §10–§13 illustrate one specific notational point and may omit boundary operators (`||...||`), Δt annotations, transit (`⇒`), and intra-system (`|...|`) markers for readability. Worked examples (§5 Core Chain Models, §17 Worked Examples, §16 JSON Records) are fully conformant: they include all v2.1 boundary operators required by core TLCTC and by R-9-BOUNDARY. When a TLCTC+ record is *produced* (not just illustrated), the full v2.1 grammar applies.

### 6.2 SRE Annotation

SRE is additive to the realized TLCTC path.

```text
#7 + [SRE]
```

SRE MUST NOT be written as a TLCTC attack step.

Incorrect:

```text
#7 → [SRE]
```

### 6.3 DRE Annotation

DRE is additive to the step or path segment that causes it.

```text
#9 + [DRE: C] → #4
```

or:

```text
#9 → #4 + [DRE: C]
```

Both are valid if placement semantics are clear.

### 6.4 BRE Annotation

A single BRE:

```text
#7 + [SRE] + [DRE: Ac] + [BRE: BRE-SVC.11 Payment Function Unavailable]
```

A BRE chain:

```text
#7 + [SRE] + [DRE: Ac]
+ [BRE: BRE-SVC.11 Payment Function Unavailable → BRE-CUS.11 Customer Account Closure]
```

Parallel BREs:

```text
#7 + [SRE] + [DRE: Ac]
+ [BRE: BRE-SVC.11 → (BRE-CUS.11 + BRE-LGL.11)]
```

The `→` operator inside `[BRE: ...]` denotes BRE-to-BRE causal sequence on the consequence side. It is **scoped to the bracket fence** and parser-distinct from the cause-side TLCTC path operator `→`. A parser tokenizing TLCTC+ MUST treat `→` outside any annotation bracket as cause-side path progression and `→` inside an `[BRE: ...]` annotation as BRE-chain causality. See §7 R-BRE-OP-SCOPE.

### 6.5 Pattern Annotation

Patterns are attached to the cause side, typically #9, and follow any boundary operator on that step.

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
```

When the cause-side step is a bridge cluster (#8, #9, #10), the v2.1 boundary operator `||...||` is REQUIRED and precedes the Pattern annotation. The order of step-level annotations on a bridge step is:

```text
#X ||[ctx][@A→@B]|| [Pattern: ...] [conf=low]?
```

A pattern may also annotate a broader path when the narrative spans multiple TLCTC steps:

```text
#9 ||[email][@External→@Org]|| [Pattern: PATTERN-FIN.22 Invoice / Mandate Fraud] → #4
```

Pattern is bracket-only (no `+`); see §3.8 and §7 R-PATTERN-POSITION.

### 6.6 Impact Annotation

```text
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

Multiple impacts:

```text
+ [Impact: IMPACT-FIN.12 + IMPACT-FIN.14]
```

### 6.7 Report Annotation

```text
+ [Report: REPORT-NIS2.11 24h Early Warning Filed]
```

Reports are workflow artefacts and do not appear in BRE chains.

---

## 7. Normative Rules

### R-SRE

If a TLCTC attack path results in Loss of Control / System Compromise, the record MUST include `+ [SRE]`.

### R-SRE-OPTIONAL-9

If a case is purely #9-anchored digital harm and no IT system is compromised, the SRE node SHALL be omitted.

### R-DRE-PLACEMENT

A DRE annotation applies to the immediately preceding TLCTC step or path segment unless explicitly linked by ID in a structured representation.

Example:

```text
#9 + [DRE: C] → #4
```

means the confidentiality loss occurred during the #9 step.

Example:

```text
#9 → #4 + [DRE: C]
```

means the confidentiality loss is associated with the #4 step or with the path segment ending at #4, depending on structured linkage.

For machine-readable records, DREs SHOULD use `linked_to_step`.

### R-BRE-CHAIN

BREs are consequence-side events. TLCTC+ MAY use `→` for sequential BRE causality and `+` for parallel or co-realized BREs inside the BRE lane.

### R-BRE-NOT-PATH

BREs MUST NOT be inserted into the TLCTC attack path.

Incorrect:

```text
#7 → [BRE: BRE-SVC.11]
```

Correct:

```text
#7 + [SRE] + [DRE: Ac] + [BRE: BRE-SVC.11]
```

### R-PATTERN-SPLIT

Scam, fraud, extortion, and manipulation playbook labels MUST be recorded as Pattern metadata, not as BREs.

Incorrect:

```text
+ [BRE: Romance Scam]
```

Correct:

```text
#9 [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
```

### R-IMPACT

Financial loss, cost, volume, number of affected customers, downtime duration, and similar measurements SHOULD be recorded as Impact attributes, not BREs.

### R-REPORT

REPORT codes describe reporting artefacts or workflow stages. They are not BREs and SHALL NOT be included inside the BRE expression.

### R-RECOVERABILITY

For cyber records, stripping all `SRE`, `DRE`, `BRE`, `Impact`, `Pattern`, and `Report` annotations MUST recover a valid TLCTC path.

For pure #9 digital-harm records, stripping all annotations MUST recover a valid #9 anchor (including its v2.1 boundary operator).

### R-PATTERN-POSITION

Pattern annotations attach to a TLCTC step in bracket-only form (`[Pattern: ...]`, no leading `+`) and qualify the cause-side step. Pattern MUST NOT appear with the additive `+ [Pattern: ...]` form. Conversely, SRE / DRE / BRE / Impact / Report annotations MUST NOT appear in bracket-only form. Pattern MUST NOT appear inside an SRE / DRE / BRE / Impact / Report annotation.

Rationale: Pattern is cause-side metadata (qualifying *what manipulation narrative occurred*), not a consequence-side event. The bracket-only form aligns Pattern with v2.1 step-level annotations (`[conf=low]`, `[inferred]`, `[Δt=...]`). See §3.8.

### R-9-BOUNDARY (TLCTC+ Profile Strengthening)

**Core TLCTC v2.1 baseline.** TLCTC v2.1 defines the boundary operator `||[ctx][@A→@B]||` for bridge clusters (#8, #9, #10) to mark cross-domain attack paths. The v2.1 specification establishes this as the canonical notation for bridge-cluster steps.

**TLCTC+ strengthening.** For TLCTC+ records — which serve national reporting, intake, and statistics — every #8 / #9 / #10 step MUST carry an explicit boundary operator. This includes pure-#9-anchored digital crimes (record_type `pure_9_digital_crime`), where the boundary operator captures the channel and source/target spheres needed for downstream warning, triage, and cross-border referral.

This is a **profile rule for TLCTC+ records**, not a modification of core TLCTC v2.1. Core TLCTC remains unchanged: TLCTC+ adds a stricter conformance requirement for the reporting layer that wraps the cause-side notation.

Correct:

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11]
+ [BRE: BRE-FIN.11]
```

Incorrect (missing boundary operator — non-conformant under TLCTC+, even if accepted by core v2.1 grammar):

```text
#9 [Pattern: PATTERN-FIN.11] + [BRE: BRE-FIN.11]
```

Core cyber records (record_type `core_cyber_incident`) and hybrid records (record_type `hybrid_cyber_enabled_harm`) likewise MUST include boundary operators on every #8/#9/#10 step they contain. Intra-system boundary operators (`|[type][@from→@to]|`) remain OPTIONAL per v2.1.

### R-BRE-OP-SCOPE

The `→` and `+` operators MAY appear both in the cause-side TLCTC path and inside an `[BRE: ...]` annotation. Their semantics are scoped:

- Outside any annotation bracket: cause-side TLCTC operators (path sequence / parallel cluster execution).
- Inside `[BRE: ...]`: consequence-side BRE-to-BRE causality (`→`) and parallel/co-realized BREs (`+`).

A conformant parser MUST track bracket nesting and disambiguate operator semantics by scope. The two scopes never mix: a TLCTC cluster reference (`#1`–`#10`) MUST NOT appear inside `[BRE: ...]`, and a BRE code MUST NOT appear in the cause-side path.

### R-V01-MIGRATION

A v0.1 record using a free-text BRE label (e.g., `#9 + [BRE: Romance Scam]`) is NOT conformant in v0.3. Migration MUST:

1. Move the narrative scam / fraud / extortion label from `+ [BRE: ...]` to `[Pattern: PATTERN-XXX.YY ...]` on the cause-side step.
2. Replace the BRE annotation with one or more structured BRE codes from §11 describing the actual consequence event(s).
3. Restore the v2.1 boundary operator on bridge-cluster anchors (per R-9-BOUNDARY) if it was omitted in the v0.1 record.

Example migration:

```text
v0.1:  #9 + [BRE: Romance Scam]
v0.3:  #9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
       + [BRE: BRE-FIN.11 Authorized Push Payment Made]
```

Free-text BRE labels remain readable in archival v0.1 records but MUST NOT be produced in new v0.3 records.

### R-CAUSE-CONSEQUENCE-INDEPENDENCE

The TLCTC cluster on the cause side and the BRE family on the consequence side are independent dimensions. A record MUST NOT assume that a given cluster automatically maps to a particular BRE family, and intake systems, mappers, or tooling MUST NOT auto-fill consequence-side BREs from cluster identity alone.

In particular:

- `#4` Identity Theft does NOT entail BRE-ID. `#4` against a **technical identity** (service account, API key, machine credential, Kerberos service ticket, OAuth client secret, certificate, robot/RPA account) typically produces BRE-SVC / BRE-FIN / BRE-DATA / BRE-ORG with no BRE-ID. BRE-ID is reserved for cases where a human or organizational identity is the harmed entity. See §11.4 note.
- `#7` Malware does NOT entail any specific BRE family — outcome depends on payload behavior and operator objective.
- `#9` Social Engineering does NOT entail BRE-FIN. Many `#9`-anchored cases produce BRE-CUS, BRE-REP, or BRE-LGL outcomes without any financial event.
- `#10` Supply Chain Attack does NOT entail BRE-REG, even where regulatory reporting is common.

Cluster identity classifies the generic vulnerability exploited (cause). BRE identity classifies the harmed business, citizen, service, regulatory, or organizational dimension (consequence). They MUST be recorded independently. See §3.9.

---

## 8. Formal Grammar

### 8.1 Top-Level Expression

```text
<tlctc-plus-record> ::= <cyber-record> | <pure-9-record>
```

### 8.2 Cyber Record

```text
<cyber-record> ::= <tlctc-path>
                   <sre-annotation>?
                   <dre-annotation>*
                   <bre-annotation>*
                   <impact-annotation>*
                   <report-annotation>*
```

Normative note: `sre-annotation` is optional in grammar because the record may represent a pre-compromise attack path hypothesis. It is mandatory under R-SRE once Loss of Control / System Compromise has occurred.

### 8.3 Pure #9 Record

```text
<pure-9-record> ::= "#9" <boundary-annotation>
                    <pattern-annotation>?
                    <dre-annotation>?
                    <bre-annotation>+
                    <impact-annotation>*
                    <report-annotation>*
```

Notes:

- `<boundary-annotation>` is REQUIRED on the #9 anchor under R-9-BOUNDARY (#9 is a v2.1 bridge cluster).
- `<dre-annotation>` is OPTIONAL and limited to the case where the #9 step itself causes a direct DRE (typically `+ [DRE: C]` for credential or PII disclosure) without system compromise. If credential use follows, the record transitions to a `<cyber-record>` of the form `#9 ... + [DRE: C] → #4 + [SRE]`. See §3.4 and §5.4.
- `<sre-annotation>` is forbidden in `<pure-9-record>` by definition (no IT system was compromised).

### 8.4 TLCTC Path

```text
<tlctc-path> ::= <tlctc-step>
               | <tlctc-path> "→" <tlctc-path>
               | <tlctc-path> "+" <tlctc-path>
               | "(" <tlctc-path> ")"

<tlctc-step> ::= <cluster> <boundary-annotation>?
                           <intra-boundary-annotation>?
                           <step-annotation>*

<cluster> ::= "#1" | "#2" | "#3" | "#4" | "#5" | "#6" | "#7" | "#8" | "#9" | "#10"

<step-annotation> ::= <pattern-annotation>
                    | <confidence-annotation>      ; "[conf=low]" etc. — v2.1
                    | <inference-annotation>       ; "[inferred]"   — v2.1
                    | <delta-t-annotation>         ; "[Δt=...]"     — v2.1
                    | <other-v21-step-annotation>
```

Notes:

- `<boundary-annotation>` is REQUIRED on bridge-cluster steps (#8, #9, #10) under R-9-BOUNDARY for the TLCTC+ profile (see §7).
- `<intra-boundary-annotation>` covers the v2.1 intra-system operator `|[type][@from→@to]|` (sandbox / privilege / process / hypervisor).
- Pattern is a step-annotation (cause-side, bracket-only) and never an additive consequence-side tag.

### 8.4a Boundary Annotation

```text
<boundary-annotation> ::= "||[" <context> "][" <sphere-list> "]||"

<sphere-list>     ::= <sphere> ( <transit-arrow> <sphere> )* <boundary-arrow> <sphere>
<boundary-arrow>  ::= "→" | "->"
<transit-arrow>   ::= "⇒"                  ; v2.1 transit operator
<sphere>          ::= "@" 1*ALNUM_SPHERE
<context>         ::= 1*ALNUM_CONTEXT
```

The `<boundary-annotation>` production is unchanged from TLCTC v2.1 (see `grammar/tlctc-attack-path.abnf`). It is included here for self-containment of the TLCTC+ grammar; the canonical definition remains in the v2.1 ABNF.

### 8.5 SRE Annotation

```text
<sre-annotation> ::= "+ [SRE]"
```

### 8.6 DRE Annotation

```text
<dre-annotation> ::= "+ [DRE: " <dre-expression> "]"

<dre-expression> ::= <dre-node>
                   | <dre-expression> "+" <dre-expression>
                   | "(" <dre-expression> ")"

<dre-node> ::= "C" | "I" | "Ac" | "Av" | "A"
            ; "A" is a legacy v2.0 alias for "Availability/Accessibility general"
            ; (see CLAUDE.md §"Attack Path Notation"). New records SHOULD prefer
            ; "Av" or "Ac" for explicit semantics. "A" remains valid for
            ; backward compatibility with the existing v2.1 attack-path corpus.
```

### 8.7 BRE Annotation

```text
<bre-annotation> ::= "+ [BRE: " <bre-expression> "]"

<bre-expression> ::= <bre-node>
                   | <bre-expression> "→" <bre-expression>
                   | <bre-expression> "+" <bre-expression>
                   | "(" <bre-expression> ")"

<bre-node> ::= <bre-code> <label>?
```

### 8.8 Pattern Annotation

```text
<pattern-annotation> ::= "[Pattern: " <pattern-expression> "]"

<pattern-expression> ::= <pattern-node>
                       | <pattern-expression> "+" <pattern-expression>
                       | "(" <pattern-expression> ")"

<pattern-node> ::= <pattern-code> <label>?
```

### 8.9 Impact Annotation

```text
<impact-annotation> ::= "+ [Impact: " <impact-expression> "]"

<impact-expression> ::= <impact-node>
                      | <impact-expression> "+" <impact-expression>
                      | "(" <impact-expression> ")"

<impact-node> ::= <impact-code> <label>? <value>?
```

### 8.10 Report Annotation

```text
<report-annotation> ::= "+ [Report: " <report-expression> "]"

<report-expression> ::= <report-node>
                      | <report-expression> "+" <report-expression>
                      | "(" <report-expression> ")"

<report-node> ::= <report-code> <label>?
```

---

## 9. Namespaces

TLCTC+ uses separate namespaces.

```text
TLCTC-XX.YY       TLCTC operational threat notation
SRE               System Risk Event / Loss of Control / System Compromise
DRE-X             Data Risk Event
PATTERN-XXX.YY    Cause-side narrative / digital crime pattern
BRE-XXX.YY        Business Risk Event
IMPACT-XXX.YY     Quantified or qualified impact
REPORT-XXX.YY     Reporting artefact / workflow state
```

These namespaces MUST NOT be collapsed.

---

# 10. Pattern Catalogue v0.2

Patterns describe attacker narratives, criminal playbooks, or reporting labels. They are **not** BREs.

## 10.1 Financial Manipulation Patterns

```text
PATTERN-FIN.00 Financial Manipulation Pattern — reserved
PATTERN-FIN.10 Induced Payment Pattern Family — reserved
PATTERN-FIN.11 Romance / Relationship Scam
PATTERN-FIN.12 Investment / Crypto-Investment Scam
PATTERN-FIN.13 Fake Tech Support Scam
PATTERN-FIN.14 Authority / Government Impersonation Scam
PATTERN-FIN.15 Advance-Fee / Prize / Grant Scam
PATTERN-FIN.16 Online Purchase / Merchandise Scam
PATTERN-FIN.17 Recovery Scam
PATTERN-FIN.18 Sextortion Scam
PATTERN-FIN.19 Mule / Money Transfer Recruitment
PATTERN-FIN.20 Business Payment Manipulation Pattern Family — reserved
PATTERN-FIN.21 Business Email Compromise
PATTERN-FIN.22 Invoice / Mandate Fraud
PATTERN-FIN.23 Payroll Diversion Scam
PATTERN-FIN.24 Supplier Impersonation
PATTERN-FIN.25 CEO / Executive Impersonation
```

## 10.2 Identity and Account Manipulation Patterns

```text
PATTERN-ID.00 Identity / Account Manipulation Pattern — reserved
PATTERN-ID.11 Phishing for Credentials
PATTERN-ID.12 MFA Fatigue / Push Manipulation
PATTERN-ID.13 Fake Login Portal
PATTERN-ID.14 SIM-Swap Inducement
PATTERN-ID.15 Account Recovery Abuse Narrative
PATTERN-ID.16 Social Media Impersonation
```

## 10.3 Coercion and Extortion Patterns

```text
PATTERN-EXT.00 Coercion / Extortion Pattern — reserved
PATTERN-EXT.11 Sextortion Threat
PATTERN-EXT.12 Data Leak Threat
PATTERN-EXT.13 Physical Harm Threat
PATTERN-EXT.14 Reputational Harm Threat
PATTERN-EXT.15 Law-Enforcement Impersonation Threat
```

---

# 11. BRE Catalogue v0.2

BREs are discrete, observable business, citizen, legal, regulatory, service, or organizational consequence events.

## 11.1 Service / Operations

```text
BRE-SVC.00 Service / Operational Consequence — reserved
BRE-SVC.11 Payment Function Unavailable
BRE-SVC.12 Authentication Service Unavailable
BRE-SVC.13 Customer Portal Unavailable
BRE-SVC.14 Transaction Processing Delayed
BRE-SVC.15 Manual Workaround Activated
BRE-SVC.16 Critical Business Process Interrupted
BRE-SVC.17 Settlement / Clearing Disruption
BRE-SVC.18 Public Service Delivery Disrupted
BRE-SVC.19 Safety-Relevant Service Degraded
```

## 11.2 Customer / Citizen / Market

```text
BRE-CUS.00 Customer / Citizen / Market Consequence — reserved
BRE-CUS.11 Customer Account Closure
BRE-CUS.12 Customer Complaint Received
BRE-CUS.13 Customer Churn Spike Observed
BRE-CUS.14 Customer Compensation Event
BRE-CUS.15 Citizen Harm Case Opened
BRE-CUS.16 Vulnerable-Person Safeguarding Trigger
BRE-CUS.17 Market Confidence Event
```

Note: generalized "loss of trust" is measurement-shaped and SHOULD be represented as an Impact unless it is formalized as a discrete event by the organization.

## 11.3 Financial Event

```text
BRE-FIN.00 Financial Event — reserved
BRE-FIN.10 Authorized Payment Family — reserved
BRE-FIN.11 Authorized Push Payment Made
BRE-FIN.12 Authorized Crypto Transfer Made
BRE-FIN.13 Gift Card / Voucher Transfer Made
BRE-FIN.14 Cash Withdrawal Made
BRE-FIN.15 Goods or Services Paid but Not Received
BRE-FIN.16 Mule Transfer Executed
BRE-FIN.20 Unauthorized Payment Family — reserved
BRE-FIN.21 Unauthorized Bank Transfer Executed
BRE-FIN.22 Unauthorized Card Transaction Executed
BRE-FIN.23 Unauthorized Crypto Transfer Executed
BRE-FIN.24 Unauthorized Payroll Change Executed
BRE-FIN.25 Refund / Reimbursement Paid to Attacker
```

Note: "account takeover financial loss" is not a BRE. Account takeover belongs under BRE-ID; financial loss belongs under Impact.

## 11.4 Identity / Account Harm

```text
BRE-ID.00 Identity / Account Harm — reserved
BRE-ID.11 Personal Identity Misuse Event
BRE-ID.12 Social Media Account Takeover Harm
BRE-ID.13 Email Account Takeover Harm
BRE-ID.14 SIM-Swap Consequence
BRE-ID.15 Digital Identity Wallet Misuse
BRE-ID.16 Credential Abuse Consequence
BRE-ID.17 Impersonation-Driven Authorization
BRE-ID.18 Unauthorized Account Creation
BRE-ID.19 Account Recovery Lockout
```

Note: not every #4 Identity Theft step produces a BRE-ID. #4 against a **technical identity** (service account, API key, machine credential, Kerberos ticket, OAuth client secret) typically yields downstream BRE-SVC, BRE-FIN, BRE-DATA, or BRE-ORG consequences without any BRE-ID entry. BRE-ID is reserved for cases where a **human or organizational identity** is the harmed entity. Cause-side classification of the credential use remains #4 in both cases (per Axiom X / R-CRED); the consequence side records what actually happened to the business or citizen.

Example: a stolen service-account credential used to disable a payment processor records `… → #4 + [SRE] + [BRE: BRE-SVC.11 Payment Function Unavailable]` — no BRE-ID, because no human or organizational identity was the harmed entity.

## 11.5 Legal

```text
BRE-LGL.00 Legal Consequence — reserved
BRE-LGL.11 Customer Legal Claim
BRE-LGL.12 Class Action Filed
BRE-LGL.13 Contractual Claim by Counterparty
BRE-LGL.14 Litigation Settlement
BRE-LGL.15 Criminal Complaint Filed
BRE-LGL.16 Evidence Preservation Obligation
BRE-LGL.17 Insurance Claim Trigger
```

## 11.6 Regulatory / Supervisory

```text
BRE-REG.00 Regulatory Consequence — reserved
BRE-REG.11 Mandatory Notification Obligation Triggered
BRE-REG.12 Supervisory Inquiry Opened
BRE-REG.13 Fine / Sanction Imposed
BRE-REG.14 Remediation Order Issued
BRE-REG.15 License / Authorization Review Opened
BRE-REG.16 Regulatory Inspection Triggered
BRE-REG.17 Cross-Border Authority Notification Obligation
BRE-REG.18 Public Authority Warning Issued
```

## 11.7 Reputation / Public Communication

```text
BRE-REP.00 Reputation / Communication Event — reserved
BRE-REP.11 Public Warning Issued
BRE-REP.12 Media Escalation Occurred
BRE-REP.13 Executive Public Statement Issued
BRE-REP.14 Parliamentary / Political Attention Triggered
BRE-REP.15 Sector-Wide Alert Issued
BRE-REP.16 Public Correction / Clarification Issued
```

Note: "public confidence harm" is impact-shaped and belongs in IMPACT-REP.

## 11.8 Third-Party / Ecosystem Consequence

```text
BRE-3P.00 Third-Party / Ecosystem Consequence — reserved
BRE-3P.11 Supplier Service Failure Observed
BRE-3P.12 Managed Service Disruption Observed
BRE-3P.13 Cloud Dependency Failure Observed
BRE-3P.14 Payment Provider Disruption Observed
BRE-3P.15 Outsourcing Contract Breach Asserted
BRE-3P.16 Concentration-Risk Event Observed
BRE-3P.17 Sector Contagion Event Observed
```

## 11.9 Internal Organization

```text
BRE-ORG.00 Internal Organizational Consequence — reserved
BRE-ORG.11 Crisis Team Activated
BRE-ORG.12 Business Continuity Plan Activated
BRE-ORG.13 Disaster Recovery Invoked
BRE-ORG.14 Internal Investigation Opened
BRE-ORG.15 Board Notification Made
BRE-ORG.16 Control Remediation Program Opened
BRE-ORG.17 Staff Productivity Disruption Event
```

---

# 12. Impact Catalogue v0.2

Impacts measure the consequences of SREs, DREs, and BREs.

## 12.1 Financial

```text
IMPACT-FIN.00 Financial Impact — reserved
IMPACT-FIN.11 Lost Revenue
IMPACT-FIN.12 Direct Fraud Loss
IMPACT-FIN.13 Compensation Paid
IMPACT-FIN.14 Legal Cost
IMPACT-FIN.15 Regulatory Fine Amount
IMPACT-FIN.16 Customer Churn Loss
IMPACT-FIN.17 Recovery Cost
IMPACT-FIN.18 Incident Response Cost
IMPACT-FIN.19 Contractual Penalty
IMPACT-FIN.20 Insurance Deductible / Premium Impact
```

## 12.2 Operational

```text
IMPACT-OPS.00 Operational Impact — reserved
IMPACT-OPS.11 Downtime Duration
IMPACT-OPS.12 Transactions Delayed
IMPACT-OPS.13 Transactions Failed
IMPACT-OPS.14 Manual Workload Hours
IMPACT-OPS.15 Recovery Time
IMPACT-OPS.16 Recovery Point Loss
IMPACT-OPS.17 Service Degradation Duration
```

## 12.3 Customer / Citizen

```text
IMPACT-CUS.00 Customer / Citizen Impact — reserved
IMPACT-CUS.11 Number of Customers Affected
IMPACT-CUS.12 Number of Complaints
IMPACT-CUS.13 Number of Accounts Closed
IMPACT-CUS.14 Vulnerable Persons Affected
IMPACT-CUS.15 Customer Harm Severity
IMPACT-CUS.16 Number of Citizens Affected
```

## 12.4 Regulatory / Legal

```text
IMPACT-REG.00 Regulatory / Legal Impact — reserved
IMPACT-REG.11 Notification Count
IMPACT-REG.12 Jurisdictions Notified
IMPACT-REG.13 Supervisory Findings Count
IMPACT-REG.14 Enforcement Severity
IMPACT-REG.15 Number of Legal Claims
```

## 12.5 Reputation

```text
IMPACT-REP.00 Reputation Impact — reserved
IMPACT-REP.11 Media Articles
IMPACT-REP.12 Social Media Volume
IMPACT-REP.13 Sentiment Change
IMPACT-REP.14 Trust Index Change
IMPACT-REP.15 Public Confidence Indicator Change
```

## 12.6 Data / Resource

```text
IMPACT-DATA.00 Data / Resource Impact — reserved
IMPACT-DATA.11 Records Exposed
IMPACT-DATA.12 Records Modified
IMPACT-DATA.13 Records Rendered Inaccessible
IMPACT-DATA.14 Records Deleted / Unavailable
IMPACT-DATA.15 Systems Affected
IMPACT-DATA.16 Accounts Affected
```

---

# 13. Report Catalogue v0.2

REPORT codes describe procedural artefacts, reporting stages, or workflow states. They do not describe threats or BREs.

## 13.1 NCSC / CERT

```text
REPORT-NCSC.00 NCSC / CERT Reporting — reserved
REPORT-NCSC.11 Voluntary NCSC/CERT Report Filed
REPORT-NCSC.12 Mandatory NCSC/CERT Report Filed
REPORT-NCSC.13 Public Warning Candidate Flagged
REPORT-NCSC.14 Law-Enforcement Referral Candidate Flagged
REPORT-NCSC.15 Cross-Border CSIRT Sharing Candidate Flagged
REPORT-NCSC.16 Sector Alert Candidate Flagged
```

## 13.2 NIS2

```text
REPORT-NIS2.00 NIS2 Reporting — reserved
REPORT-NIS2.11 24h Early Warning Filed
REPORT-NIS2.12 72h Incident Notification Filed
REPORT-NIS2.13 Intermediate Report Filed
REPORT-NIS2.14 Final Report Filed
REPORT-NIS2.15 Cross-Border Impact Indication Filed
```

## 13.3 DORA

```text
REPORT-DORA.00 DORA Reporting — reserved
REPORT-DORA.11 Initial Notification Filed
REPORT-DORA.12 Intermediate Report Filed
REPORT-DORA.13 Final Report Filed
REPORT-DORA.14 Significant Cyber Threat Voluntary Notification Filed
REPORT-DORA.15 Major Operational or Security Payment-Related Incident Report Filed
```

## 13.4 Data Protection

```text
REPORT-DP.00 Data Protection Reporting — reserved
REPORT-DP.11 Data Protection Authority Notification Filed
REPORT-DP.12 Data Subject Notification Filed
REPORT-DP.13 Processor-to-Controller Notification Filed
```

---

# 14. Regulatory Anchoring

## 14.1 NCSC / CERT Needs

NCSCs and CERTs need to process three types of cases without conflating them:

```text
Core cyber incidents
Hybrid cyber-enabled harms
Pure #9-anchored digital crimes
```

TLCTC+ supports intake, triage, statistics, warning, and referral by separating:

```text
TLCTC cause path
SRE / DRE consequence
Pattern label
BRE chain
Impact measurement
Report workflow
```

## 14.2 NIS2 Direction

NIS2-style reporting needs incident severity, likely threat/root cause, impact, mitigation, and cross-border relevance.

TLCTC+ maps this as:

```text
Likely threat/root cause     → TLCTC path
System compromise            → SRE
Data impact                  → DRE
Business/service impact      → BRE chain
Measured severity            → Impact
Notification stages          → Report
Cross-border relevance       → BRE-REG / Report metadata
```

## 14.3 DORA Direction

DORA-style ICT incident reporting needs classification around affected clients, transactions, duration, downtime, geographical spread, data losses, criticality, and economic impact.

TLCTC+ maps this as:

```text
ICT/cyber cause              → TLCTC path
System compromise            → SRE
Data losses                  → DRE + IMPACT-DATA
Critical service impact      → BRE-SVC
Clients/transactions         → IMPACT-CUS / IMPACT-OPS
Economic impact              → IMPACT-FIN
Payment-related incidents    → BRE-SVC / BRE-FIN / REPORT-DORA
```

## 14.4 Basel / OpRisk Positioning

Basel-style OpRisk categories may be used as external mapping labels, but they are not the TLCTC+ grammar.

Example:

```text
External fraud
```

can arise from many TLCTC paths:

```text
#9
#9 → #4
#2 → #7
#5 → #4
#7 → #4
#10 → #7
```

Therefore, TLCTC+ MUST NOT reduce external fraud to #9. The TLCTC path records the cause; Pattern/BRE/Impact record the reporting consequence.

---

# 15. Data Model

## 15.1 Record Types

```text
core_cyber_incident
hybrid_cyber_enabled_harm
pure_9_digital_crime
```

No `non_cyber_oprisk_event` record type exists in TLCTC+ v0.3.

## 15.2 Required Metadata

```text
case_id
record_type
framework_version
tlctc_plus_version
intake_source
reporting_entity_type
sector
country
timestamp_reported
timestamp_detected
confidence
```

## 15.3 Cause Fields

```text
tlctc_path
tlctc_steps[]
patterns[]
evidence[]
actor_attribution_optional
```

## 15.4 SRE Fields

```text
sre_present
sre_status            (enum)
sre_timestamp
sre_description
sre_scope
linked_to_step
confidence
```

`sre_status` enum: `observed | confirmed | disputed | retracted | hypothesized`. Use `hypothesized` for pre-compromise attack-path records (§8.2 grammar note) where the SRE is asserted as the projected outcome of the cause path but not yet realized.

## 15.5 DRE Fields

```text
dre_type
dre_status
affected_data_or_resource
scope
timestamp_observed
linked_to_step
linked_to_sre
confidence
```

## 15.6 BRE Fields

```text
bre_code
bre_label
bre_status            (enum)
bre_parent
bre_operator          (enum)
bre_timestamp
linked_to_dre
linked_to_sre
linked_to_step
confidence
```

`bre_status` enum: `observed | confirmed | disputed | retracted | open`. `open` indicates a BRE that has been triggered but whose downstream resolution (settlement, claim outcome, regulatory finding) is not yet known.

`bre_operator` enum: `→ | +`. Indicates the relationship of this BRE to its `bre_parent` (sequential causality vs parallel co-realization). The root BRE in a chain has neither a `bre_parent` nor a `bre_operator`.

## 15.7 Pattern Fields

```text
pattern_code
pattern_label
pattern_family
linked_to_step
channel
narrative
confidence
national_alias
```

## 15.8 Impact Fields

```text
impact_code
impact_label
amount
currency
unit
estimate_type
timestamp
linked_to_bre
linked_to_dre
linked_to_sre
confidence
```

## 15.9 Report Fields

```text
report_code
report_label
reporting_regime
stage
timestamp_due
timestamp_filed
authority
status
linked_to_bre_reg
linked_to_sre
linked_to_dre
```

---

# 16. Example JSON Records

## 16.1 Core Cyber Incident

```json
{
  "case_id": "case-001",
  "record_type": "core_cyber_incident",
  "tlctc_plus_version": "0.3",
  "tlctc_path": "#9 ||[email][@External→@Org]|| → #7",
  "sre": {
    "present": true,
    "status": "confirmed",
    "linked_to_step": "step-2",
    "description": "Endpoint compromised through executed foreign executable content"
  },
  "dre": [
    {
      "type": "Ac",
      "linked_to_sre": true,
      "affected_resource": "file shares"
    }
  ],
  "bre_chain": {
    "expression": "BRE-SVC.11 → BRE-ORG.12",
    "nodes": [
      {
        "code": "BRE-SVC.11",
        "label": "Payment Function Unavailable"
      },
      {
        "code": "BRE-ORG.12",
        "label": "Business Continuity Plan Activated"
      }
    ]
  },
  "impact": [
    {
      "code": "IMPACT-OPS.11",
      "label": "Downtime Duration",
      "value": 6,
      "unit": "hours"
    }
  ]
}
```

## 16.2 Pure #9 Digital Crime

```json
{
  "case_id": "case-002",
  "record_type": "pure_9_digital_crime",
  "tlctc_plus_version": "0.3",
  "tlctc_anchor": "#9 ||[messaging][@External→@Citizen]||",
  "patterns": [
    {
      "code": "PATTERN-FIN.11",
      "label": "Romance / Relationship Scam",
      "linked_to_step": "step-1"
    }
  ],
  "sre": {
    "present": false
  },
  "dre": [],
  "bre_chain": {
    "expression": "BRE-FIN.11",
    "nodes": [
      {
        "code": "BRE-FIN.11",
        "label": "Authorized Push Payment Made"
      }
    ]
  },
  "impact": [
    {
      "code": "IMPACT-FIN.12",
      "label": "Direct Fraud Loss",
      "amount": 4500,
      "currency": "CHF"
    }
  ],
  "report": [
    {
      "code": "REPORT-NCSC.11",
      "label": "Voluntary NCSC/CERT Report Filed"
    }
  ]
}
```

## 16.3 BEC / Invoice Fraud After Credential Capture

```json
{
  "case_id": "case-003",
  "record_type": "hybrid_cyber_enabled_harm",
  "tlctc_plus_version": "0.3",
  "tlctc_path": "#9 ||[email][@External→@Org]|| + [DRE: C] → #4",
  "patterns": [
    {
      "code": "PATTERN-FIN.22",
      "label": "Invoice / Mandate Fraud"
    }
  ],
  "sre": {
    "present": true,
    "status": "confirmed",
    "linked_to_step": "step-2",
    "description": "Mailbox accessed using captured credentials"
  },
  "dre": [
    {
      "type": "C",
      "linked_to_step": "step-1",
      "description": "Credential disclosed through social engineering"
    }
  ],
  "bre_chain": {
    "expression": "BRE-ID.13 → BRE-FIN.11",
    "nodes": [
      {
        "code": "BRE-ID.13",
        "label": "Email Account Takeover Harm"
      },
      {
        "code": "BRE-FIN.11",
        "label": "Authorized Push Payment Made"
      }
    ]
  },
  "impact": [
    {
      "code": "IMPACT-FIN.12",
      "label": "Direct Fraud Loss",
      "amount": 80000,
      "currency": "EUR"
    }
  ]
}
```

---

# 17. Worked Examples

## 17.1 Romance Scam, No Cyber Compromise

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

No SRE. No DRE. The boundary operator on #9 is REQUIRED per R-9-BOUNDARY.

## 17.2 Investment Scam With Account Takeover (Attacker-Executed Transfer)

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.12 Investment / Crypto-Investment Scam]
+ [DRE: C] → #4 + [SRE]
+ [BRE: BRE-ID.13 Email Account Takeover Harm → BRE-FIN.23 Unauthorized Crypto Transfer Executed]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 30,000]
```

Credential acquisition is caused by #9; credential use is #4 (Axiom X / R-CRED). The attacker uses the taken-over account to execute the transfer — the BRE is therefore **unauthorized** (BRE-FIN.23), not BRE-FIN.12.

**Contrast — victim-authorized variant** (no account takeover; victim is induced to transfer crypto themselves through their own banking interface):

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.12 Investment / Crypto-Investment Scam]
+ [BRE: BRE-FIN.12 Authorized Crypto Transfer Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 30,000]
```

The authorized vs unauthorized distinction matters for fraud statistics (it affects which liability and reimbursement regimes apply) and is captured directly by the BRE-FIN.10 (authorized) vs BRE-FIN.20 (unauthorized) family split in §11.3.

## 17.3 Ransomware-Driven Payment Outage

```text
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: Ac]
+ [BRE: BRE-SVC.11 Payment Function Unavailable
   → (BRE-CUS.11 Customer Account Closure + BRE-LGL.11 Customer Legal Claim)]
+ [Impact: IMPACT-FIN.16 Customer Churn Loss + IMPACT-FIN.14 Legal Cost]
```

Ransomware is not the threat cluster. The causal path is #9 → #7. The DRE is Loss of Accessibility.

## 17.4 Supply-Chain Incident With Regulatory Reporting

```text
#10 ||[update][@Vendor→@Org]|| → #7 + [SRE] + [DRE: C + I]
+ [BRE: BRE-REG.11 Mandatory Notification Obligation Triggered
   → BRE-REG.17 Cross-Border Authority Notification Obligation]
+ [Report: REPORT-NIS2.11 + REPORT-NIS2.12 + REPORT-NIS2.14]
```

## 17.5 Fake Tech Support Without Code Execution

```text
#9 ||[phone][@External→@Citizen]|| [Pattern: PATTERN-FIN.13 Fake Tech Support Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 900]
```

No SRE, no DRE, no #7.

## 17.6 Fake Tech Support With Remote Tool Execution

```text
#9 ||[phone][@External→@Citizen]|| [Pattern: PATTERN-FIN.13 Fake Tech Support Scam] → #7 + [SRE]
+ [BRE: BRE-ID.13 Email Account Takeover Harm → BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss]
```

The #7 step exists only if foreign executable content executes. If the victim merely makes a payment through their own banking interface without attacker-controlled code execution or credential use, the case remains pure #9 with a BRE.

## 17.7 Fake Tech Support With Legitimate Remote-Access Function Abuse

```text
#9 ||[phone][@External→@Citizen]|| [Pattern: PATTERN-FIN.13 Fake Tech Support Scam] → #1
+ [SRE]
+ [BRE: BRE-ID.13 Email Account Takeover Harm]
```

Use #1 only when the attacker or victim misuses a legitimate software capability in a way that gives the attacker functional control or operational advantage without an implementation flaw and without FEC execution. If a remote-access tool is installed or executed as attacker-provided foreign executable content, record #7.

## 17.8 Service-Account Compromise Causing Payment-Service Outage (Technical Identity)

```text
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: C]
→ #4 → #1 + [BRE: BRE-SVC.11 Payment Function Unavailable
   → BRE-ORG.12 Business Continuity Plan Activated]
+ [Impact: IMPACT-OPS.11 Downtime Duration = 4 hours
   + IMPACT-FIN.11 Lost Revenue = EUR 180,000]
```

The credential stolen was a **technical identity** — a payment-platform service-account credential discovered in the engineer's saved-secrets store after the workstation was compromised. Cause-side classification of the credential use is still `#4` (Axiom X / R-CRED applies regardless of whether the identity is human, organizational, or technical). The attacker then abuses legitimate operator functions on the payment service to take it offline (`#1`).

The downstream BRE chain contains **no BRE-ID** entry. No human or organizational identity is the harmed entity — the harmed entity is the payment service itself. Compare §17.2 and §17.6, which both record `BRE-ID.13 Email Account Takeover Harm` because there a personal email account is the harmed identity. See §11.4 note and §3.9.

---

# 18. Decision Procedure

## Step 1 — Is there a TLCTC cyber cause path?

If yes, classify each step using core TLCTC.

```text
#1–#10
```

If no, proceed to Step 2.

## Step 2 — Is there a pure #9 digital-harm anchor?

If a human was psychologically manipulated through a digital channel, record:

```text
#9
```

Then attach Pattern, BRE, and Impact as needed.

If there is no TLCTC path and no #9 anchor, the case is outside TLCTC+.

## Step 3 — Did Loss of Control / System Compromise occur?

If yes, attach:

```text
+ [SRE]
```

If no and the case is pure #9 digital harm, omit SRE.

## Step 4 — Did a DRE occur?

Attach as appropriate:

```text
+ [DRE: C]
+ [DRE: I]
+ [DRE: Ac]
+ [DRE: Av]
```

## Step 5 — Is there a scam/fraud/crime pattern label?

Attach as Pattern metadata:

```text
[Pattern: PATTERN-FIN.11]
```

## Step 6 — Did a business/citizen/regulatory event occur?

Attach BRE chain:

```text
+ [BRE: BRE-FIN.11 → BRE-LGL.11]
```

## Step 7 — Can the harm be measured?

Attach Impact:

```text
+ [Impact: IMPACT-FIN.12 = EUR 50,000]
```

## Step 8 — Was a report filed or required?

Attach Report artefact:

```text
+ [Report: REPORT-NCSC.11]
```

If a legal obligation was triggered, also attach the regulatory BRE:

```text
+ [BRE: BRE-REG.11]
+ [Report: REPORT-NIS2.11]
```

---

# 19. Conformance

A TLCTC+ v0.3 record is conformant if:

1. It uses a TLCTC path or #9 anchor.
2. It does not introduce new TLCTC top-level clusters.
3. It records SRE explicitly when Loss of Control / System Compromise has occurred (per R-SRE).
4. It omits SRE only in one of two cases:
   a. **Pure #9 digital harm** — no IT system was compromised (per R-SRE-OPTIONAL-9). A DRE MAY appear on the #9 step when the social-engineering act itself directly causes data disclosure, modification, inaccessibility, or unavailability without system compromise (e.g., `+ [DRE: C]` for credential or PII handover during phishing). If the disclosed artifact is later used, the record transitions to a hybrid case under §3.4 / §5.4.
   b. **Pre-compromise hypothesis record** — the record represents a projected attack path before realization, in which case `sre_status` SHOULD be set to `hypothesized` (per §15.4 and the §8.2 grammar note).
5. It records DREs as `+ [DRE: ...]`, not as path steps.
6. It records BREs as `+ [BRE: ...]`, not as path steps.
7. It records scam/fraud/crime labels as `Pattern`, not as BREs (per R-PATTERN-SPLIT).
8. It records Pattern annotations in bracket-only form (no `+`) and SRE/DRE/BRE/Impact/Report annotations in additive form (`+ [...]`) (per R-PATTERN-POSITION).
9. It records measured harm as `Impact`, not as BREs.
10. It keeps REPORT codes outside the BRE chain.
11. It does not use ORE notation.
12. It does not classify non-cyber operational failures.
13. It includes a v2.1 boundary operator on every bridge-cluster step (#8, #9, #10), including pure-#9 anchors (per R-9-BOUNDARY).
14. It uses no free-text BRE labels — every BRE is a structured code from §11 (per R-V01-MIGRATION).
15. Stripping all consequence-side annotations recovers a valid TLCTC v2.1 path or #9 anchor (per R-RECOVERABILITY).
16. Consequence-side BRE families are recorded from observed harm, not auto-derived from cause-side cluster identity (per R-CAUSE-CONSEQUENCE-INDEPENDENCE).

---

# 20. Future Architecture

The following catalogues are embedded in TLCTC+ for practical NCSC/CERT use:

```text
BRE Catalogue
Impact Catalogue
Report Catalogue
```

They are candidates for extraction into a shared consequence-side specification once TLSFC reaches publication readiness.

Target future architecture:

```text
TLCTC  ─┐
        ├─→ Shared Consequence Catalogue
TLSFC  ─┘
```

In that future architecture:

- TLCTC+ would remain the TLCTC-anchored digital-harm profile.
- TLSFC+ or a comparable profile would handle non-adversarial software/system failure.
- The shared consequence catalogue would provide common BRE, Impact, and Report codes across both.

---

# 21. Changelog

## 21.1 Changes from v0.1 to v0.2

1. Added explicit `SRE` node.
2. Removed non-cyber OpRisk event scope.
3. Removed ORE notation.
4. Removed ORE catalogue.
5. Added explicit three-case scope.
6. Added PATTERN namespace.
7. Split scam/fraud patterns from BRE events.
8. Changed BRE-FIN entries from playbook labels to event labels.
9. Removed Account-Takeover Financial Loss as BRE; replaced with BRE-ID plus IMPACT-FIN.
10. Fixed BRE grammar to support arbitrary sequential and parallel chains.
11. Renamed "Layer" terminology to "Track".
12. Clarified REPORT vs BRE-REG.
13. Added R-SRE, R-SRE-OPTIONAL-9, R-DRE-PLACEMENT, R-PATTERN-SPLIT, R-REPORT.
14. Qualified OpRisk positioning: OpRisk may consume TLCTC+ for cyber/digital-crime cases only.
15. Marked BRE / Impact / Report catalogues as extraction candidates for a future shared consequence-side specification.

---

## 21.2 Changes from v0.2 to v0.3

1. Added §3.8 **Pattern Annotation Position** — justifies why Pattern uses bracket-only form (`[Pattern: ...]`) while SRE/DRE/BRE/Impact/Report use additive form (`+ [...]`). Pattern is cause-side metadata; the others are consequence-side events.
2. Split §4 Tracks from five into **six tracks** — SRE Track and DRE Track are now separate, aligning with §15.4 / §15.5 data-model field groups.
3. Restored legacy `A` letter in DRE grammar (§8.6) as a deprecated alias for `Av`/`Ac` general — preserves backward compatibility with the existing v2.1 attack-path corpus and CLAUDE.md notation.
4. Added §6.1 **Editorial convention** — short syntax snippets in §3, §6, §7, §8 may omit boundary operators for readability; worked examples (§5, §16, §17) are fully conformant.
5. Added explicit scope note in §6.4 — the `→` operator inside `[BRE: ...]` is parser-distinguishable from the cause-side path operator via bracket fencing.
6. Added §6.5 clarification — boundary operator precedes Pattern annotation on bridge-cluster steps.
7. Added four new normative rules in §7:
   - **R-PATTERN-POSITION** — Pattern is bracket-only; SRE/DRE/BRE/Impact/Report are additive; mixing the two forms is a conformance error.
   - **R-9-BOUNDARY** — pure #9 records MUST carry the v2.1 boundary operator. SRE optionality does not relax bridge-cluster boundary semantics.
   - **R-BRE-OP-SCOPE** — `→` and `+` semantics are scoped to bracket fencing; cluster references and BRE codes never mix scopes.
   - **R-V01-MIGRATION** — explicit migration path from v0.1 free-text BRE labels to v0.3 Pattern + structured BRE.
8. Added `sre_status` enum (§15.4): `observed | confirmed | disputed | retracted | hypothesized` — supports pre-compromise attack-path records.
9. Added `bre_status` enum (§15.6): `observed | confirmed | disputed | retracted | open` — `open` for triggered-but-unresolved consequences.
10. Added `bre_operator` enum (§15.6): `→ | +` — explicit JSON-side encoding of the BRE-chain operator.
11. Added boundary operators to all #9 examples in §5 Core Chain Models and §17 Worked Examples, making them fully v2.1-conformant.
12. Tightened §19 Conformance:
    - SRE-omission rule split into two cases (pure #9 vs pre-compromise hypothesis).
    - Added conformance items for Pattern annotation form, R-9-BOUNDARY, and free-text BRE prohibition (R-V01-MIGRATION).
    - Re-anchored R-RECOVERABILITY clause on v2.1 path validity, including bridge-cluster boundary operators.
13. Bumped record schema reference from "TLCTC+ v0.2" to "TLCTC+ v0.3" in the title block.
14. **§0.1 Document and Catalogue Versions** — added an explicit version table separating document version (v0.3) from catalogue version (v0.2).
15. **§1.3 / §3.4 / §5.4 / §17.1** — refined pure-#9 DRE policy. A DRE MAY be recorded on a pure-#9 step when the social-engineering act itself directly causes data disclosure (typically `+ [DRE: C]`); this captures phishing-with-credential-disclosure cases that have not yet progressed to credential use. If credential use follows, the record transitions to hybrid form `→ #4 + [SRE]`.
16. **§7 R-9-BOUNDARY reworded** — explicitly framed as a TLCTC+ profile strengthening of the v2.1 baseline, not a silent rewrite of core TLCTC. v2.1 establishes the boundary-operator notation; TLCTC+ tightens the conformance level from SHOULD to MUST for reporting purposes.
17. **§8.3 / §8.4 grammar repaired** — `<pure-9-record>` now requires `<boundary-annotation>` and admits an optional `<dre-annotation>`. `<tlctc-path>` extended to support `<tlctc-step>` with boundary, intra-system, and step annotations (Pattern, conf, inferred, Δt). `<boundary-annotation>` production added in §8.4a for self-containment.
18. **§16 JSON examples** — added boundary operators to `tlctc_path` / `tlctc_anchor` fields in 16.1, 16.2, 16.3. Added `sre.status` field. All examples are fully v0.3-conformant.
19. **§17.2 corrected** — Investment-scam-with-account-takeover example now uses `BRE-FIN.23 Unauthorized Crypto Transfer Executed` (attacker-executed transfer through taken-over account) instead of `BRE-FIN.12 Authorized Crypto Transfer Made`. A contrasting victim-authorized variant added inline to clarify the authorized-vs-unauthorized distinction (which matters for fraud statistics and reimbursement-regime classification).
20. **§19 conformance item 4** — refined to allow DRE-without-SRE on pure-#9 steps for direct disclosure cases.
21. **§21 changelog restructure** — flat `# 21` and `# 21a` headings replaced by `# 21. Changelog` with `## 21.1` and `## 21.2` subsections.
22. **Cause/consequence independence made explicit** — added §3.9 design principle, §7 R-CAUSE-CONSEQUENCE-INDEPENDENCE rule, §11.4 note distinguishing technical from human/organizational identities, §17.8 worked example (service-account compromise causing payment outage with no BRE-ID), §19 conformance item 16, and §22 glossary entry for **Technical Identity**. Clarifies that `#4` against a technical identity does not produce a BRE-ID, and that cause-side cluster and consequence-side BRE family are independent dimensions across all clusters.

**Non-changes (v0.2 decisions retained in v0.3):**

- The 10 TLCTC clusters remain unchanged.
- The three case classes (`core_cyber_incident`, `hybrid_cyber_enabled_harm`, `pure_9_digital_crime`) remain unchanged.
- The PATTERN, BRE, IMPACT, REPORT catalogues are unchanged in structure (no codes added, removed, or renumbered).
- TLSFC remains a forward reference; no TLSFC artefacts are introduced.
- The "Tracks not Layers" terminology choice is retained.

---

# 22. Glossary

## BRE — Business Risk Event

A discrete, observable business-level event on the consequence side.

## DRE — Data Risk Event

Loss of Confidentiality, Integrity, Accessibility, or Availability.

## Impact

A quantified or qualified measurement attached to SRE, DRE, or BRE.

## Pattern

A cause-side narrative, scam label, fraud playbook, or reporting label that describes how manipulation or cyber-enabled harm was framed.

## REPORT

A procedural artefact, report filing, workflow stage, or regulatory communication state.

## SRE — System Risk Event

Loss of Control / System Compromise. The cyber Bow-Tie central event.

## Technical Identity

A non-human credential or principal: service account, API key, machine credential, Kerberos service ticket, OAuth client secret, certificate, robot/RPA account. Distinct from a *human or organizational identity* (a person, a customer account, an employee mailbox, a corporate brand). Cause-side classification of the credential use is `#4` Identity Theft regardless (per R-CRED), but the consequence-side BRE typically falls outside BRE-ID. See §11.4 note, §3.9, and §17.8.

## TLCTC+

A TLCTC-anchored digital-harm reporting profile for NCSCs, CERTs, and regulators.

---

# 23. One-Sentence Definition

**TLCTC+ is the TLCTC-anchored reporting grammar that connects cyber causes and #9 digital-harm anchors to explicit SRE, DRE, BRE, Impact, Pattern, and Report structures without turning consequences, scams, crimes, or reporting duties into threat clusters.**
