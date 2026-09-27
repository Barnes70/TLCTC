/*
 * build-clawhub-skill.js — Generate the ClawHub edition of the tlctc-classify skill
 * from the Claude Code plugin skill, so the two can never drift apart.
 *
 * Usage:  node scripts/build-clawhub-skill.js            (write the file)
 *         node scripts/build-clawhub-skill.js --check    (exit 1 if the committed file differs)
 * Source: plugins/tlctc/skills/tlctc-classify/SKILL.md   (single source of the skill text)
 * Output: integrations/clawhub/tlctc-classify/SKILL.md
 *
 * ClawHub publishes every skill under MIT-0 and forbids conflicting licence terms in
 * SKILL.md, so the edition differs from the source in exactly three ways:
 *   1. frontmatter: `license` dropped; `version` (required by ClawHub) and `homepage` added;
 *   2. an attribution line after the frontmatter (a citation, not a licence term);
 *   3. body references to the surrounding repository become absolute GitHub URLs,
 *      because a ClawHub install has no repository around it.
 * Every body replacement must hit exactly once, so an edit to the source that moves
 * the text fails the build instead of silently skipping the rewrite.
 *
 * Deps: Node builtins only. require()-able: see module.exports.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'plugins/tlctc/skills/tlctc-classify/SKILL.md');
const PLUGIN = path.join(ROOT, 'plugins/tlctc/.claude-plugin/plugin.json');
const OUT = path.join(ROOT, 'integrations/clawhub/tlctc-classify/SKILL.md');

const HOMEPAGE = 'https://www.tlctc.net';
const REPO = 'https://github.com/Barnes70/TLCTC';
const ATTRIBUTION =
  '> **TLCTC — Top Level Cyber Threat Clusters**, created by Bernhard Kreinz ' +
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

function render() {
  const src = fs.readFileSync(SRC, 'utf8');
  const eol = src.includes('\r\n') ? '\r\n' : '\n';
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n/.exec(src);
  if (!m) throw new Error('source SKILL.md has no frontmatter');
  const version = JSON.parse(fs.readFileSync(PLUGIN, 'utf8')).version;
  if (!/^\d+\.\d+\.\d+$/.test(version)) throw new Error(`plugin.json version "${version}" is not semver`);

  const fm = m[1].split(/\r?\n/);
  const pick = key => {
    const line = fm.find(l => l.startsWith(key + ':'));
    if (!line) throw new Error(`source frontmatter lacks "${key}"`);
    return line;
  };
  const front = ['---', pick('name'), pick('description'), `version: ${version}`, `homepage: ${HOMEPAGE}`, '---'];

  let body = src.slice(m[0].length);
  for (const [from, to] of BODY_REWRITES) {
    const hits = body.split(from).length - 1;
    if (hits !== 1) throw new Error(`body rewrite expected 1 hit, got ${hits}: "${from.slice(0, 60)}…"`);
    body = body.replace(from, to);
  }
  return front.join(eol) + eol + eol + ATTRIBUTION + eol + body;
}

if (require.main === module) {
  const out = render();
  if (process.argv.includes('--check')) {
    const cur = fs.existsSync(OUT) ? fs.readFileSync(OUT, 'utf8') : '';
    if (cur !== out) { console.error(`✗ ${path.relative(ROOT, OUT)} is stale — run: npm run build-clawhub`); process.exit(1); }
    console.log(`✓ ${path.relative(ROOT, OUT)} is up to date`);
  } else {
    fs.mkdirSync(path.dirname(OUT), { recursive: true });
    fs.writeFileSync(OUT, out);
    console.log(`wrote ${path.relative(ROOT, OUT)} (${Buffer.byteLength(out)} bytes)`);
  }
}

module.exports = { render, SRC, OUT, PLUGIN, ATTRIBUTION };
