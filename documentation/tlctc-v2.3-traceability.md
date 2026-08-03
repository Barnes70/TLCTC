# TLCTC v2.3 Core — Consolidation Traceability

**v2.3.0** introduced NO new normative content. Every element traces to finalized v2.1 source. **v2.3.1** and **v2.3.2** each add one deliberate, axiom-justified normative correction — see the Erratum sections below. **v2.4** adds one clarifying, backward-compatible change to the interaction model — see the Clarification section below.

| v2.3 element | Source |
|---|---|
| 10 clusters | `tlctc-framework.v2.3.json` (verbatim) / whitepaper §4.1 |
| 10 axioms | `tlctc-framework.v2.3.json` (verbatim) / whitepaper §2 |
| R-EXEC, R-ROLE, R-FLOOD, R-SUPPLY, R-MITM, R-CRED | `tlctc-framework.v2.3.json` (verbatim) |
| R-TRANSIT-3, R-INTRA-7, R-INTRA-9 | `CLAUDE.md` v2.1 boundary extensions / whitepaper §11 |
| R-UNRES-2/3/5/6/7/8/9 | `CLAUDE.md` v2.1 unresolved-step rules / whitepaper §11 |
| Thought experiment | whitepaper §3 |
| Design principles & topology | whitepaper §2 (framing) + §5 (internal/bridge) |
| Cause–Event–Consequence model (SRE→DRE→BRE) | whitepaper §6.1 / §6.3 / §6.3.1 |
| Per-cluster Boundary Tests | whitepaper §4.1 (verbatim) |
| Strategic/Operational two-layer naming (TLCTC-XX.YY) | whitepaper §4.2.1 |
| Attack-path notation (incl. velocity Δt, DCS) | whitepaper §11 / §12 / §10.6 (condensed) |
| Concise glossary | `tlctc-glossary.md` (subset) |
| References | adjacent frameworks named in spec / Scholar plan WP3 |

Version axes: `tlctc_version` 2.0/2.1 → 2.3; `schema_version` unchanged (2.0.0); tooling semver unchanged.

Deferred (NOT in this spec): application doc, integration doc, old version-string/tag cleanup, Scholar/DOI pipeline.

Core artifacts: `json-schemas/layer-1/tlctc-framework.v2.3.json`, `documentation/tlctc-v2.3-core.md`.

## Erratum — v2.3.1 (2026-07-01)

A single normative correction to the **#4 Identity Theft** cluster. Cluster identity, IDs (`#4` / `TLCTC-04.00`), definition, attacker's view, topology, and all boundary tests are **unchanged**. Two fields were retightened, and one non-normative clarifier was added.

| Field | Before | After |
|---|---|---|
| Generic vulnerability | "Weak identity management processes and/or inadequate credential protection mechanisms throughout the identity lifecycle." | "Insufficient binding, at the point of authentication, between a presented credential and the authentic holder of the identity it claims." |
| Developer's view | "…secure credential lifecycle management: storage, transmission, session handling…" | "…verify at authentication time that the presenter is the credential's authentic holder: enforce MFA, bind and validate sessions, detect credential replay/reuse and anomalous authentication, and apply least privilege…" |
| Scope paragraph | — (added) | "Credential storage and transmission are prevention controls that reduce acquisition; failures there classify to the enabling cluster (#2/#5/#7/#8), not to #4." |

**Justification (axiom-level, per the immutability rule).** The prior generic-vulnerability field claimed scope over the *whole* credential lifecycle — including storage and transmission — while the cluster's own boundary tests and **R-CRED** already assign credential acquisition/exposure/protection failures to the enabling cluster (#2/#5/#7/#8). It therefore contradicted **Axiom VI** (one generic vulnerability → one cluster), **Axiom VII** (classification anchored in the initial cause, not downstream effects), and **Axiom X** (acquisition vs. application are distinct steps). The retightened wording names the flaw #4 actually exploits — the authentication-time identity-artifact binding gap — bringing the field into conformance with the axioms and matching the structural pattern of the other nine clusters (whose generic-vulnerability line is scope-defining and 1:1 with their boundary tests). This also removes a downstream control-ownership error: storage/transmission controls belong to the enabling clusters, not #4.

**Harmonization.** The v2.3.1 wording is applied consistently across `tlctc-framework.v2.3.json`, `tlctc-v2.3-core.md`, `tlctc-glossary.md` (prose + quick-reference), `glossary/tlctc-glossary.json`, `tlctc-v2.0-whitepaper.md`, `README.md`, the `tlctc-classify` skill, and the HTML tools. The generated `okf/` bundle is rebuilt from these sources. The frozen `tlctc-framework.v2.3.json` dictionary is left as the historical v2.0 record.

## Erratum — v2.3.2 (2026-07-26)

A single normative correction to the **#5 Man in the Middle** cluster. Cluster identity, IDs (`#5` / `TLCTC-05.00`), definition, attacker's view, topology, and all boundary tests are **unchanged**. One field was retightened.

| Field | Before | After |
|---|---|---|
| Generic vulnerability | "The lack of sufficient control, integrity protection, or confidentiality over the communication channel/path." | "The lack of sufficient control over the communication path." |

**Justification (axiom-level, per the immutability rule).** The prior generic-vulnerability field named *confidentiality* and *integrity* — the very CIA properties that the framework classifies on the **consequence** side as Data Risk Events. Importing that vocabulary into a cause-side field contradicted **Axiom III** (threats are causes, not outcomes): loss of confidentiality or integrity is what *follows* a successful #5 step, not the weakness the step exploits. The phrase "integrity protection" additionally named a **control** (end-to-end protection, certificate/path validation) rather than a vulnerability, contradicting **Axiom V** (control failure is not a threat) — absent encryption is a missing control that raises likelihood, not the generic vulnerability itself. The retightened wording names the single condition #5 actually requires and exploits: insufficient control over the communication path. This also restores the 1:1 relationship between the field and **R-MITM**, which already frames the cluster in terms of *position on the path* ("gaining the position maps to another cluster; #5 begins once the position is controlled") with no reference to CIA properties.

**Consequence-side note (non-normative).** Confidentiality and integrity outcomes of a #5 step continue to be recorded where they belong — as DRE annotations (`+ [DRE: C]`, `+ [DRE: I]`) on the attack path — not in the cluster's cause-side definition.

**Harmonization.** The v2.3.2 wording is applied consistently across `tlctc-framework.v2.3.json`, `tlctc-v2.3-core.md`, `tlctc-glossary.md`, `glossary/tlctc-glossary.json`, `README.md`, the `tlctc-classify` skill, and the HTML tools (`threat-modeling.html`, `control-matrix.html`, `cbp-app.html`). The generated `okf/` bundle is rebuilt from these sources. The frozen `tlctc-framework.v2.0.json` dictionary and the v2.0 whitepaper are left as the historical v2.0 record.

## Clarification — v2.4 (2026-07-28)

A single clarifying, backward-compatible change to the **interaction model**, touching **Axiom II** and **R-ROLE**. Unlike v2.3.1 and v2.3.2, this is not an erratum: no field was wrong, and no classification changes. Cluster identity, IDs, definitions, attacker's views, generic vulnerabilities, topology, and all boundary tests are **unchanged**; the axiom set is unchanged in count and numbering, and no rule was added or removed. **Classifications valid under v2.3.2 remain valid under v2.4.**

| Element | Before (v2.3.2) | After (v2.4) |
|---|---|---|
| Axiom II statement | "All networked systems can be abstracted as client-server interaction." | "All system interactions, networked or intra-system, can be abstracted as client-server interaction." |
| R-ROLE statement | "Classify by the role of the component containing the flaw relative to the attacker: server-role flaw = #2, client-role flaw = #3." | *(unchanged first sentence)* + "Roles are established by call direction at any interface, including intra-system privilege interfaces (syscall, hypercall, IPC, driver IOCTL); a network is not a precondition." |

**Justification.** The prior Axiom II wording was read by some implementers as making a *network* a precondition of the client–server abstraction, which would place intra-system privilege interfaces — syscall, hypercall, IPC, driver IOCTL — outside the interaction model and leave their exploitation unclassifiable under #2/#3. That reading was never intended: a syscall establishes exactly the same caller–called relation as a remote protocol exchange, and **Axiom I** (the framework is generic and does not differentiate by system type) already forbids treating a transport as a scope boundary. Restating Axiom II without "networked" removes the ambiguity at its source; extending R-ROLE makes the operational consequence explicit, so that a kernel handling a crafted syscall from a lower-privileged process resolves to **server-role (#2)**, and a higher-privileged component consuming data returned from a lower-privileged one resolves to **client-role (#3)**.

**Relationship to R-INTRA-7 (important).** The clarification does **not** make intra-system boundaries a classification input. Per **R-INTRA-7**, the boundary *crossing* remains an observability annotation; the cluster follows from the role at the interface, exactly as it does across a network. The `|[privilege][@user→@root]|` operator records depth of compromise, not category.

**Not promoted to core.** Vertical stack analysis (whitepaper §13.5) remains applied guidance. It introduces no generic vulnerability, axiom, or disambiguation rule, and is fully derivable from Axiom II + R-ROLE + R-INTRA-7 over the intra-system `privilege` boundary context.

**Artifacts.** New dictionary `json-schemas/layer-1/tlctc-framework.v2.4.json` (differs from `tlctc-framework.v2.3.json` in metadata, the Axiom II statement, and the R-ROLE statement, plus explanatory `notes` on those two entries). The v2.3 dictionary is **retained unchanged** as the frozen record for classifications made under 2.3.x.

**Harmonization.** The v2.4 wording is applied consistently across `tlctc-framework.v2.4.json`, `tlctc-v2.3-core.md`, `tlctc-v2.0-whitepaper.md` (Axiom II, R-ROLE Clarification 4, two intra-system rows in the R-ROLE examples table), `tlctc-glossary.md`, `glossary/tlctc-glossary.json`, `README.md`, and the `tlctc-classify` skill. The generated `okf/` bundle is rebuilt from these sources.

## Editorial Alignment — Canonical-String Harmonization (2026-07-02)

**No normative change.** A repository-wide consistency pass eliminating wording drift between the canonical framework dictionary (`tlctc-framework.v2.3.json`) and every document that restates cluster fields. The v2.3 core paper (§4) already declared that each cluster's **Definition**, **Attacker's View**, and **Generic Vulnerability** are reproduced verbatim from the JSON dictionary; this pass enforces that declaration everywhere else, so that human readers and AI classifiers see one — and only one — string per canonical field.

**Changes:**

1. **Whitepaper §4.1** — Definition/Generic Vulnerability/Attacker's View per cluster replaced with the verbatim JSON strings. The previous long-form operational definitions are preserved under a new **Scope** field (structure is now 7 fields; a normative canonical-source note added to §4.1 states that the three JSON-owned fields are governed by the dictionary and Scope/Developer's View/Boundary Tests are governed by the whitepaper). The §4.2.8 Step-2 generic-vulnerability summary table (rows 4, 5, 9) was aligned to canonical vocabulary. The §14.3.2 example content package — previously a mixed v2.0/v2.3.1 snapshot — is now a verbatim v2.3 excerpt.
2. **`tlctc-classify` skill** — rebaselined from "v2.1" to v2.3 (v2.3.1 erratum applied); cluster sections restructured to canonical Definition + Scope, with Generic Vulnerability and Attacker's View verbatim from the dictionary; canonical-source note added to the preamble.
3. **`README.md`** — generic-vulnerability table aligned to canonical strings; the long-form section retitled from "Canonical Definitions" to "Cluster Scope (operational)" with a pointer to the dictionary.
4. **`tlctc-glossary.md`** — `#8` sub-cluster labels renamed from "Direct/Indirect Physical Access" to the canonical **#8.1 mechanical (contact) / #8.2 signal (no contact)** vector names (entry + RFID Skimming, TEMPEST, Van Eck Phreaking cross-references); `#8` generic-vulnerability sentence aligned.
5. **`tools/threat-modeling.html`** — embedded cluster-definition object aligned to canonical strings.
6. **Agentic-AI attack paths (E–I)** — step notes citing the pre-v2.3 #7 generic-vulnerability wording updated to the canonical string.

**Rationale.** A classification skill inherits whatever ambiguity exists in its references. Divergent restatements of the same canonical field are precisely the edge cases where an LLM classifier diverges run-to-run; this pass freezes a single wording per field across the repository. Long-form operational text was preserved (relabeled as Scope), so no analytical content was lost.
