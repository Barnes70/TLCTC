---
type: "attack-path"
title: "UBER-BREACH-2016"
description: "Uber data breach of 2016 (disclosed November 2017)."
resource: "tlctc:attack-path:uber-breach-2016"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.3"
---
# UBER-BREACH-2016

## Attack path

```
#4 + [DRE: C] →[Δt=instant] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-aws-credential-use | [#4](/clusters/cluster-4.md) |  | instant | C |
| s2-s3-data-exfiltration | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-aws-credential-use:** Attackers obtained AWS access keys that were hardcoded in source code within a private GitHub repository accessible to them. They used these AWS credentials to authenticate to Uber's AWS account. R-CRED: credential application (using AWS access keys to authenticate to the AWS API) is always #4, regardless of acquisition method. Axiom X: the credential was acquired by reading source code (a prior access step not fully documented in public reports); the application of the credential to authenticate is this #4 step. DRE: C — the AWS credentials themselves represent a confidentiality loss. This incident demonstrates the risk of secrets embedded in code repositories.
- **s2-s3-data-exfiltration:** Attacker used the authenticated AWS session to list and download data from Uber's S3 buckets. The buckets contained names, email addresses, and phone numbers of 57 million riders worldwide, plus driver license numbers of 600,000 US drivers. The AWS S3 API functioned as designed — the valid credentials granted legitimate access to the storage resources. #1 Abuse of Functions: the S3 API, ListBucket, and GetObject operations all worked as intended; the attacker operated within the designed functionality using stolen but technically valid credentials. DRE: C — massive PII dataset exfiltrated.

# Citations

Uber data breach of 2016 (disclosed November 2017). Attackers accessed a private GitHub repository used by Uber engineers, found AWS access keys hardcoded in the source code, and used those credentials to access S3 buckets containing personal data of 57 million riders and drivers. Uber paid $100K to the attackers through a bug bounty program to suppress disclosure, leading to criminal charges against Uber's CSO. Attack path: #4 →[Δt=instant] #1 + [DRE: C]. Sources: Uber disclosure (November 2017), Bloomberg reporting, FTC investigation, DOJ criminal case against CSO Joseph Sullivan (2022).
