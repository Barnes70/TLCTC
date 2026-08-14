---
type: "term"
title: "R-CRED (Credential Lifecycle Non-Overlap)"
description: "Global mapping rule: Credential acquisition maps to the enabling cluster; credential application MUST always map to 4 Identity Theft , provided the identity claimed is not the presenter's own ."
resource: "tlctc:term:r-cred-credential-lifecycle-non-overlap"
tags:
  - "glossary"
---
# R-CRED (Credential Lifecycle Non-Overlap)

Global mapping rule: Credential acquisition maps to the enabling cluster; credential application MUST always map to `#4 Identity Theft`, **provided the identity claimed is not the presenter's own**. If both occur, they MUST be represented as at least two steps: `(enabling cluster) → #4`.

**Self-issued identity (R-CRED proviso).** A credential issued to the presenter by the target system through a designed enrolment function makes the presenter its authentic holder; using it is authentication as self and is NOT `#4`. Where the enrolment function granted the identity or its permissions outside their intended population or scope, that enrolment step maps to `#1`. Fictitious or pseudonymous self-registration is `#1` (no identity impersonated); enrolment completed AS an existing identity is `#1 → #4`. The higher-abstraction test: is the system *deceived about who is authenticating*? Deceived → `#4`; not deceived (it enrolled this principal itself) → the vulnerability is elsewhere, usually `#1`.

**Reference:** §4.2.5 (R-CRED)

**Related reading:** [Cobalt Strike capabilities × TLCTC V2.0](https://www.tlctc.net/tlctc-cobaltstrike-mapping.html)
