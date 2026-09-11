---
type: "attack-path"
title: "TESLA-K8S-CRYPTOJACKING-2018"
description: "Tesla Kubernetes cryptojacking incident, February 2018 (discovered by RedLock)."
resource: "tlctc:attack-path:tesla-k8s-cryptojacking-2018"
tags:
  - "attack-path"
  - "cluster-1"
  - "cluster-7"
  - "cluster-4"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.5"
---
# TESLA-K8S-CRYPTOJACKING-2018

## Attack path

```
#1 →[Δt=~5m] #7 (FEC) →[Δt=~20m] #1 + [DRE: C] →[Δt=~5m] #4
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-k8s-dashboard-access | [#1](/clusters/cluster-1.md) |  | ~5m |  |
| s2-cryptominer-deployment | [#7](/clusters/cluster-7.md) (FEC) |  | ~20m |  |
| s3-k8s-secrets-access | [#1](/clusters/cluster-1.md) |  | ~5m | C |
| s4-aws-credential-use | [#4](/clusters/cluster-4.md) |  |  |  |

## Step notes

- **s1-k8s-dashboard-access:** Attacker accessed Tesla's Kubernetes dashboard, which was exposed to the internet with no authentication configured. The dashboard worked exactly as designed — it simply had no authentication requirement enabled. #1 Abuse of Functions: the K8s dashboard's legitimate management functions (viewing pods, deploying workloads, accessing logs) were available to anyone who could reach it. No code vulnerability was exploited; the misconfiguration made designed functionality publicly accessible. This is distinct from #2 (exploiting server) because no software flaw was exploited — the service operated as configured.
- **s2-cryptominer-deployment:** Attacker used the Kubernetes dashboard to deploy a cryptomining container running Stratum mining protocol, connecting to an unlisted/private mining pool behind CloudFlare to evade IP-based detection. R-EXEC: foreign executable content (cryptomining container) deployed and executing in Tesla's Kubernetes cluster — recorded as #7 with fec_executed: true. The attacker also configured the mining pod with low CPU usage to avoid resource consumption alerts — operational security within the cluster.
- **s3-k8s-secrets-access:** Attacker used Kubernetes dashboard and kubectl access to enumerate and read Kubernetes Secrets, which contained AWS credentials (access keys and secret keys). The Kubernetes Secrets API functioned as designed — Secrets were accessible to users with dashboard-level access. #1 Abuse of Functions: the K8s Secrets API is a designed capability; the attacker used it within its intended parameters. [DRE: C] is recorded here: the credentials held in Secrets were disclosed at the moment they were read. Per Axiom X the acquisition of credential material maps to the enabling cluster, which is this #1 step; it is not deferred to the #4 step that later applies them.
- **s4-aws-credential-use:** Attacker used AWS credentials discovered in Kubernetes Secrets to authenticate to Tesla's broader AWS environment. R-CRED: credential application (using AWS access keys to authenticate) = always #4, regardless of acquisition method (K8s Secrets access in this case). Axiom X: credential acquisition via #1 (K8s Secrets, where its DRE is recorded); credential use = #4. This step carries no DRE. Authenticating discloses nothing of itself, and the disclosure it would enable is not established: RedLock reported that the S3 buckets reachable with these credentials held telemetry data, but no public source establishes that Tesla data was read or exfiltrated, and the observed attacker objective was cryptomining. A [DRE: C] is therefore not asserted for the AWS environment. If evidence of actual data access emerges, it belongs on a further #1 step for the read, not on this authentication step.

# Citations

Tesla Kubernetes cryptojacking incident, February 2018 (discovered by RedLock). Attackers found an unauthenticated Kubernetes dashboard exposed to the internet for one of Tesla's AWS environments. Through the dashboard, they deployed a cryptomining container (Stratum protocol, behind CloudFlare to evade IP-based detection), then discovered AWS credentials in Kubernetes secrets, which provided access to additional Tesla data. Attack path: #1 →[Δt=~5m] #7 →[Δt=~20m] #1 + [DRE: C] →[Δt=~5m] #4. Sources: RedLock CSI Team report (February 2018), The Register reporting, Tesla acknowledgment.
