#!/usr/bin/env node
// Unit tests for tools/lib/path-stats.js — the counting rules of the Path Atlas
// (docs: tools/README.md, "Path Atlas"). Run: node --test scripts/test-path-stats.js
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const S = require('../tools/lib/path-stats.js');

const step = (id, cluster, extra = {}) => ({ step_id: id, cluster, notes: '', ...extra });
const rec = (file, seq, metadata = {}) => ({ file, source: 'repo', metadata, path_sequence: seq });
const pairs = (list) => list.map((t) => `${t.from}>${t.to}`).sort();

test('parseDelta: numeric, approximate, bounded, instant, qualitative, unknown', () => {
  assert.deepEqual(S.parseDelta('4h'), { raw: '4h', kind: 'exact', seconds: 14400, vc: 'VC-2' });
  assert.deepEqual(S.parseDelta('~7d'), { raw: '~7d', kind: 'approx', seconds: 604800, vc: 'VC-1' });
  assert.equal(S.parseDelta('~3mo').seconds, 3 * 30 * 86400);
  assert.equal(S.parseDelta('~1y').seconds, 365 * 86400);
  assert.equal(S.parseDelta('~2w').seconds, 14 * 86400);
  assert.deepEqual(S.parseDelta('<10m'), { raw: '<10m', kind: 'upper', seconds: 600, vc: 'VC-3' });
  assert.deepEqual(S.parseDelta('instant'), { raw: 'instant', kind: 'instant', seconds: 0, vc: 'VC-4' });
  assert.deepEqual(S.parseDelta('~hours'), { raw: '~hours', kind: 'qualitative', seconds: null, vc: 'VC-2' });
  assert.equal(S.parseDelta('~minutes').vc, 'VC-3');
  assert.equal(S.parseDelta('~months').vc, 'VC-1');
  assert.deepEqual(S.parseDelta('?'), { raw: '?', kind: 'unknown', seconds: null, vc: null });
  assert.equal(S.parseDelta(undefined).kind, 'unknown');
  assert.equal(S.parseDelta('soon-ish').kind, 'unknown');
});

test('parseDelta: lenient about spacing and case', () => {
  assert.equal(S.parseDelta('~ 7 d').seconds, 604800);
  assert.equal(S.parseDelta('2H').seconds, 7200);
  assert.equal(S.parseDelta('30M').seconds, 1800, 'upper-case M is minutes, not months');
});

test('vcOf: tool binning at 60 s, 60 min, 24 h', () => {
  assert.equal(S.vcOf(59), 'VC-4');
  assert.equal(S.vcOf(60), 'VC-3');
  assert.equal(S.vcOf(3599), 'VC-3');
  assert.equal(S.vcOf(3600), 'VC-2');
  assert.equal(S.vcOf(86399), 'VC-2');
  assert.equal(S.vcOf(86400), 'VC-1');
});

test('normCluster', () => {
  assert.equal(S.normCluster('#07'), '#7');
  assert.equal(S.normCluster(7), '#7');
  assert.equal(S.normCluster('#10'), '#10');
  assert.equal(S.normCluster('#11'), null);
  assert.equal(S.normCluster(undefined), null);
});

test('parallel group: fan-out and fan-in, nothing inside the group', () => {
  const r = rec('p.json', [
    step('a', '#9', { delta_t_to_next: '1h' }),
    { mode: 'parallel', group_id: 'g', delta_t_to_next: '5m', steps: [step('x', '#1'), step('y', '#7')] },
    step('b', '#4'),
  ]);
  const { list, dropped } = S.recordTransitions(r);
  assert.deepEqual(pairs(list), ['#1>#4', '#7>#4', '#9>#1', '#9>#7']);
  assert.equal(dropped, 0);
  assert.equal(list.find((t) => t.from === '#9').dt.seconds, 3600);
  assert.equal(list.find((t) => t.to === '#4').dt.seconds, 300);
});

test('parallel group without its own Δt falls back to the first member Δt', () => {
  const r = rec('p.json', [
    { mode: 'parallel', group_id: 'g', steps: [step('x', '#1'), step('y', '#7', { delta_t_to_next: '2m' })] },
    step('b', '#4'),
  ]);
  const { list } = S.recordTransitions(r);
  assert.ok(list.every((t) => t.dt.seconds === 120));
});

test('unresolved items break the chain and are counted as dropped', () => {
  const r = rec('u.json', [
    step('a', '#9', { delta_t_to_next: '1h' }),
    { step_id: 'q', status: 'unresolved', unresolved_type: 'single', notes: 'n', delta_t_to_next: '5m' },
    step('b', '#4', { delta_t_to_next: '1m' }),
    step('c', '#1'),
  ]);
  const { list, dropped } = S.recordTransitions(r);
  assert.deepEqual(pairs(list), ['#4>#1']);
  assert.equal(dropped, 2);
});

test('entry/exit: leading unresolved item means no evidenced entry; groups count each member', () => {
  const r = rec('e.json', [
    { step_id: 'q', status: 'unresolved', unresolved_type: 'gap', notes: 'n' },
    step('b', '#4'),
    { mode: 'parallel', group_id: 'g', steps: [step('x', '#1'), step('y', '#7')] },
  ]);
  const ee = S.entryExit(r);
  assert.equal(ee.entry, null);
  assert.deepEqual(ee.exit.map((e) => e.cluster).sort(), ['#1', '#7']);
});

test('empty or all-unresolved records do not crash', () => {
  const empty = rec('empty.json', []);
  const onlyQ = rec('q.json', [{ step_id: 'q', status: 'unresolved', unresolved_type: 'gap', notes: 'n' }]);
  const agg = S.aggregate([empty, onlyQ], { unit: 'transitions' });
  assert.equal(agg.records, 2);
  assert.equal(agg.total, 0);
  assert.equal(agg.entry.none.count, 2);
  assert.equal(agg.exit.none.count, 2);
});

test('dreCodes rolls refinements up to their parent', () => {
  assert.deepEqual(S.dreCodes(['Ii']), ['I', 'Ii']);
  assert.deepEqual(S.dreCodes(['Ac', 'C']), ['A', 'Ac', 'C']);
  assert.deepEqual(S.dreCodes(['A', 'Av']), ['A', 'Av'], 'parent counted once');
  assert.deepEqual(S.dreCodes(undefined), []);
});

test('aggregate: DRE counted against the step cluster', () => {
  const r = rec('d.json', [step('a', '#1', { outcomes: ['C'], delta_t_to_next: '1m' }), step('b', '#7', { outcomes: ['Ac'] })]);
  const agg = S.aggregate([r], { unit: 'transitions' });
  assert.equal(agg.dre['#1'].C.count, 1);
  assert.equal(agg.dre['#7'].A.count, 1);
  assert.equal(agg.dre['#7'].Ac.count, 1);
  assert.equal(agg.dre['#7'].C.count, 0);
});

test('incident unit collapses -AP<n> records; transition unit counts every transition', () => {
  const a = rec('a.json', [step('a', '#9', { delta_t_to_next: '1h' }), step('b', '#4')], { incident_id: 'X-2026-AP1' });
  const b = rec('b.json', [step('a', '#9', { delta_t_to_next: '2h' }), step('b', '#4', { delta_t_to_next: '1m' }), step('c', '#9', { delta_t_to_next: '1m' }), step('d', '#4')], { incident_id: 'X-2026-AP2' });
  assert.equal(S.incidentKey(a), 'X-2026');
  assert.equal(S.incidentKey(rec('n.json', [])), 'n.json');
  const tr = S.aggregate([a, b], { unit: 'transitions' });
  const inc = S.aggregate([a, b], { unit: 'incidents' });
  assert.equal(tr.cells['#9>#4'].count, 3);
  assert.equal(inc.cells['#9>#4'].count, 1);
  assert.equal(inc.cells['#9>#4'].items.length, 3, 'drill-down keeps every transition');
  assert.equal(inc.total, 2, '#9>#4 and #4>#9, once each');
});

test('filterRecords by source and confidence', () => {
  const rs = [
    { ...rec('a.json', []), source: 'repo', metadata: { analyst_confidence: 'high' } },
    { ...rec('b.json', []), source: 'example', metadata: { analyst_confidence: 'low' } },
  ];
  assert.deepEqual(S.filterRecords(rs, { sources: ['repo'] }).map((r) => r.file), ['a.json']);
  assert.deepEqual(S.filterRecords(rs, { confidence: ['low'] }).map((r) => r.file), ['b.json']);
  assert.equal(S.filterRecords(rs, {}).length, 2);
});

test('summarizeDeltas and exports', () => {
  const r = rec('s.json', [
    step('a', '#9', { delta_t_to_next: '1h' }), step('b', '#4', { delta_t_to_next: '<10m' }),
    step('c', '#1', { delta_t_to_next: '~hours' }), step('d', '#7', { delta_t_to_next: '?' }), step('e', '#1'),
  ]);
  const agg = S.aggregate([r], { unit: 'transitions' });
  const all = Object.values(agg.cells).flatMap((c) => c.items);
  const sum = S.summarizeDeltas(all);
  assert.equal(sum.n, 4);
  assert.equal(sum.n_numeric, 2);
  assert.equal(sum.min_s, 600);
  assert.equal(sum.max_s, 3600);
  assert.equal(sum.n_upper, 1);
  assert.equal(sum.n_qualitative, 1);
  assert.equal(sum.n_unknown, 1);
  assert.deepEqual(sum.vc, { 'VC-1': 0, 'VC-2': 2, 'VC-3': 1, 'VC-4': 0 });
  const json = S.toStatsJson(agg, { corpus_hash: 'abc', unit: 'transitions', filters: {} });
  assert.equal(json.schema, 'tlctc-path-atlas-stats.v1');
  assert.equal(json.transitions.length, 4);
  assert.ok(json.transitions.every((t) => t.delta_t && typeof t.count === 'number'));
  const csv = S.toTransitionsCsv(agg).trim().split('\n');
  assert.equal(csv[0], 'from,to,count,median_seconds,vc1,vc2,vc3,vc4');
  assert.equal(csv.length, 5);
});

test('quantile and P10 (the fast tail core §7.2 reads a Δt distribution at)', () => {
  assert.equal(S.quantile([], 0.1), null);
  assert.equal(S.quantile([42], 0.1), 42);
  assert.equal(S.quantile([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 0.1), 19, 'linear interpolation between order statistics');
  assert.equal(S.quantile([100, 10, 50], 0.5), 50, 'unsorted input is sorted');
  const r = rec('q.json', [
    step('a', '#4', { delta_t_to_next: '10m' }), step('b', '#1', { delta_t_to_next: '1m' }), step('c', '#4', { delta_t_to_next: '<5m' }),
    step('d', '#1', { delta_t_to_next: '~hours' }), step('e', '#4', { delta_t_to_next: '30m' }), step('f', '#1'),
  ]);
  const cell = S.aggregate([r], { unit: 'transitions' }).cells['#4>#1'];
  const d = S.summarizeDeltas(cell.items);
  assert.equal(d.p10_s, 600 + 0.1 * (1800 - 600) * 1, 'P10 over exact/approx/instant values only — bounds and qualitative values excluded');
  assert.equal(d.n_p10, 2);
});

test('formatSeconds', () => {
  assert.equal(S.formatSeconds(0), '0s');
  assert.equal(S.formatSeconds(90), '1.5m');
  assert.equal(S.formatSeconds(7200), '2h');
  assert.equal(S.formatSeconds(604800), '7d');
  assert.equal(S.formatSeconds(null), '—');
});

// ---- the bundled corpus (tools/data/path-corpus.js, built by scripts/build-path-corpus.js)
const BUNDLE = path.join(__dirname, '..', 'tools', 'data', 'path-corpus.js');
test('bundled corpus: every adjacent position pair is either a transition or dropped', { skip: !fs.existsSync(BUNDLE) && 'bundle not built' }, () => {
  const ctx = { window: {} };
  vm.runInNewContext(fs.readFileSync(BUNDLE, 'utf8'), ctx);
  const corpus = ctx.window.TLCTC_PATH_CORPUS;
  const repo = corpus.records.filter((r) => r.source === 'repo');
  const repoFiles = fs.readdirSync(path.join(__dirname, '..', 'attack-paths')).filter((f) => f.endsWith('.json'));
  assert.equal(repo.length, repoFiles.length, 'one bundled record per attack-paths/*.json');
  assert.equal(Object.keys(corpus.clusters).length, 10);

  // independent count: for adjacent items, (#members or 1) × (#members or 1)
  const width = (it) => (it.status === 'unresolved' ? 1 : Array.isArray(it.steps) ? it.steps.length : 1);
  let expected = 0;
  for (const r of repo) for (let i = 0; i + 1 < r.path_sequence.length; i++) expected += width(r.path_sequence[i]) * width(r.path_sequence[i + 1]);
  const agg = S.aggregate(repo, { unit: 'transitions' });
  // a break at an unresolved item drops one pair per neighbouring member, which is exactly width × 1
  assert.equal(agg.total + agg.dropped, expected);
  assert.ok(agg.total > 250, `sanity: ${agg.total} transitions`);
});
