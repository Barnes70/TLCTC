---
type: "term"
title: "Transit Boundary Operator (⇒)"
description: "Notation: ||[context][@Source⇒@Carrier→@Target]|| ."
resource: "tlctc:term:transit-boundary-operator"
tags:
  - "glossary"
---
# Transit Boundary Operator (⇒)

Notation: `||[context][@Source⇒@Carrier→@Target]||`. An extension to the Domain Boundary Operator that marks responsibility spheres which **carry or relay** the attack without being the source or the target. The `⇒` symbol denotes transit (relay), while `→` denotes delivery to the final target. Chained transit uses right-to-left relay order: `||[context][@Source⇒@CarrierB⇒@CarrierA→@Target]||`. Transit is distinct from `#10 Supply Chain Attack`: transit marks a passive relay, while `#10` marks a Trust Acceptance Event. Key rule (R-TRANSIT-3): vendor code running on the target device is NOT transit — it is the attack surface (classify by R-ROLE). Example: `#9 ||[human][@Attacker⇒@SMSProvider→@Victim]||` — phishing SMS relayed through carrier.

**Reference:** §11.3.5 (Transit Boundary Operator)
