# TLCTC+ for NCSCs and CERTs: A National Reporting Extension Proposal

**Author:** Bernhard Kreinz
**Framework Version:** TLCTC v2.1
**Document Version:** v0.4 (proposal, aligned with TLCTC+ specification v0.4)
**License:** CC BY 4.0
**Status:** Working proposal

**Core thesis:** Keep TLCTC pure. Extend the reporting layer.

> **Companion document:** This is the **policy proposal** — the case for adopting TLCTC+, the governance model, the adoption path. For the **implementation specification** (grammar, conformance rules, PATTERN/BRE/IMPACT/REPORT catalogues, JSON record formats, decision procedure), see [`tlctc-plus-specification.md`](tlctc-plus-specification.md). The proposal makes the case; the spec defines how to build it.
>
> Notation used throughout this proposal follows the TLCTC+ v0.4 grammar: scam, fraud, and manipulation playbook labels are recorded as `[Pattern: PATTERN-XXX.YY ...]` on the cause-side step; consequence events are recorded as structured BRE codes (`+ [BRE: BRE-XXX.YY ...]`); the cyber Bow-Tie centre is recorded as `+ [SRE]`; measurements as `+ [Impact: ...]`; procedural artefacts as `+ [Report: ...]`. Free-text BRE labels from the v0.1 draft of this proposal (`+ [BRE: Romance Scam]`) are deprecated — see spec §7 R-V01-MIGRATION for the migration path.

---

## 1. Executive Summary

National Cyber Security Centres (NCSCs) and CERTs need a stable language that supports more than one mission at the same time. They must classify cyber incidents affecting IT systems and critical sectors, but they are also increasingly expected to receive and process reports about broader digitally mediated harms such as scams, fraud, impersonation, and payment diversion.

Core TLCTC already provides a cause-oriented language for cyber threats against IT systems. That is its strength. It classifies the cause-side threat by the generic vulnerability initially exploited and keeps threats, data risk events, and business consequences separate.

This proposal argues that NCSCs and CERTs should not weaken or redefine that core model. Instead, they should adopt a controlled extension profile called **TLCTC+**.

TLCTC+ is not a new taxonomy. It is not a replacement for TLCTC. It is a national reporting extension that allows NCSCs and CERTs to capture broader digitally mediated harms inside the same analytical ecosystem without destroying the semantic discipline of the core framework.

The extension starts with one very specific gap: manipulation-driven digital harms that are clearly relevant to national centres but do not always culminate in a classical cyber incident against an IT system. The natural anchor for that gap is **#9 Social Engineering**.

The proposal is therefore simple:

- keep the ten TLCTC clusters unchanged
- preserve the Bow-Tie separation between causes, System Risk Events, Data Risk Events, and Business Risk Events
- introduce TLCTC+ as an intake and reporting profile for NCSCs and CERTs
- record scam, fraud, and manipulation playbooks as **Pattern** metadata on the cause-side step (bracket-only), and record the actual business or citizen consequence as a structured **BRE** code on the consequence side

Recommended notation (TLCTC+ v0.4):

```
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

All consequence-side tracks (`+ [SRE]`, `+ [DRE: ...]`, `+ [BRE: ...]`, `+ [Impact: ...]`, `+ [Report: ...]`) reuse the existing additive Bow-Tie grammar that TLCTC already applies to `+ [DRE: ...]`. Pattern is the only TLCTC+ annotation that attaches in bracket-only form (no `+`), because Pattern is cause-side metadata qualifying the step rather than a consequence-side event. No core TLCTC operator is overloaded, and no new symbol is introduced into the path grammar (the v2.1 transit operator `⇒` is left untouched).

The result is a model that allows national centres to use one language across:

- core cyber incidents
- hybrid cyber-enabled harms
- digitally mediated non-SRE harms

without pretending these are all the same thing.

---

## 2. Problem Statement

Most national reporting ecosystems suffer from a language problem before they suffer from a data problem.

Reports from critical sectors, citizen hotlines, public awareness channels, incident notification regimes, and fraud-related reporting mechanisms usually mix several semantic layers:

- threat categories
- incident labels
- crime labels
- actor labels
- consequence labels
- control language
- sector-specific terminology

The result is predictable:

- weak comparability across reports
- inconsistent national statistics
- blurred boundaries between cyber incidents and digital crime
- repeated semantic debates every year
- difficulty aligning awareness, intake, triage, and policy functions

Some cases are clearly cyber incidents against IT systems. Others are clearly manipulation-driven fraud or scam cases conducted through digital channels. Others again combine both worlds. NCSCs and CERTs need a reporting structure that can cope with all three realities without collapsing them into one vague bucket.

This proposal addresses that structural problem.

---

## 3. Scope of This Proposal

This proposal applies to the work of NCSCs and CERTs in the following contexts:

- mandatory incident reporting
- cyber incident intake from critical sectors
- public and citizen-facing reports of digitally mediated harm
- national incident statistics and trend reporting
- warning, awareness, and prevention messaging
- triage and referral between cyber, fraud, and law-enforcement workflows

This proposal does **not** aim to:

- redefine criminal-law categories
- replace sector-specific legal obligations
- replace law-enforcement taxonomies
- create a universal taxonomy for all crime
- change the normative semantics of core TLCTC

Its purpose is narrower and more practical: to define a stable reporting extension that national centres can use without reopening the same semantic arguments every year.

---

## 4. Normative Design Principle

**TLCTC+ shall preserve TLCTC core semantics unchanged.**

This means:

- threats remain on the cause side
- System Risk Events (Loss of Control / System Compromise) remain the cyber Bow-Tie central event
- Data Risk Events remain distinct from threats
- Business Risk Events remain consequence-side events
- Patterns remain cause-side narrative metadata; Impacts remain measurements; Reports remain procedural artefacts
- the ten TLCTC clusters remain unchanged
- TLCTC+ is an extension profile for intake and reporting, not a new threat taxonomy

This principle is the foundation of the entire proposal. If TLCTC+ weakens the core semantics, it fails.

---

## 5. Why NCSCs and CERTs Need TLCTC+

NCSCs and CERTs sit at the intersection of several reporting worlds.

They need to understand cyber incidents in critical sectors. They need to support coordination and situational awareness. They need to publish advice to the public. They often receive reports that are not classical cyber incidents at all, yet are still clearly digital, harmful, and prevention-relevant.

Examples include:

- romance scams
- fake support scams
- CEO fraud and payment diversion
- impersonation-driven induced payments
- account-takeover-enabled financial harm
- digitally mediated coercion and extortion

These cases matter operationally. They matter statistically. They matter politically. But they do not all fit naturally into the same reporting grammar.

TLCTC solves the cause-language problem for cyber threats against IT systems. TLCTC+ extends the reporting model so national centres can capture adjacent digitally mediated harms without polluting the threat taxonomy itself.

---

## 6. Core Thesis

Core TLCTC classifies cyber threats against IT systems.

**TLCTC+ extends national reporting so that digitally mediated harms can be recorded in the same analytical ecosystem without corrupting the TLCTC threat model.**

---

## 7. The Structural Gap

The main gap appears where national centres must handle cases that are:

- digital
- harmful
- prevention-relevant
- nationally reportable

but do **not** meaningfully enter the standard cyber-incident chain of IT-system compromise.

This is most visible in manipulation-driven cases. A person is deceived through email, chat, social media, phone, or another digital medium. The manipulation may lead to payment, disclosure, approval, transfer, or another harmful act. But the case may involve no malware, no exploitation, no system compromise, and no meaningful Data Risk Event in the classical cyber sense.

These cases still need a place in national reporting.

The proposal is that this place should **not** be created by inventing new top-level threats. It should be created by extending the reporting grammar around the existing framework.

---

## 8. Why the Extension Anchors on #9

The natural anchor point for TLCTC+ is **#9 Social Engineering**.

That is not because #9 is weak or incomplete. It is because #9 already identifies the cause-side vulnerability correctly: human psychology.

In many hybrid or broader digital-harm cases, the cause-side classification is already available:

- the attacker manipulates a human
- the generic vulnerability is psychological
- the cause-side step is `#9`

The problem is not how to classify the cause. The problem is how to record the downstream harm when there is no meaningful transition into the standard cyber-incident model.

That is why the first formal extension is anchored here. The mechanism itself — attaching `[Pattern: ...]` to a cause-side step and appending `+ [SRE]`, `+ [DRE: ...]`, `+ [BRE: ...]`, `+ [Impact: ...]`, and `+ [Report: ...]` to the path — is fully general and may be applied after any terminal cause-side step (e.g., `#4`, `#1`, `#7`) when the nationally relevant outcome is best captured as a Business Risk Event. The deliberate scope choice for the initial TLCTC+ profile is to begin at `#9` because that is where the structural gap between cyber-incident reporting and digitally mediated-harm reporting is widest.

---

## 9. Proposed Extension Rule

**TLCTC+ introduces six tracks — Cause / SRE / DRE / BRE / Impact / Report — layered over a TLCTC cause-side path, for cyber incidents, hybrid cyber-enabled harms, and digitally mediated harms that do not meaningfully enter core IT-system compromise analysis.**

Recommended notation (v0.4 — every BRE is a structured catalogue code, every scam/fraud playbook is a Pattern, every #8/#9/#10 step carries a boundary operator):

```
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
```

```
#9 ||[phone][@External→@Citizen]|| [Pattern: PATTERN-FIN.13 Fake Tech Support Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
```

```
#9 ||[email][@External→@Org]|| [Pattern: PATTERN-FIN.21 Business Email Compromise]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
```

```
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.18 Sextortion Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
```

### Semantics

- `→` remains the core TLCTC operator for cause-side attack-path progression
- `||[ctx][@A→@B]||` remains the v2.1 boundary operator (REQUIRED on every bridge-cluster step under TLCTC+ R-9-BOUNDARY)
- `+ [SRE]` is the cyber Bow-Tie central event (Loss of Control / System Compromise)
- `+ [DRE: X]` remains the notation for Data Risk Events
- `+ [BRE: BRE-XXX.YY ...]` is the TLCTC+ Business Risk Event annotation, structurally coded against the BRE catalogue (spec §11)
- `[Pattern: PATTERN-XXX.YY ...]` is bracket-only (no leading `+`) and attaches to a cause-side step — it carries the scam, fraud, or manipulation playbook label
- `+ [Impact: IMPACT-XXX.YY = <value>]` carries quantified or qualified measurements
- `+ [Report: REPORT-XXX.YY ...]` carries procedural / regulatory reporting artefacts

The choice to reuse the existing additive `+ [...]` grammar for consequence-side annotations is deliberate. It places SRE, DRE, BRE, Impact, and Report on the same grammatical footing — all are consequence-side events of the Bow-Tie model — without inventing a new operator class and without overloading any existing operator (in particular, the v2.1 transit operator `⇒` is left untouched). Pattern is the one intentional asymmetry: it is cause-side metadata, so it attaches bracket-only, aligned with other v2.1 step-level annotations such as `[conf=low]`, `[inferred]`, and `[Δt=...]`.

A hybrid case may carry SRE, DRE, BRE, and Impact together:

```
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-FIN.21 Business Email Compromise]
+ [DRE: C] → #4 + [SRE]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm → BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 80,000]
```

In this case, `+ [DRE: C]` records the cyber-incident data consequence (credential disclosure during phishing), `+ [SRE]` records the central cyber event (loss of control of the mailbox), `+ [BRE: ...]` records the nationally reportable downstream harm chain, and `+ [Impact: ...]` records the measured loss.

---

## 10. Why Pattern + BRE Are the Right Destinations

Romance scam, fake support scam, CEO fraud, and sextortion are not threat clusters. They are not generic vulnerabilities. They are not causes in the TLCTC sense. The cause-side classification remains `#9`.

But these labels are also not, by themselves, business events. A "romance scam" describes the attacker's manipulation narrative; the actual reportable event is the authorized push payment that follows. TLCTC+ v0.4 therefore splits the two:

- the scam/fraud/manipulation playbook → **Pattern** (cause-side, bracket-only metadata)
- the observable business or citizen consequence → **BRE** (consequence-side, structured catalogue code)
- the measured magnitude of harm → **Impact** (consequence-side measurement)

For TLCTC+ purposes the BRE catalogue (spec §11) is organized into nine families that cover:

- service / operational consequence (BRE-SVC)
- customer / citizen / market consequence (BRE-CUS)
- financial events — authorized and unauthorized (BRE-FIN)
- identity / account harm (BRE-ENT)
- legal consequence (BRE-LGL)
- regulatory / supervisory consequence (BRE-REG)
- reputation / public communication (BRE-REP)
- third-party / ecosystem consequence (BRE-3P)
- internal organizational consequence (BRE-ORG)

A BRE family is independent of cause-side cluster identity (spec §3.9 / R-CAUSE-CONSEQUENCE-INDEPENDENCE). The same `#4` step may produce BRE-ENT (when a human or organizational principal is the harmed entity), BRE-SVC (when the stolen credential is a service account that controls a service), BRE-FIN, BRE-DATA, or none of these — recorded from the actual observed harm, not auto-derived from the cluster.

This does not change TLCTC core semantics. It extends the reporting vocabulary that NCSCs and CERTs need in practice.

---

## 11. Boundary Conditions

TLCTC+ must **not** do any of the following:

- create new top-level threat clusters
- redefine scam labels as threats
- collapse Business Risk Events into threat categories
- replace law-enforcement taxonomies
- replace criminal-law categories
- weaken the cause-effect separation of TLCTC
- overload the meaning of the core sequence operator `→`

TLCTC+ must remain an extension profile around the framework, not a mutation of the framework.

---

## 12. Case Typology for NCSCs and CERTs

TLCTC+ supports three clearly separated case classes, mirrored by the three `record_type` values in spec §15.1.

### A. Core Cyber Incident (`record_type: core_cyber_incident`)

A case that meaningfully fits the core TLCTC incident logic: a TLCTC attack path leads to a System Risk Event, may produce DREs, and may cascade into BREs.

Example:

```
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: Ac]
+ [BRE: BRE-SVC.11 Payment Function Unavailable]
+ [Impact: IMPACT-OPS.11 Downtime Duration = 6 hours]
```

### B. Hybrid Cyber-Enabled Harm (`record_type: hybrid_cyber_enabled_harm`)

A case in which a core TLCTC chain exists, but the nationally or regulatorily dominant interest is the consequence side (BRE chain and impact measurement).

Example:

```
#9 ||[email][@External→@Org]|| + [DRE: C] → #4 + [SRE]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm → BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 80,000]
```

### C. Pure #9-Anchored Digital Crime (`record_type: pure_9_digital_crime`)

A case that is digitally mediated and harmful, but no IT system is compromised — so no SRE is recorded. A DRE MAY be recorded only when the `#9` step itself directly causes data disclosure (typically `+ [DRE: C]` for credential or PII handover during phishing); if the disclosed artefact is later used, the case transitions to class B.

Example (no DRE):

```
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

This three-part typology allows national centres to keep one reporting ecosystem without forcing false equivalence between all digital harms.

---

## 13. Pattern, BRE, and Impact Catalogues for National Use

TLCTC+ defines controlled catalogues for NCSC and CERT reporting. The canonical catalogues are normative in the specification (spec §10 PATTERN, §11 BRE, §12 IMPACT, §13 REPORT) and are versioned independently of the document (currently BRE catalogue v0.3, PATTERN / IMPACT / REPORT v0.2, document v0.4 — see spec §0.1).

The point of separating these into distinct namespaces is that a v0.1 entry such as "Romance Scam" was three things at once: a scam narrative, a business event, and (often) an implied financial loss. v0.4 splits them so that statistics and triage can address each dimension independently:

### Pattern catalogue (cause-side narrative — what the attacker did)

Examples from spec §10:

- `PATTERN-FIN.11` Romance / Relationship Scam
- `PATTERN-FIN.13` Fake Tech Support Scam
- `PATTERN-FIN.21` Business Email Compromise
- `PATTERN-FIN.22` Invoice / Mandate Fraud
- `PATTERN-FIN.25` CEO / Executive Impersonation
- `PATTERN-ID.11` Phishing for Credentials
- `PATTERN-EXT.11` Sextortion Threat

### BRE catalogue (consequence-side event — what happened to the victim or business)

Examples from spec §11:

- `BRE-SVC.11` Payment Function Unavailable
- `BRE-CUS.11` Customer Account Closure
- `BRE-FIN.11` Authorized Push Payment Made
- `BRE-FIN.21` Unauthorized Bank Transfer Executed
- `BRE-ENT.13` Email Account Takeover Harm
- `BRE-LGL.11` Customer Legal Claim
- `BRE-REG.11` Mandatory Notification Obligation Triggered
- `BRE-REP.11` Public Warning Issued
- `BRE-ORG.12` Business Continuity Plan Activated

### Impact catalogue (consequence-side measurement — how much it hurt)

Examples from spec §12:

- `IMPACT-FIN.12` Direct Fraud Loss
- `IMPACT-FIN.16` Customer Churn Loss
- `IMPACT-OPS.11` Downtime Duration
- `IMPACT-CUS.11` Number of Customers Affected
- `IMPACT-REG.15` Number of Legal Claims
- `IMPACT-DATA.11` Records Exposed

National centres may add national aliases or extend any catalogue under their own governance (see §16). The important point is not the perfect label list. The important point is the structural separation: cause-side classification remains TLCTC; scam narratives live in Pattern; business events live in BRE; magnitudes live in Impact; regulatory filings live in Report.

---

## 14. Intake and Triage Workflow

TLCTC+ should be used through a simple triage logic, mirroring the 8-step decision procedure in spec §18.

### Decision Flow

1. **TLCTC path?** Is there a TLCTC-classifiable cyber threat against an IT system? If yes, record the TLCTC path (`#1`–`#10`) with all required v2.1 boundary operators on bridge-cluster steps.
2. **#9 anchor?** If there is no TLCTC cyber path but a human was psychologically manipulated through a digital channel, record `#9` with its REQUIRED boundary operator (R-9-BOUNDARY). If there is neither, the case is outside TLCTC+.
3. **SRE?** Did Loss of Control / System Compromise occur? If yes, attach `+ [SRE]`. If the case is pure-#9 digital harm with no IT-system compromise, omit SRE.
4. **DRE?** Attach `+ [DRE: C | I | Ac | Av]` for any data risk events observed. A DRE on a pure-#9 step is permitted only when the social-engineering act itself directly causes disclosure (typically `+ [DRE: C]`).
5. **Pattern?** Attach `[Pattern: PATTERN-XXX.YY ...]` (bracket-only) on the cause-side step for any scam, fraud, manipulation, or playbook label.
6. **BRE chain?** Attach `+ [BRE: BRE-XXX.YY → BRE-XXX.YY + BRE-XXX.YY]` for the observed business, citizen, regulatory, or organizational consequence(s).
7. **Impact?** Attach `+ [Impact: IMPACT-XXX.YY = <value>]` for any measured magnitude (financial, operational, customer, regulatory, reputation, data).
8. **Report?** Attach `+ [Report: REPORT-XXX.YY ...]` for any regulatory or procedural filing produced. If an obligation was triggered, also attach the regulatory BRE (e.g., `+ [BRE: BRE-REG.11]`).

This workflow helps keep intake disciplined while still supporting the broader mission of national centres.

---

## 15. Data Model and Reporting Format

TLCTC+ should be machine-addressable and easy to integrate into national reporting portals.

The spec (§15 Data Model, §16 Example JSON Records) defines three record types — these are the canonical names national portals should adopt:

- `core_cyber_incident`
- `hybrid_cyber_enabled_harm`
- `pure_9_digital_crime`

Each record carries six tracks (spec §4) — Cause, SRE, DRE, BRE, Impact, Report — plus metadata (case ID, intake source, sector, country, timestamps, confidence). Pattern fields attach to cause-side steps.

### Example Records (illustrative; canonical examples in spec §16)

#### Core Cyber Incident
```json
{
  "case_id": "case-001",
  "record_type": "core_cyber_incident",
  "tlctc_plus_version": "0.4",
  "tlctc_path": "#9 ||[email][@External→@Org]|| → #7",
  "sre": { "present": true, "status": "confirmed", "linked_to_step": "step-2" },
  "dre": [ { "type": "Ac", "linked_to_sre": true } ],
  "bre_chain": {
    "expression": "BRE-SVC.11 → BRE-ORG.12",
    "nodes": [
      { "code": "BRE-SVC.11", "label": "Payment Function Unavailable" },
      { "code": "BRE-ORG.12", "label": "Business Continuity Plan Activated" }
    ]
  },
  "impact": [
    { "code": "IMPACT-OPS.11", "label": "Downtime Duration", "value": 6, "unit": "hours" }
  ],
  "sector": "energy",
  "mandatory_reporting": true
}
```

#### Hybrid Cyber-Enabled Harm
```json
{
  "case_id": "case-003",
  "record_type": "hybrid_cyber_enabled_harm",
  "tlctc_plus_version": "0.4",
  "tlctc_path": "#9 ||[email][@External→@Org]|| + [DRE: C] → #4",
  "patterns": [ { "code": "PATTERN-FIN.22", "label": "Invoice / Mandate Fraud" } ],
  "sre": { "present": true, "status": "confirmed", "linked_to_step": "step-2" },
  "dre": [ { "type": "C", "linked_to_step": "step-1" } ],
  "bre_chain": {
    "expression": "BRE-ENT.13 → BRE-FIN.11",
    "nodes": [
      { "code": "BRE-ENT.13", "label": "Email Account Takeover Harm" },
      { "code": "BRE-FIN.11", "label": "Authorized Push Payment Made" }
    ]
  },
  "impact": [
    { "code": "IMPACT-FIN.12", "label": "Direct Fraud Loss", "amount": 80000, "currency": "EUR" }
  ],
  "sector": "manufacturing",
  "mandatory_reporting": false
}
```

#### Pure #9 Digital Crime
```json
{
  "case_id": "case-002",
  "record_type": "pure_9_digital_crime",
  "tlctc_plus_version": "0.4",
  "tlctc_anchor": "#9 ||[messaging][@External→@Citizen]||",
  "patterns": [ { "code": "PATTERN-FIN.11", "label": "Romance / Relationship Scam" } ],
  "sre": { "present": false },
  "dre": [],
  "bre_chain": {
    "expression": "BRE-FIN.11",
    "nodes": [ { "code": "BRE-FIN.11", "label": "Authorized Push Payment Made" } ]
  },
  "impact": [
    { "code": "IMPACT-FIN.12", "label": "Direct Fraud Loss", "amount": 4500, "currency": "CHF" }
  ],
  "report": [ { "code": "REPORT-NCSC.11", "label": "Voluntary NCSC/CERT Report Filed" } ],
  "sector": "citizen",
  "mandatory_reporting": false
}
```

This should be treated as a reporting profile layered above the core TLCTC architecture, not as a replacement for it.

---

## 16. Governance Model

Ownership should be split clearly.

### Core TLCTC
- remains external and canonical
- is not modified by national reporting preferences

### TLCTC+ National Profile
- maintained by the NCSC/CERT community
- versioned separately from core TLCTC
- documented as an extension profile

### TLCTC+ Consequence Catalogues (PATTERN / BRE / IMPACT / REPORT)
- versioned independently of the TLCTC+ specification document (spec §0.1)
- canonical codes maintained by the TLCTC+ specification owner
- national aliases and national extensions adjustable under national governance
- harmonizable across borders without changing TLCTC core
- candidate for future extraction into a shared consequence-side specification once TLSFC reaches publication readiness (spec §20)

This separation allows evolution where needed without destabilizing the threat taxonomy.

---

## 17. Benefits

Adopting TLCTC+ offers several practical benefits.

### Semantic Benefits
- one language across cyber incident intake and broader digital-harm intake
- cleaner separation between causes and consequences
- less semantic drift over time
- fewer recurring debates about scope and terminology

### Operational Benefits
- comparable national statistics
- better triage between cyber, fraud, and law-enforcement workflows
- better routing and escalation decisions
- cleaner linkage between incident analysis and public warnings

### Strategic Benefits
- stronger basis for mandatory reporting aggregation
- improved national situational awareness
- better policy communication
- a stable reporting architecture that can survive annual changes in buzzwords

---

## 18. Risks and Mitigations

### Risk 1: TLCTC+ Becomes a Vague "Everything Digital" Bucket
**Mitigation:** strict scope, clear case typology, and the limited starting anchor at `#9`.

### Risk 2: Conflict With Legal or Law-Enforcement Categories
**Mitigation:** define TLCTC+ explicitly as a reporting grammar, not a legal ontology.

### Risk 3: Semantic Leakage Back Into TLCTC Core
**Mitigation:** keep the ten clusters unchanged and version TLCTC+ separately.

### Risk 4: BRE Vocabulary Inflation
**Mitigation:** use a controlled label set with governance and periodic review.

### Risk 5: Notation Drift Between TLCTC and TLCTC+
**Mitigation:** TLCTC+ introduces no new path operator. All consequence-side annotations (`+ [SRE]`, `+ [DRE: ...]`, `+ [BRE: ...]`, `+ [Impact: ...]`, `+ [Report: ...]`) reuse the existing additive Bow-Tie grammar already used by `+ [DRE: ...]` and are restricted to consequence-side annotations only. Pattern is bracket-only (`[Pattern: ...]`, no `+`) and aligns with existing v2.1 step-level annotations (`[conf=low]`, `[inferred]`, `[Δt=...]`). BRE annotations MUST NOT appear as cause-side steps and MUST NOT be referenced as if they were threat clusters. The v2.1 transit operator `⇒` retains its existing meaning unchanged. Stripping all TLCTC+ consequence-side annotations from a conformant record MUST recover a valid TLCTC v2.1 path or `#9` anchor (spec R-RECOVERABILITY).

### Risk 6: Free-Text BRE Labels Returning in National Implementations
**Mitigation:** spec R-V01-MIGRATION forbids free-text BRE strings in v0.3-or-later records. Every BRE is a structured code from the catalogue (`BRE-XXX.YY`). National centres can extend the catalogue or add national aliases, but cannot accept free-text BREs in conformant records.

### Risk 7: Auto-Filling Consequence Side From Cluster Identity
**Mitigation:** spec R-CAUSE-CONSEQUENCE-INDEPENDENCE (§3.9, §7) makes the cause-side cluster and consequence-side BRE family independent dimensions. Intake systems and mappers MUST NOT auto-derive a BRE family from the cluster. The same `#4` step may produce BRE-ENT, BRE-SVC, BRE-FIN, or none — recorded from observed harm.

---

## 19. Proposed Adoption Path

This proposal is intentionally designed so NCSCs and CERTs do not need years of conceptual debate before using it.

### Phase 1 — Adopt Core TLCTC
Use TLCTC as the stable cause-oriented taxonomy for cyber threats against IT systems.

### Phase 2 — Define TLCTC+
Publish a national extension profile for broader digitally mediated harms.

### Phase 3 — Start Narrow
Begin national adoption with the pure-`#9` digital-harm class — `[Pattern: PATTERN-XXX.YY] + [BRE: BRE-XXX.YY]` anchored at `#9` with its required boundary operator.

### Phase 4 — Adopt the Consequence Catalogues
Adopt the canonical PATTERN, BRE, IMPACT, and REPORT catalogues from the specification, and publish any national aliases or national extensions under documented governance.

### Phase 5 — Integrate Into Portals and Statistics
Implement the model in forms, databases, trend reporting, and public awareness workflows.

### Phase 6 — Review Without Reopening the Core
Review the extension annually, but do not reopen the semantics of core TLCTC unless the canonical framework itself changes.

---

## 20. Formal Recommendation

NCSCs and CERTs should adopt TLCTC as the stable cause-oriented taxonomy for cyber threats against IT systems and establish **TLCTC+** as a controlled national reporting extension profile for digitally mediated harms.

TLCTC+ should begin with the `[Pattern: PATTERN-XXX.YY] + [BRE: BRE-XXX.YY]` reporting form anchored at `#9 Social Engineering` (with its required v2.1 boundary operator), allowing manipulation-driven scam and fraud cases to be recorded in the same analytical ecosystem without compromising TLCTC's semantic integrity. The full six-track form — Cause / SRE / DRE / BRE / Impact / Report — supports core cyber incidents and hybrid cyber-enabled harms in the same vocabulary.

The guiding principle is simple:

**Keep TLCTC pure. Extend the reporting layer.**

---

## 21. Why Not Separate #9 Into "Vulnerabilities of Humans"?

A natural objection is this: if `#9 Social Engineering` is based on human psychology, why not split it further into greed, lust, fear, unattention, authority bias, curiosity, loneliness, fatigue, and similar human weaknesses?

The answer is: **not at the strategic layer**.

The purpose of TLCTC is to provide a stable cyber threat language. At the top level, `#9` already defines the generic vulnerability correctly: human psychology. Splitting that strategic cluster into greed, lust, fear, distraction, and similar factors would move the model away from a stable threat taxonomy and toward an open-ended psychology taxonomy.

There are three reasons not to do that here.

### 1. It becomes too complex
Real social-engineering cases rarely rely on only one human factor. They combine urgency with fear, trust with loneliness, authority with obedience, curiosity with ignorance, or greed with optimism. The categories overlap heavily.

### 2. The factors are chainable
In many real cases, one psychological factor leads to another. Curiosity leads to engagement. Engagement creates trust. Trust enables dependency. Dependency enables payment or disclosure. This makes neat strategic categorization unstable.

### 3. It is the wrong professional layer
NCSCs and CERTs need a usable reporting language, not a full behavioral-science taxonomy. The deeper decomposition of human vulnerabilities may one day be useful at an operational or research level, but it should not burden the common strategic grammar needed for national intake and reporting.

So the correct design choice is:

- keep `#9` unchanged at the strategic level
- allow future refinement only at a lower operational layer if a strong empirical and methodological basis exists
- do not force national centres into years of debate over psychological micro-taxonomies

A concise formulation is:

**NCSCs need a threat language, not a psychology taxonomy.**

---

## 22. Suggested Appendix Material

A final published version of this proposal could include the following appendices:

### Appendix A — Notation Rules

Cause-side (unchanged from TLCTC v2.1):
- `→` core TLCTC cause-side sequence
- `+` parallel cluster execution in `(#X + #Y)` groups
- `||[ctx][@A→@B]||` boundary operator — REQUIRED on every #8/#9/#10 step under TLCTC+ R-9-BOUNDARY
- `||[ctx][@A⇒@C→@B]||` v2.1 transit operator (`⇒`) — unchanged
- `|[type][@from→@to]|` v2.1 intra-system boundary — unchanged
- `?` and `…` v2.1 unresolved-step operators — unchanged
- `[Δt=...]`, `[conf=low]`, `[inferred]` v2.1 step-level annotations — unchanged

Cause-side step annotation introduced by TLCTC+:
- `[Pattern: PATTERN-XXX.YY ...]` — bracket-only (no `+`), attaches to a TLCTC step (typically `#9`), records the scam/fraud/manipulation playbook from the PATTERN catalogue

Consequence-side annotations introduced by TLCTC+ (all additive — `+ [...]`):
- `+ [SRE]` — Loss of Control / System Compromise; the cyber Bow-Tie central event
- `+ [DRE: C | I | Ac | Av]` — Data Risk Event (v2.1 extension; TLCTC+ keeps the same letter set)
- `+ [BRE: BRE-XXX.YY ...]` — Business Risk Event, structured code from the BRE catalogue
- `+ [Impact: IMPACT-XXX.YY ... = <value>]` — quantified or qualified measurement from the IMPACT catalogue
- `+ [Report: REPORT-XXX.YY ...]` — procedural / regulatory reporting artefact from the REPORT catalogue

The full formal grammar is defined in spec §8 and mirrored in `grammar/tlctc-plus-attack-path.abnf`.

### Appendix B — Sample Cases

Each case below shows the conformant TLCTC+ v0.4 notation, followed by the case-class assignment from §12 (A = core cyber incident, B = hybrid cyber-enabled harm, C = pure #9-anchored digital crime).

**B.1 Phishing leading to malware** *(case class A)*
```
#9 ||[email][@External→@Org]|| →[Δt=hours] #7 →[Δt=minutes] #4 + [SRE] + [DRE: C]
```
Classical cyber-incident chain. BRE annotations are added if a nationally reportable downstream business event was observed.

**B.2 Payment diversion after impersonation (CEO fraud)** *(case class C)*
```
#9 ||[email][@External→@Org]|| [Pattern: PATTERN-FIN.25 CEO / Executive Impersonation]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 250,000]
```
No system compromise; manipulation alone induces an authorized-but-unintended payment. Anchored at #9. The scam playbook is recorded as Pattern; the business event is recorded as a structured BRE; the magnitude is recorded as Impact.

**B.3 Romance scam without system compromise** *(case class C)*
```
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```
Pure manipulation-driven harm against a citizen. No SRE, no DRE. The boundary operator on `#9` is REQUIRED under R-9-BOUNDARY.

**B.4 Fake tech-support scam with remote-access installation** *(case class B)*
```
#9 ||[phone][@External→@Citizen]|| [Pattern: PATTERN-FIN.13 Fake Tech Support Scam]
→[Δt=minutes] #7 + [SRE] + [DRE: C]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm → BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss]
```
Hybrid case: the social-engineering step induces installation of remote-access tooling (FEC executes → #7, R-EXEC), producing an SRE and a DRE. The BRE chain captures account takeover followed by induced payment; the Impact captures the measured loss.

**B.5 Account-takeover-enabled fraud** *(case class B)*
```
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-FIN.21 Business Email Compromise]
+ [DRE: C] → #4 + [SRE]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm → BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 80,000]
```
Credential acquisition via phishing (#9 with direct disclosure `+ [DRE: C]`), credential application (#4 per R-CRED / Axiom X), with the SRE recording mailbox compromise. The BRE chain records the cyber-incident identity outcome together with the nationally reportable downstream financial event; Impact records the measured loss.

**B.6 Ransomware-driven service outage** *(case class A)*
```
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: Ac]
+ [BRE: BRE-SVC.11 Payment Function Unavailable → BRE-ORG.12 Business Continuity Plan Activated]
+ [Impact: IMPACT-OPS.11 Downtime Duration = 6 hours]
```
Ransomware is not a cluster — the cause path is `#9 → #7`. The DRE is `Ac` (data present but unusable). The BRE chain records the service consequence followed by internal response; Impact records the downtime measurement.

**B.7 Supply-chain incident triggering regulatory reporting** *(case class A)*
```
#10 ||[update][@Vendor→@Org]|| → #7 + [SRE] + [DRE: C + I]
+ [BRE: BRE-REG.11 Mandatory Notification Obligation Triggered
       → BRE-REG.17 Cross-Border Authority Notification Obligation]
+ [Report: REPORT-NIS2.11 24h Early Warning Filed + REPORT-NIS2.12 72h Incident Notification Filed]
```
The Trust Acceptance Event is on `#10` (R-SUPPLY); the regulatory BRE captures the obligation; the Report annotation captures the procedural filings. REPORT codes never appear inside BRE chains.

### Appendix C — Catalogue References
- PATTERN catalogue: spec §10 (financial manipulation, identity manipulation, coercion/extortion families)
- BRE catalogue: spec §11 (service, customer, financial, identity, legal, regulatory, reputation, third-party, organizational families)
- IMPACT catalogue: spec §12 (financial, operational, customer, regulatory/legal, reputation, data families)
- REPORT catalogue: spec §13 (NCSC/CERT, NIS2, DORA, data-protection families)

### Appendix D — JSON Profile
- canonical record skeletons: spec §15 (Data Model) and §16 (Example JSON Records)
- formal grammar: spec §8 and `grammar/tlctc-plus-attack-path.abnf`
- conformance checklist: spec §19 (16 numbered items)

### Appendix E — Routing Logic
- when to keep a case inside core TLCTC (no SRE/DRE/BRE consequences worth recording at national level)
- when to use TLCTC+ (cyber incident, hybrid harm, or pure-#9 digital crime with nationally relevant consequence)
- when to route to law enforcement or another authority (per national procedure; signalled via REPORT-NCSC.14 Law-Enforcement Referral Candidate Flagged)

---

## Closing Sentence

**TLCTC identifies the cause. TLCTC+ extends the reporting grammar. That is enough for NCSCs and CERTs to stop debating semantics and start building stable national practice.**
