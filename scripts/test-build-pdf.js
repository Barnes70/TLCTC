'use strict';
// Tests for scripts/build-pdf.js: --footer flag and PDF title metadata.
const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync, spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const has = (cmd, args) => spawnSync(cmd, args, { encoding: 'utf8' }).status === 0;
const HAVE_PYPDF = spawnSync('python', ['-c', 'import pypdf']).status === 0;
const HAVE_PDFTOTEXT = has('pdftotext', ['-v']) || spawnSync('pdftotext', ['-v']).error === undefined;

function build(md, extra) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'build-pdf-'));
  const inP = path.join(dir, 'in.md');
  const outP = path.join(dir, 'out.pdf');
  fs.writeFileSync(inP, md);
  execFileSync(process.execPath, [path.join(ROOT, 'scripts/build-pdf.js'), inP, outP, ...extra], { stdio: 'pipe' });
  return outP;
}
const text = (pdf) => execFileSync('pdftotext', ['-enc', 'UTF-8', pdf, '-'], { encoding: 'utf8' });
const title = (pdf) => execFileSync('python', ['-c', 'import sys,pypdf;print(pypdf.PdfReader(sys.argv[1]).metadata.title)', pdf], { encoding: 'utf8', env: { ...process.env, PYTHONIOENCODING: 'utf-8' } }).trim();

test('custom footer replaces the default', { skip: !HAVE_PDFTOTEXT }, () => {
  const pdf = build('# Footer Probe\n\nBody text.\n', ['--footer', 'Layered Event Modelling probe']);
  const t = text(pdf);
  assert.match(t, /Layered Event Modelling probe/);
  assert.doesNotMatch(t, /Cause-Oriented Cyber Threat Taxonomy/);
});

test('default footer is unchanged', { skip: !HAVE_PDFTOTEXT }, () => {
  assert.match(text(build('# Default Probe\n\nBody.\n', [])), /A Cause-Oriented Cyber Threat Taxonomy/);
});

test('PDF title metadata is the first heading', { skip: !HAVE_PYPDF }, () => {
  assert.strictEqual(title(build('# A Title With Δt\n\nBody.\n', ['--footer', 'x'])), 'A Title With Δt');
});
