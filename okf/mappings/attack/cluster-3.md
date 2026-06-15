---
type: "mapping-set"
title: "ATT&CK techniques → #3 Exploiting Client"
description: "2 ATT&CK techniques entries mapped to TLCTC #3 Exploiting Client."
resource: "tlctc:mapping:attack:cluster-3"
tags:
  - "mapping"
  - "attack"
  - "cluster-3"
---
# ATT&CK techniques → #3 Exploiting Client

> Source: MITRE ATT&CK Enterprise → TLCTC mapping (`mappings/mitre-attack-enterprise/`).

Mapped entries: **2**. Cluster: [#3 Exploiting Client](/clusters/cluster-3.md).

| Technique | Name | TLCTC | Rationale |
|---|---|---|---|
| T1189 | Drive-by Compromise | #3 → #7 | Victim browser/client requests content from an attacker-controlled or compromised site; the response exploits a client-side implementation flaw in the browser or plugin (#3 per R-ROLE — flawed component is in client role) and triggers attacker-supplied execution (#7 per R-EXEC). Path: `#3 \|\|[client][@External→@Org]\|\| → #7`. When the malicious site is itself a third-party legitimate site that was compromised, mark it as transit: `#3 \|\|[client][@External⇒@CompromisedSite→@Org]\|\| → #7`. |
| T1203 | Exploitation for Client Execution | #3 → #7 | Exploitation for client execution: attacker-crafted content (document, image, font, archive, web page) triggers an implementation flaw in a client-role component (browser, document reader, email client, plugin) — `#3` per R-ROLE. The exploit payload then runs attacker-controlled code on the @Org host — `#7` per R-EXEC. Cluster corrected from prior `#3`-only — the technique is by definition "for execution" and the `#7` step was missing per R-EXEC. Path: `#3 \|\|[client][@External→@Org]\|\| → #7`. |
