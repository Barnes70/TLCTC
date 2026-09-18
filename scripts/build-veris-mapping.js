#!/usr/bin/env node
/*
 * build-veris-mapping.js — Render mappings/veris/tlctc-veris.json (canonical) into the
 * upstream CSV mappings/veris/veris-<veris>_tlctc-<tlctc>.csv, in the column shape of the
 * VERIS → ATT&CK file that vz-risk/veris keeps in its mappings/ directory (MITRE CTID
 * Mappings Explorer layout), with the three ATT&CK object columns renamed for TLCTC.
 *
 * One row per (entry, target): direct/conditional/chain entries emit one row per cluster
 * target; outcome entries with a DRE code emit one row for the code; everything else
 * (context, no-cluster, outcome without DRE, unresolved) emits one row with
 * tlctc_object_id = none so the CSV still covers every VERIS value.
 *
 * Deterministic: bytes depend only on the two JSON inputs. LF line endings, no BOM.
 * Usage: node scripts/build-veris-mapping.js   (writes the CSV, prints the row count)
 * Deps: Node builtins only.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DIR = path.join(ROOT, 'mappings/veris');
const MAPPING = path.join(DIR, 'tlctc-veris.json');
const DICTIONARY = path.join(ROOT, 'json-schemas/layer-1/tlctc-framework.v2.5.json');

const HEADER = [
  '', 'mapping_framework', 'mapping_framework_version', 'capability_group', 'capability_id',
  'capability_description', 'mapping_type', 'tlctc_object_id', 'tlctc_object_name', 'tlctc_version',
  'technology_domain', 'score_category', 'score_value', 'related_score', 'references', 'comments',
  'organization', 'creation_date', 'last_update',
];
const REFERENCES = JSON.stringify([
  'https://www.tlctc.net',
  'https://github.com/Barnes70/TLCTC/tree/main/mappings/veris',
  'https://doi.org/10.5281/zenodo.20633176',
]);
const ORGANIZATION = 'TLCTC Project';

function csvField(v) {
  const s = v == null ? '' : String(v);
  return /[",\r\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

function capabilityGroup(verisId) {
  const parts = verisId.split('.');
  return parts.length >= 2 ? `${parts[0]}.${parts[1]}` : parts[0];
}

function clusterName(dictionary, id) {
  const c = dictionary.clusters[id]; // clusters is keyed by strategic id ('#1' … '#10')
  if (!c || c.strategic_id !== id) throw new Error(`cluster ${id} not in dictionary`);
  return c.name;
}

function dreName(dictionary, code) {
  const d = dictionary.data_risk_events.codes.find((x) => x.code === code);
  if (!d) throw new Error(`DRE code ${code} not in dictionary`);
  return d.name;
}

function rowsFor(entry, dictionary) {
  const t = entry.mapping_type;
  if (t === 'direct' || t === 'conditional' || t === 'chain') {
    return entry.targets.map((target) => {
      const bits = [];
      if (target.rule) bits.push(target.rule);
      if (target.condition) bits.push(`condition: ${target.condition}`);
      if (target.role_hint) bits.push(`role: ${target.role_hint}`);
      if (target.sub_cluster_hint) bits.push(`sub-cluster hint: ${target.sub_cluster_hint}`);
      if (t === 'chain' && entry.companion) {
        if (entry.companion.before) bits.push(`companion before: ${entry.companion.before}`);
        if (entry.companion.after) bits.push(`companion after: ${entry.companion.after}`);
        if (entry.companion.notation) bits.push(`notation: ${entry.companion.notation}`);
      }
      bits.push(entry.rationale);
      return { id: target.tlctc, name: clusterName(dictionary, target.tlctc), comments: bits.join('; ') };
    });
  }
  if (t === 'outcome' && entry.dre) {
    const bits = [`DRE ${entry.dre}`];
    if (entry.certainty) bits.push(`certainty: ${entry.certainty}`);
    bits.push(entry.rationale);
    return [{ id: entry.dre, name: `DRE: ${dreName(dictionary, entry.dre)}`, comments: bits.join('; ') }];
  }
  if (t === 'outcome') return [{ id: 'none', name: 'outcome (Axiom III)', comments: entry.rationale }];
  if (t === 'context') {
    const c = entry.context || {};
    const label = c.boundary_context ? `context: ${c.boundary_context}` : c.boundary ? `context: ${c.boundary}` : c.intra_system_boundary ? `context: |[${c.intra_system_boundary}]|` : c.role_hint ? `context: role ${c.role_hint}` : `context: ${c.note || 'annotation'}`;
    const bits = Object.entries(c).map(([k, v]) => `${k}: ${v}`);
    bits.push(entry.rationale);
    return [{ id: 'none', name: label, comments: bits.join('; ') }];
  }
  if (t === 'no-cluster') {
    const label = entry.out_of_scope ? `out of scope: ${entry.out_of_scope}` : `operational risk: ${entry.partition_row}`;
    const bits = [`partition row: ${entry.partition_row}`];
    if (entry.basis) bits.push(entry.basis);
    bits.push(entry.rationale);
    return [{ id: 'none', name: label, comments: bits.join('; ') }];
  }
  if (t === 'unresolved') return [{ id: 'none', name: 'unresolved (R-UNRES-2)', comments: entry.rationale }];
  throw new Error(`unknown mapping_type ${t} on ${entry.veris_id}`);
}

function buildCsv(mapping, dictionary) {
  const m = mapping.metadata;
  const lines = [HEADER.join(',')];
  let i = 0;
  for (const entry of mapping.entries) {
    for (const r of rowsFor(entry, dictionary)) {
      lines.push([
        i++, 'veris', m.veris_version, capabilityGroup(entry.veris_id), entry.veris_id,
        entry.veris_description, entry.mapping_type, r.id, r.name, m.tlctc_version,
        'all', '', '', '', REFERENCES, r.comments, ORGANIZATION, m.created, m.updated,
      ].map(csvField).join(','));
    }
  }
  return lines.join('\n') + '\n';
}

function outputPath(mapping) {
  const m = mapping.metadata;
  return path.join(DIR, `veris-${m.veris_version}_tlctc-${m.tlctc_version}.csv`);
}

module.exports = { buildCsv, outputPath, HEADER, MAPPING, DICTIONARY };

if (require.main === module) {
  const mapping = JSON.parse(fs.readFileSync(MAPPING, 'utf8'));
  const dictionary = JSON.parse(fs.readFileSync(DICTIONARY, 'utf8'));
  const csv = buildCsv(mapping, dictionary);
  const out = outputPath(mapping);
  fs.writeFileSync(out, csv, 'utf8');
  console.log(`build-veris: wrote ${path.relative(ROOT, out)} (${csv.split('\n').length - 2} rows, ${mapping.entries.length} entries)`);
}
