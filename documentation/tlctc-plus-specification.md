# TLCTC+ Specification v0.5

## TLCTC-Anchored Digital-Harm Reporting Extension for NCSCs, CERTs, Regulators, and Financial-Crime Reporting

**Author:** Bernhard Kreinz  
**Base framework:** TLCTC v2.1  
**Extension version:** TLCTC+ v0.5  
**Status:** Draft for peer review  
**License:** CC BY 4.0  
**Core thesis:** Keep TLCTC pure. Extend the reporting layer.

> **v0.5 intent:** This version cleans and compresses v0.4. It keeps the v0.4 semantic decisions, removes most migration-heavy prose, and strengthens the introduction for expected peer groups: NCSCs, CERTs/CSIRTs, regulators, financial institutions, payment-service providers, fraud teams, GRC / operational-risk teams, CTI/SOC teams, law enforcement, insurers, standards bodies, and researchers.

---

## 0. One-Sentence Definition

**TLCTC+ is a TLCTC-anchored reporting grammar that connects cyber causes and #9 digital-harm anchors to explicit SRE, DRE, Pattern, BRE, Impact, and Report structures without turning consequences, scams, crimes, actors, or reporting duties into threat clusters.**

---

## 1. Executive Summary

TLCTC+ is a reporting extension for cases that have a TLCTC anchor.

It supports three reporting realities:

1. **Core cyber incidents** — a TLCTC attack path leads to Loss of Control / System Compromise.
2. **Hybrid cyber-enabled harms** — a TLCTC path exists, but the reporting interest is fraud, service impact, regulatory impact, citizen harm, or organizational consequence.
3. **Pure #9-anchored digital harms** — the case is digitally mediated and manipulation-driven, but no IT system is compromised.

TLCTC+ is not a new threat taxonomy. It does not add an eleventh cluster. It does not redefine ransomware, romance scams, account takeover, payment fraud, data breach, or outage as threats. Those are labels, outcomes, or reporting categories. The cause-side threat remains the TLCTC path.

TLCTC+ adds a controlled reporting grammar around the TLCTC path:

```text
TLCTC cause path
+ [SRE]
+ [DRE: C|I|Ac|Av]
[Pattern: ...]
+ [BRE: ...]
+ [Impact: ...]
+ [Report: ...]
```

Pattern is cause-side metadata and uses bracket-only notation. SRE, DRE, BRE, Impact, and Report are event or consequence annotations and use additive notation.

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

SOC and CTI teams need cause-side attack paths, not only business labels. A “BEC case” may be pure #9, #9 + DRE:C, #9 → #4, #9 → #7, or #10 → #7 depending on the actual chain.

**Value:** investigation and detection remain tied to real attack steps; indicators and controls map to the cause lane, not to the reporting label.

### 2.5 GRC, Operational Risk, and Enterprise Risk Management

Operational-risk taxonomies often consume loss-event and consequence labels. TLCTC+ provides the cyber/digital-harm portion while explicitly excluding non-cyber operational failure.

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
Specification document version:   TLCTC+ v0.5
PATTERN catalogue version:        v0.2
BRE catalogue version:            v0.3
IMPACT catalogue version:         v0.2
REPORT catalogue version:         v0.2
```

v0.5 is an editorial and structural cleanup. It does **not** add, remove, or renumber catalogue entries. The v0.4 catalogue decisions remain in force.

---

## 4. Scope

TLCTC+ covers exactly three case classes.

### 4.1 Core Cyber Incident

A TLCTC path leads to Loss of Control / System Compromise.

```text
#9 ||[email][@External→@Org]|| → #7 + [SRE] + [DRE: Ac]
+ [BRE: BRE-SVC.11 Payment Function Unavailable]
```

Canonical chain:

```text
TLCTC path → SRE → DRE* → BRE* → Impact* → Report*
```

### 4.2 Hybrid Cyber-Enabled Harm

A TLCTC path exists, but the reporting interest is consequence-side.

```text
#9 ||[email][@External→@Org]|| [Pattern: PATTERN-ID.11 Phishing for Credentials]
+ [DRE: C] → #4 + [SRE]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm → BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 80,000]
```

### 4.3 Pure #9-Anchored Digital Harm

No IT system is compromised. The digital harm is anchored on #9 Social Engineering.

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

A DRE may appear in a pure #9 case only when the manipulation itself directly causes data disclosure or resource impact without system compromise:

```text
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-ID.11 Phishing for Credentials]
+ [DRE: C]
```

If the disclosed credential, token, or identity artifact is later used, the case transitions to hybrid form:

```text
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-ID.11] + [DRE: C]
→ #4 + [SRE]
```

Credential acquisition is classified by the enabling cluster. Credential use is always #4.

---

## 5. Explicit Non-Scope

TLCTC+ v0.5 does **not** cover:

- non-cyber operational failures without a TLCTC anchor;
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
SRE is the cyber Bow-Tie central event.
DREs are data/resource risk events.
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
#10 → BRE-REG.*   supplier compromise causing notification obligation
```

---

## 7. Tracks

TLCTC+ uses six tracks. They are tracks, not layers, to avoid collision with TLCTC core layering.

```text
Cause Track       TLCTC path or #9 anchor; Pattern attaches here
SRE Track         System Risk Event / Loss of Control / System Compromise
DRE Track         Confidentiality, Integrity, Accessibility, Availability events
BRE Track         Business, citizen, regulatory, service, legal, or organizational events
Impact Track      Quantified or qualified harm measurement
Report Track      Reporting artefacts, workflow stages, authority filings
```

---

## 8. Notation

### 8.1 Cause Path

TLCTC cause paths use core TLCTC notation.

```text
#9 → #4 → #7
```

Bridge clusters (#8, #9, #10) MUST carry a boundary operator in TLCTC+ records:

```text
#9 ||[email][@External→@Org]||
#10 ||[update][@Vendor→@Org]||
```

### 8.2 SRE

```text
+ [SRE]
```

SRE is never a path step.

Incorrect:

```text
#7 → [SRE]
```

### 8.3 DRE

```text
+ [DRE: C]
+ [DRE: I]
+ [DRE: Ac]
+ [DRE: Av]
```

`Ac` = Loss of Accessibility.  
`Av` = Loss of Availability.  
`A` may be accepted for backward compatibility but new records SHOULD prefer `Ac` or `Av`.

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

### 8.6 Impact

```text
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

### 8.7 Report

```text
+ [Report: REPORT-NIS2.11 24h Early Warning Filed]
```

---

## 9. Normative Rules

### R-SRE

If a TLCTC attack path results in Loss of Control / System Compromise, the record MUST include `+ [SRE]`.

### R-SRE-OPTIONAL-9

If a case is purely #9-anchored digital harm and no IT system is compromised, the SRE node SHALL be omitted.

### R-DRE-PLACEMENT

A DRE applies to the immediately preceding TLCTC step or path segment unless linked explicitly in a structured record.

```text
#9 + [DRE: C] → #4
```

means the confidentiality loss occurred during #9.

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

Inside `[BRE: ...]`, `→` and `+` express consequence-side BRE causality or co-realization. Outside annotation brackets, they express TLCTC cause-side path sequence or parallelism. The two scopes MUST NOT mix.

### R-IMPACT

Loss amounts, downtime, customer counts, affected record counts, legal costs, regulatory fine amounts, and similar measurements SHOULD be Impact, not BRE.

### R-REPORT

REPORT codes describe reporting artefacts or workflow stages. They SHALL NOT appear inside BRE chains.

### R-BOUNDARY

Every #8, #9, and #10 step in a TLCTC+ record MUST carry an explicit v2.1 boundary operator.

```text
#9 ||[email][@External→@Org]||
#10 ||[service][@Provider→@Org]||
```

This is a TLCTC+ profile rule for reporting precision; it does not modify core TLCTC.

### R-RECOVERABILITY

For cyber records, stripping all SRE, DRE, BRE, Impact, Pattern, and Report annotations MUST recover a valid TLCTC v2.1 path.

For pure #9 records, stripping all annotations MUST recover a valid #9 bridge anchor.

### R-CAUSE-CONSEQUENCE-INDEPENDENCE

Consequence-side BRE families MUST be selected from observed harm, not auto-derived from cause-side cluster identity.

### R-NO-FREE-TEXT-BRE

New records MUST use structured BRE codes. Free-text labels may be retained for archival readability but must not be the canonical BRE value.

---

## 10. Minimal Grammar

```text
<tlctc-plus-record> ::= <cyber-record> | <pure-9-record>

<cyber-record> ::= <tlctc-path>
                   <sre-annotation>?
                   <dre-annotation>*
                   <bre-annotation>*
                   <impact-annotation>*
                   <report-annotation>*

<pure-9-record> ::= "#9" <boundary-annotation>
                    <pattern-annotation>?
                    <dre-annotation>?
                    <bre-annotation>+
                    <impact-annotation>*
                    <report-annotation>*
```

```text
<sre-annotation>     ::= "+ [SRE]"
<dre-annotation>     ::= "+ [DRE: " <dre-expression> "]"
<pattern-annotation> ::= "[Pattern: " <pattern-expression> "]"
<bre-annotation>     ::= "+ [BRE: " <bre-expression> "]"
<impact-annotation>  ::= "+ [Impact: " <impact-expression> "]"
<report-annotation>  ::= "+ [Report: " <report-expression> "]"
```

```text
<dre-node> ::= "C" | "I" | "Ac" | "Av" | "A"
```

---

## 11. Namespaces

```text
TLCTC-XX.YY       TLCTC operational threat notation
SRE               System Risk Event / Loss of Control / System Compromise
DRE-X             Data Risk Event
PATTERN-XXX.YY    Cause-side narrative / scam / fraud / crime pattern
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

# 13. BRE Catalogue v0.3

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
Loss of control / compromise   → SRE
Data/resource effect           → DRE
Scam/fraud/crime narrative     → Pattern
Observable consequence         → BRE
Severity / magnitude           → Impact
Filing / workflow state        → Report
```

This structure can support NCSC/CERT reporting, financial-sector fraud reporting, DORA-style ICT incident reporting, NIS2-style incident notification, data-protection reporting, and internal OpRisk aggregation while preserving the cause/effect separation of core TLCTC.

External regime labels may be retained as aliases or metadata, but they should not override TLCTC+ semantics.

---

# 17. Minimal Data Model

## 17.1 Record Types

```text
core_cyber_incident
hybrid_cyber_enabled_harm
pure_9_digital_harm
```

## 17.2 Required Metadata

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

## 17.3 Cause Fields

```text
tlctc_path
tlctc_steps[]
patterns[]
evidence[]
actor_attribution_optional
```

## 17.4 SRE Fields

```text
present
status: observed | confirmed | disputed | retracted | hypothesized
timestamp
description
scope
linked_to_step
confidence
```

## 17.5 DRE Fields

```text
type: C | I | Ac | Av | A
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
timestamp_due
timestamp_filed
authority
status
linked_to_bre_reg
linked_to_sre
linked_to_dre
```

---

# 18. Example JSON Records

## 18.1 Pure #9 Digital Harm

```json
{
  "case_id": "case-002",
  "record_type": "pure_9_digital_harm",
  "tlctc_plus_version": "0.5",
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

## 18.2 Hybrid BEC / Invoice Fraud

```json
{
  "case_id": "case-003",
  "record_type": "hybrid_cyber_enabled_harm",
  "tlctc_plus_version": "0.5",
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
      "description": "Credential disclosed through social engineering"
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

# 19. Worked Examples

## 19.1 Romance Scam, No Cyber Compromise

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.11 Romance / Relationship Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 4,500]
```

No SRE. No DRE. #9 is the cause-side anchor.

## 19.2 Phishing With Credential Disclosure, No Observed Use Yet

```text
#9 ||[email][@External→@Citizen]|| [Pattern: PATTERN-ID.11 Phishing for Credentials]
+ [DRE: C]
```

No SRE yet. If the credential is later used, append `→ #4 + [SRE]`.

## 19.3 Investment Scam With Account Takeover

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.12 Investment / Crypto-Investment Scam]
+ [DRE: C] → #4 + [SRE]
+ [BRE: BRE-ENT.13 Email Account Takeover Harm → BRE-FIN.23 Unauthorized Crypto Transfer Executed]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 30,000]
```

Credential acquisition is #9. Credential use is #4. The transfer is unauthorized because the attacker executed it through the taken-over account.

## 19.4 Victim-Authorized Crypto Transfer

```text
#9 ||[messaging][@External→@Citizen]|| [Pattern: PATTERN-FIN.12 Investment / Crypto-Investment Scam]
+ [BRE: BRE-FIN.12 Authorized Crypto Transfer Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = EUR 30,000]
```

No SRE and no #4 unless credential use or system compromise is observed.

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
#10 ||[update][@Vendor→@Org]|| → #7 + [SRE] + [DRE: C + I]
+ [BRE: BRE-REG.11 Mandatory Notification Obligation Triggered
   → BRE-REG.17 Cross-Border Authority Notification Obligation]
+ [Report: REPORT-NIS2.11 + REPORT-NIS2.12 + REPORT-NIS2.14]
```

The #10 step occurs at the Trust Acceptance Event. Reporting obligations are BRE/Report, not threat clusters.

## 19.7 Fake Tech Support Without Code Execution

```text
#9 ||[phone][@External→@Citizen]|| [Pattern: PATTERN-FIN.13 Fake Tech Support Scam]
+ [BRE: BRE-FIN.11 Authorized Push Payment Made]
+ [Impact: IMPACT-FIN.12 Direct Fraud Loss = CHF 900]
```

No SRE, no DRE, no #7.

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

The stolen credential is a technical identity. Cause-side credential use is still #4. The consequence is service impact, not automatically BRE-ENT.

---

# 20. Decision Procedure

1. **Is there a TLCTC-classifiable cyber cause path?**  
   If yes, classify each step using core TLCTC.

2. **If not, is there a pure #9 digital-harm anchor?**  
   If a human was psychologically manipulated through a digital channel, record #9 with a boundary operator.

3. **Did Loss of Control / System Compromise occur?**  
   If yes, attach `+ [SRE]`. If no and the case is pure #9, omit SRE.

4. **Did a Data Risk Event occur?**  
   Attach `+ [DRE: C|I|Ac|Av]` to the step or segment that caused it.

5. **Is there a scam/fraud/crime narrative?**  
   Attach `[Pattern: ...]` to the cause-side step.

6. **Did a business, citizen, regulatory, legal, service, third-party, or organizational event occur?**  
   Attach `+ [BRE: ...]`.

7. **Can the harm be measured?**  
   Attach `+ [Impact: ...]`.

8. **Was a report filed, required, or routed?**  
   Attach `+ [Report: ...]`. If an obligation was triggered, also attach the regulatory BRE.

---

# 21. Conformance

A TLCTC+ v0.5 record is conformant if it:

1. uses a TLCTC path or #9 anchor;
2. does not introduce new TLCTC top-level clusters;
3. records SRE explicitly when Loss of Control / System Compromise occurred;
4. omits SRE only for pure #9 digital harm or pre-compromise hypothesis records;
5. records DREs as `+ [DRE: ...]`, never as path steps;
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
17. recovers a valid TLCTC v2.1 path or #9 bridge anchor when TLCTC+ annotations are stripped.

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
- TLSFC or another failure-cause framework handles non-adversarial operational failure.
- BRE, Impact, and Report catalogues may become shared consequence-side assets.

---

# 23. Changelog

## 23.1 v0.5 changes from v0.4

1. Condensed the document into a shorter implementation specification.
2. Added a peer-facing rationale section for expected interest groups.
3. Kept the three case classes: `core_cyber_incident`, `hybrid_cyber_enabled_harm`, and `pure_9_digital_harm`.
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

## BRE — Business Risk Event

A discrete, observable business, citizen, service, legal, regulatory, third-party, or organizational event on the consequence side.

## DRE — Data Risk Event

Loss of Confidentiality (`C`), Integrity (`I`), Accessibility (`Ac`), or Availability (`Av`).

## Impact

A quantified or qualified measurement attached to SRE, DRE, or BRE.

## Pattern

Cause-side metadata describing the scam, fraud, extortion, manipulation, or reporting narrative instantiated by a TLCTC step.

## Report

A procedural artefact, report filing, workflow stage, authority communication, or routing state.

## SRE — System Risk Event

Loss of Control / System Compromise. The cyber Bow-Tie central event.

## Technical Identity

A non-human principal or identity artifact such as a service account, API key, machine credential, OAuth client secret, certificate, robot/RPA account, or service ticket. Credential use remains #4 on the cause side; the consequence-side BRE depends on observed harm.

## TLCTC+

A TLCTC-anchored reporting profile for cyber incidents, hybrid cyber-enabled harms, and pure #9 digital harms.

