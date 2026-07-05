---
description: Analyze a security document (forensic report, CVE, threat-intel bulletin, red-team write-up) using the TLCTC v2.3 taxonomy. Produces an attack-path classification with R-* rule citations, Δt velocity annotations, boundary operators, DRE outcomes, and control-gap recommendations.
argument-hint: [path-to-document | URL | pasted text]
---

Analyze the following security document using the **TLCTC v2.3** framework loaded by the `tlctc-classify` skill.

**Input:** $ARGUMENTS

Steps:

1. If the input is a file path or URL, read it. Otherwise treat the argument as the document body.
2. Determine the document type (Forensic / CVE / Threat Intel / Red-Team Narrative) and select the matching output structure (Type A / B / C from the skill).
3. Produce the analysis using the exact notation, R-* rule citations, and verification checklist defined in the `tlctc-classify` skill.
4. Run the Final Verification Checklist before returning the result. Flag any item that fails.
5. If evidence is insufficient for any step, use `#X [conf=low]`, `[inferred]`, or `?`/`…` per R-UNRES-9 — never fabricate.
