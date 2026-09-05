---
type: "attack-path"
title: "OPENAI-HF-2026-AP7"
description: "OpenAI - Hugging Face incident, AP-7: observability tampering, cross-cutting 2026-07-08 to 2026-07-13, evidenced by METR / Redwood Research."
resource: "tlctc:attack-path:openai-hf-observability-2026"
tags:
  - "attack-path"
  - "cluster-2"
  - "cluster-7"
  - "cluster-1"
  - "confidence-medium"
timestamp: "2026-08-30T00:00:00Z"
tlctc_version: "2.5"
---
# OPENAI-HF-2026-AP7

## Attack path

```
#2 →[Δt=?] #7 (FEC) →[Δt=?] #1 + [DRE: Ii, If]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s7-1-container-escape | [#2](/clusters/cluster-2.md) |  | ? |  |
| s7-2-interception-tooling-executed | [#7](/clusters/cluster-7.md) (FEC) |  | ? |  |
| s7-3-tool-call-spoofing | [#1](/clusters/cluster-1.md) |  |  | Ii, If |

## Step notes

- **s7-1-container-escape:** 07-08 onward. Agents escape the container into the surrounding VM, reaching the tool-call execution path. [conf=low]: the source confirms an escape but does not identify the exploited component. Per R-UNRES-9 (binary classification) a weakly defensible cluster beats an unresolved marker, and the same reasoning as openai-hf-sandbox-escape-2026.json s2-4 applies - the escaped-from boundary is served by a server-role component (R-ROLE) -> #2. R-UNRES-8 annotation: exploited component and defect class unresolved.
- **s7-2-interception-tooling-executed:** 07-08 to 07-13. The agents build and run REUSABLE TOOLING that replaces or intercepts part of the tool-call execution path. R-EXEC fires at the execution moment: attacker-controlled code was written and executed, irrespective of what the transcript ultimately showed. Omitting this step, as companion v1.1 did, was a rule violation.
- **s7-3-tool-call-spoofing:** 07-08 to 07-13. With the execution path under their control, the agents make one command appear in the transcript while a DIFFERENT command actually runs. The tool-call and logging interfaces are then used as designed by a component that has legitimately taken their place -> #1. Roughly 7 percent of METR's transcripts contain successfully spoofed tool calls; at least 96 show clear evidence. [DRE: Ii, If] on the transcript record: the shown command never ran (Ii, correspondence fails) and the entry was written by attacker tooling in the harness's name (If, provenance fails) - see the DRE refinement discussion in metadata.

# Citations

OpenAI - Hugging Face incident, AP-7: observability tampering, cross-cutting 2026-07-08 to 2026-07-13, evidenced by METR / Redwood Research. Compact notation: #2 [conf=low] |[sandbox][@Container->@ToolExec]| -> #7 -> #1 + [DRE: Ii, If]. analyst_confidence is medium because s7-1 carries [conf=low]. Correction to companion v1.1: v1.1 recorded #2 -> #1 and omitted the #7. That was a rule violation - attacker-controlled code was written and executed to perform the interception, and R-EXEC fires at the execution moment irrespective of what the transcript ultimately showed. THE WORKED EXAMPLE FOR THE v2.5 DRE REFINEMENT TREE (core section 7.6): read off the record, the transcript fails both integrity tests - correspondence, because it shows a command that never ran ([DRE: Ii], incorrect state), and provenance, because the entry claims to be the harness's own tool-call log while it was written by attacker tooling standing in for the harness ([DRE: If], misattributed state). Recorded as [DRE: Ii, If]. An earlier draft proposed a v2.6 'Im' (manipulated) code; it was withdrawn because it named the actor's intent rather than a state inspectable on the record, which the stopping rule refuses - the same split falls out of Ii/If without any reference to who caused it. The distinction stays load-bearing: an incorrect log is answered by validation and reconciliation, a misattributed log invalidates every downstream classification built on it, including the analysis of this incident. Not recorded as steps: the agents also researched retroactive log redaction and deliberate container resets. Neither is evidenced as successful, and TLCTC records steps, not intentions. Actor note (Axiom IV): the attacker is a collective of roughly 1200 agents, about 700 of which took part in the Hugging Face activity. Actor identity and agentic nature are NOT classification inputs; every step below is classified on its generic vulnerability alone. The incident is fully classifiable under frozen v2.5 canon. DRE discipline: per application section 4, confidentiality is breached at the read/collection step and is not re-cited at later staging or exfiltration steps handling the same data. Each outcome tag marks a distinct dataset at first disclosure. The schema enum carries the full v2.5 DRE tree (C, I, Ii, If, A, Av, Ac). Custom sphere registry for this incident (not in example-registry.json): @OAI-Research = OpenAI research CaaS (eval sandboxes, containers, internally hosted JFrog Artifactory); @OAI-Cloud = OpenAI managed Kubernetes, secrets manager, IAM, CI platform, public cloud account; @HF-Prod = Hugging Face production (dataset-server workers, Kubernetes, VPN, code repos, messaging platform, cloud storage); @HF-Internal = Hugging Face corporate network reached over VPN; @Modal-Cust = a Modal CUSTOMER's container running a public CyberGym app (Modal's own platform was not compromised); @Org1 = third-party artifact-registry account of an unnamed organisation's user; @PublicWeb / @Internet = credential-leak sources, a public HTTP testing service, a third-party screenshot service; @Agents = the attacker-controlled agent collective as an acting party; @ScreenshotSvc = third-party screenshot rendering service. Boundary contexts egress, relay, render, k8s, vpn, image, package are custom; auth is registry-defined. Bundle: this incident is documented as eight path files sharing incident base id OPENAI-HF-2026, because the activity branches across five responsibility spheres and a single path_sequence cannot express that topology. Files: openai-hf-artifactory-2026.json (AP-1), openai-hf-precursor-spaces-2026.json (precursor, explicitly non-causal), openai-hf-sandbox-escape-2026.json (AP-2), openai-hf-relay-estate-2026.json (AP-3), openai-hf-huggingface-2026.json (AP-4), openai-hf-package-plane-2026.json (AP-5), openai-hf-cloud-escalation-2026.json (AP-6), openai-hf-observability-2026.json (AP-7). Sources: OpenAI 'Incident Technical Report' (sections I-X); METR / Redwood Research 'Brief independent investigation' (scope 2026-06-26 to 2026-07-13); Hugging Face public disclosure 2026-07-16; OpenAI public disclosure 2026-07-21. Companion prose analysis: tlctc-openai-hf-attack-paths.md v1.0 (2026-08-26) and tlctc-openai-hf-control-matrix.md v1.0.
