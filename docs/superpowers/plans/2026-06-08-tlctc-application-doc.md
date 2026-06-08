# TLCTC v2.3 Application & Governance Paper — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce `documentation/tlctc-v2.3-application.md` — a citable companion paper to the v2.3 core, in two parts (Classification in Practice; Governance, Controls & Indicators), by consolidating existing material with the taxonomy frozen.

**Architecture:** One self-contained paper built section-by-section. Part A draws on the §4.2.8 classification procedure, the decision tree, the ATT&CK/CWE mappings, and the `attack-paths/` corpus. Part B consolidates whitepaper §6–§10 (bow-tie controls, NIST CSF, local/umbrella, KRI/KCI/KPI, DCS). The taxonomy is never redefined — clusters/axioms/rules/notation are cited to the core. Rendered to PDF via the existing `scripts/build-pdf.js`.

**Tech Stack:** Markdown; `marked` + `puppeteer` for the PDF (`npm install marked puppeteer`; package.json is gitignored).

**Spec:** `docs/superpowers/specs/2026-06-08-tlctc-application-doc-design.md`
**Branch:** `v2.3-core` (off `main`). **No push / merge / PR / tag until owner approves.** Local commits only.

---

## Note on format (read first)

This is a **content-consolidation** plan, not a code feature. Paper-section tasks cannot inline thousands of words of final prose; each instead gives the **exact source** to consolidate from, **what to keep/cut**, a **length target**, and a concrete **verification check** (`grep`/`rg` for required headers/terms, or a PDF build). The "test" for a content section is a structural assertion, run and confirmed before commit.

**Hard constraint everywhere — taxonomy frozen.** Never restate or redefine a cluster, axiom, rule, operator, or the two-layer model; **cite the core** (`tlctc-v2.3-core.md`) instead. No new normative taxonomy. If applying the framework seems to need a new cluster/axiom/rule, **STOP and ask the owner**. Marketing language is banned; academic tone throughout.

**Source files** (read as needed):
- Core paper: `documentation/tlctc-v2.3-core.md` (cite it).
- Whitepaper (finalized v2.1 content): `documentation/tlctc-v2.0-whitepaper.md` — §4.2.8 classification procedure (~L1493–1570); §6 bow-tie (~L2018–2240); §7 functions→control objectives / NIST CSF lifecycle (~L2243–2350); §8 control-framework mapping (~L2351–2478); §9 local vs umbrella (~L2479–2495); §10 indicators (~L2496–2832: §10.2 KRI ~L2555, §10.3 KCI ~L2612, §10.4 velocity context ~L2658, §10.5 DCS ~L2681, §10.6 velocity-adjusted targets ~L2701, §10.7 hierarchy ~L2712).
- Decision tree: `mappings/mitre-attack-enterprise/decision-tree.md`.
- Mappings: `mappings/mitre-attack-enterprise/tlctc-enterprise-attack.json` (698), `mappings/mitre-cwe/tlctc-cwe.json` + `mappings/mitre-cwe/README.md` (987).
- Attack-path corpus: `json-schemas/layer-3/examples/solarwinds-2020.json`, `json-schemas/layer-3/examples/midnight-blizzard-microsoft-2024.json`, `attack-paths/chaos-muddywater-falseflag-2026.json`, `attack-paths/ad-domain-admin-cascade-2025.json`, `attack-paths/fancy-bear-lamehug-2025.json`.

---

## Task 1: Skeleton, front matter, abstract

**Files:** Create `documentation/tlctc-v2.3-application.md`

- [ ] **Step 1: Write the file with front matter, abstract, keywords, and section skeleton**

Front matter + abstract are NEW prose. Abstract ≤ ~200 words: this paper is the application companion to the TLCTC v2.3 core; it shows how to classify incidents reproducibly (Part A) and how to place controls, map to NIST CSF, and select indicators including velocity-adjusted detection targets (Part B); the taxonomy is taken as given from the core; audiences are operations/development and governance/risk.

```markdown
# Applying the Top Level Cyber Threat Clusters: Classification in Practice, Governance, Controls, and Indicators

**Author:** Bernhard Kreinz
**Version:** 2.3
**Date:** 2026-06-08
**License:** CC BY 4.0
**Companion to:** *A Cause-Oriented Cyber Threat Taxonomy: The TLCTC Framework* (the v2.3 core paper)

## Abstract

<~200-word abstract per the direction above>

**Keywords:** cyber threat classification; attack-path analysis; security operations; threat intelligence; cyber risk governance; NIST CSF; security controls; key risk indicators; detection coverage; TLCTC

# Part A — Classification in Practice

## 1. Introduction

<filled by Task 2>

## 2. The Classification Procedure

<filled by Task 3>

## 3. The Decision Tree

<filled by Task 4>

## 4. Recording Outcomes in Practice

<filled by Task 5>

## 5. Worked Examples

<filled by Task 6>

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
```

- [ ] **Step 2: Verify the structure**

Run: `rg -n '^# Part|^## ' documentation/tlctc-v2.3-application.md`
Expected: two `# Part` headers and sections 1–14 plus Abstract.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "feat(app): application paper skeleton, front matter, abstract"
```

---

## Task 2: §1 Introduction

**Source:** core paper §1 (problem/three audiences), spec §1–2.

- [ ] **Step 1: Replace `<filled by Task 2>` under "## 1. Introduction"**

~300–450 words: state that the core froze the taxonomy and this paper operationalizes it; name the two audiences (operations/development for Part A, governance/risk for Part B); state explicitly that no cluster/axiom/rule is redefined here — all are used as defined in the core (cite it). One short paragraph on how to read the paper (Part A then Part B).

- [ ] **Step 2: Verify**

Run: `rg -n 'filled by Task 2|core' documentation/tlctc-v2.3-application.md`
Expected: placeholder gone; the core is referenced.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "docs(app): fill introduction"
```

---

## Task 3: §2 The Classification Procedure

**Source:** whitepaper §4.2.8 Minimal Classification Procedure (~L1493–1570), 7 steps.

- [ ] **Step 1: Replace `<filled by Task 3>` under "## 2. The Classification Procedure"**

Consolidate the seven steps faithfully: (1) identify attacker action + target; (2) identify the *initial* generic vulnerability (map to one of the 10); (3) apply the R-* rules; (4) tie-breakers; (5) record outcomes separately as DRE; (6) split multi-cause steps; (7) document the classification. Present as an ordered, numbered procedure. Reference the rules by ID (cite the core's §6 for their definitions; do not restate full rule text — a one-line reminder per rule is fine). Keep it actionable (a SOC analyst should be able to follow it).

- [ ] **Step 2: Verify**

Run: `rg -n 'Step 1|Step 7|generic vulnerability|R-ROLE|R-CRED|R-EXEC' documentation/tlctc-v2.3-application.md`
Expected: the seven-step structure and rule references present.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "docs(app): fill the classification procedure"
```

---

## Task 4: §3 The Decision Tree

**Source:** `mappings/mitre-attack-enterprise/decision-tree.md` (prerequisites + the cause-first Q1…Q-n walk).

- [ ] **Step 1: Replace `<filled by Task 4>` under "## 3. The Decision Tree"**

Present a condensed cause-first triage: the two prerequisites (domain `@Org` vs `@3P`/`@AttackerInfra`; a concrete protected asset), then the ordered questions Q1→Q10 that stop at the first match (Q1 #1 designed-function abuse; Q2 #2 server flaw; Q3 #3 client flaw; Q4 #4 identity application; … through #10). Render the question ladder compactly (a list or fenced block). Note it complements the procedure (§2) and point to the full decision tree file for the complete version. Do not reproduce the entire file.

- [ ] **Step 2: Verify**

Run: `rg -n 'Q1|Q2|first match|decision-tree' documentation/tlctc-v2.3-application.md`
Expected: the ordered-questions structure and a pointer to the full tree.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "docs(app): fill the decision tree"
```

---

## Task 5: §4 Recording Outcomes in Practice

**Source:** core §3.4 (SRE→DRE→BRE), core §7.6 (DRE tags), whitepaper §6.2 (hard boundary).

- [ ] **Step 1: Replace `<filled by Task 5>` under "## 4. Recording Outcomes in Practice"**

~300–450 words: how to record outcomes alongside classified steps without changing classification — DRE tags `+ [DRE: C/I/A]` (Av/Ac refinement), the SRE pivot, and BRE chaining for incident reporting. Emphasize the hard boundary (outcomes are never clusters). Cite the core for the model; this section is the *practice* (when/how to tag during analysis), not a re-derivation.

- [ ] **Step 2: Verify**

Run: `rg -n 'DRE|SRE|BRE|Av|Ac' documentation/tlctc-v2.3-application.md`
Expected: outcome-recording terms present.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "docs(app): fill recording outcomes in practice"
```

---

## Task 6: §5 Worked Examples

**Source:** the `attack-paths/` corpus — use at least three: `json-schemas/layer-3/examples/solarwinds-2020.json`, `attack-paths/chaos-muddywater-falseflag-2026.json`, and one more (e.g. `attack-paths/ad-domain-admin-cascade-2025.json` or `json-schemas/layer-3/examples/midnight-blizzard-microsoft-2024.json`).

- [ ] **Step 1: Read the chosen corpus files, then replace `<filled by Task 6>` under "## 5. Worked Examples"**

For each of ≥3 incidents: a 1–2 sentence scenario summary, the attack path in core notation (steps, Δt, boundary operators, DRE), and 2–4 sentences of classification reasoning showing the procedure/decision-tree applied (e.g. why a step is #10 at the TAE, why credential use is #4). Cite the source JSON path for each. Do not invent incidents; use the corpus.

- [ ] **Step 2: Verify**

Run: `rg -n 'SolarWinds|→|\[DRE|attack-paths/|examples/' documentation/tlctc-v2.3-application.md`
Expected: ≥3 examples with notation and source citations.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "docs(app): fill worked examples from the corpus"
```

---

## Task 7: §6 Using the Mappings

**Source:** `mappings/mitre-attack-enterprise/` (decision-tree + `tlctc-enterprise-attack.json`, 698 techniques) and `mappings/mitre-cwe/` (`tlctc-cwe.json` + README, 987 weaknesses).

- [ ] **Step 1: Replace `<filled by Task 7>` under "## 6. Using the Mappings"**

Explain how to *use* the two reference mappings: ATT&CK technique → TLCTC cluster (operational technique to cause), and CWE weakness → TLCTC cluster (code weakness to cause), within the conceptual hierarchy Weakness (CWE) → Vulnerability (CVE) → Generic Vulnerability (TLCTC) → Cluster. Show ~3 illustrative rows per mapping (e.g. an ATT&CK technique and a CWE such as CWE-89 SQLi → #2) and then **point to the full mapping files** by path for the complete 698/987 sets. Note the CWE mapping is AI-generated/experimental (per its README). Do not paste the full tables.

- [ ] **Step 2: Verify**

Run: `rg -n 'ATT&CK|CWE|tlctc-enterprise-attack|tlctc-cwe|CWE-' documentation/tlctc-v2.3-application.md`
Expected: both mappings explained with illustrative rows and file pointers.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "docs(app): fill using the mappings (ATT&CK, CWE)"
```

---

## Task 8: §7 The Bow-Tie in Governance

**Source:** whitepaper §6.1 (structure/vocabulary), §6.2 (hard boundary), §6.5 (what the bow-tie gains).

- [ ] **Step 1: Replace `<filled by Task 8>` under "## 7. The Bow-Tie in Governance"**

~350–550 words: the five bow-tie elements (threats=clusters on the cause side; preventive controls; central event = SRE; mitigating controls; consequences = DRE/BRE), and how controls are *placed* by position — preventive controls reduce likelihood of cluster steps (IDENTIFY/PROTECT), mitigating controls act after the SRE (DETECT/RESPOND/RECOVER). Reference the core §3.4 consequence model rather than re-deriving it. Keep control taxonomy here (this is the governance application).

- [ ] **Step 2: Verify**

Run: `rg -n 'bow-tie|preventive|mitigating|central event|SRE' documentation/tlctc-v2.3-application.md`
Expected: bow-tie governance vocabulary present.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "docs(app): fill the bow-tie in governance"
```

---

## Task 9: §8 Mapping to the NIST Cybersecurity Framework

**Source:** whitepaper §7 (event-lifecycle anchor) and §8 (§8.1 NIST CSF integration).

- [ ] **Step 1: Replace `<filled by Task 9>` under "## 8. Mapping to the NIST Cybersecurity Framework"**

~350–550 words: place the six CSF 2.0 functions (GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER) against the event lifecycle (before/at/after the SRE), and show how each TLCTC cluster's controls distribute across the functions. Cite NIST CSF 2.0 (reference). A compact table (cluster × CSF function, or lifecycle phase × function) is appropriate. Do not redefine clusters.

- [ ] **Step 2: Verify**

Run: `rg -n 'GOVERN|IDENTIFY|PROTECT|DETECT|RESPOND|RECOVER|CSF' documentation/tlctc-v2.3-application.md`
Expected: the six functions and CSF mapping present.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "docs(app): fill NIST CSF mapping"
```

---

## Task 10: §9 Local and Umbrella Controls

**Source:** whitepaper §9 (Local vs Umbrella Controls).

- [ ] **Step 1: Replace `<filled by Task 10>` under "## 9. Local and Umbrella Controls"**

~200–350 words: local controls (protect a specific system) vs umbrella controls (protect groups of systems), with how each maps to clusters and the defense-in-depth interplay across clusters (e.g. #9 can circumvent #4 controls). Concrete examples.

- [ ] **Step 2: Verify**

Run: `rg -n -i 'local control|umbrella control|defense-in-depth' documentation/tlctc-v2.3-application.md`
Expected: both control types present.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "docs(app): fill local and umbrella controls"
```

---

## Task 11: §10 Indicators: KRI, KCI, KPI

**Source:** whitepaper §10 — §10.1 architecture, §10.2 KRI (~L2555), §10.3 KCI (~L2612), §10.4 velocity context (~L2658), §10.5 DCS (~L2681), §10.6 velocity-adjusted targets (~L2701).

- [ ] **Step 1: Replace `<filled by Task 11>` under "## 10. Indicators: KRI, KCI, KPI"**

~500–800 words: the KxI hierarchy (KRI = risk exposure per cluster; KCI = control effectiveness; KPI = performance), then the velocity context — same MTTD can be effective or ineffective depending on attack velocity Δt. Present **DCS as a KCI**: `DCS = MTTD / Δt` (< 1.0 effective, > 1.0 the attacker wins the transition) — this is the full control-effectiveness treatment deferred from the core. Include the velocity-adjusted DCS-target table (per velocity class → required MTTD). Cite the core §7.2 for the velocity/DCS foundation; here it is operationalized as a control indicator.

- [ ] **Step 2: Verify**

Run: `rg -n 'KRI|KCI|KPI|DCS|MTTD|velocity-adjusted|Δt' documentation/tlctc-v2.3-application.md`
Expected: the indicator hierarchy, DCS-as-KCI, and velocity-adjusted targets present.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "docs(app): fill indicators (KRI/KCI/KPI, DCS as KCI)"
```

---

## Task 12: §11 Risk Appetite and Business Impact

**Source:** whitepaper §6.3.1 (BRE chain, Business Impact role) and core §3.4.

- [ ] **Step 1: Replace `<filled by Task 12>` under "## 11. Risk Appetite and Business Impact"**

~250–400 words: how risk appetite sets DCS/KRI thresholds and determines the terminal Business Impact (BI) in a BRE chain (BI is a role, not a separate event type). Tie governance targets back to the consequence chain. Cite the core for SRE→DRE→BRE.

- [ ] **Step 2: Verify**

Run: `rg -n -i 'risk appetite|Business Impact|BRE|threshold' documentation/tlctc-v2.3-application.md`
Expected: risk-appetite → BI linkage present.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "docs(app): fill risk appetite and business impact"
```

---

## Task 13: §12 Limitations, §13 Application Glossary, §14 References

**Source:** spec §7; core glossary + `tlctc-glossary.md`; core references.

- [ ] **Step 1: Replace `<filled by Task 13>` placeholders for §12, §13, §14**

- **§12 Limitations and Scope:** this paper applies but does not validate the framework (validation is separate); control mappings are guidance, not prescriptions; the ATT&CK/CWE mappings are reference aids (CWE experimental); the taxonomy itself is defined and bounded by the core.
- **§13 Glossary (Application Terms):** concise, only application/governance terms not already core — control objective; preventive control; mitigating control; local control; umbrella control; KRI; KCI; KPI; MTTD; risk appetite. One line each (from `tlctc-glossary.md`). Add a pointer: for taxonomy terms see the core paper and `tlctc-glossary.md`.
- **§14 References:** only works actually cited in this paper — at minimum the **core paper**, NIST CSF 2.0 (CSWP 29, DOI 10.6028/NIST.CSWP.29), NIST SP 800-30r1, MITRE ATT&CK, MITRE CWE; add others only if cited. No orphan references.

- [ ] **Step 2: Verify**

Run: `rg -n 'filled by Task|^## 12|^## 13|^## 14|control objective|NIST CSF' documentation/tlctc-v2.3-application.md`
Expected: no leftover placeholders; the three closing sections present with content.

- [ ] **Step 3: Commit**

```bash
git add documentation/tlctc-v2.3-application.md
git commit -m "docs(app): fill limitations, application glossary, references"
```

---

## Task 14: Final verification + PDF

- [ ] **Step 1: No placeholders / taxonomy-frozen check**

Run: `rg -n 'filled by Task|<~|TBD|TODO' documentation/tlctc-v2.3-application.md`
Expected: no matches.
Run: `rg -n 'generic_vulnerability|"definition"|Axiom [IVX]+ —' documentation/tlctc-v2.3-application.md`
Expected: no cluster/axiom *definitions* re-stated (clusters/axioms are referenced, not redefined). Spot-check that cluster references read like citations to the core, not new definitions.

- [ ] **Step 2: Structure check**

Run: `rg -n '^# Part|^## ' documentation/tlctc-v2.3-application.md`
Expected: Part A + Part B; sections 1–14; Abstract.

- [ ] **Step 3: Build the PDF**

Run: `node scripts/build-pdf.js documentation/tlctc-v2.3-application.md documentation/tlctc-application.pdf`
Expected: `PDF written: …/tlctc-application.pdf (… KB)` (under 5 MB).

- [ ] **Step 4: Confirm core + other v2.3 artifacts untouched**

Run: `git status --porcelain documentation/tlctc-v2.3-core.md json-schemas/layer-1/tlctc-framework.v2.3.json`
Expected: no output (unmodified).

- [ ] **Step 5: Commit**

```bash
git add documentation/tlctc-v2.3-application.md documentation/tlctc-application.pdf
git commit -m "docs(app): final verification + application PDF"
```

---

## Done criteria (maps to spec §7)

1. Taxonomy frozen — no cluster/axiom/rule redefined; all cited to the core. (Tasks 2–14)
2. Both parts present with all sections; ≥3 worked examples reuse the corpus. (Tasks 1, 6)
3. Mappings referenced with illustrative rows, not bulk-reproduced. (Task 7)
4. DCS appears as a KCI in Part B. (Task 11)
5. Self-contained: abstract, references, application glossary; no placeholders. (Tasks 1, 13, 14)
6. Builds to a clean PDF via `build-pdf.js`. (Task 14)
7. Core and other v2.3 artifacts untouched. (Task 14)

**Reminder:** all work stays local on `v2.3-core`. Do NOT push, merge, open a PR, or push any tag until the owner explicitly approves.
