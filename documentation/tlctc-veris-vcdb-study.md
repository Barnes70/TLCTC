# What a Cause Axis Recovers from VERIS: A TLCTC Reading of 10,047 VCDB Records

**Author:** Bernhard Kreinz
**Version:** 1.0
**Date:** 2026-09-18
**License:** CC BY 4.0
**Implements:** TLCTC framework specification v2.5 (canonical dictionary `json-schemas/layer-1/tlctc-framework.v2.5.json`); VERIS 1.4.1 (vz-risk/veris commit `45d9d7a`, 2026-06-12); VERIS Community Database snapshot of 2026-08-04 (vz-risk/VCDB commit `230cf22`, joined dataset, 10,047 records). This study introduces no normative content; every cluster, axiom and rule is cited from the core paper and the dictionary.
**Companion to:** *A Cause-Oriented Cyber Threat Taxonomy: The TLCTC Framework* (v2.5 core paper) — DOI [10.5281/zenodo.20633176](https://doi.org/10.5281/zenodo.20633176); the mapping itself lives in `mappings/veris/` of the TLCTC repository.

## Abstract

VERIS, the Vocabulary for Event Recording and Incident Sharing, is the most widely used structured format for recording security incidents and the data spine of the Verizon Data Breach Investigations Report. Its A4 model records an incident as actors, actions, assets and attributes, and its maintainers have stated since version 1.3.2 that a future 2.0 would add sequencing of those elements. This study asks what a cause-oriented threat taxonomy adds to a VERIS record as it stands today. A mapping from every VERIS 1.4.1 action variety, action vector, action result and attribute value to the TLCTC v2.5 clusters was built (337 entries in seven mapping types), applied by a deterministic classifier to the 10,047 records of the VERIS Community Database, and cross-checked against the independently built VERIS → ATT&CK and ATT&CK → TLCTC mappings. Three findings stand out. First, more than a quarter of VCDB records carry no threat at all under the TLCTC axioms: they record errors and environmental events, which VERIS keeps on the same axis as attacks. Second, among records that do carry a threat, roughly one in seven names a cluster whose rules require a companion step the record does not contain, most often malware without its delivery step or credential use without its acquisition step, and roughly one in four needs a rule VERIS does not encode (the role of the flawed component, or capacity versus defect) before a single cluster can be assigned. Third, ransomware, the dominant recent incident type, is recorded without any availability attribute in seven of ten cases, so the distinction between data that is gone and data that is present but unusable, which determines recovery posture, cannot be read from the record. The mapping is offered to the VERIS project as a framework crosswalk in the format of its existing ATT&CK and CIS mappings; the study is the evidence for what the crosswalk recovers and for what only sequencing can recover.

**Keywords:** VERIS; VCDB; DBIR; incident classification; cause-oriented taxonomy; TLCTC; attack paths; data risk events; sequencing

## 1. Introduction

The Vocabulary for Event Recording and Incident Sharing (VERIS) [1] was designed to make incidents comparable across organisations. Its four core sections, Actor, Action, Asset and Attribute, are enumerations: an incident is recorded by ticking the values that apply. Thousands of reporters, the VERIS Community Database (VCDB) [2] and the Verizon Data Breach Investigations Report (DBIR) [3] speak this dialect, which is why any evolution of VERIS has to respect its installed base.

The framework's own maintainers have named its main structural limit. The README of the VERIS repository states that "Version 2.0 will be for major feature additions. The primary one being considered is adding sequencing of the 4A's, timeline, and discovery method so that the sequence things happened in in the incident can be captured" [4]. The corresponding issue, *Add Sequencing to VERIS*, has been open since June 2016 [5]. Without sequencing, a record that ticks Social and Hacking and Malware says that all three occurred but not which enabled which.

TLCTC approaches incidents from the other end. It classifies by cause: each of its ten clusters is defined by the generic vulnerability an attack step exploits, outcomes are recorded separately as Data Risk Events, and an incident is an ordered sequence of cluster steps, an attack path, with a velocity annotation between steps [6]. The framework's rules are explicit about companion steps: foreign code that executes is a #7 step at the moment of execution and needs a delivering step before it (R-EXEC); credential use is always #4 and needs an acquisition step before it (R-CRED); manipulation of a person is #9 and needs a technical follow-on after it. These rules are exactly the sequencing VERIS 2.0 has been promising.

An earlier essay [7] argued, on the structure of the two schemas, that VERIS's Action axis mixes causes, outcomes, errors and environmental events, and that the pragmatic evolution is to replace the semantics of that axis while keeping the four-letter mnemonic. This study tests that argument on data. It builds the mapping, applies it to every record in VCDB, and reports what the record can establish about cause, what it cannot, and where the two independent routes from VERIS to TLCTC disagree.

The study makes no claim about breaches in general. VCDB is a convenience sample of publicly reported incidents with known selection effects, which are stated in §2.3 and carried through every table as strata.

## 2. Method

### 2.1 The mapping

The mapping (`mappings/veris/tlctc-veris.json`, rendered as `veris-1.4.1_tlctc-2.5.csv` for the VERIS repository) has one entry for every value of VERIS 1.4.1 under `action.<category>.variety`, `action.<category>.vector`, `action.<category>.result`, `attribute.confidentiality.data_disclosure`, `attribute.integrity.variety` and `attribute.availability.variety`, plus one entry for a record whose action category is `unknown`. Coverage is total and machine-checked against the pinned VERIS enumeration file. Every entry carries the VERIS description verbatim, a mapping type, and a one-sentence rationale that names the rule or axiom applied.

The seven mapping types encode what a VERIS value can say about cause:

| Type | Entries | Meaning |
|---|---|---|
| `direct` | 60 | The value names exactly one generic vulnerability: one cluster. |
| `conditional` | 6 | The value spans clusters; a named rule with a stated question decides (R-ROLE for `Exploit vuln`, R-FLOOD for `DoS`, R-EXEC for `Backdoor` and `Adminware`, R-SUPPLY for `Forgery`). |
| `chain` | 47 | The value names one cluster, and the rules require a companion step that VERIS does not record: every malware variety (#7, R-EXEC), every social variety (#9), and credential application (#4, R-CRED). |
| `context` | 65 | Vectors: no cluster. The value annotates the boundary context, a responsibility-sphere crossing, an intra-system boundary, or a role hint. |
| `no-cluster` | 51 | Off the threat axis: the cause-side partition row is named (failure, error in use, abuse of rights), or the action is intentional but involves no IT-system step. |
| `outcome` | 87 | Not a cause (Axiom III). Attribute values map to a Data Risk Event code; action results map to nothing. |
| `unresolved` | 21 | `Other` and `Unknown`: the record says something happened without saying what. |

The decisions that carry weight in the results are these. `Exploit vuln` maps to #2 or #3 by R-ROLE, which VERIS cannot decide because it does not record whether the flawed component served the attacker or consumed attacker content; its named children (SQL injection, buffer overflow, path traversal and so on) are attacks on the victim's service and map to #2 directly, with cross-site scripting, cross-site request forgery and open-redirect abuse mapping to #3. `Use of stolen creds`, `Pass-the-hash`, `Session replay` and `Offline cracking` are #4 with an acquisition step before them. Every malware variety is #7 at the moment of execution with the enabling step before it; the capability VERIS names (backdoor, ransomware, keylogger) is a feature of the payload, not a separate step. `Privilege abuse` and the other insider varieties that exceed the granted purpose are #1; `Unapproved software`, `Unapproved workaround`, `Net misuse` and their kin are in-grant policy violations and sit on the Abuse of Rights row with no cluster (R-SCOPE). All `error` varieties are Error in Use or Failure, and all `environmental` varieties are Failure, with no cluster (Axiom V, Axiom II). `Extortion`, `Propaganda` and `Assault` act on people without an IT-system step and are outside the core clusters. On the outcome side, `Obscuration` is Ac (data present but unusable), `Loss` and `Destruction` are Av (data gone), and `Interruption`, `Degradation` and `Acceleration` keep the parent code A because the record does not say which. The full table, with every rationale, is the mapping file; the walk-through is `mappings/veris/decision-tree.md`.

### 2.2 The classifier

A standard-library Python classifier (`mappings/veris/cli`) reads a VERIS record, collects its values, and reports: the clusters that are *certain* (from direct and chain entries), the *rule-dependent groups* of alternatives (from conditional entries), every *chain* with whether a companion cluster is recorded elsewhere in the same record or *lost*, the cause-side *partition rows* touched, the Data Risk Events, the boundary context, and the values that resolve to nothing. Two derived sets are used throughout: the *lower bound* (certain clusters only) and the *upper bound* (certain plus every alternative of every rule-dependent group). A record is *threat-bearing* if it has at least one certain cluster or one rule-dependent group.

No attack path is emitted. VERIS records an unordered set of actions, and the classifier does not invent an order; where it reports a sequence it is labelled as the hypothesis the companion rules imply, not as an observation.

### 2.3 Data and strata

The dataset is VCDB's packaged joined file at commit `230cf22` (2026-08-04): 10,047 records, of which 9,907 are on schema 1.4.0, 111 on 1.4.1 and 29 on 1.3.x. VCDB's own packaging excludes about 5,000 web-skimmer breaches that were discovered by script in one batch, and the study inherits that exclusion. The zip's SHA-256 is recorded in the results file and in `mappings/veris/PINNED.md`; no record is stored in the TLCTC repository except twenty test fixtures under their own CC BY-SA 4.0 notice.

The VCDB README warns that most issues are chosen randomly but healthcare incidents (`plus.sub_source = phidbr`) and priority incidents (`priority`) are selected on purpose [2]. Every table below is therefore reported for the whole set and for strata: by incident year (up to 2014; 2015 to 2019; 2020 to 2026) and by `plus.sub_source` (none; phidbr; priority; other). Year strata are uneven: 5,684 records date from 2014 or earlier, 3,046 from 2015 to 2019 and 1,317 from 2020 onwards. The 2020 to 2026 stratum is the most recent coding practice and the closest to what a VERIS 2.0 would inherit.

### 2.4 The cross-check

The VERIS repository publishes a VERIS → ATT&CK mapping (1,270 edges, VERIS 1.4.1 to ATT&CK 19.1, in the MITRE Center for Threat-Informed Defense Mappings Explorer format [8]); the TLCTC repository publishes an ATT&CK → TLCTC mapping (698 techniques). Composing the two gives a second, independently built route from a VERIS value to clusters. For each record, the classifier compares the clusters its action varieties reach directly with the clusters they reach through ATT&CK. Only action varieties whose direct mapping names clusters take part; vectors, results and attributes have ATT&CK edges but no cluster on the direct route (Axiom III), so including them would measure that difference of scope, not the soundness of the mapping. A record *agrees* when every cluster the direct route names is also reached through ATT&CK, is a *subset* case when the two routes overlap but the direct route names a cluster ATT&CK does not reach, is *disjoint* when both routes name clusters and share none, and has *no ATT&CK edge* when none of its cluster-bearing varieties is mapped upstream.

### 2.5 What is not claimed

The mapping is one analyst's reading of the VERIS descriptions against the TLCTC rules; no inter-rater test has been run. The numbers describe VCDB as coded, not the population of incidents. Where VERIS coders left a value `Unknown`, the study counts an unresolved step and does not guess.

## 3. The Mapping by Category

Table 1 summarises the mapping per VERIS action category. The counts are entries, not records; the cluster column lists the clusters the category's varieties name and how many varieties name each.

**Table 1. Mapping entries per VERIS 1.4.1 action category (varieties).**

| Category | Entries | direct | conditional | chain | no-cluster | outcome | unresolved | Clusters named (varieties) |
|---|---|---|---|---|---|---|---|---|
| hacking | 56 | 43 | 3 | 6 | 1 | 1 | 2 | #2 ×33, #1 ×8, #4 ×5, #3 ×5, #5 ×3, #6 ×1, #7 ×1 |
| malware | 38 | 2 | 2 | 31 | 0 | 1 | 2 | #7 ×30, #1 ×2, #4 ×2, #3 ×2, #2 ×1 |
| social | 15 | 0 | 1 | 9 | 2 | 1 | 2 | #9 ×10, #10 ×1 |
| misuse | 15 | 5 | 0 | 1 | 6 | 1 | 2 | #1 ×5, #4 ×1; Abuse of Rights row ×6 |
| physical | 14 | 10 | 0 | 0 | 1 | 1 | 2 | #8 ×10 |
| error | 16 | 0 | 0 | 0 | 16 | 0 | 0 | Error in Use row ×12, Failure row ×4 |
| environmental | 25 | 0 | 0 | 0 | 25 | 0 | 0 | Failure row ×25 |

The 65 vector entries are all `context` (plus 12 `unresolved` for `Other`/`Unknown` vectors): the `Partner` vector in hacking, malware and social marks a responsibility-sphere crossing `@Vendor→@Org` whose cluster is #10 only if a trust artefact was honoured (R-SUPPLY), otherwise the partner is a transit carrier; `Software update` marks the `[update]` context and a Trust Acceptance Event; the mail, messaging, phone and in-person vectors mark the `[human]` context of a #9 step; `Web application` and the remote-access services are server-role hints for R-ROLE; `Email autoexecute` and `Web application - drive-by` are client-role hints. The 54 action result entries are outcomes with no Data Risk Event of their own: `Infiltrate`, `Elevate`, `Persist` and the rest describe what a step achieved, not the vulnerability it exploited.

Table 2 gives the outcome side. VERIS records what was lost in three attribute enumerations; TLCTC records the same facts as Data Risk Event codes on the record that changed state.

**Table 2. Attribute values → Data Risk Event codes.**

| VERIS attribute value | DRE | Reading |
|---|---|---|
| `confidentiality.data_disclosure = Yes` | C | confirmed disclosure |
| `confidentiality.data_disclosure = Potentially` | C (potential) | at risk, not confirmed |
| `integrity.variety` = Modify data, Defacement, Modify configuration, Log tampering, Hardware tampering, Software installation, Modify privileges, Modify authentication, Register MFA device, Created account, Repurpose | Ii | the record no longer corresponds to its intended state |
| `integrity.variety` = Misrepresentation, Fraudulent transaction | If | content may be accurate, attribution is false |
| `integrity.variety` = Other, Unknown | I | refinement unknown |
| `integrity.variety` = Alter behavior | none | a person's behaviour, not a record |
| `availability.variety` = Obscuration | Ac | present but unusable (ransomware) |
| `availability.variety` = Loss, Destruction | Av | gone |
| `availability.variety` = Interruption, Degradation, Acceleration, Other, Unknown | A | refinement not recorded |

Two rows of Table 1 deserve a note because they are where a VERIS reader would expect a cluster and the mapping gives none. `Extortion`, `Propaganda` and `Assault` are intentional and outside any grant, but they act on a person and involve no IT-system step; TLCTC's core clusters classify steps against systems, and a demand or a threat belongs to the business-side event chain. `Reverse engineering` is attacker-side preparation and touches no victim system. Both readings follow the cause-side partition of the dictionary and the scope decisions of the core paper; neither invents a category.

## 4. Results

All numbers are taken from `mappings/veris/study/results.json` (generated 2026-09-18 from the snapshot of §2.3); `results.md` holds every table for every stratum. Percentages are of the row's denominator.

### 4.1 Threat-axis purity

Under Axiom V (control failures are not threats) and Axiom II (the framework scopes to interactions between systems and actors), a record whose only actions are errors or environmental events carries no cluster. Table 3 shows how much of VCDB that is.

**Table 3. Records by threat-axis status.**

| Status | all (10,047) | ≤2014 (5,684) | 2015–2019 (3,046) | 2020–2026 (1,317) | sub_source none (8,110) | phidbr (1,310) | priority (602) |
|---|---|---|---|---|---|---|---|
| threat-bearing (≥1 cluster or rule-dependent group) | 5,632 (56.1%) | 2,869 (50.5%) | 1,701 (55.8%) | 1,062 (80.6%) | 4,679 (57.7%) | 757 (57.8%) | 185 (30.7%) |
| operational risk only, no cluster | 2,615 (26.0%) | 1,612 (28.4%) | 855 (28.1%) | 148 (11.2%) | 1,993 (24.6%) | 403 (30.8%) | 207 (34.4%) |
| — of which error in use or failure | 2,578 | 1,591 | 841 | 146 | 1,967 | 393 | 206 |
| — of which abuse of rights (in-grant misuse) | 33 | 17 | 14 | 2 | 22 | 10 | 1 |
| unknown only (action recorded, nothing named) | 1,800 (17.9%) | 1,203 (21.2%) | 490 (16.1%) | 107 (8.1%) | 1,438 (17.7%) | 150 (11.5%) | 210 (34.9%) |
| threat and operational actions mixed | 168 (1.7%) | 90 | 76 | 2 | 130 | 32 | 5 |

A quarter of the database is not a threat record at all in TLCTC terms, and in the priority stratum it is a third. The dominant single signatures (§4.6) are `error.variety.Misdelivery` alone (952 records) and `error.variety.Loss` alone (382): misdirected mail and lost devices. These are real incidents with real Data Risk Events (2,187 of the 2,615 carry a confirmed outcome: 1,922 a disclosure, 414 a loss of availability), but they have no attacker and no exploited generic vulnerability; in the bow-tie they enter at the event, not the threat. VERIS puts them on the same Action axis as SQL injection, which is what makes a DBIR pattern such as "Miscellaneous Errors" sit beside "System Intrusion" as if both answered the question *which threat*. The mixed row is small: coders rarely combine an error with an attack in one record.

### 4.2 Cause recoverability

For the 5,632 threat-bearing records, Table 4 asks whether the VERIS actions determine a cluster set or leave a rule to be applied, and whether the rules' companion steps are present.

**Table 4. Threat-bearing records by recoverability.**

| Status | all (5,632) | ≤2014 (2,869) | 2015–2019 (1,701) | 2020–2026 (1,062) | none (4,679) | phidbr (757) | priority (185) |
|---|---|---|---|---|---|---|---|
| resolved: direct rows only, companions present or not required | 3,546 (63.0%) | 2,315 (80.7%) | 1,162 (68.3%) | 69 (6.5%) | 2,911 (62.2%) | 559 (73.8%) | 70 (37.8%) |
| rule-dependent: ≥1 group VERIS cannot decide | 1,310 (23.3%) | 380 (13.2%) | 145 (8.5%) | 785 (73.9%) | 1,246 (26.6%) | 15 (2.0%) | 49 (26.5%) |
| cause lost: a required companion step is absent | 776 (13.8%) | 174 (6.1%) | 394 (23.2%) | 208 (19.6%) | 522 (11.2%) | 183 (24.2%) | 66 (35.7%) |
| — malware with no enabling step (#7 without its delivery) | 422 (7.5%) | 88 | 223 | 111 | 258 | 119 | 40 |
| — credential use with no acquisition step (#4 alone) | 206 (3.7%) | 55 | 55 | 96 | 162 | 24 | 20 |
| — social engineering with no follow-on (#9 alone) | 148 (2.6%) | 31 | 116 | 1 | 102 | 40 | 6 |
| records with ≥2 clusters in the upper bound | 1,720 (30.5%) | 599 | 304 | 817 | 1,566 | 84 | 68 |
| mean clusters per record, lower / upper bound | 1.08 / 1.68 | | | | | | |

Three readings. First, the rule-dependent share is driven by two values: `hacking.variety.Exploit vuln` (1,034 records; #2 or #3 by R-ROLE) and `hacking.variety.Backdoor` (747; #1 or #7 by R-EXEC), with `DoS` (166; R-FLOOD) third. VERIS does not record the role of the flawed component or whether the persistence was a designed function or an implant, so a single cluster cannot be assigned from the record. Second, the cause-lost share rises from 6% in the oldest stratum to 20% in the newest, and the value that most often loses its companion is `malware.variety.Ransomware` (280 records with no other action): the record says that foreign code executed and encrypted data, and nothing about how it got there. `Use of stolen creds` alone (206) is the same pattern for credentials, and `Phishing` alone (105) for the human step. Third, the upper bound doubles the mean cluster count of the lower bound; the difference is the information VERIS would need to record, or a coder would need to decide, before the record could carry one path.

### 4.3 Cluster frequency and co-occurrence

Figure 1 (`images/veris-cluster-frequency.svg`) and Table 5 give the number of records touching each cluster, as a lower bound (certain) and an upper bound (with rule-dependent alternatives).

**Table 5. Records touching each cluster, certain / upper bound.**

| Cluster | all (10,047) | sub_source none (8,110) | 2020–2026 (1,317) |
|---|---|---|---|
| #1 Abuse of Functions | 1,748 / 2,497 | 1,340 / 2,089 | 27 / 774 |
| #2 Exploiting Server | 145 / 1,289 | 120 / 1,231 | 4 / 785 |
| #3 Exploiting Client | 14 / 1,291 | 12 / 1,233 | 1 / 785 |
| #4 Identity Theft | 505 / 505 | 397 / 397 | 121 / 121 |
| #5 Man in the Middle | 11 / 11 | 11 / 11 | 0 / 0 |
| #6 Flooding Attack | 0 / 166 | 0 / 164 | 0 / 2 |
| #7 Malware | 1,482 / 1,483 | 1,281 / 1,282 | 878 / 878 |
| #8 Physical Attack | 1,593 / 1,593 | 1,419 / 1,419 | 13 / 13 |
| #9 Social Engineering | 573 / 587 | 454 / 462 | 29 / 29 |
| #10 Supply Chain Attack | 0 / 18 | 0 / 12 | 0 / 0 |

![Figure 1. Records touching each cluster.](images/veris-cluster-frequency.svg)

Two features of the historical VCDB are visible at once: #8 (1,593 records, 1,182 of them with `physical.variety.Theft`: lost and stolen devices) and #1 (1,748, 1,200 of them with `misuse.variety.Privilege abuse`) are the largest certain clusters, which reflects the years and the breach-notification sources the database draws on rather than the current threat landscape. #6 never becomes certain because VERIS's `DoS` cannot say whether capacity or a defect was exploited, and #10 never becomes certain because VERIS marks supply chain through the `Partner` vector and `Forgery`, neither of which records a Trust Acceptance Event. #2 and #3 are almost entirely upper bound: 1,034 `Exploit vuln` records that VERIS cannot place on either side of R-ROLE. The 2020 to 2026 column is #7 country: 878 of 1,317 records, and the reason is §4.6.

Co-occurrence is the closest an unordered record comes to an edge in an attack path. 541 records (5.4%) carry two or more certain clusters; Figure 2 (`images/veris-cooccurrence.svg`) is the matrix. The ten most frequent pairs, with the order the companion rules imply, are: #7 + #9 (251; #9 → #7), #4 + #9 (201; #9 → #4), #4 + #7 (136; either order), #1 + #9 (67; #9 → #1), #1 + #8 (54; order unknown), #1 + #4 (17; #1 → #4), #8 + #9 (13), #1 + #7 (10; #1 → #7), #4 + #8 (10), #2 + #7 (9; #2 → #7). The first two are the phishing-to-malware and phishing-to-credential chains the core paper's worked examples describe; VERIS records both ends and not the arrow, which is what issue #127 asks for.

![Figure 2. Records in which two clusters are both certain.](images/veris-cooccurrence.svg)

### 4.4 Availability: Av versus Ac

TLCTC refines Availability into Av (data gone) and Ac (data present but unusable, the ransomware case) because the two call for different recovery postures and are told apart by inspecting the record, not by the story of how it got there. Table 6 re-reads VERIS's availability varieties.

**Table 6. `attribute.availability.variety` re-read as DRE codes (all records).**

| VERIS value | records | DRE |
|---|---|---|
| Loss | 2,061 | Av |
| Interruption | 309 | A (refinement not recorded) |
| Obscuration | 295 | Ac |
| Destruction | 44 | Av |
| Degradation | 26 | A |
| Unknown / Other | 9 | A |
| any availability attribute | 2,669 of 10,047 | |

![Figure 3. Availability varieties as DRE codes and the ransomware split.](images/veris-availability-split.svg)

The enumeration can express the distinction: `Obscuration` is Ac and `Loss` or `Destruction` is Av. The records mostly do not. Of the 1,084 records with `malware.variety.Ransomware`, 290 (26.8%) carry `Obscuration`, 13 carry `Loss`, 16 carry `Interruption`, and 772 (71.2%) carry no availability attribute at all; 849 (78.3%) carry a confirmed confidentiality disclosure. In the 2020 to 2026 stratum the gap is wider: 754 of 873 ransomware records (86.4%) have no availability attribute. The recent VCDB therefore records ransomware as a confidentiality event with the encryption unstated, which is consistent with a coding practice driven by breach notifications (which report disclosure) rather than by incident response (which reports what was encrypted). Whatever the reason, the distinction that decides whether backups or decryption are the recovery path cannot be read from seven in ten ransomware records.

### 4.5 Unknown collapse

**Table 7. Records that give up on the action.**

| Measure | all (10,047) | 2020–2026 (1,317) | priority (602) |
|---|---|---|---|
| `action.unknown` (no category at all) | 287 (2.9%) | 19 | 26 |
| any variety `Unknown` or `Other` | 3,255 (32.4%) | 219 (16.6%) | 290 (48.2%) |
| unknown only (no cluster, no operational row) | 1,800 (17.9%) | 107 (8.1%) | 210 (34.9%) |
| hacking records / with variety `Unknown` | 3,368 / 1,695 (50.3%) | 1,038 / 131 (12.6%) | 295 / 208 (70.5%) |
| malware records / with variety `Unknown` | 1,647 / 172 (10.4%) | 879 / 1 | |

Half of all hacking records say `Unknown` for the variety, and `hacking.variety.Unknown` alone is the single most frequent action signature in the database (1,369 records). In TLCTC notation these records are `?`: something happened, the cluster cannot be defended, and the record is excluded from cluster statistics rather than counted under a catch-all (R-UNRES-3). The recent stratum is much better on hacking (12.6%) for the reason given next.

### 4.6 Template coding

The `signatures` table counts the exact set of action varieties a record carries. VCDB has 534 distinct signatures, but the 2020 to 2026 stratum has 66, and one of them accounts for 747 of its 1,317 records (56.7%): `hacking.variety.Backdoor` + `hacking.variety.Exploit vuln` + `malware.variety.Backdoor` + `malware.variety.Backdoor or C2` + `malware.variety.Ransomware`. This is a coding template (VCDB's issue labels name templates such as `Malware-ext-Ransomware-databreach`), applied to ransomware incidents whose actual initial access was not reported. The mapping cannot tell a template from an observation: it dutifully reports #7 certain, #2 | #3 and #1 | #7 rule-dependent, companion present. The 785 rule-dependent records of the 2020 to 2026 stratum in Table 4 are almost entirely this signature, and so are the #2/#3 upper bounds of Table 5. The honest TLCTC rendering of such a record is `? → #7 + [DRE: C, Ac]`: an unresolved delivery step, malware at execution, and the outcomes. VERIS has no way to say "not reported" other than `Unknown`, and the template chose to assert `Exploit vuln` instead.

### 4.7 ATT&CK-transitive agreement

**Table 8. Agreement between the direct VERIS → TLCTC route and the VERIS → ATT&CK → TLCTC route.**

| Class | all (10,047) | 2020–2026 (1,317) | sub_source none (8,110) |
|---|---|---|---|
| agree | 2,120 (21.1%) | 1,027 (78.0%) | 1,732 |
| subset (overlap, direct names a cluster ATT&CK does not reach) | 288 (2.9%) | 3 | 284 |
| disjoint | 9 (0.1%) | 0 | 8 |
| no ATT&CK edge for any cluster-bearing variety | 7,630 (75.9%) | 287 | 6,086 |

Where both routes speak, they agree on 2,120 of 2,417 records (87.7%) and contradict each other on nine. The nine, and the 288 subset cases, are explained by a handful of values: `malware.variety.Capture stored data` (187 records; direct #7, transitive #1, #4, #5, because ATT&CK's collection techniques are classified by the function they use, not by the payload that uses them), `malware.variety.Scan network` (106; #7 versus #1, same reason), `hacking.variety.Forced browsing` (19; #2 versus #1, #7), and a few single-digit cases (`Packet sniffer`, `Buffer overflow`, `OS commanding`, `Cryptanalysis`, `Session prediction`, malware `DoS`). All of them are the same disagreement in different clothes: VERIS's malware varieties name a *capability of a payload*, which the direct mapping classifies as #7 at execution under R-EXEC, while the ATT&CK route classifies the *technique the payload performs*, which is often function abuse (#1). Both are defensible readings of a value that does not say whether foreign code ran; the direct mapping follows VERIS's own placement of the value under `malware`. The three-quarters of records with no ATT&CK edge are the errors, the physical thefts, the insider misuse and the `Unknown` hacking, which ATT&CK does not model.

## 5. Discussion

**What a cause axis recovers without any change to VERIS.** Applying the mapping to a record as coded already separates the threat from the non-threat (Table 3), names the cluster for 63% of threat-bearing records (Table 4), turns the availability enumeration into Av/Ac where the coder filled it in (Table 6), and produces cluster frequencies with an honest lower and upper bound (Table 5). A VERIS user can have all of this today by joining `veris-1.4.1_tlctc-2.5.csv` to their records, exactly as they join the ATT&CK crosswalk.

**What the crosswalk cannot recover.** Three things are structurally absent from a VERIS record and no mapping can supply them. The first is the role of the flawed component: `Exploit vuln` is #2 or #3 and the record does not say (1,034 records). The second is the companion step: 776 records name a cluster whose rules require a step before or after it, and the record has none; a malware record without its delivery, a credential-use record without its theft. The third is order: 541 records name two or more clusters and none says which came first. The first could be fixed with one enumeration (`role: server | client` on `Exploit vuln`); the second and third are the sequencing that issue #127 has asked for since 2016. TLCTC's Layer 3 record is one concrete shape that sequencing could take: an ordered list of steps, each with one cluster, a velocity annotation between steps, and the Data Risk Events on the step that produced them. The earlier essay's A4⁺ proposal [7] is the same idea expressed inside the VERIS mnemonic.

**Templates are a data-quality finding, not a taxonomy finding.** The 747-record ransomware signature of §4.6 is a property of how VCDB is coded, and it inflates every statistic that counts `Exploit vuln` or `Backdoor` in recent years. Any consumer of VCDB, with or without TLCTC, should treat the five-value signature as "ransomware, initial access not reported". A cause-oriented reading makes the problem visible because it asks the record for an enabling step and finds a placeholder.

**Ransomware is recorded as disclosure, not as inaccessibility.** 71% of ransomware records, and 86% since 2020, carry no availability attribute. If the DBIR's ransomware statistics are computed from records coded like VCDB's, the encryption, the event that defines the incident type, is unrecorded in most of them. The Av/Ac distinction is not an academic refinement: it is the difference between restoring from backup and negotiating for a key, and a record format for incident sharing should be able to carry it. VERIS can (`Obscuration`); the coding practice does not.

**On the errors.** Nothing in this study says that misdelivery and lost laptops do not matter; 2,187 of the 2,615 operational-only records carry a confirmed Data Risk Event. It says that they answer a different question. A control catalogue that treats "Miscellaneous Errors" as a threat pattern beside "System Intrusion" will look for an attacker where there is none and miss the process control that would have prevented the error. Keeping the two on separate axes is what lets each be counted and controlled on its own terms.

## 6. Limitations

The mapping is one reading. Each of the 337 entries carries the rule it applied, so a reviewer can disagree with a row and re-run the study; an inter-rater test on a stratified sample of VERIS values is the obvious next step, as it is for the ATT&CK mapping the cross-check relies on. The cross-check is not an independent validation of the direct mapping: the two routes share the TLCTC rules, and the 75.9% of records with no ATT&CK edge are exactly the records where the direct mapping does most of its work. VCDB is a sample of publicly reported incidents in which healthcare and priority incidents are over-represented by design, older years dominate, and recent years are dominated by one template; every table is stratified so that a reader can discount those effects, but none of the numbers is a population estimate. Records on schema 1.3.x (29) are classified with the 1.4.1 mapping and may contain values the mapping does not know; the classifier reports them as unmapped rather than guessing. Finally, the study reads VERIS values, not the free-text summaries VCDB records also carry; a coder with the summary in front of them could often resolve the `Unknown` and the companion step that the enumerations leave open.

## 7. Reproducibility

Everything below runs with Python 3.10+ and Node 18+ from a clone of the TLCTC repository; no third-party Python package is needed.

```bash
# regenerate the upstream CSV and check the mapping against the dictionary and the pinned VERIS files
npm run build-veris && npm run validate-veris

# classify one VCDB record, a directory, or the joined file
cd mappings/veris
python -m cli classify tests/fixtures/vcdb/0012CC25-9167-40D8-8FE3-3D0DFD8FB6BB.json --format md
python -m cli classify /path/to/vcdb_1-of-1.json --summary --attack-check --format md

# re-run the study: downloads the pinned VCDB zip, verifies its sha256, writes study/results.{json,md} and the figures
python study/run-study.py

# tests
python -m unittest discover tests
```

Pinned inputs: VERIS 1.4.1 enumerations and labels and the VERIS → ATT&CK mapping from vz-risk/veris commit `45d9d7ace489b9b7bc4f1cee1daa4bf4872dfcaf`; VCDB `data/joined/vcdb.json.zip` from vz-risk/VCDB commit `230cf22b56a481dd1a994b21e4d94c59e2bccea9`, SHA-256 `e4be5dd432ccfad16520a6b60dd83e9d47c63b0f3352c26c4d43a5dd774c32c0`; the TLCTC v2.5 dictionary and the ATT&CK → TLCTC mapping at the repository commit that carries this document. `mappings/veris/PINNED.md` lists the hashes.

## References

1. Verizon. *The VERIS Framework (Vocabulary for Event Recording and Incident Sharing).* https://verisframework.org/ (schema documentation and enumerations). Repository: https://github.com/vz-risk/veris
2. Verizon RISK Team. *VERIS Community Database (VCDB).* https://github.com/vz-risk/VCDB (README, sampling warning; `data/joined/NOTE.txt`, web-skimmer exclusion). Licence CC BY-SA 4.0.
3. Verizon. *Data Breach Investigations Report.* https://www.verizon.com/business/resources/reports/dbir/
4. vz-risk/veris, `README.md`, "Note to VERIS users": the 1.4 and 2.0 roadmap. https://github.com/vz-risk/veris#readme
5. G. Bassett. *Add Sequencing to VERIS.* vz-risk/veris issue #127, opened 2016-06-06, open. https://github.com/vz-risk/veris/issues/127
6. B. Kreinz. *A Cause-Oriented Cyber Threat Taxonomy: The TLCTC Framework*, v2.5.1 core paper, 2026. DOI 10.5281/zenodo.20633176. Dictionary: `json-schemas/layer-1/tlctc-framework.v2.5.json`.
7. B. Kreinz. *Evolving VERIS: Replace the Action Axis, Expand the Attribute Axis.* tlctc.net, 2026-04-27. https://www.tlctc.net/tlctc-veris.html
8. MITRE Center for Threat-Informed Defense. *Mappings Explorer: VERIS.* https://center-for-threat-informed-defense.github.io/mappings-explorer/external/veris/ (VERIS 1.4.1 ↔ ATT&CK 19.1); file `mappings/veris-1.4.1_attack-19.1-enterprise.csv` in vz-risk/veris.
9. TLCTC Project. *MITRE ATT&CK Enterprise → TLCTC Mapping* (698 techniques). `mappings/mitre-attack-enterprise/tlctc-enterprise-attack.json`, https://github.com/Barnes70/TLCTC
10. B. Kreinz. *Applying the Top Level Cyber Threat Clusters: Classification, Governance, and Cross-Domain Application*, v2.5.1 application paper, 2026. DOI 10.5281/zenodo.22697636.
