# A Cause-Oriented Cyber Threat Taxonomy: The Top Level Cyber Threat Clusters Framework

**Author:** Bernhard Kreinz
**Version:** 2.3
**Date:** 2026-06-07
**License:** CC BY 4.0

## Abstract

Cybersecurity discourse routinely uses the term "cyber threat" to denote several distinct concepts at once: the cause of a compromise, its outcome, the actor responsible, and the technique employed. This conflation impedes consistent classification, comparable incident documentation, and clear communication of cyber risk between leadership, risk functions, and technical teams. Established frameworks address adjacent layers — control objectives, adversary techniques, software weaknesses, and quantitative risk — but none provides a compact, non-overlapping taxonomy on the cause side that holds stable across system types. The Top Level Cyber Threat Clusters (TLCTC) framework proposes ten top-level threat clusters, each defined by the single generic vulnerability it initially targets. The taxonomy separates threats (causes) from system events, data risk events, business consequences, and actor identity. This paper presents the framework's derivation logic, its design principles and threat topology, the ten cluster definitions, the ten axioms that constrain interpretation, and the classification rules that keep assignment reproducible, together with example mappings expressed in an attack-path notation. By distinguishing a stable strategic management view from a concrete operational security view, TLCTC functions as a translation layer between strategic risk governance and operational security practice.

**Keywords:** cyber threat taxonomy; cyber risk taxonomy; cybersecurity ontology; cyber threat classification; threat modeling; cause-oriented taxonomy; TLCTC; Top Level Cyber Threat Clusters

## 1. Introduction and Problem Statement

Cybersecurity suffers from a persistent language problem: the field describes fundamentally different things using the same words, and uses different words for the same thing. In practice, the term "cyber threat" is routinely mixed with threat actors, vulnerabilities, control failures, incidents, and outcomes such as data breach, denial of service, or ransomware. A single label is asked to carry the cause of a compromise, the technique used to achieve it, the actor who carried it out, and the consequence that followed. These are categorically distinct concepts, and collapsing them into one term blurs the boundary between *why* a compromise becomes possible and *what* happens once it does.

This semantic blur has practical costs. When cause, technique, actor, and outcome share a vocabulary, it becomes difficult to compare incidents across organizations, aggregate threat intelligence into stable categories, design controls that target a specific root weakness, or communicate cyber risk consistently between leadership, risk functions, and technical teams. The same event may be classified differently by two analysts not because they disagree about the facts, but because the underlying terms admit multiple readings. Outcome-named categories such as "ransomware" or "data breach" compound the problem: they describe an effect, not the generic vulnerability an attacker exploited, so they cannot anchor a reproducible mapping from threat to control.

Existing frameworks address adjacent layers of this space but leave the cause side underspecified. Control catalogues and management standards organize what an organization should do; adversary-technique knowledge bases enumerate observed behaviours; software-weakness and vulnerability registries catalogue concrete defects; and quantitative methods estimate loss. Each is valuable within its scope, yet none provides a compact, non-overlapping taxonomy of the generic vulnerabilities that compromises ultimately exploit — a stable backbone that holds across enterprise IT, cloud, OT, IoT, and endpoint environments without being tied to a particular technology or actor.

The Top Level Cyber Threat Clusters (TLCTC) framework addresses this gap by anchoring analysis in causality. A cyber threat is defined by the generic vulnerability (root weakness) it exploits, not by who performs it and not by the consequence that follows. The framework's contribution is a compact set of ten non-overlapping, cause-side threat clusters, each defined by the single generic vulnerability it initially targets. Threats are kept on the cause side and separated from outcomes, actor identity, and control failures, so that complete real-world intrusions can be expressed as ordered sequences of cluster steps — attack paths — without changing the meaning of the individual steps. By separating a stable strategic management view (clusters and generic vulnerabilities) from a concrete operational security view (specific vulnerabilities, techniques, and procedures), TLCTC is intended to function as a shared, cause-oriented vocabulary that links strategic risk governance and operational security practice.

## 2. The Thought Experiment: Deriving the Ten Clusters

The ten TLCTC clusters are not an arbitrary enumeration or an industry convention; they are derived through a systematic decomposition of the attack surfaces present in information technology. Imagine the complex world of IT as a single object. Although robust and seemingly closed, this object exposes various attack surfaces — the generic vulnerabilities, or root weaknesses. Examining each surface in turn yields, one at a time, the full set of clusters.

**1.** Begin at the software asset. Concentrating first on the essentials, consider the functional domain and scope, and observe that every function can be abused and that more scope also means more attack surface. This yields the first threat cluster: **Abuse of Functions**.

**2.** Every piece of software, however well optimized, may contain code flaws that can be exploited — especially when the software is in a **server role** and processes attacker-controlled requests or inputs. This leads to the threat cluster: **Exploiting Server**.

**3.** On the client side too, existing software code flaws can be exploited. This type of attack, where the client **processes attacker-controlled resources or content** during outbound interaction, manifests as the threat cluster: **Exploiting Client**.

**4.** Software interacts with identities and credentials, both human and technical. When **access-enabling identity artifacts** — credentials, tokens, keys, session identifiers, and the like — are **used or presented** to impersonate an identity, they can be abused. This leads to the threat cluster: **Identity Theft**.

**5.** Communication is crucial in a connected world. As data is transmitted between two points, rogue parties might eavesdrop, modify, or inject themselves into the exchange. This reveals the threat cluster: **Man in the Middle**.

**6.** Continuous connectivity also makes systems susceptible to attacks that deliberately **exhaust or overload resources** and thereby degrade service. This leads to the threat cluster: **Flooding Attack**.

**7.** The digital landscape involves a continuous exchange of files and data. Some transfers introduce **foreign executable content**, and if such content is **executed**, it poses a threat. Here arises the threat cluster: **Malware**.

**8.** Physical points of access and interaction remain, through which intruders might enter. This gives the threat cluster: **Physical Attack**.

**9.** The human factor must not be forgotten: people are susceptible to deception, manipulation, and misconduct. This human element leads to the threat cluster: **Social Engineering**.

**10.** Software and hardware ecosystems are almost always linked with third-party software, hardware, or services. When an organization **accepts and relies on** such a third-party trust relationship — components, updates, providers — that trust can be leveraged by attackers. This leads to the final threat cluster: **Supply Chain Attack**.

Through this thought experiment and a careful examination of the vulnerabilities present in the IT landscape, ten distinct top-level cyber threat clusters are derived. The decomposition is intended to be complete and mutually exclusive: it provides a clear structure and a deeper understanding of the diverse threats that IT systems, people, and processes face.

## 3. Taxonomy Design Principles and Threat Topology

### 3.1 Cause-Orientation and the Cause/Event/Consequence Separation

TLCTC is a cause-oriented taxonomy. A threat cluster sits on the *cause* side of an attack: it names the generic vulnerability an attacker exploits, not the event that follows or the consequence that results. Conceptually, this corresponds to the cause side of a bow-tie model, where threats are the causes that converge on a central risk event, and losses of confidentiality, integrity, or availability are recorded separately as outcomes on the consequence side. (The full bow-tie treatment, including control frameworks and indicators, belongs to a separate application and governance document and is out of scope here; the model is used only as the conceptual anchor for keeping cause, event, and consequence distinct.)

The practical consequence is that outcomes are never threats. Labels such as "data breach," "service outage," or "ransomware" describe effects, not the generic vulnerability that was exploited to produce them. They are recorded as data risk events on the consequence side, while the threat that caused them is classified by its cause. Keeping these layers apart is what allows two analysts to classify the same incident the same way and what makes mappings from threat to control reproducible.

### 3.2 Non-Overlap: One Generic Vulnerability, One Cluster

The taxonomy is built on a strict classification principle: every distinct attack step exploits exactly one generic vulnerability (root weakness), and each generic vulnerability belongs to exactly one of the ten clusters. The clusters are therefore non-overlapping by construction. A step that appears to belong to two clusters is, under this principle, two steps and must be split, each anchored in the single generic vulnerability it targets. Because each attack vector is defined by the generic vulnerability it *initially* targets, classification is anchored in the initial cause rather than in technique labels or downstream effects.

To remain universally applicable, the framework deliberately avoids differentiating by system type. Whether the environment is enterprise IT, cloud, SaaS, OT/SCADA, IoT, endpoints, or network infrastructure, the same foundational attack surfaces recur — software functions and implementation flaws, identity artifacts, communication paths, capacity limits, executable-content handling, physical accessibility, human psychology, and third-party trust dependencies. Sector labels do not create new threat classes; they change only the specific vulnerabilities and controls at the operational level. This supports a separation between a stable Strategic Management Layer (clusters and generic vulnerabilities, used for governance and control mapping) and an Operational Security Layer (concrete vulnerabilities, techniques, and procedures, used in detection, response, and engineering).

### 3.3 Threat Topology: Internal and Bridge

Beyond classification, each cluster carries a structural property called its *threat topology*, which describes whether the generic vulnerability is exploited within the software domain or from a different control regime. A **domain** is a set of assets governed by a coherent control regime — its policies, monitoring, enforcement, and accountability. Domains may be technical, organizational, or socio-technical (for example, the cyber/IT domain, the physical security domain, the human decision domain, or a vendor development domain).

TLCTC uses two topology types:

- **Internal** — the generic vulnerability is exploited *within* the software domain's control regime. Clusters #1 through #7 are internal: abuse of designed functions, server- and client-side implementation flaws, credential use within the identity domain, exploitation of insufficient end-to-end protection within a communication relationship, exhaustion of finite capacity, and execution of foreign executable content.
- **Bridge** — the generic vulnerability inherently enables crossing into, or leverage over, the software domain *from a different control regime* outside the software domain. Clusters #8, #9, and #10 are bridge clusters: Physical Attack originates in the physical security domain, Social Engineering in the human decision domain, and Supply Chain Attack in the third-party governance domain.

Topology matters for control ownership and defense alignment: internal threats can be addressed primarily within the software-security control regime, whereas bridge threats require controls in multiple regimes (human, physical, third-party governance) and often involve organizational handoffs. Notably, Man in the Middle (#5) is internal rather than bridge: it sits "between" communicating parties but does not inherently cross into a different governance domain, since its generic vulnerability is insufficient end-to-end protection inside a single communication relationship.

Topology is a structural property and does not change cluster classification, which remains anchored in the initial generic vulnerability. Cluster-level topology (a stable property of the cluster definition) is related to but distinct from step-level topology (whether a specific step crosses a concrete domain boundary in a given scenario). Every #8, #9, and #10 step is normally a bridge step; internal-cluster steps (#1–#7) may also cross a boundary in multi-tenant or partner contexts, in which case the crossing is annotated in the attack-path notation (Section 7) rather than reclassified.

## 4. The Ten Threat Clusters

Each cluster is identified by a strategic ID (`#N`) for management-level use and an operational root ID (`TLCTC-0N.00`) that anchors its operational sub-threats. The definition, attacker's view, and generic vulnerability for each cluster below are reproduced verbatim from the canonical machine-readable framework dictionary (`tlctc-framework.v2.3.json`) so that this paper and the schema cannot drift. Supporting prose for each cluster is drawn from the canonical cluster definitions.

### #1 Abuse of Functions

- **Strategic ID:** #1
- **Operational root ID:** TLCTC-01.00
- **Name:** Abuse of Functions
- **Definition:** An attacker abuses the logic or scope of existing, legitimate software functions for malicious purposes without exploiting a code flaw.
- **Attacker's view:** "I abuse a functionality, not a coding issue."
- **Generic vulnerability:** The inherent trust, scope, and complexity designed into software functionality and configuration.
- **Topology:** Internal.

This cluster covers the manipulation of legitimate software capabilities — features, APIs, configurations, administrative settings, and workflows — through standard interfaces using built-in input types and valid sequences of actions, achieving an attacker advantage without requiring an implementation flaw.

### #2 Exploiting Server

- **Strategic ID:** #2
- **Operational root ID:** TLCTC-02.00
- **Name:** Exploiting Server
- **Definition:** An attacker targets flaws within the server-side application's source code implementation.
- **Attacker's view:** "I abuse a flaw in the application's source code on the server side."
- **Generic vulnerability:** Server-side implementation flaws enable unintended behavior.
- **Topology:** Internal.

The vulnerable component accepts and handles inbound requests or stimuli relative to the attacker. Crafted payloads (for example SQL injection strings, buffer overflows, or XXE payloads) trigger specific implementation bugs, forcing unintended behavior or enabling code execution.

### #3 Exploiting Client

- **Strategic ID:** #3
- **Operational root ID:** TLCTC-03.00
- **Name:** Exploiting Client
- **Definition:** An attacker targets flaws within the source code implementation of any software acting in a client role.
- **Attacker's view:** "I abuse a flaw in the source code of software acting as a client."
- **Generic vulnerability:** Client-side implementation flaws enable unintended behavior.
- **Topology:** Internal.

The vulnerable component consumes external responses, content, or state. Exploitation targets coding mistakes in parsing, rendering, state management, or response handling, typically through crafted content delivered during outbound interaction.

### #4 Identity Theft

- **Strategic ID:** #4
- **Operational root ID:** TLCTC-04.00
- **Name:** Identity Theft
- **Definition:** An attacker misuses authentication credentials to impersonate an identity.
- **Attacker's view:** "I abuse stolen or forged credentials to act as someone else."
- **Generic vulnerability:** Weak identity management processes and/or inadequate credential protection mechanisms throughout the identity lifecycle.
- **Topology:** Internal.

This cluster covers the presentation or use of credentials, tokens, keys, session artifacts, or other identity representations to authenticate and act as an identity different from the presenter's own. Credential acquisition maps to the enabling cluster; credential use always maps here (see R-CRED).

### #5 Man in the Middle

- **Strategic ID:** #5
- **Operational root ID:** TLCTC-05.00
- **Name:** Man in the Middle
- **Definition:** An attacker intercepts, modifies, or relays communication between two parties by exploiting a privileged position on the communication path.
- **Attacker's view:** "I abuse my position between communicating parties."
- **Generic vulnerability:** The lack of sufficient control, integrity protection, or confidentiality over the communication channel/path.
- **Topology:** Internal.

The cluster covers interception, observation, modification, injection, replay, or protocol downgrade/stripping from a controlled position on a communication path. Gaining the position maps to another cluster; #5 begins once the position is controlled (see R-MITM).

### #6 Flooding Attack

- **Strategic ID:** #6
- **Operational root ID:** TLCTC-06.00
- **Name:** Flooding Attack
- **Definition:** An attacker intentionally overwhelms system resources or exceeds capacity limits through a high volume of requests, data, or operations, leading to denial of service.
- **Attacker's view:** "I abuse the circumstance of always limited capacity."
- **Generic vulnerability:** Finite capacity limitations inherent in any system component.
- **Topology:** Internal.

The cluster covers exhaustion of finite resources — bandwidth, CPU, memory, storage, quotas, or pools — through volume or intensity that exceeds capacity limits. Availability loss caused primarily by an implementation defect is classified as #2 or #3 instead (see R-FLOOD).

### #7 Malware

- **Strategic ID:** #7
- **Operational root ID:** TLCTC-07.00
- **Name:** Malware
- **Definition:** An attacker abuses the inherent ability of a software environment to execute foreign executable content, including malicious code or legitimate tools executing attacker-controlled code.
- **Attacker's view:** "I abuse the environment's designed capability to execute malware code, malicious scripts, or foreign-introduced tools for my purposes."
- **Generic vulnerability:** The software environment's designed capability to execute potentially untrusted foreign code.
- **Topology:** Internal.

The cluster covers execution of Foreign Executable Content (FEC) through the environment's designed execution capabilities — binaries, scripts, macros, modules, or attacker-controlled commands fed into interpreters — including dual-use tooling when it executes attacker-controlled content. If FEC executes, a #7 step must be recorded at the execution moment (see R-EXEC).

### #8 Physical Attack

- **Strategic ID:** #8
- **Operational root ID:** TLCTC-08.00
- **Name:** Physical Attack
- **Definition:** Unauthorized physical interaction with or interference to hardware, facilities, media, interfaces, or signals—via direct contact or exploitation of physical phenomena/emanations.
- **Attacker's view:** "I abuse the physical accessibility or properties of hardware, devices, and signals."
- **Generic vulnerability:** Physical accessibility of infrastructure and the exploitability of physical-layer properties.
- **Topology:** Bridge (Physical → Cyber).

The cluster spans direct contact with hardware, facilities, media, and interfaces (including removable media) as well as exploitation of physical-layer properties such as wireless spectrum, emanations, and environmental dependencies.

### #9 Social Engineering

- **Strategic ID:** #9
- **Operational root ID:** TLCTC-09.00
- **Name:** Social Engineering
- **Definition:** An attacker psychologically manipulates individuals into performing actions counter to their best interests.
- **Attacker's view:** "I abuse human trust and psychology."
- **Generic vulnerability:** Humans can be influenced into unsafe actions or decisions.
- **Topology:** Bridge (Human → Cyber).

The cluster covers psychological manipulation that causes a human to disclose information, grant access, execute content, modify configuration, or bypass procedures. #9 is only the human manipulation step; subsequent technical steps map to their own clusters. Technical vulnerabilities are never #9.

### #10 Supply Chain Attack

- **Strategic ID:** #10
- **Operational root ID:** TLCTC-10.00
- **Name:** Supply Chain Attack
- **Definition:** An attacker compromises systems by targeting vulnerabilities within third-party software, hardware, services, or update mechanisms that are trusted and integrated by the target.
- **Attacker's view:** "I abuse the trust in third-party components."
- **Generic vulnerability:** Trust in third-party components and update channels can be subverted.
- **Topology:** Bridge (Third-party → Organization).

The cluster is placed at the Trust Acceptance Event (TAE) — the moment the organization's domain honors the third-party trust link and treats a trust artifact or decision as authoritative (validate, accept, install, apply, execute, or attach privileges). Downstream effects map normally, often `#10 → #7` or `#10 → #1` (see R-SUPPLY).

## 5. The Ten Axioms

The framework relies on non-negotiable axioms as constraints on interpretation. They prevent category errors and ensure that independent practitioners classify the same situation the same way, making analysis comparable, auditable, and operationally useful. Each axiom statement below is reproduced verbatim from the canonical framework dictionary (`tlctc-framework.v2.3.json`), with one clarifying sentence drawn from the canonical axioms section.

The axioms fall into four groups: scope (I–II), separation (III–V), classification (VI–VIII), and sequence (IX–X).

**Axiom I — No System-Type Differentiation.** The framework is generic and applies to all IT systems; it does not differentiate by system type. Sector labels (e.g., SCADA, IoT, cloud, medical devices) do not create new threat classes; they only change the specific vulnerabilities and controls at the operational level.

**Axiom II — Client–Server as the Universal Interaction Model.** All networked systems can be abstracted as client-server interaction. The clusters address the generic vulnerabilities arising from these interactions, independent of protocol or architecture depth.

**Axiom III — Threats Are Causes, Not Outcomes.** Threats are on the cause side; outcomes and events are not threats. Threat clusters must not be conflated with data risk events such as Loss of Confidentiality, Integrity, or Availability/Accessibility.

**Axiom IV — Threats Are Not Threat Actors.** Threat clusters are separate from threat actors. Actor identity (attribution, motivation, capability) is not a structuring element for threat categorization; TLCTC classifies actions and exploited generic vulnerabilities, not "who."

**Axiom V — Control Failure Is Not a Threat.** Control failures are not threats. Control failure is control-risk; risk remains structured as Threat → Event/Incident → Consequences, and controls influence likelihood and impact but do not define the threat cluster.

**Axiom VI — One Step, One Generic Vulnerability, One Cluster.** For every generic vulnerability, there is one threat cluster (non-overlap). Every distinct attack step exploits exactly one generic vulnerability in the attack surface, and each generic vulnerability maps to exactly one cluster.

**Axiom VII — Attack Vectors Are Defined by the Initial Generic Vulnerability.** Each distinct attack vector is defined by the generic vulnerability it initially targets. Classification is anchored in this initial cause, not in technique labels or downstream effects.

**Axiom VIII — Strategic vs Operational Layering.** Top-level clusters have sub-threats (strategic vs operational layering). This separates a stable Strategic Management Layer (clusters / generic vulnerabilities) from an Operational Security Layer (specific vulnerabilities, techniques, and procedures).

**Axiom IX — Clusters Chain into Attack Paths; Δt Expresses Velocity.** Clusters can be used in sequence to describe an attack path; Δt measures velocity. The time between successive cluster steps is a scenario attribute (Δt), and the set of Δt values expresses the attack velocity of the path.

**Axiom X — Credentials Have Dual Operational Nature.** Credentials are system control elements; acquisition and application are distinct steps. Acquisition (credential as data) maps to the enabling cluster, while application (presenting the credential to authenticate) always maps to #4 Identity Theft.

## 6. Classification Rules

The classification rules operationalize the axioms, resolving recurring boundary questions so that assignment remains reproducible. Each rule statement below is reproduced verbatim from the canonical framework dictionary (`tlctc-framework.v2.3.json`), together with its enforcement level. All fourteen rules carry the enforcement level **must**. Two are machine-enforceable (R-EXEC, R-INTRA-9); the remainder are enforced through analyst judgment guided by the stated rule.

The rules are presented in two groups: the six core rules, and the eight v2.1 extension rules covering transit, intra-system boundaries, and unresolved steps.

### 6.1 Core Rules

**R-EXEC** (must, machine-enforceable). If Foreign Executable Content executes, a #7 step MUST be recorded at the execution moment.

**R-ROLE** (must). Classify by the role of the component containing the flaw relative to the attacker: server-role flaw = #2, client-role flaw = #3.

**R-FLOOD** (must). If the primary mechanism is volume or intensity exhausting finite resources, classify as #6. If it is an implementation defect causing crash/hang/degradation, classify as #2 or #3 per R-ROLE.

**R-SUPPLY** (must). #10 Supply Chain Attack MUST be placed at the Trust Acceptance Event (TAE) — the moment the third-party trust link is honored and the trust artifact becomes authoritative inside the target domain.

**R-MITM** (must). Position acquisition maps to the enabling cluster; once position is established, interception/modification/relay actions map to #5.

**R-CRED** (must). Credential acquisition maps to the enabling cluster. Credential application (use of the credential to authenticate) is ALWAYS classified as #4 Identity Theft, regardless of the acquisition method. These are separate attack steps.

### 6.2 v2.1 Extension Rules

**R-TRANSIT-3** (must). Vendor code running on the target device is NOT transit. Software executing on the victim's own device is the attack surface, classified by R-ROLE (typically #3), not a transit (relay/carrier) party.

**R-INTRA-7** (must). Intra-system boundary crossings never change cluster classification. They are observability annotations, not classification inputs.

**R-INTRA-9** (must, machine-enforceable). The 'memory' intra-system boundary type is deferred and MUST NOT be used.

**R-UNRES-2** (must). '?' and '…' are epistemic annotations, NOT clusters. They have no generic vulnerability, do not appear in cluster definitions, and must not be referenced as if they were '#11'/'#12'.

**R-UNRES-3** (must). '?'/'…' are excluded from statistics — they represent absence of knowledge, not a category.

**R-UNRES-5** (must). DRE tags ('+ [DRE: ...]') MUST NOT be appended to '?'/'…'. Without a classified cluster there is no causal basis for asserting a data risk event in the notation.

**R-UNRES-8** (must). Any path containing '?'/'…' MUST carry a prose annotation explaining what is unresolved and why.

**R-UNRES-9** (must). Binary rule: if any cluster can be defended — even weakly — use '#X [conf=low]', not '?'. Reserve '?'/'…' for genuine 'we know something happened, we don't know what' situations.

## 7. Attack-Path Notation

A complete intrusion is expressed as an **attack path**: an ordered list of attack steps, each mapping to exactly one cluster (Axiom VI), connected by operators. A path is read left-to-right as best-estimate chronological progression. This section defines only the primitives needed to *read* a path; the formal grammar lives in the whitepaper §11.7 and the `grammar/` ABNF.

### 7.1 Sequence and Parallel

The **sequence operator** `→` means the right-hand step occurs after, and is enabled by, the left-hand step:

```
#9 → #4 → #1 → #7
```

The **parallel operator** `+`, always inside parentheses, denotes effectively concurrent steps whose ordering is not meaningful — for example enabling persistence while executing a payload:

```
#4 → (#1 + #7)
```

Each element of a parallel group is still a separate step and must be a single cluster reference. If an order exists — even a fast one — use `→` rather than `+`.

### 7.2 Velocity (Δt)

A Δt annotation attaches to the sequence operator and records the elapsed time between two steps:

```
#9 →[Δt=2h] #4 →[Δt=5m] #1 →[Δt=instant] #7
```

The set of Δt values across a path expresses its **attack velocity** (Axiom IX). Four velocity classes group transitions by time scale and by the defense mode that can realistically operate at that speed:

| Class | Δt scale | Primary defense mode |
| --- | --- | --- |
| **VC-1: Strategic** | days → months | log retention, threat hunting |
| **VC-2: Tactical** | hours | SIEM alerting, analyst triage |
| **VC-3: Operational** | minutes | automation (SOAR/EDR), rapid containment |
| **VC-4: Real-Time** | seconds → ms | architecture, rate limits, automatic isolation |

A transition at VC-3 or faster is structurally too fast for purely human response at that edge; defense must be automated or architectural.

### 7.3 Domain Boundary Operator

The domain boundary operator makes a **responsibility-sphere transition** explicit. It annotates the boundary-crossing step (it is never a step on its own) and is required for the bridge clusters #8, #9, #10:

```
||[context][@Source→@Target]||
```

`[context]` names the channel (e.g. `update`, `auth`, `human`, `physical`); `@Source` and `@Target` are the originating and receiving spheres. For example, a supply-chain update accepted and then executed:

```
#10 ||[update][@Vendor→@Org]|| → #7
```

### 7.4 Transit Operator (v2.1)

The **transit operator** `⇒` marks a sphere that *carries or relays* the attack but is neither its source nor its target. It appears inside a domain boundary operator and never changes cluster classification. Chained transit reads **right-to-left** (the rightmost carrier delivers to the target):

```
#9 ||[human][@Attacker⇒@SMSProvider→@Victim]||
#5 ||[signaling][@Attacker⇒@CarrierB(SS7)⇒@CarrierA→@Target]||
```

Transit (`⇒`, a passive relay) is distinct from #10 (the Trust Acceptance Event, where a trust artifact becomes authoritative inside the target domain). Per R-TRANSIT-3, vendor code running on the target device is the attack surface (classified by R-ROLE, typically #3), not transit.

### 7.5 Intra-System Boundary Operator (v2.1)

The **intra-system operator** `|[type][@from→@to]|` (single pipes) marks a boundary crossing *within a single host*. There are four defined types — `sandbox`, `privilege`, `process`, `hypervisor` (the `memory` type is deferred per R-INTRA-9). These are observability annotations only and never change classification (R-INTRA-7):

```
#3 |[sandbox][@renderer→@os]|
#2 |[privilege][@user→@root]|
#2 |[hypervisor][@guest→@host]|
#7 |[process][@malware→@lsass]|
```

### 7.6 Data Risk Event Tags

A DRE tag records an **outcome** — never a step — appended with `+ [DRE: …]`, using C (Confidentiality), I (Integrity), and A (Availability/Accessibility). When the distinction is operationally relevant, use `Av` (data gone or unreachable) versus `Ac` (data present but unusable, e.g. ransomware encryption):

```
#6 + [DRE: Av]            availability loss after a flood — service unreachable
#2 → #7 + [DRE: Ac]       execution leading to ransomware encryption
```

### 7.7 Epistemic States and Unresolved Steps

Incident analysis is iterative, so a path may mix four epistemic states for a step:

| State | Syntax | Use when |
| --- | --- | --- |
| Classified | `#X` | cluster assigned, evidence supports it |
| Low-confidence | `#X [conf=low]` | best-supported cluster, explicit caveat |
| Inferred | `#X [inferred]` | not observed but logically required |
| Unresolved | `?` or `…` | something happened, no cluster defensible |

The **unresolved-step operators** are `?` (exactly one step occurred, cluster unknown) and `…` (a gap of one or more steps, both count and clusters unknown). Per R-UNRES-9, if *any* cluster can be defended — even weakly — use `#X [conf=low]` rather than `?`. Unresolved operators are epistemic annotations, not clusters (R-UNRES-2): they are excluded from statistics, never carry DRE tags, and every path containing one must carry a prose note explaining what is unresolved.

```
#3 →[Δt=0s] #7 →[Δt=4h] ? →[Δt=<10m] #4 → #1
```

### 7.8 Worked Examples

Pegasus network injection — a carrier relays the redirection (transit), Safari on the device is the exploited client (#3 with an internal privilege crossing), and the payload execution is #7:

```
#5 ||[network][@NSO_Operator⇒@MobileCarrier→@Target]|| →[Δt≈0s]
#3 ||[browser][@NSO(free247downloads.com)→@Target(Safari)]|| |[privilege][@user→@root]| →[Δt≈0s]
#7 + [DRE: C]
```

OAuth phishing — email and identity providers are topological intermediaries; the use of coerced authorization is #4, and subsequent abuse of legitimate cloud functions is #1:

```
#9 ||[email][@Attacker⇒@Microsoft(M365)→@Target]|| →[Δt=hours]
#4 ||[auth][@Attacker⇒@AzureAD.OAuth→@Target(CloudResources)]|| →[Δt≈0s]
#1 + [DRE: C]
```

## 8. Glossary

<filled by Task 10>

## 9. References

<filled by Task 11>
