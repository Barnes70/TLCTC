# Worked Example: From SOC Detection to Risk Register

This walkthrough demonstrates how to translate a set of MITRE ATT&CK detections into a TLCTC attack path for strategic risk reporting.

## Scenario

Your SOC detects the following sequence of ATT&CK techniques during an incident:

| Time | Detection | ATT&CK Technique |
|------|-----------|-------------------|
| 09:15 | Spearphishing email with malicious attachment | T1566.001 |
| 09:45 | PowerShell execution of encoded commands | T1059.001 |
| 10:02 | OS credential dumping via comsvcs.dll | T1003.001 |
| 10:08 | Valid account used for lateral movement | T1078 |
| 10:25 | Data staged for exfiltration | T1074.001 |

## Step 1: Map Each Technique to TLCTC

Using the [decision tree](../decision-tree.md), classify each detection:

### T1566.001 — Spearphishing Attachment

> Q9: Is the attacker psychologically manipulating a human? **YES**

The phishing email targets human psychology to trick the recipient into opening the attachment. This is **#9 Social Engineering**.

The attachment itself contains malware, but the *phishing step* is purely social engineering. Malware execution is the next step.

### T1059.001 — PowerShell

> Q1: Is the attacker abusing a designed function? **YES** (PowerShell is a legitimate tool)
> Q7: Is foreign code being executed? **YES** (encoded malicious commands)

PowerShell is invoked using its designed interface (#1), but the encoded commands constitute foreign executable content (#7). Per R-EXEC, both steps must be recorded.

Mapping: **#1 → #7**

### T1003.001 — LSASS Memory Credential Dumping

> Q1: Is the attacker abusing a designed function? **YES** (comsvcs.dll MiniDump is a legitimate Windows function)

The attacker uses `rundll32.exe` to call `comsvcs.dll MiniDump` — a designed Windows function being abused to dump LSASS memory. No code flaw, no foreign binary (comsvcs.dll is a system component).

Mapping: **#1** (credential *acquisition* — the credentials aren't used yet)

### T1078 — Valid Accounts

> Q4: Is the attacker acting as a legitimate identity? **YES**

The attacker uses the dumped credentials to authenticate and move laterally. This is credential *application*.

Mapping: **#4 Identity Theft**

### T1074.001 — Local Data Staging

> Q1: Is the attacker abusing a designed function? **YES**

Staging data using standard file operations (copy, move) is pure abuse of designed OS functionality. No code flaw, no foreign code.

Mapping: **#1 Abuse of Functions**

## Step 2: Construct the Attack Path

Chain the individual mappings into a TLCTC attack path with velocity annotations:

```
#9 →[Δt=30m] (#1 → #7) →[Δt=17m] #1 →[Δt=6m] #4 →[Δt=17m] #1 + [DRE: C]
```

Reading this:
1. **#9** — Social engineering (phishing email)
2. **→[Δt=30m]** — 30 minutes until victim opens attachment
3. **(#1 → #7)** — PowerShell abuse enabling malware execution
4. **→[Δt=17m]** — 17 minutes of post-exploitation
5. **#1** — Credential dumping via legitimate function abuse
6. **→[Δt=6m]** — 6 minutes later
7. **#4** — Stolen credentials used for lateral movement
8. **→[Δt=17m]** — 17 minutes of lateral movement
9. **#1** — Data staging via function abuse
10. **+ [DRE: C]** — Consequence: Loss of Confidentiality

## Step 3: Risk Register Translation

### Cluster Exposure Summary

| Cluster | Occurrences | Role in Attack |
|---------|-------------|----------------|
| **#9 Social Engineering** | 1 | Initial access vector |
| **#1 Abuse of Functions** | 3 | Execution, credential access, staging |
| **#7 Malware** | 1 | Post-exploitation payload |
| **#4 Identity Theft** | 1 | Lateral movement enabler |

### Risk Register Entry

> **Incident Classification:** Multi-step intrusion exploiting social engineering as initial vector, progressing through function abuse and identity theft to data exfiltration.
>
> **Primary Exposure:** Social Engineering (#9) and Abuse of Functions (#1)
>
> **Velocity Profile:** VC-3 (minutes between steps) — requires automated detection and response
>
> **Control Gap Analysis:**
> - #9: Email filtering and user awareness insufficient to prevent initial compromise
> - #1: Excessive privileges enabled credential dumping and data staging
> - #4: Lack of behavioral authentication allowed lateral movement with stolen credentials
>
> **Data Risk Event:** Loss of Confidentiality (C)

### What This Enables

- **For the SOC:** Continue detecting T1566, T1059, T1003, T1078. No change to detection engineering.
- **For Risk Management:** Aggregate detections into cluster exposure. The dominance of #1 signals that **excessive function scope** is the primary structural weakness.
- **For Control Design:** The VC-3 velocity profile means detective controls must operate in minutes, not hours. Automated response (SOAR/EDR) is structurally necessary.
- **For the Board:** "Our primary exposure is unauthorized use of legitimate administrative functions, enabled by a social engineering entry point." — actionable, non-technical, and precise.
