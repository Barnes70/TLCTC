#!/usr/bin/env node
// Check the standalone tools in tools/ against the canon and against the site build.
//
// The tools embed their own copy of the cluster table, and nothing checked those
// copies: validate-site-definitions.js scans the site's root pages and okf/, never
// tools/. So the CBP app kept the pre-v2.3.1 #4 generic vulnerability and the
// Threat Radar kept "#8 … hardware or facilities" long after both were corrected.
//
// Checks, per tools/*.html:
//   1. canon   every embedded generic vulnerability / attacker's view / definition
//              is VERBATIM the current dictionary's string (the three JSON-owned
//              strings are never paraphrased — feedback_cluster_definition_fields)
//   2. retired a cluster's short gloss does not use wording an erratum retired
//   3. assets  the repo copy loads no /vendor/ path (a clone must run from disk),
//              and every external script/stylesheet has a self-hosted equivalent in
//              scripts/lib/tool-vendor-map.js (the site build must end up CDN-free)
//   4. readme  tools/README.md lists the tool
//
// Usage: node scripts/validate-tools.js [--verbose]
// Exit 1 on any problem.
'use strict';
const fs = require('fs');
const path = require('path');
const { toSite, unmappedAssets } = require('./lib/tool-vendor-map');

const ROOT = path.resolve(__dirname, '..');
const TOOLS = path.join(ROOT, 'tools');
const VERBOSE = process.argv.includes('--verbose');

// The newest dictionary in layer-1 is canonical; older ones are frozen records.
const DICTS = fs.readdirSync(path.join(ROOT, 'json-schemas/layer-1'))
  .map((f) => /^tlctc-framework\.v(\d+)\.(\d+)\.json$/.exec(f)).filter(Boolean)
  .sort((a, b) => (+a[1] - +b[1]) || (+a[2] - +b[2]));
const DICT_FILE = DICTS[DICTS.length - 1][0];
const dict = require(path.join(ROOT, 'json-schemas/layer-1', DICT_FILE));

// JS/JSON keys under which a tool states a JSON-owned canonical string.
const FIELD_OF = {
  genericvuln: 'generic_vulnerability', genericvulnerability: 'generic_vulnerability', generic_vulnerability: 'generic_vulnerability',
  attackerview: 'attackers_view', attackersview: 'attackers_view', attackers_view: 'attackers_view',
  definition: 'definition',
};
const CANON = {};   // field → Set of current strings
for (const c of Object.values(dict.clusters)) {
  for (const field of new Set(Object.values(FIELD_OF))) {
    if (typeof c[field] === 'string') (CANON[field] = CANON[field] || new Set()).add(c[field]);
  }
}
const CLUSTER_NAMES = Object.entries(dict.clusters).map(([id, c]) => ({ id, name: c.name }));

// Wording retired by an erratum. Checked only on a line that carries a cluster's
// name and a short gloss (description/desc), i.e. a tool's own cluster table — the
// same words are legitimate elsewhere (a "Facilities" responsibility sphere, actor
// narratives about "energy facilities").
const RETIRED = [
  { id: '#8', re: /facilit/i, why: 'v2.5.1 erratum: #8 is hardware/OT only — facilities were removed from the definition' },
  { id: '#2', re: /source[- ]code/i, why: 'v2.5: #2/#3 are substrate-neutral — a flaw in a component in the server role, not "source code"' },
  { id: '#3', re: /source[- ]code/i, why: 'v2.5: #2/#3 are substrate-neutral — a flaw in a component in the client role, not "source code"' },
];

// key: 'value' | key: "value" | "key": "value" | key: `value`
const LITERAL = /["']?\b([A-Za-z_]+)["']?\s*:\s*(['"`])((?:\\.|(?!\2)[^\\])*)\2/g;
const unescape = (s) => s.replace(/\\(['"`\\])/g, '$1').replace(/\\n/g, '\n');

const problems = [];
const report = (file, check, msg) => problems.push({ file, check, msg });

const readme = fs.readFileSync(path.join(TOOLS, 'README.md'), 'utf8');
const files = fs.readdirSync(TOOLS).filter((f) => f.endsWith('.html')).sort();
let canonChecked = 0;

for (const f of files) {
  const raw = fs.readFileSync(path.join(TOOLS, f), 'utf8');

  // 1 + 2: canon and retired wording
  const lines = raw.split(/\r?\n/);
  lines.forEach((line, i) => {
    for (const m of line.matchAll(LITERAL)) {
      const field = FIELD_OF[m[1].toLowerCase()];
      const value = unescape(m[3]).trim();
      if (field && value.length > 20) {
        canonChecked++;
        if (!CANON[field].has(value)) report(f, 'canon', `line ${i + 1}: ${m[1]} is not verbatim ${DICT_FILE} ${field}:\n      "${value}"`);
      }
      if (/^(description|desc)$/i.test(m[1])) {
        const owner = CLUSTER_NAMES.find((c) => line.includes(`'${c.name}'`) || line.includes(`"${c.name}"`));
        if (!owner) continue;
        for (const r of RETIRED) {
          if (r.id === owner.id && r.re.test(m[3])) report(f, 'retired', `line ${i + 1}: ${owner.id} gloss "${m[3]}" — ${r.why}`);
        }
      }
    }
  });

  // 3: assets
  const vendorRefs = [...raw.matchAll(/(?:src|href)="(\/vendor\/[^"]+)"/g)].map((m) => m[1]);
  for (const v of new Set(vendorRefs)) report(f, 'assets', `repo copy loads ${v} — only tlctc.net has /vendor/; use the CDN URL (the site build maps it back)`);
  for (const u of new Set(unmappedAssets(toSite(raw)))) report(f, 'assets', `${u} has no self-hosted equivalent — add it to scripts/lib/tool-vendor-map.js and /vendor/ on the site`);

  // 4: README
  if (!readme.includes(`(${f})`)) report(f, 'readme', 'not listed in tools/README.md');
}

if (problems.length) {
  console.error(`validate-tools: ${problems.length} problem(s) in ${files.length} tools (canon = ${DICT_FILE})`);
  for (const p of problems) console.error(`  ✗ [${p.check}] ${p.file} — ${p.msg}`);
  process.exit(1);
}
console.log(`validate-tools: ${files.length} tools OK — ${canonChecked} embedded canon strings verbatim ${DICT_FILE}, assets mapped, README complete`);
if (VERBOSE) for (const f of files) console.log(`  ${f}`);
