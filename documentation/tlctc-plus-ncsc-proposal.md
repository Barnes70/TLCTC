# TLCTC+ for NCSCs and CERTs: A National Reporting Extension Proposal v0.6

## Policy proposal aligned with TLCTC+ Specification v0.6

**Author:** Bernhard Kreinz  
**Framework version:** TLCTC v2.1  
**Document version:** v0.6 proposal, aligned with TLCTC+ Specification v0.6  
**Status:** Draft for peer review  
**License:** CC BY 4.0  
**Core thesis:** Keep TLCTC pure. Extend the reporting layer.

> **Companion document:** This proposal explains why NCSCs, CERTs, CSIRTs, regulators, financial institutions, fraud teams, and adjacent peer groups should adopt TLCTC+. The implementation details — grammar, conformance, catalogues, JSON records, and decision procedure — are defined in `tlctc-plus-specification.md`.
>
> **Notation policy:** This proposal follows TLCTC+ v0.6. Scam, fraud, extortion, and manipulation labels are recorded as `[Pattern: PATTERN-XXX.YY ...]` on the cause-side step. Consequence-side events are recorded as structured BRE codes: `+ [BRE: BRE-XXX.YY ...]`. System compromise is recorded as `+ [SRE]`. Data/resource impact is recorded as `+ [DRE: C|I|Ac|Av]`. Measurements are recorded as `+ [Impact: ...]`. Procedural filings and workflow states are recorded as `+ [Report: ...]`. Free-text BRE labels are not conformant.

---

## 0. One-Sentence Proposal

**TLCTC+ should be adopted as a TLCTC-anchored national reporting grammar that connects cyber causes and #9 digital-harm anchors to explicit SRE, DRE, Pattern, BRE, Impact, and Report structures without turning scams, crimes, outcomes, actors, or reporting duties into threat clusters.**

---

## 1. Executive Summary

National Cyber Security Centres (NCSCs), CERTs, and CSIRTs increasingly handle two structurally distinct reporting realities, split on whether an IT system was compromised:

1. **Compromise records** — a TLCTC attack path leads to Loss of Control / System Compromise (SRE present). Within this single class, two reporting flavors are common: cyber-side dominance (the historic "core cyber incident" — technical compromise, service outage, regulatory notification) and consequence-side dominance (the historic "hybrid cyber-enabled harm" — fraud, citizen harm, identity harm, financial loss). The structural reality is the same; the distinction is which BRE family dominates downstream.
2. **Pure #9-anchored digital-harm records** — the case is digitally mediated and manipulation-driven, but no IT system is compromised. No SRE.

Core TLCTC already solves the cause-side problem. It classifies cyber threats by the generic vulnerability initially exploited and keeps threats, actors, control failures, data risk events, and business consequences separate.

The reporting problem is different. National centres must also process reports about romance scams, fake support scams, CEO fraud, invoice diversion, mule recruitment, sextortion, payment manipulation, account takeover, supplier incidents, ransomware service impact, and regulatory notification obligations. These labels are operationally important, but they are not TLCTC threat clusters.

TLCTC+ solves this by keeping the TLCTC cause path intact and adding a reporting layer around it:

```text
TLCTC cause path
+ [SRE]
+ [DRE: C|I|Ac|Av]
[Pattern: ...]
+ [BRE: ...]
+ [Impact: ...]
+ [Report: ...]
```

The key design move is the split between **Pattern** and **BRE**:

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

“Romance scam” is the manipulation narrative. It is therefore a Pattern. The authorized payment is the observable business/citizen event. It is therefore a BRE. The loss amount is an Impact. The cause remains `#9`.

This lets national centres use one reporting ecosystem across cyber incidents, cyber-enabled fraud, and pure manipulation-driven digital harm without pretending those cases are the same thing.

---

## 2. Why Peer Groups Should Care

### 2.1 NCSCs, CERTs, and CSIRTs

NCSCs and CERTs receive heterogeneous reports: malware, phishing, credential disclosure, service outages, ransomware, supplier incidents, romance scams, fake support scams, account takeover, payment diversion, and citizen harm. TLCTC+ gives them one intake grammar while preserving the difference between technical compromise and pure manipulation.

**Policy value:** cleaner triage, comparable national statistics, stronger warnings, better referral logic, and fewer recurring debates over whether a scam, outage, or fraud label is a “cyber threat.”

### 2.2 Financial Regulators, Central Banks, and Supervisors

Financial regulators need to compare ICT incidents, payment fraud, operational disruptions, reimbursement-relevant distinctions, and procedural reporting obligations. Existing reporting often mixes authorization status, fraud narrative, impact, and root cause.

**Policy value:** TLCTC+ separates the cause path from the payment/fraud event and measured impact. It can distinguish victim-authorized payments, attacker-executed transactions, system compromise, and pure social manipulation in one structure.

### 2.3 Banks, PSPs, Fintechs, and Fraud Teams

Banks and payment-service providers need labels such as APP fraud, invoice fraud, CEO fraud, mule recruitment, fake support scam, and account takeover. Security teams need attack paths. Risk teams need losses, obligations, and controls.

**Policy value:** one case record can support fraud operations, cybersecurity, compliance, operational risk, loss reporting, and executive reporting without flattening everything into “external fraud.”

### 2.4 SOC, CTI, and Incident Response Teams

SOC and CTI teams need cause-side attack paths. A BEC label is not enough: it may represent pure `#9`, `#9 + [DRE: C]`, `#9 → #4`, `#9 → #7`, `#10 → #7`, or another path.

**Policy value:** investigation, detection, and controls remain tied to the real attack steps. Reporting labels do not overwrite causality.

### 2.5 GRC, Operational Risk, and Enterprise Risk Management

Operational-risk functions often work with loss-event categories and consequence labels. TLCTC+ gives them the cyber/digital-harm slice while explicitly excluding non-cyber operational failures.

**Policy value:** better bridge between cyber risk and operational risk, without forcing cyber threats into broad loss buckets or turning non-cyber failures into TLCTC records.

### 2.6 Law Enforcement and Financial-Crime Units

Law enforcement needs legal and investigative categories. TLCTC+ does not replace them. It provides a structured case record that can coexist with criminal-law classification.

**Policy value:** clearer distinction between manipulation narrative, identity compromise, transaction event, loss amount, system compromise, and referral state.

### 2.7 Insurers, Actuaries, and Loss Modelers

Insurance and loss modeling need consistent separation between cause, event, consequence, and measurement.

**Policy value:** better scenario construction and loss aggregation. Labels like “ransomware loss” or “fraud loss” become decomposable into cause path, DRE, BRE, and Impact.

### 2.8 Standards Bodies, Researchers, and Framework Designers

Cybersecurity frameworks often mix causes, outcomes, actors, control failures, and reporting duties. TLCTC+ gives a clean separation model that can be tested and mapped.

**Policy value:** a stable conceptual bridge between threat taxonomies, incident reporting, fraud reporting, operational-risk reporting, and regulatory notification.

---

## 3. Problem Statement

National reporting ecosystems usually suffer from semantic mixing before they suffer from data scarcity.

Reports from critical sectors, financial institutions, citizen portals, public hotlines, fraud desks, data-protection channels, and mandatory incident regimes often mix:

- threat categories,
- incident labels,
- scam and crime labels,
- actor labels,
- consequence labels,
- impact measurements,
- reporting workflow states,
- control failures,
- sector-specific terminology.

The result is predictable:

- weak comparability between reports;
- unstable national statistics;
- blurred boundaries between cyber incidents and digital harms;
- repeated terminology debates;
- weak routing between cyber, fraud, consumer protection, law enforcement, and regulatory workflows;
- poor alignment between cause-side controls and consequence-side reporting.

Some cases are classical cyber incidents. Some are manipulation-driven digital harms with no system compromise. Others combine both. A national reporting model must handle all three without collapsing them into a vague “cybercrime” bucket.

---

## 4. Scope of the Proposal

TLCTC+ is proposed for:

- mandatory cyber incident reporting;
- voluntary NCSC/CERT intake;
- sectoral cyber incident notification;
- citizen-facing digital-harm reporting;
- financial fraud and cyber-fraud intake where a TLCTC anchor exists;
- national statistics and trend reporting;
- warning, awareness, and prevention messaging;
- routing to law enforcement, consumer protection, data protection, financial supervisors, and sector regulators.

TLCTC+ does **not** aim to:

- redefine criminal-law categories;
- replace law-enforcement taxonomies;
- replace sector-specific legal obligations;
- replace fraud typologies;
- classify all operational risk;
- classify non-cyber operational failure;
- create an eleventh TLCTC cluster;
- change the normative semantics of core TLCTC.

TLCTC+ is a reporting profile, not a new threat taxonomy.

---

## 5. Normative Design Principle

**TLCTC+ shall preserve TLCTC core semantics unchanged.**

That means:

```text
Threats remain causes.
Actors are not threats.
Control failures are not threats.
Scam labels are not threats.
Ransomware is not a threat cluster.
Data breach is not a threat cluster.
Service outage is not a threat cluster.
SRE is the cyber Bow-Tie centre.
DREs are data/resource risk events.
Patterns are cause-side descriptors.
BREs are consequence-side events.
Impacts are measurements.
Reports are workflow/procedural artefacts.
```

If a TLCTC+ implementation weakens this separation, it fails.

---

## 6. Core Model

TLCTC+ uses six tracks.

```text
Cause Track       TLCTC path or #9 anchor; Pattern attaches here
SRE Track         Loss of Control / System Compromise
DRE Track         Confidentiality, Integrity, Accessibility, Availability
BRE Track         Business, citizen, legal, regulatory, service, organizational events
Impact Track      Quantified or qualified measurements
Report Track      Filing, routing, notification, or workflow artefacts
```

The tracks are independent dimensions of one case record. They must not be collapsed.

### 6.1 Compromise Record

A TLCTC path leads to Loss of Control / System Compromise. An SRE is present. This single record class covers two reporting flavors that are structurally identical.

**Cyber-side dominance** (formerly "core cyber incident") — reporting interest is technical compromise, service impact, or regulatory notification; dominant BRE families are BRE-SVC.*, BRE-DATA.*, BRE-REG.*, BRE-ORG.*.

```text
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: Ac]
+ [BRE: BRE-SVC.11 Payment Function Unavailable]
+ [Impact: IMPACT-OPS.11 Downtime Duration = 6 hours]
```

**Consequence-side dominance** (formerly "hybrid cyber-enabled harm") — reporting interest is fraud, citizen harm, identity harm, or downstream financial consequence; dominant BRE families are BRE-FIN.*, BRE-ENT.*, BRE-CUS.*.

```text
#9 ||[email][@External→@Org]|| [Pattern: PATTERN-ID.11 Phishing for Credentials]
+ [DRE: C] → #4 + [SRE]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm → BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 80,000]
```

Both flavors are `record_type = compromise_record`. The dominant BRE family is the observable artefact that lets statistics and triage workflows tell the two flavors apart; it is not a record_type axis.

### 6.2 Pure #9-Anchored Digital-Harm Record

No IT system is compromised. The case is digitally mediated and manipulation-driven. SRE is absent.

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

A DRE may appear in a `pure_9_record` only when the manipulation itself directly causes data disclosure or resource impact without system compromise:

```text
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-ID.11 Phishing for Credentials]
+ [DRE: C]
```

If the disclosed credential, token, session artifact, or identity artifact is later used, the case transitions to a `compromise_record`:

```text
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-ID.11 Phishing for Credentials]
+ [DRE: C] → #4 + [SRE]
```

Credential acquisition is classified by the enabling cluster. Credential use is always `#4`.

---

## 7. Why the Extension Anchors on #9

The first TLCTC+ extension point is `#9 Social Engineering`, not because `#9` is incomplete, but because it already classifies the cause correctly: exploitation of human psychology.

Many nationally relevant digital-harm reports begin with manipulation:

- a citizen is persuaded to transfer money;
- an employee is persuaded to approve a payment;
- a user is persuaded to disclose credentials;
- a victim is coerced into paying;
- a customer is persuaded to install software;
- an employee is deceived into changing bank details.

Sometimes that manipulation leads to system compromise. Sometimes it does not. The cause-side anchor is still `#9`.

The structural gap is therefore not the classification of the cause. The gap is the reporting of the consequence when there is no SRE, or when the reporting interest sits downstream of the SRE.

TLCTC+ fills that gap by attaching Pattern metadata to the cause-side step and adding BRE / Impact / Report structures on the consequence side.

---

## 8. Why Pattern + BRE Is the Correct Split

A scam label is not a threat cluster. It is also not, by itself, a business event.

“Romance scam” describes the narrative.  
“Authorized Push Payment Made” describes the event.  
“Direct Fraud Loss = CHF 4,500” describes the measured impact.  
`#9` describes the cause.

Correct:

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

Incorrect:

```text
#9 + [BRE: Romance Scam]
```

This split is the central improvement over flat “cybercrime type” lists. It allows statistics to answer different questions without semantic confusion:

```text
What caused the case?             → TLCTC path
What manipulation narrative?      → Pattern
Was there system compromise?      → SRE
Was data/resource affected?       → DRE
What event happened?              → BRE
How large was the harm?           → Impact
Was a filing/referral made?       → Report
```

---

## 9. Boundary Conditions

TLCTC+ must not:

- create new TLCTC top-level clusters;
- redefine scam labels as threats;
- turn ransomware, BEC, APP fraud, data breach, or outage into threat clusters;
- collapse BREs into threat categories;
- auto-derive BRE families from TLCTC cluster identity;
- replace criminal-law categories;
- replace law-enforcement investigative taxonomies;
- classify non-cyber operational failures;
- overload the TLCTC sequence operator `→`;
- use free-text BREs in conformant records.

TLCTC+ must remain an extension profile around TLCTC, not a mutation of TLCTC.

---

## 10. Intake and Triage Workflow

A national portal or analyst workflow can use the following decision flow.

1. **Is there a TLCTC cyber cause path?**  
   If yes, classify each step using TLCTC `#1`–`#10`.

2. **If not, is there a pure #9 digital-harm anchor?**  
   If a human was psychologically manipulated through a digital or digitally mediated channel, record `#9` with the required bridge boundary.

3. **Did Loss of Control / System Compromise occur?**  
   If yes, attach `+ [SRE]`. If no and the case is pure #9 digital harm, omit SRE.

4. **Did a DRE occur?**  
   Attach `+ [DRE: C|I|Ac|Av]` to the step or segment that caused it.

5. **Is there a scam, fraud, extortion, or manipulation label?**  
   Attach `[Pattern: PATTERN-XXX.YY ...]` to the cause-side step.

6. **Did a business, citizen, service, legal, regulatory, reputation, third-party, or organizational event occur?**  
   Attach `+ [BRE: BRE-XXX.YY ...]`.

7. **Can the harm be measured?**  
   Attach `+ [Impact: IMPACT-XXX.YY = <value>]`.

8. **Was a filing, referral, or procedural stage reached?**  
   Attach `+ [Report: REPORT-XXX.YY ...]`.

If there is no TLCTC path and no #9 anchor, the case is outside TLCTC+.

---

## 11. Regulatory and Reporting Alignment

### 11.1 NIS2-Style Reporting

NIS2-style reporting needs incident severity, root cause, impact, mitigation, and cross-border relevance.

TLCTC+ maps this as:

```text
Root cause / likely threat        → TLCTC cause path
System compromise                 → SRE
Data or resource impact           → DRE
Service / business consequence    → BRE
Severity and scope                → Impact
Notification stages               → Report
Cross-border relevance            → BRE-REG / Report metadata
```

### 11.2 DORA-Style Reporting

DORA-style ICT reporting needs affected clients, affected transactions, duration, downtime, data loss, criticality, geographical spread, economic impact, and reporting stages.

TLCTC+ maps this as:

```text
ICT/cyber cause                   → TLCTC cause path
Loss of control                   → SRE
Data loss or resource impact      → DRE + IMPACT-DATA
Critical service impact           → BRE-SVC
Clients / transactions            → IMPACT-CUS / IMPACT-OPS
Economic impact                   → IMPACT-FIN
DORA filing stages                → REPORT-DORA
```

### 11.3 Payment Fraud and Financial-Crime Reporting

Payment fraud reporting often needs authorization status, fraud narrative, channel, transaction event, reimbursement relevance, and measured loss.

TLCTC+ maps this as:

```text
Manipulation / compromise cause   → TLCTC path
Fraud narrative                   → Pattern
Victim-authorized transaction     → BRE-FIN.11 / BRE-FIN.12 / BRE-FIN.13 / BRE-FIN.14
Attacker-executed transaction     → BRE-FIN.21 / BRE-FIN.22 / BRE-FIN.23 / BRE-FIN.24
Loss amount                       → IMPACT-FIN.12
Referral or report status         → REPORT-NCSC / REPORT-DORA / national extension
```

### 11.4 Operational-Risk Positioning

TLCTC+ can feed operational-risk reporting, but it is not a complete OpRisk taxonomy.

Example:

```text
External fraud
```

may arise from many cause paths:

```text
#9
#9 + [DRE: C] → #4
#5 → #4
#7 → #4
#2 → #7
#10 → #7
```

Therefore, TLCTC+ must not reduce external fraud to `#9`. The TLCTC path records the cause. Pattern, BRE, Impact, and Report record the reporting dimensions.

---

## 12. Minimal Data Model

A conformant TLCTC+ v0.6 record uses one of two record types:

```text
compromise_record
pure_9_record
```

`compromise_record` covers cases where a TLCTC path reaches Loss of Control / System Compromise — regardless of whether the dominant downstream BRE family is cyber-side (BRE-SVC.*, BRE-DATA.*, BRE-REG.*) or consequence-side (BRE-FIN.*, BRE-ENT.*, BRE-CUS.*). The historical "core cyber incident" and "hybrid cyber-enabled harm" labels remain useful descriptive prose but are not separate record types in v0.6.

Minimum metadata:

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

Minimum track fields:

```text
Cause:      tlctc_path or tlctc_anchor, tlctc_steps[], patterns[], evidence[]
SRE:        present, status, timestamp, linked_to_step, scope
DRE:        type, status, affected_data_or_resource, linked_to_step, linked_to_sre
BRE:        code, label, status, parent, operator, timestamp, linked_to_step/dre/sre
Impact:     code, label, amount/value, unit/currency, estimate_type, linked_to_bre/dre/sre
Report:     code, label, regime, stage, due/filed timestamp, authority, status
```

---

## 13. Illustrative JSON Records

### 13.1 Pure #9 Digital Harm

```json
{
  "case_id": "case-002",
  "record_type": "pure_9_record",
  "framework_version": "TLCTC v2.1",
  "tlctc_plus_version": "0.6",
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

### 13.2 Compromise Record — BEC / Invoice Fraud (Consequence-Side Dominance)

```json
{
  "case_id": "case-003",
  "record_type": "compromise_record",
  "framework_version": "TLCTC v2.1",
  "tlctc_plus_version": "0.6",
  "tlctc_path": "#9 ||[email][@External→@Org]|| [Pattern: PATTERN-ID.11 Phishing for Credentials] + [DRE: C] → #4 + [SRE]",
  "patterns": [
    {
      "code": "PATTERN-FIN.22",
      "label": "Invoice / Mandate Fraud",
      "linked_to_step": "step-1"
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
      "description": "Credentials disclosed through social engineering"
    }
  ],
  "bre_chain": {
    "expression": "BRE-ENT.13 → BRE-FIN.11",
    "nodes": [
      {
        "code": "BRE-ENT.13",
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

## 14. Governance Model

Ownership should be split clearly.

### 14.1 Core TLCTC

Core TLCTC remains external, canonical, and unchanged by national reporting needs.

### 14.2 TLCTC+ Profile

The TLCTC+ profile is versioned separately from core TLCTC. It defines the reporting grammar and conformance rules for TLCTC-anchored digital-harm records.

### 14.3 Consequence Catalogues

PATTERN, BRE, IMPACT, and REPORT catalogues are versioned independently from the document.

Current v0.6 status:

```text
Specification document version:   TLCTC+ v0.6
PATTERN catalogue version:        v0.2
BRE catalogue version:            v0.3
IMPACT catalogue version:         v0.2
REPORT catalogue version:         v0.2
```

National aliases and national extensions may be added under national governance, but core catalogue codes should remain stable enough for cross-border comparability.

### 14.4 Future Shared Consequence Catalogue

In the long-term architecture, BRE, Impact, and Report catalogues may be extracted into a shared consequence-side specification usable by both TLCTC+ and future TLSFC-aligned profiles:

```text
TLCTC  ─┐
        ├─→ Shared Consequence Catalogue
TLSFC  ─┘
```

---

## 15. Benefits

### 15.1 Semantic Benefits

- one language across cyber incident intake and broader digital-harm intake;
- clearer separation between causes, system compromise, data risk, business events, impact, and reports;
- less semantic drift between reporting years;
- fewer debates about whether “ransomware,” “BEC,” “APP fraud,” or “romance scam” is a threat.

### 15.2 Operational Benefits

- better triage between cyber, fraud, law enforcement, and regulatory workflows;
- cleaner routing and escalation;
- stronger link between public warnings and observed Patterns;
- better distinction between pure manipulation and system compromise;
- usable structure for SOC, fraud, IR, and GRC teams.

### 15.3 Strategic Benefits

- more comparable national statistics;
- better aggregation across sectors;
- stronger basis for policy communication;
- improved supervisory analysis;
- a reporting model that survives annual changes in buzzwords.

---

## 16. Risks and Mitigations

### Risk 1 — TLCTC+ Becomes an “Everything Digital” Bucket

**Mitigation:** keep strict scope. A case needs a TLCTC path or a pure #9 digital-harm anchor. Non-cyber operational failure remains outside TLCTC+.

### Risk 2 — Conflict With Legal Categories

**Mitigation:** TLCTC+ is a reporting grammar, not a legal ontology. Legal categories may coexist as external labels.

### Risk 3 — Semantic Leakage Into Core TLCTC

**Mitigation:** the ten TLCTC clusters remain unchanged. TLCTC+ is versioned separately and cannot create new clusters.

### Risk 4 — BRE Vocabulary Inflation

**Mitigation:** use controlled catalogues, versioned changes, national aliases, and periodic review. Prefer event-shaped BREs over story-shaped labels.

### Risk 5 — Notation Drift

**Mitigation:** no new path operator. SRE/DRE/BRE/Impact/Report use additive notation. Pattern remains bracket-only cause-side metadata.

### Risk 6 — Free-Text BREs Return

**Mitigation:** conformant records use structured BRE codes. Scam and fraud names belong in Pattern, not free-text BREs.

### Risk 7 — Auto-Filling BREs From Clusters

**Mitigation:** enforce cause/consequence independence. A cluster never determines a BRE family automatically.

### Risk 8 — Over-Decomposition of Human Psychology

**Mitigation:** keep `#9` at the strategic level. Human micro-factors may be useful in research, but they should not destabilize the reporting grammar.

---

## 17. Proposed Adoption Path

### Phase 1 — Adopt Core TLCTC

Use TLCTC as the stable cause-oriented taxonomy for cyber threats against IT systems.

### Phase 2 — Adopt TLCTC+ v0.6 as a Reporting Profile

Publish TLCTC+ as a national reporting extension for TLCTC-anchored digital harms.

### Phase 3 — Start With Pure #9 Digital Harm

Begin with:

```text
#9 ||[ctx][@Source→@Target]|| [Pattern: PATTERN-XXX.YY]
+ [BRE: BRE-XXX.YY]
+ [Impact: IMPACT-XXX.YY]
```

This addresses the widest gap between cyber incident reporting and digital-harm reporting.

### Phase 4 — Add Compromise Records

Extend to `compromise_record` cases where `#9`, `#4`, `#7`, `#10`, or other TLCTC steps produce nationally relevant fraud, service, identity, legal, regulatory, or organizational consequences — both the cyber-side-dominant flavor (service outages, ransomware, supplier-driven compromise) and the consequence-side-dominant flavor (BEC, account takeover, invoice fraud).

### Phase 5 — Integrate Into Forms, Databases, and Statistics

Implement the six tracks in intake portals, case databases, public warnings, dashboards, and annual reporting.

### Phase 6 — Review Without Reopening TLCTC Core

Review catalogues and national aliases annually. Do not reopen the ten clusters unless core TLCTC itself changes.

---

## 18. Formal Recommendation

NCSCs, CERTs, CSIRTs, regulators, and financial-sector reporting bodies should adopt TLCTC as the stable cause-oriented taxonomy for cyber threats and TLCTC+ v0.6 as the controlled reporting extension for TLCTC-anchored digital harms.

TLCTC+ should begin with the Pattern + BRE model anchored at `#9 Social Engineering` for manipulation-driven digital harm (`pure_9_record`), while supporting the full six-track form for compromise records — both cyber-side-dominant and consequence-side-dominant flavors:

```text
Cause / SRE / DRE / Pattern / BRE / Impact / Report
```

The guiding principle remains:

**Keep TLCTC pure. Extend the reporting layer.**

---

## Appendix A — Notation Summary

Cause side:

```text
#1–#10                         TLCTC clusters
→                              sequential cause-side progression
(#X + #Y)                      parallel cause-side steps
||[ctx][@A→@B]||               bridge boundary operator
||[ctx][@A⇒@Transit→@B]||      transit boundary operator
|[type][@from→@to]|            intra-system boundary operator
[Pattern: PATTERN-XXX.YY]      cause-side pattern metadata
```

Consequence side:

```text
+ [SRE]                        Loss of Control / System Compromise
+ [DRE: C|I|Ac|Av]             Data/resource risk event
+ [BRE: BRE-XXX.YY]            Business/citizen/service/regulatory event
+ [Impact: IMPACT-XXX.YY]      measurement
+ [Report: REPORT-XXX.YY]      procedural artefact or workflow state
```

Conformance reminders:

- Pattern uses bracket-only notation.
- SRE/DRE/BRE/Impact/Report use additive notation.
- Every #8/#9/#10 step in a TLCTC+ record carries a boundary operator.
- BREs are structured codes, not free text.
- Stripping TLCTC+ annotations recovers a valid TLCTC path or #9 anchor.

---

## Appendix B — Sample Cases

### B.1 CEO Fraud, No System Compromise

```text
#9 ||[email][@External→@Org]|| [Pattern: PATTERN-FIN.25 CEO / Executive Impersonation]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 250,000]
```

### B.2 Phishing With Credential Disclosure, No Observed Use

```text
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-ID.11 Phishing for Credentials]
+ [DRE: C]
```

### B.3 Account-Takeover-Enabled Fraud

```text
#9 ||[email][@External→@Org]|| [Pattern: PATTERN-ID.11 Phishing for Credentials]
+ [DRE: C] → #4 + [SRE]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm → BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 80,000]
```

### B.4 Ransomware-Driven Service Outage

```text
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: Ac]
+ [BRE: BRE-SVC.11 Payment Function Unavailable → BRE-ORG.12 Business Continuity Plan Activated]
+ [Impact: IMPACT-OPS.11 Downtime Duration = 6 hours]
```

Ransomware is not the threat cluster. The cause path is `#9 → #7`. The DRE is Loss of Accessibility (`Ac`).

### B.5 Supply-Chain Incident With Regulatory Reporting

```text
#10 ||[update][@Vendor→@Org]|| → #7 + [SRE] + [DRE: C + I]
+ [BRE: BRE-REG.11 Mandatory Notification Obligation Triggered
   → BRE-REG.17 Cross-Border Authority Notification Obligation]
+ [Report: REPORT-NIS2.11 24h Early Warning Filed
   + REPORT-NIS2.12 72h Incident Notification Filed]
```

### B.6 Fake Tech Support Without Code Execution

```text
#9 ||[phone][@External→@Citizen]|| [Pattern: PATTERN-FIN.13 Fake Tech Support Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 900]
```

### B.7 Fake Tech Support With Remote Tool Execution

```text
#9 ||[phone][@External→@Citizen]|| [Pattern: PATTERN-FIN.13 Fake Tech Support Scam]
→ #7 + [SRE] + [DRE: C]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm → BRE-FIN.21 Unauthorized Bank Transfer Executed]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss]
```

---

## Appendix C — Why Not Split #9 Into Human Micro-Vulnerabilities?

A common objection is that `#9 Social Engineering` could be split into greed, fear, loneliness, urgency, authority bias, curiosity, fatigue, distraction, obedience, shame, or similar psychological factors.

TLCTC+ should not do this at the strategic layer.

The reason is simple: **NCSCs need a threat language, not a psychology taxonomy.**

Three arguments support this design choice:

1. **Human factors overlap.** Real cases combine urgency, trust, fear, authority, curiosity, and dependency.
2. **Human factors chain.** Curiosity creates engagement; engagement creates trust; trust enables payment or disclosure.
3. **It is the wrong professional layer.** National reporting needs stable case grammar. Psychological micro-factor analysis may be valuable for research and awareness design, but it should not destabilize the core reporting model.

Therefore:

```text
Strategic cause:        #9 Social Engineering
Operational narrative:  [Pattern: ...]
Consequence event:      + [BRE: ...]
Measured harm:          + [Impact: ...]
```

---

## Closing Sentence

**TLCTC identifies the cause. TLCTC+ structures the reporting consequence. That is enough for NCSCs, CERTs, and peer communities to stop debating labels and start building stable national practice.**
