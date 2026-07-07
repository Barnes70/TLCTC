# Worked Example: From Vulnerability Findings to Risk Controls

This walkthrough demonstrates how to translate CWE-based vulnerability findings into TLCTC cluster exposure for strategic risk reporting and control design.

## Scenario

Your application security team runs a code audit and penetration test against a web application. The findings report contains:

| Finding | CWE | Severity | Location |
|---------|-----|----------|----------|
| SQL Injection in login form | CWE-89 | Critical | Server-side (API backend) |
| Stored XSS in comment field | CWE-79 | High | Server-side (stored), executes client-side |
| Weak password hashing (MD5) | CWE-328 | High | Server-side (auth module) |
| Missing rate limiting on API | CWE-770 | Medium | Server-side (API gateway) |
| Hardcoded credentials in config | CWE-798 | Critical | Server-side (deployment) |

## Step 1: Map Each CWE to TLCTC

### CWE-89 — SQL Injection

> Q2: Is this a code implementation flaw? **YES** — injection flaw
> Server or client? **Server** (API backend)
> Can it enable code execution? **Potentially** (via `xp_cmdshell`, `INTO OUTFILE`, etc.)

**Mapping:** `#2 → #7` (server-side flaw enabling potential code execution)

The SQL injection is a server-side implementation flaw (#2). If the attacker escalates to OS command execution via database features, that's a #7 step. Even without RCE, the immediate exploit is #2.

### CWE-79 — Cross-site Scripting (Stored)

> Q2: Is this a code implementation flaw? **YES** — the server fails to sanitize input
> Server or client? **Server stores it, client executes it**

**Mapping:** `#2 → #7`

Stored XSS is a server-side coding flaw (#2) — the server accepts and stores unsanitized input. When another user's browser renders the stored payload, foreign script executes (#7). Per R-EXEC, both steps are recorded.

### CWE-328 — Use of Weak Hash

> Q3: Is this a credential/authentication weakness? It concerns credential **protection** — making acquisition easier — **not** the point-of-authentication binding that defines #4.

**Mapping:** Enabling Condition (R-CRED) — not itself a cluster

Weak hashing makes credential acquisition trivially easier (offline cracking of exposed hashes). Under TLCTC v2.3.1, #4 Identity Theft is retightened to the insufficient binding, at the point of authentication, between a presented credential and the authentic holder; credential *storage/protection* failures are acquisition-side and classify to the enabling cluster that reaches the exposed credential store — here `#2`, the SQL-injection server exploit that dumps it — not to #4. The later use of a cracked credential to authenticate is the separate #4 step. Full chain: `#2 →[offline crack] #4`.

### CWE-770 — Allocation of Resources Without Limits

> Q5: Is this a resource exhaustion weakness? **YES** — missing rate limiting

**Mapping:** `#6`

The missing rate limit means finite API capacity can be overwhelmed. This is a flooding attack vector (#6).

### CWE-798 — Use of Hardcoded Credentials

> Q9: Is this a logic/configuration weakness? **YES** — credentials embedded by design

**Mapping:** `#1`

Hardcoded credentials are a design/configuration flaw — the credential is part of the software's designed state. Finding and using it is abuse of the application's own configuration (#1). The subsequent authentication with the credential is a separate #4 step.

Complete attack path if exploited: `#1 → #4` (discover hardcoded credential → use it to authenticate).

## Step 2: Build the Risk Exposure Map

### Cluster Exposure Summary

| Cluster | Findings | Role |
|---------|----------|------|
| **#2 Exploiting Server** | CWE-89, CWE-79 | Server-side code flaws enabling injection |
| **#7 Malware** | CWE-89 → #7, CWE-79 → #7 | Code execution enabled by server flaws |
| **#6 Flooding Attack** | CWE-770 | Resource exhaustion via API |
| **#1 Abuse of Functions** | CWE-798 | Hardcoded credential as design flaw (enables a later #4) |
| *Enabling condition (R-CRED)* | CWE-328 | Weak stored-hash eases offline cracking; acquisition-side — routes to the `#2` dump, not #4 |

### Worst-Case Attack Path

An attacker chains these weaknesses:

```
#2 →[Δt=seconds] #7 →[Δt=minutes] #1 →[Δt=seconds] #4 + [DRE: C, I]
```

1. **#2** — SQL injection exploits server-side code flaw
2. **#7** — Attacker achieves code execution via database
3. **#1** — Discovers hardcoded credentials in config files
4. **#4** — Uses hardcoded credentials to authenticate to other systems
5. **[DRE: C, I]** — Data exfiltration (Confidentiality) and potential modification (Integrity)

## Step 3: Risk Register Translation

### Risk Register Entry

> **Vulnerability Assessment:** Web application with 5 findings across 4 TLCTC clusters.
>
> **Primary Exposure:** Exploiting Server (#2) — two critical injection flaws provide the initial attack surface.
>
> **Velocity Profile:** VC-4 to VC-3 (seconds to minutes between exploitation steps) — automated exploitation is trivially possible.
>
> **Control Priorities by Cluster:**
>
> | Cluster | Control Gap | Recommended Action |
> |---------|------------|-------------------|
> | **#2** | Input validation failures in server code | Parameterized queries, output encoding, code review |
> | **#7** | Code execution possible via #2 | WAF rules, sandboxed execution, CSP headers |
> | *Enabling condition (CWE-328)* | Weak password hashing eases offline cracking | Upgrade to bcrypt/argon2, credential rotation (reduces the credential acquisition that feeds a later #4) |
> | **#6** | No rate limiting | API gateway rate limits, throttling |
> | **#1** | Hardcoded credentials | Secrets management (vault), remove from codebase |
>
> **Data Risk Events:** Loss of Confidentiality (C), Loss of Integrity (I)

### What This Enables

- **For AppSec:** Continue tracking CWE findings in your scanner. No change to tooling.
- **For Risk Management:** Aggregate findings by cluster. The concentration in #2 signals **server-side code quality** as the primary structural weakness — not individual bugs.
- **For Control Design:** The VC-4 velocity means preventive controls (input validation, parameterized queries) are structurally necessary. Detective controls alone cannot keep pace.
- **For the Board:** "Our web application has server-side code quality weaknesses that could enable data theft in seconds. Remediation of the two injection flaws eliminates the primary attack surface."
