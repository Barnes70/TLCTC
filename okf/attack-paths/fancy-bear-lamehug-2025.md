---
type: "attack-path"
title: "FANCY-BEAR-LAMEHUG-2025"
description: "FANCY BEAR's deployment of LAMEHUG, a novel LLM-enabled malware family, against Ukrainian government entities (mid-2025)."
resource: "tlctc:attack-path:fancy-bear-lamehug-2025"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-7"
  - "cluster-1"
  - "confidence-medium"
timestamp: "2026-04-16T00:00:00Z"
tlctc_version: "2.1"
---
# FANCY-BEAR-LAMEHUG-2025

## Attack path

```
||[human][@FancyBear→@UA-Govt]|| #9 →[Δt=?] #7 (FEC) →[Δt=?] #1 →[Δt=~5m] #1 + [DRE: C] →[Δt=?] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-spearphish | [#9](/clusters/cluster-9.md) | \|\|[human][@FancyBear→@UA-Govt]\|\| | ? |  |
| s2-lamehug-exec | [#7](/clusters/cluster-7.md) (FEC) |  | ? |  |
| s3-llm-recon | [#1](/clusters/cluster-1.md) |  | ~5m |  |
| s4-llm-doc-collection | [#1](/clusters/cluster-1.md) |  | ? | C |
| s5-exfiltration | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-spearphish:** FANCY BEAR delivers LAMEHUG via spear-phishing to targeted Ukrainian government entities. This is #9 Social Engineering: the spear-phishing email manipulates the recipient into engaging with the malicious payload. Boundary crossing: the attack traverses from the external attacker sphere through the human trust boundary into the Ukrainian government target environment. FANCY BEAR targets Ukrainian government officials for intelligence collection supporting Russia's strategic objectives. Specific lure content and delivery mechanism are not detailed in the CrowdStrike reporting.
- **s2-lamehug-exec:** LAMEHUG malware executes on the target system. R-EXEC: foreign executable content runs — recorded as #7 with fec_executed: true. LAMEHUG's distinguishing characteristic: it incorporates an LLM directly into its operational workflow. Rather than hardcoding traditional reconnaissance and collection logic, the adversary embeds predefined prompts that are sent to an LLM to generate commands at runtime. The malware uses deterministic model settings (e.g. temperature=0), prioritizing consistent output over creative variation. LAMEHUG lacked persistence mechanisms, consistent with short-lived 'smash-and-grab' operations designed for rapid intelligence collection.
- **s3-llm-recon:** LAMEHUG's embedded LLM generates and executes system enumeration commands. The observed prompt instructs the model to generate commands that: create C:\ProgramData\info directory, gather computer information, hardware information, running processes and services, network configuration, and Active Directory domain information, writing all output to C:\ProgramData\info\info.txt. This is #1 Abuse of Functions: all generated commands use legitimate OS utilities (systeminfo, net, wmic, etc.) exactly as designed — the generic vulnerability is that these functions perform their intended purpose for an unauthorized actor. The LLM is the novel command generation mechanism, replacing hardcoded reconnaissance logic.
- **s4-llm-doc-collection:** LAMEHUG's embedded LLM generates and executes document collection commands. The observed prompt instructs the model to generate commands that recursively copy Office documents, PDFs, and text files from user Documents, Downloads, and Desktop folders to the C:\ProgramData\info staging directory. This is #1 Abuse of Functions: standard file copy operations using legitimate OS commands, abused for intelligence collection. DRE: C — potentially sensitive government documents are collected and staged for exfiltration. The LLM delegation means the collection logic is not statically visible in the malware binary, potentially evading signature-based detection of hardcoded file-harvesting patterns.
- **s5-exfiltration:** Collected system reconnaissance data and documents are exfiltrated to adversary-controlled infrastructure. This is #1 Abuse of Functions: legitimate network transfer capabilities used to send staged data to adversary infrastructure. DRE: C — system enumeration data and sensitive Ukrainian government documents leave the target environment. CrowdStrike assessed that despite the LLM integration novelty, LAMEHUG 'did not demonstrate a meaningful increase in effectiveness or sophistication compared to traditional malware,' suggesting this campaign reflects experimentation with AI-enabled techniques rather than full operationalization. The malware signals continued state-nexus exploration of AI as a development aid and potential future mechanism for evading static detection.

# Citations

FANCY BEAR's deployment of LAMEHUG, a novel LLM-enabled malware family, against Ukrainian government entities (mid-2025). First observed instance of a state-nexus adversary embedding LLM prompting directly into malware to perform operational tasks. Rather than hardcoding reconnaissance logic, LAMEHUG uses predefined prompts to generate system enumeration and document collection commands at runtime. CrowdStrike assessed that the LLM integration 'did not demonstrate a meaningful increase in effectiveness or sophistication compared to traditional malware' — deterministic model settings and simple prompts suggest experimentation rather than operational reliance. LAMEHUG lacked persistence mechanisms, consistent with short-lived 'smash-and-grab' access. Attack path: #9 ||[human][@FancyBear→@UA-Govt]|| →[Δt=?] #7 →[Δt=?] #1 →[Δt=~5m] #1 + [DRE: C] →[Δt=?] #1 + [DRE: C]. Source: CrowdStrike 2026 Global Threat Report, p. 18, Case Highlight: FANCY BEAR's Use of LLM-Enabled Malware.
