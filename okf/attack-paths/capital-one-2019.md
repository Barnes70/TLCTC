---
type: "attack-path"
title: "CAPITAL-ONE-2019"
description: "Capital One data breach, March 2019 (disclosed July 2019)."
resource: "tlctc:attack-path:capital-one-2019"
tags:
  - "attack-path"
  - "cluster-2"
  - "cluster-4"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.3"
---
# CAPITAL-ONE-2019

## Attack path

```
#2 + [DRE: C] →[Δt=instant] #4 →[Δt=~4h] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-ssrf-exploit | [#2](/clusters/cluster-2.md) |  | instant | C |
| s2-iam-credential-use | [#4](/clusters/cluster-4.md) |  | ~4h |  |
| s3-s3-data-exfiltration | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-ssrf-exploit:** Attacker exploited a Server-Side Request Forgery (SSRF) vulnerability in Capital One's misconfigured WAF/reverse proxy running on an EC2 instance. The SSRF allowed the attacker to make the server issue HTTP requests to the internal EC2 instance metadata service (169.254.169.254 — IMDS v1), which returned temporary IAM role credentials. R-ROLE: the WAF/reverse proxy is server-role software — it receives and processes HTTP requests from the internet = #2. DRE: C — the temporary IAM credentials were exposed via the SSRF. Axiom X: the credential acquisition occurs here (enabling cluster = #2); the credential use is a separate step.
- **s2-iam-credential-use:** Attacker used the stolen temporary IAM role credentials to authenticate to AWS APIs. R-CRED: credential application (using IAM credentials to authenticate to AWS) = always #4, regardless of acquisition method (SSRF in this case). Axiom X: the SSRF (#2) acquired the credentials; this step records their use. The temporary credentials had overly broad S3 access permissions — a compounding factor but not a separate cluster (the permissions are part of the credential's authorization scope).
- **s3-s3-data-exfiltration:** Attacker used the authenticated AWS session to list and download data from over 700 Capital One S3 folders. The data included 106 million credit card applications, 140,000 Social Security numbers, and 80,000 bank account numbers. The S3 API (ListBucket, GetObject) functioned as designed — the valid IAM credentials granted legitimate access. #1 Abuse of Functions: the cloud storage APIs worked exactly as intended; the attacker operated within designed functionality using stolen credentials. DRE: C — one of the largest banking data breaches in US history. This incident led to AWS promoting IMDS v2 (which requires session tokens and mitigates SSRF-based metadata theft).

# Citations

Capital One data breach, March 2019 (disclosed July 2019). Former AWS employee Paige Thompson exploited a misconfigured WAF (ModSecurity) on Capital One's AWS infrastructure via Server-Side Request Forgery (SSRF) to reach the EC2 instance metadata service (IMDS v1), obtaining temporary IAM role credentials. Those credentials were used to access S3 buckets containing 106 million customer records (credit card applications, SSNs, bank account numbers). Attack path: #2 + [DRE: C] →[Δt=instant] #4 →[Δt=~4h] #1 + [DRE: C]. Sources: Capital One public statement (July 2019), DOJ criminal complaint, AWS IMDS security guidance, US District Court Western District of Washington case documents.
