---
type: "attack-path"
title: "MANDIANT-MULTI-YEAR-ESPIONAGE-2025"
description: "Composite attack path modeled on Mandiant M-Trends 2026 'Multi-Year Intrusions Highlighting Extreme Persistence' (pp."
resource: "tlctc:attack-path:mandiant-multi-year-espionage-2025"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-7"
  - "cluster-1"
  - "cluster-4"
  - "confidence-high"
timestamp: "2026-04-14T00:00:00Z"
tlctc_version: "2.3"
---
# MANDIANT-MULTI-YEAR-ESPIONAGE-2025

## Attack path

```
||[human][@External→@Org]|| #9 →[Δt=~1h] #7 (FEC) →[Δt=~1d] #1 + [DRE: C] →[Δt=~weeks] #4 →[Δt=~months] #1 →[Δt=~1y] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-spear-phishing | [#9](/clusters/cluster-9.md) | \|\|[human][@External→@Org]\|\| | ~1h |  |
| s2-implant-execution | [#7](/clusters/cluster-7.md) (FEC) |  | ~1d |  |
| s3-credential-harvest | [#1](/clusters/cluster-1.md) |  | ~weeks | C |
| s4-credential-use-lateral | [#4](/clusters/cluster-4.md) |  | ~months |  |
| s5-lotl-persistence | [#1](/clusters/cluster-1.md) |  | ~1y |  |
| s6-long-term-exfiltration | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-spear-phishing:** Spear-phishing lure tailored to aerospace/defense target: fake job opportunity, HR impersonation, or trade conference invitation. Generic vulnerability: human psychological susceptibility. The victim is enticed to open an attachment or visit a staging URL.
- **s2-implant-execution:** Custom implant executes on victim host (UNC1549 tradecraft favors bespoke tooling with long-term tasking). R-EXEC satisfied: FEC execution recorded. The implant is designed to minimize beacon footprint; long sleep intervals and cloud-resident C2 are characteristic.
- **s3-credential-harvest:** Living-off-the-land credential harvesting: browser data read by the implant (legitimate file access, abused scope), cached Kerberos tickets, RDP credentials. Classified #1 because the OS-native data-gathering functions are legitimate; the implant orchestrates rather than exploits. DRE:C on harvested credentials.
- **s4-credential-use-lateral:** Use of harvested credentials to authenticate to adjacent hosts, file servers, and domain services. R-CRED / Axiom X: credential application is ALWAYS #4. Lateral movement typically via RDP / WMI with native Windows tooling to avoid noisy tradecraft.
- **s5-lotl-persistence:** Living-off-the-land persistence: scheduled tasks created via schtasks, WMI event subscriptions, registry run-keys. Legitimate OS persistence mechanisms, abused scope. No new malware dropped — the implant from s2 is renewed through legitimate means to survive host rebuilds.
- **s6-long-term-exfiltration:** Slow, low-volume exfiltration of aerospace/defense intellectual property over months to years. Legitimate network functions (HTTPS to cloud storage, staged email forwarding rules), abused scope. DRE:C. The dwell time measured in years is the defining characteristic — Mandiant observed cases with 4+ year dwell in this cohort.

# Citations

Composite attack path modeled on Mandiant M-Trends 2026 'Multi-Year Intrusions Highlighting Extreme Persistence' (pp. 66-69). UNC1549 (Iran, aerospace/defense) and UNC5807 (PRC, edge/core network devices) both maintained years-long dwell. This path represents the UNC1549-style pattern: spear phishing for initial access, custom malware for long-term tasking, living-off-the-land lateral movement, and slow exfiltration over VC-1 timescales. Axiom IV: actor identity does not determine cluster classification. Sources: M-Trends 2026 pp. 66-69.
