#!/usr/bin/env node
/*
 * validate-rsit.js — Validate the RSIT → TLCTC mapping. Part of `npm run validate`.
 *
 *  1. Coverage: mappings/rsit/tlctc-rsit.json has exactly one entry per value of the pinned RSIT
 *     machinev1 (key `<predicate>/<value>`), and rsit_expanded equals the machinev1 text.
 *  2. Field pairing per mapping_type (spec §6), including partition-row / out-of-scope
 *     alternatives, which are allowed only inside `conditional`.
 *  3. Doctrine ids: every cluster, rule, axiom, DRE code and partition row named exists in the
 *     v2.6 dictionary; metadata.tlctc_version equals the dictionary's.
 *  4. The pinned machinev1 sha256 (LF-normalised) equals the one recorded in PINNED.md.
 *  5. upstream/machinetag.json and upstream/rsit_2_tlctc.md equal fresh generator output
 *     (LF-normalised); tag rule: machinetag ⇔ direct/chain, exactly 7, uuid = TLCTC MISP entry.
 *
 * Exports validateMapping(mapping, machinev1, dictionary) -> string[] (failures; [] = valid),
 * checkGenerated({...}) and checkTags(machinetag, mapping, misp).
 * Exit: 0 = valid, 1 = at least one failure (all printed). Deps: Node builtins only.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const DIR = path.join(ROOT, 'mappings/rsit');
const FILES = {
  mapping: path.join(DIR, 'tlctc-rsit.json'),
  machinev1: path.join(DIR, 'pinned/machinev1'),
  pinned: path.join(DIR, 'PINNED.md'),
  dictionary: path.join(ROOT, 'json-schemas/layer-1/tlctc-framework.v2.6.json'),
};

const TYPES = ['direct', 'conditional', 'chain', 'outcome', 'no-cluster', 'unresolved', 'context',
  'attempt', 'exposure', 'indicator'];
const BASE_FIELDS = ['rsit_id', 'rsit_expanded', 'mapping_type', 'next_question', 'rationale'];
const TYPE_FIELDS = {
  direct: ['targets', 'dre'],
  conditional: ['targets', 'dre'],
  chain: ['targets', 'companion', 'dre'],
  outcome: ['dre', 'cause_hints'],
  'no-cluster': ['partition_row', 'basis', 'out_of_scope', 'excluded'],
  unresolved: [],
  context: ['context'],
  attempt: ['targets', 'near_miss'],
  exposure: ['exposes', 'dre_potential'],
  indicator: ['implies'],
};
const CLUSTER_TARGET_KEYS = ['tlctc', 'rule', 'condition'];

const lf = (s) => s.replace(/\r\n/g, '\n');
const readJSON = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));

/** Keys of the RSIT values, in machinev1 order, mapped to their `expanded` text. */
function rsitValues(machinev1) {
  const out = new Map();
  for (const group of machinev1.values) {
    for (const e of group.entry) out.set(`${group.predicate}/${e.value}`, e.expanded);
  }
  return out;
}

function validateMapping(mapping, machinev1, dictionary) {
  const failures = [];
  const fail = (m) => failures.push(m);
  const clusters = new Set(Object.keys(dictionary.clusters));
  const rules = new Set(dictionary.rules.map((r) => r.rule_id));
  const axioms = new Set(dictionary.axioms.map((a) => a.axiom_id));
  const dreCodes = new Set(dictionary.data_risk_events.codes.map((c) => c.code));
  const rows = new Set(dictionary.cause_side_partition.rows.map((r) => r.row_id));

  if (!mapping.metadata || mapping.metadata.tlctc_version !== dictionary.metadata.tlctc_version) {
    fail(`metadata.tlctc_version must equal dictionary ${dictionary.metadata.tlctc_version}`);
  }
  if (mapping.metadata && mapping.metadata.rsit_version !== machinev1.version) {
    fail(`metadata.rsit_version ${mapping.metadata.rsit_version} != machinev1 version ${machinev1.version}`);
  }

  // 1. coverage
  const values = rsitValues(machinev1);
  const seen = new Set();
  for (const e of mapping.entries) {
    const id = e.rsit_id;
    if (seen.has(id)) fail(`${id}: duplicate entry`);
    seen.add(id);
    if (!values.has(id)) fail(`${id}: not a value of RSIT machinev1 ${machinev1.version}`);
    else if (e.rsit_expanded !== values.get(id)) fail(`${id}: rsit_expanded "${e.rsit_expanded}" != machinev1 "${values.get(id)}"`);
  }
  for (const id of values.keys()) if (!seen.has(id)) fail(`${id}: RSIT value has no entry`);

  // 2./3. pairing and doctrine ids
  const clusterTarget = (id, where, t, extraKeys = []) => {
    if (!t || typeof t !== 'object') { fail(`${id}: ${where} element must be an object`); return; }
    for (const k of Object.keys(t)) if (![...CLUSTER_TARGET_KEYS, ...extraKeys].includes(k)) fail(`${id}: ${where} field ${k} not allowed`);
    if (!clusters.has(t.tlctc)) fail(`${id}: ${where} cluster ${t.tlctc} not in dictionary`);
    if (t.rule !== undefined && !rules.has(t.rule)) fail(`${id}: ${where} rule ${t.rule} not in dictionary`);
  };
  const list = (id, name, v, min) => {
    if (!Array.isArray(v) || v.length < min) { fail(`${id}: ${name} must be an array with at least ${min} element(s)`); return []; }
    return v;
  };
  const rowOrScope = (id, where, t) => {
    const keys = Object.keys(t);
    for (const k of keys) if (!['partition_row', 'out_of_scope', 'condition'].includes(k)) fail(`${id}: ${where} field ${k} not allowed`);
    if (t.partition_row !== undefined && !rows.has(t.partition_row)) fail(`${id}: ${where} partition_row ${t.partition_row} not in dictionary`);
    if (typeof t.condition !== 'string') fail(`${id}: ${where} alternative needs a condition`);
  };

  for (const e of mapping.entries) {
    const id = e.rsit_id;
    const t = e.mapping_type;
    if (!TYPES.includes(t)) { fail(`${id}: mapping_type ${t} unknown`); continue; }
    for (const k of BASE_FIELDS) if (!(k in e)) fail(`${id}: missing ${k}`);
    if (typeof e.rationale !== 'string' || !e.rationale.trim()) fail(`${id}: rationale required`);
    if (e.next_question !== null && typeof e.next_question !== 'string') fail(`${id}: next_question must be a string or null`);
    for (const k of Object.keys(e)) if (!BASE_FIELDS.includes(k) && !TYPE_FIELDS[t].includes(k)) fail(`${id}: field ${k} not allowed for ${t}`);
    if (e.dre !== undefined && !dreCodes.has(e.dre)) fail(`${id}: dre ${e.dre} not in dictionary`);
    if (e.dre_potential !== undefined && !dreCodes.has(e.dre_potential)) fail(`${id}: dre_potential ${e.dre_potential} not in dictionary`);

    if (t === 'direct' || t === 'chain') {
      const ts = list(id, 'targets', e.targets, 1);
      if (ts.length !== 1) fail(`${id}: ${t} needs exactly one target`);
      ts.forEach((x) => clusterTarget(id, 'target', x));
    }
    if (t === 'chain') {
      const c = e.companion;
      if (!c || (!c.before && !c.after)) fail(`${id}: chain needs companion.before or .after`);
      if (!c || typeof c.notation !== 'string') fail(`${id}: chain needs companion.notation`);
    }
    if (t === 'conditional') {
      const ts = list(id, 'targets', e.targets, 2);
      for (const x of ts) {
        if (x && 'tlctc' in x) clusterTarget(id, 'target', x);
        else if (x && ('partition_row' in x || 'out_of_scope' in x)) rowOrScope(id, 'target', x);
        else fail(`${id}: conditional target needs tlctc, partition_row or out_of_scope`);
      }
      if (!ts.some((x) => x && 'tlctc' in x)) fail(`${id}: conditional needs at least one cluster target`);
    }
    if (t === 'attempt') {
      list(id, 'targets', e.targets, 1).forEach((x) => clusterTarget(id, 'target', x));
      if (e.near_miss !== true) fail(`${id}: attempt requires near_miss: true`);
    }
    if (t === 'exposure') list(id, 'exposes', e.exposes, 1).forEach((x) => clusterTarget(id, 'exposes', x));
    if (t === 'indicator') list(id, 'implies', e.implies, 1).forEach((x) => clusterTarget(id, 'implies', x));
    if (t === 'outcome') {
      if (e.dre === undefined) fail(`${id}: outcome requires dre`);
      for (const x of e.cause_hints || []) {
        if (x && 'tlctc' in x) clusterTarget(id, 'cause_hint', x);
        else if (x && 'partition_row' in x) rowOrScope(id, 'cause_hint', x);
        else fail(`${id}: cause_hint needs tlctc or partition_row`);
      }
    }
    if (t === 'no-cluster') {
      const hasRow = e.partition_row !== undefined;
      if (hasRow === (e.excluded !== undefined)) fail(`${id}: no-cluster needs exactly one of partition_row or excluded`);
      if (hasRow && !rows.has(e.partition_row)) fail(`${id}: partition_row ${e.partition_row} not in dictionary`);
      if (e.partition_row === 'attack' && !e.out_of_scope) fail(`${id}: partition_row attack requires out_of_scope`);
      if (e.partition_row !== 'attack' && e.out_of_scope) fail(`${id}: out_of_scope only with partition_row attack`);
      if (e.basis !== undefined && !rules.has(e.basis) && !axioms.has(e.basis)) fail(`${id}: basis ${e.basis} is neither a rule nor an axiom`);
    }
  }
  return failures;
}

/** Byte check of the generated upstream files, comparing LF-normalised text. */
function checkGenerated({ machinetagOnDisk, expectedMachinetag, mdOnDisk, expectedMd }) {
  const failures = [];
  if (machinetagOnDisk === null || lf(machinetagOnDisk) !== expectedMachinetag) failures.push('upstream/machinetag.json differs from generator output — run npm run build-rsit');
  if (mdOnDisk === null || lf(mdOnDisk) !== expectedMd) failures.push('upstream/rsit_2_tlctc.md differs from generator output — run npm run build-rsit');
  return failures;
}

/** Tag rule: machinetag present <=> direct/chain; exactly 7 tagged; uuid equals the MISP entry. */
function checkTags(machinetag, mapping, misp) {
  const failures = [];
  const byId = new Map(mapping.entries.map((e) => [e.rsit_id, e]));
  const mispByValue = new Map(misp.values.find((g) => g.predicate === 'cluster').entry.map((x) => [x.value, x.uuid]));
  let tagged = 0;
  for (const g of machinetag.values) {
    for (const e of g.entry) {
      const id = `${g.predicate}/${e.value}`;
      const m = byId.get(id);
      const els = e.tlctc || [];
      const hasTag = els.some((x) => x.machinetag);
      if (hasTag) tagged += 1;
      if (m && hasTag !== ['direct', 'chain'].includes(m.mapping_type)) failures.push(`${id}: machinetag present must equal mapping_type in {direct, chain} (is ${m.mapping_type})`);
      for (const x of els.filter((y) => y.machinetag)) {
        const value = (x.machinetag.match(/^tlctc:cluster="([^"]+)"$/) || [])[1];
        if (!value || mispByValue.get(value) !== x.uuid) failures.push(`${id}: ${x.machinetag} uuid ${x.uuid} does not match the TLCTC MISP taxonomy`);
      }
    }
  }
  if (tagged !== 7) failures.push(`expected 7 tagged RSIT values, found ${tagged}`);
  return failures;
}

function main() {
  const mapping = readJSON(FILES.mapping);
  const machinev1Text = fs.readFileSync(FILES.machinev1, 'utf8');
  const machinev1 = JSON.parse(machinev1Text);
  const dictionary = readJSON(FILES.dictionary);
  const failures = validateMapping(mapping, machinev1, dictionary);

  const gen = require('./build-rsit-mapping.js');
  const os = require('os');
  const misp = readJSON(gen.PATHS.misp);
  const readOrNull = (p) => (fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : null);
  const expectedMachinetag = gen.buildMachinetag(mapping, machinev1, misp);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'rsit-'));
  fs.writeFileSync(path.join(tmp, 'machinetag.json'), expectedMachinetag);
  const expectedMd = gen.renderMd(path.join(tmp, 'machinetag.json'), path.join(tmp, 'rsit_2_tlctc.md'));
  fs.rmSync(tmp, { recursive: true, force: true });
  failures.push(...checkGenerated({ machinetagOnDisk: readOrNull(gen.PATHS.outJson), expectedMachinetag,
    mdOnDisk: readOrNull(gen.PATHS.outMd), expectedMd }));
  failures.push(...checkTags(JSON.parse(expectedMachinetag), mapping, misp));

  const sha = crypto.createHash('sha256').update(lf(machinev1Text), 'utf8').digest('hex');
  const recorded = (fs.readFileSync(FILES.pinned, 'utf8').match(/`([0-9a-f]{64})`/) || [])[1];
  if (sha !== recorded) failures.push(`pinned/machinev1 sha256 ${sha} != PINNED.md ${recorded}`);
  if (mapping.metadata.rsit_source && !fs.readFileSync(FILES.pinned, 'utf8').includes(mapping.metadata.rsit_source.commit)) {
    failures.push(`metadata.rsit_source.commit ${mapping.metadata.rsit_source.commit} not in PINNED.md`);
  }

  if (failures.length) {
    for (const f of failures) console.error(`FAIL ${f}`);
    process.exit(1);
  }
  console.log(`validate-rsit: OK (${mapping.entries.length} entries, RSIT ${machinev1.version})`);
}

module.exports = { validateMapping, checkGenerated, checkTags, rsitValues, FILES };
if (require.main === module) main();
