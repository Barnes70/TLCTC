# MITRE ATLAS → TLCTC Classification Decision Tree

How an ATLAS technique is placed in `tlctc-atlas.json`, and how to classify a technique a future
ATLAS release adds. The AI-specific questions come first; whatever passes through them is
classified by the ATT&CK decision tree (`../mitre-attack-enterprise/decision-tree.md`), because
an AI system is a system and the ten clusters do not change for it (Axiom I).

## Q0 — Is there a victim system in the step at all?

```
Reconnaissance held by public sources (papers, blogs, code and app repositories, victim-owned
websites, internet-scan services, identity OSINT)
      → N/A: nothing of the victim's is touched (as ATT&CK T1589–T1594, T1596, T1597).
Reconnaissance that interacts with a victim system (Active Scanning and its sub-techniques:
enumerating hosted resources, metadata APIs, exposed AI infrastructure, agent trigger channels;
a "gather" technique performed by querying the system)
      → Q1: it classifies like any other step, normally #1 with a DRE C (as ATT&CK T1595).
Reconnaissance that elicits information from a person
      → #9 (as ATT&CK T1598 Phishing for Information); a credential learned this way is an
        Enabling Condition, its later use #4 (R-CRED).
Resource Development, AI Attack Staging (proxy models, adversarial data, deepfakes, generated
commands, prompt and retrieval-content crafting), publishing poisoned datasets / models / tools /
hallucinated entities, reputation inflation
      → N/A: attacker-side; the step is recorded when the artefact meets a victim system.
External Harms (financial, reputational, societal, user, IP theft)
      → N/A: Business Risk Events on the consequence side, never causes (Axiom III).
Everything else → Q1.
```

An umbrella technique whose description spans both an OSINT and a direct branch (Gather RAG-Indexed
Targets, Gather Victim Identity Information) keeps `N/A` as its row value, as the ATT&CK mapping does
for T1589–T1592, and names the classified branches in its rationale; `N/A` never appears inside an
alternative.

## Q1 — Is the AI component the thing exploited, or just the thing reached?

Ask what the model or agent did: if it did what it was designed to do with an input it was
designed to accept, the AI component is the **capability vector** and the step is classified by
the designed function that was abused.

```
Prompt injection (direct, indirect, triggered), jailbreak, prompt obfuscation, delayed instructions,
RAG poisoning, false RAG entries, context/memory/thread poisoning, agent tool data poisoning,
agent clickbait, prompt infiltration via a public application, prompt self-replication,
trusted-output manipulation, chat-history manipulation, model evasion (adversarial input),
agent tool invocation, agent as C2 channel, agentic resource consumption
      → #1 Abuse of Functions. The generic vulnerability is the designed scope of the model's or
        agent's input, retrieval, generation and tool-use functions. The agent is not the actor
        (Axiom IV); the SRE is recorded at the injection (agent theses).
Discovery of model family, ontology, outputs, hallucinations, system prompt, agent configuration
      → #1: a designed interface answers what it is willing to answer.
Exfiltration via the inference API (membership inference, inversion, extraction, system-prompt
and data leakage, response rendering, exfiltration via tool invocation)
      → #1: the API is used as designed; what is learned is a DRE C, never a cluster.
```

## Q2 — Was a trust artefact accepted from outside? (R-SUPPLY)

```
AI Supply Chain Compromise (hardware, software, data, model, container registry, agent tool),
poisoned agent tool adopted from a registry, rug pull of a trusted component
      → #10 at the Trust Acceptance Event.
        + #7 if the artefact executes code (software, container image, serialised model, R-EXEC)
        + #1 if the artefact carries instructions an agent then follows (agent tool)
        hardware → #10.3 (operational hint)
Poison Training Data → #1 | #10: written into a pipeline the attacker can reach (#1), or ingested
        as trusted third-party data (#10).
```

## Q3 — Did foreign executable content run? (R-EXEC)

```
Unsafe AI artefact loaded (pickle, notebook, plugin), malicious package installed, malware
embedded in a model, rogue agent deployed, local agent driven to execute attacker content
      → #7 at execution, with its enabler before it: #9 (user induced), #10 (trusted artefact),
        #1 (a deployment or code-execution function reached and used), #3 (drive-by).
Sandbox evasion → #7 (a feature of the payload, as ATT&CK T1497).
```

## Q4 — ATT&CK mirror?

```
Valid Accounts, Use Alternate Authentication Material, Application Access Token → #4 (R-CRED)
Exploit Public-Facing Application → #2; Drive-by Compromise → #3 → #7; Escape to Host → #1 | #2;
Exploitation for Credential Access / Defense Evasion → (#2 | #3) → #4 / → #7
Phishing (LLM-written, deepfake-assisted) → #9; Impersonation → #9
Command and Scripting Interpreter → #1 → #7; Masquerading → #1 | #7; Reverse Shell → #1 | #7
Unsecured Credentials → #1 → #4; OS Credential Dumping → #1 | #7
Process / Cloud Service Discovery, Data from Repositories / Local System → #1
AI Service API as C2 → #1 (as ATT&CK Web Service)
      → carried over verbatim from tlctc-enterprise-attack.json; the rationale names the analogue.
```

## Q5 — Is the effect a capacity problem? (R-SPECIFIC, capacity)

```
Denial of AI Service, Excessive Queries, Resource-Intensive Queries, Chaff Data
      → #6 where volume or intensity exhausts finite capacity;
        #1 where a designed (often metered) function is driven against its purpose below that point;
        #2 if a code defect is what fails (R-ROLE).
```

## Q6 — Physical world? (R-SPECIFIC, substrate)

```
Physical Environment Access
      → #1 where a crafted physical input is presented to a sensor that captures it as designed;
        #8 only where the system's own hardware or sensors are manipulated.
```

## Outcomes that are not steps

Poisoned model → `Ii`; eroded dataset → `Ii`; corrupted context → `Ii`; fabricated citations →
`If`; destroyed data via a tool → `Av`; extracted model, leaked training data or system prompt →
`C`; denied service → `Av`/`A`. Record them as Data Risk Events on the step that produced them.

## Worked examples

**OpenClaw (corpus flow): indirect prompt injection through a web page that an agent reads,
tool invocation, credential harvesting, exfiltration through a tool.** Q1 places every
model-facing action at #1; the derived TLCTC path is a run of #1 steps with `C` outcomes, which is
the path B / path D shape of the agentic-AI corpus.

**A poisoned model from a public hub that executes on load.** Q2: the hub download honoured as
trusted is #10 at the Trust Acceptance Event; Q3: the pickle executing is #7; `#10 → #7`.

**A membership-inference attack on a hosted model.** Q1: the inference API is queried as designed,
#1; the inferred training-set membership is a DRE C. No cluster for the outcome.
