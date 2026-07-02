---
type: "cluster"
title: "#3 Exploiting Client"
description: "An attacker targets flaws within the source code implementation of any software acting in a client role."
resource: "tlctc:cluster:#3"
tags:
  - "taxonomy"
  - "cluster"
  - "internal"
strategic_id: "#3"
operational_root_id: "TLCTC-03.00"
generic_vulnerability: "Client-side implementation flaws enable unintended behavior."
topology: "internal"
---
# #3 Exploiting Client

**Definition:** An attacker targets flaws within the source code implementation of any software acting in a client role.

**Scope:** Triggering an **implementation flaw** in **client-role** software through crafted content/responses/state (“exploit payload”), exploiting coding mistakes in parsing, rendering, state management, or response handling.

**Role criterion:** The vulnerable component **consumes external responses, content, or state**.

**Generic Vulnerability:** Client-side implementation flaws enable unintended behavior.

**Attacker’s View:** “I abuse a flaw in the source code of software acting as a client.”

**Developer’s View:** “I must apply secure coding principles for client-role code and never trust incoming data from servers, files, URLs, or APIs.”

**Boundary Tests (normative):**

- If behavior is achieved without an implementation flaw (pure feature misuse) → **#1**.
- If the vulnerable component is in a server role → **#2**.
- If exploitation results in **FEC execution** → append **`→ #7`** (i.e., **`#3 → #7`**) per **R-EXEC**.
- If exploitation yields security impact **without** FEC execution → **#3** only; document outcomes as **Data Risk Events**.

**Topology:** Internal.

---

# Schema

- **Strategic ID:** #3
- **Operational root:** TLCTC-03.00
- **Generic vulnerability:** Client-side implementation flaws enable unintended behavior.
- **Topology:** internal

# Relationships

- Governing axioms: [Axiom III](/axioms/axiom-iii.md), [Axiom VI](/axioms/axiom-vi.md), [Axiom VII](/axioms/axiom-vii.md)
- Classification rules: see [/rules/index.md](/rules/index.md)
- Control objectives: [/controls/cluster-3.md](/controls/cluster-3.md)
- Mapped techniques: [ATT&CK](/mappings/attack/cluster-3.md) · [CWE](/mappings/cwe/cluster-3.md) · [Sigma](/mappings/sigma/cluster-3.md)
