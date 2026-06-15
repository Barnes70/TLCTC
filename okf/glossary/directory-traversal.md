---
type: "term"
title: "Directory Traversal"
description: "An attack where an attacker manipulates file path references (e.g., using ../ sequences) to access files or directories outside the intended scope."
resource: "tlctc:term:directory-traversal"
tags:
  - "glossary"
---
# Directory Traversal

An attack where an attacker manipulates file path references (e.g., using `../` sequences) to access files or directories outside the intended scope. In TLCTC: maps to `#2 Exploiting Server` — an implementation flaw in how the server-side code handles file path input, enabling unauthorized access. The flaw is in server-side source code (failure to validate/sanitize path references).

**Reference:** V1.9.1 Buzz-Word Refinement (#2)

See also: Exploiting Server (#2), Implementation Flaw
