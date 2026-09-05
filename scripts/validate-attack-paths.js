#!/usr/bin/env node
/*
 * validate-attack-paths.js — Validate every Layer-3 attack path instance against
 * the Layer-3 schema. Part of `npm run validate`.
 *
 * Checks: attack-paths/*.json and json-schemas/layer-3/examples/*.json.
 * Exit: 0 = all valid, 1 = at least one invalid (each error is printed).
 *
 * Deps: ajv, ajv-formats (already in package.json).
 */
'use strict';
const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ROOT = path.resolve(__dirname, '..');
const SCHEMA = path.join(ROOT, 'json-schemas/layer-3/tlctc-attack-path.schema.json');
const DIRS = ['attack-paths', 'json-schemas/layer-3/examples'];

const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv);
const validate = ajv.compile(JSON.parse(fs.readFileSync(SCHEMA, 'utf8')));

let checked = 0;
const failures = [];
for (const dir of DIRS) {
  const abs = path.join(ROOT, dir);
  if (!fs.existsSync(abs)) continue;
  for (const name of fs.readdirSync(abs).filter((f) => f.endsWith('.json')).sort()) {
    const rel = `${dir}/${name}`;
    let data;
    try { data = JSON.parse(fs.readFileSync(path.join(abs, name), 'utf8')); }
    catch (e) { failures.push(`${rel}: unparseable JSON — ${e.message}`); continue; }
    checked++;
    if (!validate(data)) {
      const errs = validate.errors.slice(0, 5).map((e) => `${e.instancePath || '/'} ${e.message}`);
      failures.push(`${rel}: ${errs.join('; ')}${validate.errors.length > 5 ? ` (+${validate.errors.length - 5} more)` : ''}`);
    }
  }
}

console.log(`Checked ${checked} attack-path files against ${path.relative(ROOT, SCHEMA)}`);
if (failures.length) {
  console.log(`INVALID — ${failures.length} file(s):`);
  for (const f of failures) console.log('  ' + f);
  process.exit(1);
}
console.log('VALID — all attack-path instances conform to the Layer-3 schema.');
