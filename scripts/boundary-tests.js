'use strict';
/*
 * boundary-tests.js — per-cluster boundary tests are canonical in core paper §4 and
 * mirrored verbatim in whitepaper §4.1 (v2.6, change C18). build-okf renders the
 * whitepaper's cluster sections into okf/, so a stale mirror reaches every OKF reader;
 * this module finds both lists so build-okf can refuse drift and
 * sync-boundary-tests.js can repair it.
 */

const norm = (s) => String(s)
  .replace(/[‘’]/g, "'")
  .replace(/[“”]/g, '"')
  .replace(/\*\*/g, '')
  .replace(/\s+/g, ' ')
  .trim();

const LIST_HEAD = /^\*\*Boundary tests \(normative\):\*\*\s*$/i;

// Cluster sections as line ranges. level '###' = core §4, '####' = whitepaper §4.1.
function sections(lines, level) {
  const head = new RegExp(`^${level}\\s+#(\\d{1,2})\\s`);
  const anyHead = /^#{2,4}\s/;
  const out = {};
  for (let i = 0; i < lines.length; i++) {
    const m = head.exec(lines[i]);
    if (!m) continue;
    let end = i + 1;
    while (end < lines.length && !anyHead.test(lines[end])) end++;
    out[m[1]] = { from: i + 1, to: end };
  }
  return out;
}

// The bullet run under the "Boundary tests (normative):" heading, as inclusive line indices.
function findList(lines, from, to) {
  for (let i = from; i < to; i++) {
    if (!LIST_HEAD.test(lines[i])) continue;
    let j = i + 1;
    while (j < to && lines[j].trim() === '') j++;
    const first = j;
    while (j < to && /^- /.test(lines[j])) j++;
    return j > first ? { first, last: j - 1 } : null;
  }
  return null;
}

function lists(md, level) {
  const lines = md.split(/\r?\n/);
  const out = {};
  for (const [n, s] of Object.entries(sections(lines, level))) {
    const l = findList(lines, s.from, s.to);
    if (l) out[n] = { ...l, items: lines.slice(l.first, l.last + 1) };
  }
  return { lines, lists: out };
}

// Differences between core §4 (canonical) and whitepaper §4.1, as printable lines.
function diff(coreMd, whitepaperMd) {
  const core = lists(coreMd, '###').lists;
  const wp = lists(whitepaperMd, '####').lists;
  const out = [];
  for (let n = 1; n <= 10; n++) {
    const c = core[n];
    const w = wp[n];
    if (!c) { out.push(`#${n}: core §4 has no boundary-test list`); continue; }
    if (!w) { out.push(`#${n}: whitepaper §4.1 has no boundary-test list`); continue; }
    const len = Math.max(c.items.length, w.items.length);
    for (let i = 0; i < len; i++) {
      const a = c.items[i] === undefined ? '(missing)' : norm(c.items[i]);
      const b = w.items[i] === undefined ? '(missing)' : norm(w.items[i]);
      if (a !== b) out.push(`#${n} test ${i + 1}\n    core:       ${a}\n    whitepaper: ${b}`);
    }
  }
  return out;
}

// Whitepaper text with every cluster's boundary-test list replaced by the core's bullets.
function sync(coreMd, whitepaperMd) {
  const eol = whitepaperMd.includes('\r\n') ? '\r\n' : '\n';
  const core = lists(coreMd, '###').lists;
  const { lines, lists: wp } = lists(whitepaperMd, '####');
  // bottom-up, so earlier line indices stay valid
  for (const n of Object.keys(wp).map(Number).sort((a, b) => b - a)) {
    if (!core[n]) continue;
    lines.splice(wp[n].first, wp[n].last - wp[n].first + 1, ...core[n].items);
  }
  return lines.join(eol);
}

module.exports = { norm, lists, diff, sync };
