# CWE → TLCTC Classification Decision Tree

This document provides the step-by-step methodology for mapping any MITRE CWE weakness to the correct TLCTC cluster(s).

## Prerequisites

Before classifying a CWE, establish two things:

1. **Is this a concrete weakness?** Category nodes, views, and deprecated CWEs cannot be mapped → **Prohibited**.
2. **Is it specific enough?** Umbrella CWEs that span multiple root causes (e.g., CWE-20 "Improper Input Validation") → **Discouraged** or **N/A**.

## The Decision Tree

Walk through these questions **in order**. Stop at the first match.

```
Q0: Is this CWE a Category, View, or Deprecated entry?
    ├── YES → N/A (Prohibited)
    └── NO ↓

Q1: Is this CWE too abstract to determine a single generic vulnerability?
    (e.g., CWE-20 Improper Input Validation, CWE-693 Protection Mechanism Failure)
    ├── YES → N/A (Discouraged)
    └── NO ↓

Q2: Is this a CODE IMPLEMENTATION FLAW?
    (buffer overflow, injection, type confusion, use-after-free, etc.)
    ├── YES → Does the flaw exist in server-side or client-side code?
    │         ├── Server → #2 Exploiting Server
    │         ├── Client → #3 Exploiting Client
    │         └── Could be either → #2 | #3 (context-dependent)
    │
    │         Follow-up: Can the flaw enable code execution?
    │         ├── YES → append → #7 (e.g., #2 → #7)
    │         └── NO → stop here
    └── NO ↓

Q3: Is this a CREDENTIAL or AUTHENTICATION weakness?
    (weak passwords, session fixation, missing authentication, improper token handling)
    ├── YES → #4 Identity Theft
    └── NO ↓

Q4: Is this a COMMUNICATION PATH weakness?
    (missing encryption in transit, certificate validation failure, channel security)
    ├── YES → #5 Man in the Middle
    └── NO ↓

Q5: Is this a RESOURCE EXHAUSTION or CAPACITY weakness?
    (uncontrolled resource consumption, asymmetric resource usage, missing rate limiting)
    ├── YES → #6 Flooding Attack
    │         (Note: if a code bug causes crash, that's #2/#3, not #6)
    └── NO ↓

Q6: Does this weakness enable FOREIGN CODE EXECUTION directly?
    (code injection via designed execution capability, not via code flaw)
    ├── YES → #7 Malware
    │         If via legitimate tool/function → #1 → #7
    └── NO ↓

Q7: Is this a PHYSICAL LAYER weakness?
    (hardware debug interfaces, physical signal leakage, insufficient physical protection)
    ├── YES → #8 Physical Attack
    └── NO ↓

Q8: Is this a TRUST RELATIONSHIP weakness with third-party components?
    (dependency confusion, unsigned updates, unverified package sources)
    ├── YES → #10 Supply Chain Attack
    └── NO ↓

Q9: Is this a LOGIC, CONFIGURATION, or SCOPE weakness?
    (privilege escalation via design, API misuse, missing authorization, default credentials)
    ├── YES → #1 Abuse of Functions
    └── NO → Re-examine. One of the above must apply.
```

## The Role Disambiguation: #2 vs. #3

The largest context-dependent group (219 entries) maps to `#2 | #3`. These are code implementation flaws where the TLCTC cluster depends on the **role** of the vulnerable component:

```
Is the vulnerable code acting as a SERVER (receiving and processing requests)?
├── YES → #2 Exploiting Server
│         Examples: SQL injection in web app, buffer overflow in HTTP daemon
└── NO ↓

Is the vulnerable code acting as a CLIENT (requesting and rendering content)?
├── YES → #3 Exploiting Client
│         Examples: Browser rendering bug, PDF reader vulnerability
└── NO ↓

Could the same CWE appear in either role?
└── YES → #2 | #3 (context-dependent; classify at CVE/instance level)
```

### Common #2 | #3 Weakness Types

| CWE Pattern | Examples | Why Context-Dependent |
|-------------|----------|----------------------|
| Memory safety | CWE-787 Out-of-bounds Write, CWE-125 Out-of-bounds Read | Same flaw type in any compiled code |
| Injection | CWE-74 Injection, CWE-77 Command Injection | Server-side web app vs. client-side script engine |
| Type confusion | CWE-843 Type Confusion | Browser engine (client) vs. server runtime |
| Integer issues | CWE-190 Integer Overflow | Affects any compiled component |

## The Execution Chain: When to Append → #7

Per R-EXEC, if a weakness enables foreign code execution, the mapping must include a `→ #7` step:

| Weakness Type | Mapping | Rationale |
|---------------|---------|-----------|
| Buffer overflow (server) with RCE | `#2 → #7` | Code flaw enables unintended execution |
| XSS (reflected/stored) | `#2 → #7` | Server flaw delivers script to client for execution |
| XSS (DOM-based) | `#3` | Client-side flaw; script runs in client context |
| Deserialization (server) | `#2 → #7` | Server-side flaw enables arbitrary code execution |
| Code injection via API | `#1 → #7` | Designed function abused to execute foreign code |

## The Abstract CWE Problem

CWE includes many high-level entries that are too abstract to map to a single cluster:

| Verdict | Guidance | Examples |
|---------|----------|----------|
| **Discouraged** | Maps to multiple clusters depending on context | CWE-20 (Input Validation), CWE-693 (Protection Mechanism Failure) |
| **Prohibited** | Not a concrete weakness — organizational node | CWE-310 (Cryptographic Issues — Category), CWE-1000 (Research Concepts — View) |

For these entries, classify at the **child CWE** or **CVE level** instead.

## Quality Checklist

Before finalizing a CWE mapping, verify:

- [ ] **Concrete weakness** — Not a category, view, or deprecated entry
- [ ] **Specific enough** — Can determine a single generic vulnerability (or explicit alternatives)
- [ ] **Role considered** — If code flaw, is it server or client? If unclear, mark `#2 | #3`
- [ ] **R-EXEC respected** — If code execution is possible, `→ #7` is included
- [ ] **Cause, not consequence** — Mapping the exploitable flaw, not the resulting impact
- [ ] **Verdict assigned** — Confidence level reflects mapping certainty
