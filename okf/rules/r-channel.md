---
type: "rule"
title: "R-CHANNEL"
description: "If the defective logic is itself a communication-path control — peer authenticity (certificate validation, chain of trust, hostname matching, expiry or revocation checking), channel encryption, or algorithm negotiation — the generic vulnerability is the lack of sufficient control over the communication path and the weakness classifies as #5, not as #2 or #3 under R-ROLE."
resource: "tlctc:rule:R-CHANNEL"
tags:
  - "taxonomy"
  - "rule"
  - "must"
enforcement_level: "must"
machine_enforceable: false
---
# R-CHANNEL

If the defective logic is itself a communication-path control — peer authenticity (certificate validation, chain of trust, hostname matching, expiry or revocation checking), channel encryption, or algorithm negotiation — the generic vulnerability is the lack of sufficient control over the communication path and the weakness classifies as #5, not as #2 or #3 under R-ROLE. R-ROLE governs only where the defect is incidental to the control rather than constitutive of it.

> v2.4 addition. R-CHANNEL is the #5 counterpart to R-FLOOD: both resolve the same ambiguity — a weakness describable either as 'a control failed' or as 'the code was wrong' — in favour of the specific generic vulnerability rather than the residual code-flaw test. A missing or incorrect certificate check is not incidentally a code defect; it IS the absence of control over the communication path, which is #5's generic vulnerability (see also the #5 Developer's View, which names certificate/path validation). The rule is constitutive-versus-incidental, not server-versus-client: memory corruption in a TLS parser remains #2/#3 per R-ROLE, because the exploited generic vulnerability there is the code flaw, not the control. R-CHANNEL classifies the weakness; R-MITM sequences the attack path (position acquisition versus action) and is unaffected.

# Schema

- **Enforcement level:** must
- **Machine enforceable:** false
