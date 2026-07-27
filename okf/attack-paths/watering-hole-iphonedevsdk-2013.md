---
type: "attack-path"
title: "WATERING-HOLE-IPHONEDEVSDK-2013"
description: "Watering hole attack targeting Apple, Facebook, Twitter, and Microsoft employees, February 2013."
resource: "tlctc:attack-path:watering-hole-iphonedevsdk-2013"
tags:
  - "attack-path"
  - "cluster-2"
  - "cluster-3"
  - "cluster-7"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.3"
---
# WATERING-HOLE-IPHONEDEVSDK-2013

## Attack path

```
#2 →[Δt=~14d] #3 →[Δt=instant] #7 (FEC) →[Δt=~60d] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-forum-server-compromise | [#2](/clusters/cluster-2.md) |  | ~14d |  |
| s2-browser-java-exploit | [#3](/clusters/cluster-3.md) |  | instant |  |
| s3-rat-installation | [#7](/clusters/cluster-7.md) (FEC) |  | ~60d |  |
| s4-source-code-exfiltration | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-forum-server-compromise:** Attackers exploited a vulnerability in the iPhoneDevSDK.com web server (a popular iOS developer community forum) to inject malicious JavaScript/iframe that would serve a Java exploit to visitors. R-ROLE: the web server is server-role software — it receives requests and serves content to browsers = #2. The attacker exploited a server-side vulnerability to modify the content served to visitors. This is the 'watering hole' preparation step: compromising a site frequented by the target population.
- **s2-browser-java-exploit:** Visiting developers' browsers were exploited via Java zero-day (CVE-2013-0422) served from the compromised forum. The Java applet exploited a vulnerability in the Java Runtime Environment plugin running in the browser. R-ROLE: the browser and its Java plugin are client-side software that fetches and processes content from the server = #3. The browser-side Java vulnerability is distinct from the server-side compromise in s1. Axiom VI: server exploitation (#2) and client exploitation (#3) are separate generic vulnerabilities requiring separate steps.
- **s3-rat-installation:** Remote Access Trojan (RAT) installed on developer workstations via the Java exploit payload. The malware established persistence and C2 communication. R-EXEC: foreign executable content (RAT) executed on victim machines — recorded as #7 with fec_executed: true. The RAT is distinct foreign code delivered by the exploit chain.
- **s4-source-code-exfiltration:** Attackers used RAT access to developer machines to exfiltrate proprietary source code, internal documentation, and corporate data from Apple, Facebook, Twitter, and Microsoft. The RAT leveraged legitimate OS file access and network transfer functions. DRE: C — proprietary source code and internal corporate data compromised. The exfiltration used designed OS capabilities, classifying as #1 (abuse of functions).

# Citations

Watering hole attack targeting Apple, Facebook, Twitter, and Microsoft employees, February 2013. Attackers compromised the iPhoneDevSDK.com developer forum and injected a Java browser exploit (CVE-2013-0422). Developers from major tech companies visited the forum and had their browsers exploited, leading to RAT installation on corporate machines. Multiple tech companies confirmed employee compromises. Attack path: #2 →[Δt=~14d] #3 →[Δt=instant] #7 →[Δt=~60d] #1 + [DRE: C]. Sources: Facebook Security blog (February 2013), Apple and Twitter incident confirmations, iPhoneDevSDK.com compromise disclosure, Oracle CVE-2013-0422 advisory.
