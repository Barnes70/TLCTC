# Walkthrough: npm Incident to Actionable Controls

**Pattern:** NPM-PAT-002 (Maintainer Account Compromise via Phishing)
**Incident:** Chalk/Debug Phishing Campaign, September 2025

This walkthrough demonstrates how to decompose a real npm supply chain incident into TLCTC clusters and derive structurally targeted controls for each step.

---

## Step 1 — Gather the Facts

On September 5, 2025, attackers registered `npmjs.help` — a visual lookalike of `npmjs.com`. They sent a phishing email to Josh Junon ("Qix"), maintainer of chalk, debug, and 16+ other foundational npm packages. The email impersonated npm support, claimed urgent 2FA credential updates were required by September 10, and directed Junon to the phishing site. Under time pressure after "a long week and a panicky morning," Junon entered his credentials.

The attackers authenticated as Junon, published trojanized versions of 18+ packages. The payload was browser-targeted: obfuscated JavaScript that hooked `window.ethereum`, `fetch`, and `XMLHttpRequest`, replacing cryptocurrency wallet addresses across six blockchains using Levenshtein distance matching with 280+ hardcoded fallback addresses.

## Step 2 — Decompose Into Clusters

Apply the TLCTC classification rules to each causal step:

| Step | What Happened | Cluster | Rule Applied | DRE |
|------|--------------|---------|-------------|-----|
| 1 | Phishing email sent to maintainer | **#9** Social Engineering | Bridge cluster: human boundary crossed | C |
| 2 | Stolen credentials used to authenticate | **#4** Identity Theft | R-CRED: credential use is always #4 | — |
| 3 | Trojanized packages published via npm API | **#1** Abuse of Functions | Legitimate publish API, abused scope | I |
| 4 | Consumers accept poisoned update | **#10** Supply Chain Attack | TAE: trust artifact accepted | — |
| 5 | Package manager processes the artifact | **#1** Abuse of Functions | Legitimate install processing | — |
| 6 | Malicious JavaScript executes in browser | **#7** Malware | R-EXEC: FEC execution via designed mechanism | — |
| 7 | Browser APIs hooked for crypto theft | **#1** Abuse of Functions | Legitimate APIs, abused scope | C, I |

**Compact notation:**
```
#9 ||[human][@External→@Maintainer(Qix)]|| →[~3d] + [DRE: C]
→ #4 → #1 + [DRE: I]
||[update][@Maintainer(Qix)⇒@npm→@Consumers]|| #10
→ #1 → #7 → #1 + [DRE: C, I]
```

### Classification Decisions Explained

**Why #9 and not #4 for the phishing step?**
The phishing email exploits human psychological susceptibility — that is the generic vulnerability. The credential theft is the *outcome* of the social engineering. R-CRED: acquisition maps to the enabling cluster (#9); use maps to #4 in the next step.

**Why #1 for the publish step?**
The npm `publish` command works exactly as designed. No API vulnerability was exploited. The attacker is using a legitimate function with legitimate credentials for an unintended purpose.

**Why #10 for the consumer update?**
The Trust Acceptance Event: the consumer's dependency resolver accepts the new version as trustworthy. This is the supply chain boundary crossing. The transit notation (`@Maintainer(Qix)⇒@npm→@Consumers`) makes npm's role as carrier infrastructure explicit — it has its own control surface.

**Why three separate #1 steps?**
Each #1 step has a *different generic vulnerability* and a *different control surface*:
- Step 3 (#1): Publish API scope → control via publish approval workflows
- Step 5 (#1): Install processing scope → control via sandboxing, `--ignore-scripts`
- Step 7 (#1): Browser API scope → control via CSP, API interception monitoring

Collapsing them into one "#1" hides three distinct intervention opportunities.

## Step 3 — Map Controls to Each Cluster

Now derive controls that are structurally targeted to each step's generic vulnerability:

### #9 — Social Engineering (Step 1)

The generic vulnerability is human psychological susceptibility. Controls must address the human boundary:

| Control | Type | Effectiveness |
|---------|------|--------------|
| Phishing-resistant MFA (FIDO2/WebAuthn) | Prevention | **High** — credentials cannot be phished even if the human is deceived |
| Domain monitoring for registry typosquats | Detection | **Medium** — `npmjs.help` could have been flagged within hours of registration |
| Security awareness training (urgency/authority bias) | Prevention | **Low-Medium** — reduces but cannot eliminate human susceptibility |

**Key insight:** FIDO2/WebAuthn would have broken this chain completely. The phishing *succeeded* — Junon entered credentials — but hardware-bound credentials cannot be replayed from a different origin.

### #4 — Identity Theft (Step 2)

The generic vulnerability is insufficient verification of identity claims:

| Control | Type | Effectiveness |
|---------|------|--------------|
| Hardware-backed MFA on npm publish | Prevention | **High** — stolen password alone is insufficient |
| Scoped publish tokens (per-package, time-limited, IP-restricted) | Prevention | **High** — limits blast radius even if credentials are compromised |
| Publish approval workflows (require 2+ maintainers) | Prevention | **High** — single-maintainer compromise is insufficient |

**Key insight:** This is the universal kill chain position. Every npm account compromise — whether via phishing (#9), credential leak (#7/#1), or brute force — must pass through #4. Controls here break *all* campaigns.

### #1 — Publish API Abuse (Step 3)

| Control | Type | Effectiveness |
|---------|------|--------------|
| Anomaly detection on publish events (velocity, time-of-day, package count) | Detection | **Medium** — 18 packages published rapidly is anomalous |
| Rate limiting on publish operations | Prevention | **Low** — delays but doesn't prevent |
| Mandatory package provenance attestation | Detection | **Medium** — flags unsigned or misattributed publications |

### #10 — Trust Acceptance (Step 4)

| Control | Type | Effectiveness |
|---------|------|--------------|
| Lockfile-enforced version pinning | Prevention | **High** — prevents automatic acceptance of new versions |
| Staged updates with canary deployments | Detection | **High** — limits blast radius, creates detection window |
| Internal registry mirrors with review gates | Prevention | **High** — new versions require explicit approval |
| Dependency provenance checking | Detection | **Medium** — verifies publication chain |

**Key insight:** Lockfile pinning is the single most effective consumer-side control. Permissive semver ranges (`^x.y.z`) are what made this attack propagate.

### #1 — Install Processing (Step 5)

| Control | Type | Effectiveness |
|---------|------|--------------|
| `--ignore-scripts` by default | Prevention | **High** — prevents lifecycle hook execution |
| Sandboxed install with no network egress | Prevention | **High** — contains any payload that does execute |
| Lifecycle script audit before allowing | Detection | **High** — surfaces suspicious postinstall scripts |

### #7 — Payload Execution (Step 6)

| Control | Type | Effectiveness |
|---------|------|--------------|
| Content Security Policy (CSP) | Prevention | **Medium** — limits what injected scripts can do |
| Subresource Integrity (SRI) | Prevention | **Medium** — detects modified script content |
| Application whitelisting | Prevention | **High** — blocks unauthorized code execution |

### #1 — Browser API Abuse (Step 7)

| Control | Type | Effectiveness |
|---------|------|--------------|
| Browser extension monitoring for API hooks | Detection | **Medium** — detects `fetch`/`XMLHttpRequest` interception |
| Transaction verification (out-of-band wallet address confirmation) | Prevention | **High** — catches address substitution |
| Hardware wallet transaction signing | Prevention | **High** — wallet address verified on trusted display |

## Step 4 — Identify the Highest-Leverage Controls

Rank controls by how many steps they break and how early in the chain they act:

| Rank | Control | Breaks Step(s) | Position |
|------|---------|---------------|----------|
| 1 | Phishing-resistant MFA (FIDO2) | #9 (Step 1) | Earliest — prevents credential acquisition entirely |
| 2 | Publish approval workflow (2+ maintainers) | #4 (Step 2) | Universal — breaks all account compromise patterns |
| 3 | Lockfile-enforced version pinning | #10 (Step 4) | Consumer-side — prevents automatic trust acceptance |
| 4 | `--ignore-scripts` default | #1 (Step 5) | Consumer-side — blocks lifecycle hook execution path |
| 5 | Hardware wallet for crypto transactions | #1 (Step 7) | Last resort — mitigates payload impact |

## Step 5 — Build the Risk Register Entry

```
Incident:       Chalk/Debug npm Phishing Campaign (September 2025)
Attack Path:    #9 → #4 → #1 → #10 → #1 → #7 → #1
Velocity:       VC-1 (3d phishing window) → VC-4 (instant credential use to publication)
                → VC-2 (hours for consumer exposure) → VC-4 (instant payload execution)
Blast Radius:   18+ packages, billions of weekly downloads
DRE Profile:    C (credentials, transaction data), I (package integrity, wallet addresses)
Kill Chain:     #9→#4 junction — any control at #4 breaks all downstream steps
Priority:       Implement FIDO2 for npm maintainers (breaks #9→#4)
                Enforce lockfile pinning in CI/CD (breaks #10)
                Default --ignore-scripts (breaks #1→#7 install chain)
```

---

*This walkthrough uses the TLCTC v2.0 framework with v2.1 transit boundary notation. Full incident analysis: `attack-paths/chalk-debug-phishing-2025.json`. Pattern reference: `tlctc-npm-patterns.json` (NPM-PAT-002).*
