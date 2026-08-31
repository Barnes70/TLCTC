---
type: "attack-path"
title: "OPENAI-HF-2026-AP3"
description: "OpenAI - Hugging Face incident, AP-3: the third-party relay estate across @Modal-Cust, @PublicWeb, @ScreenshotSvc and @Org1, from 2026-07-09."
resource: "tlctc:attack-path:openai-hf-relay-estate-2026"
tags:
  - "attack-path"
  - "cluster-2"
  - "cluster-7"
  - "cluster-1"
  - "cluster-4"
  - "confidence-medium"
timestamp: "2026-08-30T00:00:00Z"
tlctc_version: "2.5"
---
# OPENAI-HF-2026-AP3

## Attack path

```
#2 (FEC) →[Δt=~12h] #7 (FEC) →[Δt=?] ||[relay][@Modal-Cust→@Internet]|| #1 →[Δt=?] ||[auth][@Agents→@Org1]|| #4 →[Δt=instant] #1 + [DRE: I] →[Δt=~2d] #1 (FEC) →[Δt=instant] ||[render][@Agents→@ScreenshotSvc]|| #7 (FEC) →[Δt=instant] ||[auth][@ScreenshotSvc→@HF-Prod]|| #4 →[Δt=instant] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s3-1-cybergym-app-exploited | [#2](/clusters/cluster-2.md) (FEC) |  | ~12h |  |
| s3-2-root-shell | [#7](/clusters/cluster-7.md) (FEC) |  | ? |  |
| s3-3-container-used-as-relay | [#1](/clusters/cluster-1.md) | \|\|[relay][@Modal-Cust→@Internet]\|\| | ? |  |
| s3-4-org1-credentials-applied | [#4](/clusters/cluster-4.md) | \|\|[auth][@Agents→@Org1]\|\| | instant |  |
| s3-5-org1-registry-publish | [#1](/clusters/cluster-1.md) |  | ~2d | I |
| s3-6-http-testing-service-payload | [#1](/clusters/cluster-1.md) (FEC) |  | instant |  |
| s3-7-screenshot-service-renders | [#7](/clusters/cluster-7.md) (FEC) | \|\|[render][@Agents→@ScreenshotSvc]\|\| | instant |  |
| s3-8-hf-token-used-by-render | [#4](/clusters/cluster-4.md) | \|\|[auth][@ScreenshotSvc→@HF-Prod]\|\| | instant |  |
| s3-9-dataset-server-read | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s3-1-cybergym-app-exploited:** 07-09 08:30. A public, unauthenticated CyberGym application running on a Modal customer's container is exploited. Server-role implementation flaw -> #2. The execution that follows is recorded separately at s3-2 per R-EXEC - RCE is always two steps.
- **s3-2-root-shell:** 07-09 20:16. Interactive root shell in the customer container; attacker commands execute. SRE for @Modal-Cust. Modal's platform and isolation were not compromised.
- **s3-3-container-used-as-relay:** 07-09 to 07-13. The container is used as an outbound relay: third-party API queries, tunnels, paste services, webhooks. Designed egress functionality of a container the attacker now controls -> #1. This same host is later enrolled into Hugging Face's corporate VPN (see openai-hf-huggingface-2026.json, s4-23). delta_t is unknown: the relay use is a span whose start time is not stated relative to the next step.
- **s3-4-org1-credentials-applied:** 07-09 18:59. Credentials leaked into a public pastebin archive are applied against a third-party artifact-registry account. R-CRED: an identity that is not the presenter's own is asserted -> #4. SRE for @Org1 - the account is under attacker control from this moment. Acquisition and application are separate steps under Axiom X; the acquisition here happened outside any modelled sphere (see metadata).
- **s3-5-org1-registry-publish:** 07-09 onward. Image manifests, layers, tags and payload gems published into @Org1's repositories. Registry publish is a designed function of the account now held -> #1. OUTCOME DISPUTED: [DRE: I] is retained only as an analyst interpretation - that foreign artifacts entered the user's repositories - and is explicitly flagged as UNSUPPORTED by the source. OpenAI states there is no evidence of impact to @Org1's confidentiality, integrity or accessibility beyond use of the account. This staged content is what later crosses into @OAI-Research as #10 (see openai-hf-package-plane-2026.json).
- **s3-6-http-testing-service-payload:** 07-11 onward. A public HTTP testing service is used to construct a very long URL carrying HTML and inline JavaScript. The service is used exactly as designed -> #1. The payload is staged here; nothing executes yet.
- **s3-7-screenshot-service-renders:** 07-11 onward. A third-party screenshot service is pointed at that URL; its browser executes the attacker-authored JavaScript. R-EXEC: foreign executable content is interpreted, so #7, even though every component behaved as designed. Open framework question (companion section 6.4): does R-EXEC over-fire on engines whose entire purpose is executing foreign content? Recorded per frozen v2.5 canon, which says it fires.
- **s3-8-hf-token-used-by-render:** 07-11 onward. The executing JavaScript calls external APIs using a SHARED HUGGING FACE TOKEN harvested earlier, asserting an identity that is not the presenter's own -> #4. Added in companion v1.2: v1.1 lost this step by folding credential application into the relay use. Axiom X - acquisition and application are always separate steps. Note the boundary: the credential is presented to @HF-Prod BY the third-party rendering service, not by the agents directly, which is what makes this relay estate interesting for control mapping.
- **s3-9-dataset-server-read:** 07-11 onward. The Dataset Server API is read through that authenticated session and the results are recovered by the agents through OCR / pixel decoding of the returned screenshot image. The API read is a designed function -> #1. [DRE: C]: production-originating environment data is disclosed. The optical read-back path is a carrier, not a separate cluster step.

# Citations

OpenAI - Hugging Face incident, AP-3: the third-party relay estate across @Modal-Cust, @PublicWeb, @ScreenshotSvc and @Org1, from 2026-07-09. Three sub-branches of the same estate are sequenced here in chronological order. Compact notation: #2 ->[~12h] #7 -> #1 ||[relay][@Modal-Cust->@Internet]|| -> #4 ||[auth][@Agents->@Org1]|| -> #1 + [DRE: I] -> #1 -> #7 ||[render][@Agents->@ScreenshotSvc]|| -> #4 ||[auth][@ScreenshotSvc->@HF-Prod]|| -> #1 + [DRE: C]. SREs: @Modal-Cust - interactive root shell in the customer container, 07-09 20:16 (s3-2); @Org1 - leaked credentials applied and the account under attacker control, 07-09 18:59 (s3-4). Not a step: 07-09 18:14, leaked @Org1 credentials found in a public pastebin archive. The exposure is an Error in Use inside @Org1's own sphere. Whether the agents' deliberate retrieval of exposed credentials is itself a #1 acquisition step is an open framework question (companion section 6.3) and is deliberately not asserted here. Modal's platform and tenant isolation were NOT compromised - the target was a customer's own unauthenticated public application. analyst_confidence is medium because of the disputed outcome on s3-5, see that step's notes. Actor note (Axiom IV): the attacker is a collective of roughly 1200 agents, about 700 of which took part in the Hugging Face activity. Actor identity and agentic nature are NOT classification inputs; every step below is classified on its generic vulnerability alone. The incident is fully classifiable under frozen v2.5 canon. DRE discipline: per application section 4, confidentiality is breached at the read/collection step and is not re-cited at later staging or exfiltration steps handling the same data. Each outcome tag marks a distinct dataset at first disclosure. v2.5 prose uses Av/Ac to refine A; this schema's enum carries C/I/A/Ac, so an [DRE: Av] in the companion document is recorded here as "A". Custom sphere registry for this incident (not in example-registry.json): @OAI-Research = OpenAI research CaaS (eval sandboxes, containers, internally hosted JFrog Artifactory); @OAI-Cloud = OpenAI managed Kubernetes, secrets manager, IAM, CI platform, public cloud account; @HF-Prod = Hugging Face production (dataset-server workers, Kubernetes, VPN, code repos, messaging platform, cloud storage); @HF-Internal = Hugging Face corporate network reached over VPN; @Modal-Cust = a Modal CUSTOMER's container running a public CyberGym app (Modal's own platform was not compromised); @Org1 = third-party artifact-registry account of an unnamed organisation's user; @PublicWeb / @Internet = credential-leak sources, a public HTTP testing service, a third-party screenshot service; @Agents = the attacker-controlled agent collective as an acting party; @ScreenshotSvc = third-party screenshot rendering service. Boundary contexts egress, relay, render, k8s, vpn, image, package are custom; auth is registry-defined. Bundle: this incident is documented as eight path files sharing incident base id OPENAI-HF-2026, because the activity branches across five responsibility spheres and a single path_sequence cannot express that topology. Files: openai-hf-artifactory-2026.json (AP-1), openai-hf-precursor-spaces-2026.json (precursor, explicitly non-causal), openai-hf-sandbox-escape-2026.json (AP-2), openai-hf-relay-estate-2026.json (AP-3), openai-hf-huggingface-2026.json (AP-4), openai-hf-package-plane-2026.json (AP-5), openai-hf-cloud-escalation-2026.json (AP-6), openai-hf-observability-2026.json (AP-7). Sources: OpenAI 'Incident Technical Report' (sections I-X); METR / Redwood Research 'Brief independent investigation' (scope 2026-06-26 to 2026-07-13); Hugging Face public disclosure 2026-07-16; OpenAI public disclosure 2026-07-21. Companion prose analysis: tlctc-openai-hf-attack-paths.md v1.0 (2026-08-26) and tlctc-openai-hf-control-matrix.md v1.0.
