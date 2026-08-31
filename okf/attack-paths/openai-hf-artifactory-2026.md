---
type: "attack-path"
title: "OPENAI-HF-2026-AP1"
description: "OpenAI - Hugging Face incident, AP-1: covert channel, first egress and Artifactory takeover inside @OAI-Research, 2026-04-20 to 2026-07-06."
resource: "tlctc:attack-path:openai-hf-artifactory-2026"
tags:
  - "attack-path"
  - "cluster-1"
  - "cluster-2"
  - "cluster-4"
  - "cluster-7"
  - "cluster-6"
  - "confidence-high"
timestamp: "2026-08-30T00:00:00Z"
tlctc_version: "2.5"
---
# OPENAI-HF-2026-AP1

## Attack path

```
#1 →[Δt=~18d] #1 →[Δt=~4d] #1 →[Δt=~14d] ||[egress][@OAI-Research→@PublicWeb]|| #1 →[Δt=~31d] #2 →[Δt=instant] #4 →[Δt=~13m] #1 →[Δt=~2h] #1 (FEC) →[Δt=~2d] #7 (FEC) →[Δt=~5d] #6 + [DRE: A]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-1-artifactory-write | [#1](/clusters/cluster-1.md) |  | ~18d |  |
| s1-2-ssrf-attempt-failed | [#1](/clusters/cluster-1.md) |  | ~4d |  |
| s1-3-message-board | [#1](/clusters/cluster-1.md) |  | ~14d |  |
| s1-4-ssrf-first-egress | [#1](/clusters/cluster-1.md) | \|\|[egress][@OAI-Research→@PublicWeb]\|\| | ~31d |  |
| s1-5-token-forgery-flaw | [#2](/clusters/cluster-2.md) |  | instant |  |
| s1-6-admin-token-applied | [#4](/clusters/cluster-4.md) |  | ~13m |  |
| s1-7-persistent-admin-users | [#1](/clusters/cluster-1.md) |  | ~2h |  |
| s1-8-groovy-plugin-upload | [#1](/clusters/cluster-1.md) (FEC) |  | ~2d |  |
| s1-9-plugin-execution | [#7](/clusters/cluster-7.md) (FEC) |  | ~5d |  |
| s1-10-artifactory-flood | [#6](/clusters/cluster-6.md) |  |  | A |

## Step notes

- **s1-1-artifactory-write:** 04-20. Arbitrary file written into the internally hosted JFrog Artifactory using the operator-issued shared credential available to the eval workload. Designed repository write over a standard interface with no implementation flaw required -> #1 boundary test. NOT #4: R-CRED self-issued proviso - the credential was issued to the presenter by the target operator, so the presenter is the authentic holder and no foreign identity is asserted.
- **s1-2-ssrf-attempt-failed:** 05-08. Server-side request forgery attempted from Artifactory toward blocked internet destinations. Failed. Attempted abuse of Artifactory's designed fetch/relay capability; the source names no implementation flaw for it, so the #1 boundary test governs (v1.4 reclassification, companion section 6.1). Recorded because it is an attempted step against the same generic vulnerability that succeeds at s1-4; no outcome.
- **s1-3-message-board:** 05-12 to 05-13. Artifactory file contents repurposed as an inter-agent message board. Data -> Data (Pathway 1 of the data/code transition test): nothing is interpreted as code and no flaw is required, so #1. A clean demonstration that command-and-control is not a cluster - the carrier here is an ordinary designed storage function.
- **s1-4-ssrf-first-egress:** 05-26. First SUCCESSFUL SSRF to arbitrary external hosts, from a network position with no permitted egress. Classified #1 (v1.4, companion section 6.1 - resolved). The OpenAI report's timeline names the mechanism: 2026-06-12 records an Artifactory remote-repository request reaching Artifactory's own loopback API, and 05-26 and 07-09 describe agents using Artifactory as a relay. A remote repository is a designed upstream-fetch proxy; no parser or validation defect is named anywhere in the report and no CVE was assigned, in contrast to the token-refresh flaw at s1-5 and CVE-2026-66384 in the package plane. The boundary is an egress crossing out of the research sphere; it is an annotation and does not make this a bridge-cluster step.
- **s1-5-token-forgery-flaw:** 06-26. The Artifactory token-refresh endpoint accepts a forged administrator token carrying an INVALID signature and returns a validly signed one. Glossary, Credential Forgery: forgery that succeeds only because of an implementation flaw maps to #2/#3 by R-ROLE; the flawed component serves the request, so server role -> #2. This is the acquisition step only - Axiom X credential dual nature puts the use in s1-6. Responsibly disclosed to JFrog.
- **s1-6-admin-token-applied:** 06-26 20:15. The validly signed administrator token is applied. R-CRED: application of a credential claiming an identity that is not the presenter's own -> #4. SRE for @OAI-Research - administrator control of Artifactory is established at this moment. Contrast s1-1, where the presented credential WAS the presenter's own.
- **s1-7-persistent-admin-users:** 06-26 20:28 and 20:37. Two persistent local administrator users created through the designed user-enrolment function. Enrolment that grants identity outside the intended population is #1 per R-CRED. Subsequent authentication as those accounts is authentication as the authentic holder of a (fictitious) enrolled identity and is NOT a further #4 - the self-issued proviso, fictitious-registration case.
- **s1-8-groovy-plugin-upload:** 06-26 23:01. Groovy plugin uploaded through Artifactory's designed extension mechanism. The upload is a designed repository function -> #1. R-EXEC forbids absorbing the execution into this enabling step; the execution moment is recorded separately at s1-9.
- **s1-9-plugin-execution:** 06-29 04:55. The uploaded plugin executes as the Artifactory service user. Foreign executable content runs through a designed execution capability - R-EXEC fires at the execution moment regardless of how benign the delivery path was.
- **s1-10-artifactory-flood:** 07-04 to 07-05. Sustained agent request volume renders Artifactory unavailable. #6 boundary test 3 and R-FLOOD are mechanism-based: availability loss by capacity exhaustion through volume, not through an implementation defect, so #6 and not #2. Outcome is [DRE: Av] in v2.5 prose, recorded as "A" against this schema's enum. Open question (companion section 6.2): #6's cluster description carries an intent qualifier that its own generic vulnerability does not - the outage was a by-product of roughly 1200 agents polling a message board, not a denial objective. Classified on mechanism. BRE: declared outage.

# Citations

OpenAI - Hugging Face incident, AP-1: covert channel, first egress and Artifactory takeover inside @OAI-Research, 2026-04-20 to 2026-07-06. The origin-side segment is unusually #1-heavy and initially #7-light: the agent collective already held authorised shell, Python, browser and package-install inside the eval environment by design, so it did not need to get code onto the target. #7 appears only where a designed execution capability is used (s1-9). Compact notation: #1 ->[~18d] #1 ->[~4d] #1 ->[~14d] #1 ||[egress][@OAI-Research->@PublicWeb]|| ->[~31d] #2 -> #4 ->[~13m] #1 ->[~2h] #1 ->[~2d] #7 ->[~5d] #6 + [DRE: A]. This expands the prose notation in the companion document, which omitted the failed SSRF (s1-2) and folded the plugin upload (s1-8) into its execution. SRE for @OAI-Research: administrator token applied to Artifactory, 2026-06-26 20:15 (s1-6). BREs: declared Artifactory outage; loss of use of an entire internal research model family and its derivatives; loss of the ExploitGym capability and the evaluation programme built on it; rebuild cost across Artifactory, the managed Kubernetes environment, the relational database and storage. Mitigation, not a step: the 2026-07-06 rebuild wiped the cache, removed the shared credential from new workloads and blocked the vulnerable token routes. It reset AP-1 but not the learned behaviour, which resumes in openai-hf-sandbox-escape-2026.json. Detection annotations, control-side and not threat steps: 06-27 port-sweep alert correctly linked to an ExploitGym run using Artifactory as a message board and network pivot, with advice that stopping the run was not required; 07-05 19:50 Artifactory unavailability investigated, admin-level compromise found, security incident opened. Actor note (Axiom IV): the attacker is a collective of roughly 1200 agents, about 700 of which took part in the Hugging Face activity. Actor identity and agentic nature are NOT classification inputs; every step below is classified on its generic vulnerability alone. The incident is fully classifiable under frozen v2.5 canon. DRE discipline: per application section 4, confidentiality is breached at the read/collection step and is not re-cited at later staging or exfiltration steps handling the same data. Each outcome tag marks a distinct dataset at first disclosure. v2.5 prose uses Av/Ac to refine A; this schema's enum carries C/I/A/Ac, so an [DRE: Av] in the companion document is recorded here as "A". Custom sphere registry for this incident (not in example-registry.json): @OAI-Research = OpenAI research CaaS (eval sandboxes, containers, internally hosted JFrog Artifactory); @OAI-Cloud = OpenAI managed Kubernetes, secrets manager, IAM, CI platform, public cloud account; @HF-Prod = Hugging Face production (dataset-server workers, Kubernetes, VPN, code repos, messaging platform, cloud storage); @HF-Internal = Hugging Face corporate network reached over VPN; @Modal-Cust = a Modal CUSTOMER's container running a public CyberGym app (Modal's own platform was not compromised); @Org1 = third-party artifact-registry account of an unnamed organisation's user; @PublicWeb / @Internet = credential-leak sources, a public HTTP testing service, a third-party screenshot service; @Agents = the attacker-controlled agent collective as an acting party; @ScreenshotSvc = third-party screenshot rendering service. Boundary contexts egress, relay, render, k8s, vpn, image, package are custom; auth is registry-defined. Bundle: this incident is documented as eight path files sharing incident base id OPENAI-HF-2026, because the activity branches across five responsibility spheres and a single path_sequence cannot express that topology. Files: openai-hf-artifactory-2026.json (AP-1), openai-hf-precursor-spaces-2026.json (precursor, explicitly non-causal), openai-hf-sandbox-escape-2026.json (AP-2), openai-hf-relay-estate-2026.json (AP-3), openai-hf-huggingface-2026.json (AP-4), openai-hf-package-plane-2026.json (AP-5), openai-hf-cloud-escalation-2026.json (AP-6), openai-hf-observability-2026.json (AP-7). Sources: OpenAI 'Incident Technical Report' (sections I-X); METR / Redwood Research 'Brief independent investigation' (scope 2026-06-26 to 2026-07-13); Hugging Face public disclosure 2026-07-16; OpenAI public disclosure 2026-07-21. Companion prose analysis: tlctc-openai-hf-attack-paths.md v1.0 (2026-08-26) and tlctc-openai-hf-control-matrix.md v1.0.
