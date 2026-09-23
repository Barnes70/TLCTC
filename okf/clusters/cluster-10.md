---
type: "cluster"
title: "#10 Supply Chain Attack"
description: "An attacker compromises systems by subverting third-party software, hardware, services, or update mechanisms that the target trusts and integrates, so that the subverted artifact is accepted as authoritative inside the target's domain."
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

**Definition:** An attacker compromises systems by subverting third-party software, hardware, services, or update mechanisms that the target trusts and integrates, so that the subverted artifact is accepted as authoritative inside the target's domain.

**Scope:** Subversion of an organization’s **third-party trust link** such that the organization (or its systems) **accepts subverted third-party–originating artifacts or decisions as authoritative within the organization’s domain**, enabling unauthorized action or compromise. A flaw in a legitimately supplied component is not in scope; it is classified where it is exploited.

**Hook terms (normative):**

- **Third-Party Trust Link (TTL):** any reliance relationship where a third party can influence your domain (components, services, federation, managed control planes, update/signing/provenance, firmware channels).
- **Trust Artifact / Trust Decision (TAD):** what crosses the boundary and is accepted as authoritative (e.g., SAML/OIDC assertion, token, signed update/package, CI build artifact, policy/config push, admin action, firmware image).
- **Trust Acceptance Event (TAE):** the moment your domain **honors** the TTL and treats a TAD as authoritative (validate/accept/install/apply/execute/attach privileges).

**Generic Vulnerability:** Trust in third-party components and update channels can be subverted.

**Attacker’s View:** “I abuse the trust in third-party components.”

**Developer’s View:** “I must minimize and compartmentalize third-party trust, harden trust-acceptance points, verify provenance/attestations, and ensure trust is continuously re-validated and revocable.”

**Boundary Tests (normative):**

- Place #10 at the Trust Acceptance Event (TAE), where the third-party trust link is honored and becomes authoritative inside the organization.
- Subversion test: #10 requires that the trust artifact — package, update, build output, hardware, service response, federation assertion or metadata — or the third party issuing it was subverted by the attacker before the target accepted it. A defect in a legitimately supplied component is not #10: classify it where it is exploited, by R-ROLE or R-SPECIFIC (Log4Shell → #2). Where flawed code came from is location, not generic vulnerability.
- Falsifiability: remove the attacker's subversion of the third party — not the third party itself. If the step still succeeds, it was never #10.
- Downstream effects map normally: often `#10 → #7` (accepted artifact leads to FEC execution) or `#10 → #1` (accepted authorization/entitlement enables function abuse).
- Federation: presenting a credential or assertion to authenticate as another identity is #4, wherever it is presented and however it was obtained (R-CRED). A service provider honouring an assertion from an identity provider that was not subverted is the trust link working as designed and is not a step. Where the identity provider or its federation trust material was itself subverted, the service provider's acceptance of the subverted authority is the TAE (#10), and each impersonating assertion presented through it remains #4: `#10 → #4`.

**Optional boundary notation (recommended):**

- Subverted identity provider: **`#10 ||[auth][@Vendor(IdP)→@Org(SP)]|| → #4 → #1`** (credential use at an identity provider that was not subverted is `#4` alone)
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
