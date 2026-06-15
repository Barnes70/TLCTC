---
type: "term"
title: "SSRF (Server-Side Request Forgery)"
description: "An implementation flaw where an attacker induces the server to make requests to unintended locations, potentially accessing internal resources or services."
resource: "tlctc:term:ssrf-server-side-request-forgery"
tags:
  - "glossary"
---
# SSRF (Server-Side Request Forgery)

An implementation flaw where an attacker induces the server to make requests to unintended locations, potentially accessing internal resources or services. In TLCTC: maps to `#2 Exploiting Server` — a coding flaw in how server-side code processes URL input. The server is in "server role" (accepting inbound requests) and the flaw is in its implementation.

**Reference:** V1.9.1 Buzz-Word Refinement (#2)




**Related reading:** [CVE-2026-44578: Next.js WebSocket SSRF](https://www.tlctc.net/cve-2026-44578.html)

See also: Exploiting Server (#2), Implementation Flaw
