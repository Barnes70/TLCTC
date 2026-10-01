#!/usr/bin/env node
// Unit tests for scripts/build-cis.js. Run: node --test scripts/test-build-cis.js
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { validate, buildStarter, stats } = require('./build-cis.js');

const sg = (id, extra = {}) => ({ id, control: +id.split('.')[0], asset_class: 'Software', function: 'PR', ig: 1,
  topic: 'unused services off', clusters: ['#1'], kind: 'tech', hardening: true, rationale: 'Narrows the configured surface (#1).', ...extra });
const doc = (safeguards) => ({ meta: { mapping_date: '2026-10-01' }, safeguards });
// 9 Safeguards for Controls 1–9, 8 for 10–18 = 153 (only the totals are checked, not CIS's real per-control counts)
const full = () => doc(Array.from({ length: 18 }, (_, c) => Array.from({ length: c < 9 ? 9 : 8 }, (_, s) => sg(`${c + 1}.${s + 1}`))).flat());

test('a complete 18-control / 153-Safeguard mapping validates', () => {
  assert.equal(full().safeguards.length, 153);
  assert.deepEqual(validate(full()), []);
});

test('counts are enforced', () => {
  const m = full(); m.safeguards.pop();
  assert.match(validate(m).join('\n'), /expected 153 safeguards/);
});

test('draft mode accepts unmapped rows; strict mode rejects them', () => {
  const m = full(); Object.assign(m.safeguards[0], { topic: '', clusters: null, kind: null, hardening: null, rationale: '' });
  assert.deepEqual(validate(m, { draft: true }), []);
  assert.match(validate(m).join('\n'), /1\.1: unmapped/);
});

test('field checks', () => {
  const cases = [
    [{ id: '4.x' }, /bad id/], [{ control: 7 }, /control 7 does not match/], [{ function: 'XX' }, /function/],
    [{ ig: 4 }, /ig/], [{ asset_class: '' }, /asset_class/], [{ clusters: [] }, /empty clusters/], [{ clusters: ['#11'] }, /unknown clusters/],
    [{ clusters: ['#1', '#1'] }, /duplicate clusters/], [{ clusters: 'some' }, /clusters must be/],
    [{ kind: 'people' }, /kind/], [{ hardening: 'yes' }, /hardening must be boolean/], [{ rationale: '' }, /rationale/],
    [{ topic: 'x'.repeat(61) }, /topic/],
    [{ clusters: 'none', hardening: true }, /hardening.*none/],
  ];
  for (const [patch, re] of cases) {
    const m = full(); Object.assign(m.safeguards[40], patch);
    assert.match(validate(m).join('\n'), re, JSON.stringify(patch));
  }
});

test('duplicate ids are reported', () => {
  const m = full(); m.safeguards[1].id = m.safeguards[0].id;
  assert.match(validate(m).join('\n'), /duplicate/);
});

test('starter places Local, shared Umbrella and nothing for "none"', () => {
  const m = full();
  Object.assign(m.safeguards[0], { function: 'PR', clusters: ['#1', '#4'] });
  Object.assign(m.safeguards[1], { function: 'DE', clusters: 'all', hardening: false });
  Object.assign(m.safeguards[2], { function: 'GV', clusters: 'none', hardening: false });
  const st = buildStarter(m);
  const cells = st.environments[0].cells;
  assert.equal(Object.keys(cells).length, 60);
  assert.ok(cells['1-PR'].local.some((c) => c.id === 'cis-1.1-1'));
  assert.ok(cells['4-PR'].local.some((c) => c.id === 'cis-1.1-4'));
  assert.equal(st.sharedControls.filter((c) => c.id === 'cis-1.2').length, 1);
  for (let n = 1; n <= 10; n++) assert.ok(cells[`${n}-DE`].umbrella.some((u) => u.sharedControlId === 'cis-1.2'));
  assert.ok(!JSON.stringify(st).includes('"cis-1.3'));
  assert.equal(cells['1-PR'].local.find((c) => c.id === 'cis-1.1-1').name, 'CIS 1.1 — unused services off');
  assert.equal(st.exportDate, '2026-10-01T00:00:00.000Z');
});

test('stats count hardening per cluster', () => {
  const m = full(); // every row: ['#1'], hardening true
  Object.assign(m.safeguards[0], { clusters: ['#4', '#5'] });
  Object.assign(m.safeguards[1], { clusters: 'all', hardening: false });
  const s = stats(m);
  assert.equal(s.hardening, 152);
  assert.equal(s.hardeningByCluster['#1'], 151);
  assert.equal(s.hardeningByCluster['#4'], 1);
  assert.equal(s.byCluster['#5'], 1);
  assert.equal(s.neutral, 1);
  assert.equal(s.none, 0);
});

const { dreMatrix } = require('./build-cis.js');

test('data-layer entries: dre codes instead of clusters', () => {
  const ok = full(); Object.assign(ok.safeguards[5], { clusters: null, dre: ['C'], function: 'PR' });
  assert.deepEqual(validate(ok), []);
  const cases = [
    [{ clusters: ['#8'], dre: ['C'] }, /either clusters or dre/],
    [{ clusters: null, dre: [] }, /empty dre/],
    [{ clusters: null, dre: ['I'] }, /unknown DRE codes I/],
    [{ clusters: null, dre: ['C', 'C'] }, /duplicate DRE codes/],
    [{ clusters: null, dre: 'some' }, /dre must be an array or "all"/],
  ];
  for (const [patch, re] of cases) {
    const m = full(); Object.assign(m.safeguards[5], patch);
    assert.match(validate(m).join('\n'), re, JSON.stringify(patch));
  }
});

test('data-layer entries stay out of the cluster starter and fill the DRE matrix', () => {
  const m = full();
  Object.assign(m.safeguards[5], { clusters: null, dre: ['C'], function: 'PR' });
  Object.assign(m.safeguards[6], { clusters: null, dre: ['Ii', 'Av', 'Ac'], function: 'RC' });
  Object.assign(m.safeguards[7], { clusters: null, dre: 'all', function: 'ID' });
  assert.ok(!JSON.stringify(buildStarter(m)).includes('"cis-1.6'));
  const d = dreMatrix(m);
  assert.deepEqual(d.rows, ['C', 'Ii', 'If', 'Av', 'Ac']);
  assert.deepEqual(d.cells['C-PR'], ['1.6']);
  assert.deepEqual(d.cells['Ac-RC'], ['1.7']);
  for (const r of d.rows) assert.ok(d.cells[`${r}-ID`].includes('1.8'));
  assert.equal(Object.keys(d.cells).length, 30);
  const s = stats(m);
  assert.equal(s.dataLayer, 3);
  assert.equal(s.byDre.C, 2);
});
