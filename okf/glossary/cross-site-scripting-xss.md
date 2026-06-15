---
type: "term"
title: "Cross-Site Scripting (XSS)"
description: "A class of implementation flaw where an application includes untrusted data in web output without proper validation or encoding, allowing attacker controlled scripts to execute in a victim's browser."
resource: "tlctc:term:cross-site-scripting-xss"
tags:
  - "glossary"
---
# Cross-Site Scripting (XSS)

A class of implementation flaw where an application includes untrusted data in web output without proper validation or encoding, allowing attacker-controlled scripts to execute in a victim's browser. In TLCTC:

- **Stored/Reflected XSS** (server fails to encode output): `#2 Exploiting Server` — the flaw is in server-side code.
- **DOM-Based XSS** (client script processes data unsafely): `#3 Exploiting Client` — the flaw is in client-side code.

In both cases, the XSS creates an unintended data→code transition via an implementation flaw.

**Reference:** V1.9.1 §Definitions (#2, #3), Buzz-Word Refinement

See also: Exploiting Server (#2), Exploiting Client (#3), Implementation Flaw

---
