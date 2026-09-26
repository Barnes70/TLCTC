/*
 * path-stats.js — counting rules for TLCTC Layer-3 attack paths.
 *
 * Shared by the Path Atlas (tools/path-atlas.html) and the tools built on it. No DOM:
 * the same file runs in the browser (window.TLCTCPathStats) and in Node (module.exports),
 * where scripts/test-path-stats.js pins every rule below.
 *
 * A record is { file, source, metadata, path_sequence } — path_sequence as in
 * json-schemas/layer-3 (steps, parallel groups with mode:"parallel", unresolved items).
 *
 * Rules (tools/README.md, "Path Atlas"):
 *  - a transition is an ordered pair of ADJACENT positions; a parallel group fans out from
 *    the position before it and in to the position after it, with no transitions inside it
 *    ((#X + #Y) asserts no order)
 *  - unresolved items (?/…) never form transitions — adjacency across them is not evidenced
 *    and R-UNRES-3 keeps them out of statistics; every such break is counted in `dropped`
 *  - Δt of a transition = delta_t_to_next of the earlier position (a group's own value, else
 *    its first member's)
 *  - velocity classes are binned at 60 s / 60 min / 24 h — a TOOL convention: core §7 gives
 *    the classes by scale only
 *  - DRE refinements count to their parent too (Ii, If → I; Av, Ac → A)
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.TLCTCPathStats = factory();
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const CLUSTER_IDS = ['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10'];
  const DRE_CODES = ['C', 'I', 'Ii', 'If', 'A', 'Av', 'Ac'];
  const DRE_PARENT = { Ii: 'I', If: 'I', Av: 'A', Ac: 'A' };
  const VC_CLASSES = ['VC-1', 'VC-2', 'VC-3', 'VC-4'];

  const UNIT_SECONDS = { s: 1, sec: 1, m: 60, min: 60, h: 3600, hr: 3600, d: 86400, w: 604800, mo: 2592000, y: 31536000 };
  const QUALITATIVE_VC = { seconds: 'VC-4', minutes: 'VC-3', hours: 'VC-2', days: 'VC-1', weeks: 'VC-1', months: 'VC-1', years: 'VC-1' };

  function normCluster(v) {
    const m = /^#?0*(\d{1,2})$/.exec(String(v == null ? '' : v).trim());
    if (!m) return null;
    const n = +m[1];
    return n >= 1 && n <= 10 ? `#${n}` : null;
  }

  function vcOf(seconds) {
    if (seconds == null) return null;
    if (seconds < 60) return 'VC-4';
    if (seconds < 3600) return 'VC-3';
    if (seconds < 86400) return 'VC-2';
    return 'VC-1';
  }

  function parseDelta(raw) {
    const out = (kind, seconds, vc) => ({ raw, kind, seconds, vc });
    if (raw == null) return out('unknown', null, null);
    const s = String(raw).replace(/\s+/g, '').toLowerCase();
    if (s === 'instant') return out('instant', 0, 'VC-4');
    const q = /^~?(seconds|minutes|hours|days|weeks|months|years)$/.exec(s);
    if (q) return out('qualitative', null, QUALITATIVE_VC[q[1]]);
    const m = /^(~|<|≤|<=)?(\d+(?:\.\d+)?)(s|sec|min|m|hr|h|d|w|mo|y)$/.exec(s);
    if (!m) return out('unknown', null, null);
    const seconds = +m[2] * UNIT_SECONDS[m[3]];
    const kind = m[1] === '~' ? 'approx' : m[1] ? 'upper' : 'exact';
    return out(kind, seconds, vcOf(seconds));
  }

  function formatSeconds(s) {
    if (s == null) return '—';
    const f = (x) => String(Math.round(x * 10) / 10);
    if (s < 60) return `${f(s)}s`;
    if (s < 3600) return `${f(s / 60)}m`;
    if (s < 86400) return `${f(s / 3600)}h`;
    return `${f(s / 86400)}d`;
  }

  function incidentKey(record) {
    const id = record && record.metadata && record.metadata.incident_id;
    return id ? String(id).replace(/-AP\d+$/i, '') : record.file;
  }

  // Positions: { kind: 'steps' | 'unresolved', steps, dt }. A step whose cluster is not
  // #1–#10, and a group with no classified member, are not classified: they break the chain.
  function positions(record) {
    const seq = (record && Array.isArray(record.path_sequence)) ? record.path_sequence : [];
    return seq.map((item) => {
      if (!item || item.status === 'unresolved') return { kind: 'unresolved', steps: [], dt: item && item.delta_t_to_next };
      if (Array.isArray(item.steps)) {
        const steps = item.steps.filter((s) => normCluster(s.cluster));
        const memberDt = item.steps.map((s) => s.delta_t_to_next).find((d) => d != null);
        const dt = item.delta_t_to_next != null ? item.delta_t_to_next : memberDt;
        return steps.length ? { kind: 'steps', steps, dt } : { kind: 'unresolved', steps: [], dt };
      }
      return normCluster(item.cluster) ? { kind: 'steps', steps: [item], dt: item.delta_t_to_next } : { kind: 'unresolved', steps: [], dt: item.delta_t_to_next };
    });
  }

  function recordTransitions(record) {
    const pos = positions(record);
    const incident = incidentKey(record);
    const list = [];
    let dropped = 0;
    for (let i = 0; i + 1 < pos.length; i++) {
      const a = pos[i], b = pos[i + 1];
      if (a.kind === 'unresolved' || b.kind === 'unresolved') {
        dropped += Math.max(a.steps.length, 1) * Math.max(b.steps.length, 1);
        continue;
      }
      const dt = parseDelta(a.dt);
      for (const x of a.steps) for (const y of b.steps) {
        list.push({
          from: normCluster(x.cluster), to: normCluster(y.cluster), dt,
          file: record.file, incident, fromStep: x.step_id, toStep: y.step_id, fromNotes: x.notes || '',
        });
      }
    }
    return { list, dropped };
  }

  function entryExit(record) {
    const pos = positions(record);
    const side = (p) => (!p || p.kind === 'unresolved' ? null : p.steps.map((s) => ({ cluster: normCluster(s.cluster), step: s })));
    return { entry: side(pos[0]), exit: side(pos[pos.length - 1]) };
  }

  function dreCodes(outcomes) {
    const set = new Set();
    for (const o of Array.isArray(outcomes) ? outcomes : []) {
      if (typeof o !== 'string' || !DRE_CODES.includes(o)) continue;
      set.add(o);
      if (DRE_PARENT[o]) set.add(DRE_PARENT[o]);
    }
    return [...set].sort();
  }

  function classifiedSteps(record) {
    return positions(record).flatMap((p) => p.steps);
  }

  function filterRecords(records, { sources, confidence } = {}) {
    return records.filter((r) => (!sources || sources.includes(r.source))
      && (!confidence || confidence.includes((r.metadata && r.metadata.analyst_confidence) || 'unspecified')));
  }

  const bucket = () => ({ count: 0, items: [] });
  const byCluster = () => Object.fromEntries(CLUSTER_IDS.map((c) => [c, bucket()]).concat([['none', bucket()]]));

  function aggregate(records, { unit = 'transitions' } = {}) {
    const agg = {
      unit, records: records.length, steps: 0, total: 0, dropped: 0,
      cells: {}, entry: byCluster(), exit: byCluster(),
      dre: Object.fromEntries(CLUSTER_IDS.map((c) => [c, Object.fromEntries(DRE_CODES.map((d) => [d, bucket()]))])),
    };
    for (const r of records) {
      const { list, dropped } = recordTransitions(r);
      agg.dropped += dropped;
      for (const t of list) {
        const key = `${t.from}>${t.to}`;
        (agg.cells[key] = agg.cells[key] || { from: t.from, to: t.to, count: 0, items: [] }).items.push(t);
      }
      const ref = (step, cluster) => ({ file: r.file, incident: incidentKey(r), step_id: step && step.step_id, cluster, notes: (step && step.notes) || '' });
      const ee = entryExit(r);
      for (const [side, val] of [['entry', ee.entry], ['exit', ee.exit]]) {
        if (!val) { agg[side].none.count++; agg[side].none.items.push(ref(null, null)); continue; }
        for (const e of val) { agg[side][e.cluster].count++; agg[side][e.cluster].items.push(ref(e.step, e.cluster)); }
      }
      for (const s of classifiedSteps(r)) {
        agg.steps++;
        const c = normCluster(s.cluster);
        for (const code of dreCodes(s.outcomes)) { agg.dre[c][code].count++; agg.dre[c][code].items.push(ref(s, c)); }
      }
    }
    for (const cell of Object.values(agg.cells)) {
      cell.count = unit === 'incidents' ? new Set(cell.items.map((t) => t.incident)).size : cell.items.length;
      agg.total += cell.count;
    }
    return agg;
  }

  // Linear interpolation between order statistics (the common "type 7" definition).
  function quantile(values, q) {
    if (!values || !values.length) return null;
    const x = values.slice().sort((a, b) => a - b);
    const h = (x.length - 1) * q, lo = Math.floor(h);
    return lo + 1 < x.length ? x[lo] + (h - lo) * (x[lo + 1] - x[lo]) : x[lo];
  }

  function summarizeDeltas(items) {
    const numeric = items.map((t) => t.dt).filter((d) => d.seconds != null).map((d) => d.seconds).sort((a, b) => a - b);
    // Core §7.2 reads a Δt distribution at its fast tail (P10). Only measured values enter it:
    // an upper bound (<10m) says the transition took at most that long, not how long.
    const measured = items.map((t) => t.dt).filter((d) => d.kind === 'exact' || d.kind === 'approx' || d.kind === 'instant').map((d) => d.seconds);
    const mid = numeric.length >> 1;
    const median = !numeric.length ? null : numeric.length % 2 ? numeric[mid] : (numeric[mid - 1] + numeric[mid]) / 2;
    const vc = Object.fromEntries(VC_CLASSES.map((v) => [v, 0]));
    for (const t of items) if (t.dt.vc) vc[t.dt.vc]++;
    const kind = (k) => items.filter((t) => t.dt.kind === k).length;
    return {
      n: items.length, n_numeric: numeric.length,
      min_s: numeric.length ? numeric[0] : null, median_s: median, max_s: numeric.length ? numeric[numeric.length - 1] : null,
      p10_s: quantile(measured, 0.1), n_p10: measured.length,
      vc, n_upper: kind('upper'), n_qualitative: kind('qualitative'), n_unknown: kind('unknown'),
    };
  }

  const clusterNum = (c) => (c === 'none' ? 99 : +String(c).slice(1));
  function sortedCells(agg) {
    return Object.values(agg.cells).sort((a, b) => (b.count - a.count) || (clusterNum(a.from) - clusterNum(b.from)) || (clusterNum(a.to) - clusterNum(b.to)));
  }

  function toStatsJson(agg, { corpus_hash = null, unit = agg.unit, filters = {} } = {}) {
    const counts = (o) => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, v.count]));
    return {
      schema: 'tlctc-path-atlas-stats.v1',
      corpus_hash, unit, filters,
      velocity_binning: 'tool convention: <60s VC-4, <60min VC-3, <24h VC-2, else VC-1',
      records: agg.records, steps: agg.steps, total_transitions: agg.total, dropped_transitions: agg.dropped,
      transitions: sortedCells(agg).map((c) => ({ from: c.from, to: c.to, count: c.count, delta_t: summarizeDeltas(c.items) })),
      entry: counts(agg.entry), exit: counts(agg.exit),
      dre: Object.fromEntries(Object.entries(agg.dre).map(([c, codes]) => [c, counts(codes)])),
    };
  }

  function toTransitionsCsv(agg) {
    const rows = ['from,to,count,median_seconds,vc1,vc2,vc3,vc4'];
    for (const c of sortedCells(agg)) {
      const d = summarizeDeltas(c.items);
      rows.push([c.from, c.to, c.count, d.median_s == null ? '' : d.median_s, d.vc['VC-1'], d.vc['VC-2'], d.vc['VC-3'], d.vc['VC-4']].join(','));
    }
    return rows.join('\n') + '\n';
  }

  return {
    CLUSTER_IDS, DRE_CODES, VC_CLASSES,
    normCluster, vcOf, parseDelta, formatSeconds, quantile, incidentKey, positions, recordTransitions, entryExit,
    dreCodes, classifiedSteps, filterRecords, aggregate, summarizeDeltas, sortedCells, toStatsJson, toTransitionsCsv,
  };
}));
