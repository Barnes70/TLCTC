#!/usr/bin/env node
// Unit tests for tools/lib/trainer-core.js — scenario redaction, study sets and agreement
// statistics of the Classification Trainer. Run: node --test scripts/test-trainer-core.js
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const T = require('../tools/lib/trainer-core.js');

const near = (a, b, eps = 0.0015) => assert.ok(Math.abs(a - b) < eps, `${a} ≉ ${b}`);

test('redact drops every sentence that names the answer or cites the framework', () => {
  const notes = 'Attacker used the stolen IAM role credentials to authenticate to AWS APIs. R-CRED: credential application is always #4. Axiom X applies here. This is Identity Theft. The session lasted two hours.';
  assert.equal(T.redact(notes), 'Attacker used the stolen IAM role credentials to authenticate to AWS APIs. The session lasted two hours.');
  assert.equal(T.redact('Designed platform function -> #1.'), '');
  assert.equal(T.redact('Standard file I/O — designed, legitimate, not flawed — abused at DA scope.'), '');
  assert.equal(T.redact('The console function is designed; the authority scope is abused.'), '');
  assert.equal(T.redact('DRE: C — mailbox content exfiltrated.'), '');
  assert.equal(T.redact(undefined), '');
  // lower-case "malware" is a description, not the cluster label
  assert.equal(T.redact('The dropper installs malware on the host.'), 'The dropper installs malware on the host.');
});

test('buildItems: one item per classified step with enough text, previous step as context', () => {
  const long = (s) => `${s} ${'x'.repeat(90)}.`;
  const rec = { file: 'attack-paths/a.json', source: 'repo', metadata: { incident_id: 'A-1' }, path_sequence: [
    { step_id: 's1', cluster: '#9', notes: long('A phishing mail arrives') },
    { step_id: 's2', cluster: '#4', notes: 'R-CRED only: #4.' },
    { mode: 'parallel', group_id: 'g', steps: [{ step_id: 's3a', cluster: '#1', notes: long('Mailbox rules created') }] },
    { step_id: 'q', status: 'unresolved', notes: long('unknown') },
  ] };
  const items = T.buildItems([rec]);
  assert.deepEqual(items.map((i) => i.id), ['attack-paths/a.json#s1', 'attack-paths/a.json#s3a']);
  assert.equal(items[0].key, '#9');
  assert.equal(items[0].prev, null);
  assert.equal(items[1].prev.cluster, '#4', 'context = the previous position, even when its own text is unusable');
  assert.equal(items[1].prev.text, '', 'previous text is redacted too');
  assert.equal(items[1].title, 'A');
  assert.ok(items[1].notes.includes('Mailbox rules'), 'full notes kept for the feedback');
});

test('studySet: deterministic, stratified across clusters, size-capped', () => {
  const items = [];
  for (const [c, n] of [['#1', 30], ['#4', 10], ['#5', 2], ['#9', 5]]) for (let i = 0; i < n; i++) items.push({ id: `${c}-${i}`, key: c });
  const a = T.studySet(items, { seed: 'tlctc-study-1', n: 8 });
  const b = T.studySet(items, { seed: 'tlctc-study-1', n: 8 });
  assert.deepEqual(a.map((i) => i.id), b.map((i) => i.id));
  assert.equal(a.length, 8);
  assert.deepEqual([...new Set(a.map((i) => i.key))].sort(), ['#1', '#4', '#5', '#9'], 'every cluster represented');
  assert.notDeepEqual(T.studySet(items, { seed: 'other', n: 8 }).map((i) => i.id), a.map((i) => i.id));
  assert.equal(T.studySet(items, { seed: 's', n: 500 }).length, items.length);
});

test('Fleiss kappa: the classic 10 subjects × 14 raters example gives 0.210', () => {
  const table = [[0, 0, 0, 0, 14], [0, 2, 6, 4, 2], [0, 0, 3, 5, 6], [0, 3, 9, 2, 0], [2, 2, 8, 1, 1],
    [7, 7, 0, 0, 0], [3, 2, 6, 3, 0], [2, 5, 3, 2, 2], [6, 5, 2, 1, 0], [0, 2, 2, 3, 7]];
  const r = T.fleissKappa(table);
  near(r.kappa, 0.210);
  near(r.p_bar, 0.378);
  near(r.p_e, 0.213);
  assert.equal(r.per_category.length, 5);
});

test('Fleiss kappa: perfect agreement is 1; a single category leaves kappa undefined', () => {
  assert.equal(T.fleissKappa([[3, 0], [0, 3]]).kappa, 1);
  assert.equal(T.fleissKappa([[3, 0], [3, 0]]).kappa, null);
});

test('Cohen kappa: 50 items, 20/5/10/15 gives 0.4', () => {
  const a = [], b = [];
  const push = (x, y, n) => { for (let i = 0; i < n; i++) { a.push(x); b.push(y); } };
  push('yes', 'yes', 20); push('yes', 'no', 5); push('no', 'yes', 10); push('no', 'no', 15);
  near(T.cohenKappa(a, b), 0.4);
  assert.equal(T.cohenKappa(['x', 'x'], ['x', 'x']), null, 'undefined when chance agreement is 1');
});

test('landisKoch labels', () => {
  assert.equal(T.landisKoch(-0.1), 'poor');
  assert.equal(T.landisKoch(0.1), 'slight');
  assert.equal(T.landisKoch(0.3), 'fair');
  assert.equal(T.landisKoch(0.5), 'moderate');
  assert.equal(T.landisKoch(0.7), 'substantial');
  assert.equal(T.landisKoch(0.9), 'almost perfect');
  assert.equal(T.landisKoch(null), 'undefined');
});

test('analyzeSheets: groups by study, pools ratings, compares with the key', () => {
  const items = [{ id: 'i1', key: '#1' }, { id: 'i2', key: '#4' }, { id: 'i3', key: '#9' }];
  const sheet = (rater, answers, study = 'S') => ({ schema: 'tlctc-rating-sheet.v1', study_id: study, rater, answers: answers.map((a, k) => ({ item: `i${k + 1}`, answer: a })) });
  const res = T.analyzeSheets([sheet('ann', ['#1', '#4', '#9']), sheet('bob', ['#1', '#1', '#9']), sheet('eve', ['#2'], 'OTHER')], items);
  assert.equal(res.study_id, 'S');
  assert.deepEqual(res.raters.map((r) => r.rater), ['ann', 'bob']);
  assert.deepEqual(res.rejected.map((r) => r.rater), ['eve']);
  assert.equal(res.items.length, 3);
  assert.equal(res.raters[0].accuracy, 1);
  near(res.raters[1].accuracy, 2 / 3);
  assert.equal(res.items.find((i) => i.id === 'i2').agreement, 0, 'two raters split: pairwise agreement 0');
  assert.equal(res.confusion['#4']['#1'], 1);
  assert.ok(res.fleiss.kappa > 0 && res.fleiss.kappa < 1);
  assert.equal(T.analyzeSheets([sheet('ann', ['#1', '#4', '#9'])], items).fleiss, null, 'one rater: no inter-rater kappa');
});

test('ruleIdsIn finds rule ids cited in notes', () => {
  assert.deepEqual(T.ruleIdsIn('R-CRED applies; see also R-UNRES-9 and r-exec (not a rule id).'), ['R-CRED', 'R-UNRES-9']);
});

// ---- the real corpus
const BUNDLE = path.join(__dirname, '..', 'tools', 'data', 'path-corpus.js');
test('bundled corpus: redacted scenarios never contain a cluster number, rule id or cluster name', { skip: !fs.existsSync(BUNDLE) && 'bundle not built' }, () => {
  const ctx = { window: {} };
  vm.runInNewContext(fs.readFileSync(BUNDLE, 'utf8'), ctx);
  const items = T.buildItems(ctx.window.TLCTC_PATH_CORPUS.records.filter((r) => r.source === 'repo'));
  assert.ok(items.length > 250, `${items.length} usable scenarios`);
  for (const it of items) {
    for (const re of T.LEAK_PATTERNS) {
      assert.ok(!re.test(it.text), `${it.id} leaks ${re}: ${it.text}`);
      if (it.prev) assert.ok(!re.test(it.prev.text), `${it.id} context leaks ${re}`);
    }
  }
  assert.equal(new Set(items.map((i) => i.key)).size, 10, 'all ten clusters have scenarios');
});
