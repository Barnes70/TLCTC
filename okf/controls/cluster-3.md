---
type: "control-objective-set"
title: "Controls → #3 Exploiting Client"
description: "NIST CSF control objectives and ISO 27001:2022 Annex A starter controls for TLCTC #3 Exploiting Client."
resource: "tlctc:controls:cluster-3"
tags:
  - "controls"
  - "nist-csf"
  - "iso27001"
  - "cluster-3"
cluster: "#3"
---
# Controls → #3 Exploiting Client

> **Provenance:** the ISO 27001:2022 Annex A control placements below are *starter guidance* derived from the TLCTC Control Matrix tool (`tools/`), AI-assisted and not a certified control set. The normative cause-side taxonomy is the cluster definitions; control selection is organization-specific. See `/controls/index.md`.

Cause: [#3 Exploiting Client](/clusters/cluster-3.md). Functions: [GOVERN](/controls/functions/govern.md) · [IDENTIFY](/controls/functions/identify.md) · [PROTECT](/controls/functions/protect.md) · [DETECT](/controls/functions/detect.md) · [RESPOND](/controls/functions/respond.md) · [RECOVER](/controls/functions/recover.md). Effectiveness: [/controls/effectiveness-model.md](/controls/effectiveness-model.md).

## GOVERN

*cross-cutting.* **Objective:** Establish ownership, policy, and risk-appetite for #3 Exploiting Client.

**Local controls (ISO 27001:2022 Annex A):**

- A.6.7 — Remote working — Establish security requirements for remote client devices and home networks
- A.5.37 — Documented operating procedures — Document client hardening procedures and approved application lists

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.1 — Policies for information security — Define policies for client device hardening, browser security, and application controls
- A.5.2 — Information security roles and responsibilities — Assign ownership for endpoint security program

## IDENTIFY

*preventive (left).* **Objective:** Identify the weaknesses and exposure enabling #3 Exploiting Client.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.8 — Management of technical vulnerabilities — Scan client applications for known vulnerabilities
- A.8.1 — User endpoint devices — Identify all endpoint device types and their security posture

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Monitor threat intelligence for client-side exploit campaigns (browser, document, plugin)
- A.5.9 — Inventory of information and other associated assets — Maintain inventory of all client devices, software versions, and browser extensions

## PROTECT

*preventive (left).* **Objective:** Prevent or reduce the likelihood of the #3 Exploiting Client step.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.1 — User endpoint devices — Harden endpoint configurations (disable macros, restrict plugins, enable sandboxing)
- A.8.19 — Installation of software on operational systems — Restrict software installation to approved applications only
- A.8.23 — Web filtering — Filter web content to block known exploit delivery sites
- A.8.8 — Management of technical vulnerabilities — Patch client applications (browsers, office, media) within defined SLAs

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.6.3 — Information security awareness, education and training — Train users on client-side risks (malicious documents, drive-by downloads)

## DETECT

*mitigating (right).* **Objective:** Detect #3 Exploiting Client activity within its Δt window, before it enables the next step.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.15 — Logging — Log client application events, process execution, and file downloads for exploitation detection
- A.8.16 — Monitoring activities — Monitor endpoints for client-side exploitation indicators (unexpected child processes, shellcode)
- A.8.7 — Protection against malware — Detect exploitation payloads delivered through client-side vectors

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Integrate client exploit IOCs into endpoint detection rules

## RESPOND

*mitigating (right).* **Objective:** Contain and eradicate #3 Exploiting Client once detected.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.28 — Collection of evidence — Collect endpoint forensic artifacts from exploited client systems
- A.5.25 — Assessment and decision on information security events — Triage client exploitation alerts and assess lateral movement risk

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.24 — Information security incident management planning and preparation — Prepare response procedures for client-side exploitation incidents
- A.5.26 — Response to information security incidents — Contain client exploitation (isolate endpoint, kill processes, block C2)

## RECOVER

*mitigating (right).* **Objective:** Restore trustworthy capability after #3 Exploiting Client.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.30 — ICT readiness for business continuity — Include client system rebuild in continuity plans
- A.8.1 — User endpoint devices — Reimage or restore client devices to verified clean state

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.29 — Information security during disruption — Maintain endpoint security during client system recovery
- A.5.27 — Learning from information security incidents — Review client exploitation incidents to improve endpoint controls
