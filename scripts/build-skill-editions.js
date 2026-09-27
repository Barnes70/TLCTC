/*
 * build-skill-editions.js — Generate the distributable editions of the tlctc-classify agent
 * skill from the Claude Code plugin skill, so no edition can drift from the source.
 *
 * Usage:  node scripts/build-skill-editions.js            (write the files)
 *         node scripts/build-skill-editions.js --check    (exit 1 if a committed file differs)
 * Source: plugins/tlctc/skills/tlctc-classify/SKILL.md   (single source of the skill text)
 *
 * Editions:
 *   clawhub  integrations/clawhub/tlctc-classify/SKILL.md
 *            For the ClawHub registry (OpenClaw; Hermes Agent reads ClawHub too). ClawHub
 *            publishes every skill under MIT-0 and forbids conflicting licence terms in
 *            SKILL.md, so the `license` line is dropped.
 *   web      integrations/well-known/skills/tlctc-classify/SKILL.md + index.json
 *            Served by tlctc.net at /.well-known/skills/ (Agent Skills discovery endpoint;
 *            Hermes: `well-known:` source). Keeps the CC BY 4.0 licence.
 *
 * Both editions differ from the source only in: frontmatter (`version` from plugin.json,
 * `homepage`, plus `author` in the web edition, and the licence rule above), an attribution line after the
 * frontmatter (a citation, not a licence term), and the body's reference to "the surrounding
 * TLCTC repository", which becomes absolute GitHub links because an installed skill has no
 * repository around it. Every body rewrite must hit exactly once, so an edit to the source
 * that moves the text fails the build instead of silently skipping the rewrite.
 *
 * Deps: Node builtins only. require()-able: see module.exports.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'plugins/tlctc/skills/tlctc-classify/SKILL.md');
const PLUGIN = path.join(ROOT, 'plugins/tlctc/.claude-plugin/plugin.json');

const HOMEPAGE = 'https://www.tlctc.net';
const REPO = 'https://github.com/Barnes70/TLCTC';
const AUTHOR = 'Bernhard Kreinz';
const ATTRIBUTION =
  `> **TLCTC — Top Level Cyber Threat Clusters**, created by ${AUTHOR} ` +
  '([ORCID 0009-0005-2148-9903](https://orcid.org/0009-0005-2148-9903)). ' +
  `Home: [tlctc.net](${HOMEPAGE}) · canonical releases: ` +
  '[doi.org/10.5281/zenodo.20633176](https://doi.org/10.5281/zenodo.20633176) · ' +
  `source: [github.com/Barnes70/TLCTC](${REPO}).`;

const BODY_REWRITES = [
  [
    'also follow the schema and rules in the surrounding TLCTC repository (CLAUDE.md, `json-schemas/layer-3/`).',
    `also follow the schema and rules in the TLCTC repository: [\`json-schemas/layer-3/\`](${REPO}/tree/main/json-schemas/layer-3) and [\`CLAUDE.md\`](${REPO}/blob/main/CLAUDE.md).`
  ]
];

const EDITIONS = {
  clawhub: { dir: path.join(ROOT, 'integrations/clawhub/tlctc-classify'), license: false, author: false },
  web: { dir: path.join(ROOT, 'integrations/well-known/skills/tlctc-classify'), license: true, author: true,
         index: path.join(ROOT, 'integrations/well-known/skills/index.json') }
};

function parseSource() {
  const src = fs.readFileSync(SRC, 'utf8');
  const eol = src.includes('\r\n') ? '\r\n' : '\n';
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n/.exec(src);
  if (!m) throw new Error('source SKILL.md has no frontmatter');
  const fm = m[1].split(/\r?\n/);
  const pick = key => {
    const line = fm.find(l => l.startsWith(key + ':'));
    if (!line) throw new Error(`source frontmatter lacks "${key}"`);
    return line;
  };
  const version = JSON.parse(fs.readFileSync(PLUGIN, 'utf8')).version;
  if (!/^\d+\.\d+\.\d+$/.test(version)) throw new Error(`plugin.json version "${version}" is not semver`);
  let body = src.slice(m[0].length);
  for (const [from, to] of BODY_REWRITES) {
    const hits = body.split(from).length - 1;
    if (hits !== 1) throw new Error(`body rewrite expected 1 hit, got ${hits}: "${from.slice(0, 60)}…"`);
    body = body.replace(from, to);
  }
  return { eol, pick, version, body };
}

// { 'relative/path': text } for every file an edition consists of
function render(name) {
  const ed = EDITIONS[name];
  if (!ed) throw new Error(`unknown edition ${name}`);
  const { eol, pick, version, body } = parseSource();
  const front = ['---', pick('name'), pick('description'), `version: ${version}`];
  if (ed.author) front.push(`author: ${AUTHOR}`);
  front.push(`homepage: ${HOMEPAGE}`);
  if (ed.license) front.push(pick('license'));
  front.push('---');
  const skill = front.join(eol) + eol + eol + ATTRIBUTION + eol + body;
  const out = { [path.join(ed.dir, 'SKILL.md')]: skill };
  if (ed.index) {
    const skillName = pick('name').slice('name:'.length).trim();
    const description = pick('description').slice('description:'.length).trim();
    out[ed.index] = JSON.stringify({ skills: [{ name: skillName, description, files: ['SKILL.md'] }] }, null, 2) + '\n';
  }
  return out;
}

if (require.main === module) {
  const check = process.argv.includes('--check');
  let stale = 0;
  for (const name of Object.keys(EDITIONS)) {
    for (const [file, text] of Object.entries(render(name))) {
      const relp = path.relative(ROOT, file);
      if (check) {
        const cur = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : '';
        if (cur !== text) { console.error(`✗ ${relp} is stale — run: npm run build-skills`); stale++; }
      } else {
        fs.mkdirSync(path.dirname(file), { recursive: true });
        fs.writeFileSync(file, text);
        console.log(`wrote ${relp} (${Buffer.byteLength(text)} bytes)`);
      }
    }
  }
  if (check) { if (stale) process.exit(1); console.log('✓ skill editions are up to date'); }
}

module.exports = { render, EDITIONS, SRC, PLUGIN, ATTRIBUTION, AUTHOR };
