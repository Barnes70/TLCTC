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
tlctc_version: "2.3"
---
# TESLA-K8S-CRYPTOJACKING-2018

## Attack path

```
#1 →[Δt=~5m] #7 (FEC) →[Δt=~20m] #1 →[Δt=~5m] #4 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-k8s-dashboard-access | [#1](/clusters/cluster-1.md) |  | ~5m |  |
| s2-cryptominer-deployment | [#7](/clusters/cluster-7.md) (FEC) |  | ~20m |  |
| s3-k8s-secrets-access | [#1](/clusters/cluster-1.md) |  | ~5m |  |
| s4-aws-credential-use | [#4](/clusters/cluster-4.md) |  |  | C |

## Step notes

- **s1-k8s-dashboard-access:** Attacker accessed Tesla's Kubernetes dashboard, which was exposed to the internet with no authentication configured. The dashboard worked exactly as designed — it simply had no authentication requirement enabled. #1 Abuse of Functions: the K8s dashboard's legitimate management functions (viewing pods, deploying workloads, accessing logs) were available to anyone who could reach it. No code vulnerability was exploited; the misconfiguration made designed functionality publicly accessible. This is distinct from #2 (exploiting server) because no software flaw was exploited — the service operated as configured.
- **s2-cryptominer-deployment:** Attacker used the Kubernetes dashboard to deploy a cryptomining container running Stratum mining protocol, connecting to an unlisted/private mining pool behind CloudFlare to evade IP-based detection. R-EXEC: foreign executable content (cryptomining container) deployed and executing in Tesla's Kubernetes cluster — recorded as #7 with fec_executed: true. The attacker also configured the mining pod with low CPU usage to avoid resource consumption alerts — operational security within the cluster.
- **s3-k8s-secrets-access:** Attacker used Kubernetes dashboard and kubectl access to enumerate and read Kubernetes Secrets, which contained AWS credentials (access keys and secret keys). The Kubernetes Secrets API functioned as designed — Secrets were accessible to users with dashboard-level access. #1 Abuse of Functions: the K8s Secrets API is a designed capability; the attacker used it within its intended parameters. The credentials stored in Secrets represent a DRE:C but are classified at the next step when applied.
- **s4-aws-credential-use:** Attacker used AWS credentials discovered in Kubernetes Secrets to authenticate to Tesla's broader AWS environment, gaining access to additional Tesla data including telemetry and potentially sensitive operational information. R-CRED: credential application (using AWS access keys to authenticate) = always #4, regardless of acquisition method (K8s Secrets access in this case). Axiom X: credential acquisition via #1 (K8s Secrets); credential use = #4. DRE: C — Tesla operational data and potentially customer telemetry exposed.

# Citations

Tesla Kubernetes cryptojacking incident, February 2018 (discovered by RedLock). Attackers found an unauthenticated Kubernetes dashboard exposed to the internet for one of Tesla's AWS environments. Through the dashboard, they deployed a cryptomining container (Stratum protocol, behind CloudFlare to evade IP-based detection), then discovered AWS credentials in Kubernetes secrets, which provided access to additional Tesla data. Attack path: #1 →[Δt=~5m] #7 →[Δt=~20m] #1 →[Δt=~5m] #4 + [DRE: C]. Sources: RedLock CSI Team report (February 2018), The Register reporting, Tesla acknowledgment.
