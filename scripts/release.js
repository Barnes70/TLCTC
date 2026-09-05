#!/usr/bin/env node
/*
 * release.js — Everything a Zenodo deposit needs, in one command.
 *
 *   npm run release                       dry run: validate, print checksums of the COMMITTED PDFs
 *   npm run release -- --build            also rebuild the three PDFs first (they are then
 *                                         uncommitted; with --go they are committed for you)
 *   npm run release -- --go               act: retarget the tag, push it, refresh GitHub
 *                                         release assets, patch the Zenodo checklist
 *   options: --tag v2.5.0 (default: v<version> from the dictionary's tlctc_version + ".0")
 *            --build      rebuild PDFs (PDF output is not byte-deterministic, so this
 *                         always changes the checksums — only do it when sources changed)
 *            --no-assets  skip GitHub release asset upload
 *            --no-tag     skip tag retarget/push
 *
 * What --go does, in order:
 *   1. refuses on a dirty working tree (commit first — the tag must point at a commit)
 *   2. npm run validate
 *   3. with --build: rebuilds the PDFs and commits them ("docs: rebuild PDFs for <tag>")
 *   4. git tag -f <tag> HEAD && git push -f origin <tag>
 *   5. gh release upload <tag> tlctc-v2.5-core.pdf tlctc-framework.v2.5.json tlctc-cwe.json --clobber
 *   6. rewrites the checksum/size/tag lines in input4new/zenodo-v2.5-core-metadata.md
 *   7. prints the md5 / sha256 / size / pages the Zenodo form must show
 *
 * The tag retarget is a force-push of a public tag; that is why it needs --go.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execSync, spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const flag = (f) => args.includes(f);
const opt = (f, d) => { const i = args.indexOf(f); return i >= 0 ? args[i + 1] : d; };
const GO = flag('--go');
const fw = JSON.parse(fs.readFileSync(path.join(ROOT, 'json-schemas/layer-1/tlctc-framework.v2.5.json'), 'utf8'));
const TAG = opt('--tag', `v${fw.metadata.tlctc_version}.0`);
const sh = (cmd, opts = {}) => execSync(cmd, { cwd: ROOT, stdio: ['ignore', 'pipe', 'inherit'], ...opts }).toString().trim();
// No shell anywhere: node/git/gh are real executables; npm is bypassed by calling the scripts directly.
const run = (cmd, cmdArgs) => { const r = spawnSync(cmd, cmdArgs, { cwd: ROOT, stdio: 'inherit' }); if (r.status !== 0) { console.error(`! ${cmd} ${cmdArgs.join(' ')} failed`); process.exit(1); } };
const node = (script, ...a) => run(process.execPath, [path.join(ROOT, 'scripts', script), ...a]);
const dirty = () => sh('git status --porcelain').split('\n').filter((l) => l && !l.includes(' okf/')).join('\n');

const PDFS = {
  core: 'documentation/tlctc-v2.5-core.pdf',
  application: 'documentation/tlctc-v2.5-application.pdf',
  glossary: 'documentation/tlctc-glossary.pdf',
};
const ASSETS = ['documentation/tlctc-v2.5-core.pdf', 'json-schemas/layer-1/tlctc-framework.v2.5.json', 'mappings/mitre-cwe/tlctc-cwe.json'];

console.log(`release ${TAG}${GO ? '' : ' (dry run — add --go to act)'}`);

// 1. clean tree
const d0 = dirty();
if (d0) { console.error('! working tree is dirty; commit first:\n' + d0); if (GO) process.exit(1); }

// 2. validate
console.log('\n== validate');
node('validate-framework.js', 'json-schemas/layer-1/tlctc-framework.schema.json', 'json-schemas/layer-1/tlctc-framework.v2.5.json');
node('validate-attack-paths.js');
node('validate-consistency.js');
node('build-okf.js');
node('validate-okf.js', 'okf');

// 3. PDFs (opt-in: output is not byte-deterministic)
if (flag('--build')) {
  console.log('\n== build PDFs');
  for (const rel of Object.values(PDFS)) node('build-pdf.js', rel.replace(/\.pdf$/, '.md'), rel);
  const d1 = dirty();
  if (d1 && GO) {
    run('git', ['add', ...Object.values(PDFS)]);
    run('git', ['commit', '-q', '-m', `docs: rebuild PDFs for ${TAG}\n\nCo-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`]);
    run('git', ['push', 'origin', 'HEAD']);
    console.log('  PDFs committed and pushed');
  } else if (d1) {
    console.log('! PDFs rebuilt but not committed (dry run):\n' + d1);
  }
}

// checksums
console.log('\n== checksums');
const info = {};
for (const [k, rel] of Object.entries(PDFS)) {
  const buf = fs.readFileSync(path.join(ROOT, rel));
  info[k] = {
    rel, size: buf.length,
    md5: crypto.createHash('md5').update(buf).digest('hex'),
    sha256: crypto.createHash('sha256').update(buf).digest('hex'),
    pages: (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length,
  };
  console.log(`${k.padEnd(12)} ${info[k].size.toLocaleString('en-US').padStart(10)} B  ${info[k].pages} pp  md5 ${info[k].md5}\n${' '.repeat(13)}sha256 ${info[k].sha256}`);
}
const head = sh('git rev-parse --short HEAD');
const tagAt = (() => { try { return sh(`git rev-list -n 1 --abbrev-commit ${TAG}`, { stdio: ['ignore', 'pipe', 'ignore'] }); } catch { return '(none)'; } })();
console.log(`\nHEAD ${head}   tag ${TAG} currently at ${tagAt}`);

if (!GO) { console.log('\nDry run complete. Re-run with --go to retarget the tag, refresh assets, and patch the checklist.'); process.exit(0); }

// 4. tag
if (!flag('--no-tag')) {
  console.log(`\n== tag ${TAG} → ${head} (force) and push`);
  run('git', ['tag', '-f', TAG, 'HEAD']);
  run('git', ['push', '-f', 'origin', TAG]);
}

// 5. assets
if (!flag('--no-assets')) {
  console.log(`\n== GitHub release assets for ${TAG}`);
  const exists = spawnSync('gh', ['release', 'view', TAG], { cwd: ROOT, stdio: 'ignore' }).status === 0;
  if (!exists) run('gh', ['release', 'create', TAG, '--title', `TLCTC ${TAG}`, '--notes', `TLCTC ${fw.metadata.tlctc_version} — see documentation/tlctc-v2.5-core.md`, '--verify-tag']);
  run('gh', ['release', 'upload', TAG, ...ASSETS, '--clobber']);
}

// 6. checklist
const ck = path.join(ROOT, 'input4new/zenodo-v2.5-core-metadata.md');
if (fs.existsSync(ck)) {
  console.log('\n== patch Zenodo checklist');
  let t = fs.readFileSync(ck, 'utf8');
  const fmt = (n) => n.toLocaleString('en-US');
  const c = info.core, a = info.application;
  const subs = [
    [/\| \*\*UPLOAD THIS\*\* → `documentation\/tlctc-v2\.5-core\.pdf` \| `[0-9a-f]{32}` \| [\d,]+ B \(\d+ KB\) \| \d+ \|/, `| **UPLOAD THIS** → \`documentation/tlctc-v2.5-core.pdf\` | \`${c.md5}\` | ${fmt(c.size)} B (${Math.round(c.size / 1024)} KB) | ${c.pages} |`],
    [/\| NOT this → `documentation\/tlctc-v2\.5-application\.pdf` \| `[0-9a-f]{32}` \| [\d,]+ B \(\d+ KB\) \| \d+ \|/, `| NOT this → \`documentation/tlctc-v2.5-application.pdf\` | \`${a.md5}\` | ${fmt(a.size)} B (${Math.round(a.size / 1024)} KB) | ${a.pages} |`],
    [/compare the md5 Zenodo shows against `[0-9a-f]{32}`/, `compare the md5 Zenodo shows against \`${c.md5}\``],
    [/`[0-9a-f]{64}`\.\)/, `\`${c.sha256}\`.)`],
    ...(flag('--no-tag') ? [] : [[/currently points at `[0-9a-f]{7,}`; \*\*retarget to `[0-9a-f]{7,}` before depositing\*\*/, `points at \`${head}\` (retargeted by scripts/release.js); **nothing to do**`]]),
  ];
  let n = 0; for (const [re, rep] of subs) if (re.test(t)) { t = t.replace(re, rep); n++; }
  fs.writeFileSync(ck, t);
  console.log(`  ${n}/${subs.length} checklist lines updated (the file is gitignored; review it before depositing)`);
}

// 7. summary
console.log(`\nRelease ${TAG} prepared at ${head}.`);
console.log(`Zenodo form: upload ${PDFS.core}, verify md5 ${info.core.md5}, Version ${fw.metadata.tlctc_version}.`);
