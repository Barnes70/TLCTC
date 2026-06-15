#!/usr/bin/env node
/*
 * validate-okf.js — Conformance checker for an OKF bundle (SPEC v0.1).
 *
 * Asserts:
 *   - every non-reserved .md has parseable YAML frontmatter with a non-empty `type`
 *   - reserved files (index.md, log.md, README.md) carry NO frontmatter
 * Warns (does not fail) on intra-bundle broken links — consumers must tolerate them.
 *
 * Usage:  node scripts/validate-okf.js [okf-dir]   (default: okf/)
 * Exit:   0 = conformant, 1 = errors.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const RESERVED = new Set(['index.md', 'log.md', 'README.md']);
const dir = path.resolve(process.argv[2] || path.join(__dirname, '..', 'okf'));

function walk(d, acc) {
  for (const name of fs.readdirSync(d)) {
    const p = path.join(d, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) walk(p, acc);
    else if (name.endsWith('.md')) acc.push(p);
  }
  return acc;
}

// Minimal frontmatter reader: returns { has, keys } — keys is a flat top-level set.
function readFrontmatter(text) {
  if (!text.startsWith('---')) return { has: false, type: null };
  const end = text.indexOf('\n---', 3);
  if (end === -1) return { has: true, type: null, broken: true };
  const block = text.slice(3, end);
  let type = null;
  for (const line of block.split('\n')) {
    const m = line.match(/^type:\s*(.*)$/);
    if (m) type = m[1].replace(/^["']|["']$/g, '').trim();
  }
  return { has: true, type };
}

function main() {
  if (!fs.existsSync(dir)) { console.error(`No such directory: ${dir}`); process.exit(1); }
  const files = walk(dir, []);
  const errors = [];
  const warnings = [];
  const existing = new Set(files.map((f) => '/' + path.relative(dir, f).split(path.sep).join('/')));

  for (const f of files) {
    const rel = path.relative(dir, f).split(path.sep).join('/');
    const base = path.basename(f);
    const text = fs.readFileSync(f, 'utf8');
    const fm = readFrontmatter(text);

    if (RESERVED.has(base)) {
      if (fm.has) errors.push(`${rel}: reserved file must NOT have frontmatter`);
    } else {
      if (!fm.has) errors.push(`${rel}: missing YAML frontmatter`);
      else if (fm.broken) errors.push(`${rel}: unterminated frontmatter block`);
      else if (!fm.type) errors.push(`${rel}: frontmatter missing non-empty 'type'`);
    }

    // intra-bundle absolute links: /foo/bar.md
    const linkRe = /\]\((\/[^)#\s]+\.md)(?:#[^)]*)?\)/g;
    let m;
    while ((m = linkRe.exec(text)) !== null) {
      if (!existing.has(m[1])) warnings.push(`${rel}: broken link → ${m[1]}`);
    }
  }

  console.log(`Checked ${files.length} markdown files in ${dir}`);
  if (warnings.length) {
    console.log(`\n${warnings.length} broken-link warning(s):`);
    for (const w of warnings.slice(0, 50)) console.log('  ⚠ ' + w);
    if (warnings.length > 50) console.log(`  … and ${warnings.length - 50} more`);
  }
  if (errors.length) {
    console.log(`\nINVALID — ${errors.length} error(s):`);
    for (const e of errors.slice(0, 100)) console.log('  ✗ ' + e);
    process.exit(1);
  }
  console.log('\nVALID — all non-reserved docs have a non-empty type; reserved files clean.');
}

main();
