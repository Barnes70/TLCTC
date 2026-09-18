# VERIS → TLCTC Classification Decision Tree

How a VERIS 1.4.1 enumeration value was assigned its `mapping_type` and target in
`tlctc-veris.json`, and how to classify a value the mapping does not know (a future VERIS
enumeration). Clusters, axioms and rules are cited by id from the v2.5 dictionary; nothing here
redefines them.

## Q0 — Which VERIS field is it?

```
attribute.*                     → outcome (Axiom III). Go to Q4.
action.<cat>.result.*           → outcome, no DRE: results say what a step achieved, not what it exploited.
action.<cat>.vector.*           → context (no cluster). Go to Q3.
action.<cat>.variety.*          → Q1.
action.unknown                  → unresolved.
```

## Q1 — Is the action a threat at all? (cause-side partition, R-SCOPE)

Ask the partition's three questions in order:

```
Is there an actor?
  no  → no-cluster, partition_row = failure          (environmental.*; error Malfunction, Capacity shortage,
                                                     Misconfiguration, Programming error)
Did the actor intend the outcome?
  no  → no-cluster, partition_row = error_in_use      (all other error.* varieties, incl. Other/Unknown)
Did an accountable grantor confer an entitlement covering THIS action?
  yes → no-cluster, partition_row = abuse_of_rights   (every misuse.* variety except Password or
                                                     Session Sharing and Evade Defenses)
  no  → the Attack row. Is there an IT-system step?
          no  → no-cluster, partition_row = attack, out_of_scope   (social Extortion, Propaganda;
                                                                   physical Assault; hacking Reverse engineering)
          yes → Q2.
```

VERIS defines misuse as entrusted resources or privileges used contrary to their intended
purpose: the actor is inside an entitlement a grantor genuinely conferred and acts against its
purpose. That is Abuse of Rights by definition (R-SCOPE; the dictionary's own examples are an
administrator using genuine root to exfiltrate and a badge holder propping open a door), so
`Privilege abuse`, `Possession abuse`, `Knowledge abuse`, `Data mishandling`, `Snap picture` and
the policy-violation varieties all land on that row. An insider who reaches *past* the conferred
envelope is #1, but VERIS would code that as hacking, not misuse. `Password or Session Sharing`
is the exception: the borrower authenticates as someone else (#4, R-CRED); the sharer's act is
the Abuse of Rights.

`Other` / `Unknown` in a threat-bearing category (hacking, malware, social, misuse, physical)
→ **unresolved**: the record says something happened without saying what.

`Evade Defenses` (in every category) → **outcome**: a property of how a step was carried out,
not a step of its own.

## Q2 — Which generic vulnerability? (the cluster questions, in order)

Walk the questions in this order and stop at the first that applies to the *value as VERIS
describes it*. Where the description leaves a rule open, the entry is **conditional** with one
target per branch; where the rules require a step VERIS does not record, the entry is **chain**.

```
Q2.1 Does the value describe foreign executable content running?              (R-EXEC)
       every malware.variety                     → chain #7, companion BEFORE = the enabling cluster
         except: DoS (#7 with availability DRE), AitM / Packet sniffer (#7 then #5, R-MITM),
                 Exploit vuln (conditional #2 | #3, the enabler of #7), Exploit misconfig (chain #1 → #7),
                 Client-side attack (conditional #3 | #7), Brute force / Pass-the-hash (#7 → #4, R-CRED),
                 Adminware (conditional #1 | #7)
       hacking Backdoor                          → conditional #1 (designed function left open) | #7 (implant)
       hacking RFI, Insecure deserialization     → chain #2 → #7 (the loaded code executes)

Q2.2 Does the value describe authenticating as an identity that is not the presenter's own?   (R-CRED, Axiom X)
       Use of stolen creds, Pass-the-hash, Session replay, Offline cracking   → chain #4, companion BEFORE = acquisition
       Brute force, Session fixation, Session prediction                       → direct #4 (guessing or fixing the
                                                                                 identifier is preparation; its use is #4)
       misuse Password or Session Sharing                                      → chain #4 (the sharer's act is Abuse of Rights)

Q2.3 Does the value describe manipulating a person?
       every social.variety                     → chain #9, companion AFTER = the technical follow-on (#4, #7 or #1)
         except: Forgery (conditional #9 | #10 at a Trust Acceptance Event, R-SUPPLY)

Q2.4 Does the value describe interception, relay or a channel-control defect?  (R-MITM, R-CHANNEL)
       hacking AitM                             → chain #5, companion BEFORE = position acquisition
       Routing detour                           → chain #2 → #5 (a server-role routing flaw gains the position)
       Hijack                                   → chain #1 → #5 | #4 (a designed process is taken over, then used)
       Cryptanalysis                            → direct #5 (R-CHANNEL)

Q2.5 Does the value describe exhausting capacity?                              (R-FLOOD)
       DoS                                      → conditional #6 (volume) | #2 | #3 (defect, by R-ROLE)
       XML entity expansion, XML attribute blowup → direct #6 (intensity exhausting finite capacity)

Q2.6 Does the value describe exploiting a code flaw?                           (R-ROLE)
       Exploit vuln                             → conditional #2 (server role) | #3 (client role)
       its children                             → direct #2 with role_hint server (aligned with the CWE mapping)
         except XSS                             → conditional #2 (stored/reflected) | #3 (DOM-based)
       Virtual machine escape, User breakout    → direct #2 (the platform serves the tenant; |[hypervisor]| is an
                                                  annotation only, R-INTRA-7)

Q2.7 Does the value describe using a designed function beyond its purpose?
       Abuse of functionality, Exploit misconfig, Disable controls, Profile host, Scan network,
       Prompt injection, CSRF, URL redirector abuse, Forced browsing, Cache poisoning   → direct #1
       (the last four are children of Exploit vuln in VERIS but abuse designed functions with no
        code flaw: CWE-352, CWE-601, CWE-425, CWE-349 in the repository's CWE mapping)

Q2.8 Does the value describe acting on the physical substrate?                 (R-SUBSTRATE)
       every physical.variety                   → direct #8; sub_cluster_hint 8.1 (mechanical) or
                                                  8.2 (signal: Wiretapping, Surveillance, Snooping)
```

The order matters only where a value could satisfy two questions; VERIS descriptions are
usually specific enough that one applies. When a new VERIS value appears, place it by the
first question its description satisfies and record the rule in `targets[].rule`.

## Q3 — Vectors: what does the channel tell us?

```
Partner (hacking, malware, social)     → boundary @Vendor→@Org; #10 only if a trust artefact was honoured (R-SUPPLY),
                                         otherwise the partner is a transit carrier (⇒)
Software update (malware)              → boundary_context update; R-SUPPLY: #10 at the Trust Acceptance Event
Email*, IM, SMS, Phone, Social media, In-person, Documents, Virtual meeting, Removable media (social)
                                       → boundary_context human (the #9 step's context)
Email autoexecute, Web application - drive-by (malware)
                                       → role_hint client (#3 enabler, R-ROLE)
Web application (hacking), VPN, Desktop sharing*, Other network service
                                       → role_hint server (#2 | #3 resolves to #2 here)
Physical access, physical.* vectors    → boundary_context physical
Hypervisor, Inter-tenant               → intra_system_boundary (R-INTRA-7: annotation, never a classification input)
Backdoor, C2, Command shell            → note: a channel established by an earlier step; classify that step
Direct install, Download by malware, Network propagation, Remote injection
                                       → note: the sequence the vector implies (#1 → #7, #7 → #7, #2/#3/#4 → #7, #2 → #7)
error.* vectors                        → note: contributing condition of an error (operational-risk register)
Other, Unknown                         → unresolved
```

## Q4 — Outcomes: which Data Risk Event?

```
confidentiality.data_disclosure  Yes → C;  Potentially → C (certainty: potential);  No, Unknown → none
integrity.variety                Misrepresentation, Fraudulent transaction → If (attribution failed)
                                 Alter behavior → none (a person, not a record)
                                 Hardware tampering, Repurpose → none (a system-altitude event, not a data state)
                                 Other, Unknown → I (refinement unknown)
                                 everything else → Ii (the record no longer corresponds to its intended state)
availability.variety             Obscuration → Ac;  Loss, Destruction → Av;  Interruption, Degradation, Acceleration,
                                 Other, Unknown → A (the record does not say whether the data is absent or unusable)
```

The stopping rule of the dictionary's `data_risk_events` applies: refinements are told apart by
inspecting the record, never by who caused it.

## Worked examples

**VCDB record with `social.Phishing` + `hacking.Use of stolen creds` + `data_disclosure = Yes`.**
Q0 → varieties. Q1 → attack row, IT-system steps present. Q2.3 → Phishing is chain #9 (follow-on
after); Q2.2 → Use of stolen creds is chain #4 (acquisition before). Each chain's companion is
recorded by the other value, so nothing is lost. Outcome: C. Certain clusters {#4, #9};
hypothesis from the companion rules: `#9 → #4 + [DRE: C]`.

**VCDB record with `malware.Ransomware` alone, no availability attribute.**
Q2.1 → chain #7, enabler before; no other value records it → `missing: before`. No DRE beyond
what `data_disclosure` says. Honest rendering: `? → #7`, and if the confidentiality disclosure
is confirmed, `? → #7 + [DRE: C]`; the encryption is unrecorded, so `Ac` cannot be asserted.

**VCDB record with `error.Misdelivery` + `data_disclosure = Yes`.**
Q1 → an actor acted without intending the outcome: error_in_use, no cluster. Outcome C is
recorded; the record is operational risk, off the threat axis, and its DRE is counted with the
partition row, not with a cluster.

**VCDB record with `misuse.Privilege abuse` + `data_disclosure = Yes`.**
Q1 → an entitled actor acted intentionally against the purpose of the grant: abuse_of_rights,
no cluster, no SRE. Outcome C is recorded and the consequence chain starts there. Had the
sources shown the insider reaching a system or record the grant never covered, the step would
be #1; VERIS's `misuse` category asserts the former.

**VCDB record with `hacking.Exploit vuln` + `hacking.vector.Web application`.**
Q2.6 → conditional #2 | #3. Q3 → the vector's role hint is server, so an analyst resolving the
group by R-ROLE would choose #2; the classifier reports the group and the hint and leaves the
decision to the analyst.
