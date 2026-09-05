---
type: "rule"
title: "R-SCOPE"
description: "A step is classified under a cluster only where the action fell outside the entitlement envelope an accountable grantor actually conferred for it."
resource: "tlctc:rule:R-SCOPE"
tags:
  - "taxonomy"
  - "rule"
  - "must"
enforcement_level: "must"
machine_enforceable: false
---
# R-SCOPE

A step is classified under a cluster only where the action fell outside the entitlement envelope an accountable grantor actually conferred for it. Cause-side classification asks three questions in strict order: (1) Is there an actor? No: failure or external event — operational risk, no cluster. (2) Did the actor intend the outcome? No: Error in Use — operational risk, no cluster. (3) Did an accountable grantor confer an entitlement covering THIS action? Yes: Abuse of Rights — operational risk, no cluster, no System Risk Event; the consequence chain starts at the Data Risk Event. Only then: if an implementation flaw was required, #2 or #3 per R-ROLE; otherwise #1 Abuse of Functions — cyber, SRE recorded. Entitlement means entitled, not permitted, and attaches to the person, not the token: use of a credential by anyone other than its grantee is never inside an envelope (#4 per R-CRED, subsequent function use #1), and exploiting an implementation flaw is never inside any grant.

> v2.5 scope rule (2026-09-05). Makes explicit in the registry the scope boundary the framework has always asserted: cyber risk addresses unauthorized or unknown entities, and an entitled actor inside their grant is neither. It is NOT an actor test (Axiom IV): the question is a relation between the action and the conferred envelope, never who the actor is — an outsider with no grant and an insider acting outside their grant land in the same Attack row and the same cluster. 'Insider threat' is therefore not a TLCTC category; it is a mixture of two rows answering to two control regimes. Abuse of Rights is not an eleventh cluster because it has no generic vulnerability: #1's exposure (the designed scope of functionality) is reducible by design, whereas a granted entitlement is irreducible by design — remove it and you have removed the business, not secured the system. Rights are functions (every authorization check is designed functionality), which is why the two abuses look alike; rights are the subset of functions that partitions the invocation of all the others, and the taxonomy turns on which side of that partition the action fell, never on which function was called or who called it. Entitlement is tested after intent and before the implementation-flaw test because an entitled actor exploiting a code flaw is an attack. Companion definitions live in the cause_side_partition section; worked cases (support agent, database administrator, self-enrolment, stolen credentials, Adoboli) in the core paper section 3.5. Classification-preserving for Attack-row records; records that classified an entitled actor's in-grant action as #1 SHOULD be re-checked.

# Schema

- **Enforcement level:** must
- **Machine enforceable:** false
