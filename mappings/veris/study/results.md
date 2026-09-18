# VCDB study results

Generated 2026-09-18T15:53:59Z from VCDB commit `230cf22b56a481dd1a994b21e4d94c59e2bccea9` (10047 records, sha256 `e4be5dd432ccfad16520a6b60dd83e9d47c63b0f3352c26c4d43a5dd774c32c0`), mapping updated 2026-09-18.

Every cell is n (percentage of the row's denominator). Strata follow the VCDB README's warning that `phidbr` and `priority` records are not randomly selected.

### Stratum `all` — every record in the joined dataset

Records: 10047

| Threat-axis purity | n (% of records) |
|---|---|
| records | 10047 (100.0%) |
| threat_bearing | 5632 (56.1%) |
| threat_only | 5464 (54.4%) |
| mixed_threat_and_operational | 168 (1.7%) |
| operational_only | 2615 (26.0%) |
| operational_only.error_or_failure | 2578 (25.7%) |
| operational_only.abuse_of_rights | 33 (0.3%) |
| operational_only.other_mix | 2 (0.0%) |
| out_of_scope_only | 2 (0.0%) |
| unknown_only | 1800 (17.9%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 5632 (100.0%) |
| resolved | 3546 (63.0%) |
| rule_dependent | 1310 (23.3%) |
| cause_lost | 776 (13.8%) |
| cause_lost.malware_without_enabler | 422 (7.5%) |
| cause_lost.credential_use_without_acquisition | 206 (3.7%) |
| cause_lost.social_without_follow_on | 148 (2.6%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 3912 (69.5%) |
| multi_cluster_records | 1720 (30.5%) |
| mean_clusters_lower_bound | 1.078 |
| mean_clusters_upper_bound | 1.676 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 1748 (17.4%) | 2497 (24.9%) |
| #2 | 145 (1.4%) | 1289 (12.8%) |
| #3 | 14 (0.1%) | 1291 (12.8%) |
| #4 | 505 (5.0%) | 505 (5.0%) |
| #5 | 11 (0.1%) | 11 (0.1%) |
| #6 | 0 (0.0%) | 166 (1.7%) |
| #7 | 1482 (14.8%) | 1483 (14.8%) |
| #8 | 1593 (15.9%) | 1593 (15.9%) |
| #9 | 573 (5.7%) | 587 (5.8%) |
| #10 | 0 (0.0%) | 18 (0.2%) |

Records with two or more certain clusters: 541 (5.4%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #7 + #9 | 251 | #9 → #7 |
| #4 + #9 | 201 | #9 → #4 |
| #4 + #7 | 136 | #4 → #7 | #7 → #4 |
| #1 + #9 | 67 | #9 → #1 |
| #1 + #8 | 54 | order unknown |
| #1 + #4 | 17 | #1 → #4 |
| #8 + #9 | 13 | #9 → #8 |
| #1 + #7 | 10 | #1 → #7 |
| #4 + #8 | 10 | #8 → #4 |
| #2 + #7 | 9 | #2 → #7 |

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
| any_unresolved_item | 3255 (32.4%) |
| unknown_only | 1800 (17.9%) |
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

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 2120 (21.1%) |
| subset | 288 (2.9%) |
| disjoint | 9 (0.1%) |
| no-attack-edge | 7630 (75.9%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.malware.variety.Capture stored data | 187 | #7 | #1, #4, #5 |
| action.malware.variety.Scan network | 106 | #7 | #1 |
| action.hacking.variety.Forced browsing | 19 | #2 | #1, #7 |
| action.malware.variety.Packet sniffer | 7 | #7 | #1 |
| action.hacking.variety.Buffer overflow | 5 | #2 | #3, #7 |
| action.hacking.variety.OS commanding | 4 | #2 | #1, #4, #7 |
| action.hacking.variety.Cryptanalysis | 3 | #5 | #1, #7 |
| action.hacking.variety.Session prediction | 1 | #2 | #1, #4 |
| action.malware.variety.DoS | 1 | #7 | #1, #2, #6 |

### Stratum `year:<=2014` — timeline.incident.year <= 2014

Records: 5684

| Threat-axis purity | n (% of records) |
|---|---|
| records | 5684 (100.0%) |
| threat_bearing | 2869 (50.5%) |
| threat_only | 2779 (48.9%) |
| mixed_threat_and_operational | 90 (1.6%) |
| operational_only | 1612 (28.4%) |
| operational_only.error_or_failure | 1591 (28.0%) |
| operational_only.abuse_of_rights | 17 (0.3%) |
| operational_only.other_mix | 2 (0.0%) |
| out_of_scope_only | 2 (0.0%) |
| unknown_only | 1203 (21.2%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 2869 (100.0%) |
| resolved | 2315 (80.7%) |
| rule_dependent | 380 (13.2%) |
| cause_lost | 174 (6.1%) |
| cause_lost.malware_without_enabler | 88 (3.1%) |
| cause_lost.credential_use_without_acquisition | 55 (1.9%) |
| cause_lost.social_without_follow_on | 31 (1.1%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 2270 (79.1%) |
| multi_cluster_records | 599 (20.9%) |
| mean_clusters_lower_bound | 1.108 |
| mean_clusters_upper_bound | 1.382 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 1140 (20.1%) | 1140 (20.1%) |
| #2 | 93 (1.6%) | 368 (6.5%) |
| #3 | 8 (0.1%) | 370 (6.5%) |
| #4 | 231 (4.1%) | 231 (4.1%) |
| #5 | 11 (0.2%) | 11 (0.2%) |
| #6 | 0 (0.0%) | 127 (2.2%) |
| #7 | 324 (5.7%) | 324 (5.7%) |
| #8 | 1065 (18.7%) | 1065 (18.7%) |
| #9 | 307 (5.4%) | 316 (5.6%) |
| #10 | 0 (0.0%) | 12 (0.2%) |

Records with two or more certain clusters: 335 (5.9%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #7 + #9 | 209 | #9 → #7 |
| #4 + #9 | 121 | #9 → #4 |
| #4 + #7 | 114 | #4 → #7 | #7 → #4 |
| #1 + #9 | 40 | #9 → #1 |
| #1 + #8 | 25 | order unknown |
| #1 + #4 | 10 | #1 → #4 |
| #8 + #9 | 9 | #9 → #8 |
| #1 + #7 | 7 | #1 → #7 |
| #5 + #7 | 7 | #5 → #7 |
| #5 + #9 | 7 | #9 → #5 |

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
| any_unresolved_item | 2067 (36.4%) |
| unknown_only | 1203 (21.2%) |
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

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 481 (8.5%) |
| subset | 243 (4.3%) |
| disjoint | 6 (0.1%) |
| no-attack-edge | 4954 (87.2%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.malware.variety.Capture stored data | 174 | #7 | #1, #4, #5 |
| action.malware.variety.Scan network | 105 | #7 | #1 |
| action.hacking.variety.Forced browsing | 8 | #2 | #1, #7 |
| action.malware.variety.Packet sniffer | 6 | #7 | #1 |
| action.hacking.variety.Buffer overflow | 3 | #2 | #3, #7 |
| action.hacking.variety.Cryptanalysis | 3 | #5 | #1, #7 |
| action.hacking.variety.Session prediction | 1 | #2 | #1, #4 |
| action.malware.variety.DoS | 1 | #7 | #1, #2, #6 |

### Stratum `year:2015-2019` — timeline.incident.year in 2015..2019

Records: 3046

| Threat-axis purity | n (% of records) |
|---|---|
| records | 3046 (100.0%) |
| threat_bearing | 1701 (55.8%) |
| threat_only | 1625 (53.3%) |
| mixed_threat_and_operational | 76 (2.5%) |
| operational_only | 855 (28.1%) |
| operational_only.error_or_failure | 841 (27.6%) |
| operational_only.abuse_of_rights | 14 (0.5%) |
| operational_only.other_mix | 0 (0.0%) |
| out_of_scope_only | 0 (0.0%) |
| unknown_only | 490 (16.1%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 1701 (100.0%) |
| resolved | 1162 (68.3%) |
| rule_dependent | 145 (8.5%) |
| cause_lost | 394 (23.2%) |
| cause_lost.malware_without_enabler | 223 (13.1%) |
| cause_lost.credential_use_without_acquisition | 55 (3.2%) |
| cause_lost.social_without_follow_on | 116 (6.8%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 1397 (82.1%) |
| multi_cluster_records | 304 (17.9%) |
| mean_clusters_lower_bound | 1.069 |
| mean_clusters_upper_bound | 1.228 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 581 (19.1%) | 583 (19.1%) |
| #2 | 48 (1.6%) | 136 (4.5%) |
| #3 | 5 (0.2%) | 136 (4.5%) |
| #4 | 153 (5.0%) | 153 (5.0%) |
| #5 | 0 (0.0%) | 0 (0.0%) |
| #6 | 0 (0.0%) | 37 (1.2%) |
| #7 | 280 (9.2%) | 281 (9.2%) |
| #8 | 515 (16.9%) | 515 (16.9%) |
| #9 | 237 (7.8%) | 242 (7.9%) |
| #10 | 0 (0.0%) | 6 (0.2%) |

Records with two or more certain clusters: 173 (5.7%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #4 + #9 | 61 | #9 → #4 |
| #7 + #9 | 31 | #9 → #7 |
| #1 + #8 | 28 | order unknown |
| #1 + #9 | 27 | #9 → #1 |
| #4 + #7 | 17 | #4 → #7 | #7 → #4 |
| #1 + #4 | 6 | #1 → #4 |
| #4 + #8 | 4 | #8 → #4 |
| #8 + #9 | 4 | #9 → #8 |
| #1 + #7 | 3 | #1 → #7 |
| #2 + #7 | 3 | #2 → #7 |

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
| any_unresolved_item | 969 (31.8%) |
| unknown_only | 490 (16.1%) |
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

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 612 (20.1%) |
| subset | 42 (1.4%) |
| disjoint | 3 (0.1%) |
| no-attack-edge | 2389 (78.4%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.malware.variety.Capture stored data | 12 | #7 | #1, #4, #5 |
| action.hacking.variety.Forced browsing | 11 | #2 | #1, #7 |
| action.hacking.variety.OS commanding | 4 | #2 | #1, #4, #7 |
| action.hacking.variety.Buffer overflow | 2 | #2 | #3, #7 |
| action.malware.variety.Packet sniffer | 1 | #7 | #1 |
| action.malware.variety.Scan network | 1 | #7 | #1 |

### Stratum `year:2020-2026` — timeline.incident.year in 2020..2026

Records: 1317

| Threat-axis purity | n (% of records) |
|---|---|
| records | 1317 (100.0%) |
| threat_bearing | 1062 (80.6%) |
| threat_only | 1060 (80.5%) |
| mixed_threat_and_operational | 2 (0.2%) |
| operational_only | 148 (11.2%) |
| operational_only.error_or_failure | 146 (11.1%) |
| operational_only.abuse_of_rights | 2 (0.2%) |
| operational_only.other_mix | 0 (0.0%) |
| out_of_scope_only | 0 (0.0%) |
| unknown_only | 107 (8.1%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 1062 (100.0%) |
| resolved | 69 (6.5%) |
| rule_dependent | 785 (73.9%) |
| cause_lost | 208 (19.6%) |
| cause_lost.malware_without_enabler | 111 (10.5%) |
| cause_lost.credential_use_without_acquisition | 96 (9.0%) |
| cause_lost.social_without_follow_on | 1 (0.1%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 245 (23.1%) |
| multi_cluster_records | 817 (76.9%) |
| mean_clusters_lower_bound | 1.01 |
| mean_clusters_upper_bound | 3.189 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 27 (2.1%) | 774 (58.8%) |
| #2 | 4 (0.3%) | 785 (59.6%) |
| #3 | 1 (0.1%) | 785 (59.6%) |
| #4 | 121 (9.2%) | 121 (9.2%) |
| #5 | 0 (0.0%) | 0 (0.0%) |
| #6 | 0 (0.0%) | 2 (0.2%) |
| #7 | 878 (66.7%) | 878 (66.7%) |
| #8 | 13 (1.0%) | 13 (1.0%) |
| #9 | 29 (2.2%) | 29 (2.2%) |
| #10 | 0 (0.0%) | 0 (0.0%) |

Records with two or more certain clusters: 33 (2.5%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #4 + #9 | 19 | #9 → #4 |
| #7 + #9 | 11 | #9 → #7 |
| #4 + #7 | 5 | #4 → #7 | #7 → #4 |
| #1 + #4 | 1 | #1 → #4 |
| #1 + #8 | 1 | order unknown |

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
| threat_bearing | 4679 (57.7%) |
| threat_only | 4549 (56.1%) |
| mixed_threat_and_operational | 130 (1.6%) |
| operational_only | 1993 (24.6%) |
| operational_only.error_or_failure | 1967 (24.3%) |
| operational_only.abuse_of_rights | 22 (0.3%) |
| operational_only.other_mix | 2 (0.0%) |
| out_of_scope_only | 2 (0.0%) |
| unknown_only | 1438 (17.7%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 4679 (100.0%) |
| resolved | 2911 (62.2%) |
| rule_dependent | 1246 (26.6%) |
| cause_lost | 522 (11.2%) |
| cause_lost.malware_without_enabler | 258 (5.5%) |
| cause_lost.credential_use_without_acquisition | 162 (3.5%) |
| cause_lost.social_without_follow_on | 102 (2.2%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 3113 (66.5%) |
| multi_cluster_records | 1566 (33.5%) |
| mean_clusters_lower_bound | 1.076 |
| mean_clusters_upper_bound | 1.774 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 1340 (16.5%) | 2089 (25.8%) |
| #2 | 120 (1.5%) | 1231 (15.2%) |
| #3 | 12 (0.1%) | 1233 (15.2%) |
| #4 | 397 (4.9%) | 397 (4.9%) |
| #5 | 11 (0.1%) | 11 (0.1%) |
| #6 | 0 (0.0%) | 164 (2.0%) |
| #7 | 1281 (15.8%) | 1282 (15.8%) |
| #8 | 1419 (17.5%) | 1419 (17.5%) |
| #9 | 454 (5.6%) | 462 (5.7%) |
| #10 | 0 (0.0%) | 12 (0.1%) |

Records with two or more certain clusters: 442 (5.5%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #7 + #9 | 231 | #9 → #7 |
| #4 + #9 | 159 | #9 → #4 |
| #4 + #7 | 124 | #4 → #7 | #7 → #4 |
| #1 + #9 | 58 | #9 → #1 |
| #1 + #8 | 44 | order unknown |
| #1 + #4 | 14 | #1 → #4 |
| #8 + #9 | 12 | #9 → #8 |
| #1 + #7 | 10 | #1 → #7 |
| #4 + #8 | 9 | #8 → #4 |
| #2 + #7 | 7 | #2 → #7 |

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
| any_unresolved_item | 2615 (32.2%) |
| unknown_only | 1438 (17.7%) |
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

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 1732 (21.4%) |
| subset | 284 (3.5%) |
| disjoint | 8 (0.1%) |
| no-attack-edge | 6086 (75.0%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.malware.variety.Capture stored data | 182 | #7 | #1, #4, #5 |
| action.malware.variety.Scan network | 105 | #7 | #1 |
| action.hacking.variety.Forced browsing | 15 | #2 | #1, #7 |
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
| threat_bearing | 757 (57.8%) |
| threat_only | 725 (55.3%) |
| mixed_threat_and_operational | 32 (2.4%) |
| operational_only | 403 (30.8%) |
| operational_only.error_or_failure | 393 (30.0%) |
| operational_only.abuse_of_rights | 10 (0.8%) |
| operational_only.other_mix | 0 (0.0%) |
| out_of_scope_only | 0 (0.0%) |
| unknown_only | 150 (11.5%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 757 (100.0%) |
| resolved | 559 (73.8%) |
| rule_dependent | 15 (2.0%) |
| cause_lost | 183 (24.2%) |
| cause_lost.malware_without_enabler | 119 (15.7%) |
| cause_lost.credential_use_without_acquisition | 24 (3.2%) |
| cause_lost.social_without_follow_on | 40 (5.3%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 673 (88.9%) |
| multi_cluster_records | 84 (11.1%) |
| mean_clusters_lower_bound | 1.09 |
| mean_clusters_upper_bound | 1.124 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 367 (28.0%) | 367 (28.0%) |
| #2 | 5 (0.4%) | 9 (0.7%) |
| #3 | 0 (0.0%) | 9 (0.7%) |
| #4 | 64 (4.9%) | 64 (4.9%) |
| #5 | 0 (0.0%) | 0 (0.0%) |
| #6 | 0 (0.0%) | 1 (0.1%) |
| #7 | 139 (10.6%) | 139 (10.6%) |
| #8 | 155 (11.8%) | 155 (11.8%) |
| #9 | 95 (7.3%) | 101 (7.7%) |
| #10 | 0 (0.0%) | 6 (0.5%) |

Records with two or more certain clusters: 71 (5.4%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #4 + #9 | 32 | #9 → #4 |
| #7 + #9 | 12 | #9 → #7 |
| #1 + #8 | 10 | order unknown |
| #1 + #9 | 9 | #9 → #1 |
| #4 + #7 | 6 | #4 → #7 | #7 → #4 |
| #1 + #4 | 1 | #1 → #4 |
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
| unknown_only | 150 (11.5%) |
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

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 242 (18.5%) |
| subset | 1 (0.1%) |
| disjoint | 1 (0.1%) |
| no-attack-edge | 1066 (81.4%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.malware.variety.Capture stored data | 3 | #7 | #1, #4, #5 |
| action.hacking.variety.Forced browsing | 2 | #2 | #1, #7 |
| action.hacking.variety.Buffer overflow | 1 | #2 | #3, #7 |

### Stratum `sub_source:priority` — plus.sub_source = priority (selected on purpose)

Records: 602

| Threat-axis purity | n (% of records) |
|---|---|
| records | 602 (100.0%) |
| threat_bearing | 185 (30.7%) |
| threat_only | 180 (29.9%) |
| mixed_threat_and_operational | 5 (0.8%) |
| operational_only | 207 (34.4%) |
| operational_only.error_or_failure | 206 (34.2%) |
| operational_only.abuse_of_rights | 1 (0.2%) |
| operational_only.other_mix | 0 (0.0%) |
| out_of_scope_only | 0 (0.0%) |
| unknown_only | 210 (34.9%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 185 (100.0%) |
| resolved | 70 (37.8%) |
| rule_dependent | 49 (26.5%) |
| cause_lost | 66 (35.7%) |
| cause_lost.malware_without_enabler | 40 (21.6%) |
| cause_lost.credential_use_without_acquisition | 20 (10.8%) |
| cause_lost.social_without_follow_on | 6 (3.2%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 117 (63.2%) |
| multi_cluster_records | 68 (36.8%) |
| mean_clusters_lower_bound | 1.076 |
| mean_clusters_upper_bound | 1.492 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 39 (6.5%) | 39 (6.5%) |
| #2 | 20 (3.3%) | 49 (8.1%) |
| #3 | 2 (0.3%) | 49 (8.1%) |
| #4 | 44 (7.3%) | 44 (7.3%) |
| #5 | 0 (0.0%) | 0 (0.0%) |
| #6 | 0 (0.0%) | 1 (0.2%) |
| #7 | 55 (9.1%) | 55 (9.1%) |
| #8 | 17 (2.8%) | 17 (2.8%) |
| #9 | 22 (3.7%) | 22 (3.7%) |
| #10 | 0 (0.0%) | 0 (0.0%) |

Records with two or more certain clusters: 26 (4.3%)

| Pair | n | ordering hypothesis |
|---|---|---|
| #4 + #9 | 10 | #9 → #4 |
| #4 + #7 | 6 | #4 → #7 | #7 → #4 |
| #7 + #9 | 6 | #9 → #7 |
| #1 + #4 | 2 | #1 → #4 |
| #2 + #4 | 2 | #2 → #4 |
| #2 + #7 | 1 | #2 → #7 |
| #2 + #9 | 1 | #9 → #2 |
| #3 + #4 | 1 | #3 → #4 |
| #3 + #7 | 1 | #3 → #7 |
| #3 + #9 | 1 | #9 → #3 |

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
| unknown_only | 210 (34.9%) |
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

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 139 (23.1%) |
| subset | 3 (0.5%) |
| disjoint | 0 (0.0%) |
| no-attack-edge | 460 (76.4%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
| action.hacking.variety.Forced browsing | 2 | #2 | #1, #7 |
| action.hacking.variety.OS commanding | 2 | #2 | #1, #4, #7 |
| action.malware.variety.Capture stored data | 2 | #7 | #1, #4, #5 |
| action.hacking.variety.Session prediction | 1 | #2 | #1, #4 |
| action.malware.variety.Packet sniffer | 1 | #7 | #1 |
| action.malware.variety.Scan network | 1 | #7 | #1 |

### Stratum `sub_source:other` — plus.sub_source has another value

Records: 25

| Threat-axis purity | n (% of records) |
|---|---|
| records | 25 (100.0%) |
| threat_bearing | 11 (44.0%) |
| threat_only | 10 (40.0%) |
| mixed_threat_and_operational | 1 (4.0%) |
| operational_only | 12 (48.0%) |
| operational_only.error_or_failure | 12 (48.0%) |
| operational_only.abuse_of_rights | 0 (0.0%) |
| operational_only.other_mix | 0 (0.0%) |
| out_of_scope_only | 0 (0.0%) |
| unknown_only | 2 (8.0%) |
| empty | 0 (0.0%) |

| Cause recoverability (threat-bearing records) | n (% of threat-bearing) |
|---|---|
| threat_bearing | 11 (100.0%) |
| resolved | 6 (54.5%) |
| rule_dependent | 0 (0.0%) |
| cause_lost | 5 (45.5%) |
| cause_lost.malware_without_enabler | 5 (45.5%) |
| cause_lost.credential_use_without_acquisition | 0 (0.0%) |
| cause_lost.social_without_follow_on | 0 (0.0%) |
| cause_lost.interception_without_position | 0 (0.0%) |
| single_cluster_records | 9 (81.8%) |
| multi_cluster_records | 2 (18.2%) |
| mean_clusters_lower_bound | 1.182 |
| mean_clusters_upper_bound | 1.182 |

| Cluster | certain | upper bound |
|---|---|---|
| #1 | 2 (8.0%) | 2 (8.0%) |
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

| ATT&CK-transitive agreement | n (% of records) |
|---|---|
| agree | 7 (28.0%) |
| subset | 0 (0.0%) |
| disjoint | 0 (0.0%) |
| no-attack-edge | 18 (72.0%) |

| VERIS value | disagreeing records | direct | transitive |
|---|---|---|---|
