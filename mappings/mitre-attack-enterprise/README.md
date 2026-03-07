# MITRE ATT&CK Enterprise → TLCTC Mapping

This directory contains the complete mapping of **MITRE ATT&CK Enterprise** techniques to **TLCTC threat clusters**, bridging operational detection with strategic risk management.

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
| [`tlctc-enterprise-attack.json`](tlctc-enterprise-attack.json) | 698 technique mappings with rationale, tactics, and platforms |
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

Most Reconnaissance and Resource Development techniques fall under `@AttackerInfra` and are classified as **N/A**.

## Statistics

- **698** total technique entries
- **40** unique mapping values (single clusters, alternatives, and attack paths)
- **15** ATT&CK tactics covered
- **94** techniques classified as N/A (attacker preparation / threat potential)

### Cluster Distribution (top 10)

| Mapping | Count | Description |
|---------|-------|-------------|
| `#1` | 188 | Abuse of designed functions |
| `#1 → #7` | 153 | Function abuse enabling malware execution |
| `N/A` | 94 | Not directly mappable (attacker preparation) |
| `#1 \| #7` | 61 | Context-dependent: function abuse or malware |
| `#7` | 51 | Direct malware execution |
| `#1 → #4` | 31 | Function abuse leading to credential use |
| `#4` | 15 | Direct identity theft (credential application) |
| `#4 → #1` | 15 | Credential use enabling function abuse |
| `#1 \| #10` | 10 | Function abuse or supply chain |
| `#9 → #7` | 8 | Social engineering enabling malware |

## Key Mapping Rules

1. **R-EXEC**: If foreign code executes, record a `#7` step — never absorb execution into the enabling cluster
2. **R-CRED**: Credential acquisition maps to the enabling cluster; credential *use* is always `#4`
3. **R-ROLE**: Server-side flaw = `#2`; client-side flaw = `#3`
4. **R-SUPPLY**: `#10` is placed at the Trust Acceptance Event, not at the upstream compromise

See [`decision-tree.md`](decision-tree.md) for the full classification methodology.

## Interactive Explorer

Browse the mapping interactively at [tlctc.net/tlctc-mitre-mapping.html](https://www.tlctc.net/tlctc-mitre-mapping.html).

## License

CC BY 4.0 — See [LICENSE](../../LICENSE).
