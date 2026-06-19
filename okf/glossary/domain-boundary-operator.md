---
type: "term"
title: "Domain Boundary Operator (||)"
description: "Notation: ||[context][@Source→@Target]|| ."
resource: "tlctc:term:domain-boundary-operator"
tags:
  - "glossary"
---
# Domain Boundary Operator (||)

Notation: `||[context][@Source→@Target]||`. Used to explicitly mark where an attack path crosses responsibility spheres. The operator SHOULD accompany bridge cluster steps (`#8`, `#9`, `#10`) and MAY be used with any step that crosses a domain boundary. The context describes the transition type (e.g., [dev], [idp], [update]) and the arrow shows the direction of trust crossing. The boundary test: "If removing the third-party trust link would stop the step from succeeding, #10 belongs there". Enables precise mapping of responsibility shifts and supply chain attack analysis.

**Reference:** §4.2.2 (Global Definitions), §11.3 (Domain Boundary Operator), §5.3

**Related reading:** [MITRE ATT&CK & STIX × TLCTC V2.0 — implementation guide](https://www.tlctc.net/stix-tlctc.html), [IEC 62443 × TLCTC v2.0 — industrial cybersecurity](https://www.tlctc.net/tlctc-iec62443-v2.html), [FAIR × TLCTC — enhanced quantitative risk](https://www.tlctc.net/tlctc-fair.html), [ISO/SAE 21434 × TLCTC V2.0 — automotive](https://www.tlctc.net/tlctc-blog-IsoSae21434.html), [Enhancing CVE records with TLCTC v2.1](https://www.tlctc.net/tlctc-cve-nvd.html), [EU cyber regulation needs a common taxonomy](https://www.tlctc.net/blog-eu-regulation-tlctc-taxonomy.html), [DORA TLPT × TLCTC V2.1 — boundary & velocity](https://www.tlctc.net/tlctc-regulation-dora-tlpt.html), [TLCTC classification decision tree V2.0/V2.1](https://www.tlctc.net/tlctc-decision-tree.html), [Topology of cyber attacks — Bridge vs Internal](https://www.tlctc.net/tlctc-topology-of-cyber-attacks.html), [TLCTC+ for NCSCs & CERTs — national reporting](https://www.tlctc.net/tlctc-plus-ncsc-proposal.html)
