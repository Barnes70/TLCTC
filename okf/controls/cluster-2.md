---
type: "control-objective-set"
title: "Controls → #2 Exploiting Server"
description: "NIST CSF control objectives and ISO 27001:2022 Annex A starter controls for TLCTC #2 Exploiting Server."
resource: "tlctc:controls:cluster-2"
tags:
  - "controls"
  - "nist-csf"
  - "iso27001"
  - "cluster-2"
cluster: "#2"
---
# Controls → #2 Exploiting Server

> **Provenance:** the ISO 27001:2022 Annex A control placements below are *starter guidance* derived from the TLCTC Control Matrix tool (`tools/`), AI-assisted and not a certified control set. The normative cause-side taxonomy is the cluster definitions; control selection is organization-specific. See `/controls/index.md`.

Cause: [#2 Exploiting Server](/clusters/cluster-2.md). Functions: [GOVERN](/controls/functions/govern.md) · [IDENTIFY](/controls/functions/identify.md) · [PROTECT](/controls/functions/protect.md) · [DETECT](/controls/functions/detect.md) · [RESPOND](/controls/functions/respond.md) · [RECOVER](/controls/functions/recover.md). Effectiveness: [/controls/effectiveness-model.md](/controls/effectiveness-model.md).

> The whitepaper provides a normative worked example for #2 (§8.1.5); the ISO 27001 Annex A controls below are the operational starter layer.

## GOVERN

*cross-cutting.* **Objective:** Establish ownership, policy, and risk-appetite for #2 Exploiting Server.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.31 — Legal, statutory, regulatory and contractual requirements — Identify compliance requirements for server-hosted data and services
- A.5.37 — Documented operating procedures — Document server hardening and patch management procedures
- A.8.33 — Test information — Protect test information and ensure production data is not used without safeguards

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.1 — Policies for information security — Define policies for server hardening, patching, and vulnerability management
- A.5.2 — Information security roles and responsibilities — Assign ownership for server security and vulnerability remediation
- A.5.8 — Information security in project management — Require security assessment of server components in all projects
- A.5.35 — Independent review of information security — Commission independent security reviews of server infrastructure and controls

## IDENTIFY

*preventive (left).* **Objective:** Identify the weaknesses and exposure enabling #2 Exploiting Server.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.8 — Management of technical vulnerabilities — Scan servers for known vulnerabilities and prioritize by exploitability
- A.8.9 — Configuration management — Identify server misconfigurations and deviations from hardening baselines
- A.8.29 — Security testing in development and acceptance — Conduct security testing of server applications before deployment

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Monitor threat feeds for server-side exploit campaigns targeting deployed technologies
- A.5.9 — Inventory of information and other associated assets — Maintain inventory of all server assets, OS versions, and exposed services
- A.5.6 — Contact with special interest groups — Engage ISACs and security communities for server vulnerability intelligence

## PROTECT

*preventive (left).* **Objective:** Prevent or reduce the likelihood of the #2 Exploiting Server step.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.8 — Management of technical vulnerabilities — Apply patches and mitigations for server-side vulnerabilities within defined SLAs
- A.8.27 — Secure system architecture and engineering principles — Design server architecture with defense-in-depth against exploitation
- A.8.26 — Application security requirements — Define security requirements for server-side applications
- A.8.22 — Segregation of networks — Segment server networks to limit lateral movement after exploitation
- A.8.28 — Secure coding — Apply secure coding practices to prevent introduction of server-side vulnerabilities
- A.8.31 — Separation of development, test and production environments — Separate development, test, and production server environments to prevent cross-contamination

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.23 — Information security for use of cloud services — Secure cloud-hosted server instances with provider-specific hardening

## DETECT

*mitigating (right).* **Objective:** Detect #2 Exploiting Server activity within its Δt window, before it enables the next step.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.15 — Logging — Log server access, error conditions, and authentication events for exploit detection
- A.8.16 — Monitoring activities — Monitor servers for exploitation indicators (unexpected processes, file changes, outbound connections)
- A.8.20 — Networks security — Deploy network-based intrusion detection for server exploitation attempts

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Integrate server exploit signatures and IOCs into detection systems

## RESPOND

*mitigating (right).* **Objective:** Contain and eradicate #2 Exploiting Server once detected.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.28 — Collection of evidence — Capture server forensic images and logs for exploitation analysis
- A.5.25 — Assessment and decision on information security events — Triage server security alerts and determine exploitation scope

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.24 — Information security incident management planning and preparation — Prepare response playbooks for server compromise scenarios
- A.5.26 — Response to information security incidents — Contain server exploitation (isolate, patch, rotate credentials)

## RECOVER

*mitigating (right).* **Objective:** Restore trustworthy capability after #2 Exploiting Server.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.30 — ICT readiness for business continuity — Include server compromise recovery in business continuity plans
- A.8.13 — Information backup — Restore server systems and data from verified clean backups

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.29 — Information security during disruption — Maintain server security controls during recovery operations
- A.5.27 — Learning from information security incidents — Analyze server exploitation root cause to prevent recurrence
