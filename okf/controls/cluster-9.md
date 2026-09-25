---
type: "control-objective-set"
title: "Controls → #9 Social Engineering"
description: "NIST CSF control objectives and ISO 27001:2022 Annex A starter controls for TLCTC #9 Social Engineering."
resource: "tlctc:controls:cluster-9"
tags:
  - "controls"
  - "nist-csf"
  - "iso27001"
  - "cluster-9"
cluster: "#9"
---
# Controls → #9 Social Engineering

> **Provenance:** the ISO 27001:2022 Annex A control placements below are *starter guidance* derived from the TLCTC Control Matrix tool (`tools/`), AI-assisted and not a certified control set. The normative cause-side taxonomy is the cluster definitions; control selection is organization-specific. See `/controls/index.md`.

Cause: [#9 Social Engineering](/clusters/cluster-9.md). Functions: [GOVERN](/controls/functions/govern.md) · [IDENTIFY](/controls/functions/identify.md) · [PROTECT](/controls/functions/protect.md) · [DETECT](/controls/functions/detect.md) · [RESPOND](/controls/functions/respond.md) · [RECOVER](/controls/functions/recover.md). Effectiveness: [/controls/effectiveness-model.md](/controls/effectiveness-model.md).

## GOVERN

*steering (spans the whole chain).* **Objective:** Govern the strategy, ownership, and risk appetite for the #9 Social Engineering cluster.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.14 — Information transfer — Define verification rules for information requests received via any channel
- A.5.37 — Documented operating procedures — Document verification procedures for unusual or high-risk requests

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.1 — Policies for information security — Define policies addressing social engineering risks (phishing, pretexting, baiting)
- A.5.2 — Information security roles and responsibilities — Assign ownership for security awareness and anti-social-engineering program
- A.6.2 — Terms and conditions of employment — Include security responsibilities in employment terms addressing social engineering risks

## IDENTIFY

*preventive (cause side).* **Objective:** Identify weaknesses enabling a #9 Social Engineering event.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.12 — Classification of information — Classify information to define what must never be shared in response to unsolicited requests
- A.6.8 — Information security event reporting — Track social engineering attempt frequency and success rates

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Monitor for social engineering campaigns targeting the organization or sector
- A.5.9 — Inventory of information and other associated assets — Identify high-value targets (executives, finance, IT admins) for social engineering

## PROTECT

*preventive (cause side).* **Objective:** Protect from a #9 Social Engineering event.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.23 — Web filtering — Block access to known phishing and social engineering domains
- A.8.7 — Protection against malware — Scan email attachments and links from social engineering vectors
- A.5.10 — Acceptable use of information and other associated assets — Prohibit sharing credentials or sensitive information via social channels
- A.5.13 — Labelling of information — Label information classification visibly to prevent disclosure under social pressure

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.6.3 — Information security awareness, education and training — Train staff to recognize and resist social engineering (phishing simulations, pretexting drills)
- A.6.6 — Confidentiality or non-disclosure agreements — Enforce NDAs limiting what staff may disclose to external parties

## DETECT

*central event (detects the loss of control).* **Objective:** Detect a #9 Social Engineering event.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.15 — Logging — Log email security events (blocked phishing, URL detonation, attachment analysis)
- A.8.16 — Monitoring activities — Monitor for social engineering indicators (email anomalies, impersonation, urgency patterns)

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.6.8 — Information security event reporting — Enable and encourage staff to report suspicious communications
- A.5.7 — Threat intelligence — Integrate social engineering IOCs (phishing domains, spoofed senders) into detection

## RESPOND

*central event → consequence side (contains).* **Objective:** Respond to a #9 Social Engineering event.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.28 — Collection of evidence — Preserve social engineering artifacts (emails, call logs, chat transcripts) as evidence
- A.5.25 — Assessment and decision on information security events — Assess social engineering incident scope and potential data exposure

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.24 — Information security incident management planning and preparation — Prepare response playbooks for social engineering incidents (BEC, phishing, vishing)
- A.5.26 — Response to information security incidents — Contain social engineering incidents (block sender, reset credentials, warn staff)

## RECOVER

*mitigating (consequence side).* **Objective:** Recover from a #9 Social Engineering event.

**Local controls (ISO 27001:2022 Annex A):**

- A.6.4 — Disciplinary process — Address policy violations resulting from social engineering susceptibility
- A.5.30 — ICT readiness for business continuity — Include social engineering compromise recovery in continuity plans

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.29 — Information security during disruption — Maintain awareness controls during recovery from social engineering incidents
- A.5.27 — Learning from information security incidents — Analyze social engineering incidents to improve training effectiveness
