# Anatomy of a Worm: The 2025 npm Supply Chain Attacks Through the TLCTC Lens

**How causal decomposition turns the industry's vaguest label into operational precision.**

---

## The Problem With "Supply Chain Attack"

In September 2025, a single phishing email compromised 18 npm packages with 2.6 billion combined weekly downloads. Two weeks later, a self-replicating worm turned every infected developer into an unwitting distribution node, poisoning 500+ package versions in under four days. A month earlier, a single pull request to a CI pipeline had already stolen a publishing token and trojanized a monorepo tool used by millions.

The industry called all three incidents "supply chain attacks." That label is not wrong. It is empty.

Calling a multi-stage, multi-mechanism campaign a "supply chain attack" is like diagnosing a patient with "hospital." The patient was *in* a hospital. The diagnosis is somewhere else entirely. The label names the trust boundary the attack crossed. It says nothing about the six other mechanisms that made the crossing possible and consequential — and therefore nothing about which controls would have stopped it.

The TLCTC framework decomposes every cyber incident into a sequence of causal steps, each mapped to exactly one of ten mutually exclusive threat clusters. The resulting attack path tells you *what generic vulnerabilities were exploited*, *in what sequence*, *at what velocity*, and therefore *which controls could have broken the chain at each step*.

This post applies that decomposition to the three major 2025 npm campaigns at full analytical depth.

---

## Preamble: The npm Trust Surface and the Canonical Chain

**Why npm is structurally revealing.** npm operationalizes trust at industrial scale. Developers and CI pipelines delegate trust to package names, version ranges, lockfile state, registry metadata, maintainer accounts, provenance signals, integrity hashes, and the resolver's own logic. In TLCTC terms, these are all **trust artifacts** — and the moment a build runner or developer machine accepts one of those artifacts and integrates it into the organization's software reality is the **Trust Acceptance Event**. That is where **#10 Supply Chain Attack** fires. But #10 is only the boundary crossing. It is not a bucket that absorbs everything else.

**The canonical chain.** Once a malicious package crosses the trust boundary, two further steps almost always follow — and the industry habitually compresses them into one:

```
#10 → #1 → #7
```

- **#10** — the third-party artifact is accepted as trustworthy.
- **#1 Abuse of Functions** — the package manager resolves, downloads, unpacks, and processes the artifact. All legitimate functionality, working as designed. The attacker wins here because the defender's own tooling faithfully serves a malicious payload.
- **#7 Malware** — attacker-controlled code executes through a lifecycle hook, interpreter, or build mechanism — a designed execution capability.

The `#1` between `#10` and `#7` is not invisible infrastructure. It is a distinct causal step with its own generic vulnerability (*insufficient restriction on scope of legitimate functionality*) and its own control surface: namespace restrictions, registry allowlists, install sandboxing, `--ignore-scripts`. Those controls are structurally different from trust governance (#10) and execution control (#7). Collapsing the chain to `#10 → #7` hides the richest intervention point available to defenders.

**What npm attacks are usually *not*.** Every major 2025 npm attack needed no server-side or client-side code flaw. No buffer overflow in the registry. No parser bug in the CLI. The paths are dominated by #10, #1, #4, #7, and #9. Only when there is a genuine implementation flaw in a server-role or client-role component do #2 or #3 belong — and the control implications are completely different.

**Recurring rules referenced in the decompositions below:**

- **R-CRED** (Credential Dual Nature): Credential *acquisition* maps to the enabling cluster; credential *use* always maps to **#4 Identity Theft**.
- **R-EXEC** (Execution Granularity): Each download and execution of new foreign code from an external source constitutes a separate **#7** step.
- **#10.1 vs #10.2**: Update Vector (.1) = poisoned versions pushed through an existing package's update channel. Development Vector (.2) = malicious dependency pulled during pre-deployment dependency resolution.

**Notation reference:**

| Operator | Meaning |
|---|---|
| `#X → #Y` | Sequential: X enables Y |
| `→[Δt=value]→` | Temporal gap (attack velocity) |
| `\|\|[ctx][@A→@B]\|\|` | Inter-organizational domain boundary (v2.0) |
| `\|\|[ctx][@A⇒@T→@B]\|\|` | Transit boundary: T is intermediary infrastructure (v2.1 draft) |
| `+ [DRE: C/I/Ac/Av]` | Data Risk Event: Confidentiality / Integrity / Accessibility / Availability |

---

## Campaign 1 — S1ngularity / Nx (August 26, 2025)

### What Happened

The Nx monorepo tool's GitHub repository used a `pull_request_target` workflow — a GitHub Actions trigger that runs in the *base* repository's security context, with access to repository secrets. The workflow checked out and executed code from incoming pull requests within this privileged context. An attacker submitted a PR. The CI system ran the attacker's code with access to the npm publishing token. The attacker then published trojanized versions of `nx` and related packages. The payload (QUIETVAULT) harvested environment secrets and — in a first — weaponized an LLM coding assistant already present on victims' machines to scan for additional credentials. Exfiltrated data was committed to a public GitHub repository.

### Consolidated Attack Path

```
#1 →[0s] #7 + [DRE: C]
→[minutes] #4 →[0s] #1 + [DRE: I]
→ #10.2 ||[dev][@Nrwl(Nx)⇒@npm→@Consumers]||
→[hours-days] #1 →[0s] #7
→[0s] #1 + [DRE: C] →[0s] #7 →[0s] #1 + [DRE: C]
```

### Decomposition

**Phase A — Compromising the build pipeline** `#1 →[0s] #7 + [DRE: C]`

**#1**: The attacker submits a pull request — a legitimate GitHub function. The `pull_request_target` workflow is *designed* to run with base-repo privileges. The failure is that the workflow's scope was insufficiently restricted: it permitted untrusted PR code to execute with access to secrets. No bug, no exploit — the CI system is doing what it was configured to do. The excessive scope of a legitimate function is the generic vulnerability.

**#7**: The CI pipeline executes the attacker's code via GitHub Actions' intended execution capability. Foreign code, designed mechanism, R-EXEC. The payload extracts the npm publishing token. `+ [DRE: C]` — credential acquisition; the enabling cluster is #7.

**Phase B — Package poisoning** `#4 →[minutes] #1 + [DRE: I]`

**#4**: The attacker uses the stolen npm token to authenticate as the Nx maintainer. R-CRED: credential use.

**#1**: The attacker invokes npm's legitimate `publish` command to push trojanized versions. The publish API works as designed. `+ [DRE: I]` — package integrity compromised.

**Phase C — Trust Acceptance and consumer-side execution** `#10.2 ||[dev][@Nrwl(Nx)⇒@npm→@Consumers]|| →[hours-days] #1 →[0s] #7 →[0s] #1 + [DRE: C] →[0s] #7 →[0s] #1 + [DRE: C]`

**#10.2** (Development Vector): The Trust Acceptance Event. Consumers pull the trojanized Nx version during dependency installation. The v2.1 transit notation shows npm as intermediary with its own control surface (abuse detection, provenance checking). Boundary test: if the consumer had no dependency on Nx, the attack would not reach them.

**#1** (install processing): The consumer's package manager resolves, downloads, unpacks, and processes the package — preparing the lifecycle hook environment. Controls at this step: namespace restrictions, registry allowlists, install sandboxing.

**#7**: The `postinstall` script fires. QUIETVAULT executes.

**#1**: The payload uses standard filesystem APIs and environment variable access to harvest credentials and tokens. Data stays data. `+ [DRE: C]`.

**#7**: QUIETVAULT downloads and executes TruffleHog (or, in some instances, weaponizes an LLM coding assistant) for deeper credential scanning. R-EXEC: separate #7 step. The LLM variant is notable — the AI tool itself is legitimate, but the orchestration script that directs it is foreign code.

**#1**: Exfiltration. The malware uses legitimate GitHub APIs to create a public repository and commit the stolen data. `+ [DRE: C]`.

### Velocity Profile

Initial compromise (#1→#7) through package publication (#4→#1): minutes. Supply chain propagation to consumers: hours to days (dependent on when `npm install` runs). Consumer-side install processing and payload execution: near-instantaneous once triggered.

---

## Campaign 2 — Chalk/Debug Phishing (September 8, 2025)

### What Happened

On September 5, attackers registered the domain `npmjs.help` — a visual lookalike of `npmjs.com`. They sent phishing emails to Josh Junon ("Qix"), the maintainer of chalk, debug, and other foundational npm packages. The email impersonated npm support and claimed urgent 2FA credential updates were required by September 10. Junon, under time pressure, entered his credentials on the phishing site. The attackers authenticated as Junon and published malicious versions of 18+ packages.

The payload was sophisticated: obfuscated JavaScript operating exclusively in browser environments. It hooked `window.ethereum`, `fetch`, and `XMLHttpRequest`, used Levenshtein distance algorithms to replace cryptocurrency wallet addresses with attacker-controlled addresses across six blockchains, and maintained over 280 hardcoded fallback wallet addresses.

### Consolidated Attack Path

```
#9 →[Δt≈3d] + [DRE: C]
→[0s] #4 →[0s] #1 + [DRE: I]
→ #10.1 ||[update][@Maintainer(Qix)⇒@npm→@Consumers]||
→[hours] #1 →[0s] #7 →[0s] #1 + [DRE: C, I]
```

### Decomposition

**Phase A — Credential acquisition** `#9 →[Δt≈3d] + [DRE: C]`

**#9**: The phishing email. Generic vulnerability: human psychological susceptibility — authority bias (email impersonates npm support), urgency (deadline), fatigue (the maintainer described having "a long week and a panicky morning"). No technical vulnerability exploited. The human performed the action. `+ [DRE: C]` — credential acquisition; enabling cluster is #9.

The velocity annotation `→[Δt≈3d]` records that the phishing domain was registered three days before the maintainer fell for the phish. That window is a detection opportunity: domain monitoring could have flagged `npmjs.help`.

**Phase B — Package poisoning** `#4 →[0s] #1 + [DRE: I]`

**#4**: The attacker uses stolen credentials to authenticate as Junon. R-CRED: credential use.

**#1**: Trojanized versions of 18+ packages published via the legitimate publish API. `+ [DRE: I]`.

**Phase C — Trust Acceptance and browser-side payload** `#10.1 ||[update][@Maintainer(Qix)⇒@npm→@Consumers]|| →[hours] #1 →[0s] #7 →[0s] #1 + [DRE: C, I]`

**#10.1** (Update Vector): The Trust Acceptance Event. Unlike Campaign 1, this is #10.1: these were *existing* packages receiving new versions through npm's update channel. Consumers with permissive semver ranges pulled the poisoned versions as routine updates.

**#1** (install processing): The package manager resolves the updated version, downloads, and processes it. The resolver honored the semver range; the installer unpacked the content.

**#7**: The malicious JavaScript executes when the consuming application runs in a browser — the browser's intended execution capability.

**#1**: The payload hooks browser APIs (`window.ethereum`, `fetch`, `XMLHttpRequest`) and uses them to intercept and modify cryptocurrency transactions. The APIs function as designed; their scope is abused. `+ [DRE: C, I]` — transaction data intercepted (LoC), wallet addresses modified (LoI).

### Velocity Profile

Social engineering to credential compromise: three days. Account takeover to package publication: near-instantaneous. Consumer exposure: hours for CI/CD with permissive ranges, never for pinned versions. Browser-side payload: fires on page load.

---

## Campaign 3 — Shai-Hulud: The Recursive Supply Chain Worm (September 14 – November 2025)

### What Happened

The most structurally complex npm attack to date. Patient Zero: `rxnt-authentication` v0.0.3, published September 14 at 17:58 UTC. The initial compromise vector is assessed with moderate confidence to be credentials leaked during the S1ngularity campaign, though phishing is not excluded.

The payload (`bundle.js`, 3MB+) executed during `postinstall` and performed a cascading sequence: it swept the filesystem for npm tokens, GitHub PATs, AWS and GCP credentials; downloaded and executed TruffleHog for deeper secret scanning; used any GitHub credentials found to create a public repository named "Shai-Hulud" containing exfiltrated secrets, inject malicious GitHub Actions workflows into every accessible repository, and convert private repositories to public. Then came the critical novelty: if npm credentials were found, the worm retrieved the list of all packages the victim maintained, sorted them by download count, injected itself into each one, and published new versions. Each poisoned package became a new infection vector.

**Shai-Hulud 2.0** (November 2025) escalated further: it ran at `preinstall` time and introduced a destructive fallback — if exfiltration failed entirely, it attempted to wipe the victim's home directory.

### Consolidated Attack Path (single propagation depth)

```
(#9 | #4) →[0s] #1 + [DRE: I]
→ #10.1 ||[update][@Patient0⇒@npm→@Victim₁]||
→[hours] #1 →[0s] #7
→[0s] #1 + [DRE: C] →[0s] #7 →[0s] #1 + [DRE: C]
→[0s] #4 →[0s] #1 + [DRE: C, I]
→[0s] #4 →[0s] #1 + [DRE: I]
→ #10.1 ||[update][@Victim₁⇒@npm→@Victim₂...ₙ]||
→ [RECURSIVE]
```

### Decomposition

**Phase A — Initial compromise (Patient Zero)** `(#9 | #4) →[0s] #1 + [DRE: I]`

**#9 or #4**: The initial compromise is assessed as either phishing (#9) or reuse of credentials leaked during S1ngularity (#4). The causal ambiguity is itself instructive: it shows how credential exposure (`+ [DRE: C]`) from one campaign becomes the entry vector for the next.

**#1**: The attacker publishes a trojanized version via the legitimate publish API. `+ [DRE: I]`.

**Phase B — Trust Acceptance (Victim₁)** `#10.1 ||[update][@Patient0⇒@npm→@Victim₁]|| →[hours] #1 →[0s] #7`

**#10.1** (Update Vector): The Trust Acceptance Event. Victim₁ installs the compromised package.

**#1** (install processing): The package manager resolves, downloads, unpacks, and processes the package.

**#7**: The `postinstall` hook triggers `bundle.js`. R-EXEC: first #7 on Victim₁'s machine.

**Phase C — Local exploitation** `→[0s] #1 + [DRE: C] →[0s] #7 →[0s] #1 + [DRE: C] →[0s] #4 →[0s] #1 + [DRE: C, I]`

**#1**: Filesystem credential sweep (`.npmrc`, `.gitconfig`, AWS credential files, GCP JSON keys). Data stays data. `+ [DRE: C]`.

**#7**: TruffleHog downloaded and executed. R-EXEC: separate #7 step. That TruffleHog is itself a legitimate tool is irrelevant — the malware's act of downloading and running it is the foreign-code event.

**#1**: TruffleHog scans the filesystem. `+ [DRE: C]`.

**#4**: Stolen GitHub tokens used to authenticate as the victim. R-CRED: credential use.

**#1**: Legitimate GitHub APIs exploited to create the "Shai-Hulud" repository, commit exfiltrated data, inject workflow files, create pull requests, and convert private repositories to public. `+ [DRE: C, I]`.

**Phase D — Worm propagation** `#4 →[0s] #1 + [DRE: I] → #10.1 ||[update][@Victim₁⇒@npm→@Victim₂...ₙ]|| → [RECURSIVE]`

**#4**: Stolen npm tokens authenticate as Victim₁.

**#1**: For *each* package Victim₁ maintains, the worm injects `bundle.js` into the `postinstall` script and publishes a new version — sorted by download count to maximize blast radius. `+ [DRE: I]`.

**#10.1** (recursive): Each newly poisoned package creates a *new* Trust Acceptance Event. Victim₂ trusts the package Victim₁ maintains. Victim₃ trusts Victim₂'s packages. The loop returns to Phase B. At every hop, the canonical `#10.1 → #1 → #7` chain fires again.

This is the structural novelty. Traditional attack paths are acyclic. Shai-Hulud's is cyclic: Phase D feeds back into Phase B for each new victim. The `[RECURSIVE]` annotation marks this. The key invariant is that each recursion generates a new `#10.1` boundary crossing — the supply chain trust relationship is renewed at every propagation step.

**Phase E — Destructive fallback (2.0 only)** `#1 + [DRE: Ac]`

If exfiltration fails, the worm recursively overwrites and deletes the victim's home directory using standard filesystem functions. This is #1 — the OS's delete operations are legitimate; their scope is abused. The DRE is `+ [DRE: Ac]` — Loss of Accessibility. The system remains operational (not LoAv). The files are permanently inaccessible (LoAc). Different DRE, different recovery playbook: LoAv calls for failover; LoAc calls for backups.

### Velocity Profile

Initial infection to local exploitation: seconds (postinstall is immediate). Worm propagation loop — credential theft to poisoned publication: seconds to minutes (automated). Next Trust Acceptance Event: hours to days (depends on when Victim₂ runs `npm install`). This creates a *pulsed* velocity: near-instant exploitation on each node, human-timescale delays between hops. Within 24 hours: ~200 packages compromised. Total: 500+ versions across 796 packages.

---

## What the Decomposition Reveals

Seven structural findings that a flat "supply chain attack" label cannot produce:

**1. #10 is a trust boundary, not a mechanism.** In all three campaigns, #10 marks the Trust Acceptance Event — once per propagation hop. The *mechanisms* are #9, #1, #4, and #7. Defending against "supply chain attacks" as a category means defending against a boundary crossing while ignoring the clusters that make it consequential.

**2. The `#1` between `#10` and `#7` is where defenders have the most untapped leverage.** The package manager's processing step has its own control surface — namespace policies, install sandboxing, resolver restrictions, `--ignore-scripts` — structurally distinct from trust governance (#10) and execution control (#7). This is the step the industry compresses away. It is the step with the most available, least-deployed controls.

**3. R-CRED exposes a universal kill chain.** Every campaign follows the same pattern: credential *acquisition* via one cluster (#9, #7, or #1), then credential *use* via #4. The npm ecosystem's token-based authentication means controls at the use boundary — hardware MFA, token scoping, publish approval workflows — are structurally positioned to break every campaign regardless of how the credential was acquired.

**4. #1 is the silent majority.** Count the #1 steps across all three campaigns. They outnumber every other cluster. Modern attacks work overwhelmingly by using legitimate functions for unintended purposes: the publish API, the install resolver, the GitHub API, filesystem reads, browser APIs, CI triggers. "Anti-malware" — a label that conflates #1 and #7 defenses — is structurally incapable of detecting the majority of these steps.

**5. R-EXEC reveals intermediate control points.** Each distinct #7 step — initial payload, TruffleHog download, LLM weaponization — is a separate intervention opportunity. Application whitelisting could block TruffleHog even after the initial payload runs. Collapsing everything into "malware executed" blinds you to these.

**6. The worm is a supply chain fractal.** Shai-Hulud's recursive `#10.1` generation means each propagation layer produces new propagation layers. The conventional linear model of supply chain risk fails. The notation forces each Trust Acceptance Event to be modeled explicitly, making the exponential topology visible.

**7. LoAc ≠ LoAv.** Shai-Hulud 2.0's file deletion is Loss of *Accessibility* — the machine runs, the data is gone. Not Loss of *Availability*. Wrong classification, wrong playbook.

---

## Controls Mapped to the Causal Chain

The bow-tie model maps controls to specific clusters. Note that **#1 appears three times** — for three structurally different control surfaces, each requiring different controls despite sharing the same generic vulnerability.

**Prevention (Cause-Side):**

| Cluster Step | Preventive Control |
|---|---|
| #9 (Phishing) | Phishing-resistant MFA (FIDO2/WebAuthn); domain monitoring for registry typosquats; security awareness focused on urgency/authority bias |
| #1 (CI/CD workflow abuse) | Least privilege for GitHub Actions; never checkout untrusted PR code in `pull_request_target`; restrict workflow permissions to secrets |
| #4 (Token use) | Hardware-backed MFA on npm; scoped publish tokens (per-package, time-limited, IP-restricted); mandatory publish approval workflows |
| #10 (Trust acceptance) | SBOM maintenance; dependency provenance checking; staged updates with canary deployments; internal mirrors with review gates; lockfile-enforced version pinning |
| #1 (Install processing) | Namespace/scope restrictions on allowed packages; registry allowlists; sandboxed install with no network egress; disable or audit lifecycle scripts (`--ignore-scripts`); resolver restrictions |
| #7 (Payload execution) | Application whitelisting in CI/CD; postinstall audit requirements; sandboxed build environments; code signing enforcement |
| #4 (Post-compromise) | Credential rotation; short-lived scoped tokens; separate publish from build credentials; MFA re-verification for publish actions |
| #1 (Exfiltration) | Egress filtering in build environments; restrict GitHub/cloud API access from CI/CD; network segmentation for dev machines |

**Detection (Center of Bow-Tie):**

Behavioral anomaly detection on npm publish events (velocity, package count, time-of-day); GitHub audit log monitoring for mass branch creation, workflow injection, private-to-public conversions; filesystem integrity monitoring in CI/CD; lockfile diff monitoring in PRs; webhook.site traffic detection.

**Mitigation (Consequence-Side):**

Immediate credential revocation across all platforms (npm, GitHub, AWS, GCP); lockfile-based rollback to known-good versions; SBOM-driven blast radius assessment; breach notification per GDPR/NIS2 timelines; post-mortem with explicit causal chain documentation.

---

## Quick Reference: npm Attack Path Patterns

For practitioners. Clip and use.

**Canonical install-time compromise:**
`#10.2 ||[dev][@Public⇒@npm→@Org]|| → #1 → #7`

**Maintainer-account compromise (phishing):**
`#9 + [DRE: C] → #4 → #1 + [DRE: I] → #10.1 ||[update][@Vendor⇒@npm→@Org]|| → #1 → #7`

**Typosquatting:**
`#9 → #10.2 ||[dev][@Public⇒@npm→@Org]|| → #1 → #7`
The initial #9 reflects that the wrong package choice was induced through human confusion or deceptive naming — a distinct control surface (developer verification, namespace reservation, review friction) from the #10 trust boundary that follows.

**Build-to-secret-theft (full chain):**
`#10.2 → #1 → #7 → #1 + [DRE: C] → #4 → #1 + [DRE: C, I]`

**Self-replicating worm (Shai-Hulud):**
`#10.1 → #1 → #7 → #1 + [DRE: C] → #7 → #1 + [DRE: C] → #4 → #1 + [DRE: I] → #10.1 → [RECURSIVE]`

---

## Closing

The 2025 npm attacks were not "supply chain attacks." They were multi-cluster campaigns in which social engineering (#9), function abuse (#1), identity theft (#4), malware execution (#7), and supply chain trust exploitation (#10) played structurally distinct roles at structurally distinct positions. The supply chain boundary was one element — the Trust Acceptance Event. Everything before it, and everything after it, belongs to other clusters with other generic vulnerabilities and other controls.

The most dangerous thing about an npm supply chain attack is not that malicious code exists in the ecosystem. Malicious code has always existed. The dangerous thing is that your environment decides to treat that code as if it belongs there — and then your own tooling faithfully processes it.

That is why the deepest notation is not `#10`. It is what follows acceptance:

```
#10 → #1 → #7
```

Trust was accepted. Legitimate functions processed the result. Foreign code executed.

The TLCTC framework does not add complexity for its own sake. It adds causal resolution. And causal resolution is the difference between a security program that buys a "supply chain security tool" and one that can name, at each step, what went wrong and what would have stopped it.

---

*The TLCTC framework (Top Level Cyber Threat Clusters) is published at [tlctc.net](https://tlctc.net) under CC BY 4.0. Attack path notation follows TLCTC v2.0, with transit boundary notation per the v2.1 draft specification. npm attack details drawn from public reports by Sysdig, Palo Alto Unit 42, Trend Micro, ReversingLabs, Datadog, ArmorCode, Sonatype, and community disclosures.*

*Framework version: TLCTC v2.0 + v2.1 draft transit notation | Date: March 2026*
