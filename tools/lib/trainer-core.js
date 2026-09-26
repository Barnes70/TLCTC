/*
 * trainer-core.js — scenarios and agreement statistics for the Classification Trainer
 * (tools/classification-trainer.html). No DOM: runs in the browser (window.TLCTCTrainer)
 * and in Node, where scripts/test-trainer-core.js pins it.
 *
 * Scenarios are the classified steps of the bundled attack-path records. Their notes were
 * written as analyses, so they usually state the answer ("R-CRED: … always #4"). redact()
 * keeps only the sentences that describe what happened and drops every sentence that names
 * a cluster, cites a rule or axiom, or argues the classification. The full notes are shown
 * after the answer, as the explanation.
 *
 * The answer key is the record author's classification. Agreement with the key measures
 * agreement with that analyst, not ground truth; agreement between raters (Fleiss' kappa)
 * is the reproducibility measure the core paper calls for.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.TLCTCTrainer = factory();
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const CLUSTER_IDS = ['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10'];

  // A sentence matching any of these is dropped from a scenario.
  const LEAK_PATTERNS = [
    /#\s?\d{1,2}\b/,                                   // cluster numbers, "-> #1"
    /\bR-[A-Z]{2,}/,                                   // rule ids
    /\bAxiom/i, /\bDRE\b/, /\bFEC\b/, /\bSRE\b/, /\bTAE\b/, /\bTLCTC\b/, /\bVC-\d/,
    /generic vulnerab/i, /\bclusters?\b/i, /classif/i,
    /Credential Duality/i, /Trust Acceptance/i, /Abuse of Rights/i,
    /Abuse of Functions?|Exploiting (Server|Client)|Identity Theft|Man[- ]in[- ]the[- ]Middle|Flooding Attack|Physical Attack|Social Engineering|Supply[- ]Chain Attack/i,
    /server[- ]role|client[- ]role/i,
    // the reasoning vocabulary of #1 ("designed function, abused scope")
    /\b(as|by|is) designed\b|designed (platform )?(function|feature|capability)|designed, legitimate|not flawed|legitimate (function|feature)s?\b|scope is abused|authority scope/i,
    /\bdesigned\b[^.;]{0,40}\bfunction/i, /\bno flaw\b|\bnot a (flaw|bug|vulnerability)\b/i,
    // boundary / sphere notation and the analyst talking about the path itself
    /\|\||⇒|\[@|@[A-Z][\w-]*\s*(→|->)/, /\btransit\b/i, /\bBoundary:/, /\b(included|omit) (when|if)\b/i,
    /\bboundary annotation\b|\bintra-system\b|\bresponsibility sphere\b/i,
    /\b(this|that|prior|previous|next|separate|earlier|later|subsequent|undocumented) step\b/i,
  ];

  const splitSentences = (t) => String(t || '').replace(/\s+/g, ' ').trim().split(/(?<=[.!?])\s+(?=[A-Z("'\d])/).filter(Boolean);
  function redact(text) {
    return splitSentences(text).filter((s) => !LEAK_PATTERNS.some((re) => re.test(s))).join(' ').trim();
  }

  const normCluster = (v) => { const m = /^#?0*(\d{1,2})$/.exec(String(v == null ? '' : v).trim()); return m && +m[1] >= 1 && +m[1] <= 10 ? `#${+m[1]}` : null; };
  const titleOf = (file) => String(file).split('/').pop().replace(/\.json$/i, '').split('-').map((w) => (w ? w[0].toUpperCase() + w.slice(1) : w)).join(' ');

  function buildItems(records, { minChars = 80 } = {}) {
    const items = [];
    for (const r of records) {
      const slots = (r.path_sequence || []).map((it) => {
        if (!it || it.status === 'unresolved') return { unresolved: true, steps: [], notes: it && it.notes };
        const steps = Array.isArray(it.steps) ? it.steps : [it];
        return { unresolved: false, steps: steps.filter((s) => normCluster(s.cluster)) };
      });
      slots.forEach((slot, i) => {
        for (const s of slot.steps) {
          const text = redact(s.notes);
          if (text.length < minChars) continue;
          let prev = null;
          if (i > 0) {
            const p = slots[i - 1];
            prev = p.unresolved
              ? { cluster: '?', text: redact(p.notes) }
              : { cluster: p.steps.map((x) => normCluster(x.cluster)).join(' + '), text: p.steps.length ? redact(p.steps[0].notes) : '' };
          }
          items.push({
            id: `${r.file}#${s.step_id}`, file: r.file, step_id: s.step_id,
            incident: (r.metadata && r.metadata.incident_id) || null,
            title: titleOf(r.file), position: i + 1, of: slots.length,
            key: normCluster(s.cluster), text, notes: s.notes || '', prev,
          });
        }
      });
    }
    return items;
  }

  // FNV-1a — a stable, seedable ordering without a PRNG dependency
  function hash(str) {
    let h = 0x811c9dc5;
    for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
    return h >>> 0;
  }

  // Deterministic, stratified: round-robin across clusters (so rare clusters are present),
  // each cluster's items in seed order; the final order is shuffled by seed as well.
  function studySet(items, { seed, n }) {
    const byKey = {};
    for (const it of items) (byKey[it.key] = byKey[it.key] || []).push(it);
    for (const k of Object.keys(byKey)) byKey[k].sort((a, b) => hash(`${seed}|${a.id}`) - hash(`${seed}|${b.id}`));
    const picked = [];
    for (let round = 0; picked.length < n; round++) {
      let any = false;
      for (const k of CLUSTER_IDS) {
        if (picked.length >= n) break;
        if (byKey[k] && byKey[k][round]) { picked.push(byKey[k][round]); any = true; }
      }
      if (!any) break;
    }
    return picked.sort((a, b) => hash(`${seed}|order|${a.id}`) - hash(`${seed}|order|${b.id}`));
  }

  const studyId = ({ seed, n, corpus_hash }) => `${seed}-${n}-${String(corpus_hash || '').slice(0, 8)}`;

  // Balanced practice draw: a uniformly random cluster, then a random item of it.
  function pickBalanced(items, rand = Math.random, avoid = new Set()) {
    const byKey = {};
    for (const it of items) if (!avoid.has(it.id)) (byKey[it.key] = byKey[it.key] || []).push(it);
    const keys = Object.keys(byKey);
    if (!keys.length) return items.length ? items[Math.floor(rand() * items.length)] : null;
    const pool = byKey[keys[Math.floor(rand() * keys.length)]];
    return pool[Math.floor(rand() * pool.length)];
  }

  // Fleiss' kappa. table[i][j] = raters who put item i in category j; every row sums to n.
  function fleissKappa(table) {
    const N = table.length;
    if (!N) return { kappa: null, p_bar: null, p_e: null, per_category: [] };
    const n = table[0].reduce((a, b) => a + b, 0);
    const k = table[0].length;
    const Pi = table.map((row) => (row.reduce((a, x) => a + x * x, 0) - n) / (n * (n - 1)));
    const pBar = Pi.reduce((a, b) => a + b, 0) / N;
    const pj = Array.from({ length: k }, (_, j) => table.reduce((a, row) => a + row[j], 0) / (N * n));
    const pE = pj.reduce((a, p) => a + p * p, 0);
    const kappa = pE >= 1 ? null : (pBar - pE) / (1 - pE);
    const per_category = pj.map((p, j) => ({
      p,
      kappa: p === 0 || p === 1 ? null : 1 - table.reduce((a, row) => a + row[j] * (n - row[j]), 0) / (N * n * (n - 1) * p * (1 - p)),
    }));
    return { kappa, p_bar: pBar, p_e: pE, per_item: Pi, per_category };
  }

  function cohenKappa(a, b) {
    const N = a.length;
    if (!N) return null;
    const cats = [...new Set(a.concat(b))];
    const po = a.filter((x, i) => x === b[i]).length / N;
    const pe = cats.reduce((s, c) => s + (a.filter((x) => x === c).length / N) * (b.filter((x) => x === c).length / N), 0);
    return pe >= 1 ? null : (po - pe) / (1 - pe);
  }

  // Landis & Koch (1977) — a convention for reading kappa, not a test
  function landisKoch(k) {
    if (k == null) return 'undefined';
    if (k < 0) return 'poor';
    if (k <= 0.2) return 'slight';
    if (k <= 0.4) return 'fair';
    if (k <= 0.6) return 'moderate';
    if (k <= 0.8) return 'substantial';
    return 'almost perfect';
  }

  const ruleIdsIn = (text) => [...new Set(String(text || '').match(/\bR-[A-Z]+(?:-\d+)?\b/g) || [])];

  // Pool rating sheets of one study. Only items every accepted rater answered enter the
  // statistics, so the table is complete (Fleiss requires the same raters per item).
  function analyzeSheets(sheets, items) {
    const valid = sheets.filter((s) => s && s.schema === 'tlctc-rating-sheet.v1' && Array.isArray(s.answers));
    if (!valid.length) return null;
    const counts = {};
    for (const s of valid) counts[s.study_id] = (counts[s.study_id] || 0) + 1;
    const study = Object.keys(counts).sort((a, b) => counts[b] - counts[a])[0];
    const accepted = valid.filter((s) => s.study_id === study);
    const rejected = valid.filter((s) => s.study_id !== study).map((s) => ({ rater: s.rater, study_id: s.study_id }));
    const keyOf = Object.fromEntries(items.map((it) => [it.id, it]));
    const answerMaps = accepted.map((s) => Object.fromEntries(s.answers.filter((a) => normCluster(a.answer)).map((a) => [a.item, normCluster(a.answer)])));
    const ids = Object.keys(answerMaps[0]).filter((id) => answerMaps.every((m) => m[id]));
    const table = ids.map((id) => CLUSTER_IDS.map((c) => answerMaps.filter((m) => m[id] === c).length));
    const fleiss = accepted.length >= 2 && ids.length ? fleissKappa(table) : null;
    const n = accepted.length;
    const itemRows = ids.map((id, i) => {
      const row = table[i];
      const max = Math.max(...row);
      return {
        id, key: keyOf[id] ? keyOf[id].key : null, item: keyOf[id] || null,
        counts: Object.fromEntries(CLUSTER_IDS.map((c, j) => [c, row[j]]).filter(([, v]) => v)),
        agreement: n >= 2 ? (row.reduce((a, x) => a + x * x, 0) - n) / (n * (n - 1)) : null,
        majority: CLUSTER_IDS.filter((c, j) => row[j] === max),
      };
    }).sort((a, b) => (a.agreement == null ? 0 : a.agreement) - (b.agreement == null ? 0 : b.agreement));
    const keyed = ids.filter((id) => keyOf[id]);
    const raters = accepted.map((s, r) => {
      const ans = keyed.map((id) => answerMaps[r][id]);
      const key = keyed.map((id) => keyOf[id].key);
      return {
        rater: s.rater || `rater ${r + 1}`, answered: s.answers.length,
        accuracy: keyed.length ? ans.filter((a, i) => a === key[i]).length / keyed.length : null,
        cohen_vs_key: cohenKappa(ans, key),
      };
    });
    const confusion = Object.fromEntries(CLUSTER_IDS.map((k) => [k, Object.fromEntries(CLUSTER_IDS.map((a) => [a, 0]))]));
    for (const id of keyed) for (const m of answerMaps) confusion[keyOf[id].key][m[id]]++;
    return {
      study_id: study, raters, rejected, items: itemRows, fleiss, confusion,
      unknown_items: ids.length - keyed.length, complete_items: ids.length,
    };
  }

  return {
    CLUSTER_IDS, LEAK_PATTERNS, redact, buildItems, hash, studySet, studyId, pickBalanced,
    fleissKappa, cohenKappa, landisKoch, ruleIdsIn, analyzeSheets, titleOf,
  };
}));
