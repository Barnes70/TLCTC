---
type: "control-objective-set"
title: "Controls → #5 Man in the Middle"
description: "NIST CSF control objectives and ISO 27001:2022 Annex A starter controls for TLCTC #5 Man in the Middle."
resource: "tlctc:controls:cluster-5"
tags:
  - "controls"
  - "nist-csf"
  - "iso27001"
  - "cluster-5"
cluster: "#5"
---
# Controls → #5 Man in the Middle

> **Provenance:** the ISO 27001:2022 Annex A control placements below are *starter guidance* derived from the TLCTC Control Matrix tool (`tools/`), AI-assisted and not a certified control set. The normative cause-side taxonomy is the cluster definitions; control selection is organization-specific. See `/controls/index.md`.

Cause: [#5 Man in the Middle](/clusters/cluster-5.md). Functions: [GOVERN](/controls/functions/govern.md) · [IDENTIFY](/controls/functions/identify.md) · [PROTECT](/controls/functions/protect.md) · [DETECT](/controls/functions/detect.md) · [RESPOND](/controls/functions/respond.md) · [RECOVER](/controls/functions/recover.md). Effectiveness: [/controls/effectiveness-model.md](/controls/effectiveness-model.md).

## GOVERN

*cross-cutting.* **Objective:** Establish ownership, policy, and risk-appetite for #5 Man in the Middle.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.31 — Legal, statutory, regulatory and contractual requirements — Identify regulatory requirements for data-in-transit protection
- A.5.37 — Documented operating procedures — Document certificate management and secure channel configuration procedures

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.1 — Policies for information security — Define policies for encryption standards, certificate management, and secure communications
- A.5.14 — Information transfer — Define rules and agreements for secure information transfer between parties
- A.5.2 — Information security roles and responsibilities — Assign ownership for network security and encryption program

## IDENTIFY

*preventive (left).* **Objective:** Identify the weaknesses and exposure enabling #5 Man in the Middle.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.20 — Networks security — Identify all network segments and their encryption status
- A.7.12 — Cabling security — Identify physical network cabling vulnerable to tapping

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Monitor for MitM campaign intelligence (rogue APs, certificate abuse, BGP hijacks)
- A.5.9 — Inventory of information and other associated assets — Inventory all network paths, certificates, and trust anchors

## PROTECT

*preventive (left).* **Objective:** Prevent or reduce the likelihood of the #5 Man in the Middle step.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.24 — Use of cryptography — Implement strong encryption (TLS 1.3, IPsec) for all data in transit
- A.8.20 — Networks security — Enforce network security controls (802.1X, WPA3) preventing unauthorized access
- A.8.21 — Security of network services — Secure network services with mutual authentication and encryption
- A.8.22 — Segregation of networks — Segregate networks to limit interception scope

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.14 — Information transfer — Enforce encrypted channels for all sensitive information transfers

## DETECT

*mitigating (right).* **Objective:** Detect #5 Man in the Middle activity within its Δt window, before it enables the next step.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.15 — Logging — Log certificate events, connection downgrades, and network anomalies
- A.8.16 — Monitoring activities — Monitor for MitM indicators (certificate mismatches, ARP spoofing, DNS hijacking)
- A.8.17 — Clock synchronization — Ensure accurate timestamps for correlating network interception events

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Integrate MitM indicators (rogue certificates, ARP anomalies) into detection

## RESPOND

*mitigating (right).* **Objective:** Contain and eradicate #5 Man in the Middle once detected.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.28 — Collection of evidence — Capture network traffic and certificate data for interception forensics
- A.5.25 — Assessment and decision on information security events — Triage network anomaly alerts for potential interception

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.24 — Information security incident management planning and preparation — Prepare response procedures for interception incidents
- A.5.26 — Response to information security incidents — Contain MitM attacks (revoke compromised certificates, isolate network segments)

## RECOVER

*mitigating (right).* **Objective:** Restore trustworthy capability after #5 Man in the Middle.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.30 — ICT readiness for business continuity — Include network infrastructure recovery in continuity plans
- A.8.24 — Use of cryptography — Reissue certificates and re-establish secure channels after compromise

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.29 — Information security during disruption — Maintain encrypted communications during network recovery
- A.5.27 — Learning from information security incidents — Review interception incidents to strengthen transport security
