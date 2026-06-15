---
type: "cluster"
title: "#9 Social Engineering"
description: "An attacker psychologically manipulates individuals into performing actions counter to their best interests."
resource: "tlctc:cluster:#9"
tags:
  - "taxonomy"
  - "cluster"
  - "bridge"
strategic_id: "#9"
operational_root_id: "TLCTC-09.00"
generic_vulnerability: "Humans can be influenced into unsafe actions or decisions."
topology: "bridge"
---
# #9 Social Engineering

**Definition:** Psychological manipulation that causes a human to perform an action counter to security interests—disclosing information, granting access, executing content, modifying configuration, or bypassing procedures.

**Generic Vulnerability:** Human psychological factors (trust, fear, urgency, authority bias, curiosity, ignorance, fatigue, etc.).

**Attacker’s View:** “I abuse human trust and psychology to deceive individuals.”

**Developer’s View:** “I must design interfaces and processes that promote secure behavior: clear indicators, safe defaults, and friction for high-risk actions.”

**Boundary Tests (normative):**

- Technical vulnerabilities (CVEs) are never **#9**.
- **#9** is only the human manipulation step; subsequent technical steps map to their own clusters.
- Typical sequences: **`#9 → #4`**, **`#9 → #7`**, **`#9 → #1`**.

**Topology:** Bridge (Human → Cyber).

---

# Schema

- **Strategic ID:** #9
- **Operational root:** TLCTC-09.00
- **Generic vulnerability:** Humans can be influenced into unsafe actions or decisions.
- **Topology:** bridge

# Relationships

- Governing axioms: [Axiom III](/axioms/axiom-iii.md), [Axiom VI](/axioms/axiom-vi.md), [Axiom VII](/axioms/axiom-vii.md)
- Classification rules: see [/rules/index.md](/rules/index.md)
- Control objectives: [/controls/cluster-9.md](/controls/cluster-9.md)
- Mapped techniques: [ATT&CK](/mappings/attack/cluster-9.md) · [CWE](/mappings/cwe/cluster-9.md) · [Sigma](/mappings/sigma/cluster-9.md)
