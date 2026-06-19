---
type: "mapping-set"
title: "CWE weaknesses → #7 Malware"
description: "4 CWE weaknesses entries mapped to TLCTC #7 Malware."
resource: "tlctc:mapping:cwe:cluster-7"
tags:
  - "mapping"
  - "cwe"
  - "cluster-7"
---
# CWE weaknesses → #7 Malware

> Source: MITRE CWE → TLCTC mapping (`mappings/mitre-cwe/`). AI-generated, human-reviewed; experimental.

Mapped entries: **4**. Cluster: [#7 Malware](/clusters/cluster-7.md).

| CWE | Name | TLCTC | Verdict | Rationale |
|---|---|---|---|---|
| CWE-507 | Trojan Horse | #7 | Allowed | Malicious code present in the product — trojan horse — code that masquerades as legitimate functionality. Decision tree Q6 -> #7. (Per Axiom III, presence of malware is itself the threat action; the supply-chain-insertion event is captured by #10 in the chain.) |
| CWE-508 | Non-Replicating Malicious Code | #7 | Allowed | Malicious code present in the product — non-replicating malicious code. Decision tree Q6 -> #7. (Per Axiom III, presence of malware is itself the threat action; the supply-chain-insertion event is captured by #10 in the chain.) |
| CWE-509 | Replicating Malicious Code (Virus or Worm) | #7 | Allowed | Malicious code present in the product — replicating malicious code (virus or worm) — adds R-EXEC propagation step but the cluster classification is the malware presence itself. Decision tree Q6 -> #7. (Per Axiom III, presence of malware is itself the threat action; the supply-chain-insertion event is captured by #10 in the chain.) |
| CWE-512 | Spyware | #7 | Allowed | Malicious code present in the product — spyware — covert observation/exfiltration code. Decision tree Q6 -> #7. (Per Axiom III, presence of malware is itself the threat action; the supply-chain-insertion event is captured by #10 in the chain.) |
