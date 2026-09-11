// Cross-check the human-readable attack-path notation in metadata.notes against
// the machine-readable path_sequence of the same record.
//
// The Layer 3 schema validates each step in isolation. It cannot notice that a
// record's prose notation says one thing and its step data says another, which is
// exactly how several DRE tags ended up on the wrong step: in some records the
// notation was right and `outcomes` was wrong, in others the reverse.
//
// This checker compares the two on the spine that matters — the ordered sequence
// of clusters and the Data Risk Events attached to each. Velocity, boundary
// operators and responsibility spheres are deliberately NOT compared: they are
// frequently abbreviated in prose summaries and are checked elsewhere.
//
// Usage: node scripts/validate-path-notation.js [--verbose]
// Exit 1 on any mismatch, 0 otherwise.

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DIRS = ['attack-paths', 'json-schemas/layer-3/examples'];
const VERBOSE = process.argv.includes('--verbose');

// ---------------------------------------------------------------- notation side

// Where a record introduces its notation, in order of authority. A record may also
// quote a VARIANT path in passing ("Collateral infections follow a pure supply
// chain path: …"), which a bare "path:" would match, so the tiers are tried
// strongest-first and only one tier is ever used.
//
// A lead-in may carry a qualifier — "Attack path (direct):", "Attack path (Phase
// 2):" — and a record that splits its path into phases states each separately.
// Within the winning tier every match is concatenated in document order, which is
// what makes the phase-split records line up with their step sequence.
const LEAD_IN_TIERS = [
  /attack path(?:\s*\([^)]*\))?\s*:\s*/gi,
  /(?:compact notation|compact path|textual equivalent)(?:\s*\([^)]*\))?\s*:\s*/gi,
  /(?:notation|path)(?:\s*\([^)]*\))?\s*:\s*/gi,
];

// The notation alphabet. Anything outside it means prose has resumed.
const TOKENS = [
  ['dre', /^\+\s*\[DRE:\s*([^\]]*)\]/],       // must be tried before 'parallel'
  ['cluster', /^#(\d{1,2})(?:\.\d+)?/],
  ['unresolved', /^(\?|…|\.\.\.)/],
  ['parallel', /^\+/],
  ['open', /^\(/],
  ['close', /^\)/],
  ['boundary', /^\|\|[^|]*\|\|/],             // ||[context][@a→@b]||
  ['intra', /^\|\[[^\]]*\]\[[^\]]*\]\|/],     // |[type][@a→@b]|
  ['velocity', /^(?:→|->|—>)?\s*\[[^\]]*\]/], // [Δt=…] or [~3d]
  ['arrow', /^(?:→|->|—>|⇒)/],
];

// Some records deliberately abbreviate the tail of a long or looping path rather
// than enumerating it — a worm's recursion, for example, is marked once. Where the
// notation says so explicitly, only the common prefix is compared.
const ABBREVIATION = /\[RECURSIVE\]|\[\.\.\.\]|…\s*\.?\s*$/;

function extractNotation(notes) {
  if (!notes) return null;
  for (const tier of LEAD_IN_TIERS) {
    tier.lastIndex = 0;
    const parts = [];
    for (let m = tier.exec(notes); m; m = tier.exec(notes)) {
      const seq = parseFrom(notes.slice(m.index + m[0].length));
      if (seq) parts.push(seq);
    }
    if (!parts.length) continue;
    const joined = [].concat(...parts);
    joined.abbreviated = parts.some((p) => p.abbreviated);
    joined.segments = parts.length;
    return joined;
  }
  return null;
}

function parseFrom(text) {
  let s = text;
  const abbreviated = ABBREVIATION.test(s.slice(0, 2000));

  const seq = [];        // positions: { clusters:[], dre:[] }
  let depth = 0;
  let pending = null;    // current position being built
  const flush = () => { if (pending) { seq.push(pending); pending = null; } };

  while (s.length) {
    const ws = /^\s+/.exec(s);
    if (ws) { s = s.slice(ws[0].length); continue; }

    let matched = false;
    for (const [kind, re] of TOKENS) {
      const t = re.exec(s);
      if (!t) continue;
      matched = true;
      s = s.slice(t[0].length);

      if (kind === 'cluster') {
        if (depth === 0) { flush(); pending = { clusters: [], dre: [] }; }
        else if (!pending) pending = { clusters: [], dre: [] };
        pending.clusters.push('#' + t[1]);
      } else if (kind === 'unresolved') {
        flush();
        pending = { clusters: ['?'], dre: [] };
        flush();
      } else if (kind === 'dre') {
        const codes = t[1].split(',').map((x) => x.trim()).filter(Boolean);
        if (pending) pending.dre.push(...codes);
        else seq.push({ clusters: ['(orphan DRE)'], dre: codes });
      } else if (kind === 'open') {
        flush(); depth++; pending = { clusters: [], dre: [] };
      } else if (kind === 'close') {
        depth = Math.max(0, depth - 1);
      }
      break;
    }
    if (!matched) break; // prose resumed
  }
  flush();
  if (!seq.length) return null;
  seq.abbreviated = abbreviated;
  return seq;
}

// ------------------------------------------------------------- step-data side

function assembleFromSteps(items) {
  const seq = [];
  for (const it of items || []) {
    if (!it || typeof it !== 'object') continue;
    const nested = it.steps || it.parallel_steps;
    if (Array.isArray(nested)) {
      const pos = { clusters: [], dre: [...(it.outcomes || [])] };
      for (const s of nested) {
        if (s.cluster) pos.clusters.push(s.cluster);
        if (s.outcomes) pos.dre.push(...s.outcomes);
      }
      seq.push(pos);
      continue;
    }
    if (it.status === 'unresolved' || (!it.cluster && it.unresolved_type)) {
      seq.push({ clusters: ['?'], dre: [] });
      continue;
    }
    if (!it.cluster) continue;
    seq.push({ clusters: [it.cluster], dre: [...(it.outcomes || [])] });
  }
  return seq;
}

// ------------------------------------------------------------------- compare

const fmt = (p) =>
  (p.clusters.length > 1 ? `(${p.clusters.join(' + ')})` : p.clusters[0]) +
  (p.dre.length ? ` + [DRE: ${[...p.dre].sort().join(', ')}]` : '');

// The DRE refinement tree (core §7.6): a parent code stays legal wherever the
// refinement is unknown, so "A" against "Av" is a difference in precision, not a
// contradiction. Those are reported separately and do not fail the check.
const DRE_PARENT = { Ii: 'I', If: 'I', Av: 'A', Ac: 'A' };
const root = (c) => DRE_PARENT[c] || c;

function dreRelation(a, b) {
  const x = [...a].sort(), y = [...b].sort();
  if (x.join(',') === y.join(',')) return 'equal';
  if (x.length === y.length && x.every((c, i) => root(c) === root(y[i]))) return 'imprecise';
  return 'differ';
}

function compare(notation, steps) {
  const problems = [];
  const notes = [];
  const n = Math.max(notation.length, steps.length);
  for (let i = 0; i < n; i++) {
    const a = notation[i];
    const b = steps[i];
    if (!a) {
      if (notation.abbreviated) continue; // notation stops on purpose (e.g. [RECURSIVE])
      problems.push(`  position ${i + 1}: notation ends, steps have ${fmt(b)}`);
      continue;
    }
    if (!b) { problems.push(`  position ${i + 1}: steps end, notation has ${fmt(a)}`); continue; }
    if (a.clusters.includes('?') || b.clusters.includes('?')) continue; // unresolved: don't compare

    if (a.clusters.join('|') !== b.clusters.join('|')) {
      problems.push(`  position ${i + 1}: notation ${fmt(a)}   !=   steps ${fmt(b)}`);
      continue;
    }
    const rel = dreRelation(a.dre, b.dre);
    if (rel === 'differ') problems.push(`  position ${i + 1}: notation ${fmt(a)}   !=   steps ${fmt(b)}`);
    else if (rel === 'imprecise') notes.push(`  position ${i + 1}: ${fmt(a)} vs ${fmt(b)} — same DRE family, different precision`);
  }
  return { problems, notes };
}

// ---------------------------------------------------------------------- main

const files = [];
for (const d of DIRS) {
  const abs = path.join(ROOT, d);
  if (!fs.existsSync(abs)) continue;
  for (const f of fs.readdirSync(abs)) if (f.endsWith('.json')) files.push(path.join(abs, f));
}

let checked = 0, skipped = 0, bad = 0, imprecise = 0;
const report = [];

for (const file of files) {
  let j;
  try { j = JSON.parse(fs.readFileSync(file, 'utf8')); } catch (e) {
    report.push(`${path.basename(file)}: PARSE ERROR — ${e.message}`); bad++; continue;
  }
  if (!j.path_sequence) continue;

  const notation = extractNotation(j.metadata && j.metadata.notes);
  if (!notation) { skipped++; if (VERBOSE) report.push(`${path.basename(file)}: no notation in metadata.notes — skipped`); continue; }

  const steps = assembleFromSteps(j.path_sequence);
  const { problems, notes } = compare(notation, steps);
  checked++;
  if (problems.length) {
    bad++;
    report.push(`${path.basename(file)}:\n${problems.concat(notes).join('\n')}`);
  } else if (notes.length) {
    imprecise++;
    if (VERBOSE) report.push(`${path.basename(file)} (precision only):\n${notes.join('\n')}`);
  } else if (VERBOSE) {
    report.push(`${path.basename(file)}: OK (${steps.length} positions)`);
  }
}

if (report.length) console.log(report.join('\n\n') + '\n');
console.log(`Notation cross-check: ${checked} record(s) compared, ${skipped} without a notation, ${bad} mismatching, ${imprecise} differing only in DRE precision.`);
if (bad) {
  console.log('\nA mismatch means the prose notation and path_sequence disagree. Fix whichever is wrong —');
  console.log('the schema cannot catch this, because each step validates fine in isolation.');
  process.exit(1);
}
console.log('VALID — every notation agrees with its path_sequence.');
