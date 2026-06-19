---
type: "mapping-set"
title: "CWE weaknesses → #6 Flooding Attack"
description: "27 CWE weaknesses entries mapped to TLCTC #6 Flooding Attack."
resource: "tlctc:mapping:cwe:cluster-6"
tags:
  - "mapping"
  - "cwe"
  - "cluster-6"
---
# CWE weaknesses → #6 Flooding Attack

> Source: MITRE CWE → TLCTC mapping (`mappings/mitre-cwe/`). AI-generated, human-reviewed; experimental.

Mapped entries: **27**. Cluster: [#6 Flooding Attack](/clusters/cluster-6.md).

| CWE | Name | TLCTC | Verdict | Rationale |
|---|---|---|---|---|
| CWE-400 | Uncontrolled Resource Consumption | #6 | Discouraged | Parent class for uncontrolled-resource-consumption flaws. Specific cases classify at child CWEs (CWE-770, 774, 789). Resource exhaustion / denial of service — finite capacity weakness. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-401 | Missing Release of Memory after Effective Lifetime | #6 | Allowed | Resource exhaustion / denial of service — memory not released after effective lifetime — leak grows over time until OOM. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-404 | Improper Resource Shutdown or Release | #6 | Allowed | Resource exhaustion / denial of service — resource not properly shut down or released, accumulating until exhaustion. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-405 | Asymmetric Resource Consumption (Amplification) | #6 | Allowed | Resource exhaustion / denial of service — asymmetric resource consumption (small request triggers large work / large allocation) — amplification primitive. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-406 | Insufficient Control of Network Message Volume (Network Amplification) | #6 | Allowed | Resource exhaustion / denial of service — missing rate-limit on incoming network message volume — network-flooding amplifier. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-408 | Incorrect Behavior Order: Early Amplification | #6 | Allowed | Resource exhaustion / denial of service — early amplification — server allocates resources before authenticating, magnifying flooding impact. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-409 | Improper Handling of Highly Compressed Data (Data Amplification) | #6 | Allowed | Resource exhaustion / denial of service — zip-bomb / decompression-bomb — small compressed input expands to GBs. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-410 | Insufficient Resource Pool | #6 | Allowed | Resource exhaustion / denial of service — insufficient resource pool (thread pool, connection pool too small for load). Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-412 | Unrestricted Externally Accessible Lock | #6 | Allowed | Resource exhaustion / denial of service — externally-accessible lock that any caller can acquire and hold, blocking the protected resource. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-770 | Allocation of Resources Without Limits or Throttling | #6 | Allowed | Resource exhaustion / denial of service — allocation of resources without limit/throttle — attacker drives unbounded resource creation. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-771 | Missing Reference to Active Allocated Resource | #6 | Allowed | Resource exhaustion / denial of service — missing reference to active allocated resource — orphaned resource cannot be released. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-772 | Missing Release of Resource after Effective Lifetime | #6 | Allowed | Resource exhaustion / denial of service — missing release of resource after effective lifetime — resource leak accumulates over time. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-773 | Missing Reference to Active File Descriptor or Handle | #6 | Allowed | Resource exhaustion / denial of service — missing reference to active file descriptor / handle — handles leak. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-774 | Allocation of File Descriptors or Handles Without Limits or Throttling | #6 | Allowed | Resource exhaustion / denial of service — allocation of file descriptors / handles without limit. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-775 | Missing Release of File Descriptor or Handle after Effective Lifetime | #6 | Allowed | Resource exhaustion / denial of service — missing release of file descriptor / handle after effective lifetime. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-776 | Improper Restriction of Recursive Entity References in DTDs ('XML Entity Expansion') | #6 | Allowed | Resource exhaustion / denial of service — recursive entity references in DTD (Billion Laughs / XML bomb) explode parser memory. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-779 | Logging of Excessive Data | #6 | Allowed | Resource exhaustion / denial of service — logging of excessive data fills disk / log-aggregation pipeline. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-789 | Memory Allocation with Excessive Size Value | #6 | Allowed | Resource exhaustion / denial of service — memory allocation with attacker-supplied excessive size value. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-834 | Excessive Iteration | #6 | Discouraged | Parent class for excessive-iteration / infinite-loop flaws. Specific cases at child CWEs (CWE-674 uncontrolled recursion, CWE-835 infinite loop). Resource exhaustion / denial of service — unbounded iteration. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-920 | Improper Restriction of Power Consumption | #6 | Allowed | Resource exhaustion / denial of service — missing power-consumption restriction — battery drain on mobile/IoT devices. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-1049 | Excessive Data Query Operations in a Large Data Table | #6 | Allowed | Performance issue that can be abused for Resource Exhaustion (#6). |
| CWE-1050 | Excessive Platform Resource Consumption within a Loop | #6 | Allowed | Resource exhaustion / denial of service — excessive platform-resource consumption inside a loop — amplifies cost per iteration. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-1067 | Excessive Execution of Sequential Searches of Data Resource | #6 | Allowed | Algorithmic complexity/Performance issue leading to DoS (LoA). |
| CWE-1089 | Large Data Table with Excessive Number of Indices | #6 | Allowed | Performance issue leading to potential Resource Exhaustion (#6). |
| CWE-1176 | Inefficient CPU Computation | #6 | Allowed | Resource exhaustion / denial of service — inefficient CPU computation — algorithmic complexity not appropriate for input size. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-1235 | Incorrect Use of Autoboxing and Unboxing for Performance Critical Operations | #6 | Allowed | Resource exhaustion / denial of service — unintended autoboxing/unboxing in hot loops — performance collapse exploitable for DoS. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
| CWE-1325 | Improperly Controlled Sequential Memory Allocation | #6 | Allowed | Resource exhaustion / denial of service — improperly-controlled sequential memory allocation — allocation count grows unboundedly with input. Decision tree Q5 (resource exhaustion / capacity weakness) -> #6. |
