---
type: "attack-path"
title: "TESLA-INSIDER-2023"
description: "Tesla insider data breach (May 2023)."
resource: "tlctc:attack-path:tesla-insider-2023"
tags:
  - "attack-path"
  - "cluster-1"
  - "cluster-8"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.3"
---
# TESLA-INSIDER-2023

## Attack path

```
#1 + [DRE: C] →[Δt=~2w] ||[physical][@Tesla→@External]|| #8 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-data-access | [#1](/clusters/cluster-1.md) |  | ~2w | C |
| s2-physical-exfiltration | [#8](/clusters/cluster-8.md) | \|\|[physical][@Tesla→@External]\|\| |  | C |

## Step notes

- **s1-data-access:** Abuse of legitimate system functions: two former or departing Tesla employees used their own valid credentials and authorized (or marginally over-scoped) access to query and bulk-download confidential records from Tesla's internal HR, payroll, and engineering systems. No technical exploit was involved — no vulnerability was exploited in the software, no credentials were stolen, and no authentication was bypassed. The systems functioned exactly as designed; the employees simply used those designed functions for an unauthorized purpose (mass data collection for external disclosure). The generic vulnerability is Abuse of Functions (#1): the system permitted bulk data access because it was designed to support legitimate business operations, and the employees abused that designed capability. Axiom IV (Actor Independence): the fact that these are insiders does not change the classification. If an external attacker had obtained valid credentials and performed the same queries, the classification of this step would still be #1 — the vulnerability is in the system's function scope, not the actor's identity. Axiom III (Cause, Not Outcome): 'insider threat' is an outcome label; the cause is that the system's data access functions lacked sufficient granularity controls (e.g., bulk export restrictions, data loss prevention monitoring, or need-to-know access segmentation). DRE: C (Loss of Confidentiality) — 75,735 employee records including SSNs, financial data, salary information, and proprietary manufacturing data accessed by unauthorized parties. The ~2w delta represents the approximate period over which the employees collected and staged the data before physically removing it from Tesla's domain. Detection opportunity: data loss prevention (DLP) tools monitoring for anomalous bulk data access patterns could have flagged the unusual query volumes.
- **s2-physical-exfiltration:** Physical exfiltration across organizational boundary: the employees transferred the collected confidential data from Tesla's internal domain to external control — likely via personal devices, personal email, USB storage media, or cloud storage uploads from personal accounts — and subsequently provided it to Handelsblatt. The generic vulnerability is physical access (#8): the employees had physical access to workstations and network endpoints from which they could transfer data to media or channels outside Tesla's organizational control. This step is classified as #8 (Physical Attack) because the data crossed from Tesla's responsibility sphere (@Tesla) to external control (@External) through a physical transfer mechanism. The topology_boundary marks this as a bridge cluster crossing the physical context boundary. Even if the transfer used a digital channel (e.g., email to personal account), the enabler was physical access to an endpoint within Tesla's domain — without physical presence at a Tesla workstation or VPN endpoint, the transfer could not occur. DRE: C (Loss of Confidentiality) — the data is now outside Tesla's organizational control and has been provided to a third-party news organization. Controls that could have mitigated this step: USB port disabling policies, DLP monitoring on email and cloud upload channels, endpoint data transfer restrictions, and watermarking of sensitive documents to enable tracing. This is the terminal step. Handelsblatt, as a legitimate news organization, reportedly cooperated with court orders and did not publish the raw personal data, limiting the downstream impact to affected individuals.

# Citations

Tesla insider data breach (May 2023). Two former Tesla employees exploited their legitimate access to internal systems to exfiltrate confidential data affecting 75,735 current and former employees, including Social Security numbers, financial records, salary data, and proprietary manufacturing secrets — including Elon Musk's personal SSN. The data was leaked to Handelsblatt, a German news outlet. Tesla's internal investigation traced the breach to the two individuals, who had violated IT security and data protection policies. Tesla filed lawsuits in Germany and obtained court orders to seize the leaked data and prohibit Handelsblatt from further use or distribution. This is a pure insider threat case with no technical exploitation — the employees used their own legitimate credentials and access to systems whose functions operated as designed. Attack path: #1 + [DRE: C] →[Δt=~2w] #8 + [DRE: C]. Sources: Tesla notification letter to Maine Attorney General (August 18, 2023); Handelsblatt reporting (May 2023); Tesla data breach notification to affected employees; Reuters and Bloomberg coverage of Tesla's German court filings.
