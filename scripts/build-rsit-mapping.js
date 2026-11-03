#!/usr/bin/env node
/*
 * build-rsit-mapping.js — Render mappings/rsit/tlctc-rsit.json (canonical) into the upstream
 * contribution for enisaeu/Reference-Security-Incident-Taxonomy-Task-Force working_copy/rsit2tlctc/:
 *
 *   upstream/machinetag.json  = pinned RSIT machinev1 with one `tlctc` field per value (the shape
 *                               rsit2attck uses for `attck`); keys per entry sorted; 2-space; LF.
 *   upstream/rsit_2_tlctc.md  = rendered by upstream/machinetag2tlctc.py (single md generator).
 *
 * Tag rule (owner decision 2026-11-03): a `machinetag` + `uuid` (from the TLCTC MISP taxonomy) only
 * for direct and chain entries, where the RSIT value proves the step happened; every other value
 * carries `candidates` (plain cluster ids) and a `note` with the deciding question.
 *
 * Usage: node scripts/build-rsit-mapping.js   Deps: Node builtins + python (3.10+) on PATH.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const DIR = path.join(ROOT, 'mappings/rsit');
const PATHS = {
  mapping: path.join(DIR, 'tlctc-rsit.json'),
  machinev1: path.join(DIR, 'pinned/machinev1'),
  misp: path.join(ROOT, 'integrations/misp/taxonomies/tlctc/machinetag.json'),
  dictionary: path.join(ROOT, 'json-schemas/layer-1/tlctc-framework.v2.6.json'),
  outJson: path.join(DIR, 'upstream/machinetag.json'),
  outMd: path.join(DIR, 'upstream/rsit_2_tlctc.md'),
  renderer: path.join(DIR, 'upstream/machinetag2tlctc.py'),
};
const TAGGED_TYPES = ['direct', 'chain'];
const readJSON = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const DICTIONARY = readJSON(PATHS.dictionary);
const ROW_NAMES = Object.fromEntries(DICTIONARY.cause_side_partition.rows.map((r) => [r.row_id, r.name]));

/** Expected TLCTC MISP value for a cluster id: "#7" -> "07-malware" (number + slug of the dictionary name). */
function mispValueName(clusterId) {
  const c = DICTIONARY.clusters[clusterId];
  if (!c) throw new Error(`unknown cluster ${clusterId}`);
  const slug = c.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  return `${clusterId.replace('#', '').padStart(2, '0')}-${slug}`;
}

/** The TLCTC MISP taxonomy entry (predicate `cluster`) for a cluster id. Throws naming the value if absent. */
function mispCluster(clusterId, misp) {
  const value = mispValueName(clusterId);
  const group = misp.values.find((g) => g.predicate === 'cluster');
  const e = group && group.entry.find((x) => x.value === value);
  if (!e) throw new Error(`TLCTC MISP taxonomy has no cluster value ${value} (for ${clusterId})`);
  return e;
}

const alt = (x) => {
  if (x.tlctc) return `${x.tlctc}${x.rule ? ` (${x.rule})` : ''}${x.condition ? ` if ${x.condition}` : ''}`;
  if (x.partition_row) return `no cluster, ${ROW_NAMES[x.partition_row] || x.partition_row}, if ${x.condition}`;
  return `no cluster (${x.out_of_scope}) if ${x.condition}`;
};
const dre = (e) => (e.dre ? ` + [DRE: ${e.dre}]` : e.dre_potential ? ` (potential DRE ${e.dre_potential})` : '');
const ask = (e) => (e.next_question ? ` Ask: ${e.next_question}` : '');

function noteFor(e) {
  const t = e.mapping_type;
  if (t === 'direct') return `${alt(e.targets[0])}${dre(e)}.${ask(e)}`;
  if (t === 'chain') {
    const own = `${e.targets[0].tlctc}${dre(e)}`;
    const path = e.companion.after ? `${own} → ${e.companion.notation.split('→').slice(1).join('→').trim()}`
      : `${e.companion.notation.split('→').slice(0, -1).join('→').trim()} → ${own}`;
    const rule = e.targets[0].rule ? ` (${e.targets[0].rule})` : '';
    return `${path}${rule}; RSIT does not record the ${e.companion.after ? 'following' : 'preceding'} step.${ask(e)}`;
  }
  if (t === 'conditional') return `One of: ${e.targets.map(alt).join('; ')}${dre(e)}.${ask(e)}`;
  if (t === 'attempt') return `Attempt, success not asserted: ${e.targets.map(alt).join('; ')}. A blocked attempt is a near miss, not a successful step.${ask(e)}`;
  if (t === 'exposure') return `Exposure: a state with no step and no SRE; enables ${e.exposes.map(alt).join('; ')}${e.dre_potential ? ` (potential DRE ${e.dre_potential})` : ''}.`;
  if (t === 'indicator') return `Indicator: attacker infrastructure, not a victim event; serves ${e.implies.map(alt).join('; ')}.${ask(e)}`;
  if (t === 'outcome') {
    const hints = (e.cause_hints || []).map(alt).join('; ');
    return `Data state [DRE: ${e.dre}], not a cause${hints ? `; possible causes: ${hints}` : ''}.${ask(e)}`;
  }
  if (t === 'no-cluster') {
    if (e.excluded) return `Excluded: ${e.excluded}.`;
    if (e.out_of_scope) return `No cluster: ${e.out_of_scope}.`;
    return `No cluster: ${ROW_NAMES[e.partition_row] || e.partition_row} (operational risk).${ask(e)}`;
  }
  if (t === 'unresolved') return `Unresolved (?): no cluster can be defended from the value.${ask(e)}`;
  throw new Error(`${e.rsit_id}: no note for mapping_type ${t}`);
}

function candidatesFor(e) {
  const xs = [...(e.targets || []), ...(e.exposes || []), ...(e.implies || []), ...(e.cause_hints || [])];
  return [...new Set(xs.filter((x) => x.tlctc).map((x) => x.tlctc))];
}

function timestampOf(mapping) {
  return Number(String(mapping.metadata.updated).replace(/-/g, ''));
}

/** The single `tlctc` list element for a mapping entry. Throws if a needed MISP value is missing. */
function tlctcElement(entry, misp, timestamp = 20261103) {
  if (TAGGED_TYPES.includes(entry.mapping_type)) {
    const m = mispCluster(entry.targets[0].tlctc, misp);
    return { machinetag: `tlctc:cluster="${m.value}"`, uuid: m.uuid, mapping_type: entry.mapping_type, note: noteFor(entry), timestamp };
  }
  // Untagged: still prove every candidate cluster exists in the MISP taxonomy.
  const candidates = candidatesFor(entry);
  candidates.forEach((c) => mispCluster(c, misp));
  return { candidates, mapping_type: entry.mapping_type, note: noteFor(entry), timestamp };
}

/** Exact text of upstream/machinetag.json. */
function buildMachinetag(mapping, machinev1, misp) {
  const byId = new Map(mapping.entries.map((e) => [e.rsit_id, e]));
  const ts = timestampOf(mapping);
  const out = JSON.parse(JSON.stringify(machinev1));
  for (const g of out.values) {
    g.entry = g.entry.map((e) => {
      const id = `${g.predicate}/${e.value}`;
      const m = byId.get(id);
      if (!m) throw new Error(`${id}: no entry in tlctc-rsit.json`);
      const withTag = { ...e, tlctc: [tlctcElement(m, misp, ts)] };
      return Object.fromEntries(Object.keys(withTag).sort().map((k) => [k, withTag[k]]));
    });
  }
  return JSON.stringify(out, null, 2) + '\n';
}

/** Run the upstream renderer; returns the md text it writes to `outPath`. */
function renderMd(jsonPath, outPath) {
  for (const py of ['python', 'python3']) {
    const r = spawnSync(py, [PATHS.renderer, jsonPath, outPath], { encoding: 'utf8' });
    if (r.error && r.error.code === 'ENOENT') continue;
    if (r.status !== 0) throw new Error(`machinetag2tlctc.py failed: ${r.stderr}`);
    return fs.readFileSync(outPath, 'utf8');
  }
  throw new Error('python not found on PATH');
}

function main() {
  const text = buildMachinetag(readJSON(PATHS.mapping), readJSON(PATHS.machinev1), readJSON(PATHS.misp));
  fs.mkdirSync(path.dirname(PATHS.outJson), { recursive: true });
  fs.writeFileSync(PATHS.outJson, text);
  renderMd(PATHS.outJson, PATHS.outMd);
  const tagged = (text.match(/"machinetag":/g) || []).length;
  console.log(`build-rsit: wrote upstream/machinetag.json (${tagged} tagged values) and upstream/rsit_2_tlctc.md`);
}

module.exports = { buildMachinetag, tlctcElement, renderMd, PATHS, TAGGED_TYPES };
if (require.main === module) main();
