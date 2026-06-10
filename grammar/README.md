# TLCTC Grammar

Machine-ingestable formal grammar for TLCTC attack path notation.

## Files

| File | Contents |
| --- | --- |
| `tlctc-attack-path.abnf` | ABNF (RFC 5234) grammar for the **core** attack-path notation, covering v2.0 core, v2.1 extensions (transit, intra-system boundaries, unresolved-step operators), and the v0.1 TLCTC+ free-text BRE annotation |
| `tlctc-plus-attack-path.abnf` | ABNF grammar for **TLCTC+ v0.6 records** — adds `+ [SRE]`, `+ [DRE: ...]` (already in core), `+ [BRE: BRE-XXX.YY ...]` (structured codes only), `+ [Impact: ...]`, `+ [Report: ...]`, and the cause-side `[Pattern: PATTERN-XXX.YY]` step annotation. Enforces R-9-BOUNDARY (bridge clusters #8/#9/#10 require boundary) and R-PATTERN-POSITION (Pattern is bracket-only) at the grammar level. |

The canonical *prose* specifications live in:

- `documentation/tlctc-v2.0-whitepaper.md` §11.7 — core attack-path grammar
- `documentation/tlctc-plus-specification.md` §8 — TLCTC+ v0.6 grammar

This directory is the machine-readable mirror.

### Which grammar to use

- For plain TLCTC v2.1 attack paths or v0.1-style records with free-text BRE labels → `tlctc-attack-path.abnf`.
- For TLCTC+ v0.6 records (record_type `compromise_record` or `pure_9_record`) with structured PATTERN/BRE/IMPACT/REPORT codes → `tlctc-plus-attack-path.abnf`. v0.6 collapsed the v0.3-v0.5 three-class enumeration into the two structural types above, split on SRE presence.

## What It Covers

The grammar accepts any syntactically well-formed attack path string, including:

- Strategic cluster refs (`#1`–`#10`) and operational refs (`TLCTC-01.01`)
- Sequential edges with velocity annotations (`→[Δt=5m]`)
- Parallel groups `(#X + #Y)`, including group-level DRE tags (`(#1 + #7) + [DRE: Ac]`)
- Inter-organizational boundaries `||[context][@A→@B]||` with transit chains (`@A⇒@Carrier→@B`)
- Intra-system boundaries `|[sandbox][@renderer→@os]|`
- Unresolved-step operators `?` and `…`
- Step annotations (`[conf=low]`, `[inferred]`, `[evidence=...]`)
- Data risk events (`+ [DRE: C, I, A, Av, Ac]`)
- Business risk events (`+ [BRE: <label>]`) — TLCTC+ additive consequence-side annotation; see [`documentation/tlctc-plus-ncsc-proposal.md`](../documentation/tlctc-plus-ncsc-proposal.md)

## What It Does Not Cover

The grammar checks **syntax only**. Semantic rules from the whitepaper (e.g., R-EXEC, R-CRED, R-SUPPLY, R-UNRES-5, single-cluster rule, topology constraints) are not enforceable with ABNF alone — they require a validator built on top of the parser.

A string that parses against this grammar may still be **non-conformant**. Implementations SHOULD layer a linter/validator over the parser.

## Integration Showcase

### 1. Syntax validation with `apg-js` (Node.js)

```bash
npm install apg-js
npx apg-api grammar/tlctc-attack-path.abnf -o parser.js
```

```js
import { Parser } from './parser.js';
const p = new Parser();
const ok = p.parse('#4 → (#1 + #7) + [DRE: Ac]');
console.log(ok ? 'valid' : 'syntax error');
```

### 2. Pre-commit hook for attack-path JSON contributions

Extract each `sequence[].notation`-equivalent rendering from the Layer 3 JSON and feed it to the parser before accepting a PR:

```bash
# .github/workflows/grammar-check.yml (sketch)
- run: npx tlctc-abnf-check attack-paths/*.json --grammar grammar/tlctc-attack-path.abnf
```

### 3. SIEM / ingest pipeline

Pin a schema version per event and reject events whose `tlctc_path` field does not parse. Useful for catching operator typos (`||` vs `|`, `⇒` vs `→`) at ingest rather than at analysis time.

### 4. Editor support

The ABNF can be compiled to a tree-sitter / TextMate grammar for syntax highlighting and folding of attack path strings in CTI reports and incident tickets.

### 5. Round-trip testing

Parse → AST → render → re-parse. Any Layer 3 instance that round-trips to an identical string is serialization-stable. This is the cheapest guard against rendering drift in tools.

## Versioning

The grammar version tracks the whitepaper. When the whitepaper updates §11.7, this file updates in the same commit. The header comment records the framework version this grammar targets.

## Limitations & Known Gaps

- **Unicode literals:** The grammar uses `→`, `⇒`, `…`, `Δ` directly. RFC-5234-strict parsers require hex UTF-8 substitution; most modern ABNF tools (apg, abnfgen) accept literal UTF-8.
- **No ASCII alias for `⇒`:** V2.1 transit arrow has no ASCII form today; all transit-bearing paths must be UTF-8.
- **Whitespace:** `SP*` permits zero or more spaces between most tokens; this is intentional for authoring flexibility but means pretty-printing is an implementation concern.

## License

CC BY 4.0 — aligned with the rest of the TLCTC project.
