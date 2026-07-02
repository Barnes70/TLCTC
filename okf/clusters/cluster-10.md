---
type: "cluster"
title: "#10 Supply Chain Attack"
description: "An attacker compromises systems by targeting vulnerabilities within third-party software, hardware, services, or update mechanisms that are trusted and integrated by the target."
resource: "tlctc:cluster:#10"
tags:
  - "taxonomy"
  - "cluster"
  - "bridge"
strategic_id: "#10"
operational_root_id: "TLCTC-10.00"
generic_vulnerability: "Trust in third-party components and update channels can be subverted."
topology: "bridge"
---
# #10 Supply Chain Attack

**Definition:** An attacker compromises systems by targeting vulnerabilities within third-party software, hardware, services, or update mechanisms that are trusted and integrated by the target.

**Scope:** Exploitation of an organization’s **third-party trust link** such that the organization (or its systems) **accepts third-party–originating artifacts or decisions as authoritative within the organization’s domain**, enabling unauthorized action or compromise.

**Hook terms (normative):**

- **Third-Party Trust Link (TTL):** any reliance relationship where a third party can influence your domain (components, services, federation, managed control planes, update/signing/provenance, firmware channels).
- **Trust Artifact / Trust Decision (TAD):** what crosses the boundary and is accepted as authoritative (e.g., SAML/OIDC assertion, token, signed update/package, CI build artifact, policy/config push, admin action, firmware image).
- **Trust Acceptance Event (TAE):** the moment your domain **honors** the TTL and treats a TAD as authoritative (validate/accept/install/apply/execute/attach privileges).

**Generic Vulnerability:** Trust in third-party components and update channels can be subverted.

**Attacker’s View:** “I abuse the trust in third-party components.”

**Developer’s View:** “I must minimize and compartmentalize third-party trust, harden trust-acceptance points, verify provenance/attestations, and ensure trust is continuously re-validated and revocable.”

**Boundary Tests (normative):**

- Place **#10 at the Trust Acceptance Event (TAE)** where the third-party trust link is **honored** and becomes authoritative inside the org.
- **Falsifiability:** If removing the third-party trust link stops this step from succeeding → **#10 belongs here**.
- Downstream effects map normally: often **`#10 → #7`** (accepted artifact leads to FEC execution) or **`#10 → #1`** (accepted auth/entitlement enables function abuse).
- Federation clarity: credential use at IdP is **#4**; acceptance of the IdP assertion/token at the SP is **#10**.

**Optional boundary notation (recommended):**

- Runtime federation: **`#4 → #10 ||[auth][@Vendor(IdP)→@Org(SP)]|| → #1`**
- Update channel delivery: **`#10 ||[dev][@Vendor→@Org]|| → #7`**

**Topology:** Bridge (Third-party → Organization).

---

# Schema

- **Strategic ID:** #10
- **Operational root:** TLCTC-10.00
- **Generic vulnerability:** Trust in third-party components and update channels can be subverted.
- **Topology:** bridge

# Relationships

- Governing axioms: [Axiom III](/axioms/axiom-iii.md), [Axiom VI](/axioms/axiom-vi.md), [Axiom VII](/axioms/axiom-vii.md)
- Classification rules: see [/rules/index.md](/rules/index.md)
- Control objectives: [/controls/cluster-10.md](/controls/cluster-10.md)
- Mapped techniques: [ATT&CK](/mappings/attack/cluster-10.md) · [CWE](/mappings/cwe/cluster-10.md) · [Sigma](/mappings/sigma/cluster-10.md)
