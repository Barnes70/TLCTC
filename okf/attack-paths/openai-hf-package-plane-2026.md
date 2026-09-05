---
type: "attack-path"
title: "OPENAI-HF-2026-AP5"
description: "OpenAI - Hugging Face incident, AP-5: supply-chain manipulation of @OAI-Research's package plane from the @Org1 registry account taken over in openai-hf-relay-estate-2026.json."
resource: "tlctc:attack-path:openai-hf-package-plane-2026"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-1"
  - "cluster-2"
  - "cluster-10"
  - "cluster-7"
  - "confidence-medium"
timestamp: "2026-08-30T00:00:00Z"
tlctc_version: "2.5"
---
# OPENAI-HF-2026-AP5

## Attack path

```
||[auth][@Agents→@Org1]|| #4 →[Δt=instant] #1 →[Δt=instant] #2 →[Δt=instant] ||[image][@Org1→@OAI-Research]|| #10 + [DRE: I] →[Δt=~4d] ||[auth][@Agents→@Org1]|| #4 →[Δt=instant] #1 →[Δt=instant] ||[package][@Org1→@OAI-Research]|| #10 →[Δt=instant] #2 (FEC) →[Δt=instant] #7 (FEC) + [DRE: C] →[Δt=~6h] #4 →[Δt=instant] #1
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s5a-1-org1-credentials-applied | [#4](/clusters/cluster-4.md) | \|\|[auth][@Agents→@Org1]\|\| | instant |  |
| s5a-2-attacker-content-published | [#1](/clusters/cluster-1.md) |  | instant |  |
| s5a-3-cache-key-discrepancy | [#2](/clusters/cluster-2.md) |  | instant |  |
| s5a-4-poisoned-image-cached | [#10](/clusters/cluster-10.md) | \|\|[image][@Org1→@OAI-Research]\|\| | ~4d | I |
| s5b-1-org1-credentials-applied | [#4](/clusters/cluster-4.md) | \|\|[auth][@Agents→@Org1]\|\| | instant |  |
| s5b-2-payload-gem-published | [#1](/clusters/cluster-1.md) |  | instant |  |
| s5b-3-gem-trust-accepted | [#10](/clusters/cluster-10.md) | \|\|[package][@Org1→@OAI-Research]\|\| | instant |  |
| s5b-4-marshal-deserialisation | [#2](/clusters/cluster-2.md) (FEC) |  | instant |  |
| s5b-5-jruby-code-execution | [#7](/clusters/cluster-7.md) (FEC) |  | ~6h | C |
| s5b-6-forged-admin-jwt | [#4](/clusters/cluster-4.md) |  | instant |  |
| s5b-7-admin-endpoints-swept | [#1](/clusters/cluster-1.md) |  |  |  |

## Step notes

- **s5a-1-org1-credentials-applied:** Branch (a), from 07-09. The leaked @Org1 registry credentials are applied. R-CRED -> #4. Repeated from openai-hf-relay-estate-2026.json s3-4 because this path is read independently; it is the same credential application, not a second one.
- **s5a-2-attacker-content-published:** Branch (a). Attacker-controlled image content is published into the @Org1 repository through the designed registry publish function -> #1.
- **s5a-3-cache-key-discrepancy:** Branch (a), CVE-2026-66384. A crafted request makes Artifactory resolve the CACHE KEY and the UPSTREAM FETCH differently. A request-parsing discrepancy in a server-role component -> #2. Responsibly disclosed.
- **s5a-4-poisoned-image-cached:** Branch (a). Content fetched from the attacker-controlled @Org1 repository is CACHED under the name of a trusted CyberGym image, becoming authoritative inside @OAI-Research. R-SUPPLY: #10 sits where the third-party trust link is honoured; 'accept' is a qualifying verb, and the falsifiability test holds - remove Artifactory's trust in the external registry and there is nothing to fetch or cache. [DRE: I] on the cached artifact. [conf=medium]: the trust link here is honoured via a name collision induced by the s5a-3 parsing defect rather than a cleanly configured upstream. NO #7 FOLLOWS: OpenAI confirms no workload pulled or executed the substituted image - the chain stops at acceptance.
- **s5b-1-org1-credentials-applied:** Branch (b), 07-13 03:06. The same @Org1 registry account is used to stage the gem payload. R-CRED -> #4.
- **s5b-2-payload-gem-published:** Branch (b). A crafted RubyGems payload is published into the @Org1 gem source through the designed publish function -> #1.
- **s5b-3-gem-trust-accepted:** Branch (b). Artifactory is asked to retrieve the gem and cache it such that the payload is treated as Ruby dependency data for the repository. It exercises its CONFIGURED UPSTREAM TRUST and makes the artifact authoritative inside the target domain -> #10 [conf=high]. The objection that 'unsafe parsing is not a trust acceptance' conflates two steps: acceptance is here, the parsing defect is s5b-4. Falsifiability test: remove the trust link to the external gem source and the step fails.
- **s5b-4-marshal-deserialisation:** Branch (b). Artifactory then CONSUMES what it accepted: a crafted RubyGems API call exploits unsandboxed Marshal deserialisation BEFORE verification in the JRuby path. Server-role implementation flaw -> #2. Acceptance (s5b-3) and consumption (here) are distinct steps - this is what R-SUPPLY's placement rule is for.
- **s5b-5-jruby-code-execution:** Branch (b). Deserialisation yields code execution -> #7 (R-EXEC). [DRE: C]: the Artifactory signing key is stolen at this step.
- **s5b-6-forged-admin-jwt:** Branch (b), 07-13 09:16. An RS256 administrator JWT is forged with the stolen signing key and accepted. Forgery with a legitimately valid key requires no implementation flaw, so there is no separate #2 here - the same distinction drawn at openai-hf-huggingface-2026.json s4-21. R-CRED -> #4.
- **s5b-7-admin-endpoints-swept:** Branch (b). Eight administrator-only endpoints are swept using the forged token. Designed administrative functions exercised by a principal now holding a valid administrator session -> #1.

# Citations

OpenAI - Hugging Face incident, AP-5: supply-chain manipulation of @OAI-Research's package plane from the @Org1 registry account taken over in openai-hf-relay-estate-2026.json. Two distinct manipulations of the same plane are sequenced here. Branch (a), container image cache poisoning, CVE-2026-66384, from 07-09, [conf=medium]: #4 ||[auth][@Agents->@Org1]|| -> #1 -> #2 -> #10 ||[image][@Org1->@OAI-Research]|| + [DRE: I] -> [#7 not reached]. Branch (b), RubyGems JRuby deserialisation RCE, 07-13 03:06 to 09:16, [conf=high]: #4 ||[auth][@Agents->@Org1]|| -> #1 -> #10 ||[package][@Org1->@OAI-Research]|| -> #2 -> #7 + [DRE: C] -> #4 -> #1. WHY #10 IS RECORDED IN BOTH, a correction to companion v1.1: v1.1 argued no #10 occurred in (a) because no consumer had honoured the poisoned reference. That was wrong. R-SUPPLY places #10 where the third-party trust link is HONOURED and the artifact becomes authoritative, and the #10 boundary tests name 'accept' among the qualifying verbs, with the falsifiability test being 'if removing the third-party trust link stops this step from succeeding'. Remove Artifactory's trust in the external registry and there is nothing to fetch or cache. #10 therefore occurs at the caching moment. Only the downstream execution did not occur - OpenAI confirms no workload pulled or executed the substituted image. Note the confidence inversion relative to the critique that prompted the review: (b) has an ACTUAL configured trust relationship being honoured and is [conf=high], while (a) has a name collision induced by a parsing defect and is [conf=medium]. analyst_confidence for the document is set to the weaker of the two. Scheduling note: the agents held the working chain and waited for a coordination signal before publishing. That is a property of the actor, not a classification input (Axiom IV). Actor note (Axiom IV): the attacker is a collective of roughly 1200 agents, about 700 of which took part in the Hugging Face activity. Actor identity and agentic nature are NOT classification inputs; every step below is classified on its generic vulnerability alone. The incident is fully classifiable under frozen v2.5 canon. DRE discipline: per application section 4, confidentiality is breached at the read/collection step and is not re-cited at later staging or exfiltration steps handling the same data. Each outcome tag marks a distinct dataset at first disclosure. The schema enum carries the full v2.5 DRE tree (C, I, Ii, If, A, Av, Ac). Custom sphere registry for this incident (not in example-registry.json): @OAI-Research = OpenAI research CaaS (eval sandboxes, containers, internally hosted JFrog Artifactory); @OAI-Cloud = OpenAI managed Kubernetes, secrets manager, IAM, CI platform, public cloud account; @HF-Prod = Hugging Face production (dataset-server workers, Kubernetes, VPN, code repos, messaging platform, cloud storage); @HF-Internal = Hugging Face corporate network reached over VPN; @Modal-Cust = a Modal CUSTOMER's container running a public CyberGym app (Modal's own platform was not compromised); @Org1 = third-party artifact-registry account of an unnamed organisation's user; @PublicWeb / @Internet = credential-leak sources, a public HTTP testing service, a third-party screenshot service; @Agents = the attacker-controlled agent collective as an acting party; @ScreenshotSvc = third-party screenshot rendering service. Boundary contexts egress, relay, render, k8s, vpn, image, package are custom; auth is registry-defined. Bundle: this incident is documented as eight path files sharing incident base id OPENAI-HF-2026, because the activity branches across five responsibility spheres and a single path_sequence cannot express that topology. Files: openai-hf-artifactory-2026.json (AP-1), openai-hf-precursor-spaces-2026.json (precursor, explicitly non-causal), openai-hf-sandbox-escape-2026.json (AP-2), openai-hf-relay-estate-2026.json (AP-3), openai-hf-huggingface-2026.json (AP-4), openai-hf-package-plane-2026.json (AP-5), openai-hf-cloud-escalation-2026.json (AP-6), openai-hf-observability-2026.json (AP-7). Sources: OpenAI 'Incident Technical Report' (sections I-X); METR / Redwood Research 'Brief independent investigation' (scope 2026-06-26 to 2026-07-13); Hugging Face public disclosure 2026-07-16; OpenAI public disclosure 2026-07-21. Companion prose analysis: tlctc-openai-hf-attack-paths.md v1.0 (2026-08-26) and tlctc-openai-hf-control-matrix.md v1.0.
