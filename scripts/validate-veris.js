#!/usr/bin/env node
/*
 * validate-veris.js — Validate the VERIS → TLCTC mapping artefacts. Part of `npm run validate`.
 *
 *  1. mappings/veris/tlctc-veris.json parses; metadata.tlctc_version equals the dictionary's;
 *     every rule / axiom / cluster id / DRE code / partition row it names exists in the dictionary.
 *  2. Coverage: every value of the pinned VERIS enumeration under the covered paths has exactly
 *     one entry, and no entry names a value that is not in the enumeration.
 *  3. Field pairing per mapping_type (targets only for direct/conditional/chain, companion for
 *     chain, context for context, partition_row [+ basis | out_of_scope] for no-cluster, dre only
 *     for outcome, nothing extra for unresolved); partition_row 'attack' requires out_of_scope.
 *  4. veris_description equals the pinned labels text.
 *  5. The generated CSV is byte-identical to the generator output, LF only, no BOM.
 *  6. study/results.json, when present, names the mapping's `updated` date, the VCDB sha256
 *     listed in PINNED.md, and every table cell satisfies n <= denominator.
 *
 * Exit: 0 = valid, 1 = at least one failure (all failures printed).
 * Deps: Node builtins only.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const gen = require('./build-veris-mapping.js');

const ROOT = path.resolve(__dirname, '..');
const DIR = path.join(ROOT, 'mappings/veris');
const PINNED = path.join(DIR, 'pinned');
const RESULTS = path.join(DIR, 'study/results.json');

const failures = [];
const fail = (m) => failures.push(m);
const rel = (p) => path.relative(ROOT, p).split(path.sep).join('/');
const readJSON = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));

const COVERED_ACTION = {
  hacking: ['variety', 'vector', 'result'],
  malware: ['variety', 'vector', 'result'],
  social: ['variety', 'vector', 'result'],
  misuse: ['variety', 'vector', 'result'],
  physical: ['variety', 'vector', 'result'],
  error: ['variety', 'vector'],
  environmental: ['variety'],
  unknown: ['result'],
};
const COVERED_ATTRIBUTE = {
  confidentiality: ['data_disclosure'],
  integrity: ['variety'],
  availability: ['variety'],
};
const TYPES = ['direct', 'conditional', 'chain', 'context', 'no-cluster', 'outcome', 'unresolved'];
const ALLOWED_FIELDS = {
  direct: ['targets'],
  conditional: ['targets'],
  chain: ['targets', 'companion'],
  context: ['context'],
  'no-cluster': ['partition_row', 'basis', 'out_of_scope'],
  outcome: ['dre', 'certainty'],
  unresolved: [],
};
const BASE_FIELDS = ['veris_id', 'veris_description', 'mapping_type', 'rationale'];

// ---------------------------------------------------------------- load
const dictionary = readJSON(gen.DICTIONARY);
const mapping = readJSON(gen.MAPPING);
const enumJson = readJSON(path.join(PINNED, 'verisc-enum.json'));
const labels = readJSON(path.join(PINNED, 'verisc-labels.json'));

const rules = new Set(dictionary.rules.map((r) => r.rule_id));
const axioms = new Set(dictionary.axioms.map((a) => a.axiom_id));
const clusters = new Set(Object.keys(dictionary.clusters));
const dreCodes = new Set(dictionary.data_risk_events.codes.map((c) => c.code));
const rows = new Set(dictionary.cause_side_partition.rows.map((r) => r.row_id));

// ---------------------------------------------------------------- 1. metadata and ids
if (mapping.metadata.tlctc_version !== dictionary.metadata.tlctc_version) {
  fail(`metadata.tlctc_version ${mapping.metadata.tlctc_version} != dictionary ${dictionary.metadata.tlctc_version}`);
}
if (clusters.size !== 10) fail(`dictionary has ${clusters.size} clusters, expected 10`);
if (!/^\d{4}-\d{2}-\d{2}$/.test(mapping.metadata.created) || !/^\d{4}-\d{2}-\d{2}$/.test(mapping.metadata.updated)) {
  fail('metadata.created / metadata.updated must be ISO dates');
}
if (mapping.metadata.entry_count !== mapping.entries.length) {
  fail(`metadata.entry_count ${mapping.metadata.entry_count} != entries.length ${mapping.entries.length}`);
}

// ---------------------------------------------------------------- 2. coverage
const expected = new Map(); // veris_id -> label text
const labelOf = (parts) => parts.reduce((n, p) => (n && typeof n === 'object' ? n[p] : undefined), labels);
for (const [cat, fields] of Object.entries(COVERED_ACTION)) {
  for (const f of fields) {
    const values = enumJson.action[cat] && enumJson.action[cat][f];
    if (!Array.isArray(values)) { fail(`pinned enum lacks action.${cat}.${f}`); continue; }
    for (const v of values) {
      const l = labelOf(['action', cat, f, v]);
      expected.set(`action.${cat}.${f}.${v}`, typeof l === 'string' ? l : v);
    }
  }
}
for (const [cat, fields] of Object.entries(COVERED_ATTRIBUTE)) {
  for (const f of fields) {
    const values = enumJson.attribute[cat] && enumJson.attribute[cat][f];
    if (!Array.isArray(values)) { fail(`pinned enum lacks attribute.${cat}.${f}`); continue; }
    for (const v of values) {
      const l = labelOf(['attribute', cat, f, v]);
      expected.set(`attribute.${cat}.${f}.${v}`, typeof l === 'string' ? l : v);
    }
  }
}
expected.set('action.unknown', 'Action category not recorded');

const seen = new Map();
for (const e of mapping.entries) {
  if (seen.has(e.veris_id)) fail(`duplicate veris_id ${e.veris_id}`);
  seen.set(e.veris_id, e);
  if (!expected.has(e.veris_id)) fail(`entry ${e.veris_id} is not a VERIS ${mapping.metadata.veris_version} value under a covered path`);
}
for (const id of expected.keys()) if (!seen.has(id)) fail(`no entry for ${id}`);

// ---------------------------------------------------------------- 3. field pairing, 4. descriptions
for (const e of mapping.entries) {
  const t = e.mapping_type;
  if (!TYPES.includes(t)) { fail(`${e.veris_id}: unknown mapping_type ${t}`); continue; }
  for (const k of BASE_FIELDS) if (!(k in e)) fail(`${e.veris_id}: missing ${k}`);
  const allowed = new Set([...BASE_FIELDS, ...ALLOWED_FIELDS[t]]);
  for (const k of Object.keys(e)) if (!allowed.has(k)) fail(`${e.veris_id}: field ${k} not allowed on ${t}`);
  if (typeof e.rationale !== 'string' || e.rationale.length < 20) fail(`${e.veris_id}: rationale missing or too short`);
  if (expected.has(e.veris_id) && e.veris_description !== expected.get(e.veris_id)) {
    fail(`${e.veris_id}: veris_description drifted from pinned labels`);
  }
  if (t === 'direct' || t === 'conditional' || t === 'chain') {
    if (!Array.isArray(e.targets) || e.targets.length === 0) { fail(`${e.veris_id}: targets required`); continue; }
    if (t === 'conditional' && e.targets.length < 2) fail(`${e.veris_id}: conditional needs 2+ targets`);
    if (t !== 'conditional' && e.targets.length !== 1) fail(`${e.veris_id}: ${t} needs exactly one target`);
    for (const tg of e.targets) {
      if (!clusters.has(tg.tlctc)) fail(`${e.veris_id}: target ${tg.tlctc} is not a cluster`);
      if (tg.rule && !rules.has(tg.rule)) fail(`${e.veris_id}: rule ${tg.rule} not in dictionary`);
      if (t === 'conditional' && !tg.condition) fail(`${e.veris_id}: conditional target ${tg.tlctc} lacks condition`);
      if (t !== 'conditional' && tg.condition) fail(`${e.veris_id}: condition only on conditional targets`);
      if (tg.role_hint && !['server', 'client'].includes(tg.role_hint)) fail(`${e.veris_id}: bad role_hint`);
      for (const k of Object.keys(tg)) if (!['tlctc', 'rule', 'condition', 'role_hint', 'sub_cluster_hint'].includes(k)) fail(`${e.veris_id}: target field ${k} not allowed`);
    }
    if (t === 'chain') {
      const c = e.companion;
      if (!c || (!c.before && !c.after)) fail(`${e.veris_id}: chain needs companion.before or .after`);
      if (!c || typeof c.notation !== 'string') fail(`${e.veris_id}: chain needs companion.notation`);
    }
  }
  if (t === 'context') {
    if (!e.context || typeof e.context !== 'object' || Object.keys(e.context).length === 0) fail(`${e.veris_id}: context object required`);
    else for (const k of Object.keys(e.context)) if (!['boundary_context', 'boundary', 'intra_system_boundary', 'role_hint', 'note'].includes(k)) fail(`${e.veris_id}: context field ${k} not allowed`);
  }
  if (t === 'no-cluster') {
    if (!rows.has(e.partition_row)) fail(`${e.veris_id}: partition_row ${e.partition_row} not in dictionary`);
    if (e.partition_row === 'attack' && !e.out_of_scope) fail(`${e.veris_id}: partition_row attack requires out_of_scope`);
    if (e.partition_row !== 'attack' && e.out_of_scope) fail(`${e.veris_id}: out_of_scope only with partition_row attack`);
    if (e.basis && !rules.has(e.basis) && !axioms.has(e.basis)) fail(`${e.veris_id}: basis ${e.basis} is neither a rule nor an axiom`);
  }
  if (t === 'outcome') {
    if (e.dre && !dreCodes.has(e.dre)) fail(`${e.veris_id}: dre ${e.dre} not in dictionary`);
    if (e.certainty && e.certainty !== 'potential') fail(`${e.veris_id}: certainty must be 'potential'`);
    if (e.certainty && !e.dre) fail(`${e.veris_id}: certainty without dre`);
  }
}

// ---------------------------------------------------------------- 5. CSV bytes
const csvPath = gen.outputPath(mapping);
if (!fs.existsSync(csvPath)) fail(`${rel(csvPath)} missing — run npm run build-veris`);
else {
  const onDisk = fs.readFileSync(csvPath);
  if (onDisk[0] === 0xef && onDisk[1] === 0xbb) fail(`${rel(csvPath)} has a BOM`);
  const text = onDisk.toString('utf8');
  if (text.includes('\r')) fail(`${rel(csvPath)} has CR characters (must be LF only)`);
  const expectedCsv = gen.buildCsv(mapping, dictionary);
  if (text !== expectedCsv) fail(`${rel(csvPath)} differs from generator output — run npm run build-veris`);
}

// ---------------------------------------------------------------- 6. study results
let studyNote = 'no study results';
if (fs.existsSync(RESULTS)) {
  const r = readJSON(RESULTS);
  const pinnedMd = fs.readFileSync(path.join(DIR, 'PINNED.md'), 'utf8');
  if (r.mapping_updated !== mapping.metadata.updated) fail(`study/results.json mapping_updated ${r.mapping_updated} != metadata.updated ${mapping.metadata.updated}`);
  if (!r.vcdb || !pinnedMd.includes(r.vcdb.sha256)) fail('study/results.json vcdb.sha256 is not listed in PINNED.md');
  if (!r.vcdb || !pinnedMd.includes(r.vcdb.commit)) fail('study/results.json vcdb.commit is not listed in PINNED.md');
  let cells = 0;
  const walk = (node, p) => {
    if (node && typeof node === 'object') {
      if ('n' in node && 'denominator' in node) {
        cells++;
        if (typeof node.n !== 'number' || typeof node.denominator !== 'number' || node.n > node.denominator || node.n < 0) fail(`study/results.json ${p}: n=${node.n} denominator=${node.denominator}`);
        return;
      }
      for (const [k, v] of Object.entries(node)) walk(v, `${p}.${k}`);
    }
  };
  walk(r.tables, 'tables');
  if (cells === 0) fail('study/results.json has no {n, denominator} cells');
  studyNote = `study results ok (${r.vcdb ? r.vcdb.records : '?'} records, ${cells} cells)`;
}

// ---------------------------------------------------------------- report
if (failures.length) {
  console.error(`validate-veris: ${failures.length} failure(s)`);
  for (const f of failures) console.error(`  - ${f}`);
  process.exit(1);
}
const byType = {};
for (const e of mapping.entries) byType[e.mapping_type] = (byType[e.mapping_type] || 0) + 1;
console.log(`validate-veris: OK (${mapping.entries.length} entries: ${Object.entries(byType).map(([k, v]) => `${k} ${v}`).join(', ')}; ${studyNote})`);
