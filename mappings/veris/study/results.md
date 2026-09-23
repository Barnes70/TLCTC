# VCDB study results

Generated 2026-09-22T22:48:06Z from VCDB commit `230cf22b56a481dd1a994b21e4d94c59e2bccea9` (10047 records, sha256 `e4be5dd432ccfad16520a6b60dd83e9d47c63b0f3352c26c4d43a5dd774c32c0`), mapping updated 2026-09-22.

Every cell is n (percentage of the row's denominator). Strata follow the VCDB README's warning that `phidbr` and `priority` records are not randomly selected.

### Stratum `all` — every record in the joined dataset

Records: 10047

| Threat-axis purity | n (% of records) |
|---|---|
| records | 10047 (100.0%) |
| threat_bearing | 4070 (40.5%) |
| threat_only | 3884 (38.7%) |
| mixed_threat_and_operational | 186 (1.9%) |
| operational_only | 4020 (40.0%) |
| operational_only.error_or_failure | 2578 (25.7%) |
| operational_only.abuse_of_rights | 1413 (14.1%) |
| operational_only.other_mix | 27 (0.3%) |
| out_of_scope_only | 2 (0.0%) |
| unknown_only | 1957 (19.5%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 4070 (100.0%) |
| resolved | 1911 (47.0%) |
| rule_dependent | 1311 (32.2%) |
| cause_lost | 848 (20.8%) |
| cause_lost.malware_without_enabler | 425 (10.4%) |
| cause_lost.credential_use_without_acquisition | 212 (5.2%) |
| cause_lost.social_without_follow_on | 211 (5.2%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 2468 (60.6%) |
| multi_cluster_records | 1602 (39.4%) |
| mean_clusters_lower_bound | 1.071 |
| mean_clusters_upper_bound | 1.909 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 71 (0.7%) | 822 (8.2%) |
| #2 | 125 (1.2%) | 1289 (12.8%) |
| #3 | 0 (0.0%) | 1291 (12.8%) |
| #4 | 506 (5.0%) | 506 (5.0%) |
| #5 | 11 (0.1%) | 11 (0.1%) |
| #6 | 0 (0.0%) | 166 (1.7%) |
| #7 | 1482 (14.8%) | 1486 (14.8%) |
| #8 | 1593 (15.9%) | 1593 (15.9%) |
| #9 | 573 (5.7%) | 587 (5.8%) |
| #10 | 0 (0.0%) | 18 (0.2%) |

Records with two or more certain clusters: 415 (4.1%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #7 + #9 | 251 | #9 → #7 |
| #4 + #9 | 201 | #9 → #4 |
| #4 + #7 | 136 | #4 → #7 | #7 → #4 |
| #8 + #9 | 13 | #9 → #8 |
| #4 + #8 | 10 | #8 → #4 |
| #2 + #7 | 7 | #2 → #7 |
| #5 + #7 | 7 | #5 → #7 |
| #5 + #9 | 7 | #9 → #5 |
| #1 + #7 | 6 | #1 → #7 |
| #1 + #4 | 5 | #1 → #4 |

| attribute.availability.variety | n | DRE |
|---|---|---|
| Loss | 2061 | Av |
| Destruction | 44 | Av |
| Obscuration | 295 | Ac |
| Interruption | 309 | A |
| Degradation | 26 | A |
| Acceleration | 0 | A |
| Other | 3 | A |
| Unknown | 6 | A |

| Ransomware records | n (% of ransomware) |
|---|---|
| records | 1084 (10.8%) |
| with_obscuration_Ac | 290 (26.8%) |
| with_loss_Av | 13 (1.2%) |
| with_destruction_Av | 0 (0.0%) |
| with_interruption_A | 16 (1.5%) |
| with_no_availability_attribute | 772 (71.2%) |
| with_confirmed_disclosure_C | 849 (78.3%) |

| Unknown collapse | n (% of records) |
|---|---|
| action_unknown | 287 (2.9%) |
| any_unresolved_item | 3250 (32.3%) |
| unknown_only | 1957 (19.5%) |
| unmapped_values | 0 (0.0%) |

| Category | records | variety Unknown | variety Other |
|---|---|---|---|
| hacking | 3368 (33.5%) | 1695 (16.9%) | 42 (0.4%) |
| malware | 1647 (16.4%) | 172 (1.7%) | 65 (0.6%) |
| social | 647 (6.4%) | 17 (0.2%) | 11 (0.1%) |
| misuse | 1789 (17.8%) | 47 (0.5%) | 5 (0.0%) |
| physical | 1626 (16.2%) | 6 (0.1%) | 2 (0.0%) |
| error | 2681 (26.7%) | 50 (0.5%) | 76 (0.8%) |
| environmental | 10 (0.1%) | 4 (0.0%) | 0 (0.0%) |

Distinct action-variety signatures: 534 over 9815 (97.7%) records with at least one variety

| Most frequent exact variety set | n (% of records) |
|---|---|
| hacking.variety.Unknown | 1369 (13.6%) |
| misuse.variety.Privilege abuse | 964 (9.6%) |
| error.variety.Misdelivery | 952 (9.5%) |
| physical.variety.Theft | 927 (9.2%) |
| hacking.variety.Backdoor + hacking.variety.Exploit vuln + malware.variety.Backdoor + malware.variety.Backdoor or C2 + malware.variety.Ransomware | 747 (7.4%) |
| error.variety.Loss | 382 (3.8%) |
| error.variety.Publishing error | 369 (3.7%) |
| error.variety.Disposal error | 307 (3.1%) |
| error.variety.Misconfiguration | 301 (3.0%) |
| malware.variety.Ransomware | 209 (2.1%) |

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 2122 (21.1%) |
| subset | 286 (2.8%) |
| disjoint | 9 (0.1%) |
| no-attack-edge | 7630 (75.9%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.malware.variety.Capture stored data | 187 | #7 | #1, #4, #5 |
| action.malware.variety.Scan network | 106 | #7 | #1 |
| action.malware.variety.Packet sniffer | 7 | #7 | #1 |
| action.hacking.variety.Buffer overflow | 5 | #2 | #3, #7 |
| action.hacking.variety.OS commanding | 4 | #2 | #1, #4, #7 |
| action.hacking.variety.Cryptanalysis | 3 | #5 | #1, #7 |
| action.malware.variety.DoS | 1 | #7 | #1, #2, #6 |

### Stratum `year:<=2014` — timeline.incident.year <= 2014

Records: 5684

| Threat-axis purity | n (% of records) |
|---|---|
| records | 5684 (100.0%) |
| threat_bearing | 1828 (32.2%) |
| threat_only | 1728 (30.4%) |
| mixed_threat_and_operational | 100 (1.8%) |
| operational_only | 2541 (44.7%) |
| operational_only.error_or_failure | 1591 (28.0%) |
| operational_only.abuse_of_rights | 936 (16.5%) |
| operational_only.other_mix | 12 (0.2%) |
| out_of_scope_only | 2 (0.0%) |
| unknown_only | 1315 (23.1%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 1828 (100.0%) |
| resolved | 1227 (67.1%) |
| rule_dependent | 381 (20.8%) |
| cause_lost | 220 (12.0%) |
| cause_lost.malware_without_enabler | 91 (5.0%) |
| cause_lost.credential_use_without_acquisition | 61 (3.3%) |
| cause_lost.social_without_follow_on | 68 (3.7%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 1296 (70.9%) |
| multi_cluster_records | 532 (29.1%) |
| mean_clusters_lower_bound | 1.123 |
| mean_clusters_upper_bound | 1.563 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 30 (0.5%) | 30 (0.5%) |
| #2 | 83 (1.5%) | 368 (6.5%) |
| #3 | 0 (0.0%) | 370 (6.5%) |
| #4 | 232 (4.1%) | 232 (4.1%) |
| #5 | 11 (0.2%) | 11 (0.2%) |
| #6 | 0 (0.0%) | 127 (2.2%) |
| #7 | 324 (5.7%) | 327 (5.8%) |
| #8 | 1065 (18.7%) | 1065 (18.7%) |
| #9 | 307 (5.4%) | 316 (5.6%) |
| #10 | 0 (0.0%) | 12 (0.2%) |

Records with two or more certain clusters: 262 (4.6%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #7 + #9 | 209 | #9 → #7 |
| #4 + #9 | 121 | #9 → #4 |
| #4 + #7 | 114 | #4 → #7 | #7 → #4 |
| #8 + #9 | 9 | #9 → #8 |
| #5 + #7 | 7 | #5 → #7 |
| #5 + #9 | 7 | #9 → #5 |
| #4 + #8 | 6 | #8 → #4 |
| #1 + #7 | 4 | #1 → #7 |
| #2 + #7 | 4 | #2 → #7 |
| #2 + #4 | 3 | #2 → #4 |

| attribute.availability.variety | n | DRE |
|---|---|---|
| Loss | 1598 | Av |
| Destruction | 28 | Av |
| Obscuration | 11 | Ac |
| Interruption | 225 | A |
| Degradation | 14 | A |
| Acceleration | 0 | A |
| Other | 3 | A |
| Unknown | 0 | A |

| Ransomware records | n (% of ransomware) |
|---|---|
| records | 19 (0.3%) |
| with_obscuration_Ac | 8 (42.1%) |
| with_loss_Av | 8 (42.1%) |
| with_destruction_Av | 0 (0.0%) |
| with_interruption_A | 1 (5.3%) |
| with_no_availability_attribute | 2 (10.5%) |
| with_confirmed_disclosure_C | 3 (15.8%) |

| Unknown collapse | n (% of records) |
|---|---|
| action_unknown | 199 (3.5%) |
| any_unresolved_item | 2063 (36.3%) |
| unknown_only | 1315 (23.1%) |
| unmapped_values | 0 (0.0%) |

| Category | records | variety Unknown | variety Other |
|---|---|---|---|
| hacking | 1560 (27.4%) | 1074 (18.9%) | 24 (0.4%) |
| malware | 414 (7.3%) | 100 (1.8%) | 61 (1.1%) |
| social | 344 (6.1%) | 5 (0.1%) | 7 (0.1%) |
| misuse | 1164 (20.5%) | 21 (0.4%) | 2 (0.0%) |
| physical | 1071 (18.8%) | 2 (0.0%) | 1 (0.0%) |
| error | 1631 (28.7%) | 24 (0.4%) | 39 (0.7%) |
| environmental | 8 (0.1%) | 4 (0.1%) | 0 (0.0%) |

Distinct action-variety signatures: 323 over 5495 (96.7%) records with at least one variety

| Most frequent exact variety set | n (% of records) |
|---|---|
| hacking.variety.Unknown | 906 (15.9%) |
| misuse.variety.Privilege abuse | 708 (12.5%) |
| physical.variety.Theft | 702 (12.4%) |
| error.variety.Misdelivery | 685 (12.1%) |
| error.variety.Loss | 298 (5.2%) |
| error.variety.Disposal error | 216 (3.8%) |
| error.variety.Publishing error | 210 (3.7%) |
| physical.variety.Disabled controls + physical.variety.Theft | 126 (2.2%) |
| hacking.variety.DoS | 117 (2.1%) |
| hacking.variety.Brute force + hacking.variety.Use of stolen creds + malware.variety.Backdoor + malware.variety.Backdoor or C2 + malware.variety.Brute force + malware.variety.C2 + malware.variety.Capture stored data + malware.variety.Downloader + malware.variety.Exploit vuln + malware.variety.Export data + malware.variety.Scan network + malware.variety.Spyware/Keylogger + social.variety.Phishing | 88 (1.5%) |

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 482 (8.5%) |
| subset | 242 (4.3%) |
| disjoint | 6 (0.1%) |
| no-attack-edge | 4954 (87.2%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.malware.variety.Capture stored data | 174 | #7 | #1, #4, #5 |
| action.malware.variety.Scan network | 105 | #7 | #1 |
| action.malware.variety.Packet sniffer | 6 | #7 | #1 |
| action.hacking.variety.Buffer overflow | 3 | #2 | #3, #7 |
| action.hacking.variety.Cryptanalysis | 3 | #5 | #1, #7 |
| action.malware.variety.DoS | 1 | #7 | #1, #2, #6 |

### Stratum `year:2015-2019` — timeline.incident.year in 2015..2019

Records: 3046

| Threat-axis purity | n (% of records) |
|---|---|
| records | 3046 (100.0%) |
| threat_bearing | 1199 (39.4%) |
| threat_only | 1114 (36.6%) |
| mixed_threat_and_operational | 85 (2.8%) |
| operational_only | 1312 (43.1%) |
| operational_only.error_or_failure | 841 (27.6%) |
| operational_only.abuse_of_rights | 456 (15.0%) |
| operational_only.other_mix | 15 (0.5%) |
| out_of_scope_only | 0 (0.0%) |
| unknown_only | 535 (17.6%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 1199 (100.0%) |
| resolved | 634 (52.9%) |
| rule_dependent | 145 (12.1%) |
| cause_lost | 420 (35.0%) |
| cause_lost.malware_without_enabler | 223 (18.6%) |
| cause_lost.credential_use_without_acquisition | 55 (4.6%) |
| cause_lost.social_without_follow_on | 142 (11.8%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 945 (78.8%) |
| multi_cluster_records | 254 (21.2%) |
| mean_clusters_lower_bound | 1.048 |
| mean_clusters_upper_bound | 1.288 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 34 (1.1%) | 38 (1.2%) |
| #2 | 38 (1.2%) | 136 (4.5%) |
| #3 | 0 (0.0%) | 136 (4.5%) |
| #4 | 153 (5.0%) | 153 (5.0%) |
| #5 | 0 (0.0%) | 0 (0.0%) |
| #6 | 0 (0.0%) | 37 (1.2%) |
| #7 | 280 (9.2%) | 281 (9.2%) |
| #8 | 515 (16.9%) | 515 (16.9%) |
| #9 | 237 (7.8%) | 242 (7.9%) |
| #10 | 0 (0.0%) | 6 (0.2%) |

Records with two or more certain clusters: 121 (4.0%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #4 + #9 | 61 | #9 → #4 |
| #7 + #9 | 31 | #9 → #7 |
| #4 + #7 | 17 | #4 → #7 | #7 → #4 |
| #4 + #8 | 4 | #8 → #4 |
| #8 + #9 | 4 | #9 → #8 |
| #2 + #7 | 3 | #2 → #7 |
| #1 + #4 | 2 | #1 → #4 |
| #1 + #7 | 2 | #1 → #7 |
| #1 + #2 | 1 | order unknown |
| #2 + #4 | 1 | #2 → #4 |

| attribute.availability.variety | n | DRE |
|---|---|---|
| Loss | 449 | Av |
| Destruction | 12 | Av |
| Obscuration | 166 | Ac |
| Interruption | 72 | A |
| Degradation | 11 | A |
| Acceleration | 0 | A |
| Other | 0 | A |
| Unknown | 5 | A |

| Ransomware records | n (% of ransomware) |
|---|---|
| records | 192 (6.3%) |
| with_obscuration_Ac | 164 (85.4%) |
| with_loss_Av | 5 (2.6%) |
| with_destruction_Av | 0 (0.0%) |
| with_interruption_A | 8 (4.2%) |
| with_no_availability_attribute | 16 (8.3%) |
| with_confirmed_disclosure_C | 24 (12.5%) |

| Unknown collapse | n (% of records) |
|---|---|
| action_unknown | 69 (2.3%) |
| any_unresolved_item | 968 (31.8%) |
| unknown_only | 535 (17.6%) |
| unmapped_values | 0 (0.0%) |

| Category | records | variety Unknown | variety Other |
|---|---|---|---|
| hacking | 770 (25.3%) | 490 (16.1%) | 17 (0.6%) |
| malware | 354 (11.6%) | 71 (2.3%) | 4 (0.1%) |
| social | 266 (8.7%) | 11 (0.4%) | 4 (0.1%) |
| misuse | 603 (19.8%) | 26 (0.9%) | 3 (0.1%) |
| physical | 542 (17.8%) | 4 (0.1%) | 1 (0.0%) |
| error | 904 (29.7%) | 26 (0.9%) | 36 (1.2%) |
| environmental | 2 (0.1%) | 0 (0.0%) | 0 (0.0%) |

Distinct action-variety signatures: 325 over 3009 (98.8%) records with at least one variety

| Most frequent exact variety set | n (% of records) |
|---|---|
| hacking.variety.Unknown | 367 (12.0%) |
| error.variety.Misdelivery | 253 (8.3%) |
| misuse.variety.Privilege abuse | 250 (8.2%) |
| physical.variety.Theft | 218 (7.2%) |
| error.variety.Misconfiguration | 160 (5.3%) |
| physical.variety.Skimmer | 149 (4.9%) |
| error.variety.Publishing error | 141 (4.6%) |
| malware.variety.Ransomware | 130 (4.3%) |
| error.variety.Disposal error | 90 (3.0%) |
| error.variety.Loss | 80 (2.6%) |

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 613 (20.1%) |
| subset | 41 (1.3%) |
| disjoint | 3 (0.1%) |
| no-attack-edge | 2389 (78.4%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.malware.variety.Capture stored data | 12 | #7 | #1, #4, #5 |
| action.hacking.variety.OS commanding | 4 | #2 | #1, #4, #7 |
| action.hacking.variety.Buffer overflow | 2 | #2 | #3, #7 |
| action.malware.variety.Packet sniffer | 1 | #7 | #1 |
| action.malware.variety.Scan network | 1 | #7 | #1 |

### Stratum `year:2020-2026` — timeline.incident.year in 2020..2026

Records: 1317

| Threat-axis purity | n (% of records) |
|---|---|
| records | 1317 (100.0%) |
| threat_bearing | 1043 (79.2%) |
| threat_only | 1042 (79.1%) |
| mixed_threat_and_operational | 1 (0.1%) |
| operational_only | 167 (12.7%) |
| operational_only.error_or_failure | 146 (11.1%) |
| operational_only.abuse_of_rights | 21 (1.6%) |
| operational_only.other_mix | 0 (0.0%) |
| out_of_scope_only | 0 (0.0%) |
| unknown_only | 107 (8.1%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 1043 (100.0%) |
| resolved | 50 (4.8%) |
| rule_dependent | 785 (75.3%) |
| cause_lost | 208 (19.9%) |
| cause_lost.malware_without_enabler | 111 (10.6%) |
| cause_lost.credential_use_without_acquisition | 96 (9.2%) |
| cause_lost.social_without_follow_on | 1 (0.1%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 227 (21.8%) |
| multi_cluster_records | 816 (78.2%) |
| mean_clusters_lower_bound | 1.009 |
| mean_clusters_upper_bound | 3.228 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 7 (0.5%) | 754 (57.3%) |
| #2 | 4 (0.3%) | 785 (59.6%) |
| #3 | 0 (0.0%) | 785 (59.6%) |
| #4 | 121 (9.2%) | 121 (9.2%) |
| #5 | 0 (0.0%) | 0 (0.0%) |
| #6 | 0 (0.0%) | 2 (0.2%) |
| #7 | 878 (66.7%) | 878 (66.7%) |
| #8 | 13 (1.0%) | 13 (1.0%) |
| #9 | 29 (2.2%) | 29 (2.2%) |
| #10 | 0 (0.0%) | 0 (0.0%) |

Records with two or more certain clusters: 32 (2.4%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #4 + #9 | 19 | #9 → #4 |
| #7 + #9 | 11 | #9 → #7 |
| #4 + #7 | 5 | #4 → #7 | #7 → #4 |
| #1 + #4 | 1 | #1 → #4 |

| attribute.availability.variety | n | DRE |
|---|---|---|
| Loss | 14 | Av |
| Destruction | 4 | Av |
| Obscuration | 118 | Ac |
| Interruption | 12 | A |
| Degradation | 1 | A |
| Acceleration | 0 | A |
| Other | 0 | A |
| Unknown | 1 | A |

| Ransomware records | n (% of ransomware) |
|---|---|
| records | 873 (66.3%) |
| with_obscuration_Ac | 118 (13.5%) |
| with_loss_Av | 0 (0.0%) |
| with_destruction_Av | 0 (0.0%) |
| with_interruption_A | 7 (0.8%) |
| with_no_availability_attribute | 754 (86.4%) |
| with_confirmed_disclosure_C | 822 (94.2%) |

| Unknown collapse | n (% of records) |
|---|---|
| action_unknown | 19 (1.4%) |
| any_unresolved_item | 219 (16.6%) |
| unknown_only | 107 (8.1%) |
| unmapped_values | 0 (0.0%) |

| Category | records | variety Unknown | variety Other |
|---|---|---|---|
| hacking | 1038 (78.8%) | 131 (9.9%) | 1 (0.1%) |
| malware | 879 (66.7%) | 1 (0.1%) | 0 (0.0%) |
| social | 37 (2.8%) | 1 (0.1%) | 0 (0.0%) |
| misuse | 22 (1.7%) | 0 (0.0%) | 0 (0.0%) |
| physical | 13 (1.0%) | 0 (0.0%) | 0 (0.0%) |
| error | 146 (11.1%) | 0 (0.0%) | 1 (0.1%) |
| environmental | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

Distinct action-variety signatures: 66 over 1311 (99.5%) records with at least one variety

| Most frequent exact variety set | n (% of records) |
|---|---|
| hacking.variety.Backdoor + hacking.variety.Exploit vuln + malware.variety.Backdoor + malware.variety.Backdoor or C2 + malware.variety.Ransomware | 747 (56.7%) |
| hacking.variety.Unknown | 96 (7.3%) |
| error.variety.Misconfiguration | 95 (7.2%) |
| hacking.variety.Use of stolen creds | 94 (7.1%) |
| malware.variety.Ransomware | 77 (5.8%) |
| hacking.variety.Unknown + malware.variety.Ransomware | 28 (2.1%) |
| hacking.variety.Exploit vuln | 20 (1.5%) |
| error.variety.Publishing error | 18 (1.4%) |
| error.variety.Misdelivery | 14 (1.1%) |
| hacking.variety.Use of stolen creds + social.variety.Pretexting | 11 (0.8%) |

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 1027 (78.0%) |
| subset | 3 (0.2%) |
| disjoint | 0 (0.0%) |
| no-attack-edge | 287 (21.8%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.malware.variety.Capture stored data | 1 | #7 | #1, #4, #5 |

### Stratum `sub_source:none` — plus.sub_source absent (random selection per the VCDB README)

Records: 8110

| Threat-axis purity | n (% of records) |
|---|---|
| records | 8110 (100.0%) |
| threat_bearing | 3490 (43.0%) |
| threat_only | 3339 (41.2%) |
| mixed_threat_and_operational | 151 (1.9%) |
| operational_only | 3063 (37.8%) |
| operational_only.error_or_failure | 1967 (24.3%) |
| operational_only.abuse_of_rights | 1074 (13.2%) |
| operational_only.other_mix | 20 (0.2%) |
| out_of_scope_only | 2 (0.0%) |
| unknown_only | 1557 (19.2%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 3490 (100.0%) |
| resolved | 1659 (47.5%) |
| rule_dependent | 1247 (35.7%) |
| cause_lost | 584 (16.7%) |
| cause_lost.malware_without_enabler | 261 (7.5%) |
| cause_lost.credential_use_without_acquisition | 167 (4.8%) |
| cause_lost.social_without_follow_on | 156 (4.5%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 2024 (58.0%) |
| multi_cluster_records | 1466 (42.0%) |
| mean_clusters_lower_bound | 1.066 |
| mean_clusters_upper_bound | 2.011 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 54 (0.7%) | 805 (9.9%) |
| #2 | 104 (1.3%) | 1231 (15.2%) |
| #3 | 0 (0.0%) | 1233 (15.2%) |
| #4 | 398 (4.9%) | 398 (4.9%) |
| #5 | 11 (0.1%) | 11 (0.1%) |
| #6 | 0 (0.0%) | 164 (2.0%) |
| #7 | 1281 (15.8%) | 1285 (15.8%) |
| #8 | 1419 (17.5%) | 1419 (17.5%) |
| #9 | 454 (5.6%) | 462 (5.7%) |
| #10 | 0 (0.0%) | 12 (0.1%) |

Records with two or more certain clusters: 336 (4.1%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #7 + #9 | 231 | #9 → #7 |
| #4 + #9 | 159 | #9 → #4 |
| #4 + #7 | 124 | #4 → #7 | #7 → #4 |
| #8 + #9 | 12 | #9 → #8 |
| #4 + #8 | 9 | #8 → #4 |
| #5 + #7 | 7 | #5 → #7 |
| #5 + #9 | 7 | #9 → #5 |
| #1 + #7 | 6 | #1 → #7 |
| #2 + #7 | 5 | #2 → #7 |
| #1 + #4 | 3 | #1 → #4 |

| attribute.availability.variety | n | DRE |
|---|---|---|
| Loss | 1748 | Av |
| Destruction | 34 | Av |
| Obscuration | 154 | Ac |
| Interruption | 297 | A |
| Degradation | 25 | A |
| Acceleration | 0 | A |
| Other | 3 | A |
| Unknown | 5 | A |

| Ransomware records | n (% of ransomware) |
|---|---|
| records | 924 (11.4%) |
| with_obscuration_Ac | 149 (16.1%) |
| with_loss_Av | 10 (1.1%) |
| with_destruction_Av | 0 (0.0%) |
| with_interruption_A | 12 (1.3%) |
| with_no_availability_attribute | 758 (82.0%) |
| with_confirmed_disclosure_C | 801 (86.7%) |

| Unknown collapse | n (% of records) |
|---|---|
| action_unknown | 242 (3.0%) |
| any_unresolved_item | 2610 (32.2%) |
| unknown_only | 1557 (19.2%) |
| unmapped_values | 0 (0.0%) |

| Category | records | variety Unknown | variety Other |
|---|---|---|---|
| hacking | 2857 (35.2%) | 1343 (16.6%) | 37 (0.5%) |
| malware | 1418 (17.5%) | 143 (1.8%) | 65 (0.8%) |
| social | 504 (6.2%) | 7 (0.1%) | 9 (0.1%) |
| misuse | 1361 (16.8%) | 26 (0.3%) | 5 (0.1%) |
| physical | 1439 (17.7%) | 5 (0.1%) | 2 (0.0%) |
| error | 2036 (25.1%) | 36 (0.4%) | 45 (0.6%) |
| environmental | 9 (0.1%) | 4 (0.0%) | 0 (0.0%) |

Distinct action-variety signatures: 441 over 7906 (97.5%) records with at least one variety

| Most frequent exact variety set | n (% of records) |
|---|---|
| hacking.variety.Unknown | 1076 (13.3%) |
| error.variety.Misdelivery | 818 (10.1%) |
| physical.variety.Theft | 776 (9.6%) |
| misuse.variety.Privilege abuse | 753 (9.3%) |
| hacking.variety.Backdoor + hacking.variety.Exploit vuln + malware.variety.Backdoor + malware.variety.Backdoor or C2 + malware.variety.Ransomware | 747 (9.2%) |
| error.variety.Loss | 327 (4.0%) |
| error.variety.Publishing error | 285 (3.5%) |
| error.variety.Disposal error | 245 (3.0%) |
| physical.variety.Skimmer | 178 (2.2%) |
| hacking.variety.Use of stolen creds | 146 (1.8%) |

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 1734 (21.4%) |
| subset | 282 (3.5%) |
| disjoint | 8 (0.1%) |
| no-attack-edge | 6086 (75.0%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.malware.variety.Capture stored data | 182 | #7 | #1, #4, #5 |
| action.malware.variety.Scan network | 105 | #7 | #1 |
| action.malware.variety.Packet sniffer | 6 | #7 | #1 |
| action.hacking.variety.Buffer overflow | 4 | #2 | #3, #7 |
| action.hacking.variety.Cryptanalysis | 3 | #5 | #1, #7 |
| action.hacking.variety.OS commanding | 2 | #2 | #1, #4, #7 |
| action.malware.variety.DoS | 1 | #7 | #1, #2, #6 |

### Stratum `sub_source:phidbr` — plus.sub_source = phidbr (healthcare, selected on purpose)

Records: 1310

| Threat-axis purity | n (% of records) |
|---|---|
| records | 1310 (100.0%) |
| threat_bearing | 412 (31.5%) |
| threat_only | 381 (29.1%) |
| mixed_threat_and_operational | 31 (2.4%) |
| operational_only | 715 (54.6%) |
| operational_only.error_or_failure | 393 (30.0%) |
| operational_only.abuse_of_rights | 315 (24.0%) |
| operational_only.other_mix | 7 (0.5%) |
| out_of_scope_only | 0 (0.0%) |
| unknown_only | 183 (14.0%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 412 (100.0%) |
| resolved | 205 (49.8%) |
| rule_dependent | 15 (3.6%) |
| cause_lost | 192 (46.6%) |
| cause_lost.malware_without_enabler | 119 (28.9%) |
| cause_lost.credential_use_without_acquisition | 24 (5.8%) |
| cause_lost.social_without_follow_on | 49 (11.9%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 345 (83.7%) |
| multi_cluster_records | 67 (16.3%) |
| mean_clusters_lower_bound | 1.114 |
| mean_clusters_upper_bound | 1.182 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 3 (0.2%) | 3 (0.2%) |
| #2 | 3 (0.2%) | 9 (0.7%) |
| #3 | 0 (0.0%) | 9 (0.7%) |
| #4 | 64 (4.9%) | 64 (4.9%) |
| #5 | 0 (0.0%) | 0 (0.0%) |
| #6 | 0 (0.0%) | 1 (0.1%) |
| #7 | 139 (10.6%) | 139 (10.6%) |
| #8 | 155 (11.8%) | 155 (11.8%) |
| #9 | 95 (7.3%) | 101 (7.7%) |
| #10 | 0 (0.0%) | 6 (0.5%) |

Records with two or more certain clusters: 53 (4.0%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #4 + #9 | 32 | #9 → #4 |
| #7 + #9 | 12 | #9 → #7 |
| #4 + #7 | 6 | #4 → #7 | #7 → #4 |
| #2 + #7 | 1 | #2 → #7 |
| #4 + #8 | 1 | #8 → #4 |
| #8 + #9 | 1 | #9 → #8 |

| attribute.availability.variety | n | DRE |
|---|---|---|
| Loss | 236 | Av |
| Destruction | 2 | Av |
| Obscuration | 108 | Ac |
| Interruption | 6 | A |
| Degradation | 1 | A |
| Acceleration | 0 | A |
| Other | 0 | A |
| Unknown | 0 | A |

| Ransomware records | n (% of ransomware) |
|---|---|
| records | 126 (9.6%) |
| with_obscuration_Ac | 108 (85.7%) |
| with_loss_Av | 3 (2.4%) |
| with_destruction_Av | 0 (0.0%) |
| with_interruption_A | 3 (2.4%) |
| with_no_availability_attribute | 13 (10.3%) |
| with_confirmed_disclosure_C | 22 (17.5%) |

| Unknown collapse | n (% of records) |
|---|---|
| action_unknown | 19 (1.5%) |
| any_unresolved_item | 343 (26.2%) |
| unknown_only | 183 (14.0%) |
| unmapped_values | 0 (0.0%) |

| Category | records | variety Unknown | variety Other |
|---|---|---|---|
| hacking | 213 (16.3%) | 141 (10.8%) | 1 (0.1%) |
| malware | 153 (11.7%) | 14 (1.1%) | 0 (0.0%) |
| social | 115 (8.8%) | 7 (0.5%) | 2 (0.2%) |
| misuse | 395 (30.2%) | 18 (1.4%) | 0 (0.0%) |
| physical | 168 (12.8%) | 1 (0.1%) | 0 (0.0%) |
| error | 424 (32.4%) | 13 (1.0%) | 22 (1.7%) |
| environmental | 1 (0.1%) | 0 (0.0%) | 0 (0.0%) |

Distinct action-variety signatures: 151 over 1300 (99.2%) records with at least one variety

| Most frequent exact variety set | n (% of records) |
|---|---|
| misuse.variety.Privilege abuse | 191 (14.6%) |
| physical.variety.Theft | 136 (10.4%) |
| error.variety.Misdelivery | 122 (9.3%) |
| hacking.variety.Unknown | 113 (8.6%) |
| malware.variety.Ransomware | 96 (7.3%) |
| error.variety.Disposal error | 58 (4.4%) |
| error.variety.Publishing error | 58 (4.4%) |
| error.variety.Loss | 49 (3.7%) |
| error.variety.Misconfiguration | 45 (3.4%) |
| misuse.variety.Data mishandling | 44 (3.4%) |

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 242 (18.5%) |
| subset | 1 (0.1%) |
| disjoint | 1 (0.1%) |
| no-attack-edge | 1066 (81.4%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.malware.variety.Capture stored data | 3 | #7 | #1, #4, #5 |
| action.hacking.variety.Buffer overflow | 1 | #2 | #3, #7 |

### Stratum `sub_source:priority` — plus.sub_source = priority (selected on purpose)

Records: 602

| Threat-axis purity | n (% of records) |
|---|---|
| records | 602 (100.0%) |
| threat_bearing | 159 (26.4%) |
| threat_only | 155 (25.7%) |
| mixed_threat_and_operational | 4 (0.7%) |
| operational_only | 228 (37.9%) |
| operational_only.error_or_failure | 206 (34.2%) |
| operational_only.abuse_of_rights | 22 (3.7%) |
| operational_only.other_mix | 0 (0.0%) |
| out_of_scope_only | 0 (0.0%) |
| unknown_only | 215 (35.7%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 159 (100.0%) |
| resolved | 43 (27.0%) |
| rule_dependent | 49 (30.8%) |
| cause_lost | 67 (42.1%) |
| cause_lost.malware_without_enabler | 40 (25.2%) |
| cause_lost.credential_use_without_acquisition | 21 (13.2%) |
| cause_lost.social_without_follow_on | 6 (3.8%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 92 (57.9%) |
| multi_cluster_records | 67 (42.1%) |
| mean_clusters_lower_bound | 1.069 |
| mean_clusters_upper_bound | 1.579 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 14 (2.3%) | 14 (2.3%) |
| #2 | 18 (3.0%) | 49 (8.1%) |
| #3 | 0 (0.0%) | 49 (8.1%) |
| #4 | 44 (7.3%) | 44 (7.3%) |
| #5 | 0 (0.0%) | 0 (0.0%) |
| #6 | 0 (0.0%) | 1 (0.2%) |
| #7 | 55 (9.1%) | 55 (9.1%) |
| #8 | 17 (2.8%) | 17 (2.8%) |
| #9 | 22 (3.7%) | 22 (3.7%) |
| #10 | 0 (0.0%) | 0 (0.0%) |

Records with two or more certain clusters: 24 (4.0%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #4 + #9 | 10 | #9 → #4 |
| #4 + #7 | 6 | #4 → #7 | #7 → #4 |
| #7 + #9 | 6 | #9 → #7 |
| #1 + #4 | 2 | #1 → #4 |
| #1 + #2 | 1 | order unknown |
| #2 + #4 | 1 | #2 → #4 |
| #2 + #7 | 1 | #2 → #7 |
| #2 + #9 | 1 | #9 → #2 |

| attribute.availability.variety | n | DRE |
|---|---|---|
| Loss | 75 | Av |
| Destruction | 8 | Av |
| Obscuration | 27 | Ac |
| Interruption | 6 | A |
| Degradation | 0 | A |
| Acceleration | 0 | A |
| Other | 0 | A |
| Unknown | 1 | A |

| Ransomware records | n (% of ransomware) |
|---|---|
| records | 27 (4.5%) |
| with_obscuration_Ac | 27 (100.0%) |
| with_loss_Av | 0 (0.0%) |
| with_destruction_Av | 0 (0.0%) |
| with_interruption_A | 1 (3.7%) |
| with_no_availability_attribute | 0 (0.0%) |
| with_confirmed_disclosure_C | 21 (77.8%) |

| Unknown collapse | n (% of records) |
|---|---|
| action_unknown | 26 (4.3%) |
| any_unresolved_item | 290 (48.2%) |
| unknown_only | 215 (35.7%) |
| unmapped_values | 0 (0.0%) |

| Category | records | variety Unknown | variety Other |
|---|---|---|---|
| hacking | 295 (49.0%) | 208 (34.6%) | 4 (0.7%) |
| malware | 69 (11.5%) | 15 (2.5%) | 0 (0.0%) |
| social | 26 (4.3%) | 3 (0.5%) | 0 (0.0%) |
| misuse | 31 (5.1%) | 3 (0.5%) | 0 (0.0%) |
| physical | 17 (2.8%) | 0 (0.0%) | 0 (0.0%) |
| error | 209 (34.7%) | 1 (0.2%) | 9 (1.5%) |
| environmental | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

Distinct action-variety signatures: 91 over 584 (97.0%) records with at least one variety

| Most frequent exact variety set | n (% of records) |
|---|---|
| hacking.variety.Unknown | 178 (29.6%) |
| error.variety.Misconfiguration | 141 (23.4%) |
| error.variety.Publishing error | 22 (3.7%) |
| misuse.variety.Privilege abuse | 19 (3.2%) |
| malware.variety.Ransomware | 14 (2.3%) |
| hacking.variety.Use of stolen creds | 14 (2.3%) |
| physical.variety.Theft | 13 (2.2%) |
| hacking.variety.Exploit vuln + hacking.variety.SQLi | 13 (2.2%) |
| error.variety.Other | 9 (1.5%) |
| error.variety.Misdelivery | 9 (1.5%) |

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 139 (23.1%) |
| subset | 3 (0.5%) |
| disjoint | 0 (0.0%) |
| no-attack-edge | 460 (76.4%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.hacking.variety.OS commanding | 2 | #2 | #1, #4, #7 |
| action.malware.variety.Capture stored data | 2 | #7 | #1, #4, #5 |
| action.malware.variety.Packet sniffer | 1 | #7 | #1 |
| action.malware.variety.Scan network | 1 | #7 | #1 |

### Stratum `sub_source:other` — plus.sub_source has another value

Records: 25

| Threat-axis purity | n (% of records) |
|---|---|
| records | 25 (100.0%) |
| threat_bearing | 9 (36.0%) |
| threat_only | 9 (36.0%) |
| mixed_threat_and_operational | 0 (0.0%) |
| operational_only | 14 (56.0%) |
| operational_only.error_or_failure | 12 (48.0%) |
| operational_only.abuse_of_rights | 2 (8.0%) |
| operational_only.other_mix | 0 (0.0%) |
| out_of_scope_only | 0 (0.0%) |
| unknown_only | 2 (8.0%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 9 (100.0%) |
| resolved | 4 (44.4%) |
| rule_dependent | 0 (0.0%) |
| cause_lost | 5 (55.6%) |
| cause_lost.malware_without_enabler | 5 (55.6%) |
| cause_lost.credential_use_without_acquisition | 0 (0.0%) |
| cause_lost.social_without_follow_on | 0 (0.0%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 7 (77.8%) |
| multi_cluster_records | 2 (22.2%) |
| mean_clusters_lower_bound | 1.222 |
| mean_clusters_upper_bound | 1.222 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 0 (0.0%) | 0 (0.0%) |
| #2 | 0 (0.0%) | 0 (0.0%) |
| #3 | 0 (0.0%) | 0 (0.0%) |
| #4 | 0 (0.0%) | 0 (0.0%) |
| #5 | 0 (0.0%) | 0 (0.0%) |
| #6 | 0 (0.0%) | 0 (0.0%) |
| #7 | 7 (28.0%) | 7 (28.0%) |
| #8 | 2 (8.0%) | 2 (8.0%) |
| #9 | 2 (8.0%) | 2 (8.0%) |
| #10 | 0 (0.0%) | 0 (0.0%) |

Records with two or more certain clusters: 2 (8.0%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #7 + #9 | 2 | #9 → #7 |

| attribute.availability.variety | n | DRE |
|---|---|---|
| Loss | 2 | Av |
| Destruction | 0 | Av |
| Obscuration | 6 | Ac |
| Interruption | 0 | A |
| Degradation | 0 | A |
| Acceleration | 0 | A |
| Other | 0 | A |
| Unknown | 0 | A |

| Ransomware records | n (% of ransomware) |
|---|---|
| records | 7 (28.0%) |
| with_obscuration_Ac | 6 (85.7%) |
| with_loss_Av | 0 (0.0%) |
| with_destruction_Av | 0 (0.0%) |
| with_interruption_A | 0 (0.0%) |
| with_no_availability_attribute | 1 (14.3%) |
| with_confirmed_disclosure_C | 5 (71.4%) |

| Unknown collapse | n (% of records) |
|---|---|
| action_unknown | 0 (0.0%) |
| any_unresolved_item | 7 (28.0%) |
| unknown_only | 2 (8.0%) |
| unmapped_values | 0 (0.0%) |

| Category | records | variety Unknown | variety Other |
|---|---|---|---|
| hacking | 3 (12.0%) | 3 (12.0%) | 0 (0.0%) |
| malware | 7 (28.0%) | 0 (0.0%) | 0 (0.0%) |
| social | 2 (8.0%) | 0 (0.0%) | 0 (0.0%) |
| misuse | 2 (8.0%) | 0 (0.0%) | 0 (0.0%) |
| physical | 2 (8.0%) | 0 (0.0%) | 0 (0.0%) |
| error | 12 (48.0%) | 0 (0.0%) | 0 (0.0%) |
| environmental | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

Distinct action-variety signatures: 11 over 25 (100.0%) records with at least one variety

| Most frequent exact variety set | n (% of records) |
|---|---|
| error.variety.Publishing error | 4 (16.0%) |
| error.variety.Misconfiguration | 4 (16.0%) |
| malware.variety.Ransomware | 4 (16.0%) |
| error.variety.Misdelivery | 3 (12.0%) |
| physical.variety.Theft | 2 (8.0%) |
| hacking.variety.Unknown | 2 (8.0%) |
| malware.variety.Ransomware + social.variety.Phishing | 2 (8.0%) |
| misuse.variety.Privilege abuse | 1 (4.0%) |
| error.variety.Classification error | 1 (4.0%) |
| hacking.variety.Unknown + malware.variety.Ransomware | 1 (4.0%) |

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 7 (28.0%) |
| subset | 0 (0.0%) |
| disjoint | 0 (0.0%) |
| no-attack-edge | 18 (72.0%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
