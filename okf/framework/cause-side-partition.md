---
type: "partition"
title: "Cause-side partition (actor / intent / entitlement)"
description: "The partition of the cause side of any risk event into four rows by three questions asked in strict order."
resource: "tlctc:framework:cause-side-partition"
tags:
  - "taxonomy"
  - "scope"
  - "cause-side"
  - "abuse-of-rights"
---
# Cause-side partition and scope boundary

The partition of the cause side of any risk event into four rows by three questions asked in strict order. Exactly one row — Attack — is in TLCTC scope; the ten clusters classify its steps and only its steps (R-SCOPE). The other three rows are operational risk with no cluster. The partition is a property of the action, not of the actor (Axiom IV): the same person can produce events in different rows on the same day.

## The three questions (asked in order)

1. Is there an actor?
2. Did the actor intend the outcome?
3. Did an accountable grantor confer an entitlement covering this action?

## The four rows

| Row | Actor | Intent | Entitled | Register | Clusters apply | Definition |
|---|---|---|---|---|---|---|
| **Failure / external event** (`failure`) | No | — | — | operational-risk | no | No actor. Software or hardware failure, misconfiguration without intent, capacity exhaustion without an attacker, or an external event. At the system altitude this is the Failure type of the System Risk Event. |
| **Error in Use** (`error_in_use`) | Yes | No | — | operational-risk | no | An actor, any actor, acting without intending the outcome. Entitlement is not asked: a visitor who trips a breaker is Error in Use, not #8. Can enter any altitude directly and can produce any Data Risk Event type (a misdirected email is C, an accidental purge is Av). |
| **Abuse of Rights** (`abuse_of_rights`) | Yes | Yes | Yes | operational-risk | no | An actor acting intentionally inside an entitlement — an access right, a role, a mandate — genuinely conferred by an accountable grantor, but against its purpose. The envelope is honoured and the system behaved as designed and as authorised, so there is no generic vulnerability, no cluster and no System Risk Event; the consequence chain begins at the Data Risk Event. Examples: a badge holder propping open a door, an administrator using genuine root to exfiltrate, a clerk posting a false entry inside their role, an officer approving a payment inside their mandate. Answered by segregation of duties, four-eyes, mandate limits, supervision, vetting and purpose auditing — owned by the CRO, the business line and HR, not the CISO. |
| **Attack** (`attack`) | Yes | Yes | No | cyber | yes — #1–#10 | An actor acting intentionally with no entitlement covering the action — an outsider with no grant, or an insider reaching past the envelope they were granted. The ten TLCTC clusters classify every step (exactly one per step, Axiom VI) and a System Compromise is recorded. A stolen entitlement is never Abuse of Rights: the grant attaches to the person, not the token, so credential use by a non-grantee is #4 (R-CRED) and the functions reached with it are #1. |

## Entitlement

- **definition:** What an accountable grantor actually conferred on a person for an action: an access right, a role, or a mandate, held genuinely and bounded by its purpose and scope.
- **entitled not permitted:** Permission is what the access-control system happens to return; entitlement is what a grantor conferred. The two are supposed to coincide and frequently do not; that gap is where the classification of a technical act depends on a governance document, and the framework refuses to pretend a question about authorization can be answered without consulting the authority.
- **attaches to person not token:** An entitlement is conferred on a grantee, never on a credential. An attacker holding the artifact was never a grantee, so no action they take is inside any envelope, however closely it mirrors what the grantee could have done.
- **asymmetry with cluster 1:** #1 Abuse of Functions reaches past the entitlement using functions the designer left open; its generic vulnerability is reducible by design (narrow the API, tighten the scope). Abuse of Rights uses the entitlement as given, for a purpose the grantor did not intend; a granted entitlement is irreducible by design. Two exposures, two levers, two owners, two registers.

## Third-party modifier

Third party is a modifier, not a fifth row: any of the four rows may occur in another responsibility sphere and be honoured across a trust boundary. The notation already carries the modifier as the domain-boundary operator ||[ctx][@A->@B]||. #10 Supply Chain Attack is only the Attack-row instance of it at the system altitude; a supplier's outage honoured across the boundary is third-party failure, not #10.

## Decision procedure

- 1. Is there an actor? No -> Failure / external event. Operational risk. No cluster.
- 2. Did the actor intend the outcome? No -> Error in Use. Operational risk. No cluster.
- 3. Did an accountable grantor confer an entitlement covering THIS action? Yes -> Abuse of Rights. Operational risk. No SRE; the chain starts at the DRE. No -> continue.
- 4. Was an implementation flaw required? Yes -> #2 / #3 per R-ROLE. No -> #1 Abuse of Functions. Cyber; SRE recorded. (Steps beyond the first are classified by the cluster rules; R-CRED, R-EXEC, R-SUPPLY and the others apply unchanged.)

# Schema

- **Governing rule:** [R-SCOPE](/rules/r-scope.md)
- **In-scope row:** `attack` only; the other three rows carry no cluster.
