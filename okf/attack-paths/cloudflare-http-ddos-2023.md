---
type: "attack-path"
title: "CLOUDFLARE-HTTP2-DDOS-2023"
description: "Record-breaking HTTP/2 Rapid Reset DDoS attack, October 2023."
resource: "tlctc:attack-path:cloudflare-http-ddos-2023"
tags:
  - "attack-path"
  - "cluster-6"
  - "confidence-high"
timestamp: "2026-03-20T00:00:00Z"
tlctc_version: "2.1"
---
# CLOUDFLARE-HTTP2-DDOS-2023

## Attack path

```
#6 + [DRE: A]
```

# Schema

| Step | Cluster | Boundary | Δt→next | DRE |
|---|---|---|---|---|
| s1-http2-rapid-reset-flood | [#6](/clusters/cluster-6.md) |  |  | A |

## Step notes

- **s1-http2-rapid-reset-flood:** Massive Layer 7 DDoS attack using the HTTP/2 Rapid Reset technique (CVE-2023-44487). A botnet of approximately 20,000 compromised machines sent streams of HTTP/2 requests immediately followed by RST_STREAM frames. This exploited the asymmetric cost between client (sending a small RST_STREAM frame is nearly free) and server (allocating resources for each new stream before processing the reset is expensive). Peak rate: 398 million requests per second — the largest DDoS attack recorded at the time. #6 Flooding Attack: the generic vulnerability is the target's finite resource capacity. The attack overwhelms server resources through sheer volume of protocol-compliant but malicious requests. The HTTP/2 protocol-level amplification is a technique within the flooding category — it makes the flood more efficient but doesn't change the fundamental classification. DRE: A — service availability degraded or disrupted. CVE-2023-44487 was subsequently patched in HTTP/2 implementations across Nginx, Apache, and other servers to limit rapid stream resets. Axiom III: the cause is resource exhaustion via flooding = #6; the outcome (service disruption) is the DRE, not the classification.

# Citations

Record-breaking HTTP/2 Rapid Reset DDoS attack, October 2023. Exploiting CVE-2023-44487, attackers generated up to 398 million requests per second against Cloudflare infrastructure (similar attacks hit Google at 398M rps and AWS). The attack used HTTP/2 Rapid Reset: rapidly opening and canceling HTTP/2 streams to overwhelm servers while maintaining a single TCP connection. Botnet of ~20,000 machines achieved amplification through protocol-level asymmetry. Attack path: #6 + [DRE: A]. Sources: Cloudflare blog 'HTTP/2 Rapid Reset' (October 2023), Google Cloud blog on CVE-2023-44487, AWS Shield response, CISA advisory on HTTP/2 Rapid Reset.
