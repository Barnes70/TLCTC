---
type: "term"
title: "Cyber Threat Radar"
description: "A standard visualization methodology for communicating threat posture, change over time, and comparative exposure across the 10 TLCTC clusters."
resource: "tlctc:term:cyber-threat-radar"
tags:
  - "glossary"
---
# Cyber Threat Radar

A standard visualization methodology for communicating threat posture, change over time, and comparative exposure across the 10 TLCTC clusters. The radar is a **communication surface, not a classification device** — every position on it is driven by evidence classified under the Section 4 grammar.

**Structure:**

- **Spokes (10):** one per cluster (`#1`–`#10`), fixed order; the invariant layout is what makes radars from different organizations, sectors, or snapshots directly comparable.
- **Zones (4, outer → inner):** `Latent` → `Low` → `Medium` → `High`. Radial distance encodes current exposure or impact.
- **Sectors (configurable):** angular subdivisions within each spoke representing responsibility scopes. Default alignment is to Layer 2 responsibility spheres (`@Org`, `@Customers`, `@Vendor` / `@External`). At state/national scope, sectors may encode critical-infrastructure sectors (energy, finance, healthcare, etc.).
- **Bubbles:** individual threat instances, sized by significance.
- **Movement indicators:** `▲` rising / `▼` falling exposure vs. the previous snapshot.

**Scales:** organizational view (enterprise-internal), sector / line-of-business view, and state-level / national view. The spoke layout is invariant across all three — only the sector axis changes, which is what enables cross-view comparison.

**Normative rules (R-RADAR-1…5):** spoke assignment MUST use the Section 4 grammar; multi-cluster attack paths MUST be rendered as multiple bubbles or a single bubble plus a separate Layer 3 path; zone placement SHOULD follow a disclosed scoring method; snapshots SHOULD be dated and use the same method for movement indicators to be meaningful; aggregated sector / national radars MUST use identical spoke definitions and SHOULD disclose the combination rule (max / average / weighted).

**Reference:** §17.1–17.2




**Related reading:** [CrowdStrike 2024 Threat Hunting Report — TLCTC](https://www.tlctc.net/tlctc-CrowdStrike2024.html), [ENISA Threat Landscape 2025 — TLCTC](https://www.tlctc.net/tlctc-enisa-2025-threat-report.html), [GTIG AI Threat Tracker (May 2026) — TLCTC](https://www.tlctc.net/gtig-ai-threat-tracker-2026.html), [Emerging technologies as threat enablers](https://www.tlctc.net/tlctc-emerging-tech-radar.html), [Harbor Registry × TLCTC Cyber Threat Radar](https://www.tlctc.net/tlctc-harbor-integration.html), [Report-to-Radar AI prompt for TLCTC](https://www.tlctc.net/tlctc-prompt-radar.html)

See also: Attacker Profile, Tech Enablers Overlay, Responsibility Sphere, Layer 2

**Tool:** [`/tools/radar-tlctc-app.html`](/tools/radar-tlctc-app.html)
