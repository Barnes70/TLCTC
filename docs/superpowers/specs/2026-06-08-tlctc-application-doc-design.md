# TLCTC v2.3 Application & Governance Paper — Design Spec

**Date:** 2026-06-08
**Author:** Bernhard Kreinz
**Branch:** `v2.3-core` (off `main`; local-only — no push/merge/PR/tag until owner approves)
**Status:** Approved design — ready for implementation plan

---

## 1. Background

The v2.3 **core** paper (`documentation/tlctc-v2.3-core.md`) is the frozen, citable taxonomy
(10 strategic clusters, axioms, rules, notation, two-layer model). Throughout the core build,
two kinds of material were deliberately deferred to "a separate application document":
(A) how to *apply* the taxonomy in practice, and (B) governance, controls, and indicators.
This paper delivers both, as one **citable companion paper**.

The empirical validation study (CVE/inter-rater) and the integration doc (SARIF/Sigma/tooling)
remain separate future works and are out of scope here.

## 2. Scope & format

- A single **citable companion paper**, same academic register as the core, version-aligned
  (**v2.3**), with its own machine-readable PDF and an eventual (held) DOI.
- Working title: *Applying the Top Level Cyber Threat Clusters: Classification in Practice,
  Governance, Controls, and Indicators.*
- Two parts:
  - **Part A — Classification in Practice** (audience: SOC/CTI analysts and developers).
  - **Part B — Governance, Controls & Indicators** (audience: CISO/risk management).

### Out of scope
- Empirical validation study (separate paper).
- Integration/tooling doc (SARIF, Sigma — separate).
- Any restatement or redefinition of core taxonomy (clusters/axioms/rules).

## 3. Guiding principle (hard constraint)

**Consolidation + assembly; taxonomy frozen.** Every cluster, axiom, rule, operator, and the
two-layer model is **cited to the core, never restated or redefined**. No new *normative*
taxonomy is introduced. New prose is limited to connective tissue and worked walkthroughs.
Large artifacts (the 698-technique ATT&CK map, the 987 CWE map, the full attack-path corpus)
are **referenced with a few illustrative rows**, not reproduced in bulk. If applying the
framework appears to require a new cluster/axiom/rule, that is a **stop-and-flag** for the owner,
not a quiet addition.

## 4. Sourcing map (where each part is consolidated from)

**Part A**
- Classification procedure — whitepaper §4.2.x (minimal classification procedure).
- Decision tree — `mappings/mitre-attack-enterprise/decision-tree.md` and the published decision tree.
- ATT&CK→TLCTC — `mappings/mitre-attack-enterprise/` (698 techniques).
- CWE→TLCTC — `mappings/mitre-cwe/` (987 weaknesses).
- Worked examples — `attack-paths/` corpus (e.g. `json-schemas/layer-3/examples/solarwinds-2020.json`,
  `attack-paths/chaos-muddywater-falseflag-2026.json`, and others).
- Notation, DRE, SRE→DRE→BRE — cite the core (§3.4, §7).

**Part B**
- Bow-tie control treatment — whitepaper §6 (esp. §6.1 structure, preventive/mitigating).
- NIST CSF event lifecycle & mapping — whitepaper §7, §8.
- Local vs umbrella controls — whitepaper §9.
- Indicators (KRI/KCI/KPI), DCS, velocity-adjusted targets — whitepaper §10.
- Risk appetite, BRE chain → Business Impact — whitepaper §6.3.1 + core §3.4.

## 5. Document structure

Front matter (title/author/version 2.3/date/license) · Abstract · Keywords.

**Part A — Classification in Practice**
1. Introduction (purpose; relation to the core; audience).
2. The classification procedure (step-by-step).
3. The decision tree (cause-first triage; points to the full tree).
4. Recording outcomes in practice (SRE→DRE→BRE; DRE tagging — cites core §3.4).
5. Worked examples (≥3 end-to-end, drawn from the corpus, in attack-path notation).
6. Using the mappings (how to read/use ATT&CK→TLCTC and CWE→TLCTC; a few illustrative rows + pointers to the full maps).

**Part B — Governance, Controls & Indicators**
7. The bow-tie in governance (preventive vs mitigating control placement).
8. NIST CSF mapping (six functions across the event lifecycle).
9. Local vs umbrella controls.
10. Indicators: KRI / KCI / KPI (incl. DCS as a KCI; velocity-adjusted targets).
11. Risk appetite & Business Impact (BRE chain → BI; ties to core consequence model).

**Close**
- Limitations / scope note.
- Concise **application glossary** — only application/governance terms not already in the core
  (e.g. control objective, KCI, KRI, KPI, local/umbrella control, risk appetite); relies on the
  core glossary + `tlctc-glossary.md` for the rest.
- References (reuse the core's reference set as relevant; add any needed, e.g. NIST CSF 2.0 is
  already in the core list). Only cite what the body references (no orphans).

## 6. Naming, build, workflow

- **Source file:** `documentation/tlctc-v2.3-application.md`.
- **Published name (version-agnostic, stable URL):** `tlctc-application.html` / `tlctc-application.pdf`
  (same convention as the core's `tlctc-whitepaper`).
- **PDF:** built with the existing `scripts/build-pdf.js` → `documentation/tlctc-application.pdf`.
- **Branch:** continue on `v2.3-core` (it contains the core to cite and keeps related work
  together). Local commits only; no push/merge/PR/tag until the owner approves. The core commit
  can still be tagged independently for its DOI.

## 7. Acceptance criteria

1. **Taxonomy frozen:** no cluster/axiom/rule/operator is redefined; all are cited to the core.
   (Check: the paper contains no normative cluster/axiom/rule *definitions* of its own.)
2. Both parts present with all sections in §5; ≥3 worked examples reuse the `attack-paths/` corpus.
3. Mappings are referenced with illustrative rows, not reproduced in bulk.
4. DCS appears as a **KCI** in Part B (its full control-effectiveness treatment that was deferred
   from the core).
5. Self-contained: abstract, references, and application glossary present; no leftover placeholders.
6. Builds to a clean machine-readable PDF via `build-pdf.js`.
7. Core files and all other v2.3 artifacts are untouched (this is additive).
