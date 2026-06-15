---
type: "mapping-set"
title: "CWE weaknesses → #4 Identity Theft"
description: "50 CWE weaknesses entries mapped to TLCTC #4 Identity Theft."
resource: "tlctc:mapping:cwe:cluster-4"
tags:
  - "mapping"
  - "cwe"
  - "cluster-4"
---
# CWE weaknesses → #4 Identity Theft

> Source: MITRE CWE → TLCTC mapping (`mappings/mitre-cwe/`). AI-generated, human-reviewed; experimental.

Mapped entries: **50**. Cluster: [#4 Identity Theft](/clusters/cluster-4.md).

| CWE | Name | TLCTC | Verdict | Rationale |
|---|---|---|---|---|
| CWE-6 | J2EE Misconfiguration: Insufficient Session-ID Length | #4 | Allowed | Weak session identifiers facilitate session hijacking, which is a direct form of Identity Theft (#4). |
| CWE-13 | ASP.NET Misconfiguration: Password in Configuration File | #4 | Allowed | Insecure password storage exposes credentials whose downstream use is impersonation. Decision tree Q3 (credential weakness) → #4. Note: the acquisition step takes its cluster from the access vector (per R-CRED), but the CWE itself classifies by the credential-application threat it enables. |
| CWE-256 | Plaintext Storage of a Password | #4 | Allowed | Plaintext password storage exposes credentials for downstream impersonation. Decision tree Q3 (credential weakness) → #4. |
| CWE-257 | Storing Passwords in a Recoverable Format | #4 | Allowed | Reversible password storage (encrypted vs. one-way hashed) exposes credentials once the storage is reached. Decision tree Q3 → #4. |
| CWE-258 | Empty Password in Configuration File | #4 | Allowed | Empty password in configuration file — trivial credential allowing impersonation. Decision tree Q3 -> #4. |
| CWE-259 | Use of Hard-coded Password | #4 | Allowed | Hard-coded password baked into the product's source/binaries — once extracted, every deployment is impersonable. Decision tree Q3 -> #4. |
| CWE-260 | Password in Configuration File | #4 | Allowed | Password kept in a configuration file is recoverable for impersonation. Decision tree Q3 → #4. |
| CWE-261 | Weak Encoding for Password | #4 | Allowed | Trivially-reversible password encoding (Base64, ROT13) exposes credentials. Decision tree Q3 → #4. |
| CWE-262 | Not Using Password Aging | #4 | Allowed | No password aging policy — long-lived credentials enlarge the window for offline brute force or reuse-after-leak. Decision tree Q3 -> #4. |
| CWE-263 | Password Aging with Long Expiration | #4 | Allowed | Password aging interval is too long, providing only nominal rotation. Decision tree Q3 -> #4. |
| CWE-307 | Improper Restriction of Excessive Authentication Attempts | #4 | Allowed | No throttling/lockout on authentication attempts permits credential brute-force. Decision tree Q3 -> #4. (For non-auth endpoints, the rate-limit pattern is CWE-799 -> #4\|#6.) |
| CWE-308 | Use of Single-factor Authentication | #4 | Allowed | Single-factor authentication: compromise of the one factor grants full access. Decision tree Q3 -> #4. |
| CWE-309 | Use of Password System for Primary Authentication | #4 | Allowed | Password-only primary authentication for a high-value system — passwords are the weakest factor against phishing/leak/reuse. Decision tree Q3 -> #4. |
| CWE-312 | Cleartext Storage of Sensitive Information | #4 | Allowed-with-Review | Cleartext storage of sensitive data; in the dominant case the data is credentials/tokens enabling #4 Identity Theft. For non-credential PII, the impact is a confidentiality DRE rather than a distinct cluster — classify at the access-vector cluster (per R-CRED) for credential cases and at the DRE level for general PII. |
| CWE-313 | Cleartext Storage in a File or on Disk | #4 | Allowed-with-Review | Cleartext on-disk storage typically exposes credentials/tokens for impersonation. Decision tree Q3 → #4 (credential case). For non-credential PII, the threat is a confidentiality DRE driven by the access-vector cluster. |
| CWE-314 | Cleartext Storage in the Registry | #4 | Allowed-with-Review | Cleartext credential/token storage in the Windows registry exposes secrets for impersonation. Decision tree Q3 → #4. |
| CWE-315 | Cleartext Storage of Sensitive Information in a Cookie | #4 | Allowed | Session cookies are credentials by function; cleartext cookie storage exposes them for impersonation. Decision tree Q3 → #4. The acquisition-step cluster (e.g., #3 via XSS, #5 via MitM) is separate from this CWE per R-CRED. |
| CWE-316 | Cleartext Storage of Sensitive Information in Memory | #4 | Allowed-with-Review | Cleartext credentials/tokens in memory are recoverable (via #7 Malware-driven memory read, #8 cold-boot/DMA, or debug capture) for impersonation. Decision tree Q3 → #4. Acquisition cluster is separate per R-CRED. |
| CWE-318 | Cleartext Storage of Sensitive Information in Executable | #4 | Allowed | Sensitive secrets (API keys, credentials, encryption keys) compiled into the executable are recoverable via reverse engineering. Per ruling-2 (enabling-condition CWEs map to the cluster they enable) -> #4 (the recovered credential is then applied for impersonation). Acquisition cluster (#2 / #3 / static analysis) is separate per R-CRED. |
| CWE-321 | Use of Hard-coded Cryptographic Key | #4 | Allowed | Hard-coded cryptographic key in the binary — once extracted, every deployment's encrypted data and authenticated calls are reproducible by the attacker. Decision tree Q3 -> #4. |
| CWE-328 | Use of Weak Hash | #4 | Allowed | Weak password/credential hashes are reversible by precomputation (rainbow tables) or brute force, exposing credentials for impersonation. Per ruling-2 → #4. (Non-credential hash uses fall to #5 — see CWE-327.) |
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
| CWE-522 | Insufficiently Protected Credentials | #4 | Allowed | Credentials stored or transmitted without sufficient protection are recoverable for impersonation. Decision tree Q3 → #4. |
| CWE-555 | J2EE Misconfiguration: Plaintext Password in Configuration File | #4 | Allowed | Plaintext password in J2EE configuration is recoverable for impersonation. Decision tree Q3 → #4. |
| CWE-613 | Insufficient Session Expiration | #4 | Allowed | Insufficient session expiration extends the window in which a stolen session token remains valid for impersonation. Decision tree Q3 -> #4. |
| CWE-759 | Use of a One-Way Hash without a Salt | #4 | Allowed | Unsalted password hashes are recoverable via precomputed (rainbow) tables, exposing credentials for impersonation. Per ruling-2 → #4. |
| CWE-760 | Use of a One-Way Hash with a Predictable Salt | #4 | Allowed | Predictable salts collapse password-hash protection back to rainbow-table-tractable, exposing credentials for impersonation. Per ruling-2 → #4. |
| CWE-798 | Use of Hard-coded Credentials | #4 | Allowed | Hard-coded credentials baked into the product (passwords, API keys, cryptographic keys) — once extracted from binaries/firmware, every deployment becomes impersonable. Decision tree Q3 -> #4. |
| CWE-799 | Improper Control of Interaction Frequency | #4 \| #6 | Allowed-with-Review | Missing rate-limiting / lockout permits unbounded interaction. Authentication endpoints → #4 (credential brute force / impersonation); resource endpoints → #6 (flooding / DoS). Per ruling-2 enabling-condition policy. |
| CWE-916 | Use of Password Hash With Insufficient Computational Effort | #4 | Allowed | Fast-but-insecure password hashing (MD5/SHA1) lets attackers brute-force credentials offline, enabling impersonation. Per ruling-2 → #4. |
| CWE-1004 | Sensitive Cookie Without 'HttpOnly' Flag | #4 | Allowed | Missing HttpOnly exposes the session cookie to JavaScript-readable storage; the dominant downstream threat is cookie theft for impersonation. Decision tree Q3 → #4. The XSS cluster (#3) is a separate acquisition vector per R-CRED. |
| CWE-1241 | Use of Predictable Algorithm in Random Number Generator | #4 \| #5 | Allowed | Predictable algorithm in an RNG produces guessable outputs. Token/identifier use -> #4 (impersonation); key/IV use -> #5 (channel decryption). Per ruling-2; consistent with CWE-331-339 PRNG family. |
| CWE-1391 | Use of Weak Credentials | #4 | Allowed | The product uses weak credentials (e.g., default keys, hard-coded / easily guessable passwords) that an attacker can calculate, derive, reuse, or guess and then use to authenticate. In TLCTC this is #4 Identity Theft: the generic vulnerability is that the system accepts credentials that can be trivially created/guessed and used to impersonate a legitimate identity. No separate harvesting step (#3/#5/#7/#8) is implied by the CWE itself. |
| CWE-1392 | Use of Default Credentials | #4 | Allowed | Default credentials shipped with the product (passwords or cryptographic keys) — any attacker who knows the defaults can authenticate. Decision tree Q3 -> #4. |
| CWE-1393 | Use of Default Password | #4 | Allowed | The product uses default passwords for potentially critical functionality. Real-world exploits use these known passwords to bypass authentication and gain administrative/DBA access. This matches TLCTC #4 Identity Theft: the attacker possesses a known default password and uses it as a credential to operate under a legitimate identity. There is no requirement in the CWE text that the password be first harvested via another cluster, so it is not just an enabling condition. |
| CWE-1394 | Use of Default Cryptographic Key | #4 | Allowed | Default cryptographic key shipped with the product — once known, every deployment's protected operations can be impersonated. Decision tree Q3 -> #4. |
