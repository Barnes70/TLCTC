---
type: "term"
title: "Data Risk Event (DRE)"
description: "An outcome event describing Loss of Confidentiality (C) (data stolen / unauthorized access), Loss of Integrity (I) (data modified / unauthorized changes), or Loss of Availability/Accessibility (A) (data gone or unreachable, or data present but unusable)."
resource: "tlctc:term:data-risk-event-dre"
tags:
  - "glossary"
---
# Data Risk Event (DRE)

An outcome event describing **Loss of Confidentiality (C)** (data stolen / unauthorized access), **Loss of Integrity (I)** (data modified / unauthorized changes), or **Loss of Availability/Accessibility (A)** (data gone or unreachable, or data present but unusable). Data Risk Events MUST be recorded separately from cluster steps, MUST NOT be used as threat categories, and MUST NOT change the cluster classification of the step that preceded them. Notation: `[DRE: C]`, `[DRE: I]`, `[DRE: A]`, or combinations. The type codes form a **refinement tree** (core §7.6; dictionary `data_risk_events`), not a flat list: `I` MAY be refined into **`Ii`** (Incorrect State — correspondence or completeness fails; the content is wrong) or **`If`** (Misattributed State — provenance or attribution fails; the record claims an origin it does not have, and its content may be perfectly accurate); `A` MAY be refined into **`Av`** (Unavailable State — data gone or unreachable) or **`Ac`** (Inaccessible State — data present but unusable). A parent code stays legal whenever the refinement is unknown or irrelevant. **Stopping rule:** a property is split only where the resulting states are distinguishable by inspecting the record itself, never by the story of how it got there — which admits exactly these two splits, refuses every split of `C`, and refuses any split by cause (Axiom III). Refinements are read off the record, never off the actor; there is no "manipulated" code. Examples: ransomware encryption = `[DRE: Ac]`; data deletion = `[DRE: Av]`; a value keyed wrongly on purpose = `[DRE: Ii]`; an entry posted under someone else's session = `[DRE: If]`; a transcript showing a command that never ran, written by code standing in for the harness = `[DRE: Ii, If]`; distinction unknown = `[DRE: I]` / `[DRE: A]`.

**Reference:** §4.2.2 (Global Definitions), §6.2 (Rule 2), §11.5.3

**Related reading:** [Chaos Ransomware — TLCTC forensic](https://www.tlctc.net/chaos-ransomware-tlctc-analysis.html), [Evolving VERIS — replace Action axis with TLCTC](https://www.tlctc.net/tlctc-veris.html), [LINDDUN vs TLCTC — complementary approaches](https://www.tlctc.net/tlctc-LINDDUN.html), [Enhancing CVE records with TLCTC v2.1](https://www.tlctc.net/tlctc-cve-nvd.html), [GDPR vs NIS2 — different trigger points](https://www.tlctc.net/tlctc-gdpr-nis2-triggers.html), [TLCTC classification decision tree V2.0/V2.1](https://www.tlctc.net/tlctc-decision-tree.html), [TLCTC+ for NCSCs & CERTs — national reporting](https://www.tlctc.net/tlctc-plus-ncsc-proposal.html)
