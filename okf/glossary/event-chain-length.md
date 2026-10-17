---
type: "term"
title: "Event Chain Length"
description: "The number of events between the initial incident (E1) and the event at which a regulatory duty arises (E3x)."
resource: "tlctc:term:event-chain-length"
tags:
  - "glossary"
---
# Event Chain Length

The number of events between the initial incident (E1) and the event at which a regulatory duty arises (E3x). Shorter chains mean a duty can arise sooner. Under v2.7 the duty itself is reached by a normative edge with no Δt, and its clock starts at awareness, not at the triggering event: the deadline bounds the response process from awareness. Example: NIS2 path (E1→E3b) = 2 events, early warning within 24h of becoming aware of a significant incident; GDPR path (E1→E2→E3a) = 3 events, notification within 72h of becoming aware of a personal-data breach. Understanding chain length helps CISOs structure incident response playbooks to meet multiple regulatory timelines from a single incident.
