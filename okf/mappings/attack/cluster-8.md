---
type: "mapping-set"
title: "ATT&CK techniques → #8 Physical Attack"
description: "4 ATT&CK techniques entries mapped to TLCTC #8 Physical Attack."
resource: "tlctc:mapping:attack:cluster-8"
tags:
  - "mapping"
  - "attack"
  - "cluster-8"
---
# ATT&CK techniques → #8 Physical Attack

> Source: MITRE ATT&CK Enterprise → TLCTC mapping (`mappings/mitre-attack-enterprise/`).

Mapped entries: **4**. Cluster: [#8 Physical Attack](/clusters/cluster-8.md).

| Technique | Name | TLCTC | Rationale |
|---|---|---|---|
| T1091 | Replication Through Removable Media | #8 → #7 | Removable media physically introduced into an @Org host (#8) carries foreign executable content that runs via autorun, user double-click, or scheduled scan (#7 per R-EXEC). For lateral-movement context, the prior compromised host is the source @Org sphere and the new host is the target @Org sphere — same @Org boundary, different hosts. Path: `#8 \|\|[physical][@Org→@Org]\|\| → #7`. |
| T1092 | Communication Through Removable Media | #8 | Communication Through Removable Media: bridge an air-gapped @Org segment by carrying C2 messages on physical media that cycles between connected and disconnected systems (USB sneakernet). The boundary crossing is physical — `#8`. Path: `#8 \|\|[physical][@Org→@Org]\|\|` (between connected and disconnected @Org segments) or `#8 \|\|[physical][@External→@Org]\|\|` when the medium originates outside. |
| T1200 | Hardware Additions | #8 | Attacker physically attaches malicious hardware (USB drop, rogue keyboard/HID, network tap, implanted device) to @Org infrastructure. Generic vulnerability is the trust placed in physical port/connector contact — #8. Path: `#8 \|\|[physical][@External→@Org]\|\|`. When the device subsequently runs attacker code on @Org systems, append `→ #7` per R-EXEC. |
| T1601.002 | Modify System Image: Downgrade System Image | #8 → #7 | Downgrade System Image: physically reflash device to an older, exploitable image version. Physical access required — `#8 → #7`. |
