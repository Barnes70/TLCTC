---
type: "term"
title: "Client-Server Relationship"
description: "A fundamental principle (Axiom II) stating that every software system interaction — networked or intra system — is based on client server or caller called function interaction at various levels."
resource: "tlctc:term:client-server-relationship"
tags:
  - "glossary"
---
# Client-Server Relationship

A fundamental principle (Axiom II) stating that every software system interaction — networked or intra-system — is based on client-server or caller-called function interaction at various levels. A network is not a precondition: a syscall, hypercall, or IPC call establishes the same caller-called relation as a remote protocol exchange. The relationship is contextual: the entity requesting a service is the "client," and the entity providing that service is the "server". Roles can be dynamic and change depending on interaction context, particularly across protection ring boundaries.
