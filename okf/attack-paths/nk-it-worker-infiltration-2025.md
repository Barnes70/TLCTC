---
type: "attack-path"
title: "NK-IT-WORKER-INFILTRATION-2025"
description: "North Korean state-sponsored IT worker infiltration scheme, industrialized by 2025."
resource: "tlctc:attack-path:nk-it-worker-infiltration-2025"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-04-09T00:00:00Z"
tlctc_version: "2.5"
---
# NK-IT-WORKER-INFILTRATION-2025

## Attack path

```
||[human][@DPRK→@WesternOrg]|| #9 →[Δt=~30d] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-deepfake-identity-hiring | [#9](/clusters/cluster-9.md) | \|\|[human][@DPRK→@WesternOrg]\|\| | ~30d |  |
| s2-insider-access-abuse | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-deepfake-identity-hiring:** North Korean operatives leverage fraudulent identities, AI-driven deepfakes for video interviews, and fabricated digital personas (LinkedIn, GitHub profiles) to pass the hiring process at Western organizations. This is #9 Social Engineering: the bridge cluster crosses the human boundary — the hiring managers are psychologically manipulated into trusting a fabricated persona. The deepfake technology and fabricated personas are tools that amplify the social engineering, not separate technical exploitation steps. Axiom IV: actor identity (state-sponsored) does not determine classification; the generic vulnerability is human susceptibility to identity deception. Outcome of this step: the organization onboards the operative and provisions legitimate corporate credentials (VPN, SSO, email, code repositories) to the fabricated persona. Per R-CRED (self-issued proviso), the operative's subsequent authentication with those credentials is authentication as the authentic holder of the enrolled (fictitious) identity — NOT a separate #4 step. The fraudulent trust is established here, at the #9 hiring step; there is no impersonation of a real identity to reclassify as #4.
- **s2-insider-access-abuse:** The embedded operative uses legitimate administrative and financial system access to fulfill intelligence collection objectives and funnel revenue back to the DPRK regime. Access is conducted from abroad via RMM software through US-based laptop farms that host the corporate hardware, maintaining the domestic residency illusion. All access uses designed system capabilities — code repositories, financial systems, internal documentation. This is #1 Abuse of Functions: the systems operate within their designed parameters; the scope is abused by an adversarial insider holding a legitimately provisioned identity. DRE: C — exfiltration of proprietary source code, financial data, and business intelligence. Detection indicators include impossible travel alerts, mouse-jiggling software for activity simulation, and deepfake rendering micro-artifacts in video metadata.

# Citations

North Korean state-sponsored IT worker infiltration scheme, industrialized by 2025. Operatives infiltrate Western organizations using fraudulent identities and AI-driven deepfakes to bypass video interviews, funneling hundreds of millions of dollars in revenue back to the regime. Workers maintain domestic residency illusion using US-based 'laptop farms' and facilitators to host corporate hardware, accessing devices via RMM software from abroad. Thousands create comprehensive digital personas on LinkedIn and GitHub. Detection indicators: impossible travel login alerts, mouse-jiggling software, video metadata micro-artifacts from real-time deepfake rendering. Attack path: #9 ||[human][@External->@Org]|| -> #1 + [DRE: C]. Sources: Cloudflare 2026 Threat Report (pp. 12, 24-27), Cloudforce One analysis. RECLASSIFIED under the v2.5 R-CRED self-issued proviso (2026-08-14, canonical variant = fabricated fictitious persona): the operative's daily authentication uses credentials the organization itself provisioned to the persona through its designed hiring/onboarding function, so the presenter IS the authentic holder of that (fictitious) enrolled identity — authentication as self, not #4. No legitimate identity is impersonated. The prior classification carried a separate #4 credential-use step (#9 -> #4 -> #1); that step is withdrawn per the proviso. Variant note: where operatives instead authenticate as a real complicit US citizen's rented account, a genuine identity IS presented and that variant reintroduces a #4 step (#9 -> #4 -> #1); the fictitious-persona variant modeled here is treated as canonical.
