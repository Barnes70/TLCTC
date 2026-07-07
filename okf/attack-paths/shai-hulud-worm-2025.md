---
type: "attack-path"
title: "SHAI-HULUD-WORM-2025"
description: "Shai-Hulud recursive npm supply chain worm (September 14 – November 2025)."
resource: "tlctc:attack-path:shai-hulud-worm-2025"
tags:
  - "attack-path"
  - "cluster-4"
  - "cluster-1"
  - "cluster-10"
  - "cluster-7"
  - "confidence-medium"
timestamp: "2026-03-19T00:00:00Z"
tlctc_version: "2.3"
---
# SHAI-HULUD-WORM-2025

## Attack path

```
#4 →[Δt=instant] #1 + [DRE: I] →[Δt=~12h] ||[update][@npm⇒@Patient0→@Victim1]|| #10 →[Δt=instant] #1 →[Δt=instant] #7 (FEC) →[Δt=instant] #1 + [DRE: C] →[Δt=instant] #7 (FEC) →[Δt=instant] #1 + [DRE: C] →[Δt=instant] #4 →[Δt=instant] #1 + [DRE: C, I] →[Δt=instant] #4 →[Δt=instant] #1 + [DRE: I] →[Δt=~12h] ||[update][@npm⇒@Victim1→@Victim2]|| #10 →[Δt=~12h] #1 + [DRE: Ac]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-initial-compromise | [#4](/clusters/cluster-4.md) |  | instant |  |
| s2-initial-publish | [#1](/clusters/cluster-1.md) |  | ~12h | I |
| s3-trust-acceptance-victim1 | [#10](/clusters/cluster-10.md) | \|\|[update][@npm⇒@Patient0→@Victim1]\|\| | instant |  |
| s4-install-processing | [#1](/clusters/cluster-1.md) |  | instant |  |
| s5-postinstall-execution | [#7](/clusters/cluster-7.md) (FEC) |  | instant |  |
| s6-credential-sweep | [#1](/clusters/cluster-1.md) |  | instant | C |
| s7-trufflehog-execution | [#7](/clusters/cluster-7.md) (FEC) |  | instant |  |
| s8-trufflehog-scan | [#1](/clusters/cluster-1.md) |  | instant | C |
| s9-github-token-use | [#4](/clusters/cluster-4.md) |  | instant |  |
| s10-github-abuse | [#1](/clusters/cluster-1.md) |  | instant | C, I |
| s11-npm-token-use | [#4](/clusters/cluster-4.md) |  | instant |  |
| s12-worm-publish | [#1](/clusters/cluster-1.md) |  | ~12h | I |
| s13-recursive-trust-acceptance | [#10](/clusters/cluster-10.md) | \|\|[update][@npm⇒@Victim1→@Victim2]\|\| | ~12h |  |
| s14-destructive-fallback | [#1](/clusters/cluster-1.md) |  |  | Ac |

## Step notes

- **s1-initial-compromise:** Initial compromise of Patient Zero (rxnt-authentication maintainer). Assessed with moderate confidence as reuse of credentials leaked during the S1ngularity campaign — making this a #4 (credential use). Alternative hypothesis: phishing (#9). The causal ambiguity is itself instructive: it shows how credential exposure (DRE: C) from one campaign becomes the entry vector for the next. R-CRED: regardless of acquisition method, credential use is always #4.
- **s2-initial-publish:** Attacker publishes trojanized rxnt-authentication v0.0.3 via the legitimate npm publish API. DRE: I — package integrity compromised.
- **s3-trust-acceptance-victim1:** Trust Acceptance Event (Update Vector / #10.1). Victim1 installs the compromised package version through the normal dependency resolution process. npm serves as transit infrastructure.
- **s4-install-processing:** The package manager resolves, downloads, unpacks, and processes the package — preparing the lifecycle hook environment.
- **s5-postinstall-execution:** The postinstall hook triggers bundle.js (3MB+). R-EXEC: first FEC execution on Victim1's machine. Shai-Hulud 2.0 escalated to preinstall execution for earlier interception.
- **s6-credential-sweep:** Filesystem credential sweep: .npmrc (npm tokens), .gitconfig (GitHub PATs), AWS credential files (~/.aws/credentials), GCP JSON service account keys. Data stays data — standard filesystem read operations. DRE: C.
- **s7-trufflehog-execution:** TruffleHog downloaded and executed for deeper secret scanning. R-EXEC: separate #7 step. That TruffleHog is itself a legitimate security tool is irrelevant — the malware's act of downloading and running it is the foreign-code event.
- **s8-trufflehog-scan:** TruffleHog scans the filesystem for secrets using its designed pattern-matching capabilities. Legitimate tool, legitimate function, abused scope. DRE: C.
- **s9-github-token-use:** Stolen GitHub tokens used to authenticate as Victim1. R-CRED: credential use is always #4.
- **s10-github-abuse:** Legitimate GitHub APIs abused to: create a public repository named 'Shai-Hulud' containing exfiltrated secrets, inject malicious GitHub Actions workflows into every accessible repository, create pull requests, and convert private repositories to public. DRE: C (secret exposure) and I (workflow injection, visibility changes).
- **s11-npm-token-use:** Stolen npm tokens used to authenticate as Victim1 on the npm registry. R-CRED: credential use is always #4. This step initiates the worm's propagation phase.
- **s12-worm-publish:** For each package Victim1 maintains, the worm: retrieves the package list, sorts by download count (maximizing blast radius), injects bundle.js into the postinstall script, and publishes a new version. Legitimate npm API, abused scope. DRE: I — integrity of all Victim1's packages compromised. This creates the recursive propagation vector.
- **s13-recursive-trust-acceptance:** Recursive Trust Acceptance Event (Update Vector / #10.1). Each newly poisoned package creates a new TAE. Victim2 trusts the packages Victim1 maintains. The attack path loops back to s4-install-processing for each new victim, creating a cyclic/fractal propagation pattern. The conventional linear model of supply chain risk fails here — each propagation layer produces new propagation layers. Total: 500+ versions across 796 packages within days. The key invariant is that each recursion generates a new #10 boundary crossing — supply chain trust is renewed at every propagation step.
- **s14-destructive-fallback:** Shai-Hulud 2.0 only: conditional destructive fallback. If exfiltration fails entirely, the worm recursively overwrites and deletes the victim's home directory using standard filesystem functions. This is #1 — the OS's delete operations are legitimate; their scope is abused. DRE: Ac — Loss of Accessibility. The system remains operational (not Loss of Availability). The files are permanently inaccessible (Loss of Accessibility). Different DRE, different recovery playbook: Availability loss calls for failover; Accessibility loss calls for backups. This step is conditional and fires only when the primary exfiltration path fails.

# Citations

Shai-Hulud recursive npm supply chain worm (September 14 – November 2025). The most structurally complex npm attack to date. Patient Zero: rxnt-authentication v0.0.3 (published September 14 at 17:58 UTC). Initial compromise assessed with moderate confidence as credentials leaked during the S1ngularity campaign (hence medium analyst_confidence), though phishing is not excluded. The payload (bundle.js, 3MB+) executed during postinstall: swept filesystem for npm tokens, GitHub PATs, AWS/GCP credentials; downloaded and executed TruffleHog; used GitHub credentials to create 'Shai-Hulud' repos, inject malicious workflows, and convert private repos to public. Critical novelty: if npm credentials were found, the worm retrieved the victim's package list sorted by download count, injected itself into each, and published new versions — making each poisoned package a new infection vector. Shai-Hulud 2.0 (November 2025) escalated to preinstall execution and added a destructive fallback (home directory wipe). This JSON models a single propagation depth. Attack path: #4 →[instant] #1 + [DRE: I] → #10 ||[update][@Patient0⇒@npm→@Victim1]|| →[~12h] #1 →[instant] #7 →[instant] #1 + [DRE: C] →[instant] #7 →[instant] #1 + [DRE: C] →[instant] #4 →[instant] #1 + [DRE: C, I] →[instant] #4 →[instant] #1 + [DRE: I] → #10 ||[update][@Victim1⇒@npm→@Victim2]|| → [RECURSIVE]. 500+ package versions across 796 packages compromised. Sources: Datadog Security Research, ArmorCode, Sonatype, Trend Micro, community disclosures.
