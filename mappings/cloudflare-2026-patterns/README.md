# TLCTC Cloudflare 2026 Threat Report — Attack Path Patterns

Canonical attack path patterns extracted from the **Cloudflare 2026 Threat Report** (Cloudforce One), decomposed into TLCTC threat cluster sequences.

## Source

Cloudflare, *2026 Cloudflare Threat Report: How adversaries are weaponizing the Internet*. Published March 2026 by Cloudforce One.

## Patterns

| ID | Pattern | TLCTC Sequence | Report Section |
|----|---------|---------------|----------------|
| CF26-PAT-001 | SaaS-to-SaaS Pivot | `#1 → #4 → #1` | MOE in SaaS Supply Chain (p. 7) |
| CF26-PAT-002 | Living off the XaaS (LotX) C2 | `#9 → #7 → #1` | MOE in Cloud Resources (pp. 10-11) |
| CF26-PAT-003 | Infostealer-to-Ransomware Pipeline | `#7 → #1 → #4 → #1 → (#1 + #7)` | Infostealer Engine / Ransomware 2.0 (pp. 39-41) |
| CF26-PAT-004 | PhaaS AitM Token Theft | `#9 → #5 → #4 → #1` | Industrialized PhaaS (pp. 35-36) |
| CF26-PAT-005 | Bot Chain Lifecycle | `#4 → #1 → #7 → #6` | Triple-Threat Bot Chain (pp. 42-45) |
| CF26-PAT-006 | Deepfake Identity Infiltration | `#9 → #4 → #1` | Industrialization of Insider Threats (pp. 12, 24-27) |
| CF26-PAT-007 | Edge Appliance Pre-Positioning | `#2 → #7 → #1` | China Nation-State Analysis (p. 22) |

## Structural Findings

1. **Identity over exploitation**: #4 Identity Theft appears in 6 of 7 patterns. The 2026 landscape is defined by "attacking the session" rather than "attacking the box."

2. **#1 dominance**: Abuse of Functions appears in every pattern, often multiple times with distinct control surfaces (API abuse, LotX C2, lateral movement, data exfiltration). Legitimate-function abuse is the connective tissue of modern attacks.

3. **MOE over sophistication**: The Measure of Effectiveness paradigm replaces technical complexity as the primary risk metric. High-MOE attacks achieve maximum disruption at minimum cost — often leveraging the victim's own infrastructure.

4. **Velocity compression**: AI-accelerated attack cycles compress exploitation phases to VC-3/VC-4 (minutes/seconds), closing the window for human intervention.

## Decision Tree

```
Is a human psychologically manipulated?
├── YES → #9 Social Engineering (bridge cluster, human boundary)
│   Is MFA bypassed via session interception?
│   ├── YES → #5 Man in the Middle → #4 (token replay)
│   └── NO → Does the victim reveal credentials?
│       ├── YES → [DRE: C] on #9, then #4 (credential use)
│       └── NO → Next step in chain
└── NO
    Are stolen/compromised credentials used to authenticate?
    ├── YES → #4 Identity Theft (R-CRED: always #4)
    └── NO
        Is a server-side vulnerability exploited?
        ├── YES → #2 Exploiting Server (R-ROLE: server role)
        └── NO
            Does foreign executable content run?
            ├── YES → #7 Malware (R-EXEC: fec_executed=true)
            └── NO
                Is network capacity overwhelmed by volume?
                ├── YES → #6 Flooding Attack
                └── NO → #1 Abuse of Functions
                    (legitimate functionality, abused scope)
```

## Files

- `tlctc-cloudflare-2026-patterns.json` — Pattern definitions with TLCTC notation, mapping rationale, controls, and velocity profiles

## Related Attack Paths

Full incident decompositions in `attack-paths/`:
- `grub1-saas-pivot-2025.json` (CF26-PAT-001)
- `frumpytoad-toughprogress-2025.json` (CF26-PAT-002)
- `nastyshrew-ukraine-2025.json` (CF26-PAT-002)
- `infostealer-ransomware-pipeline-2025.json` (CF26-PAT-003)
- `raccoon-phaas-aitm-2025.json` (CF26-PAT-004)
- `bot-chain-lifecycle-2025.json` (CF26-PAT-005)
- `aisuru-ddos-2025.json` (CF26-PAT-005)
- `nk-it-worker-infiltration-2025.json` (CF26-PAT-006)
- `punytoad-f5-bigip-2025.json` (CF26-PAT-007)
- `opencode-exploit-chain-2025.json`
- `rottenshrew-signal-2025.json`
- `clumsytoad-snakedisk-2025.json`
- `authorized-insider-extortion-2025.json`

## License

CC BY 4.0 — TLCTC Project
