---
type: "term"
title: "Trust Acceptance Event (TAE)"
description: "The moment your domain honors the Third Party Trust Link and treats a Trust Artifact/Decision as authoritative."
resource: "tlctc:term:trust-acceptance-event-tae"
tags:
  - "glossary"
---
# Trust Acceptance Event (TAE)

The moment your domain **honors** the Third-Party Trust Link and treats a Trust Artifact/Decision as authoritative. Actions at TAE include: validate, accept, install, apply, execute, attach privileges. `#10 Supply Chain Attack` is placed at the TAE. `#10` requires the accepted artifact, or the third party issuing it, to have been subverted before acceptance (subversion test, core §4). Planting counts as subversion: an attacker-authored artifact placed in a channel the target trusts (a malicious package on a public registry, an image or model on a trusted hub, a dependency served under a trusted name) is a subverted service response of that channel, and its acceptance is the TAE. In federation, presenting an assertion as another identity is `#4`; a service provider honouring an assertion from an identity provider that was not subverted is not a step; `#10` applies only where the identity provider or its federation trust material was itself subverted (`#10 → #4`).

**Reference:** Handbook §4.2.2 (Global Definitions), R-SUPPLY (§4.2.5), §4.1 (#10 Definition); Core paper §9, §6.1, §4
