# Reading an RSIT-tagged record by cause

An analyst holds a ticket, an incident or an indicator tagged with an RSIT value. Three questions,
in order, give the TLCTC reading. The verdict for every value is in `tlctc-rsit.json`; this page
is the walk.

## 1. Is it an event against an IT system at all?

| RSIT values | Reading |
|---|---|
| Abusive Content / Harmful Speech, (Child) Sexual Exploitation/Sexual/Violent Content; Fraud / Copyright | No step against an IT system: no cluster. |
| Availability / Outage, Misconfiguration; Information Content Security / Data Loss from a failure | No attacker: Failure row of the cause-side partition, operational risk, no cluster. |
| Fraud / Unauthorised Use of Resources | Ask: was the access legitimately granted? Yes: Abuse of Rights (R-SCOPE), no cluster. No: the use is the outcome of the attack that gained the access. |
| Test / Test | Excluded. |
| Other / Uncategorised, Undetermined | `?` — unresolved, excluded from statistics until the record is understood. |

## 2. Did a step succeed, or is this an attempt, an exposure or infrastructure?

| RSIT class | Reading |
|---|---|
| **Intrusion Attempts** | An attempt: the cluster it would be (#2 \| #3 for exploits, #4 for login attempts). Blocked: a near miss, counted per cluster, never as an incident. Succeeded: reclassify under Intrusions. |
| **Vulnerable** | An exposure: a state, no step. Note the cluster it enables (weak crypto → #5, unwanted services → #4/#1, information disclosure → #1, vulnerable system → #2 \| #3, DDoS amplifier → #6 against third parties). |
| **Malicious Code** C2 Server, Malware Distribution, Malware Configuration; **Abusive Content** Spam | Attacker infrastructure. At the victims it serves #7 (or #9 for spam that carries a lure). |

## 3. Which cluster, and what is still missing?

| RSIT value | Certain | Ask |
|---|---|---|
| Information Gathering / Scanning | #1 | — |
| Information Gathering / Social Engineering | #9 + [DRE: C] | — |
| Intrusions / Burglary | #8 | — |
| Availability / Distributed Denial of Service | #6 + [DRE: A] | — |
| Malicious Code / Infected System | #7 | How did the code arrive and start? (#9, #3, #2, #10, #4 → #1) |
| Intrusions / Unprivileged Account Compromise | #4 | How was the credential obtained? |
| Fraud / Phishing | #9 + [DRE: C] | Were the credentials used? Then #4 follows. |
| Information Gathering / Sniffing | — | Where was the capture point? #1 on a host the attacker uses, #5 on the path |
| Intrusions / Privileged Account Compromise | — | Admin credential (#4), flaw in a privileged component (#2), or designed functions (#1)? |
| Intrusions / Application Compromise | — | Did the application serve the attacker (#2) or consume attacker content (#3)? |
| Intrusions / System Compromise | — | Login (#4), commands through designed functions (#1), or a flaw (#2)? |
| Availability / Denial of Service | — | Capacity (#6) or a defect (#2 \| #3)? |
| Availability / Sabotage | — | Physical (#8), logical by an attacker (#1), or an entitled actor within the grant (Abuse of Rights)? |
| Fraud / Masquerade | — | Were people deceived (#9) or did a system authenticate the impersonator (#4)? |
| Information Content Security / Unauthorised Access, Modification, Data Loss (theft), Leak | — | A data state (C, I, Av, C). Which step caused it? RSIT's own examples name #4, #5, #7, #8. |

A single RSIT tag never yields an attack path: where the question is answered, record the steps in a
TLCTC attack path with the evidence that answered it.
