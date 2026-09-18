# Attack Flow corpus study results

Generated 2026-09-18T19:17:03Z from center-for-threat-informed-defense/attack-flow commit `0bd4a2d45dceacce499d7e94b85f7966e70f5399` (41 flows), ATT&CK→TLCTC mapping with 909 techniques.

### All corpus flows

| Corpus profile | value |
|---|---|
| flows | 41 (100.0%) |
| actions | 952 (100.0%) |
| actions_with_technique | 827 (86.9%) |
| actions_with_execution_start | 46 (4.8%) |
| conditions | 147 |
| operators | 118 |
| flows_with_cycle | 3 (7.3%) |
| flows_whose_first_step_is_unresolved | 9 (22.0%) |
| actions_with_atlas_technique | 36 (3.8%) |
| flows_using_atlas | 2 (4.9%) |
| delta_t_edges | 40 (3.5%) |

| Action classification outcome | n (% of actions) |
|---|---|
| resolved | 668 (70.2%) |
| rule_dependent | 124 (13.0%) |
| preparation | 28 (2.9%) |
| unmapped | 7 (0.7%) |
| no_technique | 125 (13.1%) |

| Cluster | actions certain | actions upper | flows certain | flows upper |
|---|---|---|---|---|
| #1 | 511 (53.7%) | 624 (65.5%) | 40 (97.6%) | 40 (97.6%) |
| #2 | 13 (1.4%) | 20 (2.1%) | 10 (24.4%) | 15 (36.6%) |
| #3 | 11 (1.2%) | 22 (2.3%) | 11 (26.8%) | 16 (39.0%) |
| #4 | 92 (9.7%) | 104 (10.9%) | 27 (65.9%) | 28 (68.3%) |
| #5 | 4 (0.4%) | 6 (0.6%) | 4 (9.8%) | 5 (12.2%) |
| #6 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| #7 | 263 (27.6%) | 380 (39.9%) | 37 (90.2%) | 40 (97.6%) |
| #8 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| #9 | 31 (3.3%) | 35 (3.7%) | 19 (46.3%) | 19 (46.3%) |
| #10 | 5 (0.5%) | 9 (0.9%) | 3 (7.3%) | 5 (12.2%) |

| Entry cluster | flows |
|---|---|
| #9 | 14 (34.1%) |
| #1 | 8 (19.5%) |
| #2 | 5 (12.2%) |
| #3 | 4 (9.8%) |
| #4 | 4 (9.8%) |
| #10 | 3 (7.3%) |
| #7 | 2 (4.9%) |
| ? | 1 (2.4%) |

| Transition | n |
|---|---|
| #1 → #7 | 179 |
| #7 → #1 | 144 |
| #4 → #1 | 69 |
| #1 → #4 | 43 |
| #9 → #7 | 26 |
| #7 → #9 | 15 |
| #7 → #4 | 12 |
| #3 → #7 | 11 |
| #2 → #1 | 6 |
| #1 → #2 | 4 |
| #10 → #7 | 4 |
| #1 → #5 | 3 |
| #7 → #3 | 2 |
| #7 → #2 | 2 |
| #7 → #10 | 2 |

Compression: 952 actions → 853 steps (1.12 actions per step); flows fully classified: 0 (0.0%)

| Flow | scope | actions | steps | ? | entry | derived path (compressed) |
|---|---|---|---|---|---|---|
| Black Basta Ransomware | malware | 38 | 33 | 5 | #9 | `#9 → #7 → #9 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → ? → #1 → ? → #1 → ? → #4 → #1 → #7 → #1 → #7 → #1 → … → #1 → #7 → ? → #1 → #7 → #1` |
| CISA AA22-138B VMWare Workspace (Alt) | incident | 11 | 9 | 3 | #3 | `#3 → #7 → ? → #1 → #7 → ? → #1 → ? → #1` |
| CISA AA22-138B VMWare Workspace (TA1) | incident | 10 | 8 | 2 | #7 | `#7 → #3 → #7 → #1 → ? → #1 → #7 → ?` |
| CISA AA22-138B VMWare Workspace (TA2) | incident | 11 | 9 | 3 | #7 | `#7 → #1 → #7 → ? → #1 → ? → #1 → ? → #1` |
| CISA Iranian APT | incident | 23 | 20 | 3 | #2 | `#2 → #1 → #7 → #1 → #7 → #4 → #1 → #4 → ? → #1 → #4 → #1 → #4 → #1 → ? → #4 → #1 → #7 → #1 → ?` |
| Cobalt Kitty Campaign | campaign | 27 | 29 | 2 | #9 | `? → #9 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → ? → #1 → #7 → #4 → #1` |
| Conti CISA Alert | malware | 18 | 16 | 5 | #9 | `#9 → #7 → #9 → ? → ? → #9 → #7 → #4 → #1 → #4 → … → #3 → #7 → ? → #7 → …` |
| Conti PWC | incident | 7 | 8 | 2 | #9 | `#9 → #7 → #9 → #7 → ? → #7 → #1 → ?` |
| Conti Ransomware | malware | 19 | 17 | 1 | #9 | `#9 → #7 → #1 → #7 → #1 → #7 → ? → #1 → #4 → #1 → #4 → #1 → #4 → #1 → #4 → #1 → #7` |
| DFIR - BumbleBee Round 2 | incident | 19 | 20 | 3 | #1 | `#1 → #7 →[Δt=14m] #1 → #7 → #1 →[Δt=0s] #7 → #1 → #7 → #1 → #7 → #1 →[Δt=5m] ? →[Δt=22m] #4 → #1 → ? → #1 →[Δt=4m] ? →[Δt=4m] #4 → #1 →[Δt=4h] #7` |
| Equifax Breach (with Mitigations/Detections) | incident | 12 | 9 | 2 | #1 | `#1 → #2 → #1 → #7 → ? → #7 → #1 → … → #1` |
| Example Attack Tree | attack-tree | 63 | 1 | 1 | ? | `…` |
| FIN13 Case 1 | incident | 40 | 42 | 7 | #1 | `#1 → #2 → #1 → #7 → #1 → … → #1 → #7 → ? → #1 → #7 → #1 → #4 → #1 → #4 → #1 → #2 → ? → #4 → #1 → ? → #1 → ? → #4 → #1 → #4 → #1 → #7 → #1 → #7 → #4 → #1 → #4 → #1 → #4 → #1 → ? → #4 → #1 → #5 → #4 → ?` |
| FIN13 Case 2 | incident | 19 | 21 | 6 | #2 | `#2 → #1 → #7 → #3 → #7 → ? → #1 → ? → ? → #4 → #1 → #4 → #1 → ? → #1 → #7 → #4 → #1 → #5 → ? → ?` |
| Gootloader | incident | 36 | 44 | 2 | #3 | `#3 → #7 → #9 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → ? → #4 → #1 → #4 → #1 → #4 → #1 → #4 → #1 → #4 → #1 → #7 → #1 → ? → #4 → #1 → #7 → #1 → #4 → #1 → #4 → #1` |
| Hancitor DLL | incident | 23 | 26 | 4 | #9 | `? → #9 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → ? → #1 → #7 → #1 → #7 → #1 → ? → #4 → #1 → ? → #1 → #7 → #1` |
| Ivanti Vulnerabilities | incident | 23 | 26 | 9 | #2 | `#2 → #4 → #1 → #4 → #1 → ? → #1 → #7 → #1 → #7 → #1 → #7 → ? → ? → #1 → #7 → ? → ? → ? → #4 → #1 → ? → ? → ? → #1 → #4` |
| JP Morgan Breach | incident | 12 | 10 | 5 | #9 | `#9 → ? → #2 → ? → ? → ? → #1 → … → #1 → #2` |
| Maastricht University Ransomware | incident | 18 | 17 | 3 | #9 | `#9 → #7 → #9 → #7 → ? → #1 → #7 → #1 → #7 → #2 → ? → #1 → ? → #1 → #7 → #1 → #7` |
| Mac Malware Steals Crypto | malware | 9 | 11 | 4 | #1 | `? → #1 → #7 → #1 → #7 → ? → ? → ? → #1 → #7 → #1` |
| Marriott Breach | incident | 8 | 6 | 3 | #9 | `#9 → ? → … → #1 → ? → #1` |
| MITRE NERVE | incident | 33 | 30 | 7 | #2 | `#2 →[Δt=0s] #1 → #7 →[Δt=3d] #1 → #4 →[Δt=7d] #1 →[Δt=0s] … →[Δt=8d] #4 →[Δt=7d] … →[Δt=0s] #1 →[Δt=14h] #4 → #1 →[Δt=12h] … →[Δt=2d] #1 →[Δt=1d] #7 →[Δt=0s] … →[Δt=0s] #1 →[Δt=0s] ? →[Δt=0s] #1 → #7 →[Δt=0s] #1 → #7 →[Δt=0s] #1 → #7 →[Δt=12d] #1 →[Δt=1d] ? →[Δt=2d] #4 → #1 →[Δt=12d] … →[Δt=15d] #7` |
| Muddy Water | threat-actor | 28 | 35 | 6 | #9 | `#9 → #7 → #9 → #7 → #9 → #7 → #9 → #7 → #9 → #7 → #1 → #7 → #1 → ? → #1 → #7 → ? → #1 → #7 → #1 → #7 → #1 → #7 → ? → #1 → #7 → ? → #7 → #1 → #7 → … → #7 → ? → #1 → #7` |
| NotPetya | incident | 23 | 26 | 6 | #10 | `#10 → #7 → #10 → #7 → #10 → ? → #1 → ? → #1 → #4 → #1 → #7 → ? → #1 → #7 → #1 → #7 → ? → #7 → #1 → #7 → ? → #7 → #1 → ? → #7` |
| OceanLotus | incident | 23 | 22 | 4 | #9 | `#9 → #7 → #9 → #7 → #9 → #7 → ? → #7 → #1 → #7 → #1 → ? → #1 → #4 → #1 → #4 → #1 → #7 → #1 → ? → #1 → ?` |
| OpenClaw Command & Control via Prompt Injection | incident | 18 | 6 | 1 | #1 | `? → #1 → #3 → #7 → #1 → #7` |
| OpenClaw Command & Control via Prompt Injection (with Mitigations/Detections) | incident | 18 | 6 | 1 | #1 | `? → #1 → #3 → #7 → #1 → #7` |
| Ragnar Locker | threat-actor | 19 | 16 | 3 | #4 | `#4 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → … → #1 → ? → #1 → #7 → #1 → … → #7` |
| REvil | malware | 25 | 23 | 3 | #3 | `#3 → #7 → #9 → #7 → #9 → #7 → ? → #7 → #1 → #4 → #1 → ? → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → …` |
| SearchAwesome Adware | malware | 11 | 13 | 3 | #9 | `#9 → #7 → #1 → ? → #5 → ? → #1 → ? → #1 → #7 → #1 → #4 → #1` |
| Shamoon | malware | 23 | 22 | 1 | #1 | `#1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #4 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #4 → #1 → #7 → ?` |
| SolarWinds | incident | 33 | 25 | 7 | #10 | `? → #10 → #7 → #1 → #7 → ? → #1 → #7 → ? → #7 → ? → #1 → #7 → #1 → ? → #1 → #4 → #1 → #7 → #4 → ? → #1 → #7 → #1 → ?` |
| Sony Malware | malware | 18 | 20 | 6 | #1 | `#1 → #7 → ? → #1 → #7 → ? → #1 → #7 → #1 → #7 → #1 → #7 → #1 → ? → #7 → ? → #7 → ? → ? → #7` |
| SWIFT Heist | incident | 11 | 9 | 3 | #9 | `#9 → #7 → #2 → ? → #4 → #1 → … → #1 → ?` |
| Target Breach | incident | 17 | 17 | 3 | #10 | `#10 → #7 → #9 → #4 → #3 → #7 → #4 → #1 → #7 → #1 → #4 → #1 → #5 → #1 → ? → ? → ?` |
| Tesla Kubernetes Breach | incident | 9 | 9 | 2 | #4 | `… → #4 → #1 → #4 → #1 → #7 → #4 → #1 → ?` |
| ToolShell Vulnerability in Sharepoint | campaign | 15 | 18 | 4 | #2 | `#2 → #1 → #7 → #1 → #7 → #1 → ? → #1 → #7 → #1 → #7 → #1 → #4 → ? → #1 → #4 → … → ?` |
| Turla - Carbon Emulation Plan | emulation-plan | 81 | 73 | 15 | #9 | `? → #9 → #7 → #1 → #7 → #1 → #7 → ? → ? → #1 → #7 → #1 → #7 → #1 → … → #1 → #7 → #1 → #7 → ? → #1 → ? → ? → #1 → #7 → #1 → #7 → #1 → #7 → … → #1 → … → #1 → #7 → #4 → #1 → #4 → #1 → #7 → #1 → #7 → ? → #1 → #7 → ? → #1 → #7 → #4 → #1 → #7 → #1 → ? → #1 → #4 → #1 → #4 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → ? → #1 → #7 → ? → #1 → #7 → ? → #3 → #7` |
| Turla - Snake Emulation Plan | emulation-plan | 74 | 72 | 9 | #3 | `#3 → #7 → #1 → #7 → #9 → #7 → ? → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → ? → #7 → #1 → #7 → ? → #7 → ? → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → ? → #1 → #7 → #1 → #4 → #1 → #4 → #1 → #7 → #4 → #1 → #7 → #1 → #7 → #1 → #7 → ? → #4 → #1 → #7 → #1 → #7 → #1 → #4 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #4 → #1 → … → #1 → … → #7 → ?` |
| Uber Breach | incident | 8 | 8 | 2 | #4 | `#4 → #1 → #9 → #4 → #1 → #4 → ? → ?` |
| WhisperGate | campaign | 19 | 21 | 3 | #4 | `#4 → #1 → ? → #1 → #7 → #1 → … → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → #7 → #1 → ?` |


### Overlap with hand-classified TLCTC paths

**SolarWinds.afb** vs `json-schemas/layer-3/examples/solarwinds-2020.json`

- hand path: `#10 → #7 → #4 → #1` (4 steps)
- derived (compressed): `? → #10 → #7 → #1 → #7 → ? → #1 → #7 → ? → #7 → ? → #1 → #7 → #1 → ? → #1 → #4 → #1 → #7 → #4 → ? → #1 → #7 → #1 → ?` (25 steps from 38 raw)
- hand clusters reached (certain / upper): 4 / 4 of 4; derived clusters not in the hand path: none
- longest common cluster subsequence: 4 of 4; entry cluster agrees: True

**Tesla Kubernetes Breach.afb** vs `attack-paths/tesla-k8s-cryptojacking-2018.json`

- hand path: `#1 → #7 → #1 → #4` (4 steps)
- derived (compressed): `… → #4 → #1 → #4 → #1 → #7 → #4 → #1 → ?` (9 steps from 11 raw)
- hand clusters reached (certain / upper): 3 / 3 of 3; derived clusters not in the hand path: none
- longest common cluster subsequence: 3 of 4; entry cluster agrees: False
