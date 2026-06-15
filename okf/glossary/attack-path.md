---
type: "term"
title: "Attack Path"
description: "The sequence of applied Attack Vectors in a cyber incident, representing an ordered sequence of Attack Steps describing a complete attack scenario."
resource: "tlctc:term:attack-path"
tags:
  - "glossary"
---
# Attack Path

The sequence of applied Attack Vectors in a cyber incident, representing an ordered sequence of Attack Steps describing a complete attack scenario. Basic notation uses `#X → #Y → #Z` (e.g., `#9→#3→#7`). Attack paths may include velocity annotations showing the time between steps (e.g., `#9→[24h]#4→[12m]#1`), domain boundary markers using the `||` operator, parallel steps, and Data Risk Event tags.

**Reference:** §4.2.2 (Global Definitions), §11.0 (Path Semantics)

**Related reading:** [CrowdStrike 2024 Threat Hunting Report — TLCTC](https://www.tlctc.net/tlctc-CrowdStrike2024.html), [Mandiant M-Trends 2025 — TLCTC](https://www.tlctc.net/tlctc-mtrends-2025.html), [ENISA Threat Landscape 2025 — TLCTC](https://www.tlctc.net/tlctc-enisa-2025-threat-report.html), [Same Attack, Four Stories — vendor report comparison](https://www.tlctc.net/tlctc-threat-report-chaos.html), [PASTA threat modeling × TLCTC](https://www.tlctc.net/tlctc-pasta.html), [CKC + ATT&CK + TLCTC — Holy Trinity of Defense](https://www.tlctc.net/blog-ckc-attack-tlctc-synthesis.html), [TLCTC × Threat Modeling Manifesto](https://www.tlctc.net/tlctc-threat-modeling-manifesto.html), [20 annotated attack paths (Ransomware, BEC, OT, ...)](https://www.tlctc.net/tlctc-attack-path-examples.html), [SSDLC for developers — the "S" problem](https://www.tlctc.net/tlctc-ssdlc.html), [TLCTC v2.1 monster prompt — CTI & Forensic](https://www.tlctc.net/tlctc-prompt-cti.html), [Report-to-Radar AI prompt for TLCTC](https://www.tlctc.net/tlctc-prompt-radar.html), [TLCTC v2.1 monster prompt — SOC & Detection](https://www.tlctc.net/tlctc-prompt-soc.html), [TLCTC v2.1 AI analysis prompt — teach any LLM](https://www.tlctc.net/tlctc-ai-analysis-prompt.html), [TLCTC v2.1 monster prompts — index](https://www.tlctc.net/tlctc-prompt-index.html)
