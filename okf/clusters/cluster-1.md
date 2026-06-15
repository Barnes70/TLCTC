---
type: "cluster"
title: "#1 Abuse of Functions"
description: "An attacker abuses the logic or scope of existing, legitimate software functions for malicious purposes without exploiting a code flaw."
resource: "tlctc:cluster:#1"
tags:
  - "taxonomy"
  - "cluster"
  - "internal"
strategic_id: "#1"
operational_root_id: "TLCTC-01.00"
generic_vulnerability: "The inherent trust, scope, and complexity designed into software functionality and configuration."
topology: "internal"
---
# #1 Abuse of Functions

**Definition:** Manipulation of legitimate software capabilities—features, APIs, configurations, administrative settings, workflows—through standard interfaces using built-in input types and valid sequences of actions (including configuration changes). The step achieves an attacker advantage **without requiring an implementation flaw**.

**Generic Vulnerability:** The inherent trust, scope, and complexity designed into software functionality and configuration.

**Attacker’s View:** “I abuse a functionality, not a coding issue.”

**Developer’s View:** “I must understand and constrain the functional domain of my code. Every feature and configuration surface needs explicit boundaries and misuse assumptions.”

**Boundary Tests (normative):**

- If an implementation flaw is required → **#2 or #3**.
- If this step enables execution of **FEC** → record **`#1`** for enablement and **`→ #7`** for execution (**`#1 → #7`**).
- If the step is primarily credential use/presentation → **#4**.

**Topology:** Internal.

---

# Schema

- **Strategic ID:** #1
- **Operational root:** TLCTC-01.00
- **Generic vulnerability:** The inherent trust, scope, and complexity designed into software functionality and configuration.
- **Topology:** internal

# Relationships

- Governing axioms: [Axiom III](/axioms/axiom-iii.md), [Axiom VI](/axioms/axiom-vi.md), [Axiom VII](/axioms/axiom-vii.md)
- Classification rules: see [/rules/index.md](/rules/index.md)
- Control objectives: [/controls/cluster-1.md](/controls/cluster-1.md)
- Mapped techniques: [ATT&CK](/mappings/attack/cluster-1.md) · [CWE](/mappings/cwe/cluster-1.md) · [Sigma](/mappings/sigma/cluster-1.md)
