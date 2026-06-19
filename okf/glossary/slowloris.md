---
type: "term"
title: "Slowloris"
description: "An application layer denial of service attack that holds many connections to the target web server open by sending partial HTTP requests, slowly exhausting server connection resources."
resource: "tlctc:term:slowloris"
tags:
  - "glossary"
---
# Slowloris

An application-layer denial of service attack that holds many connections to the target web server open by sending partial HTTP requests, slowly exhausting server connection resources. In TLCTC: maps to `#6 Flooding Attack` — the primary mechanism is exhausting finite connection/thread pool capacity. Although each individual request is small, the aggregate effect overwhelms the server's connection handling capacity.

**Reference:** V1.9.1 Buzz-Word Refinement (#6)

See also: Flooding Attack (#6), DDoS, HTTP Flood
