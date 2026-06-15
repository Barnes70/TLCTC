---
type: "mapping-set"
title: "CWE weaknesses → #5 Man in the Middle"
description: "19 CWE weaknesses entries mapped to TLCTC #5 Man in the Middle."
resource: "tlctc:mapping:cwe:cluster-5"
tags:
  - "mapping"
  - "cwe"
  - "cluster-5"
---
# CWE weaknesses → #5 Man in the Middle

> Source: MITRE CWE → TLCTC mapping (`mappings/mitre-cwe/`). AI-generated, human-reviewed; experimental.

Mapped entries: **19**. Cluster: [#5 Man in the Middle](/clusters/cluster-5.md).

| CWE | Name | TLCTC | Verdict | Rationale |
|---|---|---|---|---|
| CWE-5 | J2EE Misconfiguration: Data Transmission Without Encryption | #5 | Allowed | Failure to encrypt data in transit implies the vulnerability of the communication path, enabling Man in the Middle (#5). |
| CWE-300 | Channel Accessible by Non-Endpoint | #5 | Allowed | Communication channel where the attacker is in a position between the legitimate endpoints — the canonical Man-in-the-Middle precondition. Decision tree Q4 -> #5. |
| CWE-311 | Missing Encryption of Sensitive Data | #5 | Allowed | Sensitive data sent unencrypted in transit makes the channel exploitable for an interceptor. Per ruling-2 (enabling-condition policy) and Q4 -> #5. |
| CWE-319 | Cleartext Transmission of Sensitive Information | #5 | Allowed | Missing encryption in transit makes the communication path the exploitable surface for #5 Man in the Middle (interception/eavesdropping). Decision tree Q4 (communication-path weakness) → #5; consistent with CWE-5 and CWE-311. |
| CWE-322 | Key Exchange without Entity Authentication | #5 | Allowed | Key exchange without authenticating the peer endpoint — the key is established with whoever happens to be on the wire (the attacker if positioned). Decision tree Q4 -> #5. |
| CWE-323 | Reusing a Nonce, Key Pair in Encryption | #5 | Allowed | Nonce/key reuse breaks confidentiality of authenticated-encryption modes (e.g., AES-GCM), recoverable by an interceptor. Per ruling-2 → #5. |
| CWE-324 | Use of a Key Past its Expiration Date | #5 | Allowed | Continuing to use an expired key extends the window in which a compromised key still decrypts/authenticates traffic, exposing the channel to an interceptor. Per ruling-2 → #5. |
| CWE-325 | Missing Cryptographic Step | #5 \| #4 | Allowed-with-Review | An omitted step (e.g., missing MAC, missing certificate validation, missing key derivation) collapses the protection. Channel/data cases → #5; credential-handling cases → #4. Per ruling-2. |
| CWE-326 | Inadequate Encryption Strength | #5 | Allowed | Insufficient encryption strength makes the protected channel/data tractable for an interceptor. Per ruling-2 (enabling-condition CWEs map to the cluster they enable) and decision tree Q4 → #5. |
| CWE-327 | Use of a Broken or Risky Cryptographic Algorithm | #5 \| #4 | Allowed-with-Review | Broken/risky algorithms degrade the protection they provide. When used for transit/data encryption → #5 (recoverable plaintext for an interceptor); when used for credential hashing/MAC → #4 (recoverable credential). Per ruling-2 enabling-condition policy. |
| CWE-329 | Generation of Predictable IV with CBC Mode | #5 | Allowed | Predictable IVs in CBC mode enable chosen-plaintext attacks against the encrypted channel/data, breaking confidentiality for an interceptor. Per ruling-2 → #5. |
| CWE-523 | Unprotected Transport of Credentials | #5 | Allowed | Credentials transmitted over an unprotected channel — interceptor recovers them and subsequently applies them per R-CRED. Decision tree Q4 -> #5 (acquisition step); subsequent credential application is #4. |
| CWE-757 | Selection of Less-Secure Algorithm During Negotiation ('Algorithm Downgrade') | #5 | Allowed | Algorithm-downgrade attack: attacker manipulates protocol negotiation to force selection of a weaker cipher/hash, then exploits the weakened channel. Per ruling-2 (enabling-condition policy) and Q4 (communication-path weakness) -> #5. |
| CWE-780 | Use of RSA Algorithm without OAEP | #5 | Allowed | Textbook RSA without OAEP padding is vulnerable to chosen-ciphertext / Bleichenbacher-style attacks, recovering plaintext for an interceptor. Per ruling-2 → #5. |
| CWE-924 | Improper Enforcement of Message Integrity During Transmission in a Communication Channel | #5 | Allowed | Failure to verify message integrity in transit — attacker on the wire can modify content undetected. Decision tree Q4 -> #5. |
| CWE-940 | Improper Verification of Source of a Communication Channel | #5 | Allowed | Missing/insufficient verification that a received message originated from the expected source — spoofing/relay possible. Decision tree Q4 -> #5. |
| CWE-1204 | Generation of Weak Initialization Vector (IV) | #5 | Allowed | Weak/predictable IVs degrade encryption confidentiality, recoverable by an interceptor. Per ruling-2 → #5. |
| CWE-1240 | Use of a Cryptographic Primitive with a Risky Implementation | #5 | Allowed | A flawed primitive implementation (e.g., side-channel-leaking AES, broken curve params) degrades the protection of encrypted data, recoverable by an attacker. Per ruling-2 → #5. |
| CWE-1428 | Reliance on HTTP instead of HTTPS | #5 | Allowed | Use of HTTP where HTTPS is required leaves the channel exposed to interception, modification, and active downgrade. Decision tree Q4 -> #5. |
