---
type: "control-objective-set"
title: "Controls → #10 Supply Chain Attack"
description: "NIST CSF control objectives and ISO 27001:2022 Annex A starter controls for TLCTC #10 Supply Chain Attack."
resource: "tlctc:controls:cluster-10"
tags:
  - "controls"
  - "nist-csf"
  - "iso27001"
  - "cluster-10"
cluster: "#10"
---
# Controls → #10 Supply Chain Attack

> **Provenance:** the ISO 27001:2022 Annex A control placements below are *starter guidance* derived from the TLCTC Control Matrix tool (`tools/`), AI-assisted and not a certified control set. The normative cause-side taxonomy is the cluster definitions; control selection is organization-specific. See `/controls/index.md`.

Cause: [#10 Supply Chain Attack](/clusters/cluster-10.md). Functions: [GOVERN](/controls/functions/govern.md) · [IDENTIFY](/controls/functions/identify.md) · [PROTECT](/controls/functions/protect.md) · [DETECT](/controls/functions/detect.md) · [RESPOND](/controls/functions/respond.md) · [RECOVER](/controls/functions/recover.md). Effectiveness: [/controls/effectiveness-model.md](/controls/effectiveness-model.md).

## GOVERN

*cross-cutting.* **Objective:** Establish ownership, policy, and risk-appetite for #10 Supply Chain Attack.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.21 — Managing information security in the ICT supply chain — Define requirements for ICT supply chain integrity (signing, verification)
- A.5.37 — Documented operating procedures — Document vendor onboarding, assessment, and monitoring procedures
- A.5.32 — Intellectual property rights — Ensure supply chain agreements address intellectual property rights and code ownership
- A.8.32 — Change management — Manage changes to supply chain components with mandatory security review

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.1 — Policies for information security — Define supply chain security policies including vendor requirements and trust boundaries
- A.5.19 — Information security in supplier relationships — Establish information security requirements for supplier relationships
- A.5.20 — Addressing information security within supplier agreements — Include security clauses in all supplier contracts

## IDENTIFY

*preventive (left).* **Objective:** Identify the weaknesses and exposure enabling #10 Supply Chain Attack.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.9 — Inventory of information and other associated assets — Inventory all third-party components, libraries, and services in use
- A.8.4 — Access to source code — Identify all dependencies on external source code and assess supply chain risk

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Monitor for supply chain compromise campaigns (SolarWinds-type, dependency confusion)
- A.5.22 — Monitoring, review and change management of supplier services — Track changes in supplier services that could indicate compromise

## PROTECT

*preventive (left).* **Objective:** Prevent or reduce the likelihood of the #10 Supply Chain Attack step.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.25 — Secure development life cycle — Integrate supply chain security checks (dependency scanning, SBOM) into SDLC
- A.8.30 — Outsourced development — Enforce security requirements for outsourced development (code review, integrity verification)
- A.8.19 — Installation of software on operational systems — Verify integrity of software before installation (signatures, hashes)

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.19 — Information security in supplier relationships — Enforce supplier security requirements through contracts and assessments
- A.5.23 — Information security for use of cloud services — Secure cloud service supply chain (provider due diligence, exit plans)

## DETECT

*mitigating (right).* **Objective:** Detect #10 Supply Chain Attack activity within its Δt window, before it enables the next step.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.15 — Logging — Log software update events, package installations, and third-party API calls
- A.8.16 — Monitoring activities — Monitor for supply chain compromise indicators (unexpected update behavior, new network connections)

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.22 — Monitoring, review and change management of supplier services — Monitor supplier service changes for anomalous behavior indicating compromise
- A.5.7 — Threat intelligence — Integrate supply chain compromise IOCs into detection (malicious updates, backdoored packages)

## RESPOND

*mitigating (right).* **Objective:** Contain and eradicate #10 Supply Chain Attack once detected.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.28 — Collection of evidence — Preserve supply chain artifacts (package versions, update logs, integrity checksums) as evidence
- A.5.25 — Assessment and decision on information security events — Triage supply chain alerts and assess trust chain impact

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.24 — Information security incident management planning and preparation — Prepare response procedures for supply chain compromise incidents
- A.5.26 — Response to information security incidents — Contain supply chain compromise (isolate affected components, halt updates, notify affected parties)

## RECOVER

*mitigating (right).* **Objective:** Restore trustworthy capability after #10 Supply Chain Attack.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.30 — ICT readiness for business continuity — Include supply chain compromise recovery (vendor switching, redeployment) in continuity plans
- A.8.25 — Secure development life cycle — Rebuild and verify supply chain integrity (re-audit dependencies, update SBOMs)

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.29 — Information security during disruption — Maintain security during supply chain incident recovery
- A.5.27 — Learning from information security incidents — Review supply chain incidents to strengthen vendor management and verification
