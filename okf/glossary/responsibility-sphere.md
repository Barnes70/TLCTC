---
type: "term"
title: "Responsibility Sphere"
description: "The organizational owner of a domain, denoted as @Entity ."
resource: "tlctc:term:responsibility-sphere"
tags:
  - "glossary"
---
# Responsibility Sphere

The organizational owner of a domain, denoted as `@Entity`. Examples: `@Org`, `@Vendor`, `@Facilities`, `@HR`, `@CloudProvider`, `@MSP`. Different spheres have different policies, teams, governance structures, and potentially different legal boundaries. Domain boundary definitions identify where responsibility and control shift during an attack, which is critical for incident response, forensics, and legal responsibility. Defined in `tlctc-responsibility-spheres.json` and customizable per organization. Standard spheres include: Attacker Side, Third-Party/Vendor Side, Victim Side, Shared/Transit. Used in conjunction with the domain boundary operator (||) in attack path notation.

**Reference:** §4.2.2 (Global Definitions), §11.4, §5.1.2
