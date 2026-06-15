---
type: "term"
title: "Pass-the-Hash / Pass-the-Ticket"
description: "Attack techniques where an attacker uses captured NTLM hashes (Pass the Hash) or Kerberos tickets (Pass the Ticket) to authenticate as a legitimate user without knowing the actual password."
resource: "tlctc:term:pass-the-hash-pass-the-ticket"
tags:
  - "glossary"
---
# Pass-the-Hash / Pass-the-Ticket

Attack techniques where an attacker uses captured NTLM hashes (Pass-the-Hash) or Kerberos tickets (Pass-the-Ticket) to authenticate as a legitimate user without knowing the actual password. In TLCTC: the **acquisition** of the hash/ticket maps to the enabling cluster (e.g., `#7` if extracted by malware, `#1` if via lsass dump using a legitimate tool). The **use** of the hash/ticket to authenticate always maps to `#4 Identity Theft` per R-CRED.

**Reference:** V1.9.1 Buzz-Word Refinement (#4)

See also: Identity Theft (#4), Credential Acquisition, Credential Application
