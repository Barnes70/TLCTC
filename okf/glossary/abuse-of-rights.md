---
type: "term"
title: "Abuse of Rights"
description: "An intended action inside an entitlement — an access right, a role, a mandate — genuinely conferred by an accountable grantor, but used against its purpose."
resource: "tlctc:term:abuse-of-rights"
tags:
  - "glossary"
---
# Abuse of Rights

An intended action inside an **entitlement** — an access right, a role, a mandate — genuinely conferred by an accountable grantor, but used against its purpose. The envelope is honoured: the system behaved as designed and as authorised, so there is **no generic vulnerability, no cluster, and no System Risk Event**; the consequence chain begins at the Data Risk Event. Register: operational risk, owned by the CRO, the business line and HR, not the CISO. Examples: a badge holder propping open a door, an administrator using genuine root to exfiltrate, a clerk posting a false entry inside their role, an officer approving a payment inside their mandate, a support agent opening a celebrity's record out of curiosity. Controls: segregation of duties, four-eyes, mandate limits, supervision, vetting, purpose auditing.

**Why it is not cluster #11.** Rights are functions — every authorization check is designed functionality — which is why Abuse of Rights and `#1 Abuse of Functions` look alike. But rights are the subset of functions that partitions the invocation of all the others, and the taxonomy turns on which side of that partition the action fell. `#1` reaches *past* the entitlement using functions the designer left open, and its generic vulnerability is reducible by design (narrow the API, tighten the scope). A granted entitlement is irreducible by design — remove it and you have removed the business. Two exposures, two levers, two owners, two registers.

**Boundaries.** An insider reaching *outside* their grant is the Attack row and a cluster (the same support agent editing a region parameter to reach a record outside their territory is `#1`). A **stolen entitlement is never Abuse of Rights**: the grant attaches to the person, not the token, so credential use by a non-grantee is `#4` (R-CRED) and the functions reached with it are `#1` — an attack wearing an entitlement. Self-enrolment into a population a registration function was not meant for is `#1`, not Abuse of Rights: nobody with authority conferred anything. The row is a property of the action, not the actor (Axiom IV). The name is **Abuse of Rights**; "Abuse of Access Rights" is deprecated because an access right is only one kind of entitlement.

**Reference:** Core paper §3.5 (cause-side partition), §6.1 (R-SCOPE); dictionary `cause_side_partition`

**Related reading:** [Functions and Rights — why one is a threat cluster and the other is not](https://www.tlctc.net/tlctc-functions-vs-rights.html), [The Adoboli Paradox — Cyber vs Operational Risk](https://www.tlctc.net/tlctc-adoboli-paradox.html)

See also: Cause-Side Partition, Entitlement, Error in Use, R-SCOPE, Abuse of Functions (#1), Operational Risk (OpRisk)
