---
type: "rule"
title: "R-ROLE"
description: "Classify by the role of the component containing the flaw relative to the attacker: server-role flaw = #2, client-role flaw = #3."
resource: "tlctc:rule:R-ROLE"
tags:
  - "taxonomy"
  - "rule"
  - "must"
enforcement_level: "must"
machine_enforceable: false
---
# R-ROLE

Classify by the role of the component containing the flaw relative to the attacker: server-role flaw = #2, client-role flaw = #3. Roles are established by call direction at any interface, including intra-system privilege interfaces (syscall, hypercall, IPC, driver IOCTL); a network is not a precondition.

> v2.4 clarification. A kernel handling a crafted syscall from a lower-privileged process is in server-role for that interaction (#2); a higher-privileged component consuming data or responses returned from a lower-privileged one is in client-role (#3). Per R-INTRA-7 the boundary crossing itself remains an observability annotation and MUST NOT be treated as a classification input — the cluster follows from the role at the interface, exactly as it does across a network.

# Schema

- **Enforcement level:** must
- **Machine enforceable:** false
