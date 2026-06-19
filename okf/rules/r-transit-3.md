---
type: "rule"
title: "R-TRANSIT-3"
description: "Vendor code running on the target device is NOT transit."
resource: "tlctc:rule:R-TRANSIT-3"
tags:
  - "taxonomy"
  - "rule"
  - "must"
enforcement_level: "must"
machine_enforceable: false
---
# R-TRANSIT-3

Vendor code running on the target device is NOT transit. Software executing on the victim's own device is the attack surface, classified by R-ROLE (typically #3), not a transit (relay/carrier) party.

# Schema

- **Enforcement level:** must
- **Machine enforceable:** false
