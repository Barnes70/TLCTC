#!/usr/bin/env node
/*
 * validate-consistency.js — Cross-artifact drift checks against the canonical
 * dictionary (json-schemas/layer-1/tlctc-framework.v2.7.json). Part of `npm run validate`.
 *
 * The dictionary is the single source of truth; several derived artifacts repeat
 * its facts (rule count, DRE code list, cluster strings). This script fails when
 * any of them drifts, so a canon change cannot land half-propagated.
 *
 * Checks
 *   1. Layer-3 schema: every `outcomes` enum == dictionary DRE codes.
 *   2. ABNF grammars: DRE_LET alternatives == dictionary DRE codes.
 *   3. Rule registry: counts quoted in README / glossary / core paper match; every
 *      rule id appears in the glossary quick reference and the core paper.
 *   4. Integration enums (Cortex XSOAR DRE fields, tools/README example) == DRE codes.
 *   5. Cluster canon: each cluster's definition, attackers_view and
 *      generic_vulnerability string appears verbatim in the core paper.
 *   6. Dictionary shape: 10 clusters, 10 axioms.
 *
 * Exit: 0 = consistent, 1 = drift found (each finding printed).
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const read = (rel) => fs.readFileSync(path.join(ROOT, rel), 'utf8');
const readJSON = (rel) => JSON.parse(read(rel));
const exists = (rel) => fs.existsSync(path.join(ROOT, rel));

const fw = readJSON('json-schemas/layer-1/tlctc-framework.v2.7.json');
const findings = [];
const note = (s) => findings.push(s);
const sameSet = (a, b) => a.length === b.length && [...a].sort().join('|') === [...b].sort().join('|');

// ───────────────────────── 6. shape ──────────────────────────────────────────
const clusterIds = Object.keys(fw.clusters);
if (clusterIds.length !== 10) note(`dictionary: expected 10 clusters, found ${clusterIds.length}`);
if (fw.axioms.length !== 10) note(`dictionary: expected 10 axioms, found ${fw.axioms.length}`);

// ───────────────────────── 1. DRE codes vs Layer-3 schema ────────────────────
const dre = fw.data_risk_events ? fw.data_risk_events.codes.map((c) => c.code) : null;
if (!dre) note('dictionary: data_risk_events section missing');
else {
  const schema = readJSON('json-schemas/layer-3/tlctc-attack-path.schema.json');
  const enums = [];
  (function walk(o, p) {
    if (!o || typeof o !== 'object') return;
    if (p.endsWith('/outcomes') && o.items && Array.isArray(o.items.enum)) enums.push({ p, e: o.items.enum });
    for (const [k, v] of Object.entries(o)) walk(v, `${p}/${k}`);
  })(schema, '');
  if (!enums.length) note('layer-3 schema: no outcomes enum found');
  for (const { p, e } of enums) if (!sameSet(e, dre)) note(`layer-3 schema ${p}: enum [${e}] != dictionary DRE codes [${dre}]`);

  // ─────────────────────── 2. grammars ───────────────────────────────────────
  for (const g of ['grammar/tlctc-attack-path.abnf', 'grammar/tlctc-plus-attack-path.abnf']) {
    if (!exists(g)) { note(`${g}: missing`); continue; }
    const m = /^DRE_LET\s*=\s*([^\n;]+)/m.exec(read(g));
    if (!m) { note(`${g}: DRE_LET rule not found`); continue; }
    const toks = [...m[1].matchAll(/"([A-Za-z]+)"/g)].map((x) => x[1]);
    if (!sameSet(toks, dre)) note(`${g}: DRE_LET [${toks}] != dictionary DRE codes [${dre}]`);
  }

  // ─────────────────────── 4. integration enums ──────────────────────────────
  const enumFiles = [
    ['integrations/cortex-xsoar/incident-fields/tlctc-fields.json', /"selectValues":\s*\[([^\]]*)\]/g],
    ['integrations/cortex-xsoar-8/IncidentFields/incidentfield-tlctcdre.json', /"selectValues":\s*\[([^\]]*)\]/g],
    ['tools/README.md', /"types":\s*\[([^\]]*)\]/g],
  ];
  for (const [rel, re] of enumFiles) {
    if (!exists(rel)) continue;
    const txt = read(rel);
    let m, found = false;
    while ((m = re.exec(txt))) {
      const vals = [...m[1].matchAll(/"([^"]+)"/g)].map((x) => x[1]);
      // only lists that look like DRE lists (subset of letters)
      if (!vals.every((v) => /^[A-Z][a-z]?$/.test(v))) continue;
      found = true;
      if (!sameSet(vals, dre)) note(`${rel}: DRE list [${vals}] != dictionary [${dre}]`);
    }
    if (!found) note(`${rel}: no DRE list found to check`);
  }
}

// ───────────────────────── 3. rules ──────────────────────────────────────────
const ruleIds = fw.rules.map((r) => r.rule_id);
const extIds = ruleIds.filter((id) => /^R-(TRANSIT|INTRA|UNRES)-/.test(id));
const coreIds = ruleIds.filter((id) => !extIds.includes(id));
const N = ruleIds.length, K = coreIds.length, X = extIds.length;

const readme = read('README.md');
for (const m of readme.matchAll(/\b(\d+)\s+(classification\s+)?rules\b/g)) {
  if (Number(m[1]) !== N) note(`README.md: says "${m[0]}", registry has ${N}`);
}
const glossary = read('documentation/tlctc-glossary.md');
const gm = /exactly \*\*(\d+) rules\*\*/.exec(glossary);
if (!gm) note('glossary: "exactly **N rules**" sentence not found');
else if (Number(gm[1]) !== N) note(`glossary: says exactly ${gm[1]} rules, registry has ${N}`);
const cm = /\*\*Core rules \((\d+)\):\*\*/.exec(glossary);
if (cm && Number(cm[1]) !== K) note(`glossary: "Core rules (${cm[1]})", registry has ${K} core rules`);
const em = /extension rules \((\d+)\):\*\*/.exec(glossary);
if (em && Number(em[1]) !== X) note(`glossary: "extension rules (${em[1]})", registry has ${X}`);
for (const id of ruleIds) if (!new RegExp(`\\*\\*${id}\\*\\*`).test(glossary)) note(`glossary quick reference: ${id} missing`);

const core = read('documentation/tlctc-v2.7-core.md');
for (const id of ruleIds) if (!new RegExp(`\\*\\*${id}\\*\\*`).test(core)) note(`core paper: rule ${id} not defined in bold`);
for (const r of fw.rules) if (!core.includes(r.statement)) note(`core paper: rule ${r.rule_id} statement not reproduced verbatim`);
const words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve'];
const wm = /the (\w+) core rules \(([^)]+)\)/.exec(core);
if (!wm) note('core paper: "the N core rules (...)" sentence not found');
else {
  if (wm[1] !== words[K] && Number(wm[1]) !== K) note(`core paper: says "the ${wm[1]} core rules", registry has ${K}`);
  const listed = wm[2].split(',').map((s) => s.trim());
  for (const id of coreIds) if (!listed.includes(id)) note(`core paper: core rule list lacks ${id}`);
}

// ───────────────────────── 5. cluster canon verbatim ─────────────────────────
for (const [id, c] of Object.entries(fw.clusters)) {
  for (const field of ['definition', 'attackers_view', 'generic_vulnerability']) {
    if (!core.includes(c[field])) note(`core paper: ${id} ${field} not reproduced verbatim`);
  }
}

// ───────────────────────── 7. consequence chain (v2.7 C1–C3) ─────────────────
// A Δt exists only on causal transitions; a BRE is reached by a causal or a
// normative edge. These phrases said otherwise and must not come back.
const CHAIN_DOCS = [
  'documentation/tlctc-v2.7-core.md',
  'documentation/tlctc-v2.7-application.md',
  'documentation/tlctc-glossary.md',
  'documentation/tlctc-v2.0-whitepaper.md',
  'documentation/tlctc-layered-event-modelling.md',
  'documentation/images/tlctc-consequence-chain.svg',
];
const RETIRED_CHAIN_PHRASES = [
  /every transition carries its own Δt/i,
  /every Δt (is )?a detection/i,
  /Δt detection windows at every transition/i,
  /triggered by a (DRE|Data Risk Event)/i,
  /each (BRE→BRE )?transition (has|carries|having) its own Δt/i,
  /has its own \*\*Δt\*\* — a detection and intervention window/i,
  /Δt (representing|is) a detection/i,
  /notification obligation triggered/i,
  /Every transition \(SRE→DRE/i,
  /distinguishable by inspecting the record itself/i, // v2.7 C4: the stopping rule reads the record's present standing
  /Every node is a risk event/i, // Figure 3 draws the clusters, which are causes, not events
];
for (const rel of CHAIN_DOCS) {
  if (!exists(rel)) { note(`${rel}: missing`); continue; }
  const txt = read(rel);
  for (const p of RETIRED_CHAIN_PHRASES) if (p.test(txt)) note(`${rel}: retired consequence-chain phrase "${p.source}" (v2.7 C1/C2)`);
}
const cc = fw.consequence_chain;
if (!cc) note('dictionary: consequence_chain section missing (v2.7 C3)');
else if (!core.includes(cc.business_risk_event.definition)) note('core paper: BRE definition not reproduced verbatim from consequence_chain');

// ───────────────────────── 8. Layered Event Modelling paper ──────────────────
// The LEM paper is the method; TLCTC is its instance. It quotes the canon
// verbatim and carries no draft residue. Tasks append to both lists.
const LEM_PATH = 'documentation/tlctc-layered-event-modelling.md';
const LEM_FORBIDDEN = [
  'Changes in v0.',
  'Draft v0.',
  'Earlier drafts',
  'An earlier version of this framework',
  'P4 replaces a weaker earlier test',
  'because v0.5 named it',
  '## 11. A conjecture',
  'Generality beyond it ',
  'unauthorised actor',
  'unauthorised agent',
  'authorised agent',
  'authorised control envelope',
  'Fraud / integrity',
  'facility risk event',
  'Facility risk event',
  'A future revision should',
  '$$',
  '\\mathbb',
  '(Figure in the web edition.)',
];
const LEM_REQUIRED = [
  '**Version:** 1.0',
  '**License:** CC BY 4.0',
  'orcid.org/0009-0005-2148-9903',
  '### N6 — A conjecture beyond risk modelling',
  '## Development history',
  '## Declarations',
  '### 9.4 A worked case: possession',
  'DCS_d = TTD_P90 / Δt',
  'Δt is the duration of a transition, carried by the causal edge along which one event brings about the next; it is not the time between any two timestamps.',
  '**E0 — Structure routing.**',
  'A rack loses power',
  '11. Further S2 levels',
];
if (!exists(LEM_PATH)) note(`${LEM_PATH}: missing`);
else {
  const lem = read(LEM_PATH);
  for (const p of LEM_FORBIDDEN) if (lem.includes(p)) note(`LEM paper: forbidden text "${p}"`);
  for (const p of LEM_REQUIRED) if (!lem.includes(p)) note(`LEM paper: required text missing "${p}"`);
  const sre = fw.system_risk_event.types[0].definition;
  if (!lem.includes(sre)) note('LEM paper: System Compromise definition not quoted verbatim from the dictionary');
  if (fw.consequence_chain && !lem.includes(fw.consequence_chain.business_risk_event.definition)) note('LEM paper: BRE definition not quoted verbatim from consequence_chain');
  for (const c of fw.data_risk_events.codes.filter((x) => !x.refinements || x.refinements.length === 0)) {
    if (!lem.includes(c.name)) note(`LEM paper: DRE code ${c.code} name "${c.name}" missing`);
    if (!lem.includes(c.property)) note(`LEM paper: DRE code ${c.code} property "${c.property}" missing`);
  }
}

// ───────────────────────── 9. version pins (v2.7 final review) ───────────────
// Documents that claim to be the current version must name the dictionary's
// version; provenance tags (*(v2.6)*, "since v2.6") are not matched here.
const ver = fw.metadata.tlctc_version;
const appTxt = exists('documentation/tlctc-v2.7-application.md') ? read('documentation/tlctc-v2.7-application.md') : '';
for (const [label, txt] of [['core paper', core], ['application paper', appTxt], ['glossary', glossary]]) {
  for (const m of txt.matchAll(/(?:v(\d+\.\d+) normative registry|normative rule registry of v(\d+\.\d+)|TLCTC v(\d+\.\d+) core paper)/g)) {
    const v = m[1] || m[2] || m[3];
    if (v !== ver) note(`${label}: registry version pin "${m[0]}" != dictionary v${ver}`);
  }
}
const pin = glossary.match(/mirrors the canonical dictionary \(`tlctc-framework\.v(\d+\.\d+)\.json`\)/);
if (!pin || pin[1] !== ver) note(`glossary: canonical-dictionary filename pin ${pin ? 'v' + pin[1] : 'missing'} != v${ver}`);
if (exists(LEM_PATH)) {
  const lemTxt = read(LEM_PATH);
  if (!lemTxt.includes(`TLCTC framework specification v${ver}`)) note(`LEM paper: missing "TLCTC framework specification v${ver}"`);
  if (!lemTxt.includes(`version ${ver}. Zenodo`)) note(`LEM paper: missing "version ${ver}. Zenodo"`);
}

// ───────────────────────── report ────────────────────────────────────────────
console.log(`Consistency: ${clusterIds.length} clusters, ${fw.axioms.length} axioms, ${N} rules (${K} core + ${X} extension), DRE codes [${dre || '-'}]`);
if (findings.length) {
  console.log(`DRIFT — ${findings.length} finding(s):`);
  for (const f of findings) console.log('  ' + f);
  process.exit(1);
}
console.log('VALID — derived artifacts agree with the dictionary.');
