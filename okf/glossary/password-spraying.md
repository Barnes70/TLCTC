---
type: "term"
title: "Password Spraying"
description: "An attack that tries a small number of commonly used passwords against many accounts simultaneously, avoiding account lockout thresholds."
resource: "tlctc:term:password-spraying"
tags:
  - "glossary"
---
# Password Spraying

An attack that tries a small number of commonly used passwords against many accounts simultaneously, avoiding account lockout thresholds. In TLCTC: maps to `#4 Identity Theft` — the attacker is attempting to derive valid credentials to impersonate a legitimate identity. The generic vulnerability is the insufficient binding, at the point of authentication, between a presented credential and the authentic holder: a guessed valid password is accepted as if from the legitimate holder when controls such as MFA or lockout are absent (predictable passwords widen the guess space).

**Reference:** V1.9.1 Buzz-Word Refinement (#4)

See also: Identity Theft (#4), Brute-Force Attack
