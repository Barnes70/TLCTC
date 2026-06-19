---
type: "term"
title: "RCE (Remote Code Execution)"
description: "A commonly used but imprecise term describing CVEs that enable an attacker to execute arbitrary code on a remote target."
resource: "tlctc:term:rce-remote-code-execution"
tags:
  - "glossary"
---
# RCE (Remote Code Execution)

A commonly used but imprecise term describing CVEs that enable an attacker to execute arbitrary code on a remote target. In TLCTC, "RCE" always conflates the vulnerability with its exploitation and MUST be decomposed:

- The **vulnerability** that enables execution: `#2 Exploiting Server` (server-side flaw) or `#3 Exploiting Client` (client-side flaw)
- The **actual execution** of foreign code: `#7 Malware`
- Correct notation: `#2 → #7` or `#3 → #7`

This decomposition is essential because it identifies two distinct generic vulnerabilities being exploited, each requiring different controls.

**Reference:** V1.9.1 §F (Industry Term Decomposition)




**Related reading:** [Calif M5: #2 → #2 (Kernel's Role pt 1)](https://www.tlctc.net/calif-tlctc-chain.html), [Kernel as Client: CVE-2025-21333 (Kernel's Role pt 2)](https://www.tlctc.net/hyperv-vsp-tlctc-client.html), [Apache 2.4.67 — 11 CVEs decomposed](https://www.tlctc.net/apache-2.4.67-tlctc-analysis.html)

See also: Exploiting Server (#2), Exploiting Client (#3), Malware (#7)
