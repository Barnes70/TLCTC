#!/usr/bin/env node
// Validate mappings/nist-csf-2.0/csf2-tlctc-mapping.json and generate from it:
//   tools/control-matrix-starter-nist-csf2.json — Control Matrix starter (all 60 cells)
//   tools/data/csf2-tlctc.js                    — window.TLCTC_CSF2 for the site's CSF page
//
// The mapping file is the single source. Cluster-specific subcategories become Local controls
// in their rows; cluster-neutral ones ("all") become one shared control each, linked into the
// Umbrella list of all ten rows of their function column; "none" (outside the threat axis) is
// placed in no cell. `npm run validate` rebuilds both outputs, so a mapping change shows up as
// a git diff.
//
// Usage: node scripts/build-csf2.js
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = 'mappings/nist-csf-2.0/csf2-tlctc-mapping.json';
const OUT_STARTER = 'tools/control-matrix-starter-nist-csf2.json';
const OUT_DATA = 'tools/data/csf2-tlctc.js';
const m = JSON.parse(fs.readFileSync(path.join(ROOT, SRC), 'utf8'));

// ───────── validate ─────────
const errors = [];
const FUNCS = ['GV', 'ID', 'PR', 'DE', 'RS', 'RC'];
const CLUSTERS = Array.from({ length: 10 }, (_, i) => `#${i + 1}`);
const KINDS = ['tech', 'org'];
const EXPECT = { functions: 6, categories: 22, subcategories: 106 }; // CSF 2.0 Core, CSWP 29 Appendix A
for (const [k, n] of Object.entries(EXPECT)) if ((m[k] || []).length !== n) errors.push(`${k}: expected ${n}, found ${(m[k] || []).length}`);
if (m.functions.map((f) => f.id).join() !== FUNCS.join()) errors.push(`functions must be ${FUNCS.join(', ')} in order`);
const cats = new Map();
for (const c of m.categories) {
  if (!/^(GV|ID|PR|DE|RS|RC)\.[A-Z]{2}$/.test(c.id)) errors.push(`category id ${c.id}`);
  if (cats.has(c.id)) errors.push(`duplicate category ${c.id}`);
  if (!c.name || !c.text) errors.push(`category ${c.id}: name and text required`);
  cats.set(c.id, c);
}
const seen = new Set();
for (const s of m.subcategories) {
  const where = `subcategory ${s.id}`;
  const mm = /^((GV|ID|PR|DE|RS|RC)\.[A-Z]{2})-\d{2}$/.exec(s.id || '');
  if (!mm) { errors.push(`${where}: bad id`); continue; }
  if (seen.has(s.id)) errors.push(`${where}: duplicate`);
  seen.add(s.id);
  if (!cats.has(mm[1])) errors.push(`${where}: unknown category ${mm[1]}`);
  if (!s.text || /\s{2}|^\s|\s$/.test(s.text)) errors.push(`${where}: text missing or not whitespace-normalised`);
  if (!KINDS.includes(s.kind)) errors.push(`${where}: kind must be ${KINDS.join(' or ')}`);
  if (!s.rationale) errors.push(`${where}: rationale required`);
  if (Array.isArray(s.clusters)) {
    if (!s.clusters.length) errors.push(`${where}: empty clusters array (use "all" or "none")`);
    const bad = s.clusters.filter((c) => !CLUSTERS.includes(c));
    if (bad.length) errors.push(`${where}: unknown clusters ${bad.join(', ')}`);
    if (new Set(s.clusters).size !== s.clusters.length) errors.push(`${where}: duplicate clusters`);
  } else if (s.clusters !== 'all' && s.clusters !== 'none') errors.push(`${where}: clusters must be an array, "all" or "none"`);
}
if (errors.length) {
  console.error(`build-csf2: ${SRC} failed validation:\n  ` + errors.join('\n  '));
  process.exit(1);
}

// ───────── outputs ─────────
const fnOf = (id) => id.slice(0, 2);
const catOf = (id) => id.slice(0, 5);
const nameOf = (s) => `${s.id} — ${s.text}`;
const descOf = (s) => `${cats.get(catOf(s.id)).name} (${catOf(s.id)}). TLCTC: ${s.rationale}`;
const LINK = m.meta.source.url;
const emptyCde = () => ({ value: null, rationale: '', set_by: '', last_reviewed: '', review_trigger: '' });

const cells = {};
for (const c of CLUSTERS) for (const f of FUNCS) cells[`${c.slice(1)}-${f}`] = { local: [], umbrella: [] };
const sharedControls = [];
for (const s of m.subcategories) {
  if (Array.isArray(s.clusters)) {
    for (const c of s.clusters) cells[`${c.slice(1)}-${fnOf(s.id)}`].local.push({
      id: `csf-${s.id}-${c.slice(1)}`, name: nameOf(s), description: descOf(s), linkMore: LINK,
      ownerName: '', ownerOrgChart: '', kind: s.kind, maturity: 0, linkJira: '', role: '',
      cde_max: emptyCde(),
      cde_fitness: { target_velocity_class: '', fit: null, factor: null, rationale: '' },
      coe: { metrics: [], aggregation_method: 'weighted_mean', weights: {}, composite_coe: null },
      ecr: null,
    });
  } else if (s.clusters === 'all') {
    sharedControls.push({
      id: `csf-${s.id}`, name: nameOf(s), description: descOf(s), linkMore: LINK,
      ownerName: '', ownerOrgChart: '', kind: s.kind, scope: 'all', linkJira: '', cde_max: emptyCde(),
    });
    for (const c of CLUSTERS) cells[`${c.slice(1)}-${fnOf(s.id)}`].umbrella.push({ id: `csf-${s.id}-${c.slice(1)}`, sharedControlId: `csf-${s.id}`, maturity: 0 });
  }
}
const starter = {
  version: '1.0.0',
  tool: 'TLCTC Control Matrix Manager',
  exportDate: `${m.meta.mapping_date}T00:00:00.000Z`,
  orgName: 'NIST CSF 2.0 Core Starter',
  targetMaturity: 3,
  environments: [{ id: 'env-csf2', name: 'NIST CSF 2.0 Core', cells }],
  sharedControls,
};

const data = {
  schema: 'tlctc-csf2-data.v1',
  generated_from: SRC,
  meta: m.meta,
  functions: m.functions,
  categories: m.categories,
  subcategories: m.subcategories,
};

function write(rel, text) {
  const file = path.join(ROOT, rel);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const prev = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : null;
  if (prev !== text) fs.writeFileSync(file, text, 'utf8');
  return prev === text ? 'unchanged' : 'wrote';
}
const r1 = write(OUT_STARTER, JSON.stringify(starter, null, 2) + '\n');
const r2 = write(OUT_DATA, `// GENERATED by scripts/build-csf2.js from ${SRC} — do not edit.\nwindow.TLCTC_CSF2 = ${JSON.stringify(data, null, 1)};\n`);

const count = (k) => m.subcategories.filter((s) => (k === 'local' ? Array.isArray(s.clusters) : s.clusters === k)).length;
const locals = Object.values(cells).reduce((n, c) => n + c.local.length, 0);
console.log(`build-csf2: ${m.subcategories.length} subcategories — ${count('local')} cluster-specific (${locals} Local placements), `
  + `${count('all')} cluster-neutral (shared, Umbrella in 10 rows), ${count('none')} outside the threat axis`);
console.log(`  ${r1} ${OUT_STARTER}\n  ${r2} ${OUT_DATA}`);
