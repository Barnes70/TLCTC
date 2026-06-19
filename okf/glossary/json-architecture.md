---
type: "term"
title: "JSON Architecture"
description: "The standardized data structure for threat intelligence sharing in TLCTC V2.0, consisting of four complementary JSON files: 1."
resource: "tlctc:term:json-architecture"
tags:
  - "glossary"
---
# JSON Architecture

The standardized data structure for threat intelligence sharing in TLCTC V2.0, consisting of four complementary JSON files:

1. **tlctc-framework.json:** Core framework definitions (universal, rarely updated)
2. **tlctc-responsibility-spheres.json:** Domain boundary definitions (customizable, occasionally updated)
3. **tlctc-attack-sequence-schema.json:** Validation schema for attack instances (universal, rarely updated)
4. **[incident]-attack-path.json:** Specific attack instances (per-incident, constantly updated)

This architecture separates universal framework definitions from specific attack instances, enabling machine-readable, validated, consistent threat intelligence exchange worldwide.

---
