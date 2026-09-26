#!/usr/bin/env node
// Unit tests for tools/lib/race-core.js — the Δt Race: an attack path's transitions against a
// defender's detection and containment times (core §7.2, application §10.2–10.3).
// Run: node --test scripts/test-race-core.js
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const R = require('../tools/lib/race-core.js');
const S = require('../tools/lib/path-stats.js');

const near = (a, b, eps = 0.001) => assert.ok(Math.abs(a - b) < eps, `${a} ≉ ${b}`);
const step = (id, cluster, extra = {}) => ({ step_id: id, cluster, notes: '', ...extra });
const rec = (seq) => ({ file: 'r.json', source: 'repo', metadata: {}, path_sequence: seq });
const uniform = (ttd, ttc) => Object.fromEntries(S.CLUSTER_IDS.map((c) => [c, { ttd, ttc }]));

test('parseDuration: ISO 8601, shorthand, plain seconds', () => {
  assert.equal(R.parseDuration('PT8M'), 480);
  assert.equal(R.parseDuration('P1DT2H'), 93600);
  assert.equal(R.parseDuration('P3D'), 259200);
  assert.equal(R.parseDuration('PT1H30M'), 5400);
  assert.equal(R.parseDuration('15m'), 900);
  assert.equal(R.parseDuration('1.5h'), 5400);
  assert.equal(R.parseDuration('2 d'), 172800);
  assert.equal(R.parseDuration('90'), 90);
  assert.equal(R.parseDuration(90), 90);
  assert.equal(R.parseDuration(''), null);
  assert.equal(R.parseDuration('soon'), null);
  assert.equal(R.parseDuration(null), null);
});

test('core §7.2 example: #4 → #1 in 10 minutes, detection 15 minutes at P90 → DCS_d 1.5', () => {
  const out = R.analyzePath(rec([step('a', '#4', { delta_t_to_next: '10m' }), step('b', '#1')]), uniform(900, 3600));
  const e = out.edges[0];
  near(e.dcs_d, 1.5);
  assert.equal(e.reading_d, 'behind');
  assert.equal(e.outcome, 'missed');
});

test('application §10.2 example: the same 2 h detection is ≈0.012 against 7 days and 24 against 5 minutes', () => {
  near(R.dcs(7200, 7 * 86400), 0.0119, 0.0005);
  near(R.dcs(7200, 300), 24);
  assert.equal(R.reading(0.5), 'ahead');
  assert.equal(R.reading(1), 'marginal');
  assert.equal(R.reading(1.2), 'behind');
  assert.equal(R.reading(null), null);
});

test('outcomes: contained, seen but not stopped, missed', () => {
  const path = rec([step('a', '#4', { delta_t_to_next: '1h' }), step('b', '#1')]);
  assert.equal(R.analyzePath(path, uniform(60, 300)).edges[0].outcome, 'contained');
  assert.equal(R.analyzePath(path, uniform(300, 7200)).edges[0].outcome, 'seen', 'DCS_d < 1 with DCS_c > 1: seen but completed anyway');
  assert.equal(R.analyzePath(path, uniform(7200, 9000)).edges[0].outcome, 'missed');
  assert.equal(R.analyzePath(path, uniform(300, null)).edges[0].outcome, 'seen', 'containment time unknown: detection is all that can be said');
  assert.equal(R.analyzePath(path, uniform(null, null)).edges[0].outcome, 'no-data');
});

test('the edge is measured against the defender times of the step the attacker is leaving', () => {
  const prof = uniform(99999, 99999);
  prof['#4'] = { ttd: 60, ttc: 120 };
  const out = R.analyzePath(rec([step('a', '#4', { delta_t_to_next: '1h' }), step('b', '#1')]), prof);
  assert.equal(out.edges[0].outcome, 'contained');
  assert.equal(out.edges[0].profile_cluster, '#4');
});

test('real-time edges (VC-4, instant) are prevention-only per application §10.3', () => {
  const out = R.analyzePath(rec([step('a', '#1', { delta_t_to_next: '10s' }), step('b', '#7', { delta_t_to_next: 'instant' }), step('c', '#1')]), uniform(1, 2));
  assert.equal(out.edges[0].outcome, 'prevention-only');
  assert.equal(out.edges[1].outcome, 'prevention-only');
  assert.equal(out.edges[1].dcs_d, Infinity);
});

test('Δt that is not a measurement: upper bounds are flagged, qualitative/unknown give no score', () => {
  const out = R.analyzePath(rec([
    step('a', '#9', { delta_t_to_next: '<10m' }), step('b', '#4', { delta_t_to_next: '~hours' }), step('c', '#1', { delta_t_to_next: '?' }), step('d', '#7'),
  ]), uniform(300, 900));
  assert.equal(out.edges[0].dt.bound, true);
  near(out.edges[0].dcs_d, 0.5);
  assert.ok(out.edges[0].caveat, 'an upper-bound Δt carries a caveat: the real transition may be faster');
  assert.equal(out.edges[1].outcome, 'unknown-dt');
  assert.equal(out.edges[1].dt.vc, 'VC-2');
  assert.equal(out.edges[2].outcome, 'unknown-dt');
});

test('unresolved items break the race; parallel groups fan out and in', () => {
  const out = R.analyzePath(rec([
    step('a', '#9', { delta_t_to_next: '1h' }),
    { mode: 'parallel', group_id: 'g', delta_t_to_next: '5m', steps: [step('x', '#1'), step('y', '#7')] },
    { step_id: 'q', status: 'unresolved', notes: 'n' },
    step('b', '#4'),
  ]), uniform(60, 120));
  assert.deepEqual(out.edges.map((e) => `${e.from}>${e.to}`), ['#9>#1', '#9>#7']);
  assert.equal(out.breaks, 3);
});

test('Δt source "corpus": the transition\'s P10 across the corpus, falling back to the incident when too few samples', () => {
  const corpus = [];
  for (let i = 0; i < 5; i++) corpus.push({ file: `c${i}.json`, source: 'repo', metadata: {}, path_sequence: [step('a', '#4', { delta_t_to_next: `${(i + 1) * 10}m` }), step('b', '#1')] });
  const cells = S.aggregate(corpus, { unit: 'transitions' }).cells;
  const path = rec([step('a', '#4', { delta_t_to_next: '2h' }), step('b', '#1', { delta_t_to_next: '1h' }), step('c', '#9')]);
  const out = R.analyzePath(path, uniform(60, 120), { dtSource: 'corpus', corpusCells: cells });
  assert.equal(out.edges[0].dt.source, 'corpus-p10');
  assert.equal(out.edges[0].dt.seconds, S.quantile([600, 1200, 1800, 2400, 3000], 0.1));
  assert.equal(out.edges[0].dt.n, 5);
  assert.equal(out.edges[1].dt.source, 'incident', '#1 > #9 has no corpus samples');
});

test('targets (application §10.3 example values) are checked per velocity class', () => {
  const path = rec([step('a', '#4', { delta_t_to_next: '10m' }), step('b', '#1', { delta_t_to_next: '7d' }), step('c', '#7')]);
  const out = R.analyzePath(path, uniform(480, 4 * 86400));
  assert.equal(out.edges[0].target, 0.8);
  assert.equal(out.edges[0].meets_target_d, true, '8 min against 10 min = 0.8, exactly the VC-3 target');
  assert.equal(out.edges[1].target, 0.5);
  assert.equal(out.edges[1].meets_target_d, true, 'detection: 8 min against 7 days');
  assert.equal(out.edges[1].meets_target_c, false, 'containment: 4 days against 7 days = 0.57 > 0.5');
  assert.deepEqual(R.DEFAULT_TARGETS, { 'VC-1': 0.5, 'VC-2': 0.8, 'VC-3': 0.8, 'VC-4': null });
});

test('summary: first contained edge is the interception point', () => {
  const prof = uniform(7200, 9000);
  prof['#1'] = { ttd: 60, ttc: 300 };
  const out = R.analyzePath(rec([step('a', '#9', { delta_t_to_next: '1h' }), step('b', '#4', { delta_t_to_next: '10m' }), step('c', '#1', { delta_t_to_next: '1h' }), step('d', '#7')]), prof);
  assert.deepEqual(out.edges.map((e) => e.outcome), ['missed', 'missed', 'contained']);
  assert.equal(out.summary.interception, 2);
  assert.equal(out.summary.counts.missed, 2);
});

test('profileFromControlMatrix: DETECT cells give TTD, RESPOND cells give TTC', () => {
  const cm = { environments: [
    { id: 'e1', name: 'Production', cells: { '7-DE': { dcs_mttd: 'PT8M' }, '7-RS': { dcs_ttc: 'PT45M' }, '4-DE': { dcs_mttd: 'PT2H' } } },
    { id: 'e2', name: 'Staging', cells: {} },
  ] };
  const r = R.profileFromControlMatrix(cm);
  assert.deepEqual(r.environments.map((e) => e.name), ['Production', 'Staging']);
  assert.deepEqual(r.profile['#7'], { ttd: 480, ttc: 2700 });
  assert.deepEqual(r.profile['#4'], { ttd: 7200, ttc: null });
  assert.equal(r.found, 3);
  assert.equal(R.profileFromControlMatrix(cm, 'e2').found, 0);
  assert.equal(R.profileFromControlMatrix({ foo: 1 }), null);
});
