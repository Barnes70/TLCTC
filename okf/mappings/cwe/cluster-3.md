---
type: "mapping-set"
title: "CWE weaknesses → #3 Exploiting Client"
description: "12 CWE weaknesses entries mapped to TLCTC #3 Exploiting Client."
resource: "tlctc:mapping:cwe:cluster-3"
tags:
  - "mapping"
  - "cwe"
  - "cluster-3"
---
# CWE weaknesses → #3 Exploiting Client

> Source: MITRE CWE → TLCTC mapping (`mappings/mitre-cwe/`). AI-generated, human-reviewed; experimental.

Mapped entries: **12**. Cluster: [#3 Exploiting Client](/clusters/cluster-3.md).

| CWE | Name | TLCTC | Verdict | Rationale |
|---|---|---|---|---|
| CWE-64 | Windows Shortcut Following (.LNK) | #3 | Allowed | .LNK flaws are typically client-side exploits where the user navigates a folder/file, often exploiting the shell/explorer. |
| CWE-295 | Improper Certificate Validation | #3 | Allowed | This is a client-side code implementation flaw (#3) where certificate validation logic is improperly implemented or missing. The vulnerability exists in the client's source code that fails to correctly validate certificates. While this enables MitM scenarios, the threat being exploited is the coding bug itself. |
| CWE-296 | Improper Following of a Certificate's Chain of Trust | #3 | Allowed | Client-side code implementation flaw (#3) in certificate chain validation logic. The developer failed to properly implement chain-of-trust verification in the client software. |
| CWE-297 | Improper Validation of Certificate with Host Mismatch | #3 | Allowed | Client-side code implementation flaw (#3) where hostname verification against certificate CN/SAN is missing or incorrectly implemented. The bug is in the client's validation code. |
| CWE-298 | Improper Validation of Certificate Expiration | #3 | Allowed | Client-side code implementation flaw (#3) where certificate expiration check is missing or improperly implemented in the client software. |
| CWE-299 | Improper Check for Certificate Revocation | #3 | Allowed | Client-side code implementation flaw (#3) where OCSP/CRL revocation checking is missing or improperly implemented. The vulnerability is in the client's certificate handling code. |
| CWE-370 | Missing Check for Certificate Revocation after Initial Check | #3 | Allowed | Client-side code implementation flaw (#3) in session/connection handling where revocation status is not re-validated during long-lived sessions. |
| CWE-525 | Use of Web Browser Cache Containing Sensitive Information | #3 | Allowed | Browser cache contains sensitive information that other clients can retrieve (e.g., shared kiosk, malware reading cache files). Client-role implementation flaw -> #3. |
| CWE-539 | Use of Persistent Cookies Containing Sensitive Information | #3 | Allowed | Persistent cookies hold sensitive information that survives session end and is exposed to local malware or shared-machine attackers. Client-role implementation flaw -> #3. |
| CWE-618 | Exposed Unsafe ActiveX Method | #3 | Allowed | ActiveX control exposes an unsafe method that any web page can invoke once the control is instantiated. Client-role component vulnerability -> #3. |
| CWE-623 | Unsafe ActiveX Control Marked Safe For Scripting | #3 | Allowed | ActiveX control marked Safe-For-Scripting despite exposing dangerous functionality — any web page can drive the dangerous behavior. Client-role component vulnerability -> #3. |
| CWE-1236 | Improper Neutralization of Formula Elements in a CSV File | #3 | Allowed | CSV Injection attacks the client spreadsheet application (#3). |
