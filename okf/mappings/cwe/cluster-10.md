---
type: "mapping-set"
title: "CWE weaknesses → #10 Supply Chain Attack"
description: "11 CWE weaknesses entries mapped to TLCTC #10 Supply Chain Attack."
resource: "tlctc:mapping:cwe:cluster-10"
tags:
  - "mapping"
  - "cwe"
  - "cluster-10"
---
# CWE weaknesses → #10 Supply Chain Attack

> Source: MITRE CWE → TLCTC mapping (`mappings/mitre-cwe/`). AI-generated, human-reviewed; experimental.

Mapped entries: **11**. Cluster: [#10 Supply Chain Attack](/clusters/cluster-10.md).

| CWE | Name | TLCTC | Verdict | Rationale |
|---|---|---|---|---|
| CWE-347 | Improper Verification of Cryptographic Signature | #10 \| #5 | Allowed | Enables #10 (malicious update) or #5 (modification in transit). |
| CWE-494 | Download of Code Without Integrity Check | #10 → #7 | Allowed | Trust acceptance event (#10): downloaded code is treated as authoritative without integrity verification, enabling tampered binaries/updates. Per R-EXEC, the downloaded code subsequently executes — append → #7. |
| CWE-506 | Embedded Malicious Code | #10 | Allowed | Presence of malicious code implies a supply chain or insider threat (#10). |
| CWE-510 | Trapdoor | #10 | Allowed | Trapdoor/backdoor inserted into the product before delivery — supply-chain insertion at the trust-acceptance event. Decision tree Q8 -> #10. |
| CWE-511 | Logic/Time Bomb | #10 | Allowed | Logic/time bomb inserted into code awaiting a trigger condition — supply-chain or insider insertion. Decision tree Q8 -> #10. |
| CWE-829 | Inclusion of Functionality from Untrusted Control Sphere | #10 → #7 | Allowed | Trust acceptance event (#10): the product loads functionality (library, script, plugin) from outside its intended security domain. Per R-EXEC, included functionality runs in the host's execution context — append → #7. |
| CWE-830 | Inclusion of Web Functionality from an Untrusted Source | #10 → #7 | Allowed | Trust acceptance event (#10): the page imports executable functionality (script, widget) from an untrusted external sphere. Per R-EXEC, the included script runs in the page context — append → #7. |
| CWE-1101 | Reliance on Runtime Component in Generated Code | #10 | Allowed | Generated code relies on a runtime component that may be missing, mismatched, or substituted, exposing the deployment to supply-chain risk. Decision tree Q8 -> #10. |
| CWE-1291 | Public Key Re-Use for Signing both Debug and Production Code | #10 | Allowed | Same public key trusted for both debug and production signing — debug signing capability authenticates production-grade artifacts. Supply-chain key-management flaw. Decision tree Q8 -> #10. |
| CWE-1297 | Unprotected Confidential Information on Device is Accessible by OSAT Vendors | #10 | Allowed | Confidential information left unprotected on the device after manufacturing/supply-chain stages. Decision tree Q8 -> #10 (supply-chain handoff event). |
| CWE-1357 | Reliance on Insufficiently Trustworthy Component | #10 \| #2 \| #3 | Allowed | Reliance on a component whose trustworthiness is insufficient (untracked provenance, abandonware, suspicious supply chain). Context-dependent under the v2.6 subversion test: where the component or its supplier was subverted and the subverted artifact is accepted as authoritative, #10 at the Trust Acceptance Event; where it is merely flawed, the flaw is classified where it is exploited — #2 or #3 per R-ROLE. Decision tree Q8. |
