# MITRE CWE → TLCTC Mapping

This directory contains the mapping of **MITRE Common Weakness Enumeration (CWE)** entries to **TLCTC threat clusters**, connecting weakness taxonomy to cause-oriented threat classification.

> **Note:** This mapping was generated with AI assistance and is marked **experimental**. Community review and contributions are welcome.

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
| **Allowed** | 754 | High confidence — CWE is specific enough for unambiguous classification |
| **Allowed-with-Review** | 90 | Reasonable mapping but context-dependent — review recommended |
| **Discouraged** | 41 | CWE is too abstract or generic for reliable mapping |
| **Prohibited** | 83 | CWE is a category/view/deprecated entry, not a concrete weakness |
| **Unreviewed** | 19 | No verdict assigned yet |

## Statistics

- **987** total CWE entries
- **15** unique mapping values
- **229** context-dependent mappings (role-dependent)
- **754** high-confidence (`Allowed`) mappings

### Cluster Distribution

| Mapping | Count | Description |
|---------|-------|-------------|
| `#2 \| #3` | 219 | Server or client code flaw (role-dependent) |
| `#1` | 195 | Abuse of designed functions |
| `N/A` | 194 | Not directly mappable |
| `#2` | 175 | Server-side implementation flaw |
| `#8` | 90 | Physical attack |
| `#6` | 33 | Flooding / resource exhaustion |
| `#4` | 18 | Identity theft / credential weakness |
| `#10` | 17 | Supply chain trust weakness |
| `#3` | 12 | Client-side implementation flaw |
| `#5` | 8 | Man in the Middle / communication path |

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
