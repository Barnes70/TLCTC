---
type: "attack-path"
title: "MANDIANT-SAAS-CASCADE-2025"
description: "Attack path derived from Mandiant M-Trends 2026 'The Cascading Impact of Third-Party SaaS Compromises' (pp."
resource: "tlctc:attack-path:mandiant-saas-cascade-2025"
tags:
  - "attack-path"
  - "cluster-2"
  - "cluster-7"
  - "cluster-1"
  - "cluster-10"
  - "cluster-4"
  - "confidence-high"
timestamp: "2026-04-14T00:00:00Z"
tlctc_version: "2.6"
---
# MANDIANT-SAAS-CASCADE-2025

## Attack path

```
||[api][@External→@SaaSProvider]|| #2 →[Δt=~1h] #7 (FEC) →[Δt=~1d] #1 →[Δt=~6h] #1 + [DRE: C] →[Δt=~1h] ||[api][@SaaSProvider→@Customer]|| #10 →[Δt=instant] #4 →[Δt=~1h] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-webshell-exploit | [#2](/clusters/cluster-2.md) | \|\|[api][@External→@SaaSProvider]\|\| | ~1h |  |
| s2-webshell-persistence | [#7](/clusters/cluster-7.md) (FEC) |  | ~1d |  |
| s3-cloud-recon | [#1](/clusters/cluster-1.md) |  | ~6h |  |
| s4-service-principal-exfil | [#1](/clusters/cluster-1.md) |  | ~1h | C |
| s5-trust-acceptance | [#10](/clusters/cluster-10.md) | \|\|[api][@SaaSProvider→@Customer]\|\| | instant |  |
| s6-sp-auth-to-customer | [#4](/clusters/cluster-4.md) |  | ~1h |  |
| s7-customer-data-access | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-webshell-exploit:** Exploitation of the SaaS provider's internet-facing admin/API plane: SQL injection, deserialization, or webshell upload via an authenticated admin app. R-ROLE: the SaaS provider's application is in server role relative to the attacker → #2 (Exploiting Server).
- **s2-webshell-persistence:** Webshell / post-exploitation implant installed on the provider's infrastructure. R-EXEC satisfied: FEC execution of attacker-supplied code on the provider's server. Enables persistent hands-on-keyboard operations inside the provider's tenancy.
- **s3-cloud-recon:** Azure AD / Entra ID reconnaissance within the provider's tenant: enumerate service principals, OAuth applications, and multi-tenant integrations. Legitimate cloud management APIs, abused scope. No exploit, no FEC.
- **s4-service-principal-exfil:** Extract service-principal secrets / OAuth refresh tokens that grant the provider's app delegated access into downstream customer tenants. Legitimate secret-retrieval APIs (Key Vault, configuration store), abused scope. DRE:C — the provider's cross-tenant credentials are the crown jewels.
- **s5-trust-acceptance:** Trust Acceptance Event (R-SUPPLY): the customer tenant honors the provider's service principal as if it were the provider itself — cryptographically it is. v2.6 federation: the provider and its service-principal secret, its federation trust material, were subverted at s1-s4, so the customer's acceptance of the subverted authority is the TAE (#10). Falsifiability (v2.6): remove that subversion and the acceptance is the trust link working as designed, not a step. Each authentication presented through the subverted authority remains #4 (s6): #10 → #4. v2.5 recorded the order #4 → #10.
- **s6-sp-auth-to-customer:** Authentication into the downstream customer tenant using the exfiltrated service-principal secret. R-CRED / Axiom X: credential application is ALWAYS #4, regardless of how the credential was acquired. The authentication looks indistinguishable from normal provider-to-customer integration traffic. Under v2.6 federation it follows the TAE (s5).
- **s7-customer-data-access:** Use of delegated API access to query customer data (CRM records, documents, emails). Legitimate, audited API calls — abused scope. DRE:C. The downstream victim's only observable signal is behavioral: unusual query volume or off-hours access from the provider's service principal.

# Citations

Attack path derived from Mandiant M-Trends 2026 'The Cascading Impact of Third-Party SaaS Compromises' (pp. 74-77). UNC5221-style pattern: compromise a SaaS provider via a public-facing webshell / SQLi, extract Azure Service Principals and OAuth refresh tokens, then ride the provider's legitimate integration chain into downstream customer tenants. The downstream step is where #10 (Supply Chain) appears — at the customer's Trust Acceptance Event where the provider's service principal is honored. Sources: M-Trends 2026 pp. 21, 74-77. v2.6 requalification (2026-09-23): the provider-to-customer segment is re-sequenced from #4 -> #10 to #10 -> #4. Under v2.6 federation, the customer's acceptance of the subverted provider authority (the provider and its service-principal secret were subverted at s1-s4) is the TAE (s5, #10), and each authentication presented through it remains #4 (s6). Step ids renumbered accordingly (v2.5: s5 = #4, s6 = #10). Path: #2 -> #7 -> #1 -> #1 + [DRE: C] -> #10 -> #4 -> #1 + [DRE: C].
