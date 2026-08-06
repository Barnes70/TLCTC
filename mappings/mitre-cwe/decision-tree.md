# CWE → TLCTC Classification Decision Tree

This document provides the step-by-step methodology for mapping any MITRE CWE weakness to the correct TLCTC cluster(s).

## Prerequisites

Before classifying a CWE, establish two things:

1. **Is this a concrete weakness?** Category nodes, views, and deprecated CWEs cannot be mapped → **Prohibited**.
2. **Is it specific enough?** Umbrella CWEs that span multiple root causes (e.g., CWE-20 "Improper Input Validation") → **Discouraged** or **N/A**.

## The Decision Tree

Walk through these questions **in order**. Stop at the first match.

```
Q0: Is this CWE a Category, View, or Deprecated entry?
    ├── YES → N/A (Prohibited)
    └── NO ↓

Q1: Is this CWE too abstract to determine a single generic vulnerability?
    (e.g., CWE-20 Improper Input Validation, CWE-693 Protection Mechanism Failure)
    ├── YES → N/A (Discouraged)
    └── NO ↓

Q2: Is this a CODE IMPLEMENTATION FLAW?
    (buffer overflow, injection, type confusion, use-after-free, etc.)
    │
    │   GUARD (R-CHANNEL / R-FLOOD) — before answering YES, ask:
    │   is the defective logic ITSELF a security control whose failure
    │   constitutes another cluster's generic vulnerability?
    │   If so, that cluster wins; Q2 is the residual test, not the first one.
    │     • communication-path control (cert validation, chain of trust,
    │       hostname match, expiry/revocation, channel encryption,
    │       algorithm negotiation)              → #5   (R-CHANNEL, skip to Q4)
    │     • capacity/throttling control          → #6   (R-FLOOD, skip to Q5)
    │   The defect must be CONSTITUTIVE of the control, not incidental to it:
    │   memory corruption in a TLS parser is still Q2 → #2|#3, because the
    │   exploited generic vulnerability there is the code flaw, not the control.
    │
    ├── YES → Does the flaw exist in server-side or client-side code?
    │         ├── Server → #2 Exploiting Server
    │         ├── Client → #3 Exploiting Client
    │         └── Could be either → #2 | #3 (context-dependent)
    │
    │         Follow-up: Can the flaw enable code execution?
    │         ├── YES → append → #7 (e.g., #2 → #7)
    │         └── NO → stop here
    └── NO ↓

Q3: Is this a POINT-OF-USE authentication / identity-binding weakness?
    (the authentication or session mechanism accepts a credential without
     verifying the presenter is its authentic holder — session fixation/
     expiration, single-factor auth, no lockout on auth attempts, predictable
     session/token IDs, acceptance of default/hard-coded/weak credentials)
    ├── YES → #4 Identity Theft
    └── NO ↓

    NOTE 1 — Authentication-LOGIC bypass is NOT this question.
    Per Axiom X / R-CRED, credential acquisition follows the enabling cluster
    and credential APPLICATION is always #4. But a flaw in the authentication
    function's logic itself (e.g., bypass via spoofed parameter, missing check,
    wrong comparison) is abuse of the auth function and maps to #1 (Q9 below).
    CWE-287 Improper Authentication and similar bypass-class CWEs → #1.

    NOTE 2 — Credential STORAGE / PROTECTION / LIFECYCLE is NOT #4 (v2.3.1).
    Under the retightened v2.3.1 #4 definition (point-of-use identity-artifact
    binding), cleartext/recoverable credential storage, weak password hashing or
    encoding, and password-aging/lifecycle weaknesses are acquisition-side
    ENABLING CONDITIONS, not #4. Per R-CRED the cluster is set by the acquisition
    vector at incident time (#2/#5/#7/#8); map these to `enabling-condition`
    (see the Enabling-Condition CWEs section below). Only weaknesses in the
    authentication/session mechanism's own acceptance of a credential remain #4.

Q4: Is this a COMMUNICATION PATH weakness?
    (missing encryption in transit, certificate validation failure, channel security)
    ├── YES → #5 Man in the Middle
    └── NO ↓

    NOTE 3 — This question is reachable from the Q2 guard (R-CHANNEL).
    Peer-authenticity controls are communication-path controls even though
    the weakness reads as "the code failed to validate": per R-CHANNEL the
    generic vulnerability is the lack of sufficient control over the
    communication path (#5), not the code flaw (#2/#3). This covers
    CWE-295/296/297/298/299/370 and the OpenSSL-specific CWE-593/599, and
    aligns them with CWE-940/757/300/311/319, which were already #5.
    Incidental defects in the same code path stay #2|#3 — e.g. a memory-safety
    or parsing bug in a TLS implementation, where the exploited generic
    vulnerability is the code flaw and the control is merely its location.

    NOTE 4 — R-CHANNEL vs NOTE 1 (CWE-593). "Authentication bypass" in a
    channel-security CWE means PEER authenticity (is the far end who it
    claims to be), not identity authentication of a principal. NOTE 1's
    #1 ruling governs the latter only. CWE-593 defeats certificate
    verification by construction, so R-CHANNEL applies → #5.

Q5: Is this a RESOURCE EXHAUSTION or CAPACITY weakness?
    (uncontrolled resource consumption, asymmetric resource usage, missing rate limiting)
    ├── YES → #6 Flooding Attack
    │         (Note: if a code bug causes crash, that's #2/#3, not #6)
    └── NO ↓

Q6: Does this weakness enable FOREIGN CODE EXECUTION directly?
    (code injection via designed execution capability, not via code flaw)
    ├── YES → #7 Malware
    │         If via legitimate tool/function → #1 → #7
    └── NO ↓

Q7: Is this a PHYSICAL LAYER weakness?
    (hardware debug interfaces, physical signal leakage, insufficient physical protection)
    ├── YES → #8 Physical Attack
    └── NO ↓

Q8: Is this a TRUST RELATIONSHIP weakness with third-party components?
    (dependency confusion, unsigned updates, unverified package sources)
    ├── YES → #10 Supply Chain Attack
    └── NO ↓

Q9: Is this a LOGIC, CONFIGURATION, or SCOPE weakness?
    (privilege escalation via design, API misuse, missing authorization, default credentials)
    ├── YES → #1 Abuse of Functions
    └── NO → Re-examine. One of the above must apply.
```

## The Role Disambiguation: #2 vs. #3

The largest context-dependent group (219 entries) maps to `#2 | #3`. These are code implementation flaws where the TLCTC cluster depends on the **role** of the vulnerable component:

```
Is the vulnerable code acting as a SERVER (receiving and processing requests)?
├── YES → #2 Exploiting Server
│         Examples: SQL injection in web app, buffer overflow in HTTP daemon
└── NO ↓

Is the vulnerable code acting as a CLIENT (requesting and rendering content)?
├── YES → #3 Exploiting Client
│         Examples: Browser rendering bug, PDF reader vulnerability
└── NO ↓

Could the same CWE appear in either role?
└── YES → #2 | #3 (context-dependent; classify at CVE/instance level)
```

### Common #2 | #3 Weakness Types

| CWE Pattern | Examples | Why Context-Dependent |
|-------------|----------|----------------------|
| Memory safety | CWE-787 Out-of-bounds Write, CWE-125 Out-of-bounds Read | Same flaw type in any compiled code |
| Injection | CWE-74 Injection, CWE-77 Command Injection | Server-side web app vs. client-side script engine |
| Type confusion | CWE-843 Type Confusion | Browser engine (client) vs. server runtime |
| Integer issues | CWE-190 Integer Overflow | Affects any compiled component |

## The Execution Chain: When to Append → #7

Per R-EXEC, if a weakness enables foreign code execution, the mapping must include a `→ #7` step:

| Weakness Type | Mapping | Rationale |
|---------------|---------|-----------|
| Buffer overflow (server) with RCE | `#2 → #7` | Code flaw enables unintended execution |
| XSS (reflected/stored) | `#2 → #7` | Server flaw delivers script to client for execution |
| XSS (DOM-based) | `#3` | Client-side flaw; script runs in client context |
| Deserialization (server) | `#2 → #7` | Server-side flaw enables arbitrary code execution |
| Code injection via API | `#1 → #7` | Designed function abused to execute foreign code |

## The Abstract CWE Problem

CWE includes many high-level entries that are too abstract to map to a single cluster:

| Verdict | Guidance | Examples |
|---------|----------|----------|
| **Discouraged** | Maps to multiple clusters depending on context, OR maintainability/code-quality defect with no direct threat cluster | CWE-20 (Input Validation), CWE-693 (Protection Mechanism Failure), CWE-1120 (Excessive Code Complexity) |
| **Prohibited** | Not a concrete weakness — organizational node (category, view, list, deprecated) | CWE-310 (Cryptographic Issues — Category), CWE-1000 (Research Concepts — View), CWE-1432 (MIHW List) |

For these entries, classify at the **child CWE** or **CVE level** instead.

## Enabling-Condition CWEs

Some CWEs describe a *state of exposure* rather than a threat action — for example, cleartext password storage, missing encryption in transit, weak crypto algorithm, predictable PRNG. By policy (ruling-2), these map to **the cluster they enable**, not to N/A — **except credential storage/protection/lifecycle weaknesses**, which under TLCTC v2.3.1 map to `enabling-condition` (the retightened #4 covers only point-of-use credential application, so it no longer absorbs storage/protection flaws; the operative cluster is set by the acquisition vector per R-CRED):

| Enabling condition | Cluster | Reason |
|--------------------|---------|--------|
| Cleartext / recoverable storage of credentials/tokens | `enabling-condition` | Acquisition-side; per R-CRED the cluster is the acquisition vector (#2/#5/#7/#8), not #4 (v2.3.1) |
| Weak password hash (no salt, fast hash, broken algorithm) | `enabling-condition` | Offline crack is acquisition-side; cluster set by acquisition vector (v2.3.1), not #4 |
| Password aging / lifecycle policy weakness | `enabling-condition` | Enlarges the reuse window but is not point-of-use authentication (v2.3.1) |
| Cleartext transmission / weak channel encryption | `#5` | The weakness is the communication path itself (#5's generic vulnerability) |
| Weak encryption algorithm (broken cipher, weak IV, expired key) | `#5` | Channel/data recoverable to interceptor |
| Predictable PRNG used for security values | `#4 \| #5` | Token accepted at use → #4; key/IV use → #5 |
| Missing rate-limiting on auth endpoint | `#4 \| #6` | Auth mechanism accepts unlimited attempts → #4; resource → flooding |
| Maintainability defect (firmware-not-updateable, dead code) | `N/A` (Discouraged) | Does not map to any single cluster |

The `R-CRED` distinction still applies: the *acquisition* step takes its cluster from the access vector (e.g., `#7` malware reading the storage, `#5` MitM intercepting transit). For channel/crypto exposures the CWE is classified by the cluster it enables. For **credential storage/protection/lifecycle** exposures (v2.3.1), the CWE is instead marked `enabling-condition`: because the acquisition vector varies (#2/#5/#7/#8) and #4 covers only the later point-of-use application, no single cluster is asserted.

## Quality Checklist

Before finalizing a CWE mapping, verify:

- [ ] **Concrete weakness** — Not a category, view, list, or deprecated entry (else Prohibited)
- [ ] **Specific enough** — Can determine a single generic vulnerability (or explicit alternatives)
- [ ] **Q2 guard applied** — Before classifying as a code flaw, confirm the defective logic is not itself a communication-path control (`#5`, R-CHANNEL) or a capacity/throttling control (`#6`, R-FLOOD). Q2 is the residual test
- [ ] **Role considered** — If code flaw, is it server or client? If unclear, mark `#2 | #3`
- [ ] **R-EXEC respected** — If the weakness enables foreign code execution, `→ #7` is included (e.g., code injection, deserialization, template injection, RFI, dynamic class loading from untrusted source)
- [ ] **R-CRED respected** — Authentication-logic bypass = `#1`; credential application (point-of-use) = `#4`; credential acquisition — including cleartext/weakly-hashed credential storage — takes the cluster of the access vector, not `#4` (v2.3.1)
- [ ] **Enabling-condition policy** — Channel/crypto exposure maps to the cluster it enables (#5); credential storage/protection/lifecycle exposure maps to `enabling-condition` (acquisition vector determines cluster per R-CRED, not #4)
- [ ] **Cause, not consequence** — Mapping the exploitable flaw, not the resulting impact (Axiom III)
- [ ] **Verdict assigned** — Confidence level reflects mapping certainty
