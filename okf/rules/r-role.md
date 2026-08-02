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

# Schema

- **Enforcement level:** must
- **Machine enforceable:** false
