# Fixture selection

Twenty records from the VCDB joined dataset at commit `230cf22b56a481dd1a994b21e4d94c59e2bccea9` (10,047 records, sorted by `incident_id`).
For each predicate below, the first record in that order that satisfies it and was not already chosen. Re-running
`select-fixtures.py` against the same snapshot reproduces the same twenty files.

| # | Predicate | incident_id | schema_version |
|---|---|---|---|
| 1 | hacking only | `0012CC25-9167-40D8-8FE3-3D0DFD8FB6BB` | 1.4.0 |
| 2 | malware only | `0190acb0-b476-11e9-b6ed-d1eb4820968c` | 1.4.0 |
| 3 | social only | `000ab490-a4a9-11e8-b571-7db57cad93dd` | 1.4.0 |
| 4 | misuse only | `0000617D-276E-4AAE-9787-08D1C7EB1AFB` | 1.4.0 |
| 5 | physical only | `0008DADB-E83D-4278-A19A-CEE01610CF43` | 1.4.0 |
| 6 | error only | `000D403E-2DC9-4EA7-9294-BD3938D1C3C7` | 1.4.0 |
| 7 | environmental only | `1B19DDC2-A883-423A-A9DC-486F19130EFE` | 1.4.0 |
| 8 | unknown only | `016F24DF-547E-43B0-BBC7-2F44885F8537` | 1.4.0 |
| 9 | social + hacking | `00a2d140-e1da-11e7-8553-197c24c367d2` | 1.4.0 |
| 10 | social + malware | `032C9EBE-C5A4-4BAA-B096-5C7C7855E0AA` | 1.4.0 |
| 11 | hacking + malware | `00392c50-0bf6-11ec-9c8a-d72b813bc8ca` | 1.4.0 |
| 12 | three action categories | `011E42B7-DF7F-4D2E-BB85-24A0DD159C64` | 1.4.0 |
| 13 | availability Obscuration | `01156af0-149b-11ec-92c0-8d3c636e1e37` | 1.4.0 |
| 14 | hacking Use of stolen creds | `02E74F10-E032-7AD8-68D1-38F2B4FDD6F0` | 1.4.1 |
| 15 | Partner vector | `0E308D20-5149-4820-BBDD-72657365DE2E` | 1.3.7 |
| 16 | data_disclosure Potentially | `002599D4-A872-433B-9980-BD9F257B283F` | 1.4.0 |
| 17 | schema_version 1.3.x | `12A05887-6463-48A9-A2CD-7C958C5D31D1` | 1.3.7 |
| 18 | plus.sub_source phidbr | `00204495-81A8-4D51-B4FE-896AA0F89DA2` | 1.4.0 |
| 19 | plus.sub_source priority | `009b2f20-0b66-11e8-827c-bba53cbad290` | 1.4.0 |
| 20 | Ransomware with Loss (not Obscuration) | `230092F0-C4CC-422B-B3AA-92AD5AFB53C8` | 1.4.0 |
