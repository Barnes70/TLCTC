---
type: "term"
title: "Identity Theft (#4)"
description: "A threat cluster where an attacker targets weaknesses in identity and access management processes or credential protection mechanisms to illegitimately misuse authentication credentials (passwords, tokens, keys, session identifiers, biometrics) to impersonate a legitimate identity (human or technical)."
resource: "tlctc:term:identity-theft-4"
tags:
  - "glossary"
---
# Identity Theft (#4)

A threat cluster where an attacker targets weaknesses in identity and access management processes or credential protection mechanisms to illegitimately misuse authentication credentials (passwords, tokens, keys, session identifiers, biometrics) to impersonate a legitimate identity (human or technical). The generic vulnerability is weak Identity Management Processes and/or inadequate credential protection mechanisms throughout the identity lifecycle.

**Critical distinction:** Credentials have dual operational nature:

- **Acquisition/Exposure:** When credentials are obtained through another cluster (e.g., #2 SQL injection, #5 MitM, #7 keylogger, #9 Phishing), map to the enabling cluster (Loss of Confidentiality consequence)
- **Use/Application:** The subsequent *use* of acquired credentials—regardless of acquisition method—always maps to #4 Identity Theft (Loss of Control / system compromise event)

Non-Overlap Rule: Credential acquisition maps to the enabling threat cluster; credential use always maps to #4.

**Related reading:** [AD → Domain Admin → Ransomware cascade](https://www.tlctc.net/ad-ransomware-tlctc-cascade.html), [CVE-2026-35414: 15-year-old OpenSSH cert flaw](https://www.tlctc.net/cve-2026-35414.html), [CrowdStrike 2025 Threat Hunting Report — TLCTC](https://www.tlctc.net/tlctc-crowdstrike-2025-analysis.html), [CrowdStrike 2025 Global Threat Report — TLCTC](https://www.tlctc.net/tlctc-crowdstrike-2025-report.html), [CrowdStrike 2025 Threat Report — Strategy & Velocity](https://www.tlctc.net/tlctc-crowdstrike-2025-threat-report.html), [Verizon DBIR 2025 — TLCTC](https://www.tlctc.net/tlctc-dbir-2025.html), [blog-MFAbypass.html](https://www.tlctc.net/blog-MFAbypass.html)
