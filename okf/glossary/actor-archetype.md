---
type: "term"
title: "Actor Archetype"
description: "The typical, recurring attack sequence pattern that characterizes how an actor (or an Actor Group) chains TLCTC clusters across incidents — e.g., 9 → 7 → 4 → 1 ."
resource: "tlctc:term:actor-archetype"
tags:
  - "glossary"
---
# Actor Archetype

The typical, recurring **attack-sequence pattern** that characterizes how an actor (or an Actor Group) chains TLCTC clusters across incidents — e.g., `#9 → #7 → #4 → #1`. In the Actor Profile Designer tool the archetype is captured per-actor in the **Archetype** field (the `sequence` attribute in the JSON), and the *Most Common Archetypes* panel aggregates actors that share the same pattern, surfacing dominant attack chains across the dataset. Archetypes are a communication and trend-watching device — they are never used for cluster classification (Axiom IV). An archetype describes *which clusters an actor tends to prefer* and *in what order it tends to chain them*, not the cluster of any specific attack step. Distinct from [Actor Group](#actor-group), which is the generalized actor category (Nation-State, Cybercriminal-Ransomware, …) and carries a capability vector rather than a sequence pattern.

**Reference:** §17.3 (Attacker Profiles)

**Tool:** [`/tools/actor-profile-designer.html`](/tools/actor-profile-designer.html)




**Related reading:** [CrowdStrike 2024 Threat Hunting Report — TLCTC](https://www.tlctc.net/tlctc-CrowdStrike2024.html), [CrowdStrike 2025 Threat Report — Strategy & Velocity](https://www.tlctc.net/tlctc-crowdstrike-2025-threat-report.html), [Diamond Model × TLCTC — structuring the empty spaces](https://www.tlctc.net/tlctc-diamond-model.html), [tlctc-Attacker-Profiling.html](https://www.tlctc.net/tlctc-Attacker-Profiling.html)

See also: Actor Group, Attacker Profile, Cyber Threat Radar, Axiom IV
