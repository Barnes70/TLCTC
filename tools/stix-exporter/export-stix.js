#!/usr/bin/env node
// TLCTC Layer 3 attack-path → STIX 2.1 bundle exporter (one-way).
// Custom properties prefixed x_tlctc_*; ATT&CK enrichment is best-effort
// based on Txxxx patterns found in evidence_refs / notes.

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const TLCTC_SOURCE = 'tlctc';
const TLCTC_URL = 'https://www.tlctc.net';
const ATTACK_SOURCE = 'mitre-attack';
const ATTACK_URL_BASE = 'https://attack.mitre.org/techniques/';

const CLUSTER_NAMES = {
  '#1': 'Abuse of Functions',
  '#2': 'Exploiting Server',
  '#3': 'Exploiting Client',
  '#4': 'Identity Theft',
  '#5': 'Man in the Middle',
  '#6': 'Flooding Attack',
  '#7': 'Malware',
  '#8': 'Physical Attack',
  '#9': 'Social Engineering',
  '#10': 'Supply Chain Attack'
};

function newId(stixType) {
  return `${stixType}--${crypto.randomUUID()}`;
}

function nowIso() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
}

function strategicCluster(clusterId) {
  if (!clusterId) return null;
  if (clusterId.startsWith('#')) return clusterId;
  const m = clusterId.match(/^TLCTC-(\d{2})\.\d{2}$/);
  if (!m) return null;
  const n = parseInt(m[1], 10);
  return `#${n}`;
}

function clusterDisplayName(clusterId) {
  const strat = strategicCluster(clusterId);
  const baseName = CLUSTER_NAMES[strat];
  if (!baseName) return clusterId;
  if (clusterId === strat) return `TLCTC ${clusterId} ${baseName}`;
  return `TLCTC ${clusterId} (${strat} ${baseName})`;
}

function extractAttackTechniqueIds(step) {
  const text = [
    step.notes || '',
    ...(step.evidence_refs || [])
  ].join(' ');
  const matches = text.match(/\bT\d{4}(?:\.\d{3})?\b/g) || [];
  return [...new Set(matches)];
}

function buildExternalRefsForStep(step) {
  const refs = [{
    source_name: TLCTC_SOURCE,
    external_id: step.cluster,
    url: TLCTC_URL
  }];
  return refs;
}

function buildAttackStepSDO(step, opts) {
  const id = newId('attack-pattern');
  const sdo = {
    type: 'attack-pattern',
    spec_version: '2.1',
    id,
    created: opts.created,
    modified: opts.created,
    name: `${clusterDisplayName(step.cluster)} (${step.step_id})`,
    description: step.notes || '',
    external_references: buildExternalRefsForStep(step),
    x_tlctc_step_id: step.step_id,
    x_tlctc_cluster: step.cluster,
    x_tlctc_strategic_cluster: strategicCluster(step.cluster)
  };
  if (step.outcomes && step.outcomes.length) sdo.x_tlctc_dre = step.outcomes;
  if (step.fec_executed) sdo.x_tlctc_fec = true;
  if (step.fec_recorded_in_step_id) sdo.x_tlctc_fec_recorded_in_step_id = step.fec_recorded_in_step_id;
  if (step.topology_boundary) sdo.x_tlctc_boundary = step.topology_boundary;
  if (step.intra_system_boundaries && step.intra_system_boundaries.length) sdo.x_tlctc_intra_boundaries = step.intra_system_boundaries;
  if (step.evidence_refs && step.evidence_refs.length) sdo.x_tlctc_evidence_refs = step.evidence_refs;
  return sdo;
}

function buildUnresolvedSDO(step, opts) {
  const id = newId('attack-pattern');
  const operator = step.unresolved_type === 'single' ? '?' : '…';
  const sdo = {
    type: 'attack-pattern',
    spec_version: '2.1',
    id,
    created: opts.created,
    modified: opts.created,
    name: `TLCTC ${operator} unresolved (${step.step_id})`,
    description: step.notes,
    external_references: [{
      source_name: TLCTC_SOURCE,
      external_id: operator,
      url: TLCTC_URL
    }],
    x_tlctc_step_id: step.step_id,
    x_tlctc_status: 'unresolved',
    x_tlctc_unresolved_type: step.unresolved_type
  };
  if (step.estimated_count) sdo.x_tlctc_estimated_count = step.estimated_count;
  if (step.candidates && step.candidates.length) sdo.x_tlctc_candidates = step.candidates;
  if (step.topology_boundary) sdo.x_tlctc_boundary = step.topology_boundary;
  if (step.intra_system_boundaries && step.intra_system_boundaries.length) sdo.x_tlctc_intra_boundaries = step.intra_system_boundaries;
  if (step.evidence_refs && step.evidence_refs.length) sdo.x_tlctc_evidence_refs = step.evidence_refs;
  return sdo;
}

function buildAttackTechniqueSDOs(step, parentId, opts) {
  const techIds = extractAttackTechniqueIds(step);
  const objects = [];
  for (const tid of techIds) {
    const apId = newId('attack-pattern');
    objects.push({
      type: 'attack-pattern',
      spec_version: '2.1',
      id: apId,
      created: opts.created,
      modified: opts.created,
      name: `MITRE ATT&CK ${tid}`,
      external_references: [{
        source_name: ATTACK_SOURCE,
        external_id: tid,
        url: `${ATTACK_URL_BASE}${tid.replace('.', '/')}`
      }],
      x_tlctc_attck_technique: tid,
      x_tlctc_enrichment_basis: 'evidence_refs/notes regex'
    });
    objects.push({
      type: 'relationship',
      spec_version: '2.1',
      id: newId('relationship'),
      created: opts.created,
      modified: opts.created,
      relationship_type: 'derived-from',
      source_ref: apId,
      target_ref: parentId,
      description: 'ATT&CK technique enriched onto the TLCTC step it occurs within.'
    });
  }
  return objects;
}

function buildPrecedesRelationship(sourceId, targetId, deltaT, opts) {
  const rel = {
    type: 'relationship',
    spec_version: '2.1',
    id: newId('relationship'),
    created: opts.created,
    modified: opts.created,
    relationship_type: 'related-to',
    source_ref: sourceId,
    target_ref: targetId,
    description: 'TLCTC sequence edge (predecessor → successor).',
    x_tlctc_relation: 'precedes'
  };
  if (deltaT) rel.x_tlctc_delta_t = deltaT;
  return rel;
}

function buildParallelGrouping(group, memberIds, opts) {
  const id = newId('grouping');
  const sdo = {
    type: 'grouping',
    spec_version: '2.1',
    id,
    created: opts.created,
    modified: opts.created,
    name: `TLCTC parallel group${group.group_id ? ` (${group.group_id})` : ''}`,
    context: 'tlctc-parallel',
    object_refs: memberIds,
    x_tlctc_relation: 'parallel'
  };
  if (group.group_id) sdo.x_tlctc_group_id = group.group_id;
  if (group.notes) sdo.description = group.notes;
  return sdo;
}

function buildReport(meta, allObjectIds, opts) {
  const sdo = {
    type: 'report',
    spec_version: '2.1',
    id: newId('report'),
    created: opts.created,
    modified: opts.created,
    name: meta.incident_id,
    published: meta.created_at || opts.created,
    report_types: ['attack-pattern'],
    object_refs: allObjectIds,
    description: meta.notes || `TLCTC attack path ${meta.incident_id}`,
    external_references: [{
      source_name: TLCTC_SOURCE,
      url: TLCTC_URL,
      description: `TLCTC v${meta.tlctc_version} framework`
    }],
    x_tlctc_incident_id: meta.incident_id,
    x_tlctc_version: meta.tlctc_version,
    x_tlctc_analyst_confidence: meta.analyst_confidence
  };
  if (meta.framework_ref) sdo.x_tlctc_framework_ref = meta.framework_ref;
  if (meta.framework_sha256) sdo.x_tlctc_framework_sha256 = meta.framework_sha256;
  if (meta.registry_ref) sdo.x_tlctc_registry_ref = meta.registry_ref;
  if (meta.registry_sha256) sdo.x_tlctc_registry_sha256 = meta.registry_sha256;
  return sdo;
}

function exportPath(attackPath) {
  const opts = { created: nowIso() };
  const objects = [];
  // Per sequence_item: produce a "primary anchor" SDO id used for sequence
  // linkage. For attack_step / unresolved → the SDO itself. For parallel_group
  // → the grouping SDO.
  const anchors = []; // [{ id, deltaT }]
  for (const item of attackPath.path_sequence) {
    if (item.mode === 'parallel') {
      const memberSDOs = [];
      const memberAttackEnrich = [];
      for (const member of item.steps) {
        let sdo;
        if (member.status === 'unresolved') {
          sdo = buildUnresolvedSDO(member, opts);
        } else {
          sdo = buildAttackStepSDO(member, opts);
          memberAttackEnrich.push(...buildAttackTechniqueSDOs(member, sdo.id, opts));
        }
        memberSDOs.push(sdo);
      }
      const memberIds = memberSDOs.map(s => s.id);
      const grouping = buildParallelGrouping(item, memberIds, opts);
      objects.push(grouping);
      objects.push(...memberSDOs);
      objects.push(...memberAttackEnrich);
      anchors.push({ id: grouping.id, deltaT: item.delta_t_to_next });
    } else if (item.status === 'unresolved') {
      const sdo = buildUnresolvedSDO(item, opts);
      objects.push(sdo);
      anchors.push({ id: sdo.id, deltaT: item.delta_t_to_next });
    } else {
      const sdo = buildAttackStepSDO(item, opts);
      objects.push(sdo);
      objects.push(...buildAttackTechniqueSDOs(item, sdo.id, opts));
      anchors.push({ id: sdo.id, deltaT: item.delta_t_to_next });
    }
  }

  // Sequence edges
  for (let i = 0; i < anchors.length - 1; i++) {
    objects.push(buildPrecedesRelationship(anchors[i].id, anchors[i + 1].id, anchors[i].deltaT, opts));
  }

  const allIds = objects.map(o => o.id);
  const report = buildReport(attackPath.metadata, allIds, opts);

  const bundle = {
    type: 'bundle',
    id: newId('bundle'),
    objects: [report, ...objects]
  };
  return bundle;
}

function loadJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function writeJson(p, obj) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(obj, null, 2));
}

function deriveOutPath(inputPath, outDir) {
  const base = path.basename(inputPath, '.json');
  return path.join(outDir, `${base}.stix.json`);
}

function main(argv) {
  const args = argv.slice(2);
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log('Usage:');
    console.log('  node export-stix.js <input.json> [--out <output.json>]');
    console.log('  node export-stix.js --pilot      # SolarWinds + AD cascade');
    console.log('  node export-stix.js --all        # all attack-paths/*.json');
    return 0;
  }

  const repoRoot = path.resolve(__dirname, '..', '..');
  const stixOutDir = path.join(repoRoot, 'attack-paths', 'stix');

  if (args.includes('--pilot')) {
    const targets = [
      path.join(repoRoot, 'json-schemas', 'layer-3', 'examples', 'solarwinds-2020.json'),
      path.join(repoRoot, 'attack-paths', 'ad-domain-admin-cascade-2025.json')
    ];
    for (const t of targets) {
      const bundle = exportPath(loadJson(t));
      const outPath = deriveOutPath(t, stixOutDir);
      writeJson(outPath, bundle);
      console.log(`wrote ${path.relative(repoRoot, outPath)}`);
    }
    return 0;
  }

  if (args.includes('--all')) {
    const apDir = path.join(repoRoot, 'attack-paths');
    const files = fs.readdirSync(apDir).filter(f => f.endsWith('.json'));
    for (const f of files) {
      const t = path.join(apDir, f);
      const bundle = exportPath(loadJson(t));
      const outPath = deriveOutPath(t, stixOutDir);
      writeJson(outPath, bundle);
      console.log(`wrote ${path.relative(repoRoot, outPath)}`);
    }
    return 0;
  }

  const inputPath = args[0];
  const outIdx = args.indexOf('--out');
  const outPath = outIdx >= 0 ? args[outIdx + 1] : deriveOutPath(inputPath, stixOutDir);
  const bundle = exportPath(loadJson(inputPath));
  writeJson(outPath, bundle);
  console.log(`wrote ${outPath}`);
  return 0;
}

if (require.main === module) {
  process.exit(main(process.argv));
}

module.exports = { exportPath, extractAttackTechniqueIds, strategicCluster, clusterDisplayName };
