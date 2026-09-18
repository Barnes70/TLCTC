#!/usr/bin/env node
/*
 * validate-attack-flow.js — Validate the Attack Flow integration artefacts. Part of `npm run validate`.
 *
 *  1. stix/tlctc-stix-bundle.json is byte-identical to the generator output; it holds exactly ten
 *     x-mitre-tactic and 10 + N attack-pattern objects (N = sub-clusters in the operational
 *     enumeration); names and definitions equal the dictionary / enumeration; every technique's
 *     kill_chain_phases names an existing tactic shortname; every id is unique.
 *  2. stix/tlctc-attack-flow-extension-schema-1.0.0.json compiles; the extension bundle's
 *     extension-definition references it, lists property-extension, and its ids/timestamps are well-formed.
 *  3. Every file in stix/examples/*.attack-flow.json: each attack-flow / attack-action /
 *     attack-condition / attack-operator / attack-asset object validates against the pinned
 *     Attack Flow schema definition of its type, every TLCTC extension block validates against the
 *     extension schema, every *_refs target exists in the bundle, and both extension-definitions
 *     are present.
 *  4. study/results.json exists, names the pinned commit of PINNED.md and study/corpus-sha256.json,
 *     and every {n, denominator} cell satisfies 0 <= n <= denominator.
 *
 * Exit: 0 = valid, 1 = at least one failure (all printed). Deps: ajv (present), Node builtins.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const gen = require('./build-attack-flow-stix.js');

const ROOT = path.resolve(__dirname, '..');
const DIR = path.join(ROOT, 'integrations/attack-flow');
const PINNED_SCHEMA = path.join(DIR, 'pinned/attack-flow-schema-2.0.0.json');
const EXT_SCHEMA = path.join(DIR, 'stix/tlctc-attack-flow-extension-schema-1.0.0.json');
const EXT_BUNDLE = path.join(DIR, 'stix/tlctc-attack-flow-extension.json');
const EXAMPLES = path.join(DIR, 'stix/examples');
const RESULTS = path.join(DIR, 'study/results.json');
const CORPUS_HASHES = path.join(DIR, 'study/corpus-sha256.json');
const TLCTC_EXT_ID = 'extension-definition--69b4eaba-45a8-4101-b935-3a7ae2cb3a1a';
const AF_EXT_ID = 'extension-definition--fb9c968a-745b-4ade-9b25-c324172197f4';

const failures = [];
const fail = (m) => failures.push(m);
const rel = (p) => path.relative(ROOT, p).split(path.sep).join('/');
const readJSON = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const ID_RE = /^[a-z][a-z0-9-]+--[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const TS_RE = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/;

// ---------------------------------------------------------------- 1. source bundle
const dictionary = readJSON(gen.DICTIONARY);
const enumeration = readJSON(gen.ENUMERATION);
const expected = JSON.stringify(gen.build(dictionary, enumeration), null, 2) + '\n';
const onDisk = fs.readFileSync(gen.OUT, 'utf8').replace(/\r\n/g, '\n');
if (onDisk !== expected) fail(`${rel(gen.OUT)} differs from generator output — run npm run build-attack-flow`);
const bundle = JSON.parse(onDisk);
const tactics = bundle.objects.filter((o) => o.type === 'x-mitre-tactic');
const techniques = bundle.objects.filter((o) => o.type === 'attack-pattern');
if (tactics.length !== 10) fail(`source bundle has ${tactics.length} tactics, expected 10`);
if (techniques.length !== 10 + enumeration.sub_clusters.length) fail(`source bundle has ${techniques.length} techniques, expected ${10 + enumeration.sub_clusters.length}`);
const shortnames = new Set(tactics.map((t) => t.x_mitre_shortname));
for (const t of tactics) {
  const cid = t.external_references[0].external_id;
  const c = dictionary.clusters[cid];
  if (!c) { fail(`tactic ${cid} not in dictionary`); continue; }
  if (t.name !== c.name) fail(`tactic ${cid} name drifted`);
  if (t.description !== c.definition) fail(`tactic ${cid} definition drifted`);
}
for (const a of techniques) {
  const oid = a.external_references[0].external_id;
  const phase = a.kill_chain_phases[0].phase_name;
  if (!shortnames.has(phase)) fail(`technique ${oid} phase ${phase} has no tactic`);
  const sub = enumeration.sub_clusters.find((s) => s.id === oid);
  if (sub) {
    if (a.name !== sub.name) fail(`technique ${oid} name drifted from enumeration`);
    if (!a.description.startsWith(sub.definition)) fail(`technique ${oid} definition drifted`);
  } else if (!/^TLCTC-(0[1-9]|10)\.00$/.test(oid)) fail(`technique ${oid} is neither a root nor an enumeration entry`);
}
const ids = bundle.objects.map((o) => o.id);
if (new Set(ids).size !== ids.length) fail('source bundle has duplicate ids');
for (const o of bundle.objects) {
  if (!ID_RE.test(o.id)) fail(`bad STIX id ${o.id}`);
  if (o.created && !TS_RE.test(o.created)) fail(`bad timestamp on ${o.id}`);
}

// ---------------------------------------------------------------- 2. extension
const ajv = new Ajv({ allErrors: true, strict: false });
let validateExt;
try {
  validateExt = ajv.compile(readJSON(EXT_SCHEMA));
} catch (e) {
  fail(`extension schema does not compile: ${e.message}`);
}
const extBundle = readJSON(EXT_BUNDLE);
const extDef = extBundle.objects.find((o) => o.type === 'extension-definition');
if (!extDef || extDef.id !== TLCTC_EXT_ID) fail('extension bundle lacks the TLCTC extension-definition');
else {
  if (!extDef.extension_types.includes('property-extension')) fail('extension-definition must declare property-extension');
  if (!extDef.schema.endsWith(path.basename(EXT_SCHEMA))) fail('extension-definition.schema does not point at the schema file');
  if (!extBundle.objects.find((o) => o.id === extDef.created_by_ref)) fail('extension-definition.created_by_ref not in bundle');
  const schemaProps = Object.assign({}, ...Object.values(readJSON(EXT_SCHEMA).definitions).filter((d) => d.properties).map((d) => d.properties));
  for (const p of extDef.extension_properties) if (!(p in schemaProps)) fail(`extension_properties lists ${p} which the schema does not define`);
  for (const p of Object.keys(schemaProps)) if (p.startsWith('tlctc_') && !extDef.extension_properties.includes(p)) fail(`schema defines ${p} which extension_properties omits`);
}
for (const o of extBundle.objects) {
  if (!ID_RE.test(o.id)) fail(`bad STIX id ${o.id} in extension bundle`);
  if (!TS_RE.test(o.created) || !TS_RE.test(o.modified)) fail(`bad timestamp on ${o.id}`);
}

// ---------------------------------------------------------------- 3. examples
// The pinned Attack Flow schema is draft 2020-12 and pulls the STIX 2.1 common properties from the
// OASIS schemas by absolute $ref; those files are pinned under pinned/oasis-open/ and registered by $id.
const Ajv2020 = require('ajv/dist/2020');
const afSchema = readJSON(PINNED_SCHEMA);
const ajvAf = new Ajv2020({ allErrors: true, strict: false, unicodeRegExp: false, logger: false }); // OASIS regexes use escapes that are invalid under the u flag
const OASIS = path.join(DIR, 'pinned/oasis-open');
const OASIS_BASE = 'http://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/stix2.1/schemas/';
const walkDir = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? walkDir(path.join(d, e.name)) : [path.join(d, e.name)]));
if (fs.existsSync(OASIS)) {
  for (const f of walkDir(OASIS).filter((x) => x.endsWith('.json'))) {
    const s = readJSON(f);
    const relKey = path.relative(OASIS, f).split(path.sep).join('/');
    const key = OASIS_BASE + relKey;
    const cleaned = { ...s };
    delete cleaned.$id; delete cleaned.id;
    // The Attack Flow schema refers to these files under both the stix2.1 and master branches, http and https.
    for (const k of [key, key.replace('http://', 'https://'), key.replace('/stix2.1/', '/master/'), key.replace('http://', 'https://').replace('/stix2.1/', '/master/')]) {
      try { ajvAf.addSchema(cleaned, k); } catch (e) { fail(`cannot register ${relKey} as ${k}: ${e.message}`); }
    }
  }
} else fail('pinned/oasis-open/ missing (STIX 2.1 common schemas)');
let validateAf = null;
try {
  validateAf = ajvAf.compile(afSchema);
} catch (e) {
  fail(`pinned Attack Flow schema does not compile: ${e.message}`);
}
const afValidators = {};
for (const t of ['attack-flow', 'attack-action', 'attack-condition', 'attack-operator', 'attack-asset']) afValidators[t] = validateAf;
let exampleCount = 0;
if (fs.existsSync(EXAMPLES)) {
  for (const f of fs.readdirSync(EXAMPLES).filter((x) => x.endsWith('.attack-flow.json'))) {
    exampleCount++;
    const b = readJSON(path.join(EXAMPLES, f));
    const idSet = new Set(b.objects.map((o) => o.id));
    if (!idSet.has(TLCTC_EXT_ID)) fail(`${f}: TLCTC extension-definition missing`);
    if (!idSet.has(AF_EXT_ID)) fail(`${f}: Attack Flow extension-definition missing`);
    if (b.objects.filter((o) => o.type === 'attack-flow').length !== 1) fail(`${f}: exactly one attack-flow object required`);
    for (const o of b.objects) {
      if (afValidators[o.type]) {
        const ok = afValidators[o.type](o);
        if (!ok) fail(`${f}: ${o.id} fails Attack Flow schema: ${afValidators[o.type].errors.slice(0, 3).map((e) => `${e.instancePath} ${e.message}`).join('; ')}`);
      }
      for (const k of Object.keys(o)) {
        if (k.endsWith('_refs') && Array.isArray(o[k])) for (const r of o[k]) if (!idSet.has(r)) fail(`${f}: ${o.id}.${k} → ${r} not in bundle`);
        if (k.endsWith('_ref') && typeof o[k] === 'string' && !idSet.has(o[k])) fail(`${f}: ${o.id}.${k} → ${o[k]} not in bundle`);
      }
      const ext = o.extensions && o.extensions[TLCTC_EXT_ID];
      if (ext && validateExt && !validateExt(ext)) fail(`${f}: ${o.id} TLCTC extension invalid: ${validateExt.errors.slice(0, 3).map((e) => `${e.instancePath} ${e.message}`).join('; ')}`);
      if (o.type === 'attack-action' && !ext) fail(`${f}: ${o.id} attack-action has no TLCTC extension`);
    }
  }
}

// ---------------------------------------------------------------- 4. study results
let studyNote = 'no study results';
if (!fs.existsSync(RESULTS)) fail(`${rel(RESULTS)} missing — run python integrations/attack-flow/study/run-study.py`);
else {
  const r = readJSON(RESULTS);
  const pinnedMd = fs.readFileSync(path.join(DIR, 'PINNED.md'), 'utf8');
  const hashes = readJSON(CORPUS_HASHES);
  if (!r.corpus || !pinnedMd.includes(r.corpus.commit)) fail('study/results.json corpus.commit is not the commit in PINNED.md');
  if (!r.corpus || hashes.commit !== r.corpus.commit) fail('study/results.json corpus.commit differs from study/corpus-sha256.json');
  let cells = 0;
  const walk = (node, p) => {
    if (node && typeof node === 'object') {
      if ('n' in node && 'denominator' in node) {
        cells++;
        if (typeof node.n !== 'number' || node.n < 0 || node.n > node.denominator) fail(`study/results.json ${p}: n=${node.n} denominator=${node.denominator}`);
        return;
      }
      for (const [k, v] of Object.entries(node)) walk(v, `${p}.${k}`);
    }
  };
  walk(r.tables, 'tables');
  if (cells === 0) fail('study/results.json has no {n, denominator} cells');
  studyNote = `study results ok (${r.corpus ? r.corpus.flows : '?'} flows, ${cells} cells)`;
}

if (failures.length) {
  console.error(`validate-attack-flow: ${failures.length} failure(s)`);
  for (const f of failures) console.error(`  - ${f}`);
  process.exit(1);
}
console.log(`validate-attack-flow: OK (${tactics.length} tactics, ${techniques.length} techniques; extension schema ok; ${exampleCount} example(s); ${studyNote})`);
