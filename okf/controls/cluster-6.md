---
type: "control-objective-set"
title: "Controls → #6 Flooding Attack"
description: "NIST CSF control objectives and ISO 27001:2022 Annex A starter controls for TLCTC #6 Flooding Attack."
resource: "tlctc:controls:cluster-6"
tags:
  - "controls"
  - "nist-csf"
  - "iso27001"
  - "cluster-6"
cluster: "#6"
---
# Controls → #6 Flooding Attack

> **Provenance:** the ISO 27001:2022 Annex A control placements below are *starter guidance* derived from the TLCTC Control Matrix tool (`tools/`), AI-assisted and not a certified control set. The normative cause-side taxonomy is the cluster definitions; control selection is organization-specific. See `/controls/index.md`.

Cause: [#6 Flooding Attack](/clusters/cluster-6.md). Functions: [GOVERN](/controls/functions/govern.md) · [IDENTIFY](/controls/functions/identify.md) · [PROTECT](/controls/functions/protect.md) · [DETECT](/controls/functions/detect.md) · [RESPOND](/controls/functions/respond.md) · [RECOVER](/controls/functions/recover.md). Effectiveness: [/controls/effectiveness-model.md](/controls/effectiveness-model.md).

## GOVERN

*cross-cutting.* **Objective:** Establish ownership, policy, and risk-appetite for #6 Flooding Attack.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.23 — Information security for use of cloud services — Define cloud service availability SLAs and DDoS protection requirements
- A.5.37 — Documented operating procedures — Document DDoS response and traffic management procedures

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.1 — Policies for information security — Define availability requirements and DoS protection policies
- A.5.2 — Information security roles and responsibilities — Assign ownership for availability management and DDoS defense
- A.5.31 — Legal, statutory, regulatory and contractual requirements — Identify regulatory availability requirements (SLA, uptime)

## IDENTIFY

*preventive (left).* **Objective:** Identify the weaknesses and exposure enabling #6 Flooding Attack.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.6 — Capacity management — Assess capacity limits and identify single points of failure for resource exhaustion
- A.8.14 — Redundancy of information processing facilities — Identify redundancy gaps that increase flooding attack impact

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Monitor for flooding attack campaigns targeting organization's sector or infrastructure
- A.5.9 — Inventory of information and other associated assets — Inventory public-facing assets and their bandwidth/capacity profiles

## PROTECT

*preventive (left).* **Objective:** Prevent or reduce the likelihood of the #6 Flooding Attack step.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.6 — Capacity management — Provision capacity headroom and auto-scaling to absorb traffic spikes
- A.8.14 — Redundancy of information processing facilities — Deploy redundant processing to maintain availability during flooding
- A.8.20 — Networks security — Deploy rate limiting, traffic shaping, and DDoS mitigation at network level
- A.8.22 — Segregation of networks — Segregate critical services to contain flooding impact
- A.7.11 — Supporting utilities — Protect supporting utilities (power, cooling, comms) to maintain availability

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.29 — Information security during disruption — Ensure availability controls remain functional during flooding attacks

## DETECT

*mitigating (right).* **Objective:** Detect #6 Flooding Attack activity within its Δt window, before it enables the next step.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.15 — Logging — Log traffic volumes, connection rates, and resource utilization for flooding detection
- A.8.16 — Monitoring activities — Monitor for flooding indicators (traffic spikes, resource exhaustion, latency increases)
- A.8.6 — Capacity management — Alert when resource utilization approaches capacity thresholds

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Integrate DDoS botnet indicators and attack signatures into detection

## RESPOND

*mitigating (right).* **Objective:** Contain and eradicate #6 Flooding Attack once detected.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.25 — Assessment and decision on information security events — Assess flooding attack scope and identify targeted services

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.24 — Information security incident management planning and preparation — Prepare DDoS response runbooks with ISP and CDN escalation procedures
- A.5.26 — Response to information security incidents — Activate DDoS mitigation (upstream filtering, traffic scrubbing, failover)
- A.5.5 — Contact with authorities — Coordinate with ISPs and authorities during large-scale flooding attacks

## RECOVER

*mitigating (right).* **Objective:** Restore trustworthy capability after #6 Flooding Attack.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.30 — ICT readiness for business continuity — Test and update business continuity plans for extended DDoS scenarios
- A.8.14 — Redundancy of information processing facilities — Validate and restore redundancy after flooding-induced failover

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.29 — Information security during disruption — Restore service availability with security controls active
- A.5.27 — Learning from information security incidents — Analyze flooding attacks to improve capacity planning and mitigation
