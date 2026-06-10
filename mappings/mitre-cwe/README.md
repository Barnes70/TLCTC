# MITRE CWE → TLCTC Mapping

This directory contains the mapping of **MITRE Common Weakness Enumeration (CWE)** entries to **TLCTC threat clusters**, connecting weakness taxonomy to cause-oriented threat classification.

> **Provenance:** AI-generated, human-reviewed. The 2026-05-05 v2.1 audit closed the Unreviewed bucket, applied R-EXEC consistently to execution-enabling CWEs, reclassified enabling-condition CWEs to the cluster they enable (per policy ruling), and narrowed the Allowed-with-Review queue to genuine context-dependence cases. See `tlctc-cwe.json` `metadata.audit_history` for the change log. These assignments are not yet independently validated; the **SARIF classifier** and any CVE/KEV overlays derive from this base, so errors propagate downstream. A stratified human-expert validation (Cohen's κ) of a ~100-CWE sample is the planned highest-leverage check.

## Purpose

CWE and TLCTC answer fundamentally different questions:

| Framework | Question | Focus |
|-----------|----------|-------|
| **MITRE CWE** | "What is the technical flaw?" | Weakness type (coding error, design flaw, configuration issue) |
| **TLCTC** | "What generic vulnerability does this enable?" | Root cause cluster for risk management |

This mapping connects the two: every CWE weakness is classified by the **generic vulnerability** it enables, expressed in TLCTC cluster notation. This allows organizations to translate vulnerability scan findings and code audit results into strategic risk exposure.

### The Hierarchy

```
CWE (Weakness Type) → CVE (Specific Instance) → Generic Vulnerability → TLCTC Cluster (#1–#10)
```

A CWE describes a *class* of flaws. Each specific CVE is an instance of a CWE. TLCTC classifies by the generic vulnerability that the flaw enables an attacker to exploit.

## Why Not a Simple 1:1 Table?

Three factors prevent universal one-to-one CWE→TLCTC mapping:

1. **Role-dependent mapping (R-ROLE):** The same weakness maps to different clusters depending on where it exists. CWE-787 (Out-of-bounds Write) is **#2** in server-side code, **#3** in client-side code. This accounts for 229 context-dependent entries.

2. **Overly broad CWEs:** Umbrella entries like CWE-20 (Improper Input Validation) span multiple clusters — they are root causes of #1, #2, #3, and #6 depending on context. These are marked `Discouraged`.

3. **Category/View entries:** CWE includes organizational nodes (categories, views) that are not concrete weaknesses. These are marked `Prohibited`.

## Files

| File | Description |
|------|-------------|
| [`tlctc-cwe.json`](tlctc-cwe.json) | 987 CWE mappings with rationale, verdict, and CVE references |
| [`decision-tree.md`](decision-tree.md) | Classification methodology for CWE→TLCTC mapping |
| [`examples/cwe-to-control-walkthrough.md`](examples/cwe-to-control-walkthrough.md) | Worked example: vulnerability findings to risk controls |

## JSON Schema

Each entry in `tlctc-cwe.json` follows this structure:

```json
{
  "cweId": "CWE-79",
  "cweName": "Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')",
  "cweStatus": "Stable",
  "tlctcMapping": "#2 → #7 | #3",
  "tlctcMappingName": "Exploiting Server → Malware | Exploiting Client",
  "mappingRationale": "Reflected/Stored XSS exploits a server-side coding flaw (#2) to deliver a script that the browser executes (#7). DOM-based XSS exploits a client-side coding flaw (#3).",
  "mappingVerdict": "Allowed",
  "contextDependent": true,
  "cveReferences": ["CVE-2021-25926", "CVE-2021-25963"]
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `cweId` | string | CWE identifier (e.g., `CWE-79`) |
| `cweName` | string | Human-readable weakness name |
| `cweStatus` | string | CWE maturity status (`Stable`, `Draft`, `Incomplete`, `Deprecated`) |
| `tlctcMapping` | string | TLCTC cluster mapping using path notation |
| `tlctcMappingName` | string | Human-readable cluster name(s) |
| `mappingRationale` | string | Argument explaining why this mapping applies |
| `mappingVerdict` | string | Confidence level (see Verdict System below) |
| `contextDependent` | boolean | `true` if mapping varies by implementation context |
| `cveReferences` | string[] | Known CVEs associated with this CWE |

## Notation

The `tlctcMapping` field uses the same notation as the ATT&CK mapping:

| Symbol | Meaning | Example |
|--------|---------|---------|
| `→` | Sequential step (A enables B) | `#2 → #7` = Server exploit enables code execution |
| `\|` | Alternative (depends on context) | `#2 \| #3` = Server-side or client-side depending on role |
| `N/A` | Not directly mappable | Abstract CWE, category node, or deprecated entry |

## Verdict System

Each mapping carries a confidence verdict:

| Verdict | Count | Meaning |
|---------|-------|---------|
| **Allowed** | 756 | High confidence — CWE is specific enough for unambiguous classification |
| **Allowed-with-Review** | 16 | Cluster genuinely depends on a use-context that varies between CVE instances — review at instance level |
| **Discouraged** | 171 | CWE is too abstract or generic for reliable mapping (umbrella CWE) OR is a code-quality / maintainability / consequence-only observation with no defensible threat cluster |
| **Prohibited** | 44 | CWE is a category/view/list/deprecated entry, not a concrete weakness |

## Statistics

- **987** total CWE entries
- **22** unique mapping values
- **229** context-dependent mappings (role-dependent)
- **756** high-confidence (`Allowed`) mappings

### Cluster Distribution

| Mapping | Count | Description |
|---------|-------|-------------|
| `#2 \| #3` | 221 | Server or client code flaw (role-dependent) |
| `N/A` | 176 | Not directly mappable (Discouraged or Prohibited) |
| `#1` | 169 | Abuse of designed functions |
| `#2` | 165 | Server-side implementation flaw |
| `#8` | 90 | Physical attack |
| `#4` | 38 | Identity theft / credential weakness |
| `#6` | 32 | Flooding / resource exhaustion |
| `#5` | 16 | Man in the Middle / communication path |
| `#10` | 14 | Supply chain trust weakness |
| `#3` | 12 | Client-side implementation flaw |
| `#4 \| #5` | 9 | Predictable random values (token vs key context) |
| `#9` | 8 | Social engineering / UI deception |
| `#2 → #7 \| #3` | 8 | XSS-style: server-delivered script executes client-side |
| `#2 → #7 \| #3 → #7` | 7 | Code injection / deserialization / template injection (role-dependent RCE) |
| `#2 → #7` | 6 | Server-side code/command injection with execution |
| `#1 → #7` | 4 | Designed function abused to load foreign code (DLL hijacking, upload+exec) |
| `#7` | 4 | Direct malware presence |
| `#10 → #7` | 3 | Trust-accepted untrusted code that subsequently executes |
| `#5 \| #4` | 2 | Crypto algorithm weakness (channel vs credential context) |
| `#4 \| #6` | 1 | Missing rate-limiting (auth-endpoint vs resource-endpoint) |
| `#1 \| #4` | 1 | Predictable values (parent of #4 \| #5 group) |
| `#10 \| #5` | 1 | Trust artifact compromise vs channel compromise |

## Key Mapping Rules

1. **R-ROLE**: Server-side flaw = `#2`; client-side flaw = `#3`. The same CWE maps to different clusters depending on where the vulnerable code runs.
2. **R-EXEC**: If the weakness enables foreign code execution, record a `→ #7` step.
3. **R-CRED**: Weaknesses that expose credentials map to their enabling cluster; credential *use* is always `#4`.
4. **Cause, not consequence**: Map the exploitable weakness, not the impact. CWE-200 (Information Exposure) maps by *how* information is exposed, not *that* it is exposed.

See [`decision-tree.md`](decision-tree.md) for the full classification methodology.

## Interactive Explorer

Browse the mapping interactively at [tlctc.net/tlctc-mitre-cwe-mapping.html](https://www.tlctc.net/tlctc-mitre-cwe-mapping.html).

## License

CC BY 4.0 — See [LICENSE](../../LICENSE).
