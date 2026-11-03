'use strict';
// Tests for scripts/validate-rsit.js (node:test). Run: node --test scripts/validate-rsit.test.js
const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const { validateMapping } = require('./validate-rsit.js');

const ROOT = path.resolve(__dirname, '..');
const readJSON = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));
const load = () => ({
  mapping: readJSON('mappings/rsit/tlctc-rsit.json'),
  machinev1: readJSON('mappings/rsit/pinned/machinev1'),
  dictionary: readJSON('json-schemas/layer-1/tlctc-framework.v2.6.json'),
});
const entry = (m, id) => m.entries.find((e) => e.rsit_id === id);
const has = (failures, needle) => failures.some((f) => f.includes(needle));

test('real mapping is valid', () => {
  const { mapping, machinev1, dictionary } = load();
  assert.deepStrictEqual(validateMapping(mapping, machinev1, dictionary), []);
});

test('coverage: missing key named', () => {
  const { mapping, machinev1, dictionary } = load();
  mapping.entries = mapping.entries.filter((e) => e.rsit_id !== 'availability/dos');
  assert.ok(has(validateMapping(mapping, machinev1, dictionary), 'availability/dos'));
});

test('coverage: unknown key named', () => {
  const { mapping, machinev1, dictionary } = load();
  mapping.entries.push({ ...entry(mapping, 'availability/outage'), rsit_id: 'availability/foo' });
  assert.ok(has(validateMapping(mapping, machinev1, dictionary), 'availability/foo'));
});

test('pairing: exposure with targets rejected', () => {
  const { mapping, machinev1, dictionary } = load();
  entry(mapping, 'vulnerable/weak-crypto').targets = [{ tlctc: '#5' }];
  assert.ok(has(validateMapping(mapping, machinev1, dictionary), 'vulnerable/weak-crypto'));
});

test('pairing: attempt requires near_miss true', () => {
  const { mapping, machinev1, dictionary } = load();
  delete entry(mapping, 'intrusion-attempts/brute-force').near_miss;
  assert.ok(has(validateMapping(mapping, machinev1, dictionary), 'intrusion-attempts/brute-force'));
});

test('pairing: partition_row alternative accepted in conditional', () => {
  const { mapping, machinev1, dictionary } = load();
  const e = entry(mapping, 'availability/sabotage');
  assert.strictEqual(e.mapping_type, 'conditional');
  assert.ok(e.targets.some((t) => t.partition_row === 'abuse_of_rights'));
  assert.deepStrictEqual(validateMapping(mapping, machinev1, dictionary), []);
});

test('pairing: partition_row alternative rejected in direct', () => {
  const { mapping, machinev1, dictionary } = load();
  entry(mapping, 'intrusions/burglary').targets.push({ partition_row: 'failure', condition: 'x' });
  assert.ok(has(validateMapping(mapping, machinev1, dictionary), 'intrusions/burglary'));
});

test('doctrine: unknown rule id rejected', () => {
  const { mapping, machinev1, dictionary } = load();
  entry(mapping, 'intrusions/application-compromise').targets[0].rule = 'R-NOPE';
  assert.ok(has(validateMapping(mapping, machinev1, dictionary), 'R-NOPE'));
});

test('doctrine: unknown DRE code rejected', () => {
  const { mapping, machinev1, dictionary } = load();
  entry(mapping, 'information-content-security/data-leak').dre = 'Im';
  assert.ok(has(validateMapping(mapping, machinev1, dictionary), 'Im'));
});

test('doctrine: unknown partition row rejected', () => {
  const { mapping, machinev1, dictionary } = load();
  entry(mapping, 'availability/outage').partition_row = 'act_of_god';
  assert.ok(has(validateMapping(mapping, machinev1, dictionary), 'act_of_god'));
});

test('expanded text equals machinev1', () => {
  const { mapping, machinev1, dictionary } = load();
  entry(mapping, 'fraud/phishing').rsit_expanded = 'Fishing';
  assert.ok(has(validateMapping(mapping, machinev1, dictionary), 'fraud/phishing'));
});

test('collectFailures names added and renamed RSIT values instead of throwing', () => {
  const { collectFailures } = require('./validate-rsit.js');
  const inputs = require('./validate-rsit.js').loadInputs();
  const mv = JSON.parse(inputs.machinev1Text);
  const avail = mv.values.find((g) => g.predicate === 'availability');
  avail.entry.find((e) => e.value === 'dos').value = 'denial-of-service';
  avail.entry.push({ description: 'x', expanded: 'New Thing', value: 'new-thing' });
  const failures = collectFailures({ ...inputs, machinev1Text: JSON.stringify(mv, null, 2) + '\n' });
  assert.ok(has(failures, 'availability/new-thing'), failures.join('\n'));
  assert.ok(has(failures, 'availability/denial-of-service'));
  assert.ok(has(failures, 'availability/dos'));
  assert.ok(has(failures, 'sha256'));
});

test('collectFailures reports a malformed chain entry instead of throwing', () => {
  const { collectFailures, loadInputs } = require('./validate-rsit.js');
  const inputs = loadInputs();
  delete inputs.mapping.entries.find((e) => e.rsit_id === 'fraud/phishing').companion;
  const failures = collectFailures(inputs);
  assert.ok(has(failures, 'fraud/phishing: chain needs companion'), failures.join('\n'));
});

test('dre_potential accepted on direct and chain', () => {
  const { mapping, machinev1, dictionary } = load();
  assert.strictEqual(entry(mapping, 'fraud/phishing').dre_potential, 'C');
  assert.strictEqual(entry(mapping, 'fraud/phishing').dre, undefined);
  assert.deepStrictEqual(validateMapping(mapping, machinev1, dictionary), []);
});
