---
type: "cluster"
title: "#6 Flooding Attack"
description: "An attacker intentionally overwhelms system resources or exceeds capacity limits through a high volume of requests, data, or operations, leading to denial of service."
resource: "tlctc:cluster:#6"
tags:
  - "taxonomy"
  - "cluster"
  - "internal"
strategic_id: "#6"
operational_root_id: "TLCTC-06.00"
generic_vulnerability: "Finite capacity limitations inherent in any system component."
topology: "internal"
---
# #6 Flooding Attack

**Definition:** Exhaustion of finite system resources (bandwidth, CPU, memory, storage, quotas, pools) through volume or intensity that exceeds capacity limits, causing disruption/degradation/denial of service.

**Generic Vulnerability:** Finite capacity limitations inherent in any system component.

**Attacker’s View:** “I abuse the circumstance of always limited capacity in software and systems.”

**Developer’s View:** “I must implement efficient resource management: limits, timeouts, quotas, circuit breakers, and scalable designs—every loop and allocation must consider abuse.”

**Boundary Tests (normative):**

- If availability loss is primarily caused by an implementation defect (crash, algorithmic complexity weakness such as **ReDoS**) → **#2/#3**.
- If availability loss is primarily capacity exhaustion by volume/intensity → **#6** (**R-FLOOD**).
- If attackers amplify load by abusing legitimate functions, the enabling step may be **#1**, but the exhaustion event remains **#6**.

**Topology:** Internal.

---

# Schema

- **Strategic ID:** #6
- **Operational root:** TLCTC-06.00
- **Generic vulnerability:** Finite capacity limitations inherent in any system component.
- **Topology:** internal

# Relationships

- Governing axioms: [Axiom III](/axioms/axiom-iii.md), [Axiom VI](/axioms/axiom-vi.md), [Axiom VII](/axioms/axiom-vii.md)
- Classification rules: see [/rules/index.md](/rules/index.md)
- Control objectives: [/controls/cluster-6.md](/controls/cluster-6.md)
- Mapped techniques: [ATT&CK](/mappings/attack/cluster-6.md) · [CWE](/mappings/cwe/cluster-6.md) · [Sigma](/mappings/sigma/cluster-6.md)
