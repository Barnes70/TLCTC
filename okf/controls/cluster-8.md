---
type: "control-objective-set"
title: "Controls → #8 Physical Attack"
description: "NIST CSF control objectives and ISO 27001:2022 Annex A starter controls for TLCTC #8 Physical Attack."
resource: "tlctc:controls:cluster-8"
tags:
  - "controls"
  - "nist-csf"
  - "iso27001"
  - "cluster-8"
cluster: "#8"
---
# Controls → #8 Physical Attack

> **Provenance:** the ISO 27001:2022 Annex A control placements below are *starter guidance* derived from the TLCTC Control Matrix tool (`tools/`), AI-assisted and not a certified control set. The normative cause-side taxonomy is the cluster definitions; control selection is organization-specific. See `/controls/index.md`.

Cause: [#8 Physical Attack](/clusters/cluster-8.md). Functions: [GOVERN](/controls/functions/govern.md) · [IDENTIFY](/controls/functions/identify.md) · [PROTECT](/controls/functions/protect.md) · [DETECT](/controls/functions/detect.md) · [RESPOND](/controls/functions/respond.md) · [RECOVER](/controls/functions/recover.md). Effectiveness: [/controls/effectiveness-model.md](/controls/effectiveness-model.md).

## GOVERN

*cross-cutting.* **Objective:** Establish ownership, policy, and risk-appetite for #8 Physical Attack.

**Local controls (ISO 27001:2022 Annex A):**

- A.7.6 — Working in secure areas — Establish rules for working in secure areas (no photography, escort requirements)
- A.5.37 — Documented operating procedures — Document physical access procedures, visitor management, and emergency protocols

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.1 — Policies for information security — Define physical security policies including perimeters, access control, and environmental protection
- A.5.2 — Information security roles and responsibilities — Assign ownership for physical security program
- A.5.36 — Compliance with policies, rules and standards for information security — Verify compliance with physical security policies and regulatory standards

## IDENTIFY

*preventive (left).* **Objective:** Identify the weaknesses and exposure enabling #8 Physical Attack.

**Local controls (ISO 27001:2022 Annex A):**

- A.7.1 — Physical security perimeters — Assess physical perimeter adequacy and identify boundary weaknesses
- A.7.3 — Securing offices, rooms and facilities — Identify sensitive areas requiring enhanced physical protection

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Monitor physical threat intelligence (local crime, targeted break-ins, insider threats)
- A.5.9 — Inventory of information and other associated assets — Inventory all physical locations, server rooms, and high-value asset locations

## PROTECT

*preventive (left).* **Objective:** Prevent or reduce the likelihood of the #8 Physical Attack step.

**Local controls (ISO 27001:2022 Annex A):**

- A.7.2 — Physical entry — Implement physical access controls (badges, biometrics, mantraps)
- A.7.8 — Equipment siting and protection — Position equipment to minimize physical attack exposure
- A.7.5 — Protecting against physical and environmental threats — Protect against environmental threats (fire, flood, power loss)
- A.7.7 — Clear desk and clear screen — Enforce clear desk/screen policy to prevent physical information disclosure
- A.7.9 — Security of assets off-premises — Secure assets during transport, at remote work locations, and while traveling

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.6.1 — Screening — Screen personnel with physical access to sensitive areas
- A.6.3 — Information security awareness, education and training — Train staff on physical security awareness (tailgating, unauthorized access)

## DETECT

*mitigating (right).* **Objective:** Detect #8 Physical Attack activity within its Δt window, before it enables the next step.

**Local controls (ISO 27001:2022 Annex A):**

- A.7.4 — Physical security monitoring — Monitor physical access points with CCTV, sensors, and alarms
- A.8.15 — Logging — Log physical access events (badge reads, door opens, visitor entries)
- A.8.16 — Monitoring activities — Monitor for physical security anomalies (after-hours access, repeated denied attempts)

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.6.8 — Information security event reporting — Enable staff to report physical security anomalies

## RESPOND

*mitigating (right).* **Objective:** Contain and eradicate #8 Physical Attack once detected.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.28 — Collection of evidence — Preserve CCTV footage and access logs as evidence of physical breach

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.24 — Information security incident management planning and preparation — Prepare response procedures for physical security breaches
- A.5.26 — Response to information security incidents — Contain physical breaches (lock down, isolate area, alert authorities)
- A.5.5 — Contact with authorities — Coordinate with law enforcement for physical security incidents

## RECOVER

*mitigating (right).* **Objective:** Restore trustworthy capability after #8 Physical Attack.

**Local controls (ISO 27001:2022 Annex A):**

- A.7.13 — Equipment maintenance — Repair and verify physical security equipment after incidents
- A.7.14 — Secure disposal or re-use of equipment — Securely dispose of equipment compromised by physical attack

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.29 — Information security during disruption — Maintain security during physical facility recovery
- A.5.27 — Learning from information security incidents — Review physical security incidents to improve controls
