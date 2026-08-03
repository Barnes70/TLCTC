---
type: "term"
title: "R-ROLE (Server vs Client Determination)"
description: "Global mapping rule: If the vulnerable component accepts and handles inbound requests relative to the attacker, classify as 2 Exploiting Server ."
resource: "tlctc:term:r-role-server-vs-client-determination"
tags:
  - "glossary"
---
# R-ROLE (Server vs Client Determination)

Global mapping rule: If the vulnerable component accepts and handles inbound requests relative to the attacker, classify as `#2 Exploiting Server`. If the vulnerable component consumes external responses/content relative to the attacker, classify as `#3 Exploiting Client`. Roles are established by call direction at **any** interface, including intra-system privilege interfaces (syscall, hypercall, IPC, driver IOCTL) — a network is not a precondition. A kernel handling a crafted syscall from a lower-privileged process is in server-role (`#2`). Per R-INTRA-7, the boundary crossing itself remains an observability annotation and MUST NOT be treated as a classification input.

**Reference:** §4.2.5 (R-ROLE)

**Related reading:** [Calif M5: #2 → #2 (Kernel's Role pt 1)](https://www.tlctc.net/calif-tlctc-chain.html), [Kernel as Client: CVE-2025-21333 (Kernel's Role pt 2)](https://www.tlctc.net/hyperv-vsp-tlctc-client.html), [Apache 2.4.67 — 11 CVEs decomposed](https://www.tlctc.net/apache-2.4.67-tlctc-analysis.html)
