---
type: "attack-path"
title: "PUNYTOAD-F5-BIGIP-2025"
description: "PunyToad (UNC5221/UTA0178/Warp Panda) F5 BIG-IP breach, confirmed October 2025 by Cloudforce One."
resource: "tlctc:attack-path:punytoad-f5-bigip-2025"
tags:
  - "attack-path"
  - "cluster-2"
  - "cluster-7"
  - "cluster-1"
  - "confidence-high"
timestamp: "2026-04-09T00:00:00Z"
tlctc_version: "2.1"
---
# PUNYTOAD-F5-BIGIP-2025

## Attack path

```
#2 →[Δt=~1h] #7 (FEC) →[Δt=~1d] #1 + [DRE: C]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-edge-appliance-exploit | [#2](/clusters/cluster-2.md) |  | ~1h |  |
| s2-brickstorm-deployment | [#7](/clusters/cluster-7.md) (FEC) |  | ~1d |  |
| s3-persistent-access-exfil | [#1](/clusters/cluster-1.md) |  |  | C |

## Step notes

- **s1-edge-appliance-exploit:** PunyToad exploits vulnerabilities in F5 BIG-IP edge network appliances to gain initial access. R-ROLE: the F5 BIG-IP is in a server role relative to the attacker — it accepts and processes attacker-supplied input. This is #2 Exploiting Server: a technical vulnerability in a server-side component. PunyToad specializes in edge network appliance exploitation (F5 BIG-IP, VMware vCenter, VMware ESXi). Edge appliances are high-value targets because they sit at trust boundaries and process traffic from multiple zones.
- **s2-brickstorm-deployment:** BRICKSTORM malware deployed — a Go-based ELF binary obfuscated with Garble. R-EXEC: foreign executable content executes on the F5 system — recorded as #7 with fec_executed: true. Stealth measures: the binary masquerades as legitimate VMware/Postgres processes (pg-update, rpclistener) installed in /opt/vmware/vpostgres/. Critical architectural inversion: BRICKSTORM acts as a web server on the compromised host; the C2 infrastructure connects to it as a client via WebSockets (wss://). This reverse logic complicates egress-based detection since the compromised host never initiates outbound connections to suspicious domains.
- **s3-persistent-access-exfil:** PunyToad maintained persistent access for over a year, using DNS over HTTP (DoH) for C2 domain resolution and proxy tunneling to bypass traditional firewall rules. All data exfiltration leverages legitimate network protocols and system capabilities. This is #1 Abuse of Functions: DoH, WebSocket connections, and file read operations all function as designed. DRE: C — exfiltration of F5 BIG-IP source code and documentation on undisclosed vulnerabilities. The source code theft represents a strategic intelligence win: knowledge of undisclosed vulnerabilities in widely-deployed edge infrastructure enables future exploitation campaigns across PunyToad's global target set.

# Citations

PunyToad (UNC5221/UTA0178/Warp Panda) F5 BIG-IP breach, confirmed October 2025 by Cloudforce One. PunyToad maintained persistent access to F5 systems for over a year, exfiltrating BIG-IP source code and documentation on undisclosed vulnerabilities. Malware: BRICKSTORM, a Go-based ELF binary obfuscated with Garble. Reverse C2 logic: the malware acts as a web server; the C2 connects to it as a client via WebSockets (wss://). Stealth: masquerades as legitimate VMware/Postgres processes (pg-update, rpclistener) in /opt/vmware/vpostgres/. Infrastructure: DNS over HTTP (DoH) to resolve C2 domains, proxy tunneling to bypass firewall rules. Attack path: #2 -> #7 -> #1 + [DRE: C]. Sources: Cloudflare 2026 Threat Report (pp. 22), F5 advisory K000154696, Google Cloud blog.
