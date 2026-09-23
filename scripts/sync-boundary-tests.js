#!/usr/bin/env node
/*
 * sync-boundary-tests.js — mirror the canonical boundary tests of core paper §4 into
 * whitepaper §4.1 (v2.6, C18). `--check` reports drift and exits 1 without writing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const bt = require('./boundary-tests');

const ROOT = path.resolve(__dirname, '..');
const CORE = path.join(ROOT, 'documentation/tlctc-v2.6-core.md');
const WP = path.join(ROOT, 'documentation/tlctc-v2.0-whitepaper.md');

const core = fs.readFileSync(CORE, 'utf8');
const wp = fs.readFileSync(WP, 'utf8');
const drift = bt.diff(core, wp);

if (process.argv.includes('--check')) {
  if (drift.length) {
    console.error('boundary tests: whitepaper §4.1 differs from core §4\n  ' + drift.join('\n  '));
    process.exit(1);
  }
  console.log('boundary tests: whitepaper §4.1 mirrors core §4');
  process.exit(0);
}
if (!drift.length) {
  console.log('boundary tests: already in sync');
  process.exit(0);
}
fs.writeFileSync(WP, bt.sync(core, wp), 'utf8');
const after = bt.diff(core, fs.readFileSync(WP, 'utf8'));
if (after.length) {
  console.error('boundary tests: sync incomplete\n  ' + after.join('\n  '));
  process.exit(1);
}
console.log(`boundary tests: whitepaper §4.1 updated (${drift.length} difference(s) resolved)`);
