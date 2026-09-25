---
type: "control-objective-set"
title: "Controls → #7 Malware"
description: "NIST CSF control objectives and ISO 27001:2022 Annex A starter controls for TLCTC #7 Malware."
resource: "tlctc:controls:cluster-7"
tags:
  - "controls"
  - "nist-csf"
  - "iso27001"
  - "cluster-7"
cluster: "#7"
---
# Controls → #7 Malware

> **Provenance:** the ISO 27001:2022 Annex A control placements below are *starter guidance* derived from the TLCTC Control Matrix tool (`tools/`), AI-assisted and not a certified control set. The normative cause-side taxonomy is the cluster definitions; control selection is organization-specific. See `/controls/index.md`.

Cause: [#7 Malware](/clusters/cluster-7.md). Functions: [GOVERN](/controls/functions/govern.md) · [IDENTIFY](/controls/functions/identify.md) · [PROTECT](/controls/functions/protect.md) · [DETECT](/controls/functions/detect.md) · [RESPOND](/controls/functions/respond.md) · [RECOVER](/controls/functions/recover.md). Effectiveness: [/controls/effectiveness-model.md](/controls/effectiveness-model.md).

## GOVERN

*steering (spans the whole chain).* **Objective:** Govern the strategy, ownership, and risk appetite for the #7 Malware cluster.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.37 — Documented operating procedures — Document malware prevention, detection, and response procedures
- A.5.10 — Acceptable use of information and other associated assets — Prohibit unauthorized software installation and removable media use

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.1 — Policies for information security — Define anti-malware policies including allowed software, execution controls, and media handling
- A.5.2 — Information security roles and responsibilities — Assign ownership for malware defense program and incident handling
- A.5.4 — Management responsibilities — Ensure management enforces anti-malware controls and supports security investment

## IDENTIFY

*preventive (cause side).* **Objective:** Identify weaknesses enabling a #7 Malware event.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.8 — Management of technical vulnerabilities — Identify vulnerabilities exploited by current malware campaigns for prioritized patching
- A.8.19 — Installation of software on operational systems — Audit installed software against approved baseline to detect unauthorized additions

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Monitor malware threat intelligence (campaigns, families, IOCs targeting deployed platforms)
- A.5.9 — Inventory of information and other associated assets — Inventory all endpoints and their anti-malware coverage status

## PROTECT

*preventive (cause side).* **Objective:** Protect from a #7 Malware event.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.7 — Protection against malware — Deploy and maintain anti-malware controls (AV, EDR, application whitelisting)
- A.8.1 — User endpoint devices — Harden endpoints against malware (disable autorun, restrict macros, enable application control)
- A.8.19 — Installation of software on operational systems — Enforce application whitelisting and code signing requirements
- A.7.10 — Storage media — Control removable storage media to prevent malware introduction

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.6.3 — Information security awareness, education and training — Train users to recognize malware delivery vectors (phishing, drive-by, USB)

## DETECT

*central event (detects the loss of control).* **Objective:** Detect a #7 Malware event.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.7 — Protection against malware — Configure real-time malware detection with behavioral and signature-based engines
- A.8.15 — Logging — Log process execution, file system changes, and network connections for malware activity detection
- A.8.16 — Monitoring activities — Monitor endpoints for malware behavioral indicators (encryption activity, C2 beacons, lateral movement)

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.7 — Threat intelligence — Integrate malware IOC feeds into detection systems (hashes, domains, behaviors)

## RESPOND

*central event → consequence side (contains).* **Objective:** Respond to a #7 Malware event.

**Local controls (ISO 27001:2022 Annex A):**

- A.5.28 — Collection of evidence — Collect malware samples and forensic artifacts for analysis and attribution
- A.5.25 — Assessment and decision on information security events — Triage malware alerts and determine infection scope and impact

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.24 — Information security incident management planning and preparation — Prepare malware incident playbooks (containment, eradication, recovery)
- A.5.26 — Response to information security incidents — Contain malware spread (isolate host, block C2, quarantine files)

## RECOVER

*mitigating (consequence side).* **Objective:** Recover from a #7 Malware event.

**Local controls (ISO 27001:2022 Annex A):**

- A.8.13 — Information backup — Restore data from verified clean backups after malware eradication
- A.8.1 — User endpoint devices — Reimage or restore infected endpoints to verified clean state

**Umbrella controls (ISO 27001:2022 Annex A):**

- A.5.29 — Information security during disruption — Maintain security monitoring during malware cleanup and recovery
- A.5.27 — Learning from information security incidents — Conduct post-incident malware analysis to improve preventive controls
