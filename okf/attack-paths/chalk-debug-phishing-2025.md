---
type: "attack-path"
title: "CHALK-DEBUG-PHISHING-2025"
description: "Chalk/Debug npm phishing campaign (September 8, 2025)."
resource: "tlctc:attack-path:chalk-debug-phishing-2025"
tags:
  - "attack-path"
  - "cluster-9"
  - "cluster-4"
  - "cluster-1"
  - "cluster-10"
  - "cluster-7"
  - "confidence-high"
timestamp: "2026-03-19T00:00:00Z"
tlctc_version: "2.3"
---
# CHALK-DEBUG-PHISHING-2025

## Attack path

```
||[human][@External→@Maintainer(Qix)]|| #9 + [DRE: C] →[Δt=~3d] #4 →[Δt=instant] #1 + [DRE: I] →[Δt=~12h] ||[update][@npm⇒@Maintainer(Qix)→@Consumers]|| #10 →[Δt=instant] #1 →[Δt=instant] #7 (FEC) →[Δt=instant] #1 + [DRE: C, I]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-phishing | [#9](/clusters/cluster-9.md) | \|\|[human][@External→@Maintainer(Qix)]\|\| | ~3d | C |
| s2-credential-use | [#4](/clusters/cluster-4.md) |  | instant |  |
| s3-package-publish | [#1](/clusters/cluster-1.md) |  | ~12h | I |
| s4-trust-acceptance | [#10](/clusters/cluster-10.md) | \|\|[update][@npm⇒@Maintainer(Qix)→@Consumers]\|\| | instant |  |
| s5-install-processing | [#1](/clusters/cluster-1.md) |  | instant |  |
| s6-payload-execution | [#7](/clusters/cluster-7.md) (FEC) |  | instant |  |
| s7-browser-api-abuse | [#1](/clusters/cluster-1.md) |  |  | C, I |

## Step notes

- **s1-phishing:** Phishing email impersonating npm support, sent from domain npmjs.help (registered 3 days prior). Claimed urgent 2FA credential update required by September 10. Generic vulnerability: human psychological susceptibility — authority bias (email impersonates npm support), urgency (artificial deadline), fatigue (maintainer described 'a long week and a panicky morning'). The maintainer entered credentials on the phishing site. DRE: C — credential acquisition; enabling cluster is #9. The 3-day window between domain registration and credential compromise is a detection opportunity: domain monitoring could have flagged npmjs.help.
- **s2-credential-use:** Attacker uses stolen credentials to authenticate as Junon on the npm registry. R-CRED: credential use is always #4 regardless of acquisition method.
- **s3-package-publish:** Trojanized versions of 18+ packages (chalk, debug, and others) published via the legitimate npm publish API. The API works as designed. DRE: I — package integrity compromised.
- **s4-trust-acceptance:** Trust Acceptance Event (Update Vector / #10.1). Unlike development vector attacks, these were existing packages receiving new versions through npm's update channel. Consumers with permissive semver ranges (^x.y.z or ~x.y.z) pulled the poisoned versions as routine updates. Consumers with pinned versions or lockfile enforcement were not affected.
- **s5-install-processing:** The package manager resolves the updated version, downloads, and processes it. The resolver honored the semver range; the installer unpacked the content. Controls at this step: lockfile-enforced version pinning, registry allowlists, install sandboxing.
- **s6-payload-execution:** The malicious JavaScript executes when the consuming application runs in a browser — the browser's intended execution capability. The payload operates exclusively in browser environments. R-EXEC: FEC execution via designed mechanism.
- **s7-browser-api-abuse:** The payload hooks browser APIs (window.ethereum, fetch, XMLHttpRequest) and uses Levenshtein distance algorithms to replace cryptocurrency wallet addresses with attacker-controlled addresses across six blockchains. 280+ hardcoded fallback wallet addresses maintained. The APIs function as designed; their scope is abused. DRE: C — transaction data intercepted (Loss of Confidentiality). DRE: I — wallet addresses modified in transit (Loss of Integrity).

# Citations

Chalk/Debug npm phishing campaign (September 8, 2025). Attackers registered npmjs.help (typosquat of npmjs.com) and phished Josh Junon ('Qix'), maintainer of chalk, debug, and 16+ foundational npm packages. Stolen credentials used to publish trojanized versions with browser-targeted payload: obfuscated JavaScript hooking window.ethereum, fetch, and XMLHttpRequest to replace cryptocurrency wallet addresses across six blockchains using Levenshtein distance matching with 280+ hardcoded fallback addresses. Attack path: #9 ||[human][@External→@Maintainer(Qix)]|| →[~3d] + [DRE: C] #4 →[instant] #1 + [DRE: I] → #10 ||[update][@Maintainer(Qix)⇒@npm→@Consumers]|| →[~12h] #1 →[instant] #7 →[instant] #1 + [DRE: C, I]. Update vector (#10.1): existing packages receiving poisoned updates via permissive semver ranges. Sources: npm security advisory, Sonatype, community disclosure by Josh Junon.
