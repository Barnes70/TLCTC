---
type: "term"
title: "Attack Velocity (Δt)"
description: "The temporal dimension of cyber risk representing the time interval between two adjacent Attack Steps in an attack path."
resource: "tlctc:term:attack-velocity-t"
tags:
  - "glossary"
---
# Attack Velocity (Δt)

The temporal dimension of cyber risk representing the **time interval** between two adjacent Attack Steps in an attack path. For an edge `#X → #Y`, the value `Δt(X→Y)` represents the elapsed time between step `#X` and step `#Y` in the described scenario. Δt is an edge property attached to the sequence operator, not to steps. Attack velocity matters defensively because it bounds the time a detection-and-response control has to act between adjacent steps (see Detection Coverage Score). Categorized into four velocity classes: Latent/Slow (days to months), Medium (hours), Fast (minutes), and Realtime (seconds/milliseconds).

**Reference:** §12.0 (Definitions), §12.1 (Measurement Model), §12.2 (Notation)

**Related reading:** [CrowdStrike 2025 Threat Hunting Report — TLCTC](https://www.tlctc.net/tlctc-crowdstrike-2025-analysis.html), [CrowdStrike 2025 Threat Report — Strategy & Velocity](https://www.tlctc.net/tlctc-crowdstrike-2025-threat-report.html), [GTIG AI Threat Tracker (May 2026) — TLCTC](https://www.tlctc.net/gtig-ai-threat-tracker-2026.html), [MITRE ATT&CK & STIX × TLCTC V2.0 — implementation guide](https://www.tlctc.net/stix-tlctc.html), [IEC 62443 × TLCTC v2.0 — industrial cybersecurity](https://www.tlctc.net/tlctc-iec62443-v2.html), [FAIR × TLCTC — enhanced quantitative risk](https://www.tlctc.net/tlctc-fair.html), [ISO/SAE 21434 × TLCTC V2.0 — automotive](https://www.tlctc.net/tlctc-blog-IsoSae21434.html), [ISO 27000 × TLCTC — name vs game](https://www.tlctc.net/blog-iso27001-iso27005.html), [OCTAVE × TLCTC v2.0 — causal taxonomy](https://www.tlctc.net/blog-tlctc-octave.html), [Enhancing CVE records with TLCTC v2.1](https://www.tlctc.net/tlctc-cve-nvd.html), [EU Cybersecurity Act (CSA) × TLCTC V2.0](https://www.tlctc.net/blog-eu-cybersecurity-act-csa.html), [EU cyber regulation needs a common taxonomy](https://www.tlctc.net/blog-eu-regulation-tlctc-taxonomy.html), [DORA TLPT × TLCTC V2.1 — boundary & velocity](https://www.tlctc.net/tlctc-regulation-dora-tlpt.html), [Why ORX must rethink the "cyber event"](https://www.tlctc.net/tlctc-orx-rethink-cyber-event.html), [TLCTC classification decision tree V2.0/V2.1](https://www.tlctc.net/tlctc-decision-tree.html), [Agentic AI as consequence amplifier (right side of Bow-Tie)](https://www.tlctc.net/tlctc-agentic-ai-consequences.html), [Quantum & AI — new magic, same 10 threats](https://www.tlctc.net/tlctc-quantum-ai-velocity.html), [The Commit Is the CVE — silent fixes & the patch-gap collapse](https://www.tlctc.net/silent-fix-window.html), [tlctc-attack-velocity.html](https://www.tlctc.net/tlctc-attack-velocity.html), [TLCTC v2.1 monster prompt — SOC & Detection](https://www.tlctc.net/tlctc-prompt-soc.html)
