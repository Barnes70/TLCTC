#!/usr/bin/env node
/*
 * build-attack-flow-stix.js — Generate integrations/attack-flow/stix/tlctc-stix-bundle.json:
 * the TLCTC framework as a STIX 2.1 bundle in the shape the Attack Flow Builder consumes for
 * MITRE ATLAS and the Fight Fraud Framework (sources/download_stix_source.mjs):
 *
 *   x-mitre-tactic     one per cluster (#1..#10), x_mitre_shortname tlctc-01..tlctc-10
 *   attack-pattern     one root per cluster (TLCTC-0N.00, "vector unspecified") plus every
 *                      sub-cluster of the operational enumeration, kill_chain_phases -> its cluster
 *   identity           TLCTC Project (fixed id); marking-definition TLP:CLEAR (the standard object)
 *
 * Names, definitions and generic vulnerabilities are copied verbatim from the v2.5 dictionary and
 * the operational enumeration. Every generated id is uuid v5 over NAMESPACE_URL and a
 * https://www.tlctc.net/stix/... name, so the file regenerates byte-identical.
 *
 * Usage: node scripts/build-attack-flow-stix.js       Deps: Node builtins only.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const DICTIONARY = path.join(ROOT, 'json-schemas/layer-1/tlctc-framework.v2.5.json');
const ENUMERATION = path.join(ROOT, 'json-schemas/operational/tlctc-operational-enumeration.json');
const OUT = path.join(ROOT, 'integrations/attack-flow/stix/tlctc-stix-bundle.json');

const IDENTITY_ID = 'identity--025fe838-800e-4b4f-a9c3-2fab5d1366f5';
const TLP_CLEAR_ID = 'marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487'; // STIX 2.1 TLP:WHITE/CLEAR
const SOURCE_NAME = 'tlctc';
const KILL_CHAIN = 'tlctc';
const SITE = 'https://www.tlctc.net';
const NAMESPACE_URL = '6ba7b811-9dad-11d1-80b4-00c04fd430c8';

function uuid5(namespace, name) {
  const ns = Buffer.from(namespace.replace(/-/g, ''), 'hex');
  const hash = crypto.createHash('sha1').update(Buffer.concat([ns, Buffer.from(name, 'utf8')])).digest();
  hash[6] = (hash[6] & 0x0f) | 0x50;
  hash[8] = (hash[8] & 0x3f) | 0x80;
  const h = hash.subarray(0, 16).toString('hex');
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20, 32)}`;
}
const stixId = (type, name) => `${type}--${uuid5(NAMESPACE_URL, `${SITE}/stix/${name}`)}`;
const pad = (n) => String(n).padStart(2, '0');
const clusterNumber = (id) => parseInt(id.replace('#', ''), 10);

function build(dictionary, enumeration) {
  const created = `${dictionary.metadata.release_date}T00:00:00.000Z`;
  const version = dictionary.metadata.tlctc_version;
  const base = (type, name) => ({
    type, spec_version: '2.1', id: stixId(type, name), created_by_ref: IDENTITY_ID,
    created, modified: created, object_marking_refs: [TLP_CLEAR_ID],
  });
  const objects = [];
  objects.push({
    type: 'identity', spec_version: '2.1', id: IDENTITY_ID, created, modified: created,
    name: 'TLCTC Project', identity_class: 'organization',
    description: `Publisher of the Top Level Cyber Threat Clusters (TLCTC) framework, v${version}. ${SITE}`,
    contact_information: SITE,
  });
  objects.push({
    type: 'marking-definition', spec_version: '2.1', id: TLP_CLEAR_ID, created: '2017-01-20T00:00:00.000Z',
    definition_type: 'tlp', name: 'TLP:CLEAR', definition: { tlp: 'clear' },
  });
  const clusters = Object.keys(dictionary.clusters).sort((a, b) => clusterNumber(a) - clusterNumber(b));
  if (clusters.length !== 10) throw new Error(`expected 10 clusters, got ${clusters.length}`);
  const tactics = [];
  for (const cid of clusters) {
    const c = dictionary.clusters[cid];
    const n = clusterNumber(cid);
    const shortname = `tlctc-${pad(n)}`;
    tactics.push({
      ...base('x-mitre-tactic', `tactic/${cid}`),
      name: c.name,
      description: c.definition,
      x_mitre_shortname: shortname,
      x_mitre_domains: ['tlctc'],
      x_mitre_version: version,
      x_mitre_deprecated: false,
      external_references: [{ source_name: SOURCE_NAME, external_id: cid, url: `${SITE}/tlctc-10-definitions.html#cluster${n}` }],
    });
  }
  const techniques = [];
  for (const cid of clusters) {
    const c = dictionary.clusters[cid];
    const n = clusterNumber(cid);
    const oid = `TLCTC-${pad(n)}.00`;
    techniques.push({
      ...base('attack-pattern', `technique/${oid}`),
      name: `${c.name} (vector unspecified)`,
      description: `Generic vulnerability: ${c.generic_vulnerability} Attacker's view: ${c.attackers_view}`,
      kill_chain_phases: [{ kill_chain_name: KILL_CHAIN, phase_name: `tlctc-${pad(n)}` }],
      x_mitre_domains: ['tlctc'],
      x_mitre_version: version,
      x_mitre_is_subtechnique: false,
      x_mitre_deprecated: false,
      external_references: [{ source_name: SOURCE_NAME, external_id: oid, url: `${SITE}/tlctc-10-definitions.html#cluster${n}` }],
    });
    for (const s of enumeration.sub_clusters.filter((x) => x.parent_cluster === cid).sort((a, b) => a.id.localeCompare(b.id))) {
      techniques.push({
        ...base('attack-pattern', `technique/${s.id}`),
        name: s.name,
        description: s.examples ? `${s.definition} Examples: ${s.examples}` : s.definition,
        kill_chain_phases: [{ kill_chain_name: KILL_CHAIN, phase_name: `tlctc-${pad(n)}` }],
        x_mitre_domains: ['tlctc'],
        x_mitre_version: enumeration.metadata.schema_version,
        x_mitre_is_subtechnique: false,
        x_mitre_deprecated: false,
        external_references: [{ source_name: SOURCE_NAME, external_id: s.id, url: `${SITE}/tlctc-10-definitions.html#cluster${n}` }],
      });
    }
  }
  objects.push(...tactics, ...techniques);
  return {
    type: 'bundle',
    id: stixId('bundle', `bundle/tlctc-${version}`),
    objects,
  };
}

module.exports = { build, uuid5, stixId, IDENTITY_ID, TLP_CLEAR_ID, OUT, DICTIONARY, ENUMERATION };

if (require.main === module) {
  const dictionary = JSON.parse(fs.readFileSync(DICTIONARY, 'utf8'));
  const enumeration = JSON.parse(fs.readFileSync(ENUMERATION, 'utf8'));
  const bundle = build(dictionary, enumeration);
  fs.writeFileSync(OUT, JSON.stringify(bundle, null, 2) + '\n', 'utf8');
  const tactics = bundle.objects.filter((o) => o.type === 'x-mitre-tactic').length;
  const techniques = bundle.objects.filter((o) => o.type === 'attack-pattern').length;
  console.log(`build-attack-flow: wrote ${path.relative(ROOT, OUT)} (${tactics} tactics, ${techniques} techniques, ${bundle.objects.length} objects)`);
}
