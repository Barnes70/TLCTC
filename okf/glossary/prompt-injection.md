---
type: "term"
title: "Prompt Injection"
description: "Instructions placed in the input of a language model or agent — directly by the user, or indirectly in content the agent reads (web pages, documents, tool output) — so that the model acts on them."
resource: "tlctc:term:prompt-injection"
tags:
  - "glossary"
---
# Prompt Injection

Instructions placed in the input of a language model or agent — directly by the user, or indirectly in content the agent reads (web pages, documents, tool output) — so that the model acts on them. In TLCTC: `#1 Abuse of Functions`. Acting on natural-language input is the model's designed function; no implementation flaw is required, and natural-language instructions are not Foreign Executable Content. Jailbreaks, RAG or context poisoning and agent tool abuse classify the same way. Where the agent then executes code or commands whose content the attacker controls, the execution is `#7` (`#1 → #7`, R-EXEC); a flaw in the model-serving or agent software is `#2`/`#3`; a subverted third-party model, dataset or tool is `#10`. The agent is the attacker's capability vector, not the actor (Axiom IV).

**Reference:** Core paper §4 (#1); dictionary `fec.boundary`; MITRE ATLAS mapping (`mappings/mitre-atlas/`)

See also: Abuse of Functions (#1), Foreign Executable Content (FEC), AI / AGI / ASI (Positioning in TLCTC)
