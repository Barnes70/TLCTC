'use strict';
// Tests for the v2.7 consequence-chain canon (change items C1–C3).
const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ROOT = path.resolve(__dirname, '..');
const load = (rel) => JSON.parse(fs.readFileSync(path.join(ROOT, rel), 'utf8'));
const schema = load('json-schemas/layer-1/tlctc-framework.schema.json');
const fw = load('json-schemas/layer-1/tlctc-framework.v2.7.json');

function compile() {
  const ajv = new Ajv({ allErrors: true, strict: false });
  addFormats(ajv);
  return ajv.compile(schema);
}

test('v2.7 dictionary validates against the schema', () => {
  const v = compile();
  assert.ok(v(fw), JSON.stringify(v.errors, null, 2));
});

test('v2.6 dictionary still validates (schema change is additive)', () => {
  const v = compile();
  assert.ok(v(load('json-schemas/layer-1/tlctc-framework.v2.6.json')), JSON.stringify(v.errors, null, 2));
});

test('causal edges carry a Δt, normative edges do not', () => {
  const edges = fw.consequence_chain.edges;
  assert.deepStrictEqual(edges.map((e) => [e.kind, e.delta_t]), [['causal', true], ['normative', false]]);
});

test('schema rejects a normative edge that claims a Δt', () => {
  const bad = structuredClone(fw);
  bad.consequence_chain.edges.find((e) => e.kind === 'normative').delta_t = true;
  assert.strictEqual(compile()(bad), false);
});

test('a BRE can be entered directly, without a cluster', () => {
  const bre = fw.consequence_chain.entry_points.filter((p) => p.altitude === 'BRE');
  assert.strictEqual(bre.length, 1);
  assert.strictEqual(bre[0].cluster_applies, false);
});

test('BRE definition names both edge kinds', () => {
  const d = fw.consequence_chain.business_risk_event.definition;
  assert.match(d, /causal edge/);
  assert.match(d, /normative edge/);
  assert.doesNotMatch(d, /triggered by/);
});

test('compromise no longer claims the detection window for its type alone (C1)', () => {
  const d = fw.system_risk_event.types[0].definition;
  assert.ok(!d.includes('the detection-and-intervention window between compromise and any Data Risk Event exists only for this type'));
  assert.match(d, /causal Δt/);
});

test('change record is changes_from_v2_6 with C1–C3', () => {
  assert.strictEqual(fw.changes_from_v2_5, undefined);
  assert.deepStrictEqual(fw.changes_from_v2_6.map((c) => c.id), ['C1', 'C2', 'C3']);
});
