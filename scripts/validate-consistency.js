#!/usr/bin/env node
/*
 * validate-consistency.js — Cross-artifact drift checks against the canonical
 * dictionary (json-schemas/layer-1/tlctc-framework.v2.5.json). Part of `npm run validate`.
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

const fw = readJSON('json-schemas/layer-1/tlctc-framework.v2.5.json');
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

const core = read('documentation/tlctc-v2.5-core.md');
for (const id of ruleIds) if (!new RegExp(`\\*\\*${id}\\*\\*`).test(core)) note(`core paper: rule ${id} not defined in bold`);
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

// ───────────────────────── report ────────────────────────────────────────────
console.log(`Consistency: ${clusterIds.length} clusters, ${fw.axioms.length} axioms, ${N} rules (${K} core + ${X} extension), DRE codes [${dre || '-'}]`);
if (findings.length) {
  console.log(`DRIFT — ${findings.length} finding(s):`);
  for (const f of findings) console.log('  ' + f);
  process.exit(1);
}
console.log('VALID — derived artifacts agree with the dictionary.');
