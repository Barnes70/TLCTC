---
type: "term"
title: "SSRF (Server-Side Request Forgery)"
description: "An industry label for an effect, not for a generic vulnerability: a server is induced to issue requests to destinations the attacker chooses, such as cloud metadata endpoints, internal services, or RFC 1918 hosts."
resource: "tlctc:term:ssrf-server-side-request-forgery"
tags:
  - "glossary"
---
# SSRF (Server-Side Request Forgery)

An industry label for an effect, not for a generic vulnerability: a server is induced to issue requests to destinations the attacker chooses, such as cloud metadata endpoints, internal services, or RFC 1918 hosts. TLCTC therefore does **not** assign SSRF one cluster: it splits into `#1 Abuse of Functions` or `#2 Exploiting Server` depending on the abused capability. Decision rule: *did the abused capability execute as designed, just for a forbidden target?*

- **Yes → `#1 Abuse of Functions`.** The endpoint is meant to fetch a URL — image optimizer, link preview, webhook tester, document/PDF renderer, import-from-URL, a rewrites/proxy feature. The attacker supplies a valid input of an expected type, the fetch function runs correctly, and only the target is forbidden; inputs stay data and no foreign code is introduced (per the #1 boundary tests). A missing or bypassed allowlist is the *bypass primitive*, not the abused capability, and does not move the cluster. Examples: CVE-2026-44578 (Next.js WebSocket-upgrade SSRF), the Next.js image-optimizer SSRFs, Capital One 2019.
- **No → `#2 Exploiting Server`.** The outbound request exists only because server-side implementation is broken: URL-parser confusion, mishandled redirects, DNS rebinding in the fetch logic, or an XXE that makes the XML parser resolve an external entity. No designed fetch capability was used as intended — a flaw manufactured the request.

SSRF is never a complete threat statement (Axiom IV) — it is a position-acquisition step and must be written as a sequence. Cloud-credential theft via the instance metadata service is `#1 → #4` (fetch function abused to read `169.254.169.254`, returned IAM credentials then applied per R-CRED); reaching and then exploiting an unexposed internal service is `#1 → #2`; the XXE-driven variant starts at `#2`.

The split drives control placement: for `#1` the fetch feature itself is the surface to defend (allowlist / `remotePatterns`, protocol and response-size limits, outbound egress policy, IMDSv2) — input validation and WAF signatures are weak there because the input *is* valid; for `#2` the defence is fixing the flaw and hardening the trust check that failed to run.

**Reference:** Core paper §4 (#1 boundary tests); V1.9.1 Buzz-Word Refinement (#1, #2)

**Related reading:** [CVE-2026-44578: Next.js WebSocket SSRF](https://www.tlctc.net/cve-2026-44578.html)

See also: Abuse of Functions (#1), Exploiting Server (#2), XXE (XML External Entity) Injection, Implementation Flaw, Position Acquisition vs Position Exploitation
