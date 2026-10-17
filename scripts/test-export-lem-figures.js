'use strict';
// Tests for scripts/export-lem-figures.js.
const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const { exportFigures } = require('./export-lem-figures');

const ROOT = path.resolve(__dirname, '..');
const fig = (vb, body) => `<svg class="lem-fig" viewBox="${vb}" xmlns="http://www.w3.org/2000/svg" role="img">${body}</svg>`;
const page = `<p>x</p>${fig('0 0 920 320', '<rect class="bx"/>')}<p>y</p>${fig('0 0 900 660', '<text class="mono acc-txt">A</text>')}`;

test('exports exactly two standalone SVGs with explicit size and a style block', () => {
  const out = exportFigures(page);
  assert.strictEqual(out.length, 2);
  assert.match(out[0], /^<svg width="920" height="320" viewBox="0 0 920 320"/);
  assert.match(out[1], /^<svg width="900" height="660" viewBox="0 0 900 660"/);
  for (const s of out) {
    assert.doesNotMatch(s, /class="lem-fig"/);
    assert.match(s, /<style>[\s\S]*\.acc-txt \{ fill: #e5484d; \}[\s\S]*<\/style>/);
    assert.doesNotMatch(s, /var\(/);
  }
});

test('refuses a page without exactly two figures', () => {
  assert.throws(() => exportFigures(fig('0 0 1 1', '')), /expected 2 figures, found 1/);
});

test('committed figures: no CSS variables, no facility layer', () => {
  const f1 = fs.readFileSync(path.join(ROOT, 'documentation/images/lem-five-structures.svg'), 'utf8');
  const f2 = fs.readFileSync(path.join(ROOT, 'documentation/images/lem-typed-incident.svg'), 'utf8');
  for (const s of [f1, f2]) assert.doesNotMatch(s, /var\(/);
  assert.doesNotMatch(f1, /Facility/);
  assert.match(f1, /System risk event/);
});

test('HTML named entities become numeric references (standalone SVG is XML)', () => {
  const out = exportFigures(`${fig('0 0 9 9', '<text>&Delta;t &gt; 0</text>')}${fig('0 0 9 9', '')}`);
  assert.match(out[0], /&#916;t &gt; 0/);
  assert.doesNotMatch(out[0], /&Delta;/);
  assert.throws(() => exportFigures(`${fig('0 0 9 9', '<text>&nope;</text>')}${fig('0 0 9 9', '')}`), /unknown entity &nope;/);
});

test('entity names with digits are matched, not left raw; unexpected <svg> attribute order throws', () => {
  assert.throws(() => exportFigures(`${fig('0 0 9 9', '<text>&frac12;</text>')}${fig('0 0 9 9', '')}`), /unknown entity &frac12;/);
  const odd = '<svg class="lem-fig" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 9 9"></svg>';
  assert.throws(() => exportFigures(odd + odd), /figure <svg> tag not in the expected form/);
});

test('committed figures are well-formed: only XML entities', () => {
  for (const n of ['lem-five-structures.svg', 'lem-typed-incident.svg']) {
    const s = fs.readFileSync(path.join(ROOT, 'documentation/images', n), 'utf8');
    for (const m of s.match(/&[A-Za-z][A-Za-z0-9]*;/g) || []) assert.ok(['&amp;', '&lt;', '&gt;', '&quot;', '&apos;'].includes(m), `${n}: ${m}`);
  }
});
