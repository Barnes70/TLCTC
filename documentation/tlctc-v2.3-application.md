# Applying the Top Level Cyber Threat Clusters: Classification in Practice, Governance, Controls, and Indicators

**Author:** Bernhard Kreinz
**Version:** 2.3
**Date:** 2026-06-08
**License:** CC BY 4.0
**Companion to:** *A Cause-Oriented Cyber Threat Taxonomy: The TLCTC Framework* (the v2.3 core paper)

## Abstract

This paper is the application companion to the TLCTC v2.3 core paper, which defines and freezes the taxonomy: ten cause-oriented threat clusters, ten axioms, the classification rules, the attack-path notation, and the two-layer (strategic/operational) model. The companion takes that taxonomy as given and shows how to put it to work. Part A addresses security operations and development audiences: it consolidates the classification procedure into an actionable sequence, condenses the cause-first decision tree, explains how to record outcomes as Data Risk Events without disturbing the cause-side classification, walks through end-to-end worked examples drawn from the published attack-path corpus, and shows how to use the MITRE ATT&CK and MITRE CWE reference mappings within the weakness → vulnerability → generic-vulnerability → cluster hierarchy. Part B addresses governance and risk audiences: it places the cause–event–consequence bow-tie in a governance context, maps the clusters and the SRE→DRE→BRE chain to the NIST Cybersecurity Framework, distinguishes local from umbrella controls, and derives velocity-adjusted detection targets together with key risk, control, and performance indicators. No cluster, axiom, rule, operator, or model element is redefined here; all are cited from the core.

**Keywords:** cyber threat classification; attack-path analysis; security operations; threat intelligence; cyber risk governance; NIST CSF; security controls; key risk indicators; detection coverage; TLCTC

# Part A — Classification in Practice

## 1. Introduction

The TLCTC v2.3 core paper completed the framework: it derived the ten clusters from a single thought experiment, fixed the ten axioms and the classification rules, defined the attack-path notation and its boundary operators, and established the two-layer strategic/operational model and the cause–event–consequence bow-tie. With that publication the taxonomy is frozen. The present paper does not extend, revise, or reinterpret it. Its purpose is narrower and complementary: to operationalize a settled taxonomy so that practitioners can apply it consistently to real work.

A taxonomy is only useful if two analysts looking at the same evidence reach the same classification, and if that classification then connects to the decisions an organization actually makes — where to place a control, how to report an incident, which indicator to watch. This paper supplies the connective tissue between the frozen definitions and those decisions. It introduces no new normative content. Every cluster, axiom, rule, operator, and model element used below is used exactly as defined in the core paper (`documentation/tlctc-v2.3-core.md`); where a definition is needed, it is cited rather than restated.

The paper serves two distinct audiences, and is organized accordingly. **Part A (Classification in Practice)** is written for security operations and development teams — the analysts who triage incidents, the responders who reconstruct attack paths, the engineers who translate vulnerability findings into risk. It consolidates the classification procedure, condenses the cause-first decision tree, explains how to record outcomes faithfully, demonstrates the method on published incidents, and shows how to read the two large reference mappings (MITRE ATT&CK and MITRE CWE). **Part B (Governance, Controls, and Indicators)** is written for governance, risk, and management audiences. It places the bow-tie in a governance frame, maps the framework to the NIST Cybersecurity Framework, distinguishes local from umbrella controls, and derives velocity-adjusted detection targets and the corresponding key risk, control, and performance indicators.

**How to read this paper.** Practitioners who need to classify an incident can read Part A start to finish and keep §2 (the procedure) and §3 (the decision tree) as desk references; §5 supplies models to copy. Governance readers can begin with Part B, treating §4 (outcome recording) as the bridge that explains why cause-side classification and consequence-side reporting stay separate. Either way, the core paper remains the normative authority: when this paper says "#4 Identity Theft" or "R-CRED" or "Trust Acceptance Event," the binding definition lives in the core, and any apparent conflict should be resolved in favor of the core.

## 2. The Classification Procedure

Classification operates on **attack steps**, not on incidents as a whole. An incident is decomposed into a sequence of steps, and each step is classified independently into exactly one cluster (Axiom VI). The procedure below consolidates the seven-step minimal procedure from the whitepaper (§4.2.8) into an actionable checklist. The classification rules referenced by ID (R-EXEC, R-ROLE, R-CRED, R-FLOOD, R-MITM, R-SUPPLY) are defined in full in the core paper §6; only a one-line reminder is given here.

**Step 1 — Identify the attacker action and target.** State plainly what the attacker did in this step, which asset or component was targeted, and what the step was trying to achieve. A step without a concrete protected asset cannot be classified; abstract descriptions ("they moved laterally") must be resolved to a specific action against a specific target before proceeding.

**Step 2 — Identify the initial generic vulnerability.** Ask the cause question: *what root weakness did the attacker exploit to make this step succeed?* The answer must map to exactly one of the ten generic vulnerabilities underlying the ten clusters — designed functional scope (#1), server-side code flaw (#2), client-side code flaw (#3), identity-artifact/credential application (#4), lack of end-to-end communication protection (#5), finite-capacity exhaustion (#6), designed execution capability for untrusted content (#7), physical accessibility (#8), human psychological factors (#9), or third-party trust dependency (#10). Classify by the cause that made *this* step work, not by the outcome it produced.

**Step 3 — Apply the R-\* rules.** Check each rule for applicability and let it disambiguate:
- **R-ROLE** — implementation flaw? Server-role component = #2, client-role component = #3.
- **R-CRED** — credentials involved? Acquisition maps to the enabling cluster; application (authenticating) is always #4. Separate steps.
- **R-MITM** — communication-path position? Gaining position maps to the enabling cluster; interception/modification/relay is #5.
- **R-FLOOD** — availability impact by volume/intensity exhausting finite capacity = #6; by an implementation defect (crash/hang) = #2 or #3 per R-ROLE.
- **R-EXEC** — does Foreign Executable Content execute here? If yes, a #7 step **must** be recorded at the execution moment (in addition to the enabling cluster).
- **R-SUPPLY** — third-party trust link? Place #10 at the Trust Acceptance Event — the moment the trust artifact becomes authoritative inside the target domain.

**Step 4 — Apply tie-breakers if needed.** If more than one cluster still seems plausible, select the cluster matching the **initial** generic vulnerability — the weakness that made the step possible, not a downstream effect. If genuine ambiguity remains, assign the best-supported cluster and record the rationale; use the epistemic-state annotations (`#X [conf=low]`, `?`) from core §6/§7 only when no cluster can be defended.

**Step 5 — Record outcomes separately as DRE.** If the step produced data impact, record it as a Data Risk Event tag appended to the step (`#X + [DRE: C]`, etc.). Outcomes never change the cluster; they are recorded alongside it. The mechanics are detailed in §4.

**Step 6 — Split multi-cause steps.** If what looked like one step actually contains two distinct attacker actions exploiting two different generic vulnerabilities, split it. Each resulting step maps to exactly one cluster, expressed as a path (`#X → #Y`). The canonical case is credential acquisition followed by credential use: two steps, two clusters, never one.

**Step 7 — Document.** Record the cluster assignment (in strategic and/or operational notation), a brief rationale where the classification was non-obvious, any DRE tags, the step's position in the path, and velocity annotations (Δt) where temporal evidence exists. Documentation is what makes a classification auditable and reproducible by a second analyst.

The procedure is deliberately cause-first and step-local: never classify the incident, always classify the step; never classify the outcome, always classify the weakness that the step exploited.

## 3. The Decision Tree

The procedure in §2 establishes *what to ask*; the decision tree provides a fast, ordered triage for *answering it*. The two are complementary — the tree is a cause-first shortcut for Steps 2 and 3, not a replacement for the full procedure. It is condensed here; the complete tree, with per-tactic guidance and worked corrections, lives in `mappings/mitre-attack-enterprise/decision-tree.md`.

**Two prerequisites** must be settled before walking the tree:

1. **Domain.** Where does this step execute relative to the organization? `@Org` → classify. `@AttackerInfra` or `@OtherVictims` (attacker-side preparation, compromise of someone else) → **N/A**: it is threat potential, not a threat to this organization. `@3P` (a third party) → consider **#10** only if a trust boundary is crossed into the environment.
2. **Protected asset.** Name a concrete asset in scope that the step affects. TLCTC requires a concrete target; an abstract technique description without a target asset cannot be classified.

**The ordered questions.** Walk Q1→Q10 in order and **stop at the first match.** The ordering is deliberate: designed-function abuse is tested before code flaws, and identity application before lower-level mechanics, so that the most common and most generic causes are caught first.

```
Q1  Abusing a DESIGNED function/feature/API/config, no code flaw, no foreign
    binary required?                                  → #1 Abuse of Functions
Q2  Exploiting a CODE IMPLEMENTATION FLAW, SERVER-role component?
                                                      → #2 Exploiting Server
Q3  Exploiting a CODE IMPLEMENTATION FLAW, CLIENT-role component?
                                                      → #3 Exploiting Client
Q4  Acting as a LEGITIMATE IDENTITY by presenting credentials/tokens/keys
    (credential APPLICATION, not acquisition)?        → #4 Identity Theft
Q5  Intercepting/modifying/relaying communication from a privileged position
    on the path?                                      → #5 Man in the Middle
Q6  Overwhelming finite resources by volume or intensity? (a code bug that
    crashes is #2/#3, not #6)                         → #6 Flooding Attack
Q7  Is FOREIGN CODE executing? (if launched via a legitimate tool, #1 → #7)
                                                      → #7 Malware
Q8  Requires physical interaction with hardware/facilities?
                                                      → #8 Physical Attack
Q9  Psychologically manipulating a human?             → #9 Social Engineering
Q10 Exploiting trust in a third-party component/service/update (placed at the
    Trust Acceptance Event)?                          → #10 Supply Chain Attack
    └─ no match → re-examine; one of the above must apply.
```

Two ordering consequences are worth noting. First, because Q1 precedes Q7, the LOLBAS pattern naturally resolves to two steps: the legitimate tool invoked through its designed interface stops at Q1 (#1), and the attacker-supplied content that subsequently runs is a second step at Q7 (#7) — the `#1 → #7` shape required by R-EXEC. Second, because Q4 (credential *application*) sits above the lower mechanics, credential *acquisition* is not classified here at all; it is classified by *how* it was acquired (a separate, earlier step) and only its use lands at Q4. When a single observation seems to match two questions, that is the signal to split it into separate steps (Step 6 of §2), each re-entering the tree on its own.

## 4. Recording Outcomes in Practice

The cause–event–consequence model (core §3.4) places the ten clusters on the cause side and outcomes on the consequence side, joined by one pivot — the **System Risk Event (SRE)**, the loss of control / system compromise. Consequences then follow a variable-length chain: **SRE → DRE → BRE\***. This section is about the *practice* of recording the consequence side alongside a classified step — when and how to tag — not about redefining the model, for which the core is authoritative.

**The hard boundary.** Outcomes are never clusters. A "data breach," a "ransomware impact," an "outage" record *what happened*; none of them is a generic vulnerability and none changes the cluster of the step that caused it. This is the operational form of Axiom III. In practice it means the analyst classifies the step first (§2), and only then asks whether that step also produced a data-level effect worth recording.

**Tagging Data Risk Events.** A DRE is recorded as a tag appended to a classified step: `#X + [DRE: C]`, `#X + [DRE: I]`, `#X + [DRE: A]`. The letters are the impacted property — Confidentiality, Integrity, Availability/Accessibility (general). When the availability distinction matters operationally, use the two refinements from core §7.6: `Av` for *Availability* (data gone or unreachable — wiped, deleted) and `Ac` for *Accessibility* (data present but unusable — encrypted, locked behind a disabled account). The distinction is load-bearing for response: `Ac` (ransomware) leaves recovery options that `Av` (wiper) destroys. Tags may be combined (`+ [DRE: C, I]`). A DRE is recorded at the step where the impact *first occurs* — confidentiality is breached at the read/collection step, not re-cited at every later staging or exfiltration step that handles the same data.

**The SRE pivot, in practice.** The SRE marks the moment the attacker holds control sufficient to pursue objectives. It is not a tag on a step; it is a position in the path. Recording it matters because it opens the detection window: compromise can exist for weeks before any DRE, so naming the SRE tells responders where "we are compromised" began even when no data has yet moved. In some paths the DRE coincides with the SRE (a SQL injection that reads data the instant it succeeds); in others the SRE precedes the first DRE by days. Both are accommodated — the SRE is the pivot regardless of whether consequences are simultaneous or delayed.

**BRE chaining for reporting.** Beyond the DRE, business-level effects are recorded as Business Risk Events (`SRE → DRE → BRE₁ → … → BREₙ`): a regulatory notification, a declared outage, an imposed fine. These chain for reporting and governance (Part B), and the chain can break at any point — not every SRE yields a DRE, and not every DRE yields a BRE. In Layer-3 attack-path notation, BREs are generally narrated in prose rather than appended to steps; the notation carries the cause-side path and the DRE tags, and the business chain is reconstructed from them.

Two practitioner cautions follow directly from the boundary. First, never append a DRE to an unresolved step (`?`/`…`): without a classified cluster there is no causal basis for asserting the data effect in notation (core R-UNRES-5); record it in prose if independently confirmed. Second, never let the *name* of an outcome drive classification — a report that says "ransomware" still classifies the encryption execution as #7 and tags `[DRE: Ac]`; the brand is not the cause.

## 5. Worked Examples

The following three examples apply the procedure (§2), the decision tree (§3), and the outcome-recording rules (§4) end to end. Each is drawn verbatim from the published attack-path corpus; the source JSON is cited so the full step-by-step analysis can be consulted.

### 5.1 SolarWinds / SUNBURST (2020)

*Scenario.* A trojanized SolarWinds Orion update, digitally signed by the vendor, was distributed through the legitimate update channel; once installed it gave the actor a foothold from which forged SAML tokens unlocked cloud resources. Source: `json-schemas/layer-3/examples/solarwinds-2020.json`.

*Path.*
```
#10 ||[update][@Vendor→@Org]|| →[Δt=instant] #7 →[Δt=~14d] #4 →[Δt=~2h] #1 + [DRE: C]
```

*Reasoning.* The first step is **#10 at the Trust Acceptance Event** (R-SUPPLY): the cluster is placed not at the upstream vendor compromise but at the moment the signed update is accepted and becomes authoritative inside `@Org` — the falsifiability test holds, since declining the update would have prevented the step. The signed backdoor DLL then executing in the Orion service is a separate **#7** step (R-EXEC fires; `fec_executed: true`), recorded at the execution moment even though delivery used a designed loading mechanism. Roughly two weeks later, forged SAML tokens are *presented* to authenticate — credential **application**, always **#4** regardless of how the signing key was obtained (Axiom X / R-CRED). The final step is **#1**: using the now-valid identity to abuse Azure AD and Office 365 APIs as designed, with `[DRE: C]` recording the confidentiality breach. No code flaw appears anywhere in the path — the whole intrusion runs on trust and designed functionality.

### 5.2 Chaos / MuddyWater False-Flag (2026)

*Scenario.* An Iranian state actor used a Microsoft Teams chat impersonating IT support to harvest credentials and hijack MFA enrollment, then deployed RMM tools and an operator-gated RAT, exfiltrating data under a "Chaos ransomware" brand that performed no encryption. Source: `attack-paths/chaos-muddywater-falseflag-2026.json`.

*Path.*
```
#9 ||[human][@Attacker⇒@MSTeams→@Org]|| →[Δt=?] #4 →[Δt=?] #1 →[Δt=?] #4
   →[Δt=?] #1 →[Δt=~5s] #7 →[Δt=?] #7 + [DRE: C]
```

*Reasoning.* The opening step is **#9**, with Microsoft Teams marked as **transit** (`⇒@MSTeams`) per R-TRANSIT-3: Teams relays the deceptive content but is not itself exploited, so it is a carrier, not the attack surface. Credential acquisition happens *inside* the #9 step (the enabling cluster); the subsequent presentation of those credentials to the VPN/SSO is the separate **#4** step (R-CRED / Axiom X). The MFA self-enrollment hijack is **#1**, not #4: a flawlessly implemented self-service enrollment endpoint still permits it, so the cause is designed functional scope, and folding it into the surrounding #4 chain would erase the single highest-leverage detection point. A fresh **#4** records re-authentication now that the attacker controls the second factor. LOLBAS invocation of `curl`/installers is **#1**; the RMM and RAT binaries then executing are **#7** (R-EXEC, including dual-use tools running attacker-controlled content). Critically, the path closes on **`[DRE: C]` only** — the "ransomware" brand is extortion pressure, not a data event; tagging `[DRE: Ac]` because the report says "ransomware" would violate Axiom III.

### 5.3 Active Directory Domain-Admin → Ransomware Cascade (2025)

*Scenario.* A composite reference pattern grounded in three 2025 human-operated intrusions (Lynx, Storm-2603, Storm-0300/Akira): valid credentials reach Domain Admin, the attacker harvests the directory and destroys recovery tiers, then encrypts. Source: `attack-paths/ad-domain-admin-cascade-2025.json`.

*Path (abridged tail).*
```
… → #4 ||[prod][@Attacker→@Org]|| → #1 → #4 → #1 … → #1 + [DRE: C] (DCSync)
   → #4 (PtH/Golden Ticket) → … → #7 + [DRE: C] (exfil) → … → #7 + [DRE: Ac] (encrypt)
```

*Reasoning.* The acquisition prefix is modeled as an **unresolved gap** (`…`, R-UNRES-8) so the one file serves all five documented variants; defenders replace it with their own classified prefix. The RDP foothold with valid credentials is **#4** (clean authentication, no brute-force noise — R-CRED). The post-foothold tail is structurally **#1 Abuse of Functions**: enumeration, account creation, group elevation, and DCSync all invoke designed Active Directory capabilities at the authority the attacker holds. DCSync is the key teaching case — it is **#1 + [DRE: C]** (designed replication function abused, confidentiality breach on credential material), and its paired use (pass-the-hash or Golden Ticket presentation) is the separate **#4** with *no* DRE, because per R-CRED the DRE attaches at acquisition, never at re-use. Two `[DRE: C]` subjects appear and stay distinct: credential material (DCSync) and business file data (exfiltration). Recovery destruction (`vssadmin delete shadows`, backup-console deletion) stays **#1 + [DRE: Av]** — admin tools, data *gone*. Finally the ransomware payload running on each host is **#7 + [DRE: Ac]** — data present but encrypted; "ransomware" is the outcome label, the cluster is FEC execution.

## 6. Using the Mappings

<filled by Task 7>

# Part B — Governance, Controls, and Indicators

## 7. The Bow-Tie in Governance

<filled by Task 8>

## 8. Mapping to the NIST Cybersecurity Framework

<filled by Task 9>

## 9. Local and Umbrella Controls

<filled by Task 10>

## 10. Indicators: KRI, KCI, KPI

<filled by Task 11>

## 11. Risk Appetite and Business Impact

<filled by Task 12>

## 12. Limitations and Scope

<filled by Task 13>

## 13. Glossary (Application Terms)

<filled by Task 13>

## 14. References

<filled by Task 13>
