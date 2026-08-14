# TLCTC Core — Consolidation & Version Traceability

**v2.3.0** introduced NO new normative content. Every element traces to finalized v2.1 source. **v2.3.1** and **v2.3.2** each add one deliberate, axiom-justified normative correction — see the Erratum sections below. **v2.4** adds one clarifying, backward-compatible change to the interaction model — see the Clarification section below. **v2.5** adds two disambiguation rules (R-CHANNEL, R-SUBSTRATE) and, in a pre-publication consistency pass, retightens the #2/#3 definition strings and formalizes the rule registry — see the v2.5 sections below.

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

## Normative Change — v2.5: R-CHANNEL and R-SUBSTRATE (2026-08-07)

**Normative, and NOT classification-preserving.** Unlike the v2.4 clarification, v2.5 alters decisions that were defensible under v2.4. Two disambiguation rules are added, bringing the rule count from 16 to 18.

| Rule | Statement (abbreviated) |
|---|---|
| **R-CHANNEL** | Where the defective logic is itself a communication-path control — peer authenticity (certificate validation, chain of trust, hostname matching, expiry or revocation checking), channel encryption, or algorithm negotiation — the generic vulnerability is the lack of sufficient control over the communication path and the weakness is `#5`, not `#2`/`#3` under R-ROLE. |
| **R-SUBSTRATE** | Classify as `#8` only where a physical-layer property of the substrate — charge, voltage, electromagnetic emission, temperature, emission-borne timing, wear, material state — is itself the exploited generic vulnerability. Where the physical layer is only the readout channel for a defect in implemented logic, classify by that defect (`#2`/`#3` per R-ROLE). Attacker proximity or possession is not the test. |

**Justification.** Both rules resolve the same structural ambiguity that **R-FLOOD** already resolved for `#6`: a weakness describable either as a specific generic vulnerability or as a generic code defect. In each case the specific reading wins and R-ROLE is the residual test. Two defects motivated the addition:

1. **The `#5` case.** Certificate-validation weaknesses were being classified `#2`/`#3` because they read as "the code failed to validate," leaving CWE-295 and its children at `#3` while CWE-940/757/300/311/319 — the same generic vulnerability — sat at `#5`. The `#5` Developer's View already names "proper certificate/path validation," so the taxonomy was internally inconsistent.
2. **The `#8` case.** `#8` was being assigned on the presence of *hardware*, which is a location rather than a cause. The obvious correction — gating on whether the attacker needs physical access — fails in the other direction, because Rowhammer requires no physical access yet unambiguously abuses a physical property. The discriminator is whether the attack is against the *implemented logic* or the *physical representation* that logic runs on.

**Relationship to existing rules.** R-CHANNEL classifies the weakness; **R-MITM** sequences the attack path (position acquisition versus action) and is unaffected. R-SUBSTRATE is the *admission* test for `#8`; the legacy **R-PHYSICAL** is the *sequencing* rule, and R-PHYSICAL gains a clarification stating this, since its "unauthorized physical interaction" wording could be misread as requiring attacker presence.

**Artifacts.** New dictionary `json-schemas/layer-1/tlctc-framework.v2.5.json`. The v2.4 dictionary is **retained unchanged** as the frozen record for classifications made under 2.4, as v2.3 was before it.

**Classification impact.** The CWE mapping was re-adjudicated: the certificate/peer-authenticity family (CWE-295/296/297/298/299/370/593/599) moved to `#5`; CWE-923/941/614 moved to `#5` as the remainder of R-CHANNEL's scope; and the `#8` bucket was re-audited in full, from 81 entries to 16, with the remainder resolving to `#2` (52), `#2 | #3` (4), `#2 | #8` (7) and `#1` (2). Every decision is recorded per entry in `mappings/mitre-cwe/tlctc-cwe.json` under `metadata.audit_history`.

**Harmonization.** Applied across `tlctc-framework.v2.5.json`, `tlctc-v2.3-core.md` (§6.1 and the `#5`/`#8` boundary tests), `tlctc-v2.0-whitepaper.md` (full rule sections, Step-3 decision table, rule summary table, R-PHYSICAL Clarification 4), `tlctc-v2.3-application.md` (Step-3 reminders), `tlctc-glossary.md`, `mappings/mitre-cwe/decision-tree.md` (Q2 and Q7 guards), the `tlctc-classify` skill, and `tools/cwe-explorer.html`. The generated `okf/` bundle is rebuilt from these sources.

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

## v2.5 Consistency Pass (2026-08-08)

A repository-wide pass establishing **v2.5 as the single consistent basis**, resolving the version and rule-registry drift accumulated across v2.3–v2.5. Triggered by an external specification review; one normative retightening, everything else is governance/consistency.

**Normative change (documented in the dictionary notes):**

- **#2/#3 substrate-neutral retightening.** `definition` and `attackers_view` for `#2`/`#3` changed from "source code implementation" wording to "implementation flaws within a component acting in a server/client role". This makes the substrate-neutrality already established by R-ROLE and R-SUBSTRATE explicit in the definitions themselves (software, firmware, microcode, and hardware logic all qualify; the role of the flawed component classifies, never the location of the flaw). It also ratifies, at the definition level, the CWE mapping's completed 2026-08-07 R-SUBSTRATE re-audit (full #8 bucket 81 → 16; the entries once parked on the hardware-substrate question were decided there on the property test) — no mapping changes result, and no open question remains on this family. `generic_vulnerability` fields were already substrate-neutral and are unchanged; cluster identity, IDs, and topology unchanged.

**Version governance:**

- Canonical declaration added to the core paper: framework specification = **v2.5**; normative authority = exactly one artifact, `json-schemas/layer-1/tlctc-framework.v2.5.json`; companions declare what they implement.
- Files renamed to match their content: `tlctc-v2.3-core.md` → `tlctc-v2.5-core.md` (it already declared Version 2.5), `tlctc-v2.3-application.md` → `tlctc-v2.5-application.md` (ported 2.3 → 2.5, now carries an explicit **Implements: v2.5** line), PDFs renamed accordingly, this traceability file renamed version-neutral.
- Glossary rebased to **v2.5** (was self-declaring 2.0/2.1 while containing v2.4-marked entries) with an explicit Implements line; `glossary/tlctc-glossary.json` sources updated to v2.5, version 0.2.0.
- Whitepaper currency note updated to v2.5; its §4.1 JSON-owned strings and §14.3.2 dictionary excerpt (which claimed v2.5 but reproduced the v2.4 snapshot) re-synced verbatim.

**Rule-registry formalization:**

- Core paper §6 corrected from "six core rules" to **eight** (R-EXEC, R-ROLE, R-FLOOD, R-SUPPLY, R-MITM, R-CHANNEL, R-SUBSTRATE, R-CRED) and now states the complete 18-rule registry plus the retired-alias policy: a rule ID is never reused with a different proposition.
- **Deprecated aliases enumerated:** R-ABUSE, R-HUMAN, R-PHYSICAL (v2.0 whitepaper) — substance carried by cluster definitions/boundary tests; marked as deprecated aliases in the glossary.
- **Draft-series withdrawal:** the v2.1 draft numberings R-TRANSIT-1/2/4–8, R-INTRA-1–6/8, and R-UNRES-1/4 are withdrawn. The glossary's quick reference now mirrors the canonical 18-rule registry and carries a deprecated-IDs table.
- **Numbering erratum recorded:** draft R-INTRA-7 ("distinct vulnerabilities") ≠ canonical R-INTRA-7 ("no cluster change"); draft R-UNRES-4 (conf=low threshold) ≠ canonical R-UNRES-9. The glossary previously restated the draft meanings under the canonical IDs — a silent semantic change of normative IDs, now corrected and documented in the glossary's R-INTRA entry so it cannot recur.

**Claim hardening (per external review):**

- "Non-overlapping / mutually exclusive **by construction**" reworded throughout the core: completeness is stated as a **falsifiable hypothesis** (no counterexample yet under the stated axioms and rules, with an explicit challenge protocol), and mutual exclusivity as a property **produced by** the definitions, boundary tests, and precedence rules — raw observable properties may overlap; the rules force uniqueness. §3.2 and §8 rewritten accordingly.
- Glossary attack-velocity overclaim ("single most accurate predictor … only metric that truthfully measures control effectiveness") deleted; replaced with the defensible statement that Δt bounds the detection-and-response window.
- DCS entry hardened: DCS measures **detection timing adequacy**, not coverage; a scope note now states that detection probability and rule coverage must be assessed separately.

**Classification fix:**

- Application paper §KRI example corrected: harvested-but-never-used phishing credentials are `#9 + [DRE: C]` with **no** `#4` step (per R-CRED, `#4` exists only at credential presentation); the averted `#4` is the near-miss the KRI counts. The previous text asserted a realized `#9 → #4`, contradicting R-CRED.

**Harmonization.** Applied across `tlctc-framework.v2.5.json`, `tlctc-v2.5-core.md`, `tlctc-v2.5-application.md`, `tlctc-glossary.md`, `glossary/tlctc-glossary.json`, `tlctc-v2.0-whitepaper.md`, `README.md`, `CLAUDE.md`, the `tlctc-classify` skill, `tools/threat-modeling.html`, `tools/radar-tlctc-app.html`, `agentic-ai/attack-paths/path-F-runtime-exploit.json`, and `mappings/mitre-cwe/tlctc-cwe.json` (audit-history ruling entry). The generated `okf/` bundle is rebuilt from these sources.

## Erratum — v2.5.1 (2026-08-14)

A single normative clarification to **R-CRED** (self-issued identity), applied in place to the v2.5 dictionary. Following the v2.3.1/v2.3.2 erratum precedent (and as the framework schema requires — `tlctc_version` matches `^\d+\.\d+$`), the machine `tlctc_version` field stays **2.5** and the erratum is recorded in `metadata.notes`; "v2.5.1" is the prose erratum label. `schema_version` is unchanged at 2.0.0 — no schema-shape change. No cluster identity, ID, definition, attacker's view, generic vulnerability, or topology changed; the axiom set and rule count (**18**) are unchanged.

| Element | Before | After |
|---|---|---|
| R-CRED statement | "Credential application (use of the credential to authenticate) is ALWAYS classified as #4 Identity Theft, regardless of the acquisition method. These are separate attack steps." | *(unchanged first clause)* + "PROVIDED the identity claimed is not the presenter's own. A credential issued to the presenter by the target system through a designed enrolment function makes the presenter its authentic holder; such use MUST NOT be classified as #4, and where the enrolment function granted the identity or its permissions outside their intended population or scope, the enrolment step maps to #1." |
| Core §4 boundary tests | — | #1 gains an enrolment-scope test (out-of-scope enrolment → #1; authentication as self is not #4); #4 gains a self-issued test (system-issued credential → not #4; enrolment-as-existing-identity → #1 → #4). |
| Canonical declaration | "…supplies the derivation, boundary tests, and notation…" | States explicitly that per-cluster boundary tests are **normative and homed in the core paper (§4)** by design; the dictionary deliberately carries no boundary-test field. |

**Justification.** The #4 generic vulnerability is the binding gap "between a presented credential and **the authentic holder of the identity it claims**." When the target system itself issued the credential to the presenter through a designed enrolment function, that binding is intact — the presenter *is* the authentic holder — so authentication as self exploits no #4 generic vulnerability; the exploited weakness is the scope of the enrolment function and of the permissions attached to the resulting principal, which is **#1 Abuse of Functions**. The clarification promotes into the rule registry a scope the #4 field already implied, closing a gap in which an attacker holding a self-enrolled principal was read as #4 by analogy to "unauthorized account use." The higher-abstraction test is whether the system is *deceived about who is authenticating*; attacker effort is never the criterion (a replayed session cookie is #4; elaborate fraudulent self-registration is #1).

**Not fully classification-preserving.** Unlike the v2.4 clarification, this erratum can change a decision: records that classified *use* of a self-enrolled account as #4 SHOULD be re-checked against the proviso. Fictitious/pseudonymous self-registration is #1; enrolment completed as an existing identity is #1 → #4.

**Companion (non-normative).** The TI Sharing Profile gains an optional step-level `extensions.ti.identity_relation` field (`impersonated` | `self-issued` | `unknown`) with a validator consistency check: `#4` + `self-issued` is a mechanical contradiction. No base Layer 3 schema change (reserved `extensions` namespace).

**Harmonization.** Applied across `tlctc-framework.v2.5.json` (R-CRED statement + notes, metadata notes, version), `tlctc-v2.5-core.md` (declaration, §6 R-CRED, §4 #1/#4 boundary tests), `tlctc-glossary.md` (R-CRED entry, quick-reference table, Credential Application entry), `glossary/tlctc-glossary.json` (R-CRED entry), the `tlctc-classify` skill (R-CRED boundary tests, rule section, Kerberos LOTL worked example), and `tlctc-ti-sharing-profile.md` (§3.1 field + consistency check). The generated `okf/` bundle, HTML docs, and PDFs are rebuilt from these sources.
