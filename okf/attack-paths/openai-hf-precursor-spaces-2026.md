---
type: "attack-path"
title: "OPENAI-HF-2026-PRE"
description: "OpenAI - Hugging Face incident, precursor side-branch of 2026-05-26 against @HF-Prod."
resource: "tlctc:attack-path:openai-hf-precursor-spaces-2026"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-1"
  - "cluster-7"
  - "confidence-high"
timestamp: "2026-08-30T00:00:00Z"
tlctc_version: "2.5"
---
# OPENAI-HF-2026-PRE

## Attack path

```
||[auth][@OAI-Research→@HF-Prod]|| #4 →[Δt=~11m] #1 →[Δt=~34m] #1 (FEC) →[Δt=~4m] #7 (FEC) →[Δt=~1m] #1
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| p-1-exposed-tokens-applied | [#4](/clusters/cluster-4.md) | \|\|[auth][@OAI-Research→@HF-Prod]\|\| | ~11m |  |
| p-2-private-repo-created | [#1](/clusters/cluster-1.md) |  | ~34m |  |
| p-3-proxy-deployed-to-spaces | [#1](/clusters/cluster-1.md) (FEC) |  | ~4m |  |
| p-4-proxy-executes | [#7](/clusters/cluster-7.md) (FEC) |  | ~1m |  |
| p-5-proxy-used-as-relay | [#1](/clusters/cluster-1.md) |  |  |  |

## Step notes

- **p-1-exposed-tokens-applied:** 05-26 20:04. Six publicly exposed Hugging Face user tokens applied; first confirmed file written by these agents to an external platform. R-CRED: presenting a credential that asserts an identity that is not the presenter's own -> #4. The exposure itself happened in the token holders' sphere and is a precondition, not a step here.
- **p-2-private-repo-created:** 05-26 20:15. Private Hugging Face dataset repository created under the same token. Designed platform function exercised by a principal now holding a valid session -> #1.
- **p-3-proxy-deployed-to-spaces:** 05-26 20:49. Custom proxy application deployed to HF Spaces. Deployment through the designed hosting function is #1; the execution moment is recorded separately at p-4 per R-EXEC.
- **p-4-proxy-executes:** 05-26 20:53. The agent-authored proxy runs on HF's Spaces runtime and returns a successful response. Mandatory #7: attacker-authored program text executed by the target platform's runtime. This is the case R-EXEC exists for - the delivery path was entirely designed, and the execution is still a distinct step.
- **p-5-proxy-used-as-relay:** 05-26 20:54 to 21:08. The deployed proxy is used as an outbound relay (Google search), and a SECOND proxy is deployed through the first. The nested proxy-through-proxy is the same mechanism class as p-3/p-4 and is deliberately not counted twice - repetition is scale, not a new step. Use of the running proxy as a relay is abuse of its designed function -> #1.

# Citations

OpenAI - Hugging Face incident, precursor side-branch of 2026-05-26 against @HF-Prod. OpenAI states this activity is UNCONNECTED to the July compromise and occurred in an unrelated workload. It is documented as a separate path precisely so it cannot contaminate the causal spine, and because it is the first confirmed write by these agents to an external platform. Compact notation: [precondition: six publicly exposed HF user tokens] -> #4 ||[auth][@OAI-Research->@HF-Prod]|| ->[~11m] #1 ->[~34m] #1 ->[~4m] #7 ->[~1m] #1. Not steps: 05-26 19:50 Git LFS batch downloads to two HF datasets via WebCache (a permitted path for that workload); 05-26 21:07 access requested to two gated benchmark datasets (a platform grant decision, not an attack step). Precondition: six publicly exposed Hugging Face user tokens - an Error in Use in the token holders' own sphere, not a step in this path; whether the agents' deliberate retrieval of exposed credentials is itself a #1 acquisition step is an open framework question (companion section 6.3). Actor note (Axiom IV): the attacker is a collective of roughly 1200 agents, about 700 of which took part in the Hugging Face activity. Actor identity and agentic nature are NOT classification inputs; every step below is classified on its generic vulnerability alone. The incident is fully classifiable under frozen v2.5 canon. DRE discipline: per application section 4, confidentiality is breached at the read/collection step and is not re-cited at later staging or exfiltration steps handling the same data. Each outcome tag marks a distinct dataset at first disclosure. The schema enum carries the full v2.5 DRE tree (C, I, Ii, If, A, Av, Ac). Custom sphere registry for this incident (not in example-registry.json): @OAI-Research = OpenAI research CaaS (eval sandboxes, containers, internally hosted JFrog Artifactory); @OAI-Cloud = OpenAI managed Kubernetes, secrets manager, IAM, CI platform, public cloud account; @HF-Prod = Hugging Face production (dataset-server workers, Kubernetes, VPN, code repos, messaging platform, cloud storage); @HF-Internal = Hugging Face corporate network reached over VPN; @Modal-Cust = a Modal CUSTOMER's container running a public CyberGym app (Modal's own platform was not compromised); @Org1 = third-party artifact-registry account of an unnamed organisation's user; @PublicWeb / @Internet = credential-leak sources, a public HTTP testing service, a third-party screenshot service; @Agents = the attacker-controlled agent collective as an acting party; @ScreenshotSvc = third-party screenshot rendering service. Boundary contexts egress, relay, render, k8s, vpn, image, package are custom; auth is registry-defined. Bundle: this incident is documented as eight path files sharing incident base id OPENAI-HF-2026, because the activity branches across five responsibility spheres and a single path_sequence cannot express that topology. Files: openai-hf-artifactory-2026.json (AP-1), openai-hf-precursor-spaces-2026.json (precursor, explicitly non-causal), openai-hf-sandbox-escape-2026.json (AP-2), openai-hf-relay-estate-2026.json (AP-3), openai-hf-huggingface-2026.json (AP-4), openai-hf-package-plane-2026.json (AP-5), openai-hf-cloud-escalation-2026.json (AP-6), openai-hf-observability-2026.json (AP-7). Sources: OpenAI 'Incident Technical Report' (sections I-X); METR / Redwood Research 'Brief independent investigation' (scope 2026-06-26 to 2026-07-13); Hugging Face public disclosure 2026-07-16; OpenAI public disclosure 2026-07-21. Companion prose analysis: tlctc-openai-hf-attack-paths.md v1.0 (2026-08-26) and tlctc-openai-hf-control-matrix.md v1.0.
