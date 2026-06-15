---
type: "term"
title: "Foreign Executable Content (FEC)"
description: "Attacker controlled (or otherwise untrusted) program text or bytes that are interpreted, loaded, or executed by a general purpose execution engine in the target environment."
resource: "tlctc:term:foreign-executable-content-fec"
tags:
  - "glossary"
---
# Foreign Executable Content (FEC)

Attacker-controlled (or otherwise untrusted) program text or bytes that are **interpreted, loaded, or executed** by a **general-purpose execution engine** in the target environment. Includes attacker-controlled commands fed into interpreters. FEC execution includes in-memory (fileless) execution, interpreted code, macro execution, and reflective loading—no "on-disk" requirement exists.

**Reference:** §4.2.2 (Global Definitions)

**Related reading:** [The File Type Fallacy — extension blocklists](https://www.tlctc.net/tlctc-file-type-fallacy.html), [GovCERT-CH blocked filetypes × TLCTC](https://www.tlctc.net/tlctc-govcert-blocked-filetypes.html)
