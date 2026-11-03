'use strict';
// Tests for scripts/build-rsit-mapping.js (node:test). Run: node --test scripts/build-rsit-mapping.test.js
const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const { buildMachinetag, tlctcElement } = require('./build-rsit-mapping.js');
const { checkGenerated } = require('./validate-rsit.js');

const ROOT = path.resolve(__dirname, '..');
const readJSON = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));
const load = () => ({
  mapping: readJSON('mappings/rsit/tlctc-rsit.json'),
  machinev1: readJSON('mappings/rsit/pinned/machinev1'),
  misp: readJSON('integrations/misp/taxonomies/tlctc/machinetag.json'),
});
const allEntries = (mt) => mt.values.flatMap((g) => g.entry.map((e) => ({ id: `${g.predicate}/${e.value}`, e })));

test('tag rule: exactly 7 tagged values', () => {
  const { mapping, machinev1, misp } = load();
  const out = JSON.parse(buildMachinetag(mapping, machinev1, misp));
  const tagged = allEntries(out).filter(({ e }) => e.tlctc.some((x) => x.machinetag)).map(({ id }) => id).sort();
  assert.deepStrictEqual(tagged, [
    'availability/ddos', 'fraud/phishing', 'information-gathering/scanner', 'information-gathering/social-engineering',
    'intrusions/burglary', 'intrusions/unprivileged-account-compromise', 'malicious-code/infected-system',
  ]);
});

test('uuid equals the TLCTC MISP taxonomy entry', () => {
  const { mapping, misp } = load();
  const el = tlctcElement(mapping.entries.find((e) => e.rsit_id === 'malicious-code/infected-system'), misp);
  const mispEntry = misp.values.find((g) => g.predicate === 'cluster').entry.find((x) => x.value === '07-malware');
  assert.strictEqual(el.machinetag, 'tlctc:cluster="07-malware"');
  assert.strictEqual(el.uuid, mispEntry.uuid);
});

test('missing MISP value throws, naming it', () => {
  const { mapping, misp } = load();
  const g = misp.values.find((x) => x.predicate === 'cluster');
  g.entry = g.entry.filter((x) => x.value !== '07-malware');
  assert.throws(() => tlctcElement(mapping.entries.find((e) => e.rsit_id === 'malicious-code/infected-system'), misp), /07-malware/);
});

test('untagged element carries candidates and no machinetag', () => {
  const { mapping, misp } = load();
  const el = tlctcElement(mapping.entries.find((e) => e.rsit_id === 'availability/dos'), misp);
  assert.deepStrictEqual(el.candidates, ['#6', '#2', '#3']);
  assert.strictEqual(el.machinetag, undefined);
  assert.strictEqual(el.uuid, undefined);
  assert.strictEqual(el.mapping_type, 'conditional');
});

test('entry keys sorted', () => {
  const { mapping, machinev1, misp } = load();
  const out = JSON.parse(buildMachinetag(mapping, machinev1, misp));
  for (const { e } of allEntries(out)) assert.deepStrictEqual(Object.keys(e), ['description', 'expanded', 'tlctc', 'value']);
});

test('generated text = machinev1 + tlctc only', () => {
  const { mapping, machinev1, misp } = load();
  const text = buildMachinetag(mapping, machinev1, misp);
  assert.ok(text.endsWith('}\n') && !text.includes('\r'));
  const out = JSON.parse(text);
  for (const g of out.values) for (const e of g.entry) delete e.tlctc;
  assert.deepStrictEqual(out, machinev1);
});

test('CRLF copy of generated files passes the byte check', () => {
  const { mapping, machinev1, misp } = load();
  const text = buildMachinetag(mapping, machinev1, misp);
  const failures = checkGenerated({ machinetagOnDisk: text.replace(/\n/g, '\r\n'), expectedMachinetag: text,
    mdOnDisk: 'a\r\nb\r\n', expectedMd: 'a\nb\n' });
  assert.deepStrictEqual(failures, []);
});

test('changed generated file fails the byte check', () => {
  const failures = checkGenerated({ machinetagOnDisk: '{}\n', expectedMachinetag: '{"a":1}\n', mdOnDisk: 'a\n', expectedMd: 'a\n' });
  assert.strictEqual(failures.length, 1);
});

test('chain note puts the DRE on the RSIT step, before an after-companion', () => {
  const { mapping, misp } = load();
  const el = tlctcElement(mapping.entries.find((e) => e.rsit_id === 'fraud/phishing'), misp);
  assert.ok(el.note.startsWith('#9 + [DRE: C] → #4'), el.note);
});
