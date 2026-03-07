# MITRE ATT&CK → TLCTC Classification Decision Tree

This document provides the step-by-step methodology for mapping any MITRE ATT&CK Enterprise technique to the correct TLCTC cluster(s).

## Prerequisites

Before classifying, establish two things:

1. **Domain** — Where does this technique execute relative to your organization?
   - `@Org` → proceed with mapping
   - `@AttackerInfra` or `@OtherVictims` → **N/A** (threat potential, not threat)
   - `@3P` → consider **#10** if trust boundary is crossed into your environment

2. **Protected Asset** — Which asset in your scope is affected? TLCTC requires a concrete target; abstract technique descriptions without a target asset cannot be classified.

## The Decision Tree

Walk through these questions **in order**. Stop at the first match.

```
Q1: Is the attacker abusing a DESIGNED function/feature/API/configuration,
    with NO code flaw and NO foreign binary required?
    ├── YES → #1 Abuse of Functions
    │         (e.g., admin tool misuse, API abuse, config manipulation)
    └── NO ↓

Q2: Is the attacker exploiting a CODE IMPLEMENTATION FLAW on the SERVER side?
    ├── YES → #2 Exploiting Server
    │         (e.g., SQL injection, buffer overflow in server app)
    └── NO ↓

Q3: Is the attacker exploiting a CODE IMPLEMENTATION FLAW in a CLIENT role?
    ├── YES → #3 Exploiting Client
    │         (e.g., browser exploit, PDF reader vulnerability)
    └── NO ↓

Q4: Is the attacker's main power that they ACT AS A LEGITIMATE IDENTITY
    using credentials/tokens/keys?
    ├── YES → #4 Identity Theft
    │         (credential APPLICATION — the use, not the acquisition)
    └── NO ↓

Q5: Is the attacker intercepting/modifying/relaying communication
    from a privileged position on the path?
    ├── YES → #5 Man in the Middle
    └── NO ↓

Q6: Is the attacker overwhelming resources through volume or intensity?
    ├── YES → #6 Flooding Attack
    │         (Note: if a code bug causes crash, that's #2/#3, not #6)
    └── NO ↓

Q7: Is FOREIGN CODE being executed?
    ├── YES → #7 Malware
    │         (Note: if launched via legitimate tool → #1 → #7)
    └── NO ↓

Q8: Does the attack require physical interaction with hardware/facilities?
    ├── YES → #8 Physical Attack
    └── NO ↓

Q9: Is the attacker psychologically manipulating a human?
    ├── YES → #9 Social Engineering
    └── NO ↓

Q10: Is the attack exploiting trust in a third-party component/service/update?
     ├── YES → #10 Supply Chain Attack
     └── NO → Re-examine. One of the above must apply.
```

## The Software Quadrant: #1, #2, #3, and #7

Most ATT&CK techniques fall into the "software" space. This disambiguation handles the majority:

```
START: Is there a CODE FLAW being exploited?
│
├── YES → Is it server-side or client-side?
│          ├── Server → #2 Exploiting Server
│          └── Client → #3 Exploiting Client
│
│          Note: The payload delivered is usually the NEXT step (#7)
│          giving paths like: #2 → #7 or #3 → #7
│
└── NO → Is FOREIGN CODE being executed?
         │
         ├── YES → #7 Malware
         │         If launched via legitimate tool (LOLBAS) → #1 → #7
         │
         └── NO → #1 Abuse of Functions
                  (Pure abuse of admin tools, APIs, configs)
```

## The Credential Rule

TLCTC Axiom X establishes that credentials have a dual operational nature. This is critical for accurate mapping.

| Phase | Classification | Examples |
|-------|---------------|----------|
| **Acquisition** | Maps to the **enabling cluster** | Keylogger → `#7`; Phishing → `#9`; SQLi → `#2`; MitM → `#5` |
| **Application** | **Always `#4`** | Presenting stolen creds to authenticate → `#4 Identity Theft` |

These are separate attack steps. A complete path looks like:

```
#9 → #4 → #1
```

1. `#9` — Phishing tricked user into entering credentials
2. `#4` — Attacker uses stolen credentials to authenticate
3. `#1` — Attacker abuses admin functions with that authenticated identity

## Handling Reconnaissance and Resource Development

These ATT&CK tactics often describe attacker preparation, not attacks against your assets.

**Rule:** If the technique only affects `@AttackerInfra` or `@OtherVictims`, classify as **N/A — Threat Potential**. Only map to a TLCTC cluster when your organization is the specific target of exploitation.

Examples:
- T1595 "Active Scanning" → **N/A** (attacker scanning from their infra)
- T1588 "Obtain Capabilities" → **N/A** (attacker acquiring tools)
- T1589 "Gather Victim Identity Information" → **N/A** (OSINT, no vulnerability exploited on your asset)

## LOLBAS / Dual-Use Tool Pattern

Many ATT&CK techniques describe "Living off the Land" — using legitimate system tools maliciously. The pattern is almost always:

```
#1 → #7
```

1. `#1` — The legitimate tool (PowerShell, certutil, mshta, etc.) is invoked using its designed interface
2. `#7` — The attacker-controlled script/command/payload executes within that tool's execution environment

The `#1` step reflects that the tool's **designed function** is being abused. The `#7` step reflects that **foreign executable content** runs. Both steps must be recorded (R-EXEC rule).

## Quality Checklist

Before finalizing a mapping, verify:

- [ ] **Domain identified** — Is it clear where this technique happens?
- [ ] **Asset identified** — Which protected asset is affected?
- [ ] **Cause, not consequence** — Are you mapping the vulnerability exploited, not the outcome?
- [ ] **Single step vs. path** — If multiple steps, did you express them as an attack path?
- [ ] **Credentials handled correctly** — Acquisition vs. use distinction applied?
- [ ] **R-EXEC respected** — If code executes, is `#7` recorded?
- [ ] **Context considered** — Same technique label can map differently in different implementations
