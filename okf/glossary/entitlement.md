---
type: "term"
title: "Entitlement"
description: "What an accountable grantor actually conferred on a person for an action: an access right, a role, or a mandate, held genuinely and bounded by its purpose and scope."
resource: "tlctc:term:entitlement"
tags:
  - "glossary"
---
# Entitlement

What an accountable grantor actually conferred on a person for an action: an access right, a role, or a mandate, held genuinely and bounded by its purpose and scope. **Entitled is not permitted.** Permission is what the access-control system happens to return; entitlement is what a grantor conferred. The two are supposed to coincide and frequently do not, and that gap is where the classification of a technical act can depend on a governance document — the framework refuses to pretend a question about authorization can be answered without consulting the authority. **An entitlement attaches to the person, never to the token:** an attacker holding a credential was never a grantee, so no action they take is inside any envelope (`#4` per R-CRED, then `#1`). The entitlement test is the authorization-side counterpart of R-CRED's authentication-side test (is the system deceived about who is authenticating?): both ask about the truth of a relation, never about the identity of the claimant.

**Reference:** Core paper §3.5; dictionary `cause_side_partition.entitlement`

See also: Abuse of Rights, Cause-Side Partition, R-SCOPE, R-CRED
