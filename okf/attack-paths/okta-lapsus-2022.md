---
type: "attack-path"
title: "OKTA-LAPSUS-2022"
description: "Lapsus$ attack on Okta via Sitel (third-party support contractor), January 2022 (disclosed March 2022)."
resource: "tlctc:attack-path:okta-lapsus-2022"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-4"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.3"
---
# OKTA-LAPSUS-2022

## Attack path

```
||[human][@Lapsus→@Sitel]|| #9 →[Δt=~1h] #4 →[Δt=~5d] #1 →[Δt=~25m] ||[auth][@Sitel→@Okta]|| #4 →[Δt=~30m] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-social-engineering | [#9](/clusters/cluster-9.md) | \|\|[human][@Lapsus→@Sitel]\|\| | ~1h |  |
| s2-sitel-credential-use | [#4](/clusters/cluster-4.md) |  | ~5d |  |
| s3-sitel-internal-navigation | [#1](/clusters/cluster-1.md) |  | ~25m |  |
| s4-okta-superuser-access | [#4](/clusters/cluster-4.md) | \|\|[auth][@Sitel→@Okta]\|\| | ~30m |  |
| s5-customer-tenant-access | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-social-engineering:** Lapsus$ group socially engineered a Sitel customer support contractor, likely via phone-based social engineering (vishing) or phishing. Sitel provides outsourced support services for Okta. #9 Social Engineering: the generic vulnerability is human psychological susceptibility. The boundary crossing is from external (@Lapsus) into the contractor's domain (@Sitel) via the human context. The contractor role creates an extended attack surface — third-party personnel with privileged access.
- **s2-sitel-credential-use:** Attacker used compromised credentials to authenticate to Sitel's internal systems. R-CRED: credential application (authenticating to Sitel's infrastructure) is always #4 regardless of how the credentials were obtained (social engineering in this case). Axiom X: the credential acquisition occurred in s1 (#9); the credential use is this separate #4 step.
- **s3-sitel-internal-navigation:** Attacker navigated Sitel's internal systems over ~5 days, locating and accessing Okta support tools available to Sitel contractors. The internal systems functioned as designed — Sitel personnel were authorized to use these tools as part of their support role. #1 Abuse of Functions: the attacker used legitimate internal navigation and support tooling within their (stolen) authorization scope.
- **s4-okta-superuser-access:** Attacker used Sitel's legitimate delegated support credentials to authenticate to Okta's SuperUser internal support tool, crossing the trust boundary from the contractor domain to Okta's customer-facing administrative domain. R-CRED: credential application = always #4. The topology boundary annotation shows the authentication crossing from @Sitel to @Okta — a critical trust boundary where contractor credentials grant access to customer identity infrastructure.
- **s5-customer-tenant-access:** Attacker used the SuperUser tool to view and potentially modify data across ~366 Okta customer tenants. The SuperUser tool functioned as designed — it was built to allow support staff to view customer configurations and assist with troubleshooting. #1 Abuse of Functions: the tool's legitimate capabilities were used for unauthorized access. DRE: C — customer tenant data, configurations, and potentially authentication tokens exposed. This step demonstrates the cascading impact of identity provider compromise on downstream customers.

# Citations

Lapsus$ attack on Okta via Sitel (third-party support contractor), January 2022 (disclosed March 2022). Attackers socially engineered a Sitel support engineer, gained access to Sitel systems, then used Okta's internal SuperUser support tool to access ~366 customer tenants. Demonstrated third-party/contractor supply chain risk to identity providers. Attack path: #9 ||[human][@External→@Sitel]|| →[Δt=~1h] #4 →[Δt=~5d] #1 →[Δt=~25m] #4 ||[auth][@Sitel→@Okta]|| →[Δt=~30m] #1 + [DRE: C]. Sources: Okta official incident report (March 2022), Sitel/Sykes investigation findings, Lapsus$ Telegram disclosures, Mandiant analysis.
