---
type: "term"
title: "Privilege Escalation"
description: "A commonly used but multi faceted term describing an attacker gaining higher level permissions than initially authorized."
resource: "tlctc:term:privilege-escalation"
tags:
  - "glossary"
---
# Privilege Escalation

A commonly used but multi-faceted term describing an attacker gaining higher-level permissions than initially authorized. In TLCTC: privilege escalation is **not a single cluster** — it maps to different clusters depending on the technique employed:

- **Via software vulnerability** (buffer overflow, injection flaw): `#2 Exploiting Server` or `#3 Exploiting Client` per R-ROLE
- **Via misuse of legitimate features** (misconfiguration, overly permissive defaults): `#1 Abuse of Functions`
- **Via stolen credentials** (using admin credentials): `#4 Identity Theft`
- **Via social engineering** (manipulating users into granting access): `#9 Social Engineering`

Distinguishing the underlying technique allows for more targeted control implementation. The Intra-System Boundary Operator (`|[privilege][@from→@to]|`) can annotate privilege escalation in attack paths without changing cluster classification.

**Reference:** V1.9.1 Clarifications




**Related reading:** [AD → Domain Admin → Ransomware cascade](https://www.tlctc.net/ad-ransomware-tlctc-cascade.html), [Calif M5: #2 → #2 (Kernel's Role pt 1)](https://www.tlctc.net/calif-tlctc-chain.html), [CVE-2026-31431 (Copy Fail): Linux kernel AF_ALG](https://www.tlctc.net/cve-2026-31431.html), [CVE-2026-46300 (Fragnesia): Linux kernel XFRM](https://www.tlctc.net/cve-2026-46300.html)

See also: Abuse of Functions (#1), Exploiting Server (#2), Identity Theft (#4), Intra-System Boundary Operator
