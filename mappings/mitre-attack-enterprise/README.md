# MITRE ATT&CK Enterprise → TLCTC Mapping

This directory contains the complete mapping of **MITRE ATT&CK Enterprise** techniques to **TLCTC threat clusters**, bridging operational detection with strategic risk management.

> **Pinned to ATT&CK Enterprise v20.0** (2026-10-13). The 32 techniques new in that update are AI-generated; the project owner accepted the judgement calls among them on 2026-11-02 (T1684.002, T1685.003, the T1696 family and T1027.018).
>
> **Provenance & validation (read before relying on the numbers).** These cluster assignments are AI-generated and human-reviewed, but not yet independently validated. This mapping is the source of truth for the derived **Sigma** view, so any classification error here propagates downstream. A stratified human-expert validation (Cohen's κ) of a ~100-technique sample is the planned highest-leverage check — validating this base also validates everything derived from it.

## Purpose

MITRE ATT&CK and TLCTC answer fundamentally different questions:

| Framework | Question | Audience |
|-----------|----------|----------|
| **MITRE ATT&CK** | "What can we detect?" — Observable adversary behaviors | SOC, Detection Engineering |
| **TLCTC** | "What vulnerability enables this?" — Root causes and risk | CISO, Risk Management, Board |

This mapping connects the two: every ATT&CK technique is classified by the **generic vulnerability** it exploits, expressed in TLCTC cluster notation. This enables organizations to aggregate SOC detections into strategic risk exposure metrics.

## Files

| File | Description |
|------|-------------|
| [`tlctc-enterprise-attack.json`](tlctc-enterprise-attack.json) | 706 technique mappings with rationale, tactics, and platforms, plus 24 retired entries |
| [`decision-tree.md`](decision-tree.md) | Classification methodology and disambiguation logic |
| [`examples/soc-to-risk-walkthrough.md`](examples/soc-to-risk-walkthrough.md) | Worked example: translating SOC detections to risk register entries |

## JSON Schema

Each entry in `tlctc-enterprise-attack.json` follows this structure:

```json
{
  "techniqueId": "T1059.001",
  "techniqueName": "Command and Scripting Interpreter: PowerShell",
  "tlctcMapping": "#1 | (#1 → #7)",
  "tlctcMappingName": "Abuse of Functions | (Abuse of Functions → Malware)",
  "mappingRationale": "Context-dependent: #1 when using PowerShell within its designed scope...",
  "techniqueDescription": "Adversaries may abuse PowerShell commands and scripts...",
  "tactics": ["Execution"],
  "platforms": ["Windows"]
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `techniqueId` | string | MITRE ATT&CK technique ID (e.g., `T1059.001`) |
| `techniqueName` | string | Human-readable technique name |
| `tlctcMapping` | string | Normalized TLCTC cluster mapping using path notation |
| `tlctcMappingName` | string | Human-readable cluster name(s) matching the mapping |
| `mappingRationale` | string | Detailed argument explaining why this mapping applies |
| `techniqueDescription` | string | MITRE's description of the technique |
| `tactics` | string[] | ATT&CK tactics (e.g., `["Execution", "Persistence"]`) |
| `platforms` | string[] | Applicable platforms (e.g., `["Windows", "Linux"]`) |

### Retired Techniques

`mappings` holds exactly the active techniques of the pinned ATT&CK version. Entries that ATT&CK has since revoked or deprecated move to the top-level `retired` array, with `attackStatus` (`revoked` or `deprecated`) and `replacedBy` (the replacement ID, or `null`). They stay resolvable because detection rules, alerts and published flows keep using old IDs such as T1562.001. Consumers that look up an ID should read both arrays.

## Notation

The `tlctcMapping` field uses standardized notation:

| Symbol | Meaning | Example |
|--------|---------|---------|
| `→` | Sequential step (A enables B) | `#1 → #7` = Abuse of Functions enables Malware execution |
| `\|` | Alternative (depends on context) | `#1 \| #7` = either Abuse of Functions or Malware |
| `( )` | Groups a multi-step path in alternatives | `#7 \| (#1 → #7)` = Malware alone, or Abuse leading to Malware |
| `N/A` | Not directly mappable | Attacker preparation, not a threat against your assets |

## The "Technique in Context" Principle

The same ATT&CK technique can map to different TLCTC clusters depending on implementation. Never map just the label — always ask:

> *"When an adversary uses this technique **in this way**, **in this domain**, what generic vulnerability is being abused on the protected asset?"*

**Example — T1059.001 (PowerShell):**
- **#1** — Legitimately invoking `PowerShell.exe` with expected parameters
- **#7** — Executing a foreign malicious script
- **#1 → #7** — Abusing PowerShell to invoke and execute a foreign script (most common)

## Domain Scoping

Before mapping, determine where the technique occurs:

| Domain | Description | Mapping Guidance |
|--------|-------------|------------------|
| `@Org` | Your organization's environment | Your risk scope — map to TLCTC |
| `@3P` | Third-party / supply chain | May affect you via **#10** |
| `@AttackerInfra` | Attacker's own infrastructure | Threat potential, not threat — **N/A** |
| `@OtherVictims` | Other organizations being compromised | Threat potential, not your threat — **N/A** |

Most Resource Development techniques (and pure-OSINT Reconnaissance techniques) fall under `@AttackerInfra` / `@External` and are classified as **N/A**. Reconnaissance techniques that *do* cross into `@Org` are classified: active scanning (T1595*) → `#1` with `[DRE: C]`; phishing-for-information (T1598*) → `#9` with `[DRE: C]`.

## Statistics

- **706** total technique entries (227 techniques, 479 sub-techniques)
- **24** retired entries, outside that count
- **45** unique mapping values (single clusters, alternatives, and attack paths)
- **15** ATT&CK tactics covered
- **88** techniques classified as N/A (no `@Org` boundary crossing / attacker preparation)

### Cluster Distribution (top 10)

| Mapping | Count | Description |
|---------|-------|-------------|
| `#1` | 182 | Abuse of designed functions |
| `#1 → #7` | 176 | Function abuse enabling malware execution |
| `N/A` | 88 | Not directly mappable (no `@Org` boundary crossing) |
| `#1 \| #7` | 57 | Context-dependent: function abuse or malware |
| `#7` | 46 | Direct malware execution |
| `#1 → #4` | 28 | Function abuse leading to credential use |
| `#4` | 18 | Direct identity theft (credential application) |
| `#4 → #1` | 15 | Credential use enabling function abuse |
| `#7 \| (#1 → #7)` | 12 | Malware execution, possibly via abused launcher |
| `#9` | 9 | Social engineering (info elicitation / internal phishing / impersonation) |
| `#6` | 8 | Flooding attack |
| `(#1 \| #7) → #4` | 7 | Credential extraction (either mode) then application |
| `#9 → #7` | 7 | Social engineering enabling malware |
| `#1 \| #10` | 3 | Function abuse or subverted third-party signing trust (T1553, .001, .002) |

## Key Mapping Rules

1. **R-EXEC**: If foreign code executes, record a `#7` step — never absorb execution into the enabling cluster
2. **R-CRED**: Credential acquisition maps to the enabling cluster; credential *use* is always `#4`
3. **R-ROLE**: Server-side flaw = `#2`; client-side flaw = `#3`
4. **R-SUPPLY**: `#10` is placed at the Trust Acceptance Event, not at the upstream compromise — and only where the trust artifact, or the third party issuing it, was subverted (v2.6 subversion test). A flaw in a legitimately supplied component is `#2`/`#3`; presenting a partner's or IdP-issued credential is `#4`

See [`decision-tree.md`](decision-tree.md) for the full classification methodology.

## Interactive Explorer

Browse the mapping interactively at [tlctc.net/tlctc-mitre-mapping.html](https://www.tlctc.net/tlctc-mitre-mapping.html).

## License

CC BY 4.0 — See [LICENSE](../../LICENSE).
