---
type: "term"
title: "Call-Level Mapping Rule"
description: "A TLCTC classification principle for function call level threat analysis: Parameter tampering , unauthorized function selection, or misuse of valid functions without executing foreign code → always 1 Abuse of Functions ."
resource: "tlctc:term:call-level-mapping-rule"
tags:
  - "glossary"
---
# Call-Level Mapping Rule

A TLCTC classification principle for function-call-level threat analysis:

- **Parameter tampering**, unauthorized function selection, or misuse of valid functions without executing foreign code → always `#1 Abuse of Functions`.
- **Presentation of identity artifacts** at call time (e.g., stolen API keys, session tokens, cookies, Kerberos tickets) to impersonate a subject → always `#4 Identity Theft`.

This rule prevents overlap between logic misuse (`#1`) and identity presentation/use (`#4`) at the function call level, where the caller acts as "client" and the called function as "server".

**Reference:** V1.9.1 §Concept Applicability (At Function Call Level)

See also: Abuse of Functions (#1), Identity Theft (#4)
