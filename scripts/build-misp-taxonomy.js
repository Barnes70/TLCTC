#!/usr/bin/env node
/*
 * build-misp-taxonomy.js — Generate the `tlctc` MISP taxonomy (machinetag.json)
 * from the canonical TLCTC v2.5 framework dictionary.
 *
 * Usage:  node scripts/build-misp-taxonomy.js            (write the file)
 *         node scripts/build-misp-taxonomy.js --check    (exit 1 if the committed file differs)
 * Output: integrations/misp/taxonomies/tlctc/machinetag.json
 *
 * Format matches `jq .` (2-space indent, insertion key order, raw UTF-8, trailing
 * newline) so MISP's jq_all_the_things.sh produces no diff. UUIDs are version 5
 * over uuid.NAMESPACE_DNS with the names MISP's gen_uuid.py uses
 * (`tlctc`, `tlctc:<predicate>`, `tlctc:<predicate>="<value>"`), so upstream
 * regeneration is idempotent.
 *
 * Deps: Node builtins only (fs, path, crypto). require()-able: see module.exports.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const DICT = path.join(ROOT, 'json-schemas/layer-1/tlctc-framework.v2.5.json');
const OUT = path.join(ROOT, 'integrations/misp/taxonomies/tlctc/machinetag.json');

const NAMESPACE_DNS = '6ba7b810-9dad-11d1-80b4-00c04fd430c8';
const TAXONOMY_VERSION = 1;

// Fixed value slugs. Derived from the canonical names and cross-checked in
// buildTaxonomy(); a mismatch means a cluster was renamed, which is a breaking
// change for every MISP instance carrying these tags — fail loudly.
const CLUSTER_VALUES = {
  '#1': '01-abuse-of-functions',
  '#2': '02-exploiting-server',
  '#3': '03-exploiting-client',
  '#4': '04-identity-theft',
  '#5': '05-man-in-the-middle',
  '#6': '06-flooding-attack',
  '#7': '07-malware',
  '#8': '08-physical-attack',
  '#9': '09-social-engineering',
  '#10': '10-supply-chain-attack',
};

// Existing tool palette (tools/attack-path-architect.html); bridge clusters share amber.
const CLUSTER_COLOURS = {
  '#1': '#3b82f6', '#2': '#ef4444', '#3': '#f97316', '#4': '#8b5cf6', '#5': '#06b6d4',
  '#6': '#eab308', '#7': '#ec4899', '#8': '#f59e0b', '#9': '#f59e0b', '#10': '#f59e0b',
};

function uuid5(namespaceUuid, name) {
  const ns = Buffer.from(namespaceUuid.replace(/-/g, ''), 'hex');
  const h = crypto.createHash('sha1').update(Buffer.concat([ns, Buffer.from(name, 'utf8')])).digest();
  h[6] = (h[6] & 0x0f) | 0x50; // version 5
  h[8] = (h[8] & 0x3f) | 0x80; // RFC 4122 variant
  const x = h.subarray(0, 16).toString('hex');
  return `${x.slice(0, 8)}-${x.slice(8, 12)}-${x.slice(12, 16)}-${x.slice(16, 20)}-${x.slice(20, 32)}`;
}

function slug(s) {
  return String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

// Verbatim dictionary strings — never paraphrased (spec §4, §9).
function entryDescription(cluster) {
  return `${cluster.definition} Generic vulnerability: ${cluster.generic_vulnerability}`;
}

const DESCRIPTION =
  'TLCTC (Top Level Cyber Threat Clusters) is a cause-oriented cyber threat taxonomy: exactly ten ' +
  'non-overlapping clusters, each defined by the generic vulnerability an attacker exploits rather than ' +
  'by the outcome of the attack. Tags follow TLCTC v2.5. Use cluster= for every cluster whose generic ' +
  'vulnerability was exploited at some step of the attack path (one tag per distinct cluster observed) ' +
  'and entry-cluster= for the cluster of the first step.';

const PREDICATES = [
  {
    value: 'cluster',
    expanded: 'Threat cluster (cause)',
    description:
      'Every TLCTC cluster whose generic vulnerability was exploited at some step of the attack path. ' +
      'Axiom VI (one step, one cluster) applies per step, not per event, so an event carries one tag ' +
      'per distinct cluster observed. Not exclusive.',
  },
  {
    value: 'entry-cluster',
    expanded: 'Entry cluster (first step)',
    description:
      'The cluster of the first step of the attack path, i.e. the initial cause. Exactly one per event.',
    exclusive: true,
  },
];

function orderedClusterIds(dict) {
  const ids = Object.keys(dict.clusters || {});
  if (ids.length !== 10) throw new Error(`dictionary has ${ids.length} clusters, expected exactly 10`);
  return ids.sort((a, b) => Number(a.slice(1)) - Number(b.slice(1)));
}

function buildTaxonomy(dict) {
  const ids = orderedClusterIds(dict);
  const entries = (predicate) =>
    ids.map((id) => {
      const c = dict.clusters[id];
      const n = Number(id.slice(1));
      if (c.strategic_id !== id) throw new Error(`cluster ${id}: strategic_id is ${c.strategic_id}`);
      const value = CLUSTER_VALUES[id];
      const derived = `${String(n).padStart(2, '0')}-${slug(c.name)}`;
      if (value !== derived) throw new Error(`cluster ${id}: value ${value} does not match name "${c.name}" (${derived})`);
      if (!c.definition || !c.generic_vulnerability) throw new Error(`cluster ${id}: missing definition or generic_vulnerability`);
      return {
        value,
        expanded: `${id} ${c.name}`,
        numerical_value: n,
        colour: CLUSTER_COLOURS[id],
        description: entryDescription(c),
        uuid: uuid5(NAMESPACE_DNS, `tlctc:${predicate}="${value}"`),
      };
    });

  return {
    namespace: 'tlctc',
    expanded: 'TLCTC - Top Level Cyber Threat Clusters',
    description: DESCRIPTION,
    version: TAXONOMY_VERSION,
    refs: [
      'https://www.tlctc.net',
      'https://github.com/Barnes70/TLCTC',
      'https://doi.org/10.5281/zenodo.20633176',
    ],
    uuid: uuid5(NAMESPACE_DNS, 'tlctc'),
    predicates: PREDICATES.map((p) => ({ ...p, uuid: uuid5(NAMESPACE_DNS, `tlctc:${p.value}`) })),
    values: PREDICATES.map((p) => ({ predicate: p.value, entry: entries(p.value) })),
  };
}

function serialize(taxonomy) {
  return JSON.stringify(taxonomy, null, 2) + '\n';
}

function main() {
  const dict = JSON.parse(fs.readFileSync(DICT, 'utf8'));
  const text = serialize(buildTaxonomy(dict));
  if (process.argv.includes('--check')) {
    const current = fs.existsSync(OUT) ? fs.readFileSync(OUT, 'utf8') : null;
    if (current !== text) {
      console.error(`OUT OF DATE: ${path.relative(ROOT, OUT)} differs from the generator output. Run: node scripts/build-misp-taxonomy.js`);
      process.exit(1);
    }
    console.log(`UP TO DATE: ${path.relative(ROOT, OUT)}`);
    return;
  }
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, text, 'utf8');
  console.log(`Wrote ${path.relative(ROOT, OUT)} (${Buffer.byteLength(text)} bytes, 2 predicates x 10 entries)`);
}

module.exports = { buildTaxonomy, serialize, uuid5, entryDescription, CLUSTER_VALUES, CLUSTER_COLOURS, NAMESPACE_DNS, DICT, OUT };

if (require.main === module) main();
