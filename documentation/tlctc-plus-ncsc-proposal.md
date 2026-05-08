# TLCTC+ for NCSCs and CERTs: A National Reporting Extension Proposal

**Author:** Bernhard Kreinz
**Framework Version:** TLCTC v2.1
**Document Version:** v0.1 (proposal)
**License:** CC BY 4.0
**Status:** Working proposal

**Core thesis:** Keep TLCTC pure. Extend the reporting layer.

> **Companion document:** This is the **policy proposal** — the case for adopting TLCTC+, the governance model, the adoption path. For the **implementation specification** (grammar, conformance rules, BRE/PATTERN/IMPACT/REPORT catalogues, JSON record formats, decision procedure), see [`tlctc-plus-specification.md`](tlctc-plus-specification.md). The proposal makes the case; the spec defines how to build it.
>
> Note: the spec's annotation grammar refines what this proposal sketches in §9 — in particular, free-text BRE labels (e.g. `+ [BRE: Romance Scam]`) are deprecated in v0.3 in favor of structured codes (`[Pattern: PATTERN-FIN.11] + [BRE: BRE-FIN.11]`). See spec §7 R-V01-MIGRATION for the migration path.

---

## 1. Executive Summary

National Cyber Security Centres (NCSCs) and CERTs need a stable language that supports more than one mission at the same time. They must classify cyber incidents affecting IT systems and critical sectors, but they are also increasingly expected to receive and process reports about broader digitally mediated harms such as scams, fraud, impersonation, and payment diversion.

Core TLCTC already provides a cause-oriented language for cyber threats against IT systems. That is its strength. It classifies the cause-side threat by the generic vulnerability initially exploited and keeps threats, data risk events, and business consequences separate.

This proposal argues that NCSCs and CERTs should not weaken or redefine that core model. Instead, they should adopt a controlled extension profile called **TLCTC+**.

TLCTC+ is not a new taxonomy. It is not a replacement for TLCTC. It is a national reporting extension that allows NCSCs and CERTs to capture broader digitally mediated harms inside the same analytical ecosystem without destroying the semantic discipline of the core framework.

The extension starts with one very specific gap: manipulation-driven digital harms that are clearly relevant to national centres but do not always culminate in a classical cyber incident against an IT system. The natural anchor for that gap is **#9 Social Engineering**.

The proposal is therefore simple:

- keep the ten TLCTC clusters unchanged
- preserve the Bow-Tie separation between causes, Data Risk Events, and Business Risk Events
- introduce TLCTC+ as an intake and reporting profile for NCSCs and CERTs
- begin TLCTC+ with a formal handoff from `#9 Social Engineering` to standardized `BRE` notation for digitally mediated harms that fall outside core cyber-compromise analysis

Recommended notation:

`#9 + [BRE: Romance Scam]`

This reuses the existing additive Bow-Tie grammar that TLCTC already applies to Data Risk Events (`+ [DRE: ...]`). BREs sit on the consequence side of the Bow-Tie alongside DREs, so an additive annotation — not a new operator — is the semantically correct extension. No core TLCTC operator is overloaded, and no new symbol is introduced into the path grammar.

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
- Data Risk Events remain distinct from threats
- Business Risk Events remain consequence-side events
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

That is why the first formal extension is anchored here. The mechanism itself — appending `+ [BRE: ...]` to a cause-side path — is fully general and may be applied after any terminal cause-side step (e.g., `#4`, `#1`, `#7`) when the nationally relevant outcome is best captured as a Business Risk Event. The deliberate scope choice for the initial TLCTC+ profile is to begin at `#9` because that is where the structural gap between cyber-incident reporting and digitally mediated-harm reporting is widest.

---

## 9. Proposed Extension Rule

**TLCTC+ introduces a controlled `BRE` (Business Risk Event) annotation, appended to a TLCTC cause-side path, for digitally mediated harms that do not meaningfully enter core IT-system compromise analysis.**

Recommended notation:

`#9 + [BRE: Romance Scam]`
`#9 + [BRE: Fake Tech Support Payment]`
`#9 + [BRE: CEO Fraud Transfer]`
`#9 + [BRE: Sextortion Payment]`

### Semantics

- `→` remains the core TLCTC operator for cause-side attack-path progression
- `+ [DRE: X]` remains the notation for Data Risk Events
- `+ [BRE: ...]` is introduced as a TLCTC+ Business Risk Event annotation, parallel to `+ [DRE: ...]`

The choice to reuse the existing additive `+ [...]` grammar is deliberate. It places BREs on the same grammatical footing as DREs — both are consequence-side events of the Bow-Tie model — without inventing a new operator class and without overloading any existing operator (in particular, the v2.1 transit operator `⇒` is left untouched).

A path may carry both a DRE and a BRE annotation when both are relevant:

`#9 → #4 + [DRE: C] + [BRE: Account Takeover Fraud]`

In this hybrid case, `+ [DRE: C]` records the cyber-incident consequence (loss of confidentiality through credential application) and `+ [BRE: Account Takeover Fraud]` records the nationally reportable downstream harm.

---

## 10. Why BRE Is the Right Destination

Romance scam, fake support payment, induced transfer, or sextortion payment are not threat clusters. They are not generic vulnerabilities. They are not causes in the TLCTC sense.

The cause-side classification remains `#9`.

What follows is better understood as a consequence-side event. That is why `BRE` is the correct anchor for the extension.

For TLCTC+ purposes, BRE should be interpreted broadly enough to cover:

- organizational harm
- financial harm
- citizen-level economic harm
- reputational harm
- induced obligations or reporting consequences
- other discrete consequence-side events relevant to national reporting

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

TLCTC+ should support three clearly separated case classes.

### A. Core Cyber Incident

A case that meaningfully fits the core TLCTC incident logic.

Example:

`#9 → #4 → #7 + [DRE: C]`

### B. Hybrid Cyber-Enabled Harm

A case in which a core TLCTC chain exists, but the nationally relevant outcome is best captured as a BRE.

Example:

`#9 → #4 + [BRE: Account Takeover Fraud]`

### C. Digitally Mediated Non-SRE Harm

A case that is digitally mediated and harmful, but does not meaningfully enter the standard cyber-incident chain (no System Risk Event, no DRE).

Example:

`#9 + [BRE: Romance Scam]`

This three-part typology allows national centres to keep one reporting ecosystem without forcing false equivalence between all digital harms.

---

## 13. BRE Profile for National Use

TLCTC+ should define a controlled BRE vocabulary for NCSC and CERT reporting.

The exact label set can vary nationally, but a first candidate structure could include:

### Financial Harm
- Fraudulent Transfer
- Induced Payment
- Romance Scam
- Fake Tech Support Payment
- Sextortion Payment
- Investment Scam Loss

### Identity and Account Harm
- Account Takeover Fraud
- Identity Misuse Harm
- Impersonation-Driven Authorization
- Credential Abuse Consequence

### Organizational Harm
- Public Service Deception
- Supplier Payment Diversion
- Internal Approval Fraud
- Regulatory Notification Obligation
- Customer Compensation Event

### Societal or Reputational Harm
- Public Confidence Harm
- Reputational Damage
- Citizen Harm Event
- Media Escalation Event

The important point is not the perfect label list. The important point is that the labels live on the consequence side and remain subordinate to the cause-side classification.

---

## 14. Intake and Triage Workflow

TLCTC+ should be used through a simple triage logic.

### Decision Flow

1. Is there a TLCTC-classifiable cyber threat against an IT system?
2. If yes, record the TLCTC path.
3. Did a Data Risk Event occur?
4. Did one or more Business Risk Events follow?
5. If no meaningful SRE/DRE exists, ask whether the case is digitally mediated and driven primarily by `#9 Social Engineering`.
6. If yes, append the `+ [BRE: <label>]` annotation to the cause-side path.
7. If not, route the case outside the TLCTC+ intake model.

This workflow helps keep intake disciplined while still supporting the broader mission of national centres.

---

## 15. Data Model and Reporting Format

TLCTC+ should be machine-addressable and easy to integrate into national reporting portals.

A simple starting point is to define three record types:

- `core_incident`
- `hybrid_case`
- `digital_harm_case`

Each record should preserve:

- case identifier
- intake source
- sector or citizen flag
- TLCTC path or anchor cluster
- DRE fields where relevant
- BRE fields
- mandatory reporting flag
- law-enforcement referral flag
- public warning relevance flag
- statistical category version

### Example Records

#### Core Incident
```json
{
  "record_type": "core_incident",
  "path": "#9 -> #4 -> #7",
  "dre": ["C"],
  "bre": [],
  "sector": "energy",
  "mandatory_reporting": true
}
```

#### Hybrid Case
```json
{
  "record_type": "hybrid_case",
  "path": "#9 -> #4",
  "dre": [],
  "bre": ["Account Takeover Fraud"],
  "sector": "citizen",
  "mandatory_reporting": false
}
```

#### Digital Harm Case
```json
{
  "record_type": "digital_harm_case",
  "path": "#9",
  "dre": [],
  "bre": ["Romance Scam"],
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

### BRE Label Sets
- maintained nationally or regionally
- adjustable over time
- harmonizable across borders without changing TLCTC core

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
**Mitigation:** TLCTC+ introduces no new operator. `+ [BRE: ...]` reuses the existing additive Bow-Tie grammar already used by `+ [DRE: ...]` and is restricted to consequence-side annotations only. BRE annotations MUST NOT appear as cause-side steps and MUST NOT be referenced as if they were threat clusters. The v2.1 transit operator `⇒` retains its existing meaning unchanged.

---

## 19. Proposed Adoption Path

This proposal is intentionally designed so NCSCs and CERTs do not need years of conceptual debate before using it.

### Phase 1 — Adopt Core TLCTC
Use TLCTC as the stable cause-oriented taxonomy for cyber threats against IT systems.

### Phase 2 — Define TLCTC+
Publish a national extension profile for broader digitally mediated harms.

### Phase 3 — Start Narrow
Limit the first extension rule to the `+ [BRE: ...]` annotation anchored at `#9`.

### Phase 4 — Define BRE Vocabulary
Publish and govern a national BRE label set for digital-harm reporting.

### Phase 5 — Integrate Into Portals and Statistics
Implement the model in forms, databases, trend reporting, and public awareness workflows.

### Phase 6 — Review Without Reopening the Core
Review the extension annually, but do not reopen the semantics of core TLCTC unless the canonical framework itself changes.

---

## 20. Formal Recommendation

NCSCs and CERTs should adopt TLCTC as the stable cause-oriented taxonomy for cyber threats against IT systems and establish **TLCTC+** as a controlled national reporting extension profile for digitally mediated harms.

TLCTC+ should begin with the `+ [BRE: <label>]` annotation anchored at `#9 Social Engineering`, allowing manipulation-driven scam and fraud cases to be recorded in the same analytical ecosystem without compromising TLCTC's semantic integrity.

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
- `→` for core TLCTC cause-side sequence (unchanged)
- `+ [DRE: X]` for Data Risk Events (unchanged)
- `+ [BRE: <label>]` for TLCTC+ Business Risk Events (additive consequence-side annotation, parallel to `+ [DRE: ...]`; appended to a cause-side path, never used as a step)
- All v2.1 boundary, intra-system, and unresolved-step operators (`||...||`, `⇒` transit, `|...|` intra-system, `?`, `…`) retain their existing meanings unchanged

### Appendix B — Sample Cases

Each case below shows the intended TLCTC+ notation, followed by the case-class assignment from §12 (A = core cyber incident, B = hybrid cyber-enabled harm, C = digitally mediated non-SRE harm).

**B.1 Phishing leading to malware** *(case class A)*
```
#9 ||[email][@External→@Org]|| →[Δt=hours] #7 →[Δt=minutes] #4 + [DRE: C]
```
Classical cyber-incident chain. No BRE annotation required for national reporting unless a downstream business-impact event is independently relevant.

**B.2 Payment diversion after impersonation (CEO fraud)** *(case class C)*
```
#9 ||[email][@External→@Org]|| + [BRE: CEO Fraud Transfer]
```
No system compromise; manipulation alone induces an authorized-but-unintended payment. Anchored at #9, terminated with a BRE annotation.

**B.3 Romance scam without system compromise** *(case class C)*
```
#9 ||[messaging][@External→@Citizen]|| + [BRE: Romance Scam]
```
Pure manipulation-driven harm against a citizen. No DRE, no SRE.

**B.4 Fake tech-support scam with remote-access installation** *(case class B)*
```
#9 ||[human][@External→@Citizen]|| →[Δt=minutes] #7 + [DRE: C] + [BRE: Fake Tech Support Payment]
```
Hybrid case: the social-engineering step induces installation of remote-access tooling (FEC executes → #7, R-EXEC), producing both a DRE (loss of confidentiality through observed activity) and a BRE (induced payment). Both annotations co-exist on the consequence side.

**B.5 Account-takeover-enabled fraud** *(case class B)*
```
#9 ||[email][@External→@Citizen]|| →[Δt=hours] #4 + [DRE: C, I] + [BRE: Account Takeover Fraud]
```
Credential acquisition via phishing (#9), credential application (#4 per R-CRED / Axiom X), with both the cyber-incident outcome (DRE) and the nationally reportable downstream harm (BRE) recorded.

### Appendix C — BRE Vocabulary Draft
- candidate BRE labels
- definitions
- scope notes
- de-duplication rules

### Appendix D — JSON Profile Sketch
- example schemas
- record validation rules
- required vs optional fields

### Appendix E — Routing Logic
- when to keep a case inside core TLCTC
- when to use TLCTC+
- when to route to law enforcement or another authority

---

## Closing Sentence

**TLCTC identifies the cause. TLCTC+ extends the reporting grammar. That is enough for NCSCs and CERTs to stop debating semantics and start building stable national practice.**
