---
type: "term"
title: "Session Hijacking"
description: "An attack where an adversary takes over an active session by stealing or predicting session tokens/cookies."
resource: "tlctc:term:session-hijacking"
tags:
  - "glossary"
---
# Session Hijacking

An attack where an adversary takes over an active session by stealing or predicting session tokens/cookies. In TLCTC: the **acquisition** of the session token maps to the enabling cluster (e.g., `#5` if intercepted via MitM, `#3` if stolen via XSS, `#7` if captured by malware). The **use** of the stolen session to impersonate the legitimate user always maps to `#4 Identity Theft` per R-CRED.

**Reference:** V1.9.1 Buzz-Word Refinement (#4)

See also: Identity Theft (#4), Credential Acquisition, Credential Application
