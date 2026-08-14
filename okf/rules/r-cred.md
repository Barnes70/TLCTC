---
type: "rule"
title: "R-CRED"
description: "Credential acquisition maps to the enabling cluster."
resource: "tlctc:rule:R-CRED"
tags:
  - "taxonomy"
  - "rule"
  - "must"
enforcement_level: "must"
machine_enforceable: false
---
# R-CRED

Credential acquisition maps to the enabling cluster. Credential application (use of the credential to authenticate) is ALWAYS classified as #4 Identity Theft, regardless of the acquisition method, PROVIDED the identity claimed is not the presenter's own. A credential issued to the presenter by the target system through a designed enrolment function makes the presenter its authentic holder; such use MUST NOT be classified as #4, and where the enrolment function granted the identity or its permissions outside their intended population or scope, the enrolment step maps to #1. These are separate attack steps.

> v2.5.1 clarification (self-issued identity). Makes normative in the rule registry what the #4 generic_vulnerability already implies ('the authentic holder of the identity it claims'): when the target system itself issued the credential to the presenter, the point-of-authentication binding between presented credential and authentic holder is intact, so authentication as self exploits no #4 generic vulnerability — the exploited generic vulnerability is the scope of the enrolment function and of the permissions attached to the resulting principal (#1). Examples (non-normative): fictitious or pseudonymous self-registration is #1, no identity being impersonated; enrolment completed AS an existing identity (e.g. domain-based auto-affiliation, or identity verification satisfied via prior access to the victim's mailbox) is #1 -> #4 — the enrolment abuse is #1, the subsequent authentication as the victim is #4. NOT fully classification-preserving: records that classified use of a self-enrolled account as #4 SHOULD be re-checked.

# Schema

- **Enforcement level:** must
- **Machine enforceable:** false
