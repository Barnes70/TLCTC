#!/usr/bin/env node
/*
 * build-site.js — One command from repo sources to a deploy-ready tlctc.net tree.
 *
 *   npm run site              build only (idempotent; prints what changed)
 *   npm run site:deploy       build, then upload changed files via deploy-changed.ps1
 *   node scripts/build-site.js --no-pdf --no-okf --site <dir>
 *
 * Pipeline (order matters; each step is skipped when nothing changed):
 *   1. mirror   documentation/{core,application,glossary}.md → site tree (read-only mirrors)
 *   2. pdfs     scripts/build-pdf.js for any paper whose .md is newer than its .pdf
 *   3. stable   copy PDFs under the site's stable names (tlctc-whitepaper.pdf, …)
 *   4. html     node html-build.js --no-pdf in the site tree (core, application, handbook)
 *   5. glossary python build_glossary_page.py + build_glossary_index.py; "Last updated"
 *               in the glossary page shell follows the .md header
 *   6. views    copy generated html back into documentation/ (gitignored local views)
 *   7. images   documentation/images/*.svg → site images/
 *   8. okf      repo okf/ → site okf/ (adds, updates, removes)
 *   9. figures  re-inline <svg> blocks in index.html from their source files
 *               (markers: <!-- INLINE-SVG src="…" … --> … <!-- /INLINE-SVG -->)
 *  10. sitemap  bump <lastmod> for every deployable file whose content changed
 *               since the last build; add okf entries for new files, drop removed ones
 *  11. dates    warn when a paper .md changed but its **Date:** header is stale
 *
 * State: <site>/.site-build-state.json (hashes of outputs after the last build).
 * Site dir: --site, $TLCTC_SITE_DIR, or ../web/tlctc relative to the repo.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync, spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const flag = (f) => args.includes(f);
const opt = (f, d) => { const i = args.indexOf(f); return i >= 0 ? args[i + 1] : d; };
const SITE = path.resolve(opt('--site', process.env.TLCTC_SITE_DIR || path.join(ROOT, '..', 'web', 'tlctc')));
const TODAY = new Date().toISOString().slice(0, 10);
const NO_PDF = flag('--no-pdf'), NO_OKF = flag('--no-okf'), DEPLOY = flag('--deploy');

if (!fs.existsSync(SITE)) { console.error(`site dir not found: ${SITE}`); process.exit(2); }
const STATE_FILE = path.join(SITE, '.site-build-state.json');
const state = fs.existsSync(STATE_FILE) ? JSON.parse(fs.readFileSync(STATE_FILE, 'utf8')) : { hashes: {} };
const prevHashes = state.hashes || {};
const changed = new Set();      // site-relative paths whose content changed in this build
const log = (s) => console.log(s);

const sha = (buf) => crypto.createHash('sha256').update(buf).digest('hex');
const fileHash = (p) => (fs.existsSync(p) ? sha(fs.readFileSync(p)) : null);
const rel = (p) => path.relative(SITE, p).split(path.sep).join('/');
function copyIfChanged(src, dst, label) {
  const before = fileHash(dst);
  const data = fs.readFileSync(src);
  if (before === sha(data)) return false;
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.writeFileSync(dst, data);
  changed.add(rel(dst));
  log(`  ${label || 'copy'}  ${rel(dst)}`);
  return true;
}
function run(cmd, cmdArgs, cwd, env) {
  const r = spawnSync(cmd, cmdArgs, { cwd, stdio: ['ignore', 'pipe', 'pipe'], env: { ...process.env, PYTHONIOENCODING: 'utf-8', ...env }, shell: process.platform === 'win32' && !/\.(exe|js)$/i.test(cmd) && cmd !== 'node' });
  if (r.status !== 0) { console.error(`  ! ${cmd} ${cmdArgs.join(' ')} failed:\n${r.stderr || r.stdout}`); process.exit(1); }
  return (r.stdout || '').toString();
}

// ───────────────────────── 1. mirrors ────────────────────────────────────────
log('1. mirrors');
const PAPERS = [
  { md: 'documentation/tlctc-v2.5-core.md', pdf: 'documentation/tlctc-v2.5-core.pdf', stablePdf: 'tlctc-whitepaper.pdf', html: 'tlctc-whitepaper.html' },
  { md: 'documentation/tlctc-v2.5-application.md', pdf: 'documentation/tlctc-v2.5-application.pdf', stablePdf: 'tlctc-application.pdf', html: 'tlctc-application.html' },
  { md: 'documentation/tlctc-glossary.md', pdf: 'documentation/tlctc-glossary.pdf', stablePdf: 'tlctc-glossary.pdf', html: 'tlctc-glossary.html' },
];
const mdChanged = {};
for (const p of PAPERS) mdChanged[p.md] = copyIfChanged(path.join(ROOT, p.md), path.join(SITE, path.basename(p.md)), 'mirror');

// ───────────────────────── 2. PDFs ───────────────────────────────────────────
log('2. pdfs' + (NO_PDF ? ' (skipped: --no-pdf)' : ''));
if (!NO_PDF) {
  for (const p of PAPERS) {
    const md = path.join(ROOT, p.md), pdf = path.join(ROOT, p.pdf);
    const stale = !fs.existsSync(pdf) || fs.statSync(md).mtimeMs > fs.statSync(pdf).mtimeMs || mdChanged[p.md];
    if (!stale) continue;
    log(`  build ${p.pdf}`);
    run('node', [path.join(ROOT, 'scripts/build-pdf.js'), md, pdf], ROOT);
  }
}

// ───────────────────────── 3. stable-name PDFs ───────────────────────────────
log('3. stable pdfs');
for (const p of PAPERS) if (fs.existsSync(path.join(ROOT, p.pdf))) copyIfChanged(path.join(ROOT, p.pdf), path.join(SITE, p.stablePdf), 'pdf  ');

// ───────────────────────── 4. html ───────────────────────────────────────────
log('4. html (html-build.js --no-pdf)');
{
  const before = {};
  for (const f of ['tlctc-whitepaper.html', 'tlctc-application.html', 'tlctc-v2.0-whitepaper.html']) before[f] = fileHash(path.join(SITE, f));
  const out = run('node', [path.join(SITE, 'html-build.js'), '--no-pdf'], SITE);
  for (const f of Object.keys(before)) if (fileHash(path.join(SITE, f)) !== before[f]) { changed.add(f); log(`  built ${f}`); }
  if (!/Done/.test(out)) log('  (html-build printed no "Done" line — check its output)');
}

// ───────────────────────── 5. glossary ───────────────────────────────────────
log('5. glossary (build_glossary_page.py, build_glossary_index.py)');
{
  const shell = path.join(SITE, 'tlctc-glossary.html');
  const beforeShell = fileHash(shell), beforeIdx = fileHash(path.join(SITE, 'glossary-index.html'));
  // "Last updated" in the hand-maintained shell follows the markdown header
  const md = fs.readFileSync(path.join(ROOT, 'documentation/tlctc-glossary.md'), 'utf8');
  const m = /\*Author:.*?\|\s*Last Updated:\s*(.+?)\*/.exec(md);
  if (m && fs.existsSync(shell)) {
    let s = fs.readFileSync(shell, 'utf8');
    const s2 = s.replace(/<time>Last updated: [^<]*<\/time>/, `<time>Last updated: ${m[1].trim()}</time>`);
    if (s2 !== s) { fs.writeFileSync(shell, s2, 'utf8'); log(`  shell "Last updated" → ${m[1].trim()}`); }
  }
  run('python', ['build_glossary_page.py'], SITE);
  run('python', ['build_glossary_index.py'], SITE);
  if (fileHash(shell) !== beforeShell) { changed.add('tlctc-glossary.html'); log('  built tlctc-glossary.html'); }
  if (fileHash(path.join(SITE, 'glossary-index.html')) !== beforeIdx) { changed.add('glossary-index.html'); log('  built glossary-index.html'); }
}

// ───────────────────────── 6. local views ────────────────────────────────────
log('6. local html views → documentation/');
for (const p of PAPERS) if (fs.existsSync(path.join(SITE, p.html))) fs.copyFileSync(path.join(SITE, p.html), path.join(ROOT, 'documentation', p.html));

// ───────────────────────── 7. images ─────────────────────────────────────────
log('7. images');
for (const f of fs.readdirSync(path.join(ROOT, 'documentation/images')).filter((x) => x.endsWith('.svg'))) {
  copyIfChanged(path.join(ROOT, 'documentation/images', f), path.join(SITE, 'images', f), 'image');
}

// ───────────────────────── 8. okf ────────────────────────────────────────────
log('8. okf' + (NO_OKF ? ' (skipped: --no-okf)' : ''));
const removedOkf = [];
if (!NO_OKF) {
  const src = path.join(ROOT, 'okf'), dst = path.join(SITE, 'okf');
  const walk = (d, base, acc) => { for (const n of fs.readdirSync(d)) { const p = path.join(d, n); if (fs.statSync(p).isDirectory()) walk(p, base, acc); else acc.push(path.relative(base, p).split(path.sep).join('/')); } return acc; };
  const srcFiles = walk(src, src, []), dstFiles = fs.existsSync(dst) ? walk(dst, dst, []) : [];
  for (const f of srcFiles) copyIfChanged(path.join(src, f), path.join(dst, f), 'okf  ');
  for (const f of dstFiles) if (!srcFiles.includes(f)) { fs.unlinkSync(path.join(dst, f)); removedOkf.push('okf/' + f); log(`  remove okf/${f} (gone from repo)`); }
}

// ───────────────────────── 9. inline figures in index.html ───────────────────
log('9. inline figures (index.html)');
{
  const idx = path.join(SITE, 'index.html');
  let t = fs.readFileSync(idx, 'utf8');
  const NL = t.includes('\r\n') ? '\r\n' : '\n';
  const re = /([ \t]*)<!-- INLINE-SVG ([^>]*?) -->[\s\S]*?<!-- \/INLINE-SVG -->/g;
  let n = 0;
  const t2 = t.replace(re, (whole, indent, attrs) => {
    const a = {}; for (const m of attrs.matchAll(/(\w+)="([^"]*)"/g)) a[m[1]] = m[2];
    const srcFile = path.join(SITE, a.src);
    if (!fs.existsSync(srcFile)) { console.error(`  ! INLINE-SVG source missing: ${a.src}`); process.exit(1); }
    let svg = fs.readFileSync(srcFile, 'utf8').replace(/^﻿/, '').replace(/<\?xml[^>]*\?>\s*/, '');
    const open = /<svg\b[^>]*>/.exec(svg); const close = svg.lastIndexOf('</svg>');
    if (!open || close < 0) { console.error(`  ! not an svg: ${a.src}`); process.exit(1); }
    const viewBox = /viewBox="([^"]+)"/.exec(open[0]); const style = /style="([^"]*)"/.exec(open[0]);
    const fontOnly = style ? (style[1].match(/font-family:[^;]+;?/) || [''])[0] : '';
    const body = svg.slice(open.index + open[0].length, close).trim();
    const rootAttrs = [`id="${a.id}"`, viewBox ? `viewBox="${viewBox[1]}"` : '', `class="${a.class || 'w-full h-auto'}"`, 'xmlns="http://www.w3.org/2000/svg"', 'role="img"',
      a.label ? `aria-label="${a.label}"` : '', fontOnly ? `style="${fontOnly}"` : ''].filter(Boolean).join(' ');
    const ground = a.ground && viewBox ? `${indent}    <rect width="${viewBox[1].split(/\s+/)[2]}" height="${viewBox[1].split(/\s+/)[3]}" rx="20" fill="${a.ground}"/>${NL}` : '';
    n++;
    return `${indent}<!-- INLINE-SVG ${attrs} -->${NL}${indent}<!-- generated by scripts/build-site.js from ${a.src}; do not hand-edit -->${NL}${indent}<svg ${rootAttrs}>${NL}${ground}${body.split(/\r?\n/).map((l) => indent + '    ' + l).join(NL)}${NL}${indent}</svg>${NL}${indent}<!-- /INLINE-SVG -->`;
  });
  if (t2 !== t) { fs.writeFileSync(idx, t2, 'utf8'); changed.add('index.html'); log(`  re-inlined ${n} figure(s); index.html changed`); }
  else log(`  ${n} figure(s) up to date`);
}

// ───────────────────────── 10. sitemap ───────────────────────────────────────
log('10. sitemap');
{
  const smPath = path.join(SITE, 'sitemap.xml');
  let sm = fs.readFileSync(smPath, 'utf8');
  const NL = sm.includes('\r\n') ? '\r\n' : '\n';
  const setLastmod = (urlPath, date) => {
    const loc = `<loc>https://www.tlctc.net/${urlPath}</loc>`;
    const i = sm.indexOf(loc); if (i === -1) return false;
    const j = sm.indexOf('<lastmod>', i), k = sm.indexOf('</lastmod>', j);
    if (j === -1 || k === -1 || j - i > 120) return false;
    const cur = sm.slice(j + 9, k); if (cur === date) return true;
    sm = sm.slice(0, j + 9) + date + sm.slice(k); return true;
  };
  // deployable outputs whose content changed → lastmod today (compare against last build state)
  const deployable = [...changed].filter((f) => /\.(html|pdf|md|json)$/.test(f) && !/^tlctc-(v2\.5-core|v2\.5-application|glossary)\.md$/.test(f));
  let bumped = 0, added = 0, dropped = 0;
  for (const f of deployable) {
    if (prevHashes[f] && prevHashes[f] === fileHash(path.join(SITE, f))) continue; // unchanged vs last build
    if (setLastmod(f, TODAY)) bumped++;
    else if (f.startsWith('okf/')) { // new okf page → append after the manifest.json entry
      const anchor = '<loc>https://www.tlctc.net/okf/manifest.json</loc>';
      const a = sm.indexOf(anchor); const e = sm.indexOf('</url>', a) + 6 + NL.length;
      sm = sm.slice(0, e) + `  <url>${NL}    <loc>https://www.tlctc.net/${f}</loc>${NL}    <lastmod>${TODAY}</lastmod>${NL}  </url>${NL}` + sm.slice(e); added++;
    }
  }
  for (const f of removedOkf) {
    const loc = `<loc>https://www.tlctc.net/${f}</loc>`; const i = sm.indexOf(loc); if (i === -1) continue;
    const s = sm.lastIndexOf('<url>', i), e = sm.indexOf('</url>', i) + 6;
    sm = sm.slice(0, s) + sm.slice(e).replace(/^\r?\n/, ''); dropped++;
  }
  const before = fileHash(smPath);
  fs.writeFileSync(smPath, sm, 'utf8');
  if (fileHash(smPath) !== before) changed.add('sitemap.xml');
  log(`  lastmod bumped: ${bumped}, okf entries added: ${added}, removed: ${dropped}`);
}

// ───────────────────────── 11. date sanity ───────────────────────────────────
log('11. dates');
for (const p of PAPERS.slice(0, 2)) {
  const md = fs.readFileSync(path.join(ROOT, p.md), 'utf8');
  const m = /^\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})/m.exec(md);
  if (m && mdChanged[p.md] && m[1] !== TODAY) log(`  ! ${p.md} changed but **Date:** is ${m[1]} — set it by hand if this is a content change`);
}

// ───────────────────────── state + summary ───────────────────────────────────
const hashes = {};
const collect = (dir, base) => { for (const n of fs.readdirSync(dir)) { const p = path.join(dir, n); if (fs.statSync(p).isDirectory()) { if (!['.git', 'node_modules', '__pycache__'].includes(n)) collect(p, base); } else hashes[rel(p)] = fileHash(p); } };
for (const top of ['okf', 'images']) if (fs.existsSync(path.join(SITE, top))) collect(path.join(SITE, top), SITE);
for (const f of fs.readdirSync(SITE)) { const p = path.join(SITE, f); if (fs.statSync(p).isFile() && /\.(html|pdf|xml|json)$/.test(f) && !f.startsWith('.')) hashes[f] = fileHash(p); }
fs.writeFileSync(STATE_FILE, JSON.stringify({ built_at: new Date().toISOString(), hashes }, null, 1));
log(`\nBuild done. ${changed.size} site file(s) changed:`);
for (const f of [...changed].sort()) log('  ' + f);

// ───────────────────────── optional deploy ───────────────────────────────────
if (DEPLOY) {
  log('\nDeploying changed files (deploy-changed.ps1 -Confirm) …');
  const r = spawnSync('powershell.exe', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', path.join(SITE, 'deploy-changed.ps1'), '-Confirm'], { cwd: SITE, stdio: 'inherit' });
  process.exit(r.status || 0);
}
