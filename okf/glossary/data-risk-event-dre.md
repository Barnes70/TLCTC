---
type: "term"
title: "Data Risk Event (DRE)"
description: "An outcome event describing Loss of Confidentiality (C) (data stolen / unauthorized access), Loss of Integrity (I) (data modified / unauthorized changes), or Loss of Availability/Accessibility (A) (data gone or unreachable, or data present but unusable)."
resource: "tlctc:term:data-risk-event-dre"
tags:
  - "glossary"
---
# Data Risk Event (DRE)

An outcome event describing **Loss of Confidentiality (C)** (data stolen / unauthorized access), **Loss of Integrity (I)** (data modified / unauthorized changes), or **Loss of Availability/Accessibility (A)** (data gone or unreachable, or data present but unusable). Data Risk Events MUST be recorded separately from cluster steps, MUST NOT be used as threat categories, and MUST NOT change the cluster classification of the step that preceded them. Notation: `[DRE: C]`, `[DRE: I]`, `[DRE: A]`, or combinations. When the distinction between Availability and Accessibility is operationally relevant, the general code `A` MAY be refined into **`Av`** (Availability — data gone or unreachable) or **`Ac`** (Accessibility — data present but unusable). Example: ransomware encryption = `[DRE: Ac]`; data deletion = `[DRE: Av]`; distinction unknown = `[DRE: A]`.

**Reference:** §4.2.2 (Global Definitions), §6.2 (Rule 2), §11.5.3

**Related reading:** [Chaos Ransomware — TLCTC forensic](https://www.tlctc.net/chaos-ransomware-tlctc-analysis.html), [Evolving VERIS — replace Action axis with TLCTC](https://www.tlctc.net/tlctc-veris.html), [LINDDUN vs TLCTC — complementary approaches](https://www.tlctc.net/tlctc-LINDDUN.html), [Enhancing CVE records with TLCTC v2.1](https://www.tlctc.net/tlctc-cve-nvd.html), [GDPR vs NIS2 — different trigger points](https://www.tlctc.net/tlctc-gdpr-nis2-triggers.html), [TLCTC classification decision tree V2.0/V2.1](https://www.tlctc.net/tlctc-decision-tree.html), [TLCTC+ for NCSCs & CERTs — national reporting](https://www.tlctc.net/tlctc-plus-ncsc-proposal.html)
