# Propagated Controls — Managing Controls Over Event Chains

**Status:** Companion note to TLCTC v2.0 (formalizes a v2.0 glossary concept and generalizes it beyond compliance).
**Audience:** CISOs, IR designers, BCM/operational-risk owners, GRC architects.

---

## TL;DR

A single incident produces a **chain of events** — `SRE → DRE → BRE₁ → … → BREₙ`. Each event has its own NIST CSF container (`ID, PR, DE, RS, RC, GV`) **and its own recovery objective**: System Recovery for the SRE, Data Recovery for the DRE, Disaster Recovery / business continuity for the BRE. These objectives are usually owned by *different organisations* with *different clocks*.

The obligation to satisfy a downstream Protection Requirement (PR) therefore usually fires **earlier** in the chain — the GDPR notification clock for a future BRE starts at the DRE; the handover to the enterprise BCM/crisis-management organisation that owns disaster recovery starts at the DRE too. TLCTC models this with a single, generic mechanism: **propagation of PR controls backward into the RS (Respond) container of an upstream event.**

```
RS(Eₙ) = { Response } ∪ { Propagated PR(Eₙ₊₁) } ∪ … ∪ { Propagated PR(Eₙ₊ₓ) }
```

The simplest reading: a propagated control is the upstream RS step that *hands an obligation off to whoever owns the downstream recovery objective* — a regulator, a contract counterparty, or the BCM organisation. This document lifts the mechanism out of the glossary, names the **sources** of propagation (regulatory, contractual, BCM, internal policy), and works through two examples — one compliance, one BCM — that share the same structure.

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

Two propagated controls can sit in the same RS container with completely different clocks and authorities (see §5.1).

---

## 2. Sources of propagated controls

Compliance is the **most visible** source of propagation, but not the only one. Four sources cover the practical cases:

| Source            | Examples                                                                 | Typical host event | Typical timing |
|-------------------|--------------------------------------------------------------------------|--------------------|---------------|
| **Regulatory**    | GDPR Art. 33, NIS2 Art. 23, DORA, SEC 8-K cyber, HIPAA breach notice     | DRE or SRE         | Hours to days |
| **Contractual**   | Customer SLA notification, partner-disclosure clauses, cyber-insurance trigger conditions | DRE or SRE | Minutes to hours |
| **BCM / BIA**     | **Handover to enterprise BCM / crisis-management organisation**; continuity-plan invocation; failover/alternate-site activation; crisis-comms playbook | DRE (mandatory, SLA-clocked); SRE (preemptive) | Minutes |
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

Compliance is the *visible* propagation case. The same mechanism — without any regulator involved — is the BCM/BIA control set. The cleanest way to see it is to read each event by its **recovery objective**:

| Event | Recovery objective | Typical owner | Governing clock |
|-------|--------------------|---------------|-----------------|
| **SRE** — System Risk Event | **System Recovery** — restore the system to a trustworthy state | IT Ops / IR | Containment-driven |
| **DRE** — Data Risk Event | **Data Recovery** — restore CIA properties of data | IR + data owners | **SLA ticker** (RPO, customer-comms SLA, regulatory disclosure windows) |
| **BRE** — Business Risk Event | **Disaster Recovery / business continuity** | Enterprise BCM, crisis management, executive | **Service Recovery Time ticker** (RTO for disaster recovery; BIA-defined target) |

These objectives belong to **different organisations**. The IR team owns system and data recovery; the enterprise BCM / crisis-management organisation owns disaster recovery. Propagation is what keeps that handover from being lost between them.

**Two tickers, two questions, two event knots.** The chain carries two distinct clocks, anchored to different events:

- The **SLA ticker** anchors at the **DRE** and times *obligations*: when must you notify? when must you hand over? when must customer-comms go out? RPO, customer-comms SLA, and regulatory windows all live here.
- The **Service Recovery Time ticker** anchors at the **BRE** and times *delivery*: when must business operations be restored? RTO for the disruption BRE lives here, with the BIA defining the target.

It is easy to conflate them because both involve deadlines and both are visible in IR runbooks. They answer different questions. The DRE *fires the handover* (SLA clock); the BRE *owns the RTO countdown* (delivery clock).

A ransomware-driven outage of a payment-processing platform:

```
SRE (System Compromise) — RC objective: System Recovery
  └─ DRE [Ac] (data present but encrypted, application data inaccessible)
                — RC objective: Data Recovery
        └─ BRE_disruption  (payment platform unavailable > RTO)
              — RC objective: Disaster Recovery / continuity
              └─ BRE_revenue_loss / BRE_contract_breach
```

`BRE_disruption` has its own PR set — the **business continuity controls**: failover capability, alternate-site readiness, RTO/RPO targets, manual-process playbooks, customer-communication SLAs. But none of those *execute* at BRE time, and crucially, none are owned by the IR team. They execute earlier, propagated backward, with the **handover to the BCM organisation** as the dominant control:

```
RS(SRE) = { containment, eradication, forensics }
        ∪ { Propagated PR(BRE_disruption): preemptive BCM alert when SRE
                                            classification severity alone justifies it }

RS(DRE) = { restore from clean backup, validate data integrity,
            verify application state }
        ∪ { Propagated PR(BRE_disruption): MANDATORY — formal handover to enterprise
                                            BCM / crisis-management organisation;
                                            activate manual processing;
                                            execute customer-comms SLA }
```

**The DRE response plan must include the formal handover** — because disaster recovery is not an IR responsibility. The DRE is where the **SLA ticker** that times the handover starts running (RPO commitments, contractual customer-comms SLAs, regulatory disclosure windows). The **Service Recovery Time ticker** (RTO countdown for the disruption BRE) is a separate clock owned by the BCM organisation downstream — the DRE handover is what *starts that clock running under the correct owner*. RS(SRE) may include a preemptive alert when severity is obvious; RS(DRE) **must** include the handover because by then a business-relevant consequence is on the table.

This is why mature IR runbooks have **BCM hand-off steps** baked in: those steps are propagated PR controls in TLCTC terms. The BCM team's RTO/RPO is the timeline; the IR team's SRE/DRE classification is the trigger; the handover itself is the control.

---

## 5. Recovery objectives and the escalation handover

Once propagation is read through the recovery-objective lens, the existing examples and most real propagated controls collapse into **two families**.

### 5.1 The two families of propagated controls

**Family 1 — Compliance reporting.** A notification obligation hosted upstream of the BRE it would otherwise enforce: GDPR Art. 33, NIS2 Art. 23, SEC 8-K cyber, DORA major-incident reporting, HIPAA breach notice, contractual SLA-breach notifications, cyber-insurance trigger notifications. The downstream "event" is a *regulatory* or *contractual* BRE. The propagated control is a **disclosure** to an external authority.

**Family 2 — Organisational handover.** A recovery objective owned by a downstream organisation, triggered by an upstream technical event: BCP/disaster-recovery invocation, crisis-comms activation, legal-hold trigger, board notification, ethics-committee referral. The downstream "event" is a *business* BRE owned by a *non-IR* organisation (BCM, executive, legal). The propagated control is an **escalation** that transfers ownership of the next recovery objective.

Both families are mechanically identical — `Propagated PR(downstream)` hosted in `RS(upstream)`. They differ in *who owns* the downstream recovery objective:

| Family | Downstream owner | Control verb | Clock |
|--------|------------------|--------------|-------|
| Compliance reporting | External authority or counterparty | Notify / report | Regulatory or contractual |
| Organisational handover | Internal BCM / executive / legal | Escalate / hand over | SLA / RTO / RPO |

A single IR playbook routinely contains both — a GDPR notification and a BCM handover sit in the same RS container, with different clocks and different recipients.

### 5.2 Why the DRE is the natural BCM trigger point

The SRE is technical — *something is wrong with the system*. The BRE is business — *the customer cannot transact*. The DRE sits between them: it is the first event in the chain where a **business-relevant consequence** is observable. CIA properties of data are not internal IT properties; they are what the business depends on.

That makes RS(DRE) the canonical home for the IR → BCM handover:

1. **The SLA ticker starts here.** Customer-comms SLAs, RPO commitments, regulatory disclosure windows — they all anchor to data-impact awareness, not to system compromise. The DRE is the formal start of those clocks. The separate **Service Recovery Time ticker** (RTO for the disruption BRE) is measured downstream, owned by the BCM organisation — but the DRE handover is what transfers ownership so that BRE-level clock can begin running against the right team. The DRE is the *trigger*; the BRE is where the *delivery clock* runs.
2. **The classification is sufficient.** A DRE classification (with CIA tags) carries enough information to trigger BCM and disclosure obligations. The SRE alone usually does not.
3. **Uncertainty is acceptable but bounded.** Acting at the SRE risks invoking obligations that may not apply; acting at the BRE is too late. The DRE is the earliest event where the *risk of false trigger* is dominated by the *risk of missed deadline*.

Preemptive SRE-level escalation is still valuable when classification severity alone justifies it (catastrophic outage, ransomware on a tier-0 system) — but it is the exception, not the pattern. **The rule is: every DRE response plan must include the handover, and the SLA clock attached to that handover is what makes the obligation mandatory rather than discretionary.**

---

## 6. Placement rule

Where does a propagated control belong?

> **Rule of Propagation:** A PR control for event `Eₙ₊ₓ` is hosted in `RS(Eᵢ)` where `Eᵢ` is the **earliest** event in the chain whose **classification suffices to trigger** the obligation.

Two practical consequences:

1. **GDPR-Art-33-style** obligations propagate to the **DRE**, because they require PII (i.e., a DRE-C classification) to fire — the SRE alone is not enough.
2. **NIS2-Art-23-style** or **BCM-RTO-style** obligations propagate all the way back to the **SRE**, because an incident classification *of sufficient severity* is the trigger — no downstream event is needed.

Earlier placement = longer reaction time but also more uncertainty (you may invoke obligations that turn out not to apply). The classification quality at each event determines how aggressively propagation can reach upstream.

---

## 7. Relationship to existing v2.0 concepts

Already in the glossary:

- **Propagated PR** *(V2.0)* — line 1073 of `tlctc-glossary.md`. Defined for regulatory use. This document **generalizes the source** to four categories without changing the definition.
- **RS Container (Respond Container)** *(V2.0)* — line 1205. The formula `RS(Eₙ) = { Response } ∪ { Propagated PR(Eₙ₊₁) } ∪ { Propagated PR(Eₙ₊ₓ) }` is the canonical statement.
- **Eₙ Event Notation (Regulatory)** *(V2.0)* — line 528. The subscript notation (`E3a`, `E3b`) generalizes naturally to non-regulatory branches.
- **Event Chain** — line 560. The `SRE → DRE → BRE₁ → BREₙ` chain is the substrate of all propagation.

This document does **not** introduce new notation, axioms, or classification rules. The "recovery objective per event" mapping (System / Data / Disaster Recovery) is a *reading lens* on top of existing v2.0 mechanics, not a new glossary term. It is a clarification of where existing v2.0 mechanics apply.

---

## 8. Open questions

- **JSON representation.** Layer 3 attack paths currently model PR/DE/RS/RC controls indirectly. A future schema extension could carry an explicit `propagated_controls[]` array on each event node, with fields `{ source_event, source_type (regulatory|contractual|bcm|policy), family (reporting|handover), authority, clock_start, deadline }`. Not in scope here.
- **Layer 2 registry — regulatory side.** A reference list of common propagated controls per source type (a "propagation registry") would let organizations stamp their IR playbooks without reinventing the mapping each time.
- **Layer 2 registry — handover side.** Per-organisation BCM invocation procedures (who is the crisis-management duty officer, what is the activation channel, what defines "formal handover complete") are the natural pair to the regulatory registry. Both fit the same Layer 2 reference-registry slot.
- **TLCTC+ alignment.** The TLCTC+ NCSC/CERT proposal (`documentation/tlctc-plus-ncsc-proposal.md`) defines a `+ [BRE: ...]` annotation. A propagated control is operationally adjacent — they may or may not warrant explicit linkage. Deferred.

---

## References

- `documentation/tlctc-glossary.md` — entries: *Propagated PR*, *RS Container*, *Event Chain*, *Eₙ Event Notation*, *Business Risk Event (BRE)*, *Business Impact (BI)*.
- `documentation/tlctc-v2.0-whitepaper.md` — §1.4.3.1 (Consequence Chain).
- `integrations/cortex-xsoar-8/Playbooks/playbook-sub-rs-container.yml` — reference implementation of the RS container concept (regulatory propagation).
- Companion blog: *GDPR vs NIS2: Different Trigger Points for Compliance Events* (2026-01-24) — `/tlctc-gdpr-nis2-triggers.html`.
