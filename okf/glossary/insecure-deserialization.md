---
type: "term"
title: "Insecure Deserialization"
description: "A class of implementation flaw where an application deserializes untrusted data without proper validation, potentially allowing arbitrary code execution or object manipulation."
resource: "tlctc:term:insecure-deserialization"
tags:
  - "glossary"
---
# Insecure Deserialization

A class of implementation flaw where an application deserializes untrusted data without proper validation, potentially allowing arbitrary code execution or object manipulation. In TLCTC: maps to `#2 Exploiting Server` or `#3 Exploiting Client` depending on the role of the vulnerable component per R-ROLE. The deserialization flaw creates an unintended data→code transition via an implementation defect.

**Reference:** V1.9.1 Buzz-Word Refinement (#2, #3)

See also: Exploiting Server (#2), Exploiting Client (#3), Implementation Flaw
