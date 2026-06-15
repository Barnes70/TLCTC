---
type: "term"
title: "Credential Forgery"
description: "The act of creating a credential without possessing the legitimate secret."
resource: "tlctc:term:credential-forgery"
tags:
  - "glossary"
---
# Credential Forgery

The act of creating a credential without possessing the legitimate secret. If forgery succeeds due to an implementation flaw (e.g., weak signing algorithm, missing validation, predictable tokens), the forgery step maps to `#2` or `#3` per R-ROLE. The subsequent use of the forged credential maps to `#4`.

**Reference:** §4.2.2 (Global Definitions), R-CRED (§4.2.5)
