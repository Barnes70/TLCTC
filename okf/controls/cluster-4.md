---
type: "control-objective-set"
title: "Controls → #4 Identity Theft"
description: "NIST CSF control objectives and ISO 27001:2022 Annex A starter controls for TLCTC #4 Identity Theft."
resource: "tlctc:controls:cluster-4"
tags:
  - "controls"
  - "nist-csf"
  - "iso27001"
  - "cluster-4"
cluster: "#4"
---
# Controls → #4 Identity Theft

> **Provenance:** the ISO 27001:2022 Annex A control placements below are *starter guidance* derived from the TLCTC Control Matrix tool (`tools/`), AI-assisted and not a certified control set. The normative cause-side taxonomy is the cluster definitions; control selection is organization-specific. See `/controls/index.md`.

Cause: [#4 Identity Theft](/clusters/cluster-4.md). Functions: [GOVERN](/controls/functions/govern.md) · [IDENTIFY](/controls/functions/identify.md) · [PROTECT](/controls/functions/protect.md) · [DETECT](/controls/functions/detect.md) · [RESPOND](/controls/functions/respond.md) · [RECOVER](/controls/functions/recover.md). Effectiveness: [/controls/effectiveness-model.md](/controls/effectiveness-model.md).

> The whitepaper provides a normative worked example for #4 (§8.1.6); the ISO 27001 Annex A controls below are the operational starter layer.

## GOVERN

*cross-cutting.* **Objective:** Establish ownership, policy, and risk-appetite for #4 Identity Theft.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.17 — Authentication information — Define requirements for credential strength, rotation, and protection
- A.5.37 — Documented operating procedures — Document credential management and identity verification procedures

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.1 — Policies for information security — Define identity and access management policies including MFA requirements
- A.5.16 — Identity management — Govern identity lifecycle from provisioning through decommissioning
- A.5.3 — Segregation of duties — Enforce duty separation to limit impact of single compromised identity

## IDENTIFY

*preventive (left).* **Objective:** Identify the weaknesses and exposure enabling #4 Identity Theft.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.2 — Privileged access rights — Identify all privileged accounts and their access scope
- A.5.18 — Access rights — Review access rights to identify excessive or orphaned permissions

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.9 — Inventory of information and other associated assets — Inventory all identity stores, directories, and authentication systems
- A.5.7 — Threat intelligence — Monitor for credential dump campaigns, password spray attacks, and identity theft TTPs

## PROTECT

*preventive (left).* **Objective:** Prevent or reduce the likelihood of the #4 Identity Theft step.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.5 — Secure authentication — Enforce MFA and strong authentication to prevent credential abuse
- A.8.3 — Information access restriction — Implement role-based access to limit impact of stolen credentials
- A.8.2 — Privileged access rights — Restrict and time-limit elevated access to reduce identity theft impact
- A.5.34 — Privacy and protection of PII — Protect personally identifiable information to reduce identity theft impact
- A.8.11 — Data masking — Apply data masking to reduce exposure of sensitive identifiers in non-production contexts

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.15 — Access control — Enforce access control policies preventing unauthorized identity assumption
- A.6.5 — Responsibilities after termination or change of employment — Revoke access promptly upon role changes or termination

## DETECT

*mitigating (right).* **Objective:** Detect #4 Identity Theft activity within its Δt window, before it enables the next step.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.15 — Logging — Log authentication events, failed attempts, and access anomalies
- A.8.16 — Monitoring activities — Monitor for credential abuse indicators (impossible travel, unusual hours, brute force)
- A.8.5 — Secure authentication — Detect authentication anomalies (token replay, session hijack, MFA bypass attempts)

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Integrate credential theft indicators (leaked credentials, dark web monitoring) into detection

## RESPOND

*mitigating (right).* **Objective:** Contain and eradicate #4 Identity Theft once detected.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.28 — Collection of evidence — Preserve authentication logs and session data for identity theft forensics
- A.5.25 — Assessment and decision on information security events — Triage identity alerts and assess scope of compromised access

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.24 — Information security incident management planning and preparation — Prepare response playbooks for credential compromise
- A.5.26 — Response to information security incidents — Contain identity theft (force password reset, revoke sessions, disable accounts)

## RECOVER

*mitigating (right).* **Objective:** Restore trustworthy capability after #4 Identity Theft.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.30 — ICT readiness for business continuity — Include identity system recovery in continuity plans
- A.5.16 — Identity management — Re-establish verified identity states and clean up compromised accounts
- A.5.11 — Return of assets — Ensure return of all access tokens, devices, and credentials upon separation

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.29 — Information security during disruption — Maintain access controls during identity recovery operations
- A.5.27 — Learning from information security incidents — Analyze identity theft incidents to strengthen authentication controls
