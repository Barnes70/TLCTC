/*
 * validate-skill-editions.js — Check the distributable editions of the tlctc-classify skill
 * (see build-skill-editions.js) against their channels' rules and against the source.
 *
 * Usage:  node scripts/validate-skill-editions.js
 *
 * Both editions:
 *   - the skill folder holds SKILL.md only (every regular file in it is distributed);
 *   - frontmatter: name 1–64 of [a-z0-9-], description, semver version equal to plugin.json;
 *   - attribution line present;
 *   - byte-identical to a fresh render from the plugin skill (no drift).
 * clawhub: no licence terms anywhere (ClawHub publishes all skills as MIT-0 and forbids
 *          conflicting terms in SKILL.md); bundle under the 50 MB limit.
 * web:     `license: CC-BY-4.0` present; index.json lists exactly the skill with the same
 *          name and description and files ["SKILL.md"] (Agent Skills discovery format read
 *          by Hermes Agent's well-known source).
 *
 * Deps: Node builtins only.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { render, EDITIONS, PLUGIN, ATTRIBUTION } = require('./build-skill-editions');

const errors = [];
const pv = JSON.parse(fs.readFileSync(PLUGIN, 'utf8')).version;

function frontmatter(text) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n/.exec(text);
  const fm = {};
  (m ? m[1].split(/\r?\n/) : []).forEach(l => { const i = l.indexOf(':'); if (i > 0) fm[l.slice(0, i).trim()] = l.slice(i + 1).trim(); });
  return m ? fm : null;
}

for (const [name, ed] of Object.entries(EDITIONS)) {
  const fail = msg => errors.push(`[${name}] ${msg}`);
  const files = fs.existsSync(ed.dir) ? fs.readdirSync(ed.dir) : [];
  if (files.length !== 1 || files[0] !== 'SKILL.md') { fail(`skill folder must contain SKILL.md only, found: ${files.join(', ') || 'nothing'}`); continue; }
  const text = fs.readFileSync(path.join(ed.dir, 'SKILL.md'), 'utf8');
  const fm = frontmatter(text);
  if (!fm) { fail('no frontmatter'); continue; }
  if (!/^[a-z0-9-]{1,64}$/.test(fm.name || '')) fail(`name "${fm.name}" must be 1–64 of [a-z0-9-]`);
  if (!fm.description) fail('description missing');
  if (fm.version !== pv) fail(`version "${fm.version}" differs from plugin version ${pv}`);
  if (!text.includes(ATTRIBUTION)) fail('attribution line missing');

  if (ed.license) {
    if (fm.license !== 'CC-BY-4.0') fail(`license must be CC-BY-4.0, is "${fm.license}"`);
  } else {
    if ('license' in fm) fail('frontmatter carries a license key (ClawHub: MIT-0 only, no overrides)');
    const lic = text.match(/.{0,40}\b(licen[cs]e[ds]?|CC[- ]BY|copyright|all rights reserved)\b.{0,40}/i);
    if (lic) fail(`licence term in SKILL.md: "…${lic[0]}…"`);
    if (Buffer.byteLength(text) > 50 * 1024 * 1024) fail('bundle exceeds 50 MB');
  }

  if (ed.index) {
    let idx;
    try { idx = JSON.parse(fs.readFileSync(ed.index, 'utf8')); } catch (e) { fail(`index.json unreadable: ${e.message}`); }
    const s = idx && Array.isArray(idx.skills) && idx.skills.find(x => x.name === fm.name);
    if (!s) fail(`index.json does not list "${fm.name}"`);
    else {
      if (s.description !== fm.description) fail('index.json description differs from SKILL.md');
      if (JSON.stringify(s.files) !== '["SKILL.md"]') fail(`index.json files must be ["SKILL.md"], is ${JSON.stringify(s.files)}`);
      if (path.basename(ed.dir) !== s.name) fail(`skill folder "${path.basename(ed.dir)}" must equal the index name "${s.name}"`);
    }
  }

  for (const [file, want] of Object.entries(render(name))) {
    const cur = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : null;
    if (cur !== want) fail(`${path.relative(path.resolve(__dirname, '..'), file)} differs from a fresh render — run: npm run build-skills`);
  }
  if (!errors.some(e => e.startsWith(`[${name}]`))) console.log(`✓ ${name} edition: ${fm.name}@${fm.version}, ${Buffer.byteLength(text)} bytes, in sync with the plugin skill`);
}

if (errors.length) { errors.forEach(e => console.error('✗ ' + e)); process.exit(1); }
