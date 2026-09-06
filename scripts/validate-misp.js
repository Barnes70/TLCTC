#!/usr/bin/env node
/*
 * validate-misp.js — Validate the MISP integration artefacts. Part of `npm run validate`.
 *
 *  1. taxonomies/tlctc/machinetag.json validates against the pinned misp-taxonomies schema
 *     and is byte-identical to the generator output (build-misp-taxonomy.js).
 *  2. Exactly two predicates (cluster, entry-cluster), entry-cluster exclusive, 10 entries each.
 *  3. Entry descriptions / expanded / numerical_value equal the v2.5 dictionary byte for byte.
 *  4. Every predicate and entry carries a uuid.
 *  5. Both object templates validate against the pinned misp-objects schema, are in
 *     `jq -S -j .` format, and their values_lists match the dictionary and Layer 3 enums.
 *
 * Exit: 0 = valid, 1 = at least one failure (all failures printed).
 * Deps: ajv (already in package.json), Node builtins.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const tax = require('./build-misp-taxonomy.js');

const ROOT = path.resolve(__dirname, '..');
const MISP = path.join(ROOT, 'integrations/misp');
const TAX_SCHEMA = path.join(MISP, 'taxonomies/schema.misp-taxonomy.json');
const OBJ_SCHEMA = path.join(MISP, 'objects/schema_objects.misp.json');
const TEMPLATES = ['tlctc-attack-path', 'tlctc-attack-step'].map((n) => path.join(MISP, 'objects', n, 'definition.json'));
const LAYER3_SCHEMA = path.join(ROOT, 'json-schemas/layer-3/tlctc-attack-path.schema.json');

const failures = [];
const fail = (m) => failures.push(m);
const rel = (p) => path.relative(ROOT, p).split(path.sep).join('/');
const readJSON = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
// Byte checks are line-ending agnostic: a Windows checkout with core.autocrlf may
// hand us CRLF; the files are committed with LF (what upstream jq emits).
const readLF = (p) => fs.readFileSync(p, 'utf8').replace(/\r\n/g, '\n');

// MISP schemas are draft-04 flavoured (`id`, `$schema: .../schema#`); ajv v8 rejects `id`.
function compileMispSchema(p) {
  const s = readJSON(p);
  delete s.$schema;
  delete s.id;
  return new Ajv({ allErrors: true, strict: false }).compile(s);
}
const fmtErrors = (errs) => errs.slice(0, 5).map((e) => `${e.instancePath || '/'} ${e.message}`).join('; ');

function sortKeys(v) {
  if (Array.isArray(v)) return v.map(sortKeys);
  if (v && typeof v === 'object') return Object.fromEntries(Object.keys(v).sort().map((k) => [k, sortKeys(v[k])]));
  return v;
}

function checkTaxonomy(dict) {
  const raw = readLF(tax.OUT);
  const t = JSON.parse(raw);
  const validate = compileMispSchema(TAX_SCHEMA);
  if (!validate(t)) fail(`${rel(tax.OUT)}: schema — ${fmtErrors(validate.errors)}`);

  // 1. byte-identical to the generator
  const regenerated = tax.serialize(tax.buildTaxonomy(dict));
  if (regenerated !== raw) fail(`${rel(tax.OUT)}: differs from generator output — run node scripts/build-misp-taxonomy.js`);

  // 2. predicates
  const preds = (t.predicates || []).map((p) => p.value);
  if (preds.join(',') !== 'cluster,entry-cluster') fail(`${rel(tax.OUT)}: predicates are [${preds}], expected [cluster, entry-cluster]`);
  const entry = (t.predicates || []).find((p) => p.value === 'entry-cluster');
  if (!entry || entry.exclusive !== true) fail(`${rel(tax.OUT)}: entry-cluster must be exclusive: true`);
  const clusterPred = (t.predicates || []).find((p) => p.value === 'cluster');
  if (clusterPred && clusterPred.exclusive) fail(`${rel(tax.OUT)}: cluster predicate must not be exclusive`);

  // 3 + 4. entries vs dictionary, uuids present
  for (const p of t.predicates || []) if (!p.uuid) fail(`${rel(tax.OUT)}: predicate ${p.value} has no uuid`);
  for (const v of t.values || []) {
    if (!Array.isArray(v.entry) || v.entry.length !== 10) fail(`${rel(tax.OUT)}: predicate ${v.predicate} has ${(v.entry || []).length} entries, expected 10`);
    for (const e of v.entry || []) {
      const id = Object.keys(tax.CLUSTER_VALUES).find((k) => tax.CLUSTER_VALUES[k] === e.value);
      if (!id) { fail(`${rel(tax.OUT)}: ${v.predicate}="${e.value}" is not a known cluster value`); continue; }
      const c = dict.clusters[id];
      if (!e.uuid) fail(`${rel(tax.OUT)}: ${v.predicate}="${e.value}" has no uuid`);
      if (e.description !== tax.entryDescription(c)) fail(`${rel(tax.OUT)}: ${v.predicate}="${e.value}" description drifted from dictionary`);
      if (e.expanded !== `${id} ${c.name}`) fail(`${rel(tax.OUT)}: ${v.predicate}="${e.value}" expanded "${e.expanded}" != "${id} ${c.name}"`);
      if (e.numerical_value !== Number(id.slice(1))) fail(`${rel(tax.OUT)}: ${v.predicate}="${e.value}" numerical_value ${e.numerical_value}`);
    }
  }
}

function checkTemplates(dict) {
  const validate = compileMispSchema(OBJ_SCHEMA);
  const clusterIds = Object.keys(dict.clusters).sort((a, b) => Number(a.slice(1)) - Number(b.slice(1)));
  const dreEnum = readJSON(LAYER3_SCHEMA).definitions.attack_step.properties.outcomes.items.enum;
  for (const p of TEMPLATES) {
    if (!fs.existsSync(p)) { fail(`${rel(p)}: missing`); continue; }
    const raw = readLF(p);
    const o = JSON.parse(raw);
    if (!validate(o)) fail(`${rel(p)}: schema — ${fmtErrors(validate.errors)}`);
    if (raw !== JSON.stringify(sortKeys(o), null, 2)) fail(`${rel(p)}: not in jq -S -j format (sorted keys, 2-space indent, no trailing newline)`);
    if (o.name !== path.basename(path.dirname(p))) fail(`${rel(p)}: name "${o.name}" != directory name`);
    for (const relName of ['cluster', 'entry-cluster']) {
      const a = o.attributes[relName];
      if (a && JSON.stringify(a.values_list) !== JSON.stringify(clusterIds)) fail(`${rel(p)}: ${relName}.values_list != dictionary cluster IDs`);
    }
    const dre = o.attributes['data-risk-event'];
    if (!dre) fail(`${rel(p)}: data-risk-event attribute missing`);
    else if (JSON.stringify(dre.values_list) !== JSON.stringify(dreEnum)) fail(`${rel(p)}: data-risk-event.values_list != Layer 3 outcomes enum ${JSON.stringify(dreEnum)}`);
  }
  const uuids = TEMPLATES.filter(fs.existsSync).map((p) => readJSON(p).uuid);
  if (new Set(uuids).size !== uuids.length) fail('object templates share a uuid');
}

function main() {
  const dict = readJSON(tax.DICT);
  checkTaxonomy(dict);
  checkTemplates(dict);
  if (failures.length) {
    console.log(`INVALID — ${failures.length} problem(s):`);
    for (const f of failures) console.log('  ' + f);
    process.exit(1);
  }
  console.log('VALID — MISP taxonomy and object templates conform (schema, dictionary text, uuids, format).');
}

module.exports = { compileMispSchema, sortKeys, failures, checkTaxonomy, checkTemplates };
if (require.main === module) main();
