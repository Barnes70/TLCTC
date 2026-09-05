---
type: "term"
title: "R-SCOPE (Entitlement Scope Boundary)"
description: "Admission rule for the whole registry: a step is classified under a cluster only where the action fell outside the entitlement envelope an accountable grantor actually conferred for it."
resource: "tlctc:term:r-scope-entitlement-scope-boundary"
tags:
  - "glossary"
---
# R-SCOPE (Entitlement Scope Boundary)

Admission rule for the whole registry: a step is classified under a cluster only where the action fell **outside the entitlement envelope** an accountable grantor actually conferred for it. Cause-side classification asks three questions in strict order — is there an actor; did they intend the outcome; did an accountable grantor confer an entitlement covering *this* action — and only an intended, unentitled action enters the Attack row where the clusters apply (implementation flaw required → `#2/#3` per R-ROLE; otherwise `#1`). No actor is failure or external event; an unintended outcome is Error in Use; an intended in-grant action is **Abuse of Rights** — operational risk, no cluster, no System Risk Event, the consequence chain starting at the DRE. Entitlement means entitled, not permitted, and attaches to the person, not the token: credential use by anyone other than the grantee is never inside an envelope (`#4` per R-CRED, subsequent function use `#1`), and exploiting an implementation flaw is never inside any grant. Not an actor test (Axiom IV). Entitlement is tested after intent and before the code-flaw test because an entitled actor exploiting a code flaw is an attack.

**Reference:** Core paper §3.5, §6.1; dictionary `rules[R-SCOPE]`, `cause_side_partition`

See also: Cause-Side Partition, Abuse of Rights, Entitlement, Error in Use, R-CRED
