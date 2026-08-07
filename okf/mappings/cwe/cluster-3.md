---
type: "mapping-set"
title: "CWE weaknesses → #3 Exploiting Client"
description: "6 CWE weaknesses entries mapped to TLCTC #3 Exploiting Client."
resource: "tlctc:mapping:cwe:cluster-3"
tags:
  - "mapping"
  - "cwe"
  - "cluster-3"
---
# CWE weaknesses → #3 Exploiting Client

> Source: MITRE CWE → TLCTC mapping (`mappings/mitre-cwe/`). AI-generated, human-reviewed; experimental.

Mapped entries: **6**. Cluster: [#3 Exploiting Client](/clusters/cluster-3.md).

| CWE | Name | TLCTC | Verdict | Rationale |
|---|---|---|---|---|
| CWE-64 | Windows Shortcut Following (.LNK) | #3 | Allowed | .LNK flaws are typically client-side exploits where the user navigates a folder/file, often exploiting the shell/explorer. |
| CWE-525 | Use of Web Browser Cache Containing Sensitive Information | #3 | Allowed | Browser cache contains sensitive information that other clients can retrieve (e.g., shared kiosk, malware reading cache files). Client-role implementation flaw -> #3. |
| CWE-539 | Use of Persistent Cookies Containing Sensitive Information | #3 | Allowed | Persistent cookies hold sensitive information that survives session end and is exposed to local malware or shared-machine attackers. Client-role implementation flaw -> #3. |
| CWE-618 | Exposed Unsafe ActiveX Method | #3 | Allowed | ActiveX control exposes an unsafe method that any web page can invoke once the control is instantiated. Client-role component vulnerability -> #3. |
| CWE-623 | Unsafe ActiveX Control Marked Safe For Scripting | #3 | Allowed | ActiveX control marked Safe-For-Scripting despite exposing dangerous functionality — any web page can drive the dangerous behavior. Client-role component vulnerability -> #3. |
| CWE-1236 | Improper Neutralization of Formula Elements in a CSV File | #3 | Allowed | CSV Injection attacks the client spreadsheet application (#3). |
