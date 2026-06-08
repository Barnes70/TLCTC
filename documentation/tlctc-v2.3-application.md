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
