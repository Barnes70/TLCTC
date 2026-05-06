# MITRE ATT&CK → TLCTC Classification Decision Tree

This document provides the step-by-step methodology for mapping any MITRE ATT&CK Enterprise technique to the correct TLCTC cluster(s).

## Prerequisites

Before classifying, establish two things:

1. **Domain** — Where does this technique execute relative to your organization?
   - `@Org` → proceed with mapping
   - `@AttackerInfra` or `@OtherVictims` → **N/A** (threat potential, not threat)
   - `@3P` → consider **#10** if trust boundary is crossed into your environment

2. **Protected Asset** — Which asset in your scope is affected? TLCTC requires a concrete target; abstract technique descriptions without a target asset cannot be classified.

## The Decision Tree

Walk through these questions **in order**. Stop at the first match.

```
Q1: Is the attacker abusing a DESIGNED function/feature/API/configuration,
    with NO code flaw and NO foreign binary required?
    ├── YES → #1 Abuse of Functions
    │         (e.g., admin tool misuse, API abuse, config manipulation)
    └── NO ↓

Q2: Is the attacker exploiting a CODE IMPLEMENTATION FLAW on the SERVER side?
    ├── YES → #2 Exploiting Server
    │         (e.g., SQL injection, buffer overflow in server app)
    └── NO ↓

Q3: Is the attacker exploiting a CODE IMPLEMENTATION FLAW in a CLIENT role?
    ├── YES → #3 Exploiting Client
    │         (e.g., browser exploit, PDF reader vulnerability)
    └── NO ↓

Q4: Is the attacker's main power that they ACT AS A LEGITIMATE IDENTITY
    using credentials/tokens/keys?
    ├── YES → #4 Identity Theft
    │         (credential APPLICATION — the use, not the acquisition)
    └── NO ↓

Q5: Is the attacker intercepting/modifying/relaying communication
    from a privileged position on the path?
    ├── YES → #5 Man in the Middle
    └── NO ↓

Q6: Is the attacker overwhelming resources through volume or intensity?
    ├── YES → #6 Flooding Attack
    │         (Note: if a code bug causes crash, that's #2/#3, not #6)
    └── NO ↓

Q7: Is FOREIGN CODE being executed?
    ├── YES → #7 Malware
    │         (Note: if launched via legitimate tool → #1 → #7)
    └── NO ↓

Q8: Does the attack require physical interaction with hardware/facilities?
    ├── YES → #8 Physical Attack
    └── NO ↓

Q9: Is the attacker psychologically manipulating a human?
    ├── YES → #9 Social Engineering
    └── NO ↓

Q10: Is the attack exploiting trust in a third-party component/service/update?
     ├── YES → #10 Supply Chain Attack
     └── NO → Re-examine. One of the above must apply.
```

## The Software Quadrant: #1, #2, #3, and #7

Most ATT&CK techniques fall into the "software" space. This disambiguation handles the majority:

```
START: Is there a CODE FLAW being exploited?
│
├── YES → Is it server-side or client-side?
│          ├── Server → #2 Exploiting Server
│          └── Client → #3 Exploiting Client
│
│          Note: The payload delivered is usually the NEXT step (#7)
│          giving paths like: #2 → #7 or #3 → #7
│
└── NO → Is FOREIGN CODE being executed?
         │
         ├── YES → #7 Malware
         │         If launched via legitimate tool (LOLBAS) → #1 → #7
         │
         └── NO → #1 Abuse of Functions
                  (Pure abuse of admin tools, APIs, configs)
```

## The Credential Rule

TLCTC Axiom X establishes that credentials have a dual operational nature. This is critical for accurate mapping.

| Phase | Classification | Examples |
|-------|---------------|----------|
| **Acquisition** | Maps to the **enabling cluster** | Keylogger → `#7`; Phishing → `#9`; SQLi → `#2`; MitM → `#5` |
| **Application** | **Always `#4`** | Presenting stolen creds to authenticate → `#4 Identity Theft` |

These are separate attack steps. A complete path looks like:

```
#9 → #4 → #1
```

1. `#9` — Phishing tricked user into entering credentials
2. `#4` — Attacker uses stolen credentials to authenticate
3. `#1` — Attacker abuses admin functions with that authenticated identity

## Handling Resource Development Techniques

Resource Development describes attacker-side preparation that happens **before** the attacker engages `@Org`. All 47 entries are `N/A` from `@Org`'s threat-model perspective. The cluster is `N/A` not because the techniques are unimportant — they are critical to threat-intelligence analysis and tracking — but because they have no boundary crossing into `@Org`.

**Two sphere categories:**

| Category | Sphere | Examples |
|---|---|---|
| Attacker-side preparation | `@AttackerInfra` | T1583 Acquire Infrastructure, T1585 Establish Accounts, T1587 Develop Capabilities, T1588 Obtain Capabilities, T1608 Stage Capabilities, T1650 Acquire Access from broker |
| Compromise of someone else | `@OtherVictims` | T1584 Compromise Infrastructure, T1586 Compromise Accounts |

**Why `@OtherVictims` is `N/A` from `@Org`'s perspective:**

The compromise of a third party (a domain registrar, a botnet host, someone else's social-media account) is a real attack — but it is not `@Org`'s attack. The compromised third party has their own threat model. From `@Org`, the attacker simply shows up later with the resulting capability — and that *use* against `@Org` is recorded as the relevant downstream technique.

**The `N/A` rationale phrasing was refreshed in v2.1 revalidation:**

The older boilerplate was *"Resource development activities fall outside TLCTC scope as they involve attacker infrastructure preparation before targeting any victim system."* That conflated two distinct N/A reasons (attacker-side prep vs other-victim prep) and used the imprecise "outside scope." Now each entry uses the precise sphere language (`@AttackerInfra` or `@OtherVictims`) and explicitly notes that the *use* of the resource against `@Org` will be classified at its own technique downstream.

## Handling Reconnaissance Techniques

Reconnaissance is mixed: some techniques cross into `@Org`, others stay outside it.

**Rule:** Classify by whether the technique crosses the `@Org` boundary, not by which kill-chain phase it sits in.

- **Active probing of `@Org` infrastructure** — `#1 Abuse of Functions + [DRE: C]`. Target services respond through their designed interfaces and disclose information; that response function is the generic vulnerability. Path: `||[api][@External→@Org]|| #1 + [DRE: C]`. Applies to T1595 Active Scanning and its sub-techniques.
- **Human elicitation against `@Org`** — `#9 Social Engineering + [DRE: C]`. Same generic vulnerability as T1566 phishing; only the goal differs (info disclosure rather than payload execution). Path: `||[human][@External→@Org]|| #9 + [DRE: C]`. Applies to T1598 Phishing for Information and its sub-techniques.
- **OSINT / closed-source collection** — **N/A**. No `@Org` boundary crossing; data is held by `@External` (registrars, DNS, search engines, breach dumps, dark-web markets) or was voluntarily published by `@Org`. This is a Layer-2 exposure condition, not a Layer-3 step. Applies to T1593, T1594, T1596, T1597, T1681 and the OSINT mode of the umbrella techniques T1589/T1590/T1591/T1592.
- **Resource Development** — generally **N/A** (`@AttackerInfra`).

Examples:
- T1595.002 "Vulnerability Scanning" → **#1** (probes hit `@Org`, services leak banners/versions through designed responses)
- T1598.003 "Spearphishing Link" (for info) → **#9** (human in `@Org` coerced into disclosure)
- T1596.002 "WHOIS" → **N/A** (registrar holds the data; no `@Org` system queried)
- T1589 "Gather Victim Identity Information" → **N/A** at the umbrella level (OSINT default; the active and SE branches are already covered by T1595 / T1598)
- T1588 "Obtain Capabilities" → **N/A** (attacker acquiring tools)

## LOLBAS / Dual-Use Tool Pattern

Many ATT&CK techniques describe "Living off the Land" — using legitimate system tools maliciously. The pattern is almost always:

```
#1 → #7
```

1. `#1` — The legitimate tool (PowerShell, certutil, mshta, etc.) is invoked using its designed interface
2. `#7` — The attacker-controlled script/command/payload executes within that tool's execution environment

The `#1` step reflects that the tool's **designed function** is being abused. The `#7` step reflects that **foreign executable content** runs. Both steps must be recorded (R-EXEC rule).

## Handling Initial Access Techniques

Initial Access techniques always cross the @Org boundary. The key distinctions:

**Auth-via-credentials vs flaw-exploitation** (R-ROLE / R-CRED test):

- If the technique describes **using valid/stolen credentials** to authenticate via a legitimate auth surface → `#4` per R-CRED. Examples: T1078 Valid Accounts (all sub-techniques), T1133 External Remote Services.
- If the technique describes **exploiting an implementation flaw** in a server-role component → `#2` per R-ROLE. Example: T1190 Exploit Public-Facing Application.
- If the technique describes **exploiting an implementation flaw** in a client-role component → `#3` per R-ROLE. Example: T1189 Drive-by Compromise.
- These are mutually exclusive: a technique is exploiting a flaw OR presenting a credential, not both. T1133 (legitimate VPN with stolen creds) is `#4`, NOT `#2`. T1190 (RCE in a web app) is `#2`, NOT `#4`.

**Phishing variants and transit**:

- T1566 Phishing parent → `#9` (the social-engineering act).
- T1566.001 Spearphishing Attachment → `#9 → #7` (FEC executes when attachment opened).
- T1566.002 Spearphishing Link → `(#9 → #3 → #7) | (#9 → #4)` — browser-exploit chain ends in `#7` per R-EXEC; credential-harvest path ends at `#4`. Always chain `#7` after `#3` when FEC executes.
- T1566.003 Spearphishing via Service → use transit operator `⇒@Service` for the relaying platform. Path: `||[human][@External⇒@Service→@Org]|| #9 → …`.
- T1566.004 Spearphishing Voice (vishing) → use `⇒@Telco`. Outcomes include `#9 → #1` (victim performs an authorized business function under attacker direction — wire transfer, password reset, config change), in addition to `#9 → #4` and `#9 → #7`.

**Supply chain placement (R-SUPPLY)**:

- T1195.001 Software Dependencies → `#10.2 → #7` at the `||[dev][@Vendor→@Org]||` boundary.
- T1195.002 Software Supply Chain → `#10.1 → #7` at the `||[update][@Vendor→@Org]||` boundary.
- T1195.003 Hardware Supply Chain → `#10.3 → #7` at the `||[physical][@Vendor→@Org]||` boundary.
- T1199 Trusted Relationship → `#10 → #7` at the `||[trust][@Vendor→@Org]||` boundary; `#10` placed at the Trust Acceptance Event, not at the upstream compromise.

## Handling Credential Access Techniques

Credential Access techniques are almost all **acquisition** steps. Per **R-CRED / Axiom X**, acquisition maps to its enabling cluster — the technique that *gets* the credential is classified by *how* it gets it, not by what the credential ultimately enables.

**Acquisition cluster table:**

| Acquisition mechanism | Cluster |
|---|---|
| Read from memory / file / registry / IMDS / config via designed APIs | `#1` |
| Foreign attacker code performs the read (Mimikatz, infostealer) | `#7` |
| MitM interception on the wire | `#5` |
| Exploit a flaw to dump (server-role) | `#2` |
| Exploit a flaw to dump (client-role) | `#3` |
| Repeated guessing/spraying/stuffing against an auth surface | `#4` (this is application of candidate credentials, not acquisition) |
| Consent phishing / fake login dialog | `#9` |

**Application is always `#4`** (Axiom X). When the technique encompasses both acquisition AND eventual application, the path is `<acquisition_cluster> → #4`.

**Common patterns:**

| Pattern | Path | Examples |
|---|---|---|
| Dump-then-use | `(#1 \| #7) → #4` (extract via API or malware, then apply) | T1555* Password Stores |
| Read-then-use | `#1 → #4` (read via API, then apply) | T1552* Unsecured Credentials, T1558.003 Kerberoasting, T1606* Forge Web Credentials |
| Pure dump (acquisition only) | `#1 \| #7` | T1003* OS Credential Dumping, T1056* Input Capture, T1539 Steal Web Session Cookie |
| Brute force | `#4` | T1110* (repeated application against auth surface) |
| AiTM | `#5` (often `#1 → #5 → #4`) | T1557* Adversary-in-the-Middle |
| Auth-process modification | `#1 \| (#1 → #7) \| #7` | T1556* Modify Authentication Process |

**Common older-mapping errors corrected in v2.1 revalidation:**

- T1539 Steal Web Session Cookie was `#4` (mistaking theft for application). T1539 is theft → `#1 \| #7`. T1550.004 is the use side → `#4`.
- T1555 family was inconsistently mapped (some `#1 \| #7`, some `#1 → #4`). Standardized to `(#1 \| #7) → #4`.
- T1003.006 DCSync is `#1`-only (designed AD replication), not `#1 \| #7` — no foreign code needs to execute on the DC.
- T1056.002 GUI Input Capture missed `#9` for the fake-dialog social-engineering step. Now `(#1 \| #7) → #9`.
- T1528 Steal App Access Token missed the consent-phishing variant. Now `(#1 \| #9) → #4`.
- T1621 MFA Request Generation (push fatigue) missed `#9` for the user-approval-under-fatigue step. Now `#1 → #9 → #4`.

## Handling Execution Techniques

Execution techniques are dominated by the LOLBAS pattern (`#1 → #7`) — a designed system feature is invoked to run attacker-supplied content. **Both steps must be recorded** per R-EXEC; never collapse them.

**Pattern map:**

| Technique family | Path | Notes |
|---|---|---|
| Interpreters and shells (T1059*) | `#1 → #7` | Signed interpreter is `#1`; attacker script content is `#7` |
| Schedulers (T1053*) | `#1 → #7` | Scheduling registration is `#1`; the executed binary is `#7` |
| IPC (T1559*) | `#1 → #7` | COM/DDE/XPC mechanism is `#1`; cross-process payload is `#7` |
| Service control (T1569*) | `#1 → #7` | Service register/start is `#1`; service binary is `#7` |
| Native API (T1106) | `#1 → #7` | Direct OS-API invocation that loads/runs attacker code |
| Module load (T1129) | `#1 → #7` | `LoadLibrary`/`dlopen` is `#1`; foreign DLL/dylib is `#7` |
| Cloud control plane (T1059.009, T1648, T1651) | `#1 → #7` | Provider API is `#1`; injected code is `#7` |
| Container runtime (T1609, T1610, T1059.013, T1053.007) | `#1 → #7` | Runtime/orchestrator API is `#1`; container content is `#7` |
| User Execution (T1204*) | `#9 → #7` | Human induction is `#9`; what they run is `#7` |
| Client exploit (T1203) | `#3 → #7` | Client-role flaw is `#3`; payload that runs is `#7` |
| Supply-chain pipeline (T1677) | `#1 → #10.2 → #7` | Repo/pipeline injection (`#1`) → TAE in dev sphere (`#10.2`) → runner execution (`#7`) |

**Common older-mapping errors corrected in v2.1 revalidation:**

- T1203 Exploitation for Client Execution was `#3` only — missing the `→ #7` chain. The technique is by definition "for execution"; per R-EXEC the FEC step must be recorded. Now `#3 → #7` (consistent with T1189 Drive-by Compromise).
- T1059.008 Network Device CLI was `#1 | #7` — inconsistent with all other T1059 sub-techniques. Standardized to `#1 → #7`.
- Sub-techniques of T1053, T1059, T1559, T1569, and T1204 had identical copy-pasted rationales ("Sub-technique inherits parent mapping"). Each now has a specific rationale naming the actual mechanism.

## Handling Collection Techniques

Collection techniques are about **reading** @Org data — file content, mailboxes, repositories, screen, audio/video, clipboard, network-device configurations. Almost all map to `#1` (designed read/access APIs abused) and carry `[DRE: C]` at the read step.

**Cluster patterns:**

| Pattern | Path | Examples |
|---|---|---|
| Direct read with existing access | `#1 + [DRE: C]` | T1005 Local System, T1039 Network Share, T1113 Screen, T1115 Clipboard, T1119 Automated, T1123 Audio, T1125 Video, T1213* Information Repositories, T1602* Config Repositories |
| Auth-then-read | `#4 → #1 + [DRE: C]` | T1114* Email Collection, T1530 Cloud Storage |
| Hijack-then-impersonate | `#1 → #4 + [DRE: C]` | T1185 Browser Session Hijacking |
| AiTM (dual-tagged) | `#5` (often `#1 → #5`) | T1557* — see Credential Access for full treatment |
| Capture from input surface (dual-tagged) | `#1 \| #7` | T1056* — see Credential Access |
| Staging / archiving (post-collection) | `#1` (no incremental DRE) | T1074* Data Staged, T1560* Archive Collected Data |

**`[DRE: C]` placement rule:** the data-risk event is recorded at the **collection step** (the moment the attacker reads the data), not at later staging/archiving/exfiltration steps which would re-cite the same breach. Collection is when confidentiality is first violated; later steps are intra-attacker movement/preparation.

**Common older-mapping errors corrected in v2.1 revalidation:**

- T1213.002 SharePoint was `N/A` with rationale "out of scope because post-compromise" — that reasoning would invalidate the entire Collection tactic. Corrected to `#1` matching the rest of the T1213 family.
- T1185 Browser Session Hijacking was `#1` only — the technique by definition results in identity impersonation through the hijacked session. Corrected to `#1 → #4` per R-CRED.

## Handling Command and Control Techniques

C2 techniques split into three cluster groups depending on whether the C2 mechanism is a **feature of the malware payload**, an **abuse of legitimate third-party services**, or a **mix**.

**Cluster groups:**

| Group | Cluster | Examples |
|---|---|---|
| FEC capability (C2 logic embedded in malware) | `#7` | T1071* Application Layer Protocol, T1001* Data Obfuscation, T1568* Dynamic Resolution / DGA, T1573* Encrypted Channel, T1132.002 Non-Standard Encoding, T1008 Fallback Channels, T1665 Hide Infrastructure |
| Third-party service as relay | `#1` (with transit `⇒`) | T1102* Web Service (`⇒@WebService`), T1102.001-003 (paste sites, social media, cloud storage) |
| Mix — depends on whether implementation reuses designed APIs or is malware-implemented | `#1 \| #7` | T1090* Proxy, T1095 Non-Application Layer, T1132.001 Standard Encoding, T1571 Non-Standard Port, T1572 Protocol Tunneling, T1219* Remote Access Software, T1104 Multi-Stage Channels |

**Transit operator (`⇒`) is the v2.1 win for C2:**

| Technique | Carrier | Transit notation |
|---|---|---|
| T1102* Web Service | Twitter, GitHub Gists, Pastebin, Discord | `||[network][@Org⇒@WebService→@External]||` |
| T1090.001 Internal Proxy | Compromised @Org host as relay | `||[network][@External⇒@OrgRelay→@Org]||` |
| T1090.002 External Proxy | Commercial / residential proxy | `||[network][@External⇒@Proxy→@Org]||` |
| T1090.003 Multi-hop Proxy | Tor, layered VPN | `||[network][@External⇒@HopN⇒…⇒@Hop1→@Org]||` (chained `⇒`) |
| T1090.004 Domain Fronting | CDN serving multiple tenants | `||[network][@External⇒@CDN→@Org]||` |
| T1219* Remote Access Software | Vendor cloud (TeamViewer, AnyDesk, VS Code Tunnels) | `||[network][@External⇒@VendorCloud→@Org]||` |
| T1568.001 Fast Flux DNS | DNS resolver chain | `||[network][@Org⇒@DNSResolvers→@External]||` |
| T1071.005 Pub/Sub Protocols | Third-party MQTT/AMQP broker | `||[network][@Org⇒@Broker→@External]||` |

**Common older-mapping errors corrected in v2.1 revalidation:**

- T1105 Ingress Tool Transfer was `#7` — but the *transfer* step itself uses designed network functions to move a file, not to execute foreign code. R-EXEC fires when/if the transferred tool runs (a separate `#7` step in the chain). T1105 corrected to `#1`.
- Sub-techniques in T1071, T1090, T1102, T1132, T1219, T1568, T1573 had identical "Sub-technique inherits parent mapping" boilerplate. Each now has a specific rationale naming the actual protocol/service/mechanism.

## Handling Persistence Techniques

Persistence techniques almost all share the **autostart pattern**: register attacker-supplied code in a designed system mechanism so the OS/application launches it on a future trigger (boot, logon, file-open, event, schedule, network signal). The cluster shape is `#1 → #7` — `#1` for the registration step (designed mechanism abused), `#7` for the FEC at trigger time (per R-EXEC).

**Cluster groups within Persistence:**

| Pattern | Cluster | Examples |
|---|---|---|
| Autostart / trigger registration | `#1 → #7` | T1037* Init Scripts, T1137* Office Startup, T1176* Extensions, T1543* System Process, T1546* Event Triggered, T1547* Autostart, T1554 Compromise Binary, T1574* Hijack Execution Flow, T1653 Power Settings, T1671 Cloud App Integration |
| Identity-state change (no FEC at this step) | `#1` | T1098* Account Manipulation, T1136* Create Account, T1112 Modify Registry |
| Credential application (use a valid account for ongoing access) | `#4` | T1078* Valid Accounts, T1133 External Remote Services |
| Auth-process modification | `#1 \| (#1 → #7) \| #7` | T1556* (see Credential Access) |
| Pre-OS Boot implants | `#7 \| (#1 → #7)` | T1542* (firmware / bootkit) — supply-chain variants chain `#10.3 → #7` |

**The placement-vs-execution distinction (T1505.003 correction):**

T1505.003 Web Shell was `#7`-only — but every persistence technique that ends in FEC execution must record the placement step. The web shell has to be written somewhere (`#1` — file write to web-served directory) before it can be invoked (`#7` per R-EXEC). Corrected to `#1 → #7` to match the rest of the Persistence family.

**Why T1098*/T1112/T1136* stay `#1`-only (no `→ #7`):**

These techniques modify identity-management or registry state *without* introducing FEC. Adding an SSH key, creating a user, granting an IAM role, or writing a registry value is configuration change. The persistence is the standing access; subsequent attacker activity using that access is recorded under its own cluster (typically `#4` for using the new credential, or whatever cluster the action falls into).

## Handling Privilege Escalation Techniques

PrivEsc techniques split between **abuse of designed elevation mechanisms** (`#1 → #7`) and **exploitation of a flawed component** (`(#2 | #3) → #7` per R-ROLE), with `#1` (no FEC) for some configuration-only techniques like Account Manipulation and Domain/Tenant Policy Modification (already covered under Persistence).

**Cluster patterns:**

| Pattern | Cluster | Examples |
|---|---|---|
| Process injection (intra-process FEC) | `#1 → #7` with `\|[process][@procA→@procB]\|` | T1055* (DLL injection, hollowing, doppelgänging, APC, ptrace, etc.) |
| Token manipulation (token = identity artifact) | `#1 → #4` | T1134.001-003, T1134.005 — manipulation step is `#1`, operating under new token is `#4` per R-CRED |
| Token manipulation enabling new FEC | `#1 → #7` | T1134.004 Parent PID Spoofing — spawned process runs FEC |
| Elevation-mechanism abuse | `#1 → #7` | T1548* (UAC bypass, sudo, polkit, TCC, cloud assume-role) |
| Setuid + attacker binary | `#1 → #7` | T1548.001 |
| Exploit a flaw to elevate | `(#2 \| #3) → #7` | T1068 |
| Container/VM escape | `(#1 \| #2)` with `\|[hypervisor][@container→@host]\|` | T1611 |
| Configuration change (no FEC at this step) | `#1` | T1484* Domain/Tenant Policy Modification |

**The v2.1 intra-system boundary operator is critical here:**

| Technique | Boundary | Notation |
|---|---|---|
| T1055* Process Injection | Cross-process | `\|[process][@procA→@procB]\|` |
| T1611 Escape to Host | Container/VM ↔ host | `\|[hypervisor][@container→@host]\|` |
| Sandbox-escape variants | Sandbox ↔ OS | `\|[sandbox][@renderer→@os]\|` (e.g., browser-renderer-to-OS escape, classified as `#3` for the renderer flaw) |

**Common older-mapping errors corrected in v2.1 revalidation:**

- T1055* Process Injection family had most sub-techniques as `#1`-only — but the injected code IS FEC executing in target process. Per R-EXEC, all injection variants chain to `#7`. Corrected to `#1 → #7`.
- T1068 Exploitation for PrivEsc was `#2 | #3` — missing the `→ #7` chain that is the entire point of PrivEsc exploitation. Corrected to `(#2 | #3) → #7`.
- T1611 Escape to Host was `#1`-only — covered configuration-abuse escapes but missed runtime/kernel-exploit escapes (`#2`). Corrected to `#1 | #2` and given the canonical intra-system boundary `|[hypervisor][@container→@host]|`.
- T1134.004 Parent PID Spoofing was `#1`-only — the spawned attacker process runs FEC, requiring the `#7` step. Corrected to `#1 → #7`.
- T1548.001 Setuid was `#1`-only — when the suid target is attacker binary, future invocation runs FEC at elevated privilege. Corrected to `#1 → #7`.

## Handling Defense Evasion Techniques

Defense Evasion is the largest tactic (215 entries) and the most varied. Most map to `#1` (abuse of designed admin/configuration features) or `#1 → #7` (LOLBAS-style proxied execution). FEC-feature framing (per the user-clarified pattern from T1497/T1622) applies to several malware-internal evasion behaviors.

**Cluster patterns:**

| Pattern | Cluster | Examples |
|---|---|---|
| LOLBAS — signed proxy execution | `#1 → #7` | T1216* Signed Script Proxy, T1218* System Binary Proxy (mshta, regsvr32, rundll32, etc.), T1220 XSL, T1127* Trusted Dev Utilities (MSBuild/ClickOnce) |
| Defender impairment via designed admin | `#1` | T1562* Impair Defenses (disable EDR, AV, firewall, logging) |
| Indicator removal via designed admin | `#1` | T1070* Indicator Removal (event logs, history, files) |
| Hide artifacts via designed file/proc features | `#1` | T1564* Hide Artifacts (hidden attrs, ADS, hidden window, exclusions) |
| Cloud admin abuse | `#1` | T1535, T1578*, T1666 |
| Trust subversion (TAE for malicious-signed artifact) | `#1 \| #10` | T1553* Subvert Trust Controls (code signing, MOTW, root CA install) |
| Obfuscation as FEC build feature | `#7` | T1027 sub-techniques: polymorphic, junk insertion, stripped, dynamic API, etc. |
| Obfuscation reusing system libraries | `#1 \| #7` | T1027 mixed-mode subs |
| FEC environmental gating | `#7` | T1480* Execution Guardrails, T1678 Delay, T1679 Selective Exclusion (and T1497 sandbox evasion, T1622 debugger evasion) |
| Exploit a flaw to disable defenses | `(#2 \| #3) → #7` | T1211 |
| Reflective in-memory loading | `#1 → #7` | T1620 |
| Impersonation (social engineering) | `#9` | T1656 |

**Common older-mapping errors corrected in v2.1 revalidation:**

- **T1127* Trusted Developer Utilities** was `#1 | #10` — but no malicious artifact crosses a trust boundary; this is the LOLBAS pattern (signed utility runs attacker code). Corrected to `#1 → #7`.
- **T1211 Exploitation for Defense Evasion** was `#2 | #3` — missing the `→ #7` chain that is the entire point of exploitation. Corrected to `(#2 | #3) → #7` (cf. T1068 PrivEsc).
- **T1480* Execution Guardrails** was `#1` — but environmental gating logic is integral to the malware payload (FEC-feature framing). Corrected to `#7` to align with T1497/T1622.
- **T1620 Reflective Code Loading** was `#1` — the loaded code IS FEC executing. Corrected to `#1 → #7` per R-EXEC.
- **T1656 Impersonation** was `#1` — impersonating people to manipulate them is the canonical example of `#9 Social Engineering`. Corrected to `#9`.

**FEC-feature framing applies to evasion behaviors built into the malware:**

Use `#7` (not `#1`) when the technique describes a malware capability that runs as part of the payload:
- Environmental gating (T1480*, T1497*, T1622)
- Polymorphism / metamorphism / junk code (T1027.014, T1027.016)
- Indicator removal from tools (T1027.005)
- Dynamic API resolution (T1027.007)
- Stripped/embedded payloads (T1027.008, T1027.009)
- Sleep/delay logic (T1678)
- Selective exclusion (T1679)
- Build-time naming masquerade (T1036.001, T1036.005, T1036.007)
- Deobfuscation-at-runtime (T1140)
- Rootkit (T1014)

This is **not Axiom IV** (actor identity) — it is the framework distinction that built-in malware capabilities are properties of the `#7` step rather than discrete `#1` actions.

## Handling Discovery Techniques

Discovery techniques are post-foothold enumeration: the attacker (or attacker-controlled tooling) is already running inside @Org and queries designed system/network/cloud APIs to learn the environment. The generic vulnerability is **information disclosure through legitimate enumeration interfaces** — every Discovery technique except T1040 Network Sniffing maps to `#1`.

**Single rule:** Discovery = `#1`. Specific commands/APIs differ but the cluster does not.

| Sub-area | Typical commands/APIs |
|---|---|
| System info | `systeminfo`, `uname`, `Get-ComputerInfo`, `wmic` |
| Process / service | `tasklist`, `ps`, `sc query`, `systemctl` |
| Network | `ipconfig`, `netstat`, `arp`, `nltest`, `Get-NetTCPConnection` |
| Account / group | `net user`, `Get-ADUser`, IAM `list-users` |
| File / storage | `dir`, `ls`, `Get-Volume`, browser SQLite reads |
| Cloud control plane | `aws ec2 describe-*`, `az resource list`, `gcloud` listings |

**T1040 Network Sniffing is one exception:** `#1 | #5` (passive observation on a host vs. AiTM positioning on the wire) — handled under Credential Access.

**T1497*/T1622 are the other exception (`#7`, not `#1`):**

T1497 Virtualization/Sandbox Evasion and T1622 Debugger Evasion are classified `#7` because they describe **features of the FEC payload itself** — environmental checks (sandbox detection, debugger detection) that are integral capabilities of the malware, not discrete enumeration steps performed by an actor. They are properties of the `#7` step, not new `#1` steps. This is distinct from Axiom IV (which prohibits classifying by actor identity); the framing here is "FEC capability" — the technique describes a built-in malware feature, not a separate action with its own generic vulnerability. Contrast with T1057 Process Discovery and other interactive-enumeration techniques, which are discrete `#1` steps regardless of who runs them.

## Handling Lateral Movement Techniques

Lateral movement is internal — both source host and target host are inside `@Org`. No external boundary mark is needed; the path is just a step sequence (with optional `||[physical][@Org→@Org]||` for removable-media cases).

**Two dominant patterns:**

| Pattern | Path | Examples |
|---|---|---|
| **Auth-then-abuse** | `#4 → #1` | T1021* Remote Services (RDP, SMB, SSH, WinRM, VNC, DCOM, cloud), T1570 Lateral Tool Transfer |
| **Auth-material reuse** | `#4` | T1550* Use Alternate Authentication Material (Pass-the-Hash, Pass-the-Ticket, App Tokens, Web Cookies) |
| **Hijack-then-impersonate** | `#1 → #4` | T1563* Session Hijacking |
| **Exploit remote service** | `#2` (→ `#7`) | T1210 Exploitation of Remote Services |
| **Plant-then-execute** | `#1 → #7` | T1072 Software Deployment Tools, T1080 Taint Shared Content |

**Critical R-CRED reminders specific to lateral movement:**

- Every artifact that authenticates an identity is a credential: passwords, hashes, Kerberos tickets, OAuth tokens, web cookies, SSH keys, kubeconfig contexts. Per **Axiom X**, presenting any of them is `#4`.
- T1550* must be `#4` — the older mapping pass had T1550, T1550.001, T1550.004 as `#1` with a copy-pasted "defense evasion" rationale. That conflated the *evasion goal* (no MFA prompt) with the *generic vulnerability* (identity artifact accepted by auth surface). The vulnerability is the latter — `#4`.

**R-EXEC reminder for deployment-style techniques:**

- T1072 Software Deployment Tools must chain `→ #7` for every target host: the deployment tool's designed function is abused (`#1`) to push attacker-supplied content that then runs (`#7`).
- T1080 Taint Shared Content is `#1 → #7` — placement on a network share is file-write abuse, not physical attack. (Removable-media replication is T1091, which is `#8 → #7`.)

**Internal spearphishing (T1534):**

- `#9` only. The `#1`-only mode does not exist — without social engineering, it is just T1072 or T1564 mail-rule abuse. Internal spearphishing is by definition a `#9` step.

## Handling Exfiltration Techniques

Exfiltration techniques carry `[DRE: C]` (Confidentiality breached — data left @Org). The cluster reflects **how** the data moves, not **where** it lands.

**Cluster modes:**

- `#1` — data movement uses legitimate egress / transfer / storage functions abused for the goal (HTTPS upload, DNS query payload, file copy to USB, port mirroring, scheduled `rsync`).
- `#7` — data movement is performed by malware\'s own embedded transfer code (custom protocol, malware-implemented upload).
- Many techniques span both modes → `#1 | #7`.

**Transit operator (`⇒`) for legitimate-service exfil:**

When data is exfiltrated through a legitimate web service that the attacker uses as a staging/relay point, mark the service as transit between `@Org` and `@External`:

| Technique | Carrier | Transit notation |
|---|---|---|
| T1567.001 Code Repository | GitHub / GitLab | `||[network][@Org⇒@CodeRepo→@External]||` |
| T1567.002 Cloud Storage | S3 / Azure Blob / GCS / Dropbox | `||[network][@Org⇒@CloudStorage→@External]||` |
| T1567.003 Text Storage Sites | Pastebin / hastebin | `||[network][@Org⇒@PasteSite→@External]||` |
| T1567.004 Webhook | Discord / Slack / Teams webhook | `||[network][@Org⇒@Webhook→@External]||` |
| T1537 Cloud Account Transfer | Cloud provider | `||[network][@Org⇒@CloudProvider→@External]||` |

For T1041 (over C2 channel) and T1048* (alternative protocol), the destination is typically the attacker\'s own infrastructure — no transit operator needed: `||[network][@Org→@External]||`.

**Physical media (T1052*) is `#1`, not `#8`:**

The older mapping pass had T1052 / T1052.001 (USB exfil) as `#8 Physical Attack`. Corrected: copying data to a connected USB is designed-function abuse (`#1`), not physical exploitation. `#8` only applies when the attacker first **bypasses physical security** to insert their own medium — in which case prepend it: `||[physical][@External→@Org]|| #8 → #1 + [DRE: C]`.

**T1041 Exfiltration Over C2 must allow `#1` mode:**

The older mapping pass had T1041 as `#7`-only. Corrected to `#1 | #7` to align with T1048/T1567: when the C2 protocol is itself an abused legitimate protocol (HTTPS, DNS, named pipes), the exfiltration step is `#1`; when the C2 is a malware-implemented protocol, it is `#7`.

## Handling Impact Techniques (DRE annotations + Axiom III)

Impact techniques describe outcomes. The cluster captures **how** the impact is delivered (#1, #6, #7, #2 — the cause), and a `[DRE: …]` tag captures **what data risk event** results.

**Axiom III applied to outcome-named techniques:** "Ransomware" is not a cluster — the encryption execution is `#7`, the data state is `[DRE: Ac]`. "Wiper" is not a cluster — the destructive execution is `#7`, the data state is `[DRE: Av]`. "Defacement" is not a cluster — the placement of attacker content is `#7`, the data state is `[DRE: I]`.

**DRE selection guide for Impact:**

| Outcome on @Org data | DRE tag |
|---|---|
| Data confidentiality breached (read/exfiltrated) | `[DRE: C]` |
| Data integrity violated (manipulated, defaced) | `[DRE: I]` |
| Data unavailable (service down, network flooded, account locked) | `[DRE: A]` (general) |
| Data **gone** / unrecoverable (wiped, deleted) | `[DRE: Av]` |
| Data **present but unusable** (encrypted, locked behind disabled account) | `[DRE: Ac]` |

The `Av` vs `Ac` distinction matters operationally: ransomware (`Ac`) leaves recovery options that wipers (`Av`) destroy.

**Cluster mode by destruction method:**

- Foreign attacker code performs the action (custom binary, wiper, ransomware) → `#7`
- Designed admin tool performs the action (`vssadmin`, `sc stop`, cloud lifecycle policy, IAM disable API) → `#1`
- Volume overwhelms capacity (network, application, mailbox) → `#6`
- Server-side flaw is triggered to crash → `#2`

**Examples:**

- T1486 Data Encrypted for Impact → `#7 + [DRE: Ac]`
- T1485 Data Destruction → `#7 + [DRE: Av]`
- T1485.001 Lifecycle-Triggered Deletion → `#1 + [DRE: Av]` (cloud platform performs the deletion per policy)
- T1490 Inhibit System Recovery → `#1 + [DRE: Av]` (admin tool deletes shadows)
- T1491 Defacement → `#7 + [DRE: I]`
- T1498.002 Reflection Amplification → `||[network][@External⇒@Reflectors→@Org]|| #6 + [DRE: A]`
- T1565.002 Transmitted Data Manipulation → `#1 | #5 + [DRE: I]` (host-side abuse vs MitM)
- T1667 Email Bombing → `#6 + [DRE: A]` (volumetric, not function-abuse)

## Quality Checklist

Before finalizing a mapping, verify:

- [ ] **Domain identified** — Is it clear where this technique happens?
- [ ] **Asset identified** — Which protected asset is affected?
- [ ] **Cause, not consequence** — Are you mapping the vulnerability exploited, not the outcome?
- [ ] **Single step vs. path** — If multiple steps, did you express them as an attack path?
- [ ] **Credentials handled correctly** — Acquisition vs. use distinction applied?
- [ ] **R-EXEC respected** — If code executes, is `#7` recorded?
- [ ] **Context considered** — Same technique label can map differently in different implementations
