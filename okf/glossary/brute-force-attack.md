---
type: "term"
title: "Brute-Force Attack"
description: "A method of systematically trying all possible credential combinations (passwords, PINs, encryption keys) to gain unauthorized access."
resource: "tlctc:term:brute-force-attack"
tags:
  - "glossary"
---
# Brute-Force Attack

A method of systematically trying all possible credential combinations (passwords, PINs, encryption keys) to gain unauthorized access. In TLCTC: maps to `#4 Identity Theft` — the attacker is attempting to derive and use credentials to impersonate a legitimate identity. The generic vulnerability is the insufficient binding, at the point of authentication, between a presented credential and the authentic holder: the endpoint cannot distinguish a guessing attacker from the legitimate holder when controls such as account lockout, rate-limiting, or strong-password requirements are absent. (Weak credential *storage/protection* is a separate, acquisition-side concern that classifies to the enabling cluster, not #4.)

**Reference:** V1.9.1 Buzz-Word Refinement (#4)

See also: Identity Theft (#4), Password Spraying, Credential / Identity Artifact
