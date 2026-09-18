#!/usr/bin/env node
/*
 * validate-atlas-mapping.js — Validate mappings/mitre-atlas/tlctc-atlas.json. Part of `npm run validate`.
 *
 *  1. Every technique of the pinned ATLAS v2026.09 release (dist/v6 YAML) and every active attack-pattern of
 *     the pinned STIX distribution has exactly one mapping; no mapping names an unknown technique; atlasStatus
 *     (current | retired) agrees with the v2026.09 release.
 *  2. techniqueName equals the ATLAS name; tactics resolve to ATLAS tactic ids.
 *  3. tlctcMapping is 'N/A' or parses under the mapping notation grammar (#N, #N.M, →, |, parentheses),
 *     every cluster id is one of the ten, and tlctcMappingName is consistent with it.
 *  4. Every rationale is at least 40 characters; metadata.tlctc_version equals the dictionary's;
 *     metadata.total_techniques equals the mapping count.
 *
 * Exit: 0 = valid, 1 = at least one failure (all printed). Deps: Node builtins only.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const MAPPING = path.join(ROOT, 'mappings/mitre-atlas/tlctc-atlas.json');
const PINNED = path.join(ROOT, 'mappings/mitre-atlas/pinned/stix-atlas.json');
const DICTIONARY = path.join(ROOT, 'json-schemas/layer-1/tlctc-framework.v2.5.json');

const failures = [];
const fail = (m) => failures.push(m);
const readJSON = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));

const mapping = readJSON(MAPPING);
const atlas = readJSON(PINNED);
const dictionary = readJSON(DICTIONARY);
const clusterNames = Object.fromEntries(Object.entries(dictionary.clusters).map(([id, c]) => [id, c.name]));

// grammar: alt := seq ('|' seq)* ; seq := atom ('→' atom)* ; atom := cluster | '(' alt ')'
function parseMapping(s) {
  const toks = s.match(/#(?:10|[1-9])(?:\.\d)?|→|->|\||\(|\)|\S/g) || [];
  let pos = 0;
  const peek = () => toks[pos];
  const alt = () => { seq(); while (peek() === '|') { pos++; seq(); } };
  const seq = () => { atom(); while (peek() === '→' || peek() === '->') { pos++; atom(); } };
  const atom = () => {
    const t = peek();
    if (t === '(') { pos++; alt(); if (peek() !== ')') throw new Error('missing )'); pos++; return; }
    if (t && /^#(10|[1-9])(\.\d)?$/.test(t)) { pos++; return; }
    throw new Error(`unexpected ${t}`);
  };
  alt();
  if (pos !== toks.length) throw new Error('trailing tokens');
}

const active = atlas.objects.filter((o) => o.type === 'attack-pattern' && !o.revoked && !o.x_mitre_deprecated);
const byId = new Map(active.map((o) => [o.external_references[0].external_id, { name: o.name, source: 'stix' }]));
const tacticIds = new Set(atlas.objects.filter((o) => o.type === 'x-mitre-tactic').map((o) => o.external_references[0].external_id));
// ATLAS v2026.09 (format 6) YAML: a minimal line reader for `id:` / `name:` pairs (no YAML dependency).
const V6 = path.join(ROOT, 'mappings/mitre-atlas/pinned/ATLAS-2026.09.yaml');
const v6Names = new Map();
if (fs.existsSync(V6)) {
  const lines = fs.readFileSync(V6, 'utf8').split(/\r?\n/);
  // In the format-6 YAML an entry's `name:` line precedes its `id:` line.
  let lastName = null;
  for (const line of lines) {
    const nm = line.match(/^\s*-?\s*(?:&\S+\s+)?name:\s*(.+?)\s*$/);
    if (nm) { lastName = nm[1].replace(/^['"]|['"]$/g, ''); continue; }
    const idm = line.match(/^\s*-?\s*(?:&\S+\s+)?id:\s*(AML\.T[A\d.]+)\s*$/);
    if (idm) { if (!v6Names.has(idm[1]) && lastName) v6Names.set(idm[1], lastName); lastName = null; }
  }
  for (const [id, name] of v6Names) {
    if (id.startsWith('AML.TA')) tacticIds.add(id);
    else if (!byId.has(id)) byId.set(id, { name, source: 'v6' });
  }
} else fail('pinned/ATLAS-2026.09.yaml missing');
const v6TechniqueCount = [...v6Names.keys()].filter((k) => !k.startsWith('AML.TA')).length;
if (v6TechniqueCount < 200) fail(`ATLAS v2026.09 YAML parse found only ${v6TechniqueCount} techniques`);

const seen = new Set();
for (const m of mapping.mappings) {
  if (seen.has(m.techniqueId)) fail(`duplicate ${m.techniqueId}`);
  seen.add(m.techniqueId);
  const o = byId.get(m.techniqueId);
  if (!o) { fail(`${m.techniqueId} is not an active ATLAS technique`); continue; }
  const v6name = v6Names.get(m.techniqueId);
  if (m.techniqueName !== o.name && m.techniqueName !== v6name) fail(`${m.techniqueId}: name drifted (${m.techniqueName} vs ${o.name}${v6name ? ' / ' + v6name : ''})`);
  if (!['current', 'retired'].includes(m.atlasStatus)) fail(`${m.techniqueId}: atlasStatus must be current or retired`);
  if (m.atlasStatus === 'current' && !v6name) fail(`${m.techniqueId}: marked current but absent from ATLAS v2026.09`);
  if (m.atlasStatus === 'retired' && v6name) fail(`${m.techniqueId}: marked retired but present in ATLAS v2026.09`);
  for (const t of m.tactics || []) if (!tacticIds.has(t)) fail(`${m.techniqueId}: tactic ${t} unknown`);
  if (typeof m.mappingRationale !== 'string' || m.mappingRationale.length < 40) fail(`${m.techniqueId}: rationale missing or too short`);
  if (m.tlctcMapping === 'N/A') {
    if (m.tlctcMappingName !== 'N/A') fail(`${m.techniqueId}: N/A mapping with a mapping name`);
    continue;
  }
  try { parseMapping(m.tlctcMapping); } catch (e) { fail(`${m.techniqueId}: bad notation '${m.tlctcMapping}': ${e.message}`); continue; }
  for (const id of m.tlctcMapping.match(/#(?:10|[1-9])/g) || []) if (!clusterNames[id]) fail(`${m.techniqueId}: cluster ${id} not in dictionary`);
  const expectedName = m.tlctcMapping.replace(/#(10|[1-9])(\.\d)?/g, (all, n) => `${clusterNames['#' + n]} (${all})`);
  if (m.tlctcMappingName !== expectedName) fail(`${m.techniqueId}: tlctcMappingName inconsistent`);
}
for (const id of byId.keys()) if (!seen.has(id)) fail(`no mapping for ${id}`);
if (mapping.metadata.tlctc_version !== dictionary.metadata.tlctc_version) fail('metadata.tlctc_version drifted from the dictionary');
if (mapping.metadata.total_techniques !== mapping.mappings.length) fail('metadata.total_techniques != mappings.length');

if (failures.length) {
  console.error(`validate-atlas-mapping: ${failures.length} failure(s)`);
  for (const f of failures) console.error(`  - ${f}`);
  process.exit(1);
}
const na = mapping.mappings.filter((m) => m.tlctcMapping === 'N/A').length;
const retired = mapping.mappings.filter((m) => m.atlasStatus === 'retired').length;
console.log(`validate-atlas-mapping: OK (${mapping.mappings.length} techniques = ${v6TechniqueCount} in ATLAS v2026.09 + ${retired} retired ids kept for the STIX distribution; ${na} N/A)`);
