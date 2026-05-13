# Propagated Controls — Managing Controls Over Event Chains

**Status:** Companion note to TLCTC v2.0 (formalizes a v2.0 glossary concept and generalizes it beyond compliance).
**Audience:** CISOs, IR designers, BCM/operational-risk owners, GRC architects.

---

## TL;DR

A single incident produces a **chain of events** — `SRE → DRE → BRE₁ → … → BREₙ`. Each event has its own NIST CSF container (`ID, PR, DE, RS, RC, GV`). But the obligation to satisfy a downstream Protection Requirement (PR) usually fires **earlier** in the chain — the GDPR notification clock for a future BRE starts at the DRE; a continuity-plan invocation for a future business-disruption BRE starts at the SRE. TLCTC models this with a single, generic mechanism: **propagation of PR controls backward into the RS (Respond) container of an upstream event.**

```
RS(Eₙ) = { Response } ∪ { Propagated PR(Eₙ₊₁) } ∪ … ∪ { Propagated PR(Eₙ₊ₓ) }
```

This document lifts that mechanism out of the glossary, names the **sources** of propagation (regulatory, contractual, BCM, internal policy), and works through two examples — one compliance, one BCM — that share the same structure.

---

## 1. The mechanism

The Bow-Tie consequence chain (see glossary: *Event Chain*, *Business Risk Event*) is causally directional: an SRE may cause a DRE, which may cause one or more BREs. Controls in the NIST CSF sense are normally placed **at the event they protect** — `PR(BRE_GDPR-violation)` would be "do the things that prevent a GDPR violation".

But many of those PR controls only make sense as **actions taken earlier in the chain**:

- *Notify the supervisory authority within 72h* prevents the GDPR-violation BRE, but the **action** is part of responding to the DRE.
- *Invoke the continuity plan* prevents the prolonged-outage BRE, but the **action** is part of responding to the SRE.
- *Activate the customer-communication SLA* prevents the contractual-breach BRE, but the **action** is part of responding to the DRE.

So the PR for the downstream event is hosted in the **RS container of the upstream event**. This is *propagation backward up the chain*. It is purely a placement rule — the control is still semantically a PR for `Eₙ₊ₓ`; it just executes during `RS(Eₙ)`.

### 1.1 Why this matters

Without naming the mechanism, IR playbooks degenerate into "reporting checklists" — flat lists of obligations bolted onto the response procedure with no causal grounding. With it, every propagated control has:

1. **A source event** (which downstream BRE this PR belongs to).
2. **A host event** (which upstream RS container is the right place to execute it).
3. **A timeline** anchored to the *host* event clock, not the source.
4. **A trigger condition** based on the host event's classification.

Two propagated controls can sit in the same RS container with completely different clocks and authorities (see §3.1).

---

## 2. Sources of propagated controls

Compliance is the **most visible** source of propagation, but not the only one. Four sources cover the practical cases:

| Source            | Examples                                                                 | Typical host event | Typical timing |
|-------------------|--------------------------------------------------------------------------|--------------------|---------------|
| **Regulatory**    | GDPR Art. 33, NIS2 Art. 23, DORA, SEC 8-K cyber, HIPAA breach notice     | DRE or SRE         | Hours to days |
| **Contractual**   | Customer SLA notification, partner-disclosure clauses, cyber-insurance trigger conditions | DRE or SRE | Minutes to hours |
| **BCM / BIA**     | Continuity-plan invocation, failover decision, alternate-site activation, crisis-comms playbook | SRE or DRE | Minutes |
| **Internal policy** | Board notification thresholds, internal legal-hold triggers, ethics-committee referral | SRE, DRE, or BRE | Hours |

All four behave identically: they are **PR controls of a downstream BRE** that execute as **RS steps of an upstream event**. The framework is source-agnostic; the source only changes who owns the obligation and what defines "trigger".

---

## 3. Worked example A — Compliance (GDPR vs NIS2)

> **Companion blog:** [GDPR vs NIS2: Different Trigger Points for Compliance Events](/tlctc-gdpr-nis2-triggers.html) — full visual treatment of the example below.

A ransomware incident affects a NIS2-scoped operator whose data includes PII.

```
SRE (System Compromise)
  └─ DRE [C] (PII confidentiality loss)
        ├─ BRE_GDPR  (notification obligation, Art. 33, 72h)
        └─ BRE_NIS2  (incident report, Art. 23, 24h early warning + 72h report)
```

Trigger placement:

| Regulation | Triggers at | Propagated PR hosted in | Timeline |
|------------|-------------|--------------------------|---------|
| GDPR Art. 33 | DRE (PII confirmed) | `RS(DRE)` | 72h after awareness |
| NIS2 Art. 23 | SRE (significant incident classified) | `RS(SRE)` | 24h early warning + 72h notification |

In notation:

```
RS(SRE) = { containment, eradication, forensics }
        ∪ { Propagated PR(BRE_NIS2):  notify CSIRT within 24h }

RS(DRE) = { breach assessment, evidence preservation }
        ∪ { Propagated PR(BRE_GDPR): notify DPA within 72h }
```

The two propagated controls sit in **different** RS containers and have **different** clocks. Confusing them — putting GDPR in `RS(SRE)` or NIS2 in `RS(DRE)` — is the standard failure mode of generic "incident reporting checklists".

---

## 4. Worked example B — BCM (business disruption)

Compliance is the *visible* propagation case. The same mechanism — without any regulator involved — is the BCM/BIA control set.

A ransomware-driven outage of a payment-processing platform:

```
SRE (System Compromise)
  └─ DRE [Ac] (data present but encrypted, application data inaccessible)
        └─ BRE_disruption  (payment platform unavailable > RTO)
              └─ BRE_revenue_loss / BRE_contract_breach
```

`BRE_disruption` has its own PR set — the **business continuity controls**: failover capability, alternate-site readiness, RTO/RPO targets, manual-process playbooks, customer-communication SLAs. But none of those *execute* at BRE time. They execute earlier, propagated backward:

```
RS(SRE) = { containment, eradication, forensics }
        ∪ { Propagated PR(BRE_disruption): invoke BCP, declare alternate site,
                                            engage crisis-comms within RTO clock }

RS(DRE) = { restore from clean backup, validate data integrity,
            verify application state }
        ∪ { Propagated PR(BRE_disruption): activate manual processing,
                                            execute customer-comms SLA }
```

The IR playbook for the SRE *is* the BCM invocation point. The continuity controls that protect the disruption-BRE live inside `RS(SRE)` and `RS(DRE)` — exactly the same pattern as GDPR/NIS2, but driven by a BIA rather than a regulation.

This is why mature IR runbooks have **BCM hand-off steps** baked in: those steps are propagated PR controls in TLCTC terms. The BCM team's RTO/RPO is the timeline; the IR team's SRE/DRE classification is the trigger.

---

## 5. Placement rule

Where does a propagated control belong?

> **Rule of Propagation:** A PR control for event `Eₙ₊ₓ` is hosted in `RS(Eᵢ)` where `Eᵢ` is the **earliest** event in the chain whose **classification suffices to trigger** the obligation.

Two practical consequences:

1. **GDPR-Art-33-style** obligations propagate to the **DRE**, because they require PII (i.e., a DRE-C classification) to fire — the SRE alone is not enough.
2. **NIS2-Art-23-style** or **BCM-RTO-style** obligations propagate all the way back to the **SRE**, because an incident classification *of sufficient severity* is the trigger — no downstream event is needed.

Earlier placement = longer reaction time but also more uncertainty (you may invoke obligations that turn out not to apply). The classification quality at each event determines how aggressively propagation can reach upstream.

---

## 6. Relationship to existing v2.0 concepts

Already in the glossary:

- **Propagated PR** *(V2.0)* — line 1073 of `tlctc-glossary.md`. Defined for regulatory use. This document **generalizes the source** to four categories without changing the definition.
- **RS Container (Respond Container)** *(V2.0)* — line 1205. The formula `RS(Eₙ) = { Response } ∪ { Propagated PR(Eₙ₊₁) } ∪ { Propagated PR(Eₙ₊ₓ) }` is the canonical statement.
- **Eₙ Event Notation (Regulatory)** *(V2.0)* — line 528. The subscript notation (`E3a`, `E3b`) generalizes naturally to non-regulatory branches.
- **Event Chain** — line 560. The `SRE → DRE → BRE₁ → BREₙ` chain is the substrate of all propagation.

This document does **not** introduce new notation, axioms, or classification rules. It is a clarification of where existing v2.0 mechanics apply.

---

## 7. Open questions

- **JSON representation.** Layer 3 attack paths currently model PR/DE/RS/RC controls indirectly. A future schema extension could carry an explicit `propagated_controls[]` array on each event node, with fields `{ source_event, source_type (regulatory|contractual|bcm|policy), authority, clock_start, deadline }`. Not in scope here.
- **Layer 2 registry.** A reference list of common propagated controls per source type (a "propagation registry") would let organizations stamp their IR playbooks without reinventing the mapping each time.
- **TLCTC+ alignment.** The TLCTC+ NCSC/CERT proposal (`documentation/tlctc-plus-ncsc-proposal.md`) defines a `+ [BRE: ...]` annotation. A propagated control is operationally adjacent — they may or may not warrant explicit linkage. Deferred.

---

## References

- `documentation/tlctc-glossary.md` — entries: *Propagated PR*, *RS Container*, *Event Chain*, *Eₙ Event Notation*, *Business Risk Event (BRE)*, *Business Impact (BI)*.
- `documentation/tlctc-v2.0-whitepaper.md` — §1.4.3.1 (Consequence Chain).
- `integrations/cortex-xsoar-8/Playbooks/playbook-sub-rs-container.yml` — reference implementation of the RS container concept (regulatory propagation).
- Companion blog: *GDPR vs NIS2: Different Trigger Points for Compliance Events* (2026-01-24) — `/tlctc-gdpr-nis2-triggers.html`.
