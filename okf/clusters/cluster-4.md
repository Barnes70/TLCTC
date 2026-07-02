---
type: "cluster"
title: "#4 Identity Theft"
description: "An attacker misuses authentication credentials to impersonate an identity."
resource: "tlctc:cluster:#4"
tags:
  - "taxonomy"
  - "cluster"
  - "internal"
strategic_id: "#4"
operational_root_id: "TLCTC-04.00"
generic_vulnerability: "Insufficient binding, at the point of authentication, between a presented credential and the authentic holder of the identity it claims."
topology: "internal"
---
# #4 Identity Theft

**Definition:** An attacker misuses authentication credentials to impersonate an identity.

**Scope:** Presentation/use of credentials, tokens, keys, session artifacts, or other identity representations to authenticate and act **as an identity different from the presenter’s own**. Credential storage and transmission are prevention controls that reduce acquisition; failures there classify to the enabling cluster (#2/#5/#7/#8), not to #4.

**Generic Vulnerability:** Insufficient binding, at the point of authentication, between a presented credential and the authentic holder of the identity it claims.

**Attacker’s View:** “I abuse stolen or forged credentials to act as someone else.”

**Developer’s View:** “I must verify at authentication time that the presenter is the credential’s authentic holder: enforce MFA, bind and validate sessions, detect credential replay/reuse and anomalous authentication, and apply least privilege with defense-in-depth.”

**Boundary Tests (normative):**

- Credential acquisition/exposure/derivation/forgery maps to the enabling cluster; credential use/presentation always maps to **#4** (**R-CRED**).
- If the step involves creating fraudulent credentials, certificates, or tokens, map **that creation/derivation** to the enabling mechanism (**#1/#2/#3/#7/#10** as appropriate), then map subsequent use to **#4**.
- If the step is primarily persuading a human to reveal/approve → **#9** for that manipulation step.

**Topology:** Internal.

**Analytical note (non-normative):** #4 can be analyzed as a **micro-bridge** across the AuthN→AuthZ decision boundary, while still remaining within a single organizational control regime.

---

# Schema

- **Strategic ID:** #4
- **Operational root:** TLCTC-04.00
- **Generic vulnerability:** Insufficient binding, at the point of authentication, between a presented credential and the authentic holder of the identity it claims.
- **Topology:** internal

# Relationships

- Governing axioms: [Axiom III](/axioms/axiom-iii.md), [Axiom VI](/axioms/axiom-vi.md), [Axiom VII](/axioms/axiom-vii.md)
- Classification rules: see [/rules/index.md](/rules/index.md)
- Control objectives: [/controls/cluster-4.md](/controls/cluster-4.md)
- Mapped techniques: [ATT&CK](/mappings/attack/cluster-4.md) · [CWE](/mappings/cwe/cluster-4.md) · [Sigma](/mappings/sigma/cluster-4.md)
