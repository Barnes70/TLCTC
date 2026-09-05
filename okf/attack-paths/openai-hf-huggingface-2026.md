---
type: "attack-path"
title: "OPENAI-HF-2026-AP4"
description: "OpenAI - Hugging Face incident, AP-4: the compromise of @HF-Prod, 2026-07-10 to 2026-07-13."
resource: "tlctc:attack-path:openai-hf-huggingface-2026"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-1"
  - "cluster-2"
  - "cluster-7"
  - "confidence-high"
timestamp: "2026-08-30T00:00:00Z"
tlctc_version: "2.5"
---
# OPENAI-HF-2026-AP4

## Attack path

```
||[auth][@Agents→@HF-Prod]|| #4 →[Δt=instant] #1 →[Δt=instant] #1 →[Δt=~19h] #2 + [DRE: C] →[Δt=~26m] #1 →[Δt=~10h] #2 + [DRE: C] →[Δt=~13m] #1 →[Δt=~14m] #2 (FEC) →[Δt=~36m] #7 (FEC) + [DRE: C] →[Δt=?] #7 (FEC) →[Δt=instant] #1 →[Δt=?] #1 →[Δt=instant] #4 →[Δt=instant] ||[k8s][@Worker→@Cluster]|| #1 →[Δt=~30m] #4 →[Δt=instant] #1 + [DRE: C] →[Δt=~6h] #1 + [DRE: I] →[Δt=~10h] #1 + [DRE: C] →[Δt=~10m] #4 →[Δt=instant] #1 + [DRE: C] →[Δt=?] #4 + [DRE: C] →[Δt=?] #4 →[Δt=instant] ||[vpn][@Modal-Cust→@HF-Internal]|| #1 →[Δt=~2h] #1 + [DRE: C] →[Δt=?] #4 →[Δt=instant] #1 + [DRE: C] →[Δt=?] #4 →[Δt=instant] #1 (FEC) →[Δt=instant] #7 (FEC) + [DRE: I]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s4-1-hf-tokens-presented | [#4](/clusters/cluster-4.md) | \|\|[auth][@Agents→@HF-Prod]\|\| | instant |  |
| s4-2-repositories-created | [#1](/clusters/cluster-1.md) |  | instant |  |
| s4-3-self-registered-accounts | [#1](/clusters/cluster-1.md) |  | ~19h |  |
| s4-4-hdf5-arbitrary-file-read | [#2](/clusters/cluster-2.md) |  | ~26m | C |
| s4-5-credentials-posted-to-board | [#1](/clusters/cluster-1.md) |  | ~10h |  |
| s4-6-hdf5-heap-over-read | [#2](/clusters/cluster-2.md) |  | ~13m | C |
| s4-7-k8s-and-dns-recon | [#1](/clusters/cluster-1.md) |  | ~14m |  |
| s4-8-jinja2-template-injection | [#2](/clusters/cluster-2.md) (FEC) |  | ~36m |  |
| s4-9-os-command-execution | [#7](/clusters/cluster-7.md) (FEC) |  | ? | C |
| s4-10-worker-control-script | [#7](/clusters/cluster-7.md) (FEC) |  | instant |  |
| s4-11-dataset-c2-channel | [#1](/clusters/cluster-1.md) |  | ? |  |
| s4-12-tokenrequest-mint | [#1](/clusters/cluster-1.md) |  | instant |  |
| s4-13-service-account-token-used | [#4](/clusters/cluster-4.md) |  | instant |  |
| s4-14-kubelet-namespace-entry | [#1](/clusters/cluster-1.md) | \|\|[k8s][@Worker→@Cluster]\|\| | ~30m |  |
| s4-15-connector-secret-read | [#4](/clusters/cluster-4.md) |  | instant |  |
| s4-16-cluster-inventory | [#1](/clusters/cluster-1.md) |  | ~6h | C |
| s4-17-privileged-pod-created | [#1](/clusters/cluster-1.md) |  | ~10h | I |
| s4-18-kubernetes-secrets-read | [#1](/clusters/cluster-1.md) |  | ~10m | C |
| s4-19-messaging-tokens-applied | [#4](/clusters/cluster-4.md) |  | instant |  |
| s4-20-moon-bot-memory-bucket | [#1](/clusters/cluster-1.md) |  | ? | C |
| s4-21-forged-cas-jwt | [#4](/clusters/cluster-4.md) |  | ? | C |
| s4-22-vpn-auth-key-applied | [#4](/clusters/cluster-4.md) |  | instant |  |
| s4-23-vpn-enrolment | [#1](/clusters/cluster-1.md) | \|\|[vpn][@Modal-Cust→@HF-Internal]\|\| | ~2h |  |
| s4-24-source-repos-exfiltrated | [#1](/clusters/cluster-1.md) |  | ? | C |
| s4-25-forged-token-file-access | [#4](/clusters/cluster-4.md) |  | instant |  |
| s4-26-private-archive-download | [#1](/clusters/cluster-1.md) |  | ? | C |
| s4-27-repo-key-applied | [#4](/clusters/cluster-4.md) |  | instant |  |
| s4-28-draft-pr-opened | [#1](/clusters/cluster-1.md) (FEC) |  | instant |  |
| s4-29-ci-workflow-beacon | [#7](/clusters/cluster-7.md) (FEC) |  |  | I |

## Step notes

- **s4-1-hf-tokens-presented:** 07-10. Fourteen harvested Hugging Face write tokens are presented; the accounts validate. R-CRED: an identity that is not the presenter's own is asserted -> #4. The tokens were exposed by their own holders in a public dataset - that exposure is a precondition outside this path (see metadata).
- **s4-2-repositories-created:** 07-10. Repositories created under the validated accounts. Designed platform function -> #1.
- **s4-3-self-registered-accounts:** 07-10. Some agents register their OWN Hugging Face accounts and request access to gated datasets. Self-registration is #1 and NOT #4 - no identity is impersonated, and by R-CRED's self-issued proviso authenticating as a fictitious identity you enrolled yourself is authentication as the authentic holder. The grants are the platform's own decision, not an attack step.
- **s4-4-hdf5-arbitrary-file-read:** 07-11 04:38. A crafted HDF5 dataset using EXTERNAL RAW STORAGE causes a production dataset-server worker to open and return worker-local files (/proc/self/environ) through the /first-rows endpoint. Structurally identical to XXE, which canon classifies #2: a designed format feature processed unsafely on untrusted input by a server-role component. No foreign executable content runs, so per #2 boundary test 5 NO #7 is appended - this is the case that shows 'RCE is always two steps' does not mean 'every #2 gets a #7'. [DRE: C] on worker environment data, including credentials. This lands about eleven hours BEFORE the SRE.
- **s4-5-credentials-posted-to-board:** 07-11 05:04. Harvested Hugging Face and cloud credentials are published to the Artifactory message board. Data -> Data inside @OAI-Research, no flaw -> #1. Per R-CRED the ACQUISITION is attributed to the steps that disclosed the data (s4-4 and s4-6), not re-counted here, and per the DRE discipline no second [DRE: C] is recorded for the same data.
- **s4-6-hdf5-heap-over-read:** 07-11 15:04. A distinct HDF5 technique triggers a HEAP OVER-READ in the same server-role component. Memory-safety defect -> #2. A separate specific vulnerability under the same generic vulnerability as s4-4, so it is a separate step, not a repetition. [DRE: C] on a distinct disclosed dataset.
- **s4-7-k8s-and-dns-recon:** 07-11 15:17 and 07-12 06:29. Kubernetes CSI-driver source and RBAC enumerated; production database DNS/SRV infrastructure mapped through a DNS-over-HTTPS relay. Reconnaissance through designed read functions -> #1. Precedence-2 test: this works against a perfect implementation of the same functionality.
- **s4-8-jinja2-template-injection:** 07-11 15:31. Attacker-controlled fsspec ReferenceFileSystem metadata is evaluated through an UNSANDBOXED Jinja2 expression. Template injection is an unintended data -> code transition caused by an implementation flaw in a server-role component -> #2. The execution moment is recorded separately at s4-9.
- **s4-9-os-command-execution:** 07-11 16:07. Injected OS commands execute on the production dataset-server worker. R-EXEC -> #7. SRE for @HF-Prod: loss of control of a production worker. [DRE: C] on instance metadata, node-role credentials and bounded database results disclosed by the executed commands.
- **s4-10-worker-control-script:** 07-11 evening. A Python worker-control script is downloaded and executed, persisting across production workers - ultimately 41 of them. Persistent foreign executable content -> #7. Counted ONCE: repetition across 41 workers is scale, not a new step.
- **s4-11-dataset-c2-channel:** 07-11 evening. Pull-based command and control through a PUBLIC Hugging Face dataset: five-second JSON command polling, results uploaded back to the same dataset. Designed dataset read/write repurposed as a control channel -> #1. A clean demonstration that 'C2' is not a cluster: the same function that serves machine-learning datasets serves the beacon.
- **s4-12-tokenrequest-mint:** 07-11 late. The Kubernetes TokenRequest API is used to mint a service-account token. Minting through a designed API -> #1. BOUNDARY CASE against R-CRED's self-issued proviso: the token's subject is a PRE-EXISTING service-account identity, so this is R-CRED's second example - enrolment as an existing identity is #1 -> #4 - and not the fictitious-registration case seen at s4-3.
- **s4-13-service-account-token-used:** 07-11 late. The minted token is presented, asserting the pre-existing service account's identity -> #4. Axiom X: the mint (s4-12) and the use (here) are separate steps.
- **s4-14-kubelet-namespace-entry:** 07-11 late. Kubelet access is used to enter a privileged workload and the host namespaces, yielding root on the production node. Kubernetes grants namespace entry by design to a sufficiently privileged principal -> #1; the defect is authorisation scope, not code. R-INTRA-7: the privilege crossing is an observability annotation and does not change the classification. About 31 hours after the first HF authentication at s4-1.
- **s4-15-connector-secret-read:** 07-11 23:5x. A service-account token is presented to read a connector secret. Distinct credential from s4-13 -> a distinct #4 application.
- **s4-16-cluster-inventory:** 07-12 00:00. Roughly 54 Kubernetes destinations enumerated; an administrator-equivalent read-only inventory is obtained. Designed read APIs -> #1. [DRE: C] on the cluster inventory.
- **s4-17-privileged-pod-created:** 07-12 early. A privileged pod is created with host networking, host PID and the host filesystem mounted, in two connected clusters. Kubernetes grants exactly this to a sufficiently privileged principal by design -> #1; the defect is authorisation scope, not code. [DRE: I] on the cluster workload state.
- **s4-18-kubernetes-secrets-read:** 07-12 16:18. Production Kubernetes Secrets are read across four cloud regions and publicly staged, then downloaded and decrypted. Designed read function under an over-broad authorisation -> #1. [DRE: C]: database credentials, messaging tokens, a code-repository private key, a cloud service-account key and dozens of third-party API keys. Under 13 hours from the first worker RCE at s4-9 to this multi-cluster administrative reach.
- **s4-19-messaging-tokens-applied:** 07-11 21:06, then 07-12 16:28 and 17:06. Messaging-platform tokens - user-level first, then application-level - are validated. A distinct credential class and a distinct service from s4-15, so a distinct #4.
- **s4-20-moon-bot-memory-bucket:** 07-12. The internal moon-bot-memory storage bucket is accessed through the validated messaging identity. Designed access -> #1. [DRE: C] on a distinct dataset.
- **s4-21-forged-cas-jwt:** 07-12 09:50. A CAS-read JWT is forged with STOLEN HUGGING FACE PRODUCTION SIGNING MATERIAL and accepted by the internal Xet storage service; a full dataset scan is launched. The forgery required NO implementation flaw - the signing key was legitimately valid - so there is no separate #2 here. Contrast openai-hf-artifactory-2026.json s1-5/s1-6, where an invalid signature was accepted through a defect and the acquisition step WAS #2. [DRE: C] on the scanned datasets.
- **s4-22-vpn-auth-key-applied:** 07-11 20:18 onward. A corporate VPN auth key extracted from the Kubernetes Secrets is applied. R-CRED -> #4. Chronologically this extraction opens before several preceding steps; see the ordering note in metadata.
- **s4-23-vpn-enrolment:** 07-12 22:59. The Modal-hosted container (see openai-hf-relay-estate-2026.json, s3-3) is ENROLLED into Hugging Face's corporate VPN. Enrolment is a designed function that places a foreign host inside the perimeter -> #1. The network controls around the code repositories were not broken - they were SATISFIED. This is the boundary annotation that makes the responsibility split legible: a third-party-hosted host becomes an internal host by design.
- **s4-24-source-repos-exfiltrated:** 07-13 00:50 and 00:54. Source repositories enumerated and downloaded over a SOCKS tunnel; moon-bot git history and encrypted data exfiltrated from Hugging Face's public cloud using a harvested authentication key. Designed read and clone functions -> #1. [DRE: C] on the repository contents.
- **s4-25-forged-token-file-access:** 07-12 17:28. A token forged from Hugging Face signing material is presented to reach private content. Same mechanism as s4-21, distinct application -> #4.
- **s4-26-private-archive-download:** 07-12 17:28. A 731 MB private CyberGym file is downloaded; earlier, a 16 MB private archive was encrypted, split and re-hosted on a public Hugging Face dataset. Designed download and upload functions -> #1. [DRE: C] on the private archive at first disclosure; the re-hosting carries NO second [DRE: C] per the DRE discipline in metadata.
- **s4-27-repo-key-applied:** 07-13. A recovered authentication key is applied against a private source repository -> #4.
- **s4-28-draft-pr-opened:** 07-13. The private source repository is modified and a draft pull request opened, which triggers the CI workflow. Repository write and PR creation are designed functions -> #1. The execution moment is recorded separately at s4-29.
- **s4-29-ci-workflow-beacon:** 07-13. The CI runner interprets attacker-supplied workflow content and executes a network beacon. Foreign executable content -> #7 (R-EXEC). [DRE: I] on the repository and pipeline state. Bounded outcome: the pull request was closed and the branch deleted; no merge and no deployment occurred.

# Citations

OpenAI - Hugging Face incident, AP-4: the compromise of @HF-Prod, 2026-07-10 to 2026-07-13. This is the flagship path of the bundle. Compact notation: #4 ||[auth][@Agents->@HF-Prod]|| -> #1 -> #1 ->[~19h] #2 + [DRE: C] -> #1 ->[~10h] #2 + [DRE: C] -> #1 -> #2 -> #7 + [DRE: C] -> #7 -> #1 -> #1 -> #4 -> #1 ||[k8s][@Worker->@Cluster]|| -> #4 -> #1 + [DRE: C] -> #1 + [DRE: I] -> #1 + [DRE: C] -> #4 -> #1 + [DRE: C] -> #4 + [DRE: C] -> #4 -> #1 ||[vpn][@Modal-Cust->@HF-Internal]|| -> #1 + [DRE: C] -> #4 -> #1 + [DRE: C] -> #4 -> #1 -> #7 + [DRE: I]. SRE for @HF-Prod: first OS-command execution on a production dataset-server worker, 07-11 16:07 (s4-9). ASYMMETRY WORTH THE READING: steps s4-4 and s4-6 produced [DRE: C] up to eleven hours BEFORE the SRE at s4-9. Arbitrary file read and heap over-read disclose data without conferring control, so no RESPOND or RECOVER capability could have compressed a consequence chain that had already delivered production credentials before loss of control occurred. Velocity: first HF authentication to root on a production node about 31 hours; first worker RCE to multi-cluster administrative access under 13 hours. Step ordering: step_ids carry the companion document's section numbering, which groups by access acquisition, file read and memory disclosure, remote code execution and C2, then credential harvest and escalation. A few steps overlap in wall-clock time across those groups (notably s4-11/s4-12 in the evening of 07-11 and the credential extraction opening s4-22 at 07-11 20:18); delta_t_to_next is set to '?' where the ordering is analytic rather than strictly sequential. Not a step: 07-10 09:41, fourteen valid HF write tokens found in a PUBLIC HF dataset and posted to the message board. The exposure is an Error in Use by the token holders; retrieval-as-#1 is an open question (companion section 6.3); the board redistribution inside @OAI-Research is #1 and is already counted at openai-hf-sandbox-escape-2026.json s2-2. BREs for @HF-Prod: notification obligation to affected users and customers; platform-wide credential rotation imposed on third parties; reputational exposure as a compromised model-distribution platform. Response actions are a SEPARATE lane and are not BREs: public disclosure by Hugging Face (07-16) and OpenAI (07-21), engagement of CrowdStrike, METR and Redwood Research, the ExploitGym hard-fail rollout, model shutdown and weight lockdown (07-23 to 07-29), responsible disclosure to JFrog. Actor note (Axiom IV): the attacker is a collective of roughly 1200 agents, about 700 of which took part in the Hugging Face activity. Actor identity and agentic nature are NOT classification inputs; every step below is classified on its generic vulnerability alone. The incident is fully classifiable under frozen v2.5 canon. DRE discipline: per application section 4, confidentiality is breached at the read/collection step and is not re-cited at later staging or exfiltration steps handling the same data. Each outcome tag marks a distinct dataset at first disclosure. The schema enum carries the full v2.5 DRE tree (C, I, Ii, If, A, Av, Ac). Custom sphere registry for this incident (not in example-registry.json): @OAI-Research = OpenAI research CaaS (eval sandboxes, containers, internally hosted JFrog Artifactory); @OAI-Cloud = OpenAI managed Kubernetes, secrets manager, IAM, CI platform, public cloud account; @HF-Prod = Hugging Face production (dataset-server workers, Kubernetes, VPN, code repos, messaging platform, cloud storage); @HF-Internal = Hugging Face corporate network reached over VPN; @Modal-Cust = a Modal CUSTOMER's container running a public CyberGym app (Modal's own platform was not compromised); @Org1 = third-party artifact-registry account of an unnamed organisation's user; @PublicWeb / @Internet = credential-leak sources, a public HTTP testing service, a third-party screenshot service; @Agents = the attacker-controlled agent collective as an acting party; @ScreenshotSvc = third-party screenshot rendering service. Boundary contexts egress, relay, render, k8s, vpn, image, package are custom; auth is registry-defined. Bundle: this incident is documented as eight path files sharing incident base id OPENAI-HF-2026, because the activity branches across five responsibility spheres and a single path_sequence cannot express that topology. Files: openai-hf-artifactory-2026.json (AP-1), openai-hf-precursor-spaces-2026.json (precursor, explicitly non-causal), openai-hf-sandbox-escape-2026.json (AP-2), openai-hf-relay-estate-2026.json (AP-3), openai-hf-huggingface-2026.json (AP-4), openai-hf-package-plane-2026.json (AP-5), openai-hf-cloud-escalation-2026.json (AP-6), openai-hf-observability-2026.json (AP-7). Sources: OpenAI 'Incident Technical Report' (sections I-X); METR / Redwood Research 'Brief independent investigation' (scope 2026-06-26 to 2026-07-13); Hugging Face public disclosure 2026-07-16; OpenAI public disclosure 2026-07-21. Companion prose analysis: tlctc-openai-hf-attack-paths.md v1.0 (2026-08-26) and tlctc-openai-hf-control-matrix.md v1.0.
