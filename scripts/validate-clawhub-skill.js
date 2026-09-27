/*
 * validate-clawhub-skill.js — Check the ClawHub edition of tlctc-classify against
 * ClawHub's publishing rules and against its source.
 *
 * Usage:  node scripts/validate-clawhub-skill.js
 *
 * Rules checked (ClawHub docs/skill-format.md):
 *   - the skill folder holds SKILL.md only (every regular file in it would be published);
 *   - frontmatter has name (1–64 of [a-z0-9-]), description and a semver version;
 *   - no licence terms anywhere: ClawHub publishes all skills as MIT-0 and forbids
 *     conflicting terms in SKILL.md;
 *   - bundle under the 50 MB limit.
 * Project rules:
 *   - version equals the plugin version;
 *   - the attribution line is present;
 *   - the file is byte-identical to a fresh render from the plugin skill (no drift).
 *
 * Deps: Node builtins only.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { render, OUT, PLUGIN, ATTRIBUTION } = require('./build-clawhub-skill');

const errors = [];
const fail = msg => errors.push(msg);

const dir = path.dirname(OUT);
const files = fs.readdirSync(dir);
if (files.length !== 1 || files[0] !== 'SKILL.md') fail(`skill folder must contain SKILL.md only, found: ${files.join(', ')}`);

const text = fs.readFileSync(OUT, 'utf8');
const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n/.exec(text);
if (!m) fail('no frontmatter');
const fm = {};
(m ? m[1].split(/\r?\n/) : []).forEach(l => { const i = l.indexOf(':'); if (i > 0) fm[l.slice(0, i).trim()] = l.slice(i + 1).trim(); });

if (!/^[a-z0-9-]{1,64}$/.test(fm.name || '')) fail(`name "${fm.name}" must be 1–64 of [a-z0-9-]`);
if (!fm.description) fail('description missing');
if (!/^\d+\.\d+\.\d+$/.test(fm.version || '')) fail(`version "${fm.version}" is not semver`);
const pv = JSON.parse(fs.readFileSync(PLUGIN, 'utf8')).version;
if (fm.version !== pv) fail(`version ${fm.version} differs from plugin version ${pv}`);
if ('license' in fm) fail('frontmatter carries a license key (ClawHub: MIT-0 only, no overrides)');
const lic = text.match(/.{0,40}\b(licen[cs]e[ds]?|CC[- ]BY|copyright|all rights reserved)\b.{0,40}/i);
if (lic) fail(`licence term in SKILL.md: "…${lic[0]}…"`);
if (!text.includes(ATTRIBUTION)) fail('attribution line missing');

const bytes = Buffer.byteLength(text);
if (bytes > 50 * 1024 * 1024) fail(`bundle ${bytes} bytes exceeds 50 MB`);
if (text !== render()) fail('file differs from a fresh render of the plugin skill — run: npm run build-clawhub');

if (errors.length) {
  errors.forEach(e => console.error('✗ ' + e));
  process.exit(1);
}
console.log(`✓ ClawHub skill ${fm.name}@${fm.version}: ${bytes} bytes, frontmatter valid, no licence terms, attribution present, in sync with plugin`);
