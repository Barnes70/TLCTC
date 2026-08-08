---
type: "term"
title: "R-CHANNEL (Channel Control vs Code Flaw)"
description: "Global mapping rule (v2.5): If the defective logic is itself a communication path control — peer authenticity (certificate validation, chain of trust, hostname matching, expiry or revocation checking), channel encryption, or algorithm negotiation — the generic vulnerability is the lack of sufficient control over the communication path and the weakness classifies as 5 Man in the Middle , not as 2 or 3 under R ROLE."
resource: "tlctc:term:r-channel-channel-control-vs-code-flaw"
tags:
  - "glossary"
---
# R-CHANNEL (Channel Control vs Code Flaw)

Global mapping rule (v2.5): If the defective logic is itself a communication-path control — peer authenticity (certificate validation, chain of trust, hostname matching, expiry or revocation checking), channel encryption, or algorithm negotiation — the generic vulnerability is the lack of sufficient control over the communication path and the weakness classifies as `#5 Man in the Middle`, not as `#2` or `#3` under R-ROLE. R-ROLE governs only where the defect is incidental to the control rather than constitutive of it (for example, memory corruption in a TLS parser).

R-CHANNEL classifies the *weakness*; R-MITM sequences the *attack path* (position acquisition versus action). The two do not conflict.

**Reference:** §6.1 (R-CHANNEL)
