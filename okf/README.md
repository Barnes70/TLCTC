# TLCTC Open Knowledge Format (OKF) bundle

This directory is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
bundle (SPEC v0.1): a tree of markdown files with YAML frontmatter, built so both humans and
LLM agents can consume the TLCTC taxonomy. It is a **rendered view** — the canonical sources
(JSON schemas in `json-schemas/`, documentation in `documentation/`, tools in `tools/`) remain
the single source of truth.

## Regenerate

```bash
node scripts/build-okf.js
node scripts/validate-okf.js okf/
```

## Contents

Generated from TLCTC v2.3. 412 concept documents across
9 sections (clusters, axioms, rules, spheres, contexts, glossary, attack-paths,
controls, mappings).

## Provenance notes

- Cluster bodies render the whitepaper §4.1 six-field definitions.
- Control docs combine NIST CSF objectives (normative) with ISO 27001:2022 Annex A *starter*
  controls (AI-assisted, from `tools/`) — guidance, not a certified control set.
- CWE mappings are AI-generated and experimental.

## License

CC BY 4.0 — see [../LICENSE](../LICENSE).
