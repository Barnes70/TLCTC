---
type: "cluster"
title: "#5 Man in the Middle"
description: "An attacker intercepts, modifies, or relays communication between two parties by exploiting a privileged position on the communication path."
resource: "tlctc:cluster:#5"
tags:
  - "taxonomy"
  - "cluster"
  - "internal"
strategic_id: "#5"
operational_root_id: "TLCTC-05.00"
generic_vulnerability: "The lack of sufficient control, integrity protection, or confidentiality over the communication channel/path."
topology: "internal"
---
# #5 Man in the Middle

**Definition:** An attacker intercepts, modifies, or relays communication between two parties by exploiting a privileged position on the communication path.

**Scope:** Exploitation of a controlled position on a communication path—on the local network or via control over an intermediary—through interception, observation, modification, injection, replay, or protocol downgrade/stripping.

**Generic Vulnerability:** The lack of sufficient control, integrity protection, or confidentiality over the communication channel/path.

**Attacker’s View:** “I abuse my position between communicating parties.”

**Developer’s View:** “I must ensure confidentiality and integrity of data in transit: strong E2E protection, proper certificate/path validation, and designs that assume uncontrolled networks are hostile.”

**Boundary Tests (normative):**

- Gaining the privileged position maps to another cluster; **#5 begins once the position is controlled** (**R-MITM**).
- If the primary act is credential use after capture → **#4** for the use step.

**Examples (position acquisition, non-normative):**

- Via **#1**: abusing network/protocol functions to obtain a path advantage (local redirection patterns).
- Via **#8**: physical tap on cable or device access enabling interception.
- Via **#9**: tricking a user/admin into granting network access or installing a trust anchor.

**Topology:** Internal (within the communication/protocol domain).

---

# Schema

- **Strategic ID:** #5
- **Operational root:** TLCTC-05.00
- **Generic vulnerability:** The lack of sufficient control, integrity protection, or confidentiality over the communication channel/path.
- **Topology:** internal

# Relationships

- Governing axioms: [Axiom III](/axioms/axiom-iii.md), [Axiom VI](/axioms/axiom-vi.md), [Axiom VII](/axioms/axiom-vii.md)
- Classification rules: see [/rules/index.md](/rules/index.md)
- Control objectives: [/controls/cluster-5.md](/controls/cluster-5.md)
- Mapped techniques: [ATT&CK](/mappings/attack/cluster-5.md) · [CWE](/mappings/cwe/cluster-5.md) · [Sigma](/mappings/sigma/cluster-5.md)
