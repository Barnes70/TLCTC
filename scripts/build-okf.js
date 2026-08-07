#!/usr/bin/env node
/*
 * build-okf.js — Generate an Open Knowledge Format (OKF) bundle from the
 * canonical TLCTC sources. OKF (GoogleCloudPlatform/knowledge-catalog, SPEC v0.1)
 * packages knowledge as a tree of markdown files with YAML frontmatter so both
 * humans and LLM agents can consume it. This bundle is a *rendered view* over the
 * existing JSON / whitepaper sources — those remain the single source of truth.
 *
 * Usage:  node scripts/build-okf.js
 * Output: okf/  (overwritten on each run)
 *
 * Deps: Node builtins only (fs, path). No frontmatter library — see fm().
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'okf');

// ───────────────────────── source paths ──────────────────────────────────────
const SRC = {
  framework: 'json-schemas/layer-1/tlctc-framework.v2.5.json',
  registry: 'json-schemas/layer-2/example-registry.json',
  whitepaper: 'documentation/tlctc-v2.0-whitepaper.md',
  glossary: 'documentation/tlctc-glossary.md',
  isoMatrix: 'tools/control-matrix-starter-iso27001.json',
  genericMatrix: 'tools/control-matrix-starter.json',
  attackPathsDir: 'attack-paths',
  mapAttack: 'mappings/mitre-attack-enterprise/tlctc-enterprise-attack.json',
  mapCwe: 'mappings/mitre-cwe/tlctc-cwe.json',
  mapSigma: 'mappings/sigma/tlctc-sigma.json',
};

// ───────────────────────── io helpers ────────────────────────────────────────
const readText = (rel) => fs.readFileSync(path.join(ROOT, rel), 'utf8');
const readJSON = (rel) => JSON.parse(readText(rel));

function slug(s) {
  return String(s)
    .toLowerCase()
    .replace(/['’"]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/-{2,}/g, '-');
}

function firstSentence(s) {
  if (!s) return '';
  const m = String(s).match(/^(.*?[.!?])(\s|$)/s);
  return (m ? m[1] : String(s)).replace(/\s+/g, ' ').trim();
}

// directory → list of {file, title, type} for index.md generation
const dirEntries = new Map();
let docCount = 0;
const typeCounts = new Map();
// flat inventory of every concept doc, for manifest.json
const manifest = [];

function recordEntry(relFile, title, type) {
  const dir = path.dirname(relFile);
  if (!dirEntries.has(dir)) dirEntries.set(dir, []);
  dirEntries.get(dir).push({ file: path.basename(relFile), title, type });
}

// ───────────────────────── frontmatter serializer ────────────────────────────
function yamlScalar(v) {
  if (v === null || v === undefined) return '';
  if (typeof v === 'number' || typeof v === 'boolean') return String(v);
  const s = String(v).replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\s+/g, ' ').trim();
  return `"${s}"`;
}

function fm(obj) {
  const lines = ['---'];
  for (const [k, v] of Object.entries(obj)) {
    if (v === undefined || v === null) continue;
    if (Array.isArray(v)) {
      if (v.length === 0) continue;
      lines.push(`${k}:`);
      for (const item of v) lines.push(`  - ${yamlScalar(item)}`);
    } else if (typeof v === 'object') {
      lines.push(`${k}:`);
      for (const [kk, vv] of Object.entries(v)) lines.push(`  ${kk}: ${yamlScalar(vv)}`);
    } else {
      lines.push(`${k}: ${yamlScalar(v)}`);
    }
  }
  lines.push('---', '');
  return lines.join('\n');
}

// write a normal concept doc (frontmatter + body); records it for indexing
function writeDoc(relFile, frontmatterObj, body) {
  const abs = path.join(OUT, relFile);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.writeFileSync(abs, fm(frontmatterObj) + body.trimEnd() + '\n', 'utf8');
  recordEntry(relFile, frontmatterObj.title || relFile, frontmatterObj.type || '');
  docCount++;
  typeCounts.set(frontmatterObj.type, (typeCounts.get(frontmatterObj.type) || 0) + 1);
  manifest.push({
    path: '/' + relFile.split(path.sep).join('/'),
    type: frontmatterObj.type || '',
    title: frontmatterObj.title || '',
    description: frontmatterObj.description || '',
    resource: frontmatterObj.resource || '',
    tags: frontmatterObj.tags || [],
  });
}

// write a reserved file (index.md / log.md / README.md) — NO frontmatter
function writeReserved(relFile, body) {
  const abs = path.join(OUT, relFile);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.writeFileSync(abs, body.trimEnd() + '\n', 'utf8');
}

const PROVENANCE_ISO =
  '> **Provenance:** the ISO 27001:2022 Annex A control placements below are *starter guidance* ' +
  'derived from the TLCTC Control Matrix tool (`tools/`), AI-assisted and not a certified control ' +
  'set. The normative cause-side taxonomy is the cluster definitions; control selection is ' +
  'organization-specific. See `/controls/index.md`.';

// ═════════════════════════ SOURCES ═══════════════════════════════════════════
const framework = readJSON(SRC.framework);
const registry = readJSON(SRC.registry);
const whitepaper = readText(SRC.whitepaper);
const glossaryMd = readText(SRC.glossary);

const CLUSTER_IDS = Object.keys(framework.clusters); // ['#1'..'#10']
const clusterNum = (id) => String(id).replace('#', '');
const clusterByNum = {};
for (const id of CLUSTER_IDS) clusterByNum[clusterNum(id)] = framework.clusters[id];

// ═════════════════════════ CLUSTERS ══════════════════════════════════════════
// Cluster body prose comes from whitepaper §4.1 (the only source with all six
// fields). Split on '#### #N Name' headings, capture until the next heading.
function extractClusterSections(md) {
  const out = {};
  const re = /\n####\s+#(\d{1,2})\s+([^\n]+)\n/g;
  const marks = [];
  let m;
  while ((m = re.exec(md)) !== null) {
    marks.push({ num: m[1], name: m[2].trim(), start: m.index + m[0].length, headStart: m.index });
  }
  for (let i = 0; i < marks.length; i++) {
    const cur = marks[i];
    let end = md.length;
    // stop at the next '#### ' or a higher-level heading ('### ' / '## ')
    const tail = md.slice(cur.start);
    const stop = tail.search(/\n(?:####\s|###\s|##\s)/);
    end = stop === -1 ? md.length : cur.start + stop;
    out[cur.num] = md.slice(cur.start, end).trim();
  }
  return out;
}
const clusterSections = extractClusterSections(whitepaper);

function buildClusters() {
  for (const id of CLUSTER_IDS) {
    const c = framework.clusters[id];
    const n = clusterNum(id);
    const title = `${id} ${c.name}`;
    const body = [];
    body.push(`# ${title}`, '');
    body.push(clusterSections[n] || `**Definition:** ${c.definition}`, '');
    body.push('# Schema', '');
    body.push(`- **Strategic ID:** ${c.strategic_id}`);
    body.push(`- **Operational root:** ${c.operational_root_id}`);
    body.push(`- **Generic vulnerability:** ${c.generic_vulnerability}`);
    body.push(`- **Topology:** ${c.topology}`);
    body.push('');
    body.push('# Relationships', '');
    body.push(`- Governing axioms: [Axiom III](/axioms/axiom-iii.md), [Axiom VI](/axioms/axiom-vi.md), [Axiom VII](/axioms/axiom-vii.md)`);
    body.push(`- Classification rules: see [/rules/index.md](/rules/index.md)`);
    body.push(`- Control objectives: [/controls/cluster-${n}.md](/controls/cluster-${n}.md)`);
    body.push(`- Mapped techniques: [ATT&CK](/mappings/attack/cluster-${n}.md) · [CWE](/mappings/cwe/cluster-${n}.md) · [Sigma](/mappings/sigma/cluster-${n}.md)`);
    writeDoc(`clusters/cluster-${n}.md`, {
      type: 'cluster',
      title,
      description: firstSentence(c.definition),
      resource: `tlctc:cluster:${id}`,
      tags: ['taxonomy', 'cluster', c.topology],
      strategic_id: c.strategic_id,
      operational_root_id: c.operational_root_id,
      generic_vulnerability: c.generic_vulnerability,
      topology: c.topology,
    }, body.join('\n'));
  }
}

// ═════════════════════════ AXIOMS & RULES ════════════════════════════════════
const ROMAN = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'];

function buildAxioms() {
  framework.axioms.forEach((a, i) => {
    const file = `axioms/axiom-${ROMAN[i + 1] || slug(a.axiom_id)}.md`;
    writeDoc(file, {
      type: 'axiom',
      title: a.axiom_id,
      description: firstSentence(a.statement),
      resource: `tlctc:axiom:${slug(a.axiom_id)}`,
      tags: ['taxonomy', 'axiom'],
    }, `# ${a.axiom_id}\n\n${a.statement}\n${a.notes ? `\n> ${a.notes}\n` : ''}`);
  });
}

function buildRules() {
  for (const r of framework.rules) {
    const body = [
      `# ${r.rule_id}`, '',
      r.statement, '',
      ...(r.notes ? [`> ${r.notes}`, ''] : []),
      '# Schema', '',
      `- **Enforcement level:** ${r.enforcement_level}`,
      `- **Machine enforceable:** ${r.machine_enforceable}`,
    ].join('\n');
    writeDoc(`rules/${slug(r.rule_id)}.md`, {
      type: 'rule',
      title: r.rule_id,
      description: firstSentence(r.statement),
      resource: `tlctc:rule:${r.rule_id}`,
      tags: ['taxonomy', 'rule', r.enforcement_level],
      enforcement_level: r.enforcement_level,
      machine_enforceable: r.machine_enforceable,
    }, body);
  }
}

// ═════════════════════════ LAYER-2 REGISTRY ══════════════════════════════════
function buildRegistry() {
  for (const s of registry.spheres) {
    const id = s.sphere_id.replace('@', '');
    writeDoc(`spheres/${slug(id)}.md`, {
      type: 'sphere',
      title: s.sphere_id,
      description: firstSentence(s.description),
      resource: `tlctc:sphere:${s.sphere_id}`,
      tags: ['registry', 'sphere', s.typical_domain],
      typical_domain: s.typical_domain,
    }, `# ${s.sphere_id}\n\n${s.description}\n\n- **Typical domain:** ${s.typical_domain}\n`);
  }
  for (const b of registry.boundary_contexts) {
    writeDoc(`contexts/${slug(b.context)}.md`, {
      type: 'boundary-context',
      title: b.context,
      description: firstSentence(b.description),
      resource: `tlctc:context:${b.context}`,
      tags: ['registry', 'boundary-context'],
    }, `# ${b.context}\n\n${b.description}\n`);
  }
  for (const t of registry.intra_system_boundary_types) {
    writeDoc(`contexts/intra-${slug(t.type)}.md`, {
      type: 'intra-boundary-type',
      title: `${t.type} (intra-system)`,
      description: firstSentence(t.description),
      resource: `tlctc:intra-boundary:${t.type}`,
      tags: ['registry', 'intra-system-boundary'],
    }, `# ${t.type} (intra-system boundary)\n\n${t.description}\n\n${t.notes ? '> ' + t.notes + '\n' : ''}`);
  }
}

// ═════════════════════════ GLOSSARY ══════════════════════════════════════════
function buildGlossary() {
  // terms are '### Term' headings; capture body until next '### ' or '## '
  const re = /\n###\s+([^\n]+)\n/g;
  const marks = [];
  let m;
  while ((m = re.exec(glossaryMd)) !== null) {
    marks.push({ term: m[1].trim(), start: m.index + m[0].length, headStart: m.index });
  }
  const seen = new Set();
  for (let i = 0; i < marks.length; i++) {
    const cur = marks[i];
    const tail = glossaryMd.slice(cur.start);
    const stop = tail.search(/\n(?:###\s|##\s)/);
    const end = stop === -1 ? glossaryMd.length : cur.start + stop;
    const body = glossaryMd.slice(cur.start, end).trim();
    // term titles may carry trailing markers like *(V2.1)* — keep clean title
    const cleanTitle = cur.term.replace(/\*\([^)]*\)\*/g, '').trim();
    let s = slug(cleanTitle);
    if (!s || seen.has(s)) s = slug(cur.term) || `term-${i}`;
    if (seen.has(s)) s = `${s}-${i}`;
    seen.add(s);
    writeDoc(`glossary/${s}.md`, {
      type: 'term',
      title: cleanTitle,
      description: firstSentence(body.replace(/[*_`>#-]/g, ' ')),
      resource: `tlctc:term:${s}`,
      tags: ['glossary'],
    }, `# ${cleanTitle}\n\n${body}\n`);
  }
}

// ═════════════════════════ ATTACK PATHS ══════════════════════════════════════
function boundaryStr(b) {
  if (!b) return '';
  const transit = (b.transit_spheres && b.transit_spheres.length)
    ? b.transit_spheres.map((t) => `${t}⇒`).join('') : '';
  return `||[${b.context}][${transit}${b.source_sphere}→${b.target_sphere}]||`;
}

function stepNotation(step) {
  if (step.status === 'unresolved') {
    return `${boundaryStr(step.topology_boundary)}${step.unresolved_type === 'gap' ? '…' : '?'}`.trim();
  }
  let s = step.cluster || '';
  const b = boundaryStr(step.topology_boundary);
  if (b) s = `${b}${s ? ' ' + s : ''}`.trim();
  if (step.fec_executed) s += ' (FEC)';
  if (step.outcomes && step.outcomes.length) s += ` + [DRE: ${step.outcomes.join(', ')}]`;
  return s;
}

function buildNotation(seq) {
  const parts = [];
  for (const item of seq) {
    let token;
    if (item.mode === 'parallel' && item.steps) {
      token = '(' + item.steps.map((s) => s.cluster).join(' + ') + ')';
    } else {
      token = stepNotation(item);
    }
    const dt = item.delta_t_to_next;
    parts.push(token);
    if (dt) parts.push(`→[Δt=${dt}]`);
    else if (item !== seq[seq.length - 1]) parts.push('→');
  }
  return parts.join(' ').replace(/\s+→\s+→/g, ' →').trim();
}

function clustersUsed(seq) {
  const set = new Set();
  for (const item of seq) {
    if (item.cluster) set.add(item.cluster);
    if (item.steps) item.steps.forEach((s) => s.cluster && set.add(s.cluster));
  }
  return [...set];
}

function buildAttackPaths() {
  const dir = path.join(ROOT, SRC.attackPathsDir);
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.json'));
  for (const f of files) {
    let data;
    try { data = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')); }
    catch (e) { console.warn(`  ! skipped ${f}: ${e.message}`); continue; }
    if (!data || !data.path_sequence || !data.metadata) continue;
    const meta = data.metadata;
    const seq = data.path_sequence;
    const used = clustersUsed(seq);
    const body = [];
    body.push(`# ${meta.incident_id || f.replace(/\.json$/, '')}`, '');
    body.push('## Attack path', '', '```', buildNotation(seq), '```', '');
    body.push('# Schema', '', '| Step | Cluster | Boundary | Δt→next | DRE |', '|---|---|---|---|---|');
    const eb = (b) => boundaryStr(b).replace(/\|/g, '\\|');
    for (const item of seq) {
      if (item.mode === 'parallel') {
        const cl = item.steps.map((s) => `[${s.cluster}](/clusters/cluster-${clusterNum(s.cluster)}.md)`).join(' + ');
        body.push(`| ${item.group_id || 'parallel'} | ${cl} | | ${item.delta_t_to_next || ''} | |`);
        continue;
      }
      if (item.status === 'unresolved') {
        body.push(`| ${item.step_id} | ${item.unresolved_type === 'gap' ? '…' : '?'} (unresolved) | ${eb(item.topology_boundary)} | ${item.delta_t_to_next || ''} | |`);
        continue;
      }
      const cl = item.cluster ? `[${item.cluster}](/clusters/cluster-${clusterNum(item.cluster)}.md)` : '';
      const dre = (item.outcomes || []).join(', ');
      body.push(`| ${item.step_id} | ${cl}${item.fec_executed ? ' (FEC)' : ''} | ${eb(item.topology_boundary)} | ${item.delta_t_to_next || ''} | ${dre} |`);
    }
    body.push('');
    body.push('## Step notes', '');
    for (const item of seq) {
      if (item.notes) body.push(`- **${item.step_id || item.group_id || 'step'}:** ${item.notes}`);
    }
    body.push('');
    if (meta.notes) body.push('# Citations', '', meta.notes, '');
    const incidentSlug = f.replace(/\.json$/, '');
    writeDoc(`attack-paths/${incidentSlug}.md`, {
      type: 'attack-path',
      title: meta.incident_id || incidentSlug,
      description: firstSentence(meta.notes) || `TLCTC attack-path analysis: ${incidentSlug}`,
      resource: `tlctc:attack-path:${incidentSlug}`,
      tags: ['attack-path', ...used.map((c) => c.replace('#', 'cluster-')), `confidence-${meta.analyst_confidence || 'unknown'}`],
      timestamp: meta.created_at,
      tlctc_version: meta.tlctc_version,
    }, body.join('\n'));
  }
}

// ═════════════════════════ MAPPINGS ══════════════════════════════════════════
const primaryCluster = (mappingStr) => {
  const m = String(mappingStr || '').match(/#(\d{1,2})/);
  return m ? m[1] : null;
};

function buildMappingSource(key, jsonRel, opts) {
  let data;
  try { data = readJSON(jsonRel); } catch (e) { console.warn(`  ! mapping ${key} unavailable: ${e.message}`); return; }
  const groups = {};
  for (let n = 1; n <= 10; n++) groups[n] = [];
  let unmapped = 0;
  for (const rec of data.mappings || []) {
    const n = opts.clusterOf(rec);
    if (n && groups[n]) groups[n].push(rec); else unmapped++;
  }
  for (let n = 1; n <= 10; n++) {
    const recs = groups[n];
    const c = clusterByNum[n];
    const body = [];
    body.push(`# ${opts.label} → #${n} ${c.name}`, '');
    body.push(`> ${opts.provenance}`, '');
    body.push(`Mapped entries: **${recs.length}**. Cluster: [#${n} ${c.name}](/clusters/cluster-${n}.md).`, '');
    if (recs.length) {
      body.push(opts.header, opts.divider);
      for (const rec of recs) body.push(opts.row(rec));
      body.push('');
    }
    writeDoc(`mappings/${key}/cluster-${n}.md`, {
      type: 'mapping-set',
      title: `${opts.label} → #${n} ${c.name}`,
      description: `${recs.length} ${opts.label} entries mapped to TLCTC #${n} ${c.name}.`,
      resource: `tlctc:mapping:${key}:cluster-${n}`,
      tags: ['mapping', key, `cluster-${n}`],
    }, body.join('\n'));
  }
  return { total: (data.mappings || []).length, unmapped };
}

const esc = (s) => String(s == null ? '' : s).replace(/\|/g, '\\|').replace(/\n+/g, ' ').trim();

function buildMappings() {
  buildMappingSource('attack', SRC.mapAttack, {
    label: 'ATT&CK techniques',
    provenance: 'Source: MITRE ATT&CK Enterprise → TLCTC mapping (`mappings/mitre-attack-enterprise/`).',
    clusterOf: (r) => primaryCluster(r.tlctcMapping),
    header: '| Technique | Name | TLCTC | Rationale |',
    divider: '|---|---|---|---|',
    row: (r) => `| ${esc(r.techniqueId)} | ${esc(r.techniqueName)} | ${esc(r.tlctcMapping)} | ${esc(r.mappingRationale)} |`,
  });
  buildMappingSource('cwe', SRC.mapCwe, {
    label: 'CWE weaknesses',
    provenance: 'Source: MITRE CWE → TLCTC mapping (`mappings/mitre-cwe/`). AI-generated, human-reviewed; experimental.',
    clusterOf: (r) => primaryCluster(r.tlctcMapping),
    header: '| CWE | Name | TLCTC | Verdict | Rationale |',
    divider: '|---|---|---|---|---|',
    row: (r) => `| ${esc(r.cweId)} | ${esc(r.cweName)} | ${esc(r.tlctcMapping)} | ${esc(r.mappingVerdict)} | ${esc(r.mappingRationale)} |`,
  });
  buildMappingSource('sigma', SRC.mapSigma, {
    label: 'Sigma rules',
    provenance: 'Source: SigmaHQ rules → TLCTC mapping (`mappings/sigma/`). Derived via ATT&CK technique mapping.',
    clusterOf: (r) => (r.primaryCluster ? primaryCluster(r.primaryCluster) : null),
    header: '| Rule | Techniques | Cluster set | Status |',
    divider: '|---|---|---|---|',
    row: (r) => `| ${esc(r.ruleTitle)} | ${esc((r.techniques || []).join(', '))} | ${esc((r.clusterSet || []).join(', '))} | ${esc(r.derivationStatus)} |`,
  });
}

// ═════════════════════════ CONTROLS ══════════════════════════════════════════
const CSF = [
  { key: 'GV', name: 'GOVERN', side: 'cross-cutting' },
  { key: 'ID', name: 'IDENTIFY', side: 'preventive (left)' },
  { key: 'PR', name: 'PROTECT', side: 'preventive (left)' },
  { key: 'DE', name: 'DETECT', side: 'mitigating (right)' },
  { key: 'RS', name: 'RESPOND', side: 'mitigating (right)' },
  { key: 'RC', name: 'RECOVER', side: 'mitigating (right)' },
];
const CSF_DESC = {
  GOVERN: 'Set direction, accountability and ownership, risk appetite, and assurance so all clusters are managed consistently. Cross-cutting — does not counter a single cluster.',
  IDENTIFY: 'Find the weaknesses and exposure that enable the cluster step. Left (cause) side of the bow-tie.',
  PROTECT: 'Prevent or reduce the likelihood of the cluster step succeeding. Left (cause) side of the bow-tie.',
  DETECT: 'Recognize the cluster step / loss of control within its Δt window. Straddles the central event.',
  RESPOND: 'Contain and eradicate the realized step before a Data Risk Event matures into a Business Risk Event. Right (consequence) side.',
  RECOVER: 'Restore trustworthy capability and limit the consequence chain after the central event. Right (consequence) side.',
};
function objectiveLine(funcName, id, name) {
  switch (funcName) {
    case 'GOVERN': return `Establish ownership, policy, and risk-appetite for ${id} ${name}.`;
    case 'IDENTIFY': return `Identify the weaknesses and exposure enabling ${id} ${name}.`;
    case 'PROTECT': return `Prevent or reduce the likelihood of the ${id} ${name} step.`;
    case 'DETECT': return `Detect ${id} ${name} activity within its Δt window, before it enables the next step.`;
    case 'RESPOND': return `Contain and eradicate ${id} ${name} once detected.`;
    case 'RECOVER': return `Restore trustworthy capability after ${id} ${name}.`;
    default: return '';
  }
}

function buildControlFunctions() {
  for (const fnc of CSF) {
    const body = [
      `# ${fnc.name}`, '',
      CSF_DESC[fnc.name], '',
      '# Schema', '',
      `- **CSF function:** ${fnc.name} (${fnc.key})`,
      `- **Bow-tie position:** ${fnc.side}`,
      '',
      'Applies across all ten clusters; see each [control-objective set](/controls/index.md).',
    ].join('\n');
    writeDoc(`controls/functions/${slug(fnc.name)}.md`, {
      type: 'csf-function',
      title: fnc.name,
      description: firstSentence(CSF_DESC[fnc.name]),
      resource: `tlctc:csf-function:${fnc.key}`,
      tags: ['controls', 'nist-csf', fnc.key],
    }, body);
  }
}

function buildControlClusters() {
  let isoCells = {};
  try { isoCells = readJSON(SRC.isoMatrix).environments[0].cells; }
  catch (e) { console.warn(`  ! ISO matrix unavailable: ${e.message}`); }
  for (let n = 1; n <= 10; n++) {
    const c = clusterByNum[n];
    const id = `#${n}`;
    const body = [];
    body.push(`# Controls → ${id} ${c.name}`, '');
    body.push(PROVENANCE_ISO, '');
    body.push(`Cause: [${id} ${c.name}](/clusters/cluster-${n}.md). Functions: [GOVERN](/controls/functions/govern.md) · [IDENTIFY](/controls/functions/identify.md) · [PROTECT](/controls/functions/protect.md) · [DETECT](/controls/functions/detect.md) · [RESPOND](/controls/functions/respond.md) · [RECOVER](/controls/functions/recover.md). Effectiveness: [/controls/effectiveness-model.md](/controls/effectiveness-model.md).`, '');
    if (n === 2 || n === 4) {
      body.push(`> The whitepaper provides a normative worked example for ${id} (§8.1.${n === 2 ? '5' : '6'}); the ISO 27001 Annex A controls below are the operational starter layer.`, '');
    }
    for (const fnc of CSF) {
      const cell = isoCells[`${n}-${fnc.key}`] || {};
      body.push(`## ${fnc.name}`, '');
      body.push(`*${fnc.side}.* **Objective:** ${objectiveLine(fnc.name, id, c.name)}`, '');
      const renderList = (label, arr) => {
        if (!arr || !arr.length) return;
        body.push(`**${label} controls (ISO 27001:2022 Annex A):**`, '');
        for (const ctl of arr) body.push(`- ${ctl.name}${ctl.description ? ' — ' + ctl.description : ''}`);
        body.push('');
      };
      renderList('Local', cell.local);
      renderList('Umbrella', cell.umbrella);
    }
    writeDoc(`controls/cluster-${n}.md`, {
      type: 'control-objective-set',
      title: `Controls → ${id} ${c.name}`,
      description: `NIST CSF control objectives and ISO 27001:2022 Annex A starter controls for TLCTC ${id} ${c.name}.`,
      resource: `tlctc:controls:cluster-${n}`,
      tags: ['controls', 'nist-csf', 'iso27001', `cluster-${n}`],
      cluster: id,
    }, body.join('\n'));
  }
}

function buildEffectivenessModel() {
  const body = `# Control Effectiveness Model

The TLCTC Control Matrix assesses each control in three layers and combines them into a
single **Effective Control Rating (ECR)**. The model lives in the Control Matrix tool
(\`tools/control-matrix.html\`); this document summarizes it for agent consumption.

## Three layers

- **CDE_max** — *Design effectiveness ceiling* (0.00–0.99, never 1.0): the theoretical
  prevention/detection limit of the control by design. No control is perfect.
- **CDE_fitness** — *Velocity fitness* (factor 1.0 / 0.5 / 0.0): whether the control can
  structurally act within the cell's attack-velocity (Δt) window.
- **COE** — *Operational effectiveness*: measured performance from typed metrics
  (coverage, currency, mode, configuration, performance).

\`\`\`
ECR = COE × CDE_max × fitness_factor
\`\`\`

## Cell aggregation

- **Essential** controls set a **worst-of floor**.
- **Complementary** controls add a probabilistic **ceiling raise**.
- **Cell ECR = floor + raise.**
- **Residual ceiling gap = 1.0 − cell CDE_max composite** — risk that operations cannot
  close, only new control *types* or explicit acceptance can.

## Detection Coverage Score (DETECT cells)

\`\`\`
DCS = MTTD / Δt
\`\`\`

| DCS | Verdict |
|---|---|
| < 0.5 | effective |
| 0.5–0.8 | adequate |
| 0.8–1.0 | marginal |
| 1.0–2.0 | ineffective |
| > 2.0 | structurally failed |

The same MTTD can be effective or ineffective depending on the Δt of the transition being
defended — see [/controls/indicators.md](/controls/indicators.md) and
[velocity classes](/glossary/velocity-class.md).

## Worked example (DETECT × #7 Malware)

EDR (behavioral): CDE_max 0.85 (misses novel fileless techniques), fitness 1.0 (acts within
seconds, VC-3), COE 0.97 (active-agent coverage) → **ECR ≈ 0.82**. Combined in the DE×#7 cell
with SIEM correlation and sandbox detonation as complementary controls to raise the ceiling.
Source: \`tools/control-matrix-starter.json\`.
`;
  writeDoc('controls/effectiveness-model.md', {
    type: 'effectiveness-model',
    title: 'Control Effectiveness Model (CDE → COE → ECR, DCS)',
    description: 'Three-layer control effectiveness model: CDE_max, CDE_fitness, COE, ECR, and the Detection Coverage Score.',
    resource: 'tlctc:controls:effectiveness-model',
    tags: ['controls', 'effectiveness', 'dcs', 'metrics'],
  }, body);
}

function buildIndicators() {
  const body = `# Indicators: KRI, KCI, KPI, DCS

The cluster × function matrix becomes measurable through a small hierarchy of strategic
indicators, each anchored to the organization's risk appetite. Source: application paper §10.

## KRI — Key Risk Indicators
Sit at the risk-event layer; measure *exposure to threat pressure* per cluster (incidents and
**near-misses**, where the threat materialized but a control held). Bounded directly by risk
appetite. Example: credential-stuffing volume (#4), malware execution attempts (#7), split
into blocked (near-miss) vs successful (incident).

## KCI — Key Control Indicators
Sit at the control-objectives layer; measure whether each matrix objective is achieved against
a risk-appetite-derived target.
- **Technical KCI** — state/coverage ("what *is* the posture?"): % privileged accounts with
  hardware MFA (#4), % endpoints with application allowlisting (#7).
- **Procedural KCI** — process performance ("how fast/well?"): mean time to patch critical CVEs
  (#1/#2), mean time to revoke compromised tokens (#4).

## KPI — Key Performance Indicators
The procedural KCIs viewed as process-performance measures; KPI is the performance facet of KCI,
not a separate fourth type. The strategic three-way split is: risk exposure (KRI), control state
(technical KCI), control performance (procedural KCI/KPI).

## DCS — Detection Coverage Score
\`DCS = MTTD / Δt\`. A control's performance is only sufficient *relative to attacker speed*. See
[/controls/effectiveness-model.md](/controls/effectiveness-model.md).
`;
  writeDoc('controls/indicators.md', {
    type: 'indicator-framework',
    title: 'Indicators: KRI, KCI, KPI, DCS',
    description: 'Strategic indicator hierarchy (KRI / KCI / KPI / DCS) for measuring the TLCTC × CSF control matrix.',
    resource: 'tlctc:controls:indicators',
    tags: ['controls', 'indicators', 'kri', 'kci', 'kpi', 'dcs'],
  }, body);
}

// ═════════════════════════ INDEX / RESERVED FILES ════════════════════════════
function writeIndexes() {
  // Collect every directory, including intermediate parents (e.g. 'mappings').
  const allDirs = new Set();
  for (const dir of dirEntries.keys()) {
    if (dir === '.') continue;
    const parts = dir.split('/');
    for (let i = 1; i <= parts.length; i++) allDirs.add(parts.slice(0, i).join('/'));
  }
  const childDirsOf = (dir) => [...allDirs].filter(
    (d) => d !== dir && d.startsWith(dir + '/') && d.slice(dir.length + 1).indexOf('/') === -1
  );

  for (const dir of allDirs) {
    const entries = (dirEntries.get(dir) || []).slice()
      .sort((a, b) => a.file.localeCompare(b.file, undefined, { numeric: true }));
    const subdirs = childDirsOf(dir).sort();
    const title = dir.split('/').map((p) => p.replace(/-/g, ' ')).join(' / ');
    const lines = [`# ${title}`, ''];
    if (subdirs.length) {
      lines.push('Subsections:', '');
      for (const sd of subdirs) lines.push(`- [${sd.split('/').pop()}](/${sd}/index.md)`);
      lines.push('');
    }
    if (entries.length) {
      lines.push(`${entries.length} document(s).`, '');
      for (const e of entries) lines.push(`- [${e.title}](/${dir}/${e.file})${e.type ? ` — \`${e.type}\`` : ''}`);
    }
    writeReserved(`${dir}/index.md`, lines.join('\n'));
  }
}

function topDirs() {
  // distinct top-level dirs under okf/
  const set = new Set();
  for (const dir of dirEntries.keys()) if (dir !== '.') set.add(dir.split('/')[0]);
  return [...set].sort();
}

function writeRoot() {
  const sections = {
    clusters: 'The ten cause-oriented threat clusters.',
    axioms: 'The ten framework axioms.',
    rules: 'Classification rules (R-*).',
    spheres: 'Responsibility spheres (Layer 2).',
    contexts: 'Boundary contexts and intra-system boundary types (Layer 2).',
    glossary: 'Glossary of TLCTC terms.',
    'attack-paths': 'Layer-3 incident attack-path analyses.',
    controls: 'NIST CSF × TLCTC control matrix, ISO 27001 starter, effectiveness model, indicators.',
    mappings: 'Mappings to MITRE ATT&CK, MITRE CWE, and SigmaHQ.',
  };
  const lines = [
    '# TLCTC — Open Knowledge Format bundle', '',
    'A rendered, agent-consumable view of the TLCTC (Top Level Cyber Threat Clusters) taxonomy,',
    'generated from the canonical JSON schemas and documentation. See [README.md](/README.md).', '',
  ];
  for (const d of topDirs()) {
    lines.push(`- [${d}](/${d}/index.md) — ${sections[d] || ''}`);
  }
  lines.push('', '[manifest.json](/manifest.json) — machine-readable inventory of every document (path, type, title, tags).');
  writeReserved('index.md', lines.join('\n'));

  const today = new Date().toISOString().slice(0, 10);
  writeReserved('log.md', [
    '# Changelog', '',
    `## ${today}`, '',
    `- Initial OKF bundle generated from TLCTC v${framework.metadata.tlctc_version} sources (${docCount} documents).`,
  ].join('\n'));

  writeReserved('README.md', [
    '# TLCTC Open Knowledge Format (OKF) bundle', '',
    'This directory is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)',
    'bundle (SPEC v0.1): a tree of markdown files with YAML frontmatter, built so both humans and',
    'LLM agents can consume the TLCTC taxonomy. It is a **rendered view** — the canonical sources',
    '(JSON schemas in `json-schemas/`, documentation in `documentation/`, tools in `tools/`) remain',
    'the single source of truth.', '',
    '## Regenerate', '', '```bash', 'node scripts/build-okf.js', 'node scripts/validate-okf.js okf/', '```', '',
    '## Machine-readable inventory', '',
    '[`manifest.json`](manifest.json) lists every document with its `path`, `type`, `title`,',
    '`description`, `resource`, and `tags` — plus per-type counts — so programmatic consumers',
    'can index the bundle without walking links. It is deterministic (no build timestamp).', '',
    '## Contents', '',
    `Generated from TLCTC v${framework.metadata.tlctc_version}. ${docCount} concept documents across`,
    `${topDirs().length} sections (clusters, axioms, rules, spheres, contexts, glossary, attack-paths,`,
    'controls, mappings).', '',
    '## Provenance notes', '',
    '- Cluster bodies render the whitepaper §4.1 seven-field definitions (Definition, Generic',
    '  Vulnerability, and Attacker\'s View verbatim from `tlctc-framework.v2.5.json`; Scope,',
    '  Developer\'s View, and Boundary Tests canonical in the whitepaper).',
    '- Control docs combine NIST CSF objectives (normative) with ISO 27001:2022 Annex A *starter*',
    '  controls (AI-assisted, from `tools/`) — guidance, not a certified control set.',
    '- CWE mappings are AI-generated and experimental.', '',
    '## License', '', 'CC BY 4.0 — see [../LICENSE](../LICENSE).',
  ].join('\n'));
}

// machine-readable inventory of every concept doc (deterministic: no timestamp)
function writeManifest() {
  const documents = manifest.slice().sort((a, b) => a.path.localeCompare(b.path));
  const type_counts = {};
  for (const t of [...typeCounts.keys()].sort()) type_counts[t] = typeCounts.get(t);
  const data = {
    bundle: 'tlctc-okf',
    okf_spec_version: '0.1',
    tlctc_version: framework.metadata.tlctc_version,
    generator: 'scripts/build-okf.js',
    document_count: documents.length,
    type_counts,
    documents,
  };
  fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify(data, null, 2) + '\n', 'utf8');
}

// ═════════════════════════ MAIN ══════════════════════════════════════════════
function main() {
  console.log('Building OKF bundle →', OUT);
  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(OUT, { recursive: true });

  buildClusters();
  buildAxioms();
  buildRules();
  buildRegistry();
  buildGlossary();
  buildAttackPaths();
  buildMappings();
  buildControlFunctions();
  buildControlClusters();
  buildEffectivenessModel();
  buildIndicators();

  writeIndexes();
  writeRoot();
  writeManifest();

  console.log(`\nWrote ${docCount} concept documents + manifest.json`);
  for (const [t, n] of [...typeCounts].sort()) console.log(`  ${t}: ${n}`);
  console.log(`Sections: ${topDirs().join(', ')}`);
}

main();
