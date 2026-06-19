---
type: "term"
title: "Ransomware"
description: "Malware that encrypts a victim's data and demands payment for the decryption key."
resource: "tlctc:term:ransomware"
tags:
  - "glossary"
---
# Ransomware

Malware that encrypts a victim's data and demands payment for the decryption key. In TLCTC: the execution of the ransomware binary maps to `#7 Malware` (foreign code executed via designed execution capability). The resulting data encryption is a Data Risk Event: `[DRE: Ac]` (Loss of Accessibility — data exists but is unusable). Note: this is Loss of **Accessibility**, not Loss of Availability (the encrypted files still exist on disk). A full ransomware attack path typically involves multiple clusters, e.g., `#9 → #7 → #7 → #4 → #1 → #7` as seen in the Emotet/Ryuk case study (the final `#1 → #7` is sequential — function abuse deploys the payload, which then executes; per §11.2.2 a known order uses `→`, not a parallel group).

**Reference:** V1.9.1 §Definitions (#7), §Data Risk Event Types, §E (Emotet@Heise)




**Related reading:** [AD → Domain Admin → Ransomware cascade](https://www.tlctc.net/ad-ransomware-tlctc-cascade.html), [Chaos Ransomware — TLCTC forensic](https://www.tlctc.net/chaos-ransomware-tlctc-analysis.html), [Verizon DBIR 2025 — TLCTC](https://www.tlctc.net/tlctc-dbir-2025.html), [20 annotated attack paths (Ransomware, BEC, OT, ...)](https://www.tlctc.net/tlctc-attack-path-examples.html)

See also: Malware (#7), Accessibility (Data Risk Event), Loss of Accessibility
