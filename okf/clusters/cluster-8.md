---
type: "cluster"
title: "#8 Physical Attack"
description: "Unauthorized physical interaction with or interference to hardware, facilities, media, interfaces, or signals—via direct contact or exploitation of physical phenomena/emanations."
resource: "tlctc:cluster:#8"
tags:
  - "taxonomy"
  - "cluster"
  - "bridge"
strategic_id: "#8"
operational_root_id: "TLCTC-08.00"
generic_vulnerability: "Physical accessibility of infrastructure and the exploitability of physical-layer properties."
topology: "bridge"
---
# #8 Physical Attack

**Definition:** Unauthorized physical interaction with or interference to hardware, facilities, media, interfaces (including **removable media**), or signals—via direct contact or exploitation of physical phenomena/emanations.

**Generic Vulnerability:** Physical accessibility of infrastructure and the exploitability of physical-layer properties (interfaces, wireless spectrum, emanations, environmental dependencies).

**Attacker’s View:** “I abuse the physical accessibility or properties of hardware, devices, and signals.”

**Developer’s View:** “I must assume physical access can mean compromise: secure key storage, encryption at rest, tamper evidence, secure failure modes, and exposure-minimizing designs.”

**Boundary Tests (normative):**

- If the physical step leads to FEC execution → **`#8 → #7`**.

**Topology:** Bridge (Physical → Cyber).

---

# Schema

- **Strategic ID:** #8
- **Operational root:** TLCTC-08.00
- **Generic vulnerability:** Physical accessibility of infrastructure and the exploitability of physical-layer properties.
- **Topology:** bridge

# Relationships

- Governing axioms: [Axiom III](/axioms/axiom-iii.md), [Axiom VI](/axioms/axiom-vi.md), [Axiom VII](/axioms/axiom-vii.md)
- Classification rules: see [/rules/index.md](/rules/index.md)
- Control objectives: [/controls/cluster-8.md](/controls/cluster-8.md)
- Mapped techniques: [ATT&CK](/mappings/attack/cluster-8.md) · [CWE](/mappings/cwe/cluster-8.md) · [Sigma](/mappings/sigma/cluster-8.md)
