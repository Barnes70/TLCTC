---
type: "term"
title: "Supply Chain Attack (#10)"
description: "A top level threat cluster on the cause side of the bow tie, where an attacker compromises systems by subverting third party software, hardware, services, or update mechanisms that the target trusts and integrates, so that the subverted artifact is accepted as authoritative inside the target's domain."
resource: "tlctc:term:supply-chain-attack-10"
tags:
  - "glossary"
---
# Supply Chain Attack (#10)

A top-level threat cluster on the cause side of the bow-tie, where an attacker compromises systems by subverting third-party software, hardware, services, or update mechanisms that the target trusts and integrates, so that the subverted artifact is accepted as authoritative inside the target's domain. The generic vulnerability is that trust in third-party components and update channels can be subverted. A defect in a legitimately supplied component is **not** `#10`: it is classified where it is exploited, by R-ROLE or R-SPECIFIC (Log4Shell is `#2`), because where flawed code came from is location, not generic vulnerability. Falsifier: remove the attacker's subversion of the third party, not the third party itself; if the step still succeeds, it was never `#10`.

**Supply Chain as "Bridge Not Bucket":** #10 is a *bridge* threat cluster that marks the use of a trusted supply-chain channel as an attack vector to cross from one domain/trust boundary into another (e.g. @Vendor → @Org). It does *not* absorb the semantics of other clusters (#1–#9).

**Three Key Supply-Chain Vectors (#10.x):**

- **#10.1 Update Vector:** Post-deployment delivery/update flow compromise
- **#10.2 Development Vector:** Pre-deployment build/dev pipeline, repositories, or package ecosystem compromise
- **#10.3 Hardware Supply Chain Vector:** Hardware component, firmware, or manufacturing/assembly compromise

**Control-Level Third-Party Dependencies (Not #10):** Dependencies on third parties for patch delivery, security updates, or managed services are treated as *governance/control dependencies* on the right side of the bow-tie. They are **not themselves** a #10 Supply Chain Attack unless the trusted integration channel is directly abused as an attack vector.

**Related reading:** [Topology of cyber attacks — Bridge vs Internal](https://www.tlctc.net/tlctc-topology-of-cyber-attacks.html), [20 annotated attack paths (Ransomware, BEC, OT, ...)](https://www.tlctc.net/tlctc-attack-path-examples.html), [blog-attack-path-supply-chain.html](https://www.tlctc.net/blog-attack-path-supply-chain.html), [tlctc-npm-supply-chain.html](https://www.tlctc.net/tlctc-npm-supply-chain.html)
