---
type: "cluster"
title: "#7 Malware"
description: "An attacker abuses the inherent ability of a software environment to execute foreign executable content, including malicious code or legitimate tools executing attacker-controlled code."
resource: "tlctc:cluster:#7"
tags:
  - "taxonomy"
  - "cluster"
  - "internal"
strategic_id: "#7"
operational_root_id: "TLCTC-07.00"
generic_vulnerability: "The software environment's designed capability to execute potentially untrusted foreign code."
topology: "internal"
---
# #7 Malware

**Definition:** Execution of **Foreign Executable Content (FEC)** through the environment’s designed execution capabilities (binaries, scripts, macros, modules, or attacker-controlled commands fed into interpreters), including dual-use tooling when it executes attacker-controlled FEC.

**Generic Vulnerability:** The environment’s intended capability to execute potentially untrusted executable content.

**Attacker’s View:** “I abuse the environment’s designed capability to execute malware code, malicious scripts, or foreign-introduced tools for my purposes.”

**Developer’s View:** “I must control execution paths: allow-listing, code signing/verification, sandboxing, safe file handling, and avoiding uncontrolled dynamic execution.”

**Boundary Tests (normative):**

- If **FEC executes** → **#7** (per **R-EXEC**), even if execution is **in-memory** and no files are created.
- If legitimate function misuse enables FEC execution → **`#1 → #7`**.
- If exploit payload triggers an implementation flaw and results in FEC execution → **`#2/#3 → #7`**.
- If an implementation flaw is exploited but no FEC executes → **do not add #7**.

**Explicit SQLi clarification (non-normative but recommended):**

- SQL injection that reads/writes data **without** invoking a general-purpose execution engine → **#2** only (plus Data Risk Events).
- SQL injection that invokes OS/command execution via database features → **`#2 → #7`** (e.g., SQL Server `xp_cmdshell`, PostgreSQL `COPY … PROGRAM`, or equivalent OS-execution features).

**Topology:** Internal.

---

# Schema

- **Strategic ID:** #7
- **Operational root:** TLCTC-07.00
- **Generic vulnerability:** The software environment's designed capability to execute potentially untrusted foreign code.
- **Topology:** internal

# Relationships

- Governing axioms: [Axiom III](/axioms/axiom-iii.md), [Axiom VI](/axioms/axiom-vi.md), [Axiom VII](/axioms/axiom-vii.md)
- Classification rules: see [/rules/index.md](/rules/index.md)
- Control objectives: [/controls/cluster-7.md](/controls/cluster-7.md)
- Mapped techniques: [ATT&CK](/mappings/attack/cluster-7.md) · [CWE](/mappings/cwe/cluster-7.md) · [Sigma](/mappings/sigma/cluster-7.md)
