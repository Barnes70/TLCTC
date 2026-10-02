#!/usr/bin/env node
// Validate mappings/cis-controls-v8.1/cis-v8.1-tlctc-mapping.json and generate from it:
//   tools/control-matrix-starter-cis-v8.1.json      — Control Matrix starter (all 60 cells, system-risk layer)
//   mappings/cis-controls-v8.1/cis-v8.1-dre-matrix.json — data-risk layer matrix (DRE rows C·Ii·If·Av·Ac × 6 functions)
//
// Two layers: a Safeguard that acts on a cluster step up to the System Risk Event carries `clusters`
// (system-risk layer, the 10 × 6 control matrix); one that acts after it, at the Data Risk Event, carries
// `dre` instead (`clusters: null`) and lands in the separate DRE matrix (owner ruling 2026-10-01).
//
// Same placement rules as scripts/build-csf2.js: a cluster array becomes Local controls in those
// rows of the Safeguard's security-function column; "all" becomes one shared control linked into
// the Umbrella list of all ten rows; "none" (outside the threat axis) is placed in no cell.
// The source holds no CIS text (CC BY-NC-ND 4.0): ids and facts from the spreadsheet,
// topic/rationale in TLCTC wording. `--draft` accepts unmapped rows and writes nothing.
//
// Usage: node scripts/build-cis.js [--draft]
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = 'mappings/cis-controls-v8.1/cis-v8.1-tlctc-mapping.json';
const OUT_STARTER = 'tools/control-matrix-starter-cis-v8.1.json';
const OUT_DRE = 'mappings/cis-controls-v8.1/cis-v8.1-dre-matrix.json';
const OUT_DRE_STARTER = 'tools/dre-matrix-starter-cis-v8.1.json';
const SIDES = ['P', 'DR']; // Bow-Tie side, judged per Safeguard: P = stops the step, DR = finds/contains it afterwards
const FUNCS = ['GV', 'ID', 'PR', 'DE', 'RS', 'RC'];
const CLUSTERS = Array.from({ length: 10 }, (_, i) => `#${i + 1}`);
const KINDS = ['tech', 'org'];
const DRE = ['C', 'Ii', 'If', 'Av', 'Ac']; // DRE refinement-tree leaves (core §7.6)
const EXPECT = { controls: 18, safeguards: 153 }; // CIS Controls v8.1 / v8.1.2
const LINK = 'https://www.cisecurity.org/controls/v8-1';

function validate(m, { draft = false } = {}) {
  const errors = [];
  const list = m.safeguards || [];
  if (list.length !== EXPECT.safeguards) errors.push(`expected ${EXPECT.safeguards} safeguards, found ${list.length}`);
  const controls = new Set(list.map((s) => s.control));
  if (controls.size !== EXPECT.controls) errors.push(`expected ${EXPECT.controls} controls, found ${controls.size}`);
  const seen = new Set();
  for (const s of list) {
    const where = `${s.id}`;
    const mm = /^(\d{1,2})\.(\d{1,2})$/.exec(s.id || '');
    if (!mm) { errors.push(`${where}: bad id`); continue; }
    if (seen.has(s.id)) errors.push(`${where}: duplicate`);
    seen.add(s.id);
    if (+mm[1] !== s.control) errors.push(`${where}: control ${s.control} does not match id`);
    if (!FUNCS.includes(s.function)) errors.push(`${where}: function must be one of ${FUNCS.join(', ')}`);
    if (![1, 2, 3].includes(s.ig)) errors.push(`${where}: ig must be 1, 2 or 3`);
    if (!s.asset_class) errors.push(`${where}: asset_class required`);
    const unmapped = s.clusters === null && s.kind === null && s.hardening === null && !s.rationale && !s.topic;
    if (unmapped) { if (!draft) errors.push(`${where}: unmapped`); continue; }
    if (!s.topic || s.topic.length > 60) errors.push(`${where}: topic required, at most 60 characters (TLCTC wording, no CIS text)`);
    if (!KINDS.includes(s.kind)) errors.push(`${where}: kind must be ${KINDS.join(' or ')}`);
    if (typeof s.hardening !== 'boolean') errors.push(`${where}: hardening must be boolean`);
    if (!s.rationale) errors.push(`${where}: rationale required`);
    if (s.dre !== undefined && s.dre !== null) { // data-risk layer
      if (s.clusters !== null) errors.push(`${where}: either clusters or dre, not both (set clusters to null)`);
      if (Array.isArray(s.dre)) {
        if (!s.dre.length) errors.push(`${where}: empty dre array (use "all")`);
        const bad = s.dre.filter((c) => !DRE.includes(c));
        if (bad.length) errors.push(`${where}: unknown DRE codes ${bad.join(', ')} (rows are ${DRE.join(', ')})`);
        if (new Set(s.dre).size !== s.dre.length) errors.push(`${where}: duplicate DRE codes`);
      } else if (s.dre !== 'all') errors.push(`${where}: dre must be an array or "all"`);
      if (s.side !== undefined) errors.push(`${where}: side only on cluster-acting Safeguards`);
      continue;
    }
    if (Array.isArray(s.clusters)) {
      if (!s.clusters.length) errors.push(`${where}: empty clusters array (use "all" or "none")`);
      const bad = s.clusters.filter((c) => !CLUSTERS.includes(c));
      if (bad.length) errors.push(`${where}: unknown clusters ${bad.join(', ')}`);
      if (new Set(s.clusters).size !== s.clusters.length) errors.push(`${where}: duplicate clusters`);
      if (!SIDES.includes(s.side)) errors.push(`${where}: side must be P or DR`);
    } else {
      if (s.clusters !== 'all' && s.clusters !== 'none') errors.push(`${where}: clusters must be an array, "all" or "none"`);
      if (s.side !== undefined) errors.push(`${where}: side only on cluster-acting Safeguards`);
    }
    if (s.hardening === true && s.clusters === 'none') errors.push(`${where}: hardening Safeguard cannot be outside the threat axis ("none")`);
  }
  return errors;
}

const emptyCde = () => ({ value: null, rationale: '', set_by: '', last_reviewed: '', review_trigger: '' });
const nameOf = (s) => `CIS ${s.id} — ${s.topic}`;
const descOf = (s) => `CIS Control ${s.control}, IG${s.ig}, ${s.asset_class}${s.hardening ? ', hardening' : ''}${s.side ? `, ${s.side === 'P' ? 'prevention' : 'detection-response'}` : ''}. TLCTC: ${s.rationale}`;

function buildStarter(m) {
  const cells = {};
  for (const c of CLUSTERS) for (const f of FUNCS) cells[`${c.slice(1)}-${f}`] = { local: [], umbrella: [] };
  const sharedControls = [];
  for (const s of m.safeguards) {
    if (Array.isArray(s.clusters)) {
      for (const c of s.clusters) cells[`${c.slice(1)}-${s.function}`].local.push({
        id: `cis-${s.id}-${c.slice(1)}`, name: nameOf(s), description: descOf(s), linkMore: LINK,
        ownerName: '', ownerOrgChart: '', kind: s.kind, maturity: 0, linkJira: '', role: '',
        cde_max: emptyCde(),
        cde_fitness: { target_velocity_class: '', fit: null, factor: null, rationale: '' },
        coe: { metrics: [], aggregation_method: 'weighted_mean', weights: {}, composite_coe: null },
        ecr: null,
      });
    } else if (s.clusters === 'all') {
      sharedControls.push({ id: `cis-${s.id}`, name: nameOf(s), description: descOf(s), linkMore: LINK,
        ownerName: '', ownerOrgChart: '', kind: s.kind, scope: 'all', linkJira: '', cde_max: emptyCde() });
      for (const c of CLUSTERS) cells[`${c.slice(1)}-${s.function}`].umbrella.push({ id: `cis-${s.id}-${c.slice(1)}`, sharedControlId: `cis-${s.id}`, maturity: 0 });
    }
  }
  return {
    version: '1.0.0', tool: 'TLCTC Control Matrix Manager',
    exportDate: `${m.meta.mapping_date}T00:00:00.000Z`, orgName: 'CIS Controls v8.1.2 Starter', targetMaturity: 3,
    environments: [{ id: 'env-cis81', name: 'CIS Controls v8.1.2', cells }], sharedControls,
  };
}

function dreMatrix(m) {
  const cells = {};
  for (const r of DRE) for (const f of FUNCS) cells[`${r}-${f}`] = [];
  for (const s of m.safeguards) {
    if (s.dre === undefined || s.dre === null) continue;
    for (const r of s.dre === 'all' ? DRE : s.dre) cells[`${r}-${s.function}`].push(s.id);
  }
  return { rows: DRE, columns: FUNCS, cells };
}

// Starter for tools/dre-matrix.html: one control per (DRE row, Safeguard); "all" = an umbrella control in every row.
function buildDreStarter(m) {
  const cells = {};
  for (const r of DRE) for (const f of FUNCS) cells[`${r}-${f}`] = [];
  for (const s of m.safeguards) {
    if (s.dre === undefined || s.dre === null) continue;
    for (const r of s.dre === 'all' ? DRE : s.dre) cells[`${r}-${s.function}`].push({
      id: `cis-${s.id}-${r}`, name: nameOf(s), description: descOf(s), kind: s.kind, maturity: 0, owner: '',
      scope: s.dre === 'all' ? 'umbrella' : 'local', linkMore: LINK,
    });
  }
  return { version: '1.0.0', tool: 'TLCTC DRE Matrix', exportDate: `${m.meta.mapping_date}T00:00:00.000Z`,
    orgName: 'CIS Controls v8.1.2 — data-layer Safeguards', targetMaturity: 3, cells };
}

function stats(m) {
  const byCluster = Object.fromEntries(CLUSTERS.map((c) => [c, 0]));
  const hardeningByCluster = Object.fromEntries(CLUSTERS.map((c) => [c, 0]));
  const byDre = Object.fromEntries(DRE.map((c) => [c, 0]));
  const bySide = Object.fromEntries(CLUSTERS.map((c) => [c, { P: 0, DR: 0 }]));
  let neutral = 0, none = 0, hardening = 0, dataLayer = 0;
  for (const s of m.safeguards) {
    if (s.hardening === true) hardening++;
    if (s.dre !== undefined && s.dre !== null) { dataLayer++; for (const r of s.dre === 'all' ? DRE : s.dre) byDre[r]++; continue; }
    if (Array.isArray(s.clusters)) for (const c of s.clusters) { byCluster[c]++; if (s.hardening) hardeningByCluster[c]++; if (SIDES.includes(s.side)) bySide[c][s.side]++; }
    else if (s.clusters === 'all') neutral++;
    else if (s.clusters === 'none') none++;
  }
  return { byCluster, hardeningByCluster, bySide, neutral, none, hardening, dataLayer, byDre };
}

module.exports = { validate, buildStarter, buildDreStarter, dreMatrix, stats };

if (require.main === module) {
  const draft = process.argv.includes('--draft');
  const m = JSON.parse(fs.readFileSync(path.join(ROOT, SRC), 'utf8'));
  const errors = validate(m, { draft });
  if (errors.length) {
    console.error(`build-cis: ${SRC} failed validation:\n  ` + errors.join('\n  '));
    process.exit(1);
  }
  if (draft) {
    const open = m.safeguards.filter((s) => s.clusters === null).length;
    console.log(`build-cis: ${m.safeguards.length} safeguards valid (draft, ${open} unmapped; nothing written)`);
    process.exit(0);
  }
  const write = (rel, text) => {
    const file = path.join(ROOT, rel);
    const prev = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : null;
    if (prev !== text) fs.writeFileSync(file, text, 'utf8');
    return `${prev === text ? 'unchanged' : 'wrote'} ${rel}`;
  };
  const d = dreMatrix(m);
  const w1 = write(OUT_STARTER, JSON.stringify(buildStarter(m), null, 2) + '\n');
  const w3 = write(OUT_DRE_STARTER, JSON.stringify(buildDreStarter(m), null, 2) + '\n');
  const w2 = write(OUT_DRE, JSON.stringify({ schema: 'tlctc-cis-v8.1-dre-matrix.v1', generated_from: SRC, ...d }, null, 2) + '\n');
  const s = stats(m);
  console.log(`build-cis: ${m.safeguards.length} safeguards — system-risk layer ${m.safeguards.length - s.dataLayer} (${s.neutral} cluster-neutral, ${s.none} outside the threat axis), data-risk layer ${s.dataLayer}; ${s.hardening} hardening`);
  for (const c of CLUSTERS) console.log(`  ${c.padEnd(4)} Local ${String(s.byCluster[c]).padStart(3)}  P/DR ${s.bySide[c].P}/${s.bySide[c].DR}  (hardening ${s.hardeningByCluster[c]})`);
  const width = Object.fromEntries(FUNCS.map((f) => [f, Math.max(4, ...DRE.map((r) => d.cells[`${r}-${f}`].join(',').length)) + 2]));
  console.log('  DRE   ' + FUNCS.map((f) => f.padEnd(width[f])).join(''));
  for (const r of DRE) console.log('  ' + r.padEnd(5) + ' ' + FUNCS.map((f) => (d.cells[`${r}-${f}`].join(',') || '-').padEnd(width[f])).join(''));
  console.log(`  ${w1}\n  ${w2}\n  ${w3}`);
}
