# TLCTC+ Specification v0.9

## TLCTC-Anchored Digital-Harm Reporting Extension for NCSCs, CERTs, Regulators, and Financial-Crime Reporting

**Author:** Bernhard Kreinz  
**Base framework:** TLCTC v2.7 (dictionary `tlctc-framework.v2.7.json`, `tlctc_version` 2.7; core paper v2.7, DOI 10.5281/zenodo.23437984)  
**Extension version:** TLCTC+ v0.9  
**Status:** Draft for peer review  
**License:** CC BY 4.0  
**Core thesis:** Keep TLCTC pure. Extend the reporting layer.

> **v0.9 intent:** Re-based TLCTC+ from TLCTC v2.5.1 to TLCTC v2.7, and added a third record type for near misses. Both core releases are classification-preserving: no existing record type, catalogue code or track changes, and every v0.8 record stays valid after its version fields are updated. From v2.6: a cluster step is recorded only if it succeeded (§4.3). A reported lure nobody acted on, or a blocked attempt, is therefore not an incident; but the attacker did act, and the application companion counts such events as **near misses** per cluster (its §10, Key Risk Indicators). v0.9 gives them a record of their own, the `near_miss_record` (§4.4), written `[Attempt: …]` so that the attempted step is an annotation, never a path step; it carries no SRE, DRE, BRE or Impact and never enters incident statistics. Where a path stopped because a later step was averted, `averted_next` names that step. Also from v2.6: #10 requires that the trusted third party or its artifact was subverted before acceptance (R-SUPPLY). From v2.7: a BRE is reached by a **causal** edge (brought about, after a Δt) or a **normative** edge (a duty arises or a norm is violated, no Δt); a statutory deadline such as the NIS2 24-hour early warning bounds the separate response process from awareness and is never a Δt; a BRE entered directly by a normative edge, with no cluster before it, is compliance risk outside TLCTC+; and the DRE stopping rule uses the v2.7 wording. The BRE edge kind is recorded in the data model (§17.6), not in the notation. The grammar gains one production, the near-miss record; the other productions are unchanged.
>
> **v0.8 intent (retained):** Three sharpenings of v0.7, none of which changes a record type, a catalogue code, or a track. (1) The record-type split is restated as a distinction between two **SRE kinds** — *direct* (any non-#9 step, #8 and #10 included: the system itself leaves its owner's control) and *induced* (#9: the departure is exercised through the manipulated person's action) — replacing the v0.7 wording "technical step vs. reached a person", which misdescribed the bridge clusters. (2) `+ [SRE]` becomes a deterministic **first-direct-SRE marker**, computable from the path; the v0.7 "decisive compromise" conflated the ontic position of a compromise with the reporting choice of which compromise a record foregrounds, and that choice now lives in its own field, `reporting_pivot_step`. (3) The minimal grammar is restructured so that SRE, DRE and Pattern are annotations of a step inside the path rather than tokens that syntactically follow the path; validator constraints V-1…V-6 are listed explicitly.
>
> **v0.7 intent (retained):** Re-based TLCTC+ from TLCTC v2.1 to TLCTC v2.5.1. Core v2.5.1 (§3.4) makes explicit that **every cluster step records its own System Risk Event** — including #9 — so a record type defined by "SRE absent" is no longer expressible. The two record types were kept, with the split moved from *SRE presence* to *path composition*. The DRE tree was aligned to the v2.5 refinements (`Ii`/`If`, `Av`/`Ac`), the cause-side partition (R-SCOPE) adopted as the scope boundary, and the R-CRED self-issued-identity proviso carried into the credential examples.
>
> **v0.6 intent (retained):** Collapsed the v0.5 three-case-class model into two structurally distinct record types (`compromise_record` and `pure_9_record`), aligning the prose with the formal grammar in §10. The former "Core" vs "Hybrid" split is retained only as descriptive language.

---

## 0. One-Sentence Definition

**TLCTC+ is a TLCTC-anchored reporting grammar that connects cyber causes and #9 digital-harm anchors to explicit SRE, DRE, Pattern, BRE, Impact, and Report structures without turning consequences, scams, crimes, actors, or reporting duties into threat clusters.**

---

## 1. Executive Summary

TLCTC+ is a reporting extension for cases that have a TLCTC anchor.

It supports two structurally distinct incident realities, split on the composition of the TLCTC path, and one record for the attacks that did not succeed:

1. **Compromise records** — a TLCTC attack path contains at least one cluster step other than #9, i.e. at least one **direct SRE**: the system itself is made to behave outside its owner's control (a function abused, a flaw exploited, a credential applied, a path intercepted, capacity exhausted, content executed, hardware reached, a trust artifact accepted). This single class covers cases historically described as "core cyber incidents" (cyber-side reporting interest, BRE-SVC.* / BRE-DATA.* / BRE-REG.* dominant) and "hybrid cyber-enabled harms" (consequence-side reporting interest, BRE-FIN.* / BRE-ENT.* / BRE-CUS.* dominant). The structural reality — a TLCTC path containing a direct SRE — is the same; the difference is downstream consequence dominance, captured in the BRE family selection.
2. **Pure #9-anchored digital-harm records** — the path is a single #9 step: the case is digitally mediated and manipulation-driven, and no IT system is compromised by the attacker directly. Per core §3.4 the #9 step still records a System Risk Event — the loss of control lands on the system the manipulated person operates, exercised through the victim's own action — but this SRE is **induced**, not direct: no step made a system misbehave; a person was made to act. No `+ [SRE]` marker is rendered.
3. **Near-miss records** (v0.9) — the attacker acted, but no step succeeded because a control held: a lure delivered and reported without anyone acting on it, a campaign filtered before delivery, an exploit blocked. The attempted step is written inside `[Attempt: …]` and is not a path step; the record carries no SRE, DRE, BRE or Impact. Near misses are counted per cluster for Key Risk Indicators and never as incidents. For national centres they are usually the largest share of citizen reports.

Under TLCTC (since v2.5.1, unchanged in v2.7) "no SRE" means "no cluster" (Failure, Error in Use, Abuse of Rights — see §5). An incident record therefore always has at least one SRE; what distinguishes the two incident record types is the kind of SRE the path contains — direct system-level loss of control versus manipulation-induced loss of control. The distinction is between two SRE kinds, not between "technical" and "human" steps: #8 and #10 are bridge clusters, and both produce direct SREs.

The phrase "hybrid cyber-enabled fraud" remains a useful descriptor for compromise records with consequence-side dominance, but it is not a separate record type.

TLCTC+ is not a new threat taxonomy. It does not add an eleventh cluster. It does not redefine ransomware, romance scams, account takeover, payment fraud, data breach, or outage as threats. Those are labels, outcomes, or reporting categories. The cause-side threat remains the TLCTC path.

TLCTC+ adds a controlled reporting grammar around the TLCTC path:

```text
TLCTC cause path
+ [SRE]
+ [DRE: C|I|Ii|If|A|Av|Ac]
[Pattern: ...]
+ [BRE: ...]
+ [Impact: ...]
+ [Report: ...]
```

Pattern is cause-side metadata and uses bracket-only notation. SRE, DRE, BRE, Impact, and Report are event or consequence annotations and use additive notation. `+ [SRE]` marks the first direct SRE; every cluster step records its own SRE whether or not the marker is rendered (§8.2).

A near miss has no path, and its record says so in its first token:

```text
[Attempt: #X ...]
[Pattern: ...]
+ [Report: ...]
```

---

## 2. Why Peer Groups Should Care

### 2.1 NCSCs, CERTs, and CSIRTs

NCSCs and CERTs receive heterogeneous reports: malware, outages, phishing, account takeover, romance scams, payment diversion, ransomware, supplier incidents, and citizen harm. TLCTC+ lets them keep one intake grammar without pretending all of these are the same type of event.

**Value:** cleaner triage, better national statistics, stronger warning products, and clearer referral logic between cyber, fraud, consumer-protection, and law-enforcement workflows.

### 2.2 Financial Regulators, Central Banks, and Supervisors

Payment fraud and ICT incidents are often reported through impact categories, authorization status, and procedural reporting stages. TLCTC+ separates the cause path from the fraud/event label and the measured impact.

**Value:** compatible fraud reporting without losing root-cause clarity; better distinction between victim-authorized payments, attacker-executed transactions, system compromise, and pure manipulation.

### 2.3 Banks, PSPs, Fintechs, and Fraud Teams

Fraud teams need labels such as APP fraud, invoice fraud, CEO fraud, mule recruitment, and fake support scams. Security teams need TLCTC cause paths. Risk teams need impact, loss, and obligation data.

**Value:** one case record can serve fraud operations, cyber security, operational risk, compliance, and management reporting without flattening all semantics into “external fraud.”

### 2.4 SOC, CTI, and Incident Response Teams

SOC and CTI teams need cause-side attack paths, not only business labels. A "BEC case" may be a `pure_9_record` (#9 only, no IT system compromised by the attacker), a `compromise_record` dominated by BRE-FIN.* (cyber-enabled fraud, formerly "hybrid"), or a `compromise_record` dominated by BRE-SVC.* (operational impact, formerly "core") — depending on the actual chain (#9, #9 + DRE:C, #9 → #4, #9 → #7, or #10 → #7).

**Value:** investigation and detection remain tied to real attack steps; indicators and controls map to the cause lane, not to the reporting label.

### 2.5 GRC, Operational Risk, and Enterprise Risk Management

Operational-risk taxonomies often consume loss-event and consequence labels. TLCTC+ provides the cyber/digital-harm portion while explicitly excluding the three non-cyber rows of the cause-side partition (Failure / external event, Error in Use, Abuse of Rights — core §3.5, R-SCOPE). Internal fraud inside a conferred mandate is Abuse of Rights, not #1, and is out of TLCTC+ scope even when the consequence looks identical to a cyber-enabled fraud.

**Value:** better bridge between cyber risk and OpRisk without forcing cyber threats into broad loss-event buckets.

### 2.6 Law Enforcement and Fraud / Financial-Crime Units

Law-enforcement categories are legal and investigative categories. TLCTC+ does not replace them. It gives a technical-causal and reporting structure that can coexist with criminal-law labels.

**Value:** clearer distinction between manipulation narrative, identity compromise, transaction event, loss amount, and reporting/referral status.

### 2.7 Insurers, Actuaries, and Loss Modelers

Loss modeling needs consistent separation between cause, event, consequence, and measurement.

**Value:** better scenario construction, cleaner aggregation, and fewer ambiguous labels such as “ransomware loss” or “fraud loss” that hide different causal paths.

### 2.8 Standards Bodies, Researchers, and Framework Designers

Existing frameworks often mix causes, outcomes, actors, and control failures. TLCTC+ demonstrates how to extend reporting semantics without mutating the underlying threat taxonomy.

**Value:** a reusable grammar for harmonization work, comparative reporting, and empirical incident datasets.

---

## 3. Version and Catalogue Status

```text
Specification document version:   TLCTC+ v0.9
Base framework:                   TLCTC v2.7 (dictionary tlctc_version 2.7)
PATTERN catalogue version:        v0.2
BRE catalogue version:            v0.4   (2026-11-05: adds the BRE-DATA family, §13.10)
IMPACT catalogue version:         v0.2
REPORT catalogue version:         v0.2
```

BRE catalogue v0.4 is a catalogue release within TLCTC+ v0.9: the catalogues are versioned independently of the document. It adds the `BRE-DATA` family, which earlier versions named (§4.1.1, §13.4) without cataloguing, and five catalogue rules for it (D-1…D-5). No existing code is changed, renumbered or removed, and no grammar production changes: `BRE-DATA.11` already parses as a BRE code. Every v0.9 record stays valid.

v0.9 re-bases the profile from TLCTC v2.5.1 to TLCTC v2.7, carries the v2.6 and v2.7 doctrine that a reporting profile must state (successful steps only, the subversion test for #10, causal and normative BRE edges, deadlines from awareness), and adds the `near_miss_record`. v0.8 sharpened the v0.7 re-base (direct/induced SRE kinds, deterministic marker plus `reporting_pivot_step`, step-level grammar); v0.7 re-based the profile from TLCTC v2.1 to TLCTC v2.5.1 and changed the record-type split criterion from SRE presence to path composition (see the intent boxes and §23). None of them adds, removes, or renumbers catalogue entries. The v0.5 catalogue decisions remain in force.

`framework_version` in a v0.9 record is `"2.7"`. Because v2.6 and v2.7 preserve every v2.5.1 classification, a v0.8 record (`"2.5.1"`) stays readable; it is converted by changing the two version fields and checking it against §4.3 and R-BRE-EDGE. The v2.3 and v2.4 dictionaries are frozen records; v0.9 records MUST NOT declare them.

---

## 4. Scope

TLCTC+ covers exactly three record types: two incident record types, split on the composition of the TLCTC path (§4.1, §4.2), and the near-miss record for attacks in which no step succeeded (§4.4). Under the core (since v2.5.1, unchanged in v2.7) every cluster step records an SRE, so the split cannot be "SRE present / absent"; it is the **kind** of SRE the path contains. Every non-#9 cluster step records a *direct* SRE — the system itself departs from its owner's control. A #9 step records an *induced* SRE — the departure is exercised through the manipulated person's own action. Bridge topology is not the criterion: #8 and #10 are bridge clusters and produce direct SREs.

### 4.1 Compromise Record

The TLCTC path contains at least one non-#9 cluster step, hence at least one direct SRE. The **first direct SRE** in path order is marked `+ [SRE]` (status `observed`, `confirmed`, `disputed`, or `retracted`; epistemic uncertainty about the step itself is expressed on the step per core §7.7, not by omitting the marker). The marker is an ontic statement — *here the system first left its owner's control* — and is fully determined by the path. Which compromise a record chooses to foreground for reporting is a separate, representational choice recorded in `reporting_pivot_step` (§17.4), never in the marker.

Canonical chain:

```text
TLCTC path (n steps, n SREs) → first direct SRE → DRE* → BRE* → Impact* → Report*
```

This single class covers two reporting flavors that are structurally identical:

**4.1.1 Cyber-side dominance** (formerly "core cyber incident") — the reporting interest is technical compromise, service impact, or regulatory notification. Dominant BRE families: BRE-SVC.*, BRE-DATA.*, BRE-REG.*, BRE-ORG.*.

```text
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: Ac]
+ [BRE: BRE-SVC.11 Payment Function Unavailable]
```

**4.1.2 Consequence-side dominance** (formerly "hybrid cyber-enabled harm") — the reporting interest is fraud, citizen harm, identity harm, or downstream financial consequence. Dominant BRE families: BRE-FIN.*, BRE-ENT.*, BRE-CUS.*.

```text
#9 ||[email][@External→@Org]|| [Pattern: PATTERN-ID.11 Phishing for Credentials]
+ [DRE: C] → #4 + [SRE]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm → BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 80,000]
```

The 4.1.1 / 4.1.2 distinction is descriptive, not normative. Both are `record_type = compromise_record`. The dominant BRE family is the observable artefact that lets analysts and statistics consumers tell them apart; it is not a record_type axis.

### 4.2 Pure #9-Anchored Digital-Harm Record

The path is a single #9 step. No IT system is compromised by the attacker directly; the digital harm is anchored on #9 Social Engineering. The #9 step records its own SRE per core §3.4 (the loss of control lands on the system the victim operates — a payment channel, a mailbox, a wallet — exercised through the victim's own action). There is no direct SRE, so `+ [SRE]` is not rendered.

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

A DRE may appear in a `pure_9_record` only when the manipulation itself directly causes data disclosure or resource impact; it hangs off the #9 step's own SRE, so the core chain SRE → DRE is preserved:

```text
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-ID.11 Phishing for Credentials]
+ [DRE: C]
```

If the disclosed credential, token, or identity artifact is later used, the case transitions to a `compromise_record`:

```text
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-ID.11] + [DRE: C]
→ #4 + [SRE]
```

Credential acquisition is classified by the enabling cluster. Credential use is #4 provided the identity claimed is not the presenter's own (R-CRED). A credential the target system itself issued to the attacker through a designed enrolment function is not #4 when used; where the enrolment granted an identity or permissions outside their intended population or scope, the enrolment step is #1 (fictitious self-registration: `#1`; enrolment completed as an existing identity: `#1 → #4`).

### 4.3 Successful Steps Only

A cluster assignment asserts the step's SRE, so a TLCTC+ path contains only steps that succeeded (core §3.4, since v2.6). An attempted or blocked step records no SRE and is not a step of the path. It is a near miss: the application companion (§10) counts it in the attempted cluster's Key Risk Indicator, and it is evidence about the control that stopped it (Axiom V).

For a #9 step, success means the manipulation produced the unsafe action it aimed at: the person paid, disclosed, installed, approved, or otherwise acted. A lure that was received and recognised, reported but not acted on, or filtered before delivery, is not a #9 step. Counting it as an incident would turn a measure of control success into a count of compromises. It is recorded as a near miss instead (§4.4).

The same applies inside a path: where a later step was attempted and averted, the path ends at the last step that succeeded, and the averted step is named in `averted_next` (§17.3), never written as a step.

### 4.4 Near-Miss Record

A near miss is an attack in which the attacker acted but a control held before any step succeeded. The application companion (v2.7, §10) makes near misses part of every cluster's Key Risk Indicator: the threat materialised, the control held, and both facts are information. A near-miss record has:

- one **attempted step**, classified by the cluster the attack aimed at and written inside `[Attempt: …]`, so that it is an annotation and not a path step. Bridge clusters keep their boundary operator (R-BOUNDARY);
- an optional **Pattern**, which carries the narrative for public warnings;
- optional **Report** annotations, such as the citizen's report or a warning flag;
- in the data model, **which control held** (`held_by`) and **where the attack stopped** (`stopped_at`: at `delivery`, before it reached the target, or at the `target`, which did not perform the step). Both are required (V-7).

It has no SRE, no DRE, no BRE and no Impact (R-NEAR-MISS): nothing left its owner's control, so the consequence chain never began.

```text
[Attempt: #9 ||[messaging][@External→@Citizen]||] [Pattern: PATTERN-ID.13 Fake Login Portal]
+ [Report: REPORT-NCSC.11 Voluntary NCSC/CERT Report Filed]
```

Near misses arrive in volume. A record MAY stand for one campaign rather than one message, with `campaign_id` and `report_count` in the data model (§17.10), so that a thousand forwarded copies of the same text message are one record with a count.

Near-miss records are never counted as incidents and never enter incident statistics. They are counted as near misses per cluster (Key Risk Indicator, alongside the cluster's incidents) and they feed control indicators such as block rates and the share of lures recognised by recipients.

**Near misses inside an incident.** Where a path succeeded up to a point and the next step was averted, the record stays an incident record and names the averted cluster in `averted_next`. The credential-phishing case is the application companion's own example: the credential was disclosed (`#9 + [DRE: C]`), the victim reported it and the password was reset before the attacker presented it, so the `#4` step was averted. That is a `pure_9_record` with `averted_next: "#4"`, and it counts as a `#9` incident and a `#4` near miss. `averted_next` is set only where a control is known to have held — a credential revoked, a login blocked by MFA, an execution stopped by an allowlist — not merely because the next step has not been observed yet.

---

## 5. Explicit Non-Scope

TLCTC+ v0.9 does **not** cover:

- the three non-cyber rows of the TLCTC cause-side partition (core §3.5, R-SCOPE): Failure / external event, Error in Use, and Abuse of Rights — none has a cluster, none has a System Risk Event, and Abuse of Rights enters the consequence chain at the DRE;
- compliance events entered directly by a normative edge with no cluster before them (core §3.4, entry points) — for example a norm amended so that an unchanged process becomes non-compliant;
- complete enterprise operational-risk taxonomies;
- criminal-law classification;
- law-enforcement investigative taxonomies;
- actor attribution taxonomies;
- control-failure taxonomies;
- an ORE notation;
- new TLCTC top-level clusters.

Incorrect:

```text
[ORE: Batch Failure] → [BRE: Payment Function Unavailable]
```

Incorrect:

```text
#11 Romance Scam
```

Incorrect (Abuse of Rights is not #1):

```text
#1 [Pattern: PATTERN-FIN.22 Invoice / Mandate Fraud]      ← clerk posting a false invoice inside their mandate
```

Correct for that case: no TLCTC+ record; the event is operational risk and the chain begins at `[DRE: If]`. The same clerk reaching past their mandate (changing an approval limit they were not granted) is `#1` and in scope.

Correct:

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
```

---

## 6. Design Principles

### 6.1 Preserve TLCTC Core

TLCTC+ SHALL preserve TLCTC semantics unchanged:

```text
Threats remain causes.
Actors are not threats.
Control failures are not threats.
SRE is the cyber Bow-Tie central event; every cluster step records one (core §3.4).
An entitled actor inside their grant is not cyber (R-SCOPE).
DREs are Data Risk Events read off the record, never off the cause (Axiom III).
Patterns are cause-side descriptors.
BREs are consequence-side events.
Impacts are measurements.
Reports are workflow/procedural artefacts.
```

### 6.2 Cause First

Every TLCTC+ record MUST begin with a TLCTC cause path or a #9 anchor.

Correct:

```text
#9 ||[email][@External→@Org]|| → #4 + [SRE]
```

Incorrect:

```text
[BRE: Account Takeover] → #4
```

### 6.3 Pattern/Event Separation

Scam names, fraud labels, and criminal playbooks are Patterns, not BREs.

Correct:

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
```

Incorrect:

```text
#9 + [BRE: Romance Scam]
```

### 6.4 BRE/Impact Separation

A BRE is what happened. Impact is how much it hurt.

Correct:

```text
+ [BRE: BRE-CUS.11 Customer Account Closure]
+ [Impact: IMPACT-FIN.16 Customer Churn Loss = EUR 1.2m]
```

Incorrect:

```text
+ [BRE: Financial Loss]
```

### 6.5 REPORT/BRE-REG Separation

BRE-REG codes describe regulatory consequences. REPORT codes describe procedural artefacts or workflow stages.

```text
+ [BRE: BRE-REG.11 Mandatory Notification Obligation Triggered]
+ [Report: REPORT-NIS2.11 24h Early Warning Filed]
```

### 6.6 Cause/Consequence Independence

A TLCTC cluster does not determine the BRE family. The cause-side cluster classifies the generic vulnerability. The BRE family classifies the observed consequence.

Examples:

```text
#4 → BRE-ENT.*    human or organizational identity harm
#4 → BRE-SVC.*    technical-identity use causing service impact
#7 → BRE-FIN.*    malware-enabled fraud consequence
#7 → BRE-SVC.*    malware-enabled service consequence
#9 → BRE-FIN.*    pure induced payment
#9 → BRE-CUS.*    citizen harm without payment
#10 → BRE-REG.*   subverted supplier; a notification duty arises (normative edge)
```

---

## 7. Tracks

TLCTC+ uses six tracks. They are tracks, not layers, to avoid collision with TLCTC core layering.

```text
Cause Track       TLCTC path or #9 anchor; Pattern attaches here
SRE Track         System Risk Events — one per cluster step (direct or induced); the first direct SRE is marked
DRE Track         Confidentiality, Integrity (incorrect / misattributed), Availability (unavailable / inaccessible) events
BRE Track         Business, citizen, regulatory, service, legal, or organizational events
Impact Track      Quantified or qualified harm measurement
Report Track      Reporting artefacts, workflow stages, authority filings
```

---

## 8. Notation

### 8.1 Cause Path

TLCTC cause paths use core TLCTC v2.7 notation (core §7): sequence `→`, parallel `+`, velocity `→[Δt=…]`, domain boundary `||[context][@Source→@Target]||`, transit `⇒`, intra-system boundary `|[context][@a→@b]|`, and the epistemic annotations `[conf=low]`, `[inferred]`, `?`, `…`. A Δt on the path is the causal interval between two steps and bounds the window in which detection and response can act (core §7.2).

```text
#9 → #4 → #7
#9 →[Δt=hours] #4 →[Δt=5m] #1
```

Unresolved-step operators (`?`, `…`) are admitted in a `compromise_record` path under the core R-UNRES rules: they never carry DRE tags (R-UNRES-5), are excluded from statistics (R-UNRES-2), and require a prose note. A `pure_9_record` admits none — its path is exactly one classified #9 step.

Bridge clusters (#8, #9, #10) MUST carry a boundary operator in TLCTC+ records:

```text
#9 ||[email][@External→@Org]||
#10 ||[update][@Vendor→@Org]||
```

A #10 step sits at the Trust Acceptance Event and requires that the trusted third party, or the trust artifact it issued, was subverted before acceptance (core R-SUPPLY, since v2.6). A defect in a legitimately supplied component is classified where it is exploited (#2 or #3 per R-ROLE), and a supplier's outage honoured across the boundary is third-party failure, not #10 (core §3.5). A record that reports a supplier incident therefore names #10 only where the subversion is evidenced.

### 8.2 SRE

```text
+ [SRE]
```

Under the core every cluster step records its own SRE; a path of *n* steps has *n* SREs. TLCTC+ does not annotate each of them. `+ [SRE]` is the **first-direct-SRE marker**: it is a step annotation, written once, on the first classified non-#9 cluster step in path order. It is determined by the path and carries no reporting judgement; it states where the system first left its owner's control. In a `compromise_record` it is REQUIRED (R-SRE). In a `pure_9_record` it is not rendered: the #9 step's SRE is induced, not direct (R-SRE-9). The compromise a record wants to foreground for reporting purposes is a separate field, `reporting_pivot_step` (§17.4); it may coincide with the marked step and often will, but it is not the marker.

```text
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: Ac]        first direct SRE at #7
#9 ||[email][@External→@Org]|| → #4 + [SRE] → #1                  first direct SRE at #4; #1 records its own (direct) SRE, unmarked
#10 ||[update][@Vendor→@Org]|| + [SRE] → #7 + [DRE: C, I]        first direct SRE at #10 (the TAE); #7 unmarked
```

SRE is never a path step.

Incorrect:

```text
#7 → [SRE]
```

### 8.3 DRE

DRE codes are the core refinement tree (core §7.6; dictionary `data_risk_events`; introduced in v2.5, unchanged in v2.7): three parent properties, two admitted refinements each side of I and A.

```text
+ [DRE: C]        Loss of Confidentiality — disclosed (no refinement)
+ [DRE: I]        Loss of Integrity — refinement unknown or irrelevant
+ [DRE: Ii]       incorrect state — correspondence / completeness failed
+ [DRE: If]       misattributed state — provenance / attribution failed
+ [DRE: A]        Loss of Availability/Accessibility — refinement unknown or irrelevant
+ [DRE: Av]       unavailable state — data gone or unreachable
+ [DRE: Ac]       inaccessible state — data present but unusable (e.g. ransomware encryption)
+ [DRE: C, Ii]    several outcomes on one step — comma-separated, per core §7.6
```

A parent code (`I`, `A`) stays legal whenever the refinement is unknown or not evidenced; records SHOULD refine where the state is distinguishable by inspecting the record itself. The core stopping rule (v2.7 wording) applies: a property is split only where the states differ in the record's present standing — checked against its referent, declared scope, claimed origin or entitled agents — never by the story of how it came to be (mechanism, actor, intent). The vocabulary is closed, by decision, at the two splits above; `C` is not split, and there is no split by cause (Axiom III). Inside `[DRE: …]` the separator is `,`; `+` and `→` are not used there (see R-BRE-OP-SCOPE).

### 8.4 Pattern

Pattern is cause-side metadata and is written without `+`.

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
```

### 8.5 BRE

Single BRE:

```text
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
```

BRE chain:

```text
+ [BRE: BRE-SVC.11 Payment Function Unavailable → BRE-CUS.11 Customer Account Closure]
```

Parallel BREs:

```text
+ [BRE: BRE-SVC.11 → (BRE-CUS.11 + BRE-LGL.11)]
```

The `→` and `+` operators inside `[BRE: ...]` are scoped to the BRE lane and do not change the TLCTC cause path.

Under core v2.7 a BRE is reached by one of two kinds of edge (core §3.4, dictionary `consequence_chain`):

```text
causal      the BRE is brought about by the preceding DRE or BRE, after a Δt
            e.g. BRE-SVC.11 Payment Function Unavailable → BRE-CUS.11 Customer Account Closure
normative   a duty arises or a norm is violated; nothing propagates, no Δt is defined
            e.g. [DRE: C] on personal data → BRE-REG.11 Mandatory Notification Obligation Triggered
```

The edge kind belongs to the transition, not to the BRE code: a fine (BRE-REG.13) is imposed after a supervisory process and is reached causally, while the notification duty that preceded it arose normatively. The notation does not mark the edge kind; `→` inside `[BRE: ...]` covers both. Records carry it in the data model (`edge`, §17.6) under R-BRE-EDGE.

### 8.6 Impact

```text
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

Impact measures harm on the SRE, DRE or BRE it is linked to. It is not the core term **Business Impact**, which is a role a BRE can hold: an organization's risk appetite designates a terminal BRE as its Business Impact (core §3.4). A TLCTC+ record does not set that role; it records the BREs and measures them.

### 8.7 Report

```text
+ [Report: REPORT-NIS2.11 24h Early Warning Filed]
```

A statutory deadline (NIS2 24 h early warning and 72 h notification, DORA, GDPR Art. 33) bounds the response process, and its clock starts at awareness. It is not a Δt: it does not measure a causal interval between two events in the chain. Deadlines are recorded on the Report track (`timestamp_due`, §17.9), computed from the awareness time the regime defines.

### 8.8 Attempt (near-miss records)

```text
[Attempt: #9 ||[email][@External→@Org]||]
[Attempt: #2 ||[web][@External→@Org]||]
```

`[Attempt: …]` encloses exactly one classified cluster step and opens a near-miss record (§4.4). It is bracket-only, like Pattern, because it is not an event: nothing succeeded. It is never written inside a path, and no SRE, DRE, BRE or Impact annotation may follow it; only an optional Pattern and Report annotations. A bridge cluster inside the brackets keeps its boundary operator. Epistemic annotations (`[conf=low]`) are allowed on the attempted step where the target of the attack is uncertain; the unresolved operators `?` and `…` are not, because a near miss names the cluster it is counted under.

---

## 9. Normative Rules

### R-SRE

A `compromise_record` MUST carry exactly one `+ [SRE]` marker, on the first classified non-#9 cluster step in path order (the first direct SRE). The position is determined by the path; a validator can compute it and MUST reject any other placement. The marker does not assert that other steps lack an SRE (per core §3.4 every classified step records one), and it does not assert that the marked compromise is the one the record reports on — that is `reporting_pivot_step` (§17.4).

### R-SRE-9

A `pure_9_record` SHALL NOT render `+ [SRE]`. The #9 step's SRE (manipulation-induced loss of control over the system the victim operates) is implicit in the classified step. Rendering the marker would assert an IT-system compromise the record does not contain. *(Replaces v0.6 R-SRE-OPTIONAL-9.)*

### R-SRE-EPISTEMIC

Uncertainty about whether the first direct compromise occurred is expressed on the step (`#X [conf=low]`, `#X [inferred]`, core §7.7), never by omitting `+ [SRE]` from a `compromise_record`. The `sre.status` field (§17.4) records the evidence status of the marked SRE; it inherits the step's epistemic state. *(Replaces the v0.6 `hypothesized` carve-out.)*

### R-DRE-PLACEMENT

A DRE applies to the immediately preceding TLCTC step — that is, to that step's own SRE — unless linked explicitly in a structured record.

```text
#9 + [DRE: C] → #4
```

means the confidentiality loss occurred at #9 and hangs off the #9 SRE.

```text
#9 → #4 + [DRE: C]
```

means the confidentiality loss is associated with #4 or the path segment ending in #4, depending on structured linkage.

### R-PATTERN-POSITION

Pattern annotations MUST use bracket-only form:

```text
[Pattern: PATTERN-FIN.11]
```

Pattern MUST NOT use additive form:

```text
+ [Pattern: PATTERN-FIN.11]
```

SRE, DRE, BRE, Impact, and Report MUST use additive form.

### R-PATTERN-SPLIT

Scam, fraud, extortion, and manipulation labels MUST be Patterns, not BREs.

### R-BRE-NOT-PATH

BREs MUST NOT be inserted into the TLCTC path.

Incorrect:

```text
#7 → [BRE: BRE-SVC.11]
```

Correct:

```text
#7 + [SRE] + [DRE: Ac] + [BRE: BRE-SVC.11]
```

### R-BRE-OP-SCOPE

Inside `[BRE: ...]`, `→` expresses a consequence-side transition between BREs (causal or normative, R-BRE-EDGE) and `+` expresses co-realization. Outside annotation brackets, they express TLCTC cause-side path sequence or parallelism. The two scopes MUST NOT mix.

### R-BRE-EDGE

Each BRE is reached by a causal edge or a normative edge (core §3.4, v2.7). Where a structured record states the edge kind (`edge`, §17.6), a causal edge MAY carry a Δt and a normative edge MUST NOT. A duty arising or a norm being violated — a notification obligation triggered, a deadline missed — is reached by a normative edge; an event brought about by the preceding one — an outage, a payment, a filing, a fine imposed after a supervisory process — by a causal edge. A statutory deadline is never recorded as a Δt; it belongs on the Report track as `timestamp_due`, counted from awareness.

### R-SUCCESS

A TLCTC+ path contains only cluster steps that succeeded (core §3.4, since v2.6). An attempted or blocked step, and a lure nobody acted on, MUST NOT be recorded as a path step or as an incident record. Where no step succeeded it is a `near_miss_record`; where it followed successful steps it is named in `averted_next` (§4.3, §4.4).

### R-NEAR-MISS

A `near_miss_record` carries exactly one attempted step in `[Attempt: …]`, an optional Pattern, and optional Report annotations. It MUST NOT carry `+ [SRE]`, DRE, BRE or Impact annotations, MUST state `held_by` and `stopped_at` in the data model, and MUST NOT be counted in incident statistics. It is counted as a near miss of the attempted cluster.

### R-IMPACT

Loss amounts, downtime, customer counts, affected record counts, legal costs, regulatory fine amounts, and similar measurements SHOULD be Impact, not BRE.

### R-REPORT

REPORT codes describe reporting artefacts or workflow stages. They SHALL NOT appear inside BRE chains.

### R-BOUNDARY

Every #8, #9, and #10 step in a TLCTC+ record MUST carry an explicit domain boundary operator (core §7.3).

```text
#9 ||[email][@External→@Org]||
#10 ||[service][@Provider→@Org]||
```

This is a TLCTC+ profile rule for reporting precision; it does not modify core TLCTC.

### R-RECOVERABILITY

For compromise records, stripping all SRE, DRE, BRE, Impact, Pattern, and Report annotations MUST recover a valid TLCTC v2.7 path (core §7, including any epistemic annotations, which belong to the core path and are retained).

For pure #9 records, stripping all annotations MUST recover a valid #9 bridge anchor.

For near-miss records, stripping all annotations, `[Attempt: …]` included, leaves no path. That is the intended result: no step succeeded.

### R-CAUSE-CONSEQUENCE-INDEPENDENCE

Consequence-side BRE families MUST be selected from observed harm, not auto-derived from cause-side cluster identity.

### R-NO-FREE-TEXT-BRE

New records MUST use structured BRE codes. Free-text labels may be retained for archival readability but must not be the canonical BRE value.

---

## 10. Minimal Grammar

```text
<tlctc-plus-record> ::= <compromise-record> | <pure-9-record> | <near-miss-record>

<compromise-record> ::= <annotated-path> <record-annotation>*

<pure-9-record>     ::= <annotated-9-step> <record-annotation>*

<near-miss-record>  ::= <attempt-annotation> <pattern-annotation>? <report-annotation>*
<attempt-annotation> ::= "[Attempt: " <cluster-step> "]"                ; v0.9, §4.4, §8.8

<annotated-path>    ::= <annotated-step> (<path-operator> <annotated-step>)*
<annotated-step>    ::= <step> <step-annotation>*
<annotated-9-step>  ::= "#9" <boundary-annotation> <pattern-annotation>? <dre-annotation>?

<step>              ::= <cluster-step> | <unresolved-step>          ; core §7: "#X" with optional
                                                                     ; boundary, transit, intra-system,
                                                                     ; epistemic annotations; "?" | "…"
<path-operator>     ::= "→" | "→[Δt=" <velocity> "]" | "+"          ; core §7.1–7.2

<step-annotation>   ::= <sre-marker> | <dre-annotation> | <pattern-annotation>
<record-annotation> ::= <bre-annotation> | <impact-annotation> | <report-annotation>
```

Step annotations attach to the step they follow; record annotations follow the whole path. `<step>` and `<path-operator>` are the core v2.7 attack-path grammar (core §7) and are not redefined here. The grammar admits more than R-* allows; the following constraints are enforced by the validator, not by the grammar:

```text
V-1  a <compromise-record> contains at least one <cluster-step> other than "#9"
V-2  exactly one <annotated-step> in a <compromise-record> carries <sre-marker>,
     and it is the first <cluster-step> other than "#9" in path order          (R-SRE)
V-3  a <pure-9-record> carries no <sre-marker>                                  (R-SRE-9)
V-4  an <unresolved-step> carries no <dre-annotation>                           (R-UNRES-5)
V-5  a <pure-9-record> has at least one <dre-annotation> or <bre-annotation>,
     or sets averted_next
V-6  reporting_pivot_step, if set, names a <cluster-step> present in the path
V-7  a <near-miss-record> states held_by and stopped_at                         (R-NEAR-MISS)
V-8  averted_next, if set, names a cluster and appears only on a
     <compromise-record> or a <pure-9-record>                                    (R-SUCCESS)
```

The near-miss production admits no SRE, DRE, BRE or Impact annotation, so R-NEAR-MISS's notation half is enforced by the grammar itself.

```text
<sre-marker>         ::= "+ [SRE]"
<dre-annotation>     ::= "+ [DRE: " <dre-expression> "]"
<pattern-annotation> ::= "[Pattern: " <pattern-expression> "]"
<bre-annotation>     ::= "+ [BRE: " <bre-expression> "]"
<impact-annotation>  ::= "+ [Impact: " <impact-expression> "]"
<report-annotation>  ::= "+ [Report: " <report-expression> "]"
```

```text
<dre-expression> ::= <dre-node> ("," <dre-node>)*
<dre-node>       ::= "C" | "I" | "Ii" | "If" | "A" | "Av" | "Ac"
```

---

## 11. Namespaces

```text
TLCTC-XX.YY       TLCTC operational threat notation
SRE               System Risk Event / Loss of Control / System Compromise (one per cluster step; marker = first direct SRE)
DRE-X             Data Risk Event (core tree: C, I/Ii/If, A/Av/Ac)
PATTERN-XXX.YY    Cause-side narrative / scam / fraud / crime pattern
Attempt           Attempted cluster step of a near-miss record (no SRE; not a path step)
BRE-XXX.YY        Business Risk Event
IMPACT-XXX.YY     Quantified or qualified impact
REPORT-XXX.YY     Reporting artefact / workflow state
```

Namespaces MUST NOT be collapsed.

---

# 12. Pattern Catalogue v0.2

Patterns describe attacker narratives, criminal playbooks, or reporting labels. They are not BREs.

## 12.1 Financial Manipulation Patterns

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

## 12.2 Identity and Account Manipulation Patterns

```text
PATTERN-ID.00 Identity / Account Manipulation Pattern — reserved
PATTERN-ID.11 Phishing for Credentials
PATTERN-ID.12 MFA Fatigue / Push Manipulation
PATTERN-ID.13 Fake Login Portal
PATTERN-ID.14 SIM-Swap Inducement
PATTERN-ID.15 Account Recovery Abuse Narrative
PATTERN-ID.16 Social Media Impersonation
```

## 12.3 Coercion and Extortion Patterns

```text
PATTERN-EXT.00 Coercion / Extortion Pattern — reserved
PATTERN-EXT.11 Sextortion Threat
PATTERN-EXT.12 Data Leak Threat
PATTERN-EXT.13 Physical Harm Threat
PATTERN-EXT.14 Reputational Harm Threat
PATTERN-EXT.15 Law-Enforcement Impersonation Threat
```

---

# 13. BRE Catalogue v0.4

BREs are discrete, observable business, citizen, legal, regulatory, service, third-party, or organizational consequence events.

## 13.1 Service / Operations

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

## 13.2 Customer / Citizen / Market

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

## 13.3 Financial Event

```text
BRE-FIN.00 Financial Event — reserved
BRE-FIN.10 Authorized Payment Family — reserved
BRE-FIN.11 Authorized Push Payment Made
BRE-FIN.12 Authorized Crypto Transfer Made
BRE-FIN.13 Gift Card / Voucher Transfer Made
BRE-FIN.14 Cash Withdrawal Made
BRE-FIN.15 Goods or Services Paid but Not Received
BRE-FIN.16 Onward Funds Transfer Executed
BRE-FIN.20 Unauthorized Payment Family — reserved
BRE-FIN.21 Unauthorized Bank Transfer Executed
BRE-FIN.22 Unauthorized Card Transaction Executed
BRE-FIN.23 Unauthorized Crypto Transfer Executed
BRE-FIN.24 Unauthorized Payroll Change Executed
BRE-FIN.25 Refund / Reimbursement Diverted to Third Party
```

## 13.4 Entity / Identity / Account Harm

`BRE-ENT.*` records consequences where a human or organizational principal is the harmed entity.

```text
BRE-ENT.00 Identity / Account Harm — reserved
BRE-ENT.11 Personal Identity Used Without Consent
BRE-ENT.12 Social Media Account Takeover Harm
BRE-ENT.13 Email Account Takeover Harm
BRE-ENT.14 SIM-Swap Consequence
BRE-ENT.15 Digital Identity Wallet Used Without Consent
BRE-ENT.16 Compromised Credential Used to Authenticate
BRE-ENT.17 Authorization Granted Under False Identity
BRE-ENT.18 Unauthorized Account Creation
BRE-ENT.19 Account Recovery Lockout
```

Technical-identity use remains #4 on the cause side but may produce BRE-SVC, BRE-FIN, BRE-DATA, BRE-ORG, or another observed consequence family rather than BRE-ENT.

`BRE-ENT.18 Unauthorized Account Creation` is a consequence code and does not fix the cause-side cluster: self-registration through a designed enrolment function into a population or scope it was not meant for is `#1` at enrolment (R-CRED), and subsequent use of that self-issued account is not `#4`. Enrolment completed *as an existing identity* is `#1 → #4`.

## 13.5 Legal

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

## 13.6 Regulatory / Supervisory

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

## 13.7 Reputation / Public Communication

```text
BRE-REP.00 Reputation / Communication Event — reserved
BRE-REP.11 Public Warning Issued
BRE-REP.12 Media Escalation Occurred
BRE-REP.13 Executive Public Statement Issued
BRE-REP.14 Parliamentary / Political Attention Triggered
BRE-REP.15 Sector-Wide Alert Issued
BRE-REP.16 Public Correction / Clarification Issued
```

## 13.8 Third-Party / Ecosystem Consequence

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

BRE-3P captures observed ecosystem consequences. It is not automatically implied by #10.

## 13.9 Internal Organization

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

## 13.10 Data Consequence (v0.4)

`BRE-DATA.*` records what a Data Risk Event means for the organization that holds the data: its custody of other people's data, its own secrets, its control over its systems, the records it relies on, and whether it can get its data back. The DRE states what happened to the data; a BRE-DATA code states what happened to the business because of it.

```text
BRE-DATA.00 Data Consequence — reserved

BRE-DATA.10 Disclosure Family — reserved              reached from [DRE: C]
BRE-DATA.11 Entrusted Data Exposed
BRE-DATA.12 Proprietary Data Exposed
BRE-DATA.13 Control Material Exposed
BRE-DATA.14 Exposed Data Published
BRE-DATA.15 Exposed Data Offered for Sale
BRE-DATA.16 Exposed Data Used to Target Data Subjects

BRE-DATA.20 Reliance Family — reserved                reached from [DRE: I], [DRE: Ii] or [DRE: If]
BRE-DATA.21 Decision Taken on Incorrect Data
BRE-DATA.22 Incorrect Data Passed to Counterparties
BRE-DATA.23 Records Restatement Required
BRE-DATA.24 Misattributed Record Accepted
BRE-DATA.25 Record Provenance Not Demonstrable

BRE-DATA.30 Recoverability Family — reserved          reached from [DRE: A], [DRE: Av] or [DRE: Ac]
BRE-DATA.31 Data Restored With Loss
BRE-DATA.32 Data Permanently Lost
BRE-DATA.33 Records Reconstructed From Secondary Sources
BRE-DATA.34 Recovery Dependent on Attacker
```

**Structure.** The decades follow the core DRE tree (core §7.6): the decade of a code names the DRE property it is reached from — disclosure from `C`, reliance from `I`, recoverability from `A`. Inside a decade, codes split by the organization's relation to the data — whose data it is, what it does, what relied on it — and never by how the data state came about. This is the business-layer counterpart of the core DRE stopping rule (§8.3): mechanism, actor and intent do not create codes. The decades are keyed to the DRE, which is consequence-side, and never to a cluster (R-CAUSE-CONSEQUENCE-INDEPENDENCE). In the disclosure decade, .11–.13 are the exposure itself, one code per data role; .14–.16 are what happens to exposed data afterwards, reached causally from .11–.13.

| Code | Reached from | Event |
|---|---|---|
| BRE-DATA.11 | `C` | Data the organization holds for others — customers, citizens, employees, clients — has left its control. The custody event. |
| BRE-DATA.12 | `C` | The organization's own confidential information — trade secrets, source code, strategy, pricing or deal data — has left its control. |
| BRE-DATA.13 | `C` | Credentials, keys, tokens, certificates or configurations that grant control over systems have left the organization's control. Every system the material opens is no longer under assured control until it is re-keyed. Exposure is the event: use of the material is a separate `#4` on the cause side (core Axiom X) and need not have occurred. |
| BRE-DATA.14 | .11, .12 or .13; causal | Exposed data is made publicly accessible (leak site, paste site, media). |
| BRE-DATA.15 | .11, .12 or .13; causal | Exposed data is offered to buyers. |
| BRE-DATA.16 | .11 or .13; causal | Exposed data is used to approach the people or organizations it describes, e.g. tailored phishing of customers. The harm to them is recorded in their own records. |
| BRE-DATA.21 | `Ii` or `I` | A business decision, calculation or automated action relied on data in an incorrect state. |
| BRE-DATA.22 | `Ii` or `I` | Incorrect data was passed to customers, partners, markets or authorities. |
| BRE-DATA.23 | `Ii` or `I` | Records the organization answers for — books, statements, registers — must be corrected and reissued. |
| BRE-DATA.24 | `If` or `I` | A business process accepted a record or instruction as authoritative although its claimed origin is false. |
| BRE-DATA.25 | `If` or `I` | The organization can no longer demonstrate who created or changed a set of records — audit trails, signatures, logs. Their evidential value is lost. |
| BRE-DATA.31 | `A`, `Av` or `Ac` | Data was restored, but changes since the last recovery point are lost. |
| BRE-DATA.32 | `Av` or `A` | No recovery path exists; the data is lost. |
| BRE-DATA.33 | `A`, `Av` or `Ac` | Records are recreated from secondary sources — paper, partners, correspondence. |
| BRE-DATA.34 | `Ac` or `A` | The only recovery path for inaccessible data runs through the attacker (decryptor or key); the organization faces the ransom decision. A ransom paid is `BRE-FIN.12 Authorized Crypto Transfer Made`, reached causally from it. |

Five catalogue rules apply to the family:

```text
D-1  Reachability. A record carrying a BRE-DATA code carries a DRE of the code's decade
     (linked_to_dre, §17.6), and the code is reached from that DRE directly or through
     other BREs. Where a code names a refinement (.21–.23 Ii; .24–.25 If; .32 Av; .34 Ac),
     the DRE is that refinement or its parent. Checkable by a validator.
D-2  One code per role. Data that plays several roles gets one code per role, co-realized
     with "+": (BRE-DATA.11 + BRE-DATA.13). There are no combined codes.
D-3  Specific family first. Where the consequence is a payment (BRE-FIN), an authorization
     or identity harm (BRE-ENT), a stopped process (BRE-SVC), a duty (BRE-REG, BRE-LGL) or
     an ecosystem disruption (BRE-3P), that family is used. BRE-DATA records the
     consequence for the data itself: custody, reliance, recoverability. A misattributed
     instruction executed as a payment is BRE-FIN.21, not BRE-DATA.24; a forged
     authorization is BRE-ENT.17.
D-4  Event, not count. Record, account and system counts are IMPACT-DATA.* (R-IMPACT).
D-5  Duties on top. Where the custody event is known, the record SHOULD carry it and reach
     the notification duty from it by a normative edge, so that the first BRE is a business
     event and the duty sits on it: [DRE: C] + [BRE: BRE-DATA.11 → BRE-REG.11]. Reaching
     BRE-REG.11 directly from the DRE (§8.5) remains valid.
```

Examples:

```text
… → #4 ||[auth][@External→@MSP]|| + [SRE] → #1 + [DRE: C]
+ [BRE: (BRE-DATA.11 Entrusted Data Exposed + BRE-DATA.13 Control Material Exposed)
   → (BRE-REG.11 Mandatory Notification Obligation Triggered + BRE-ORG.16 Control Remediation Program Opened)]
```

A managed service provider's document store held its customers' MFA and RMM API keys and backup-storage credentials. The material is both entrusted and control material, so it takes two codes (D-2). The notification duty is reached from BRE-DATA.11 by a normative edge; the remediation programme from BRE-DATA.13 by a causal edge.

```text
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: Ac]
+ [BRE: (BRE-SVC.16 Critical Business Process Interrupted + BRE-DATA.34 Recovery Dependent on Attacker)
   → BRE-FIN.12 Authorized Crypto Transfer Made]
```

The stopped process is BRE-SVC.16 and the data's recoverability is BRE-DATA.34: two consequences of one DRE, in two families (D-3). The ransom payment follows from the recoverability event.

---

# 14. Impact Catalogue v0.2

Impacts measure SRE, DRE, or BRE consequences.

## 14.1 Financial

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

## 14.2 Operational

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

## 14.3 Customer / Citizen

```text
IMPACT-CUS.00 Customer / Citizen Impact — reserved
IMPACT-CUS.11 Number of Customers Affected
IMPACT-CUS.12 Number of Complaints
IMPACT-CUS.13 Number of Accounts Closed
IMPACT-CUS.14 Vulnerable Persons Affected
IMPACT-CUS.15 Customer Harm Severity
IMPACT-CUS.16 Number of Citizens Affected
```

## 14.4 Regulatory / Legal

```text
IMPACT-REG.00 Regulatory / Legal Impact — reserved
IMPACT-REG.11 Notification Count
IMPACT-REG.12 Jurisdictions Notified
IMPACT-REG.13 Supervisory Findings Count
IMPACT-REG.14 Enforcement Severity
IMPACT-REG.15 Number of Legal Claims
```

## 14.5 Reputation

```text
IMPACT-REP.00 Reputation Impact — reserved
IMPACT-REP.11 Media Articles
IMPACT-REP.12 Social Media Volume
IMPACT-REP.13 Sentiment Change
IMPACT-REP.14 Trust Index Change
IMPACT-REP.15 Public Confidence Indicator Change
```

## 14.6 Data / Resource

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

# 15. Report Catalogue v0.2

REPORT codes describe procedural artefacts, reporting stages, or workflow states.

## 15.1 NCSC / CERT

```text
REPORT-NCSC.00 NCSC / CERT Reporting — reserved
REPORT-NCSC.11 Voluntary NCSC/CERT Report Filed
REPORT-NCSC.12 Mandatory NCSC/CERT Report Filed
REPORT-NCSC.13 Public Warning Candidate Flagged
REPORT-NCSC.14 Law-Enforcement Referral Candidate Flagged
REPORT-NCSC.15 Cross-Border CSIRT Sharing Candidate Flagged
REPORT-NCSC.16 Sector Alert Candidate Flagged
```

## 15.2 NIS2

```text
REPORT-NIS2.00 NIS2 Reporting — reserved
REPORT-NIS2.11 24h Early Warning Filed
REPORT-NIS2.12 72h Incident Notification Filed
REPORT-NIS2.13 Intermediate Report Filed
REPORT-NIS2.14 Final Report Filed
REPORT-NIS2.15 Cross-Border Impact Indication Filed
```

## 15.3 DORA

```text
REPORT-DORA.00 DORA Reporting — reserved
REPORT-DORA.11 Initial Notification Filed
REPORT-DORA.12 Intermediate Report Filed
REPORT-DORA.13 Final Report Filed
REPORT-DORA.14 Significant Cyber Threat Voluntary Notification Filed
REPORT-DORA.15 Major Operational or Security Payment-Related Incident Report Filed
```

## 15.4 Data Protection

```text
REPORT-DP.00 Data Protection Reporting — reserved
REPORT-DP.11 Data Protection Authority Notification Filed
REPORT-DP.12 Data Subject Notification Filed
REPORT-DP.13 Processor-to-Controller Notification Filed
```

---

# 16. Regulatory and Reporting Alignment

TLCTC+ should be read as a semantic bridge, not as a replacement for external reporting regimes.

```text
Likely cyber/root cause        → TLCTC path
Loss of control / compromise   → SRE (one per step; the first direct one is marked; the reporting pivot is a field)
Data/resource effect           → DRE (C, I/Ii/If, A/Av/Ac)
Scam/fraud/crime narrative     → Pattern
Observable consequence         → BRE (reached by a causal or a normative edge)
Severity / magnitude           → Impact
Filing / workflow state        → Report
Statutory deadline             → Report timestamp_due, counted from awareness (never a Δt)
Attempt, blocked or not acted on → near_miss_record (near-miss KRI, never an incident)
```

This structure can support NCSC/CERT reporting, financial-sector fraud reporting, DORA-style ICT incident reporting, NIS2-style incident notification, data-protection reporting, and internal OpRisk aggregation while preserving the cause/effect separation of core TLCTC.

External regime labels may be retained as aliases or metadata, but they should not override TLCTC+ semantics.

---

# 17. Minimal Data Model

## 17.1 Record Types

```text
compromise_record
pure_9_record
near_miss_record
```

`compromise_record` covers any case whose TLCTC path contains at least one cluster step other than #9 — an actor holds capability over an IT system directly — regardless of whether the dominant downstream BRE family is cyber-side (BRE-SVC.*, BRE-DATA.*, BRE-REG.*) or consequence-side (BRE-FIN.*, BRE-ENT.*, BRE-CUS.*). `pure_9_record` covers manipulation-driven digital harm whose path is a single #9 step; its only SRE is the #9 step's own. `near_miss_record` (v0.9) covers an attack in which no step succeeded because a control held; it has no path and no SRE, and only its Cause, Pattern and Report fields apply, plus the near-miss fields of §17.10.

## 17.2 Required Metadata

```text
case_id
record_type
framework_version            "2.7" for v0.9 records
tlctc_plus_version           "0.9"
intake_source
reporting_entity_type
sector
country
timestamp_reported
timestamp_detected
confidence
```

## 17.3 Cause Fields

```text
tlctc_path                         compromise_record (pure_9_record: tlctc_anchor)
tlctc_steps[]
attempted_step                     near_miss_record only: the [Attempt: ...] content, e.g. "#9 ||[messaging][@External→@Citizen]||"
averted_next                       OPTIONAL — incident records only: the cluster of the next step, which a control
                                   is known to have averted (e.g. "#4"); counted as a near miss of that cluster
patterns[]
evidence[]
actor_attribution_optional
```

## 17.4 SRE Fields

The `sre` block describes the **marked SRE**: in a `compromise_record` the first direct SRE (the step carrying `+ [SRE]`); in a `pure_9_record` the #9 step's induced SRE. Other steps' SREs are not enumerated at v0.9; they are implied by `tlctc_steps[]`.

```text
kind: direct | induced             direct for compromise_record (non-#9 step); induced for pure_9_record (#9)
status: observed | confirmed | disputed | retracted
epistemic: classified | low_confidence | inferred   mirrors the step annotation (core §7.7)
timestamp
description
scope
linked_to_step                     the marked step; for compromise_record this is derivable (V-2) and MUST agree
confidence
reporting_pivot_step               OPTIONAL — the step whose compromise this record foregrounds for reporting;
                                   a representational choice, independent of the marker; defaults to linked_to_step
```

`present` (v0.6) is removed: under core v2.5.1 an SRE is present for every classified step, so the field carried no information. `decisive` (v0.7) is removed: it conflated the ontic position of the first direct SRE with the reporting choice, which `reporting_pivot_step` now carries on its own.

## 17.5 DRE Fields

```text
type: C | I | Ii | If | A | Av | Ac
status
affected_data_or_resource
scope
timestamp_observed
linked_to_step
linked_to_sre
confidence
```

## 17.6 BRE Fields

```text
code
label
status: observed | confirmed | disputed | retracted | open
parent
operator: → | +
edge: causal | normative           OPTIONAL — how this BRE is reached from its parent, DRE or SRE (R-BRE-EDGE)
delta_t                            OPTIONAL — causal interval from the parent event; only where edge = causal
timestamp
linked_to_dre
linked_to_sre
linked_to_step
confidence
```

## 17.7 Pattern Fields

```text
code
label
family
linked_to_step
channel
narrative
confidence
national_alias
```

## 17.8 Impact Fields

```text
code
label
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

## 17.9 Report Fields

```text
code
label
reporting_regime
stage
timestamp_due                      deadline set by the regime, counted from awareness; not a Δt (§8.7)
timestamp_filed
authority
status
linked_to_bre_reg
linked_to_sre
linked_to_dre
```

## 17.10 Near-Miss Fields

Required on a `near_miss_record` (V-7); not used on incident records, which name an averted step in `averted_next` instead.

```text
held_by: user | filter | provider | authority | other
                                   the control that held: the recipient recognised the lure; a mail, SMS or
                                   web filter; a platform or operator; a takedown or block by an authority
stopped_at: delivery | target      delivery = the attack never reached the target; target = it reached the
                                   person or system, which did not perform the step
campaign_id                        OPTIONAL — groups reports of the same campaign
report_count                       OPTIONAL — number of reports or blocked items this record stands for
first_seen, last_seen              OPTIONAL
```

---

# 18. Example JSON Records

## 18.1 Pure #9 Digital Harm

```json
{
  "case_id": "case-002",
  "record_type": "pure_9_record",
  "framework_version": "2.7",
  "tlctc_plus_version": "0.9",
  "tlctc_anchor": "#9 ||[messaging][@External→@Citizen]||",
  "patterns": [
    {
      "code": "PATTERN-FIN.11",
      "label": "Romance / Relationship Scam",
      "linked_to_step": "step-1"
    }
  ],
  "sre": {
    "kind": "induced",
    "status": "confirmed",
    "linked_to_step": "step-1",
    "description": "Victim induced to initiate a payment through their own e-banking; no IT system compromised by the attacker"
  },
  "dre": [],
  "bre_chain": {
    "expression": "BRE-FIN.11",
    "nodes": [
      {
        "code": "BRE-FIN.11",
        "label": "Authorized Push Payment Made",
        "edge": "causal"
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

## 18.2 Hybrid BEC / Invoice Fraud

```json
{
  "case_id": "case-003",
  "record_type": "compromise_record",
  "framework_version": "2.7",
  "tlctc_plus_version": "0.9",
  "tlctc_path": "#9 ||[email][@External→@Org]|| [Pattern: PATTERN-ID.11 Phishing for Credentials] + [DRE: C] → #4 + [SRE]",
  "patterns": [
    {
      "code": "PATTERN-FIN.22",
      "label": "Invoice / Mandate Fraud",
      "linked_to_step": "step-1"
    }
  ],
  "sre": {
    "kind": "direct",
    "status": "confirmed",
    "epistemic": "classified",
    "linked_to_step": "step-2",
    "reporting_pivot_step": "step-2",
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
    "expression": "BRE-ENT.13 → BRE-FIN.11",
    "nodes": [
      {
        "code": "BRE-ENT.13",
        "label": "Email Account Takeover Harm",
        "edge": "causal"
      },
      {
        "code": "BRE-FIN.11",
        "label": "Authorized Push Payment Made",
        "edge": "causal",
        "delta_t": "3d"
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

## 18.3 Near Miss — Reported Fake Login Portal

```json
{
  "case_id": "case-004",
  "record_type": "near_miss_record",
  "framework_version": "2.7",
  "tlctc_plus_version": "0.9",
  "attempted_step": "#9 ||[messaging][@External→@Citizen]||",
  "patterns": [
    {
      "code": "PATTERN-ID.13",
      "label": "Fake Login Portal"
    }
  ],
  "held_by": "user",
  "stopped_at": "target",
  "campaign_id": "camp-2026-118",
  "report_count": 412,
  "report": [
    {
      "code": "REPORT-NCSC.11",
      "label": "Voluntary NCSC/CERT Report Filed"
    },
    {
      "code": "REPORT-NCSC.13",
      "label": "Public Warning Candidate Flagged"
    }
  ]
}
```

No `sre`, `dre`, `bre_chain` or `impact` block: nothing left its owner's control.

---

# 19. Worked Examples

## 19.1 Romance Scam, No Cyber Compromise

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

No `+ [SRE]` marker: the #9 step's SRE (the victim's payment channel used under manipulation) is implicit, and no IT system was compromised by the attacker. No DRE. #9 is the cause-side anchor.

## 19.2 Phishing With Credential Disclosure, No Observed Use Yet

```text
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-ID.11 Phishing for Credentials]
+ [DRE: C]
```

Still a `pure_9_record`: the DRE hangs off the #9 step's own SRE. If the credential is later used, append `→ #4 + [SRE]` — the record becomes a `compromise_record` with the marker at #4. If instead the victim reports it and the password is reset before use, the record stays a `pure_9_record` with `averted_next: "#4"`: a `#9` incident and a `#4` near miss (§4.4).

## 19.3 Investment Scam With Account Takeover

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.12 Investment / Crypto-Investment Scam]
+ [DRE: C] → #4 + [SRE]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm → BRE-FIN.23 Unauthorized Crypto Transfer Executed]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 30,000]
```

Credential acquisition is #9. Credential use is #4 (the identity claimed is the victim's, not the presenter's own — R-CRED). The transfer is unauthorized because the attacker executed it through the taken-over account.

## 19.4 Victim-Authorized Crypto Transfer

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.12 Investment / Crypto-Investment Scam]
+ [BRE: BRE-FIN.12 Authorized Crypto Transfer Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 30,000]
```

No `+ [SRE]` marker and no #4 unless credential use or system compromise is observed. The victim executed the transfer; the attacker held capability over the victim's decision, not over the wallet.

## 19.5 Ransomware-Driven Payment Outage

```text
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: Ac]
+ [BRE: BRE-SVC.11 Payment Function Unavailable
   → (BRE-CUS.11 Customer Account Closure + BRE-LGL.11 Customer Legal Claim)]
+ [Impact: IMPACT-FIN.16 Customer Churn Loss + IMPACT-FIN.14 Legal Cost]
```

Ransomware is not the threat cluster. The causal chain is #9 → #7. The DRE is Loss of Accessibility, not Loss of Availability, unless the service/resource is actually unavailable.

## 19.6 Supply-Chain Incident With Regulatory Reporting

```text
#10 ||[update][@Vendor→@Org]|| + [SRE] → #7 + [DRE: C, I]
+ [BRE: BRE-REG.11 Mandatory Notification Obligation Triggered
   → BRE-REG.17 Cross-Border Authority Notification Obligation]
+ [Report: REPORT-NIS2.11 + REPORT-NIS2.12 + REPORT-NIS2.14]
```

The #10 step occurs at the Trust Acceptance Event (R-SUPPLY) and is admissible because the vendor's update channel was subverted before the update was accepted; had the vendor shipped a legitimate update with an exploitable defect, the path would start where that defect is exploited. Two direct SREs are recorded (#10, #7); the marker sits on #10 because accepting the trust artifact is already the system leaving its owner's control. A record whose reporting interest is the malware execution sets `reporting_pivot_step` to the #7 step; the marker does not move. Reporting obligations are BRE/Report, not threat clusters.

Both BREs are reached by normative edges (R-BRE-EDGE): the data events meet the conditions of the notification norms, and the duties arise; no Δt is defined on either. The three filings are causal acts of the response process. Their deadlines are recorded as `timestamp_due` on each Report entry, not as Δt: the early warning and the incident notification count from awareness (24 h and 72 h), the final report from the incident notification (one month, NIS2 Art. 23(4)).

## 19.7 Fake Tech Support Without Code Execution

```text
#9 ||[phone][@External→@Citizen]|| [Pattern: PATTERN-FIN.13 Fake Tech Support Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 900]
```

No `+ [SRE]` marker, no DRE, no #7. The #9 SRE is implicit.

## 19.8 Fake Tech Support With Remote Tool Execution

```text
#9 ||[phone][@External→@Citizen]|| [Pattern: PATTERN-FIN.13 Fake Tech Support Scam]
→ #7 + [SRE]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm → BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss]
```

Add #7 only when Foreign Executable Content executes.

## 19.9 Legitimate Remote-Access Function Abuse

```text
#9 ||[phone][@External→@Citizen]|| [Pattern: PATTERN-FIN.13 Fake Tech Support Scam]
→ #1 + [SRE]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm]
```

Use #1 when legitimate software functionality is abused without implementation flaw and without FEC execution.

## 19.10 Service-Account Compromise Causing Payment-Service Outage

```text
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: C]
→ #4 → #1
+ [BRE: BRE-SVC.11 Payment Function Unavailable → BRE-ORG.12 Business Continuity Plan Activated]
+ [Impact: IMPACT-OPS.11 Downtime Duration = 4 hours
   + IMPACT-FIN.11 Lost Revenue = EUR 180,000]
```

The stolen credential is a technical identity. Cause-side credential use is still #4. Four SREs are recorded (#9 induced; #7, #4, #1 direct); the marker sits on #7, the first direct SRE. The consequence is service impact, not automatically BRE-ENT.

## 19.11 Reported Lure, Nobody Acted On

A citizen forwards a text message to the national centre: it imitates their bank and links to a fake login page. They did not open the link. A mobile operator's filter blocked the same campaign for most of its subscribers.

```text
[Attempt: #9 ||[messaging][@External→@Citizen]||] [Pattern: PATTERN-ID.13 Fake Login Portal]
+ [Report: REPORT-NCSC.11 Voluntary NCSC/CERT Report Filed + REPORT-NCSC.13 Public Warning Candidate Flagged]
```

No #9 step succeeded, so there is no path and no SRE (§4.3, R-SUCCESS). The citizen's report is a `near_miss_record` with `held_by: user` and `stopped_at: target`; the operator's blocks are a second one with `held_by: provider`, `stopped_at: delivery` and the blocked count in `report_count`. Both count as `#9` near misses and feed the public warning; neither is an incident. If another recipient enters their credentials on the page, that case is a `pure_9_record`, as in 19.2:

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-ID.13 Fake Login Portal]
+ [DRE: C]
```

## 19.12 Exploit Blocked at the Perimeter

A web application firewall blocks an injection attempt against a public portal. Nothing reached the application logic.

```text
[Attempt: #2]
```

A `#2` near miss with `held_by: filter`, `stopped_at: delivery`. Had the injection reached the application and been rejected by its input validation, `stopped_at` would be `target`. Either way, no SRE: the system never left its owner's control.

## 19.13 Malicious Attachment Opened, Execution Blocked

An employee opens an attachment from a convincing invoice email; application allowlisting stops the payload from executing.

```text
#9 ||[email][@External→@Org]|| [Pattern: PATTERN-FIN.22 Invoice / Mandate Fraud]
```

A `pure_9_record` with `averted_next: "#7"`: the manipulation succeeded (the employee acted), so `#9` is an incident with an induced SRE, and the averted execution is a `#7` near miss. No DRE and no BRE are needed; V-5 is met by `averted_next`.

---

# 20. Decision Procedure

1. **Is the event in the Attack row?** (core §3.5, R-SCOPE)  
   Ask in strict order: Is there an actor? Did the actor intend the outcome? Did an accountable grantor confer an entitlement covering this action? No actor → Failure; no intent → Error in Use; entitled → Abuse of Rights. All three are operational risk, carry no cluster and no SRE, and are outside TLCTC+. Only the Attack row continues.

2. **Did a step succeed, and how is the cause path classified?**  
   Record only steps that succeeded (R-SUCCESS). If no step succeeded — a lure nobody acted on, a blocked attempt — record a `near_miss_record`: write the attempted step in `[Attempt: …]`, state `held_by` and `stopped_at`, attach Pattern and Report where they apply, and stop (§4.4). Otherwise classify each successful step using core TLCTC v2.7 (one cluster per step, R-* rules, epistemic annotations where evidence is thin; #10 only where the subversion of the trusted third party is evidenced, R-SUPPLY). If the only step is a human manipulated through a digital channel, record `#9` with a boundary operator.

3. **Determine the record type from path composition.**  
   At least one step other than #9 → `compromise_record`; place `+ [SRE]` on the first non-#9 cluster step (R-SRE). Exactly one step, #9 → `pure_9_record`; render no `+ [SRE]` (R-SRE-9). Every classified step records its own SRE either way (core §3.4); if the record should foreground a later compromise, set `reporting_pivot_step` rather than moving the marker. If a control is known to have averted the next step, set `averted_next`.

4. **Did a Data Risk Event occur?**  
   Attach `+ [DRE: C|I|Ii|If|A|Av|Ac]` to the step whose SRE it belongs to. Refine `I`/`A` only where the state is readable off the record.

5. **Is there a scam/fraud/crime narrative?**  
   Attach `[Pattern: ...]` to the cause-side step.

6. **Did a business, citizen, regulatory, legal, service, third-party, or organizational event occur?**  
   Attach `+ [BRE: ...]`. In the structured record, state for each BRE whether it was brought about (causal edge, Δt allowed) or arose as a duty or a norm violation (normative edge, no Δt) — R-BRE-EDGE.

7. **Can the harm be measured?**  
   Attach `+ [Impact: ...]`.

8. **Was a report filed, required, or routed?**  
   Attach `+ [Report: ...]`. If an obligation was triggered, also attach the regulatory BRE. Record each deadline as `timestamp_due`, counted from awareness as the regime defines it, never as a Δt.

---

# 21. Conformance

A TLCTC+ v0.9 record is conformant if it:

1. uses a TLCTC path, a #9 anchor, or (as a `near_miss_record`) an `[Attempt: …]` step, and lies in the Attack row of the cause-side partition (R-SCOPE);
2. does not introduce new TLCTC top-level clusters;
3. as a `compromise_record`, carries exactly one `+ [SRE]`, on the first non-#9 cluster step in path order (V-2);
4. as a `pure_9_record`, renders no `+ [SRE]` and has a path of exactly one classified #9 step;
5. records DREs as `+ [DRE: ...]` using only the core codes `C | I | Ii | If | A | Av | Ac`, never as path steps, and never on unresolved steps;
6. records BREs as `+ [BRE: ...]`, never as path steps;
7. records scam/fraud/crime labels as Pattern, not BRE;
8. records Pattern in bracket-only form, without `+`;
9. records SRE/DRE/BRE/Impact/Report in additive form, with `+`;
10. records measured harm as Impact, not BRE;
11. keeps Report outside the BRE chain;
12. includes a boundary operator on every #8, #9, and #10 step;
13. uses structured BRE codes, not free-text BRE labels;
14. does not use ORE notation;
15. does not classify non-cyber operational failures;
16. selects BRE families from observed harm, not from the cause-side cluster alone;
17. recovers a valid TLCTC v2.7 path or #9 bridge anchor when TLCTC+ annotations are stripped (a `near_miss_record` recovers no path);
18. declares `framework_version = "2.7"` and `tlctc_plus_version = "0.9"`;
19. contains only path steps that succeeded; an attempt, a blocked step, or a lure nobody acted on is a `near_miss_record` or an `averted_next` entry, never a path step (R-SUCCESS);
20. gives a Δt only to BREs reached by a causal edge, and records statutory deadlines as Report `timestamp_due`, never as Δt (R-BRE-EDGE);
21. as a `near_miss_record`, carries one `[Attempt: …]` step, no SRE, DRE, BRE or Impact, and states `held_by` and `stopped_at` (R-NEAR-MISS, V-7);
22. keeps near-miss records out of incident statistics and counts them as near misses of the attempted cluster (R-NEAR-MISS).

---

# 22. Future Architecture

TLCTC+ is the first consumer of a broader consequence-side catalogue.

Target architecture:

```text
TLCTC  ─┐
        ├─→ Shared Consequence Catalogue
TLSFC  ─┘
```

In that future architecture:

- TLCTC remains the cause-side cyber-threat taxonomy.
- TLCTC+ remains the TLCTC-anchored cyber/digital-harm reporting profile.
- TLSFC or another failure-cause framework handles the non-cyber rows of the cause-side partition (Failure / external event, Error in Use, Abuse of Rights) — the events that reach the consequence chain with no cluster and, for Abuse of Rights, no SRE.
- BRE, Impact, and Report catalogues may become shared consequence-side assets.

---

# 23. Changelog

## 23.0 BRE catalogue v0.4 (2026-11-05, within v0.9)

1. Added the `BRE-DATA` family (§13.10): three reserved decades aligned with the core DRE tree — disclosure (`BRE-DATA.10`, from `C`), reliance (`BRE-DATA.20`, from `I`/`Ii`/`If`), recoverability (`BRE-DATA.30`, from `A`/`Av`/`Ac`) — and fifteen codes. Inside a decade, codes split by the organization's relation to the data, never by how the data state came about.
2. Added the catalogue rules D-1 (reachability from a DRE of the code's decade, validator-checkable through `linked_to_dre`), D-2 (one code per data role, co-realized), D-3 (more specific families first), D-4 (counts are Impact) and D-5 (notification duties sit on the custody event).
3. The family closes a gap: since v0.3 the specification referred to `BRE-DATA.*` as a dominant family of cyber-side records (§4.1.1, §13.4, §17.1) without cataloguing a single code, so the first business event of a data breach could not be coded.
4. Did not change any existing code, the PATTERN/IMPACT/REPORT catalogues (v0.2 / v0.2 / v0.2), the grammar, the data model, the record types or the specification version (v0.9).

## 23.1 v0.9 changes from v0.8

1. Re-based the profile from TLCTC v2.5.1 to TLCTC v2.7 (dictionary `tlctc-framework.v2.7.json`, core paper v2.7, DOI 10.5281/zenodo.23437984). `framework_version` is `"2.7"` and `tlctc_plus_version` `"0.9"` (§3, §17.2, §18, conformance 18). References to "core v2.5 notation / path / grammar" now point to v2.7; core section numbers are unchanged. v0.8 records stay readable and convert by changing the two version fields (§3).
2. Carried the v2.6 "successful steps only" doctrine (core §3.4): new §4.3 and rule R-SUCCESS. A lure nobody acted on, or a blocked attempt, is not a path step and not an incident; for #9, success means the unsafe action occurred.
3. Added a third record type, `near_miss_record` (§4.4), for attacks in which the attacker acted and a control held before any step succeeded — the near misses the application companion (§10) counts in every cluster's Key Risk Indicator, and the largest share of citizen reports to national centres. Notation `[Attempt: #X …]` (§8.8), bracket-only so that the attempted step is never a path step; Pattern and Report may follow, SRE, DRE, BRE and Impact may not (R-NEAR-MISS, enforced by the grammar). Data model: `attempted_step`, required `held_by` and `stopped_at` (V-7), optional `campaign_id`, `report_count`, `first_seen`, `last_seen` (§17.10). Near-miss records never enter incident statistics. For averted steps after successful ones, incident records gain the optional field `averted_next` (§17.3, V-8). New: §8.8, §17.10, JSON example 18.3, worked examples 19.11–19.13, decision procedure step 2, conformance 21–22, glossary entries; §1, §3, §4, §10, §11, §16, §17.1 updated. The ABNF grammar gains the NEAR_MISS_RECORD alternative.
4. Carried the v2.6 subversion test for #10 (R-SUPPLY): §8.1 note, example 19.6, §20 step 2. A defect in a legitimately supplied component is classified where it is exploited; a supplier's outage is third-party failure. §6.6 example reworded.
5. Carried the v2.7 consequence chain (core §3.4, dictionary `consequence_chain`): a BRE is reached by a causal edge (with Δt) or a normative edge (no Δt). §8.5 explains the two kinds; new rule R-BRE-EDGE; R-BRE-OP-SCOPE now speaks of a transition, causal or normative; data model §17.6 gains the optional fields `edge` and `delta_t`; both JSON examples in §18 show `edge`; example 19.6 names its normative edges; conformance 20.
6. Stated that a statutory deadline bounds the response process from awareness and is not a Δt (§8.7, R-BRE-EDGE, §16, §17.9 `timestamp_due`, §20 step 8, example 19.6 with the NIS2 Art. 23(4) deadlines).
7. Added the v2.7 entry point "BRE entered directly by a normative edge" (compliance risk, no cluster) to non-scope (§5).
8. Distinguished the Impact track from the core term Business Impact, a role a BRE holds under the organization's risk appetite (§8.6).
9. Restated the DRE stopping rule in the v2.7 wording (§8.3): a split only where states differ in the record's present standing, never by how it came to be; closure at two splits is a decision.
10. Resolved an inconsistency carried since v0.7: V-5 required a BRE on every `pure_9_record`, while §4.2, example 19.2 and proposal B.2 show a pure #9 credential disclosure with a DRE only. V-5 now requires at least one DRE or BRE annotation, or `averted_next` (example 19.13: the person acted, the payload was blocked).
11. Did not change the two incident record types, the SRE marker, PATTERN/BRE/IMPACT/REPORT catalogues (v0.2 / v0.3 / v0.2 / v0.2), the six tracks, the existing notation and grammar productions, boundary-operator requirements, or cause/consequence independence. Did not touch core TLCTC.

## 23.2 v0.8 changes from v0.7

1. Replaced the v0.7 split wording ("did the attacker reach an IT system through a technical step, or only a person") with a distinction between two **SRE kinds**: *direct* — any non-#9 cluster step, #8 and #10 included, makes the system itself depart from its owner's control; *induced* — a #9 step makes a person act, and the departure lands on the system that person operates. Bridge topology is explicitly not the criterion. `sre.kind` values renamed from `technical_compromise | induced_action` to `direct | induced`. Sections 0, 1, 4, 7, 24 reworded.
2. Replaced the v0.7 **decisive-compromise marker** with a deterministic **first-direct-SRE marker**: `+ [SRE]` is a step annotation on the first non-#9 cluster step in path order, computable from the path and validator-enforced (V-2). The v0.7 definition ("the step at which an actor first holds capability over an IT system directly, *or* the step the reporting interest pivots on where several qualify") mixed an ontic fact with a representational choice. That choice is now the optional data-model field `reporting_pivot_step` (§17.4), defaulting to the marked step. `sre.decisive` removed. R-SRE, R-SRE-EPISTEMIC, §4.1, §8.2, §11, §16, §20 step 3, conformance rule 3, glossary updated; example 19.6 moves the marker from #7 to #10, with `reporting_pivot_step` shown as the way to foreground #7.
3. Restructured the minimal grammar (§10): `<compromise-record> ::= <annotated-path> <record-annotation>*`, `<annotated-step> ::= <step> <step-annotation>*`, with `+ [SRE]`, DRE and Pattern as step annotations and BRE, Impact and Report as record annotations. The v0.7 grammar placed `<sre-annotation>` after `<tlctc-path>` while the prose required it mid-path. Validator constraints V-1…V-6 are listed explicitly; core §7 step and operator syntax is referenced, not redefined.
4. Did not change record-type names, PATTERN/BRE/IMPACT/REPORT catalogues (v0.2 / v0.3 / v0.2 / v0.2), the six tracks, boundary-operator requirements, BRE operator scoping, cause/consequence independence, or the base framework (TLCTC v2.5.1).

## 23.3 v0.7 changes from v0.6

1. Re-based the profile from TLCTC v2.1 to TLCTC v2.5.1 (dictionary `tlctc-framework.v2.5.json`, core paper v2.5.1, erratum 2026-09-10). All references to "v2.1 boundary operator" and "valid TLCTC v2.1 path" now point to the v2.5 core (§7). `framework_version` is `"2.5.1"`.
2. Changed the record-type split criterion from **SRE presence** to **path composition**. Core v2.5.1 §3.4 states that every cluster step records its own SRE — including #9, whose loss of control lands on the system the manipulated person operates — so "SRE absent" is no longer an expressible property of a record with a TLCTC anchor. `compromise_record` = path with at least one step other than #9; `pure_9_record` = a single #9 step. Record-type names unchanged.
3. Redefined `+ [SRE]` as a decisive-compromise marker (written once, after the step at which an actor holds capability over an IT system directly), mirroring the v2.5.1 erratum's reframing of the core repository's attack-path records. *(Superseded in v0.8 by the first-direct-SRE marker.)*
4. Replaced R-SRE-OPTIONAL-9 with R-SRE-9 (a `pure_9_record` SHALL NOT render the marker) and added R-SRE-EPISTEMIC (uncertainty about the marked SRE is expressed on the step per core §7.7, never by omitting the marker). Removed the v0.6 `hypothesized` SRE carve-out from the grammar, decision procedure, and conformance rule 4; the SRE annotation became required in a compromise record.
5. Aligned the DRE lane to the core v2.5 refinement tree: `C | I | Ii | If | A | Av | Ac`, parent codes legal when the refinement is not evidenced, comma as the in-bracket separator (`[DRE: C, I]`, previously `[DRE: C + I]`), stopping rule referenced. Updated §8.3, §10, §17.5, §20 step 4, §24, and example 19.6.
6. Adopted the core cause-side partition (core §3.5, R-SCOPE) as the TLCTC+ scope boundary: Failure / external event, Error in Use, and Abuse of Rights are named as explicit non-scope; added an "Abuse of Rights is not #1" counter-example in §5 and made R-SCOPE the first step of the §20 decision procedure. Relevant to fraud teams: internal fraud inside a conferred mandate is not a TLCTC+ record.
7. Carried the R-CRED self-issued-identity proviso into §4.2 and example 19.3: credential use is #4 only where the identity claimed is not the presenter's own; out-of-scope self-enrolment is #1.
8. Data model §17.4: removed `sre.present` (always true under v2.5.1); added `kind`, `decisive`, and `epistemic`; dropped `hypothesized` from `status`. Both JSON examples in §18 updated, with `framework_version` added. *(`decisive` removed again in v0.8.)*
9. Added the core epistemic and unresolved-step operators (`[conf=low]`, `[inferred]`, `?`, `…`) to §8.1 as admissible in a `compromise_record` path under R-UNRES-2/-5; a `pure_9_record` admits none.
10. Updated worked-example prose (19.1, 19.2, 19.4, 19.6, 19.7, 19.10) from "No SRE" to "no `+ [SRE]` marker; the #9 SRE is implicit", and noted per-step SRE counts where a path has several steps.
11. Did not change PATTERN, BRE, IMPACT, or REPORT catalogues (versions remain v0.2 / v0.3 / v0.2 / v0.2), the six tracks, boundary-operator requirements, BRE operator scoping, or cause/consequence independence.
12. Did not touch core TLCTC — this is a TLCTC+ profile change that follows the core; it does not modify the core.

## 23.4 v0.6 changes from v0.5

1. Collapsed the three v0.5 case classes (`core_cyber_incident`, `hybrid_cyber_enabled_harm`, `pure_9_digital_harm`) into two structural record types split on SRE presence: `compromise_record` and `pure_9_record`. The split now matches the formal grammar in §10, which already enumerated only two record variants.
2. Renamed the grammar non-terminal `<cyber-record>` to `<compromise-record>` to align with the new record_type name. `<pure-9-record>` unchanged.
3. Retained "hybrid cyber-enabled fraud" as descriptive prose for compromise records with consequence-side BRE dominance (BRE-FIN.*, BRE-ENT.*, BRE-CUS.*). It is no longer a record_type; it is a sub-pattern derivable from the BRE family selection.
4. Reworded conformance rule 4 to cover SRE omission in two clean cases: `pure_9_record`, or `compromise_record` with `sre.status = hypothesized`.
5. Updated §20 decision procedure step 3 to map directly to the two record_types.
6. Updated both JSON examples in §18 to use the new record_type names and `tlctc_plus_version = 0.6`.
7. Added one glossary entry pointing to §17.1 for the new record_type names.
8. Did not change PATTERN, BRE, IMPACT, or REPORT catalogues (versions remain v0.2 / v0.3 / v0.2 / v0.2).
9. Did not change the six tracks, any R-* rule (other than rule 4's editorial reword), boundary operator requirements, BRE operator scoping, or cause/consequence independence.
10. Did not touch core TLCTC v2.1 — this is a TLCTC+ profile change, not a taxonomy change.

## 23.5 v0.5 changes from v0.4

1. Condensed the document into a shorter implementation specification.
2. Added a peer-facing rationale section for expected interest groups.
3. Kept the three case classes: `core_cyber_incident`, `hybrid_cyber_enabled_harm`, and `pure_9_digital_harm` (later collapsed in v0.6).
4. Kept the six-track model.
5. Kept the Pattern/BRE/Impact/Report separation.
6. Kept explicit SRE semantics and pure-#9 SRE omission rule.
7. Kept mandatory boundary operators for #8/#9/#10 in TLCTC+ records.
8. Kept BRE operator scoping inside `[BRE: ...]`.
9. Kept cause/consequence independence.
10. Removed most detailed v0.1–v0.4 migration prose from the main specification.
11. Did not add, remove, or renumber catalogue codes.

---

# 24. Glossary

## `compromise_record` / `pure_9_record` / `near_miss_record`

The three TLCTC+ record types. The two incident types (since v0.6; split on path composition since v0.7): `compromise_record` carries a TLCTC path with at least one direct SRE and marks the first of them with `+ [SRE]`; `pure_9_record` carries a single #9 step whose SRE is induced and renders no marker. `near_miss_record` (v0.9) carries one attempted step in `[Attempt: …]` and no SRE. See §4, §17.1.

## Attempt

The notation `[Attempt: #X …]` that opens a near-miss record (§8.8). It encloses one classified cluster step, the cluster the attack aimed at, and is bracket-only because nothing succeeded: it is never a path step.

## `averted_next`

Optional field on an incident record naming the cluster of a next step that a control is known to have averted (§4.4, §17.3). Counted as a near miss of that cluster.

## Near miss

An attack in which the attacker acted but a control held before the step succeeded (application companion §10). Counted per cluster in the Key Risk Indicator alongside incidents, never as an incident. In TLCTC+ a `near_miss_record` where nothing succeeded, or `averted_next` on an incident record.

## Abuse of Rights

An intended action inside an entitlement an accountable grantor genuinely conferred, used against its purpose (core §3.5, R-SCOPE). Operational risk: no cluster, no SRE, the consequence chain begins at the DRE. Outside TLCTC+ scope. Not an eleventh cluster.

## Direct SRE / Induced SRE

TLCTC+ distinction between two kinds of System Risk Event, both defined by the core (§3.4). *Direct:* a non-#9 cluster step makes the system itself depart from its owner's control (#8 and #10 included). *Induced:* a #9 step makes a person act, and the departure lands on the system that person operates. The kind is a property of the step's cluster, not a reporting choice.

## First direct SRE

The SRE of the first non-#9 cluster step in path order. Marked once with `+ [SRE]` (R-SRE, V-2). Computable from the path; carries no reporting judgement.

## Reporting pivot

The compromise a record chooses to foreground (`reporting_pivot_step`, §17.4). A representational choice, independent of the marker; defaults to the marked step.

## BRE — Business Risk Event

A discrete, observable business, citizen, service, legal, regulatory, third-party, or organizational event on the consequence side, reached from a DRE or a preceding BRE by a causal or a normative edge (core §3.4, v2.7).

## Causal edge / Normative edge

The two ways a BRE is reached (core §3.4, v2.7; R-BRE-EDGE). *Causal:* the BRE is brought about by the preceding event, after a Δt. *Normative:* a duty arises or a norm is violated; nothing propagates and no Δt is defined. A statutory deadline belongs to neither: it bounds the response process from awareness and is recorded on the Report track.

## DRE — Data Risk Event

An outcome recorded on the record that changed state, never a step and never a classification input (Axiom III). Codes form the core refinement tree (since v2.5): `C` (disclosed); `I` with refinements `Ii` (incorrect state) and `If` (misattributed state); `A` with refinements `Av` (unavailable — gone or unreachable) and `Ac` (inaccessible — present but unusable).

## Impact

A quantified or qualified measurement attached to SRE, DRE, or BRE. Not the core term Business Impact, which is a role a terminal BRE holds under an organization's risk appetite (§8.6).

## Pattern

Cause-side metadata describing the scam, fraud, extortion, manipulation, or reporting narrative instantiated by a TLCTC step.

## Report

A procedural artefact, report filing, workflow stage, authority communication, or routing state.

## Successful step

A cluster step that achieved its effect; only successful steps are recorded (core §3.4, R-SUCCESS). For #9, the manipulated person performed the unsafe action. Attempts and blocked steps are near misses, never path steps (§4.3, §4.4).

## SRE — System Risk Event

Any risk event at the system altitude — the point at which a system's behaviour, privileges, data, or trust relationships depart from what its owner controls. The SRE the framework defines is System Compromise — Loss of Control, reached only through cluster steps; every classified step records one (core §3.4). System Failure sits at the same altitude with no actor holding capability and is operational risk, not TLCTC+ scope. The cyber Bow-Tie central event.

## Technical Identity

A non-human principal or identity artifact such as a service account, API key, machine credential, OAuth client secret, certificate, robot/RPA account, or service ticket. Credential use remains #4 on the cause side, provided the identity claimed is not the presenter's own (R-CRED); the consequence-side BRE depends on observed harm.

## TLCTC+

A TLCTC-anchored reporting profile for cyber incidents, hybrid cyber-enabled harms, and pure #9 digital harms.

