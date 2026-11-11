---
type: "mapping-set"
title: "CWE weaknesses → #4 Identity Theft"
description: "37 CWE weaknesses entries mapped to TLCTC #4 Identity Theft."
resource: "tlctc:mapping:cwe:cluster-4"
tags:
  - "mapping"
  - "cwe"
  - "cluster-4"
---
# CWE weaknesses → #4 Identity Theft

> Source: MITRE CWE → TLCTC mapping (`mappings/mitre-cwe/`). AI-generated, human-reviewed; experimental.

Mapped entries: **37**. Cluster: [#4 Identity Theft](/clusters/cluster-4.md).

| CWE | Name | TLCTC | Verdict | Rationale |
|---|---|---|---|---|
| CWE-6 | J2EE Misconfiguration: Insufficient Session-ID Length | #4 | Allowed | Weak session identifiers facilitate session hijacking, which is a direct form of Identity Theft (#4). |
| CWE-258 | Empty Password in Configuration File | #4 | Allowed | Empty password in configuration file — trivial credential allowing impersonation. Decision tree Q3 -> #4. |
| CWE-259 | Use of Hard-coded Password | #4 | Allowed | Hard-coded password baked into the product's source/binaries — once extracted, every deployment is impersonable. Decision tree Q3 -> #4. |
| CWE-307 | Improper Restriction of Excessive Authentication Attempts | #4 | Allowed | No throttling/lockout on authentication attempts permits credential brute-force. Decision tree Q3 -> #4. (For non-auth endpoints, the rate-limit pattern is CWE-799 -> #4\|#6.) |
| CWE-308 | Use of Single-factor Authentication | #4 | Allowed | Single-factor authentication: compromise of the one factor grants full access. Decision tree Q3 -> #4. |
| CWE-309 | Use of Password System for Primary Authentication | #4 | Allowed | Password-only primary authentication for a high-value system — passwords are the weakest factor against phishing/leak/reuse. Decision tree Q3 -> #4. |
| CWE-321 | Use of Hard-coded Cryptographic Key | #4 | Allowed | Hard-coded cryptographic key in the binary — once extracted, every deployment's encrypted data and authenticated calls are reproducible by the attacker. Decision tree Q3 -> #4. |
| CWE-331 | Insufficient Entropy | #4 \| #5 | Allowed | Insufficient entropy makes generated values guessable. When the value is a session token/identifier → #4 (impersonation); when it is a key/IV → #5 (channel decryption). Per ruling-2. |
| CWE-332 | Insufficient Entropy in PRNG | #4 \| #5 | Allowed | PRNG with insufficient entropy yields predictable outputs. Token/identifier use → #4; key/IV use → #5. Per ruling-2. |
| CWE-333 | Improper Handling of Insufficient Entropy in TRNG | #4 \| #5 | Allowed | Failure to detect/handle TRNG entropy starvation produces predictable outputs. Token/identifier use → #4; key/IV use → #5. Per ruling-2. |
| CWE-334 | Small Space of Random Values | #4 \| #5 | Allowed | A small value space lets an attacker enumerate the full range. Token/identifier use → #4; key/IV use → #5. Per ruling-2. |
| CWE-335 | Incorrect Usage of Seeds in Pseudo-Random Number Generator (PRNG) | #4 \| #5 | Allowed | Seed misuse (constant, low-entropy, exposed) makes PRNG outputs predictable. Token/identifier use → #4; key/IV use → #5. Per ruling-2. |
| CWE-336 | Same Seed in Pseudo-Random Number Generator (PRNG) | #4 \| #5 | Allowed | A reused seed produces identical PRNG sequences across runs/users, making outputs trivially predictable. Token/identifier use → #4; key/IV use → #5. Per ruling-2. |
| CWE-337 | Predictable Seed in Pseudo-Random Number Generator (PRNG) | #4 \| #5 | Allowed | Predictable seeds (e.g., time-based) let an attacker reproduce the PRNG sequence. Token/identifier use → #4; key/IV use → #5. Per ruling-2. |
| CWE-338 | Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG) | #4 \| #5 | Allowed | Non-cryptographic PRNGs (Mersenne Twister, java.util.Random) are state-recoverable from outputs. Token/identifier use → #4; key/IV use → #5. Per ruling-2. |
| CWE-339 | Small Seed Space in PRNG | #4 \| #5 | Allowed | A small seed space lets an attacker brute-force the seed and predict the entire PRNG sequence. Token/identifier use → #4; key/IV use → #5. Per ruling-2. |
| CWE-340 | Generation of Predictable Numbers or Identifiers | #4 | Allowed | Predictable session/token IDs let an attacker derive a valid credential and impersonate the legitimate user. Per ruling-2 → #4. (When the predictable value is a key, see CWE-327/#5.) |
| CWE-341 | Predictable from Observable State | #4 | Allowed | Token/identifier derivable from observable state lets an attacker compute a valid credential and impersonate the legitimate user. Per ruling-2 → #4. |
| CWE-342 | Predictable Exact Value from Previous Values | #4 | Allowed | Sequential/derivable next-value lets an attacker compute the next valid token/identifier and impersonate. Per ruling-2 → #4. |
| CWE-343 | Predictable Value Range from Previous Values | #4 | Allowed | Constrained range from prior outputs lets an attacker brute-force the next valid token/identifier. Per ruling-2 → #4. |
| CWE-384 | Session Fixation | #4 | Allowed | Weak session management allows an attacker to fix or reuse a victim's session identifier. The attacker thereby creates/possesses a valid credential (the session ID) and uses it to impersonate the victim, which is #4 Identity Theft in TLCTC. |
| CWE-521 | Weak Password Requirements | #4 | Allowed | Weak password requirements (low minimum length, no complexity) yield credentials trivially brute-forceable offline. Decision tree Q3 -> #4. |
| CWE-798 | Use of Hard-coded Credentials | #4 | Allowed | Hard-coded credentials baked into the product (passwords, API keys, cryptographic keys) — once extracted from binaries/firmware, every deployment becomes impersonable. Decision tree Q3 -> #4. |
| CWE-799 | Improper Control of Interaction Frequency | #4 \| #6 | Allowed-with-Review | Missing rate-limiting / lockout permits unbounded interaction. Authentication endpoints → #4 (credential brute force / impersonation); resource endpoints → #6 (flooding / DoS). Per ruling-2 enabling-condition policy. |
| CWE-1241 | Use of Predictable Algorithm in Random Number Generator | #4 \| #5 | Allowed | Predictable algorithm in an RNG produces guessable outputs. Token/identifier use -> #4 (impersonation); key/IV use -> #5 (channel decryption). Per ruling-2; consistent with CWE-331-339 PRNG family. |
| CWE-1273 | Device Unlock Credential Sharing | #4 | Allowed | Device unlock credential shared across many devices (a master unlock key). Obtaining the credential maps to the enabling cluster; presenting it to unlock a device is credential use — #4 (R-CRED). Nothing third-party was subverted, so v2.6 does not place this at #10. Decision tree Q3 -> #4. |
| CWE-1391 | Use of Weak Credentials | #4 | Allowed | The product uses weak credentials (e.g., default keys, hard-coded / easily guessable passwords) that an attacker can calculate, derive, reuse, or guess and then use to authenticate. In TLCTC this is #4 Identity Theft: the generic vulnerability is that the system accepts credentials that can be trivially created/guessed and used to impersonate a legitimate identity. No separate harvesting step (#3/#5/#7/#8) is implied by the CWE itself. |
| CWE-1392 | Use of Default Credentials | #4 | Allowed | Default credentials shipped with the product (passwords or cryptographic keys) — any attacker who knows the defaults can authenticate. Decision tree Q3 -> #4. |
| CWE-1393 | Use of Default Password | #4 | Allowed | The product uses default passwords for potentially critical functionality. Real-world exploits use these known passwords to bypass authentication and gain administrative/DBA access. This matches TLCTC #4 Identity Theft: the attacker possesses a known default password and uses it as a credential to operate under a legitimate identity. There is no requirement in the CWE text that the password be first harvested via another cluster, so it is not just an enabling condition. |
| CWE-1394 | Use of Default Cryptographic Key | #4 | Allowed | Default cryptographic key shipped with the product — once known, every deployment's protected operations can be impersonated. Decision tree Q3 -> #4. |
| CWE-1462 | Improper Session Management | #4 | Discouraged | Parent class for session-management weaknesses, introduced in CWE 5.0 when CWE-613 was split. Specific cases classify at child CWEs (CWE-1463 timeout, CWE-1464 invalidation, CWE-1467 shared artifact, CWE-384 fixation). Decision tree Q3 -> #4. |
| CWE-1463 | Insufficient Session Timeout Value | #4 | Allowed | A session without a timeout, or with an excessive one, keeps a session artifact valid long after its holder has gone, so whoever presents it is still accepted. Point-of-use weakness in the session mechanism (successor of CWE-613). Decision tree Q3 -> #4. |
| CWE-1464 | Improper Session Invalidation | #4 | Allowed | The session mechanism keeps accepting a session artifact that should have been invalidated (inactivity, account change), so a presenter who is not its authentic holder is accepted. Decision tree Q3 -> #4. |
| CWE-1465 | Improper Session Invalidation after User Logout | #4 | Allowed | Logout does not invalidate the session on the server, so the session artifact remains acceptable after its holder has ended the session. Variant of CWE-1464. Decision tree Q3 -> #4. |
| CWE-1466 | Improper Session Invalidation after Authentication Credential Change | #4 | Allowed | Existing sessions survive a change of password or other authentication credential, so a session artifact held by someone else stays valid after the holder has rotated the credential. Variant of CWE-1464. Decision tree Q3 -> #4. |
| CWE-1467 | Use of Singular Authentication Artifact for Multiple User Sessions | #4 | Allowed | One authentication artifact serves every authenticated session, so presenting it proves nothing about which holder is present: the mechanism cannot bind the artifact to its authentic holder. Decision tree Q3 -> #4. |
| CWE-1469 | Improper Check for Credential Expiration | #4 | Allowed | The product accepts a credential (key, password, confirmation code, token) without checking whether it has expired, so a credential that should be dead is still honoured at the point of use. Decision tree Q3 -> #4, as for session expiration. Peer-certificate expiry in a channel is CWE-298 (#5, R-SPECIFIC channel); issuing credentials with too long a life is CWE-1472 (enabling condition). |
