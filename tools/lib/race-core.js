/*
 * race-core.js — the Δt Race: an attack path's transitions against a defender's detection and
 * containment times. No DOM: runs in the browser (window.TLCTCRace, after lib/path-stats.js) and
 * in Node, where scripts/test-race-core.js pins it.
 *
 * Canon (core §7.2, application §10.2–10.3):
 *   DCS_d = TTD_P90 / Δt   (detection)      DCS_c = TTC_P90 / Δt   (containment)
 *   < 1 the defender acts before the attacker completes the transition; = 1 marginal, no buffer;
 *   > 1 the step completes first. Only DCS_c < 1 stops a transition: DCS_d < 1 with DCS_c > 1
 *   means the step was seen but completed anyway. A Δt distribution is read at P10. Below about a
 *   minute (VC-4) detection and response are structurally too slow: prevention only.
 *   The mean-based MTTD / Δt is the special case where only means exist.
 *
 * Tool conventions (stated in the UI, not canon):
 *   - an edge X → Y is measured against the defender times of X, the step the attacker is leaving:
 *     detecting or containing X must happen before Y starts
 *   - VC binning is path-stats' (<60 s VC-4, <60 min VC-3, <24 h VC-2, else VC-1)
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./path-stats.js'));
  else root.TLCTCRace = factory(root.TLCTCPathStats);
}(typeof self !== 'undefined' ? self : this, function (S) {
  'use strict';

  // application §10.3 example targets — an organization sets its own from risk appetite
  const DEFAULT_TARGETS = { 'VC-1': 0.5, 'VC-2': 0.8, 'VC-3': 0.8, 'VC-4': null };
  const OUTCOMES = ['contained', 'seen', 'missed', 'prevention-only', 'no-data', 'unknown-dt'];

  function parseDuration(v) {
    if (v == null) return null;
    if (typeof v === 'number') return Number.isFinite(v) && v >= 0 ? v : null;
    const s = String(v).trim();
    if (!s) return null;
    if (/^\d+(\.\d+)?$/.test(s)) return +s;
    const iso = /^P(?:(\d+(?:\.\d+)?)W)?(?:(\d+(?:\.\d+)?)D)?(?:T(?:(\d+(?:\.\d+)?)H)?(?:(\d+(?:\.\d+)?)M)?(?:(\d+(?:\.\d+)?)S)?)?$/i.exec(s);
    if (iso && iso.slice(1).some((x) => x != null)) {
      const [, w, d, h, m, sec] = iso.map((x) => +(x || 0));
      return w * 604800 + d * 86400 + h * 3600 + m * 60 + sec;
    }
    const p = S.parseDelta(s);
    return p.kind === 'exact' || p.kind === 'approx' ? p.seconds : null;
  }

  function dcs(defenderSeconds, dtSeconds) {
    if (defenderSeconds == null || dtSeconds == null) return null;
    if (dtSeconds === 0) return Infinity;
    return defenderSeconds / dtSeconds;
  }

  function reading(score) {
    if (score == null) return null;
    if (Math.abs(score - 1) < 1e-9) return 'marginal';
    return score < 1 ? 'ahead' : 'behind';
  }

  function edgeDelta(rawDt, from, to, { dtSource, corpusCells, minSamples }) {
    const p = S.parseDelta(rawDt);
    const inc = { raw: p.raw == null ? null : String(p.raw), seconds: p.seconds, kind: p.kind, vc: p.vc, source: 'incident', bound: p.kind === 'upper', n: null };
    if (dtSource !== 'corpus' || !corpusCells) return inc;
    const cell = corpusCells[`${from}>${to}`];
    if (!cell) return inc;
    const sum = S.summarizeDeltas(cell.items);
    if (sum.n_p10 < minSamples) return { ...inc, corpus_n: sum.n_p10 };
    return { raw: `P10 of ${sum.n_p10}`, seconds: sum.p10_s, kind: 'p10', vc: S.vcOf(sum.p10_s), source: 'corpus-p10', bound: false, n: sum.n_p10, incident_raw: inc.raw };
  }

  function analyzePath(record, profile, { dtSource = 'incident', corpusCells = null, targets = DEFAULT_TARGETS, minSamples = 3 } = {}) {
    const pos = S.positions(record);
    const edges = [];
    let breaks = 0;
    for (let i = 0; i + 1 < pos.length; i++) {
      const a = pos[i], b = pos[i + 1];
      if (a.kind === 'unresolved' || b.kind === 'unresolved') {
        breaks += Math.max(a.steps.length, 1) * Math.max(b.steps.length, 1);
        continue;
      }
      for (const x of a.steps) for (const y of b.steps) {
        const from = S.normCluster(x.cluster), to = S.normCluster(y.cluster);
        const dt = edgeDelta(a.dt, from, to, { dtSource, corpusCells, minSamples });
        const prof = (profile && profile[from]) || {};
        const ttd = prof.ttd == null ? null : prof.ttd, ttc = prof.ttc == null ? null : prof.ttc;
        const dcsD = dcs(ttd, dt.seconds), dcsC = dcs(ttc, dt.seconds);
        let outcome;
        if (dt.seconds == null) outcome = 'unknown-dt';
        else if (dt.vc === 'VC-4') outcome = 'prevention-only';
        else if (ttd == null && ttc == null) outcome = 'no-data';
        else if (dcsC != null && dcsC < 1) outcome = 'contained';
        else if (dcsD != null && dcsD < 1) outcome = 'seen';
        else outcome = 'missed';
        const target = dt.vc && Object.prototype.hasOwnProperty.call(targets, dt.vc) ? targets[dt.vc] : null;
        const meets = (score) => (target == null || score == null ? null : score <= target + 1e-9);
        edges.push({
          index: edges.length, from, to, fromStep: x.step_id, toStep: y.step_id, fromNotes: x.notes || '',
          profile_cluster: from, dt, ttd, ttc,
          dcs_d: dcsD, dcs_c: dcsC, reading_d: reading(dcsD), reading_c: reading(dcsC), outcome,
          target, meets_target_d: meets(dcsD), meets_target_c: meets(dcsC),
          caveat: dt.bound ? `Δt is an upper bound (${dt.raw}): the real transition may have been faster, so the scores are at least these values.` : null,
        });
      }
    }
    const counts = Object.fromEntries(OUTCOMES.map((o) => [o, edges.filter((e) => e.outcome === o).length]));
    const first = edges.find((e) => e.outcome === 'contained');
    return { edges, breaks, summary: { counts, interception: first ? first.index : null, total: edges.length } };
  }

  // Control Matrix export → defender profile: DETECT cells carry TTD (dcs_mttd), RESPOND cells TTC (dcs_ttc).
  function profileFromControlMatrix(json, envId) {
    if (!json || !Array.isArray(json.environments) || !json.environments.length) return null;
    const env = (envId && json.environments.find((e) => e.id === envId)) || json.environments[0];
    const cells = env.cells || {};
    const profile = {};
    let found = 0;
    for (let n = 1; n <= 10; n++) {
      const ttd = parseDuration(cells[`${n}-DE`] && cells[`${n}-DE`].dcs_mttd);
      const ttc = parseDuration(cells[`${n}-RS`] && cells[`${n}-RS`].dcs_ttc);
      if (ttd != null) found++;
      if (ttc != null) found++;
      profile[`#${n}`] = { ttd, ttc };
    }
    return { profile, env: { id: env.id, name: env.name }, environments: json.environments.map((e) => ({ id: e.id, name: e.name })), found };
  }

  return { DEFAULT_TARGETS, OUTCOMES, parseDuration, dcs, reading, analyzePath, profileFromControlMatrix };
}));
