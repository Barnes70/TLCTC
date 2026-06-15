---
type: "attack-path"
title: "S1NGULARITY-NX-2025"
description: "S1ngularity / Nx monorepo tool supply chain compromise (August 26, 2025)."
resource: "tlctc:attack-path:s1ngularity-nx-2025"
tags:
  - "attack-path"
  - "cluster-1"
  - "cluster-7"
  - "cluster-4"
  - "cluster-10"
  - "confidence-high"
timestamp: "2026-03-19T00:00:00Z"
tlctc_version: "2.1"
---
# S1NGULARITY-NX-2025

## Attack path

```
#1 →[Δt=instant] #7 (FEC) + [DRE: C] →[Δt=~5m] #4 →[Δt=instant] #1 + [DRE: I] →[Δt=~1d] ||[dev][@npm⇒@Nrwl(Nx)→@Consumers]|| #10 →[Δt=instant] #1 →[Δt=instant] #7 (FEC) →[Δt=instant] #1 + [DRE: C] →[Δt=instant] #7 (FEC) →[Δt=instant] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-ci-workflow-abuse | [#1](/clusters/cluster-1.md) |  | instant |  |
| s2-payload-execution-ci | [#7](/clusters/cluster-7.md) (FEC) |  | ~5m | C |
| s3-token-use | [#4](/clusters/cluster-4.md) |  | instant |  |
| s4-package-publish | [#1](/clusters/cluster-1.md) |  | ~1d | I |
| s5-trust-acceptance | [#10](/clusters/cluster-10.md) | \|\|[dev][@npm⇒@Nrwl(Nx)→@Consumers]\|\| | instant |  |
| s6-install-processing | [#1](/clusters/cluster-1.md) |  | instant |  |
| s7-postinstall-execution | [#7](/clusters/cluster-7.md) (FEC) |  | instant |  |
| s8-credential-sweep | [#1](/clusters/cluster-1.md) |  | instant | C |
| s9-secondary-tool-execution | [#7](/clusters/cluster-7.md) (FEC) |  | instant |  |
| s10-exfiltration | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-ci-workflow-abuse:** Attacker submits a pull request — a legitimate GitHub function. The pull_request_target workflow is designed to run with base-repo privileges. The failure is that the workflow's scope was insufficiently restricted: it permitted untrusted PR code to execute with access to secrets. No bug, no exploit — the CI system is doing what it was configured to do. The excessive scope of a legitimate function is the generic vulnerability.
- **s2-payload-execution-ci:** The CI pipeline executes the attacker's code via GitHub Actions' intended execution capability. Foreign code, designed mechanism, R-EXEC. The payload extracts the npm publishing token. DRE: C — credential acquisition; the enabling cluster is #7.
- **s3-token-use:** Attacker uses the stolen npm token to authenticate as the Nx maintainer. R-CRED: credential use is always #4 regardless of acquisition method.
- **s4-package-publish:** Attacker invokes npm's legitimate publish command to push trojanized versions of nx and related packages. The publish API works as designed. DRE: I — package integrity compromised.
- **s5-trust-acceptance:** Trust Acceptance Event (Development Vector / #10.2). Consumers pull the trojanized Nx version during dependency installation. npm serves as transit infrastructure with its own control surface (abuse detection, provenance checking). Boundary test: if the consumer had no dependency on Nx, the attack would not reach them.
- **s6-install-processing:** The consumer's package manager resolves, downloads, unpacks, and processes the package — preparing the lifecycle hook environment. Controls at this step: namespace restrictions, registry allowlists, install sandboxing, --ignore-scripts.
- **s7-postinstall-execution:** The postinstall script fires. QUIETVAULT executes on the consumer's machine. R-EXEC: FEC execution via designed lifecycle hook mechanism.
- **s8-credential-sweep:** The payload uses standard filesystem APIs and environment variable access to harvest credentials and tokens (.npmrc, .gitconfig, AWS credential files, GCP JSON keys). Data stays data — no foreign code introduced at this step. DRE: C.
- **s9-secondary-tool-execution:** QUIETVAULT downloads and executes TruffleHog (or, in some instances, weaponizes an LLM coding assistant already present on the victim's machine) for deeper credential scanning. R-EXEC: separate #7 step. TruffleHog and the LLM are legitimate tools, but the malware's act of downloading/invoking them constitutes a foreign-code event. The LLM variant is notable — the AI tool's code execution capability is directed by the malware's orchestration script.
- **s10-exfiltration:** Exfiltration via legitimate GitHub APIs: the malware creates a public repository and commits the stolen credential data. The APIs function as designed; their scope is abused. DRE: C.

# Citations

S1ngularity / Nx monorepo tool supply chain compromise (August 26, 2025). A pull_request_target GitHub Actions workflow ran attacker-submitted PR code in the base repo's security context, exposing the npm publishing token. Trojanized versions of nx and related packages were published. The QUIETVAULT payload harvested credentials, downloaded TruffleHog, and — notably — weaponized an LLM coding assistant already present on victims' machines for deeper credential scanning. Exfiltrated data was committed to a public GitHub repository. Attack path: #1 →[instant] #7 + [DRE: C] →[~5m] #4 →[instant] #1 + [DRE: I] → #10 ||[dev][@Nrwl(Nx)⇒@npm→@Consumers]|| →[instant] #1 →[instant] #7 →[instant] #1 + [DRE: C] →[instant] #7 →[instant] #1 + [DRE: C]. Development vector (#10.2): consumers pulled trojanized versions during dependency installation. Velocity profile: CI compromise to publication in minutes; consumer exposure hours to days; consumer-side exploitation near-instantaneous. Sources: Sysdig TRT, Palo Alto Unit 42, ReversingLabs, Nx post-mortem disclosure.
