// Check that where the site states a cluster's canonical wording, it states it
// verbatim.
//
// Blogs are free to NAME a cluster ("#3 Exploiting Client") and free to GLOSS it
// for their domain ("targeting infotainment systems"). What they must not do is
// restate a definition or generic vulnerability in their own words, because a
// paraphrase is accurate on the day it is written and silently decays afterwards.
// That is how "#8 … facilities" and "#2 … source code implementation flaws"
// survived on the site for versions after the framework moved.
//
// The check is deliberately narrow. It only fires where a page is clearly trying
// to state canon — a near-match to a dictionary string — and reports how it
// differs. Pages that merely name clusters are untouched.
//
// Usage: node scripts/validate-site-definitions.js [--site <dir>] [--verbose]
// Exit 1 if any near-match is not verbatim.

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const argv = process.argv.slice(2);
const opt = (flag, dflt) => {
  const i = argv.indexOf(flag);
  return i >= 0 && argv[i + 1] ? argv[i + 1] : dflt;
};
const VERBOSE = argv.includes('--verbose');
const SITE = path.resolve(opt('--site', process.env.TLCTC_SITE_DIR || path.join(ROOT, '..', 'web', 'tlctc')));

const dict = require(path.join(ROOT, 'json-schemas/layer-1/tlctc-framework.v2.5.json'));

// The strings the dictionary owns. Per feedback_cluster_definition_fields these
// are never paraphrased: definition, generic vulnerability, attacker's view.
const CANON = [];
for (const [id, c] of Object.entries(dict.clusters)) {
  for (const field of ['definition', 'generic_vulnerability', 'attackers_view']) {
    if (typeof c[field] === 'string' && c[field].length > 30) {
      CANON.push({ id, field, text: c[field] });
    }
  }
}

if (!fs.existsSync(SITE)) {
  console.error(`site dir not found: ${SITE}`);
  process.exit(2);
}

const strip = (h) => h
  .replace(/<script[\s\S]*?<\/script>/gi, ' ')
  .replace(/<style[\s\S]*?<\/style>/gi, ' ')
  .replace(/<[^>]+>/g, ' ')
  .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/&quot;/g, '"').replace(/&#39;|&rsquo;|&apos;/g, "'")
  .replace(/&nbsp;/g, ' ').replace(/&[a-z]+;/gi, ' ')
  .replace(/\s+/g, ' ');

// Normalise for comparison: case, curly quotes, hyphen styles, trailing period.
const norm = (s) => s.toLowerCase()
  .replace(/[‘’]/g, "'")
  .replace(/[“”]/g, '"')
  .replace(/[‐-―]/g, '-')
  .replace(/[^a-z0-9'"/+#.\- ]/g, ' ')
  .replace(/\s+/g, ' ')
  .replace(/\.$/, '')
  .trim();

// Content words carry the meaning; shared rare words are what make two strings
// "the same claim, worded differently".
const STOP = new Set(('the a an of to in and or is are it its by for with that this which within into ' +
  'be can not no as at on from any their there these those any').split(' '));
const words = (s) => norm(s).split(' ').filter((w) => w.length > 3 && !STOP.has(w));

function overlap(a, b) {
  const A = new Set(words(a)), B = new Set(words(b));
  if (!A.size || !B.size) return 0;
  let hit = 0;
  for (const w of A) if (B.has(w)) hit++;
  return hit / Math.min(A.size, B.size);
}

// Only look where a page CLAIMS to be stating canon. An inline gloss — "#2
// Exploiting Server, which targets flaws on the server side" — is legitimate and
// must not be flagged; a labelled field is the page asserting the framework's own
// wording, and that is what has to match.
const LABEL = /\b(Definition|Generic Vulnerability|Generic vulnerability|Attacker'?s? View|Attacker'?s? view)\s*[:–-]\s*/g;

function labelledClaims(text) {
  const out = [];
  LABEL.lastIndex = 0;
  for (let m = LABEL.exec(text); m; m = LABEL.exec(text)) {
    const after = text.slice(m.index + m[0].length, m.index + m[0].length + 400);
    // the claim runs to the end of the sentence, or to the next field label
    const end = after.search(/(?:\.\s)|(?:\b(?:Definition|Generic Vulnerability|Attacker'?s? View|Scope|Developer'?s? View|Boundary Test)\b\s*[:–-])/);
    out.push({ field: m[1].toLowerCase(), text: (end > 0 ? after.slice(0, end + 1) : after).trim() });
  }
  return out;
}

function bestClaim(claims, canon) {
  let best = { score: 0, text: '' };
  for (const c of claims) {
    if (c.text.length < canon.length * 0.4 || c.text.length > canon.length * 2.2) continue;
    const s = overlap(canon, c.text);
    if (s > best.score) best = { score: s, text: c.text };
  }
  return best;
}

// Historical artifacts: superseded paper snapshots are records of what was
// published then, and must not be "corrected" (provenance rule).
const ARCHIVED = /^(TLCTCWhitePaperVersion|tlctc-v[12]\.|index-new|index\d|unused)/i;

const files = fs.readdirSync(SITE).filter((f) => f.endsWith('.html'));
let scanned = 0, verbatim = 0;
const problems = [];

let skipped = 0;
for (const f of files) {
  if (ARCHIVED.test(f)) { skipped++; continue; }
  const text = strip(fs.readFileSync(path.join(SITE, f), 'utf8'));
  if (!/#\d/.test(text)) continue;
  const claims = labelledClaims(text);
  if (!claims.length) continue;
  scanned++;
  for (const c of CANON) {
    if (text.includes(c.text)) { verbatim++; continue; }      // quoted correctly
    const hit = bestClaim(claims, c.text);
    if (hit.score < 0.75) continue;                            // not attempting this string
    if (norm(hit.text) === norm(c.text)) { verbatim++; continue; } // punctuation-only
    problems.push({ file: f, id: c.id, field: c.field, found: hit.text, canon: c.text, score: hit.score });
  }
}

problems.sort((a, b) => (a.file === b.file ? b.score - a.score : a.file.localeCompare(b.file)));
let last = '';
for (const p of problems) {
  if (p.file !== last) { console.log(`\n${p.file}`); last = p.file; }
  console.log(`  ${p.id} ${p.field}  (${Math.round(p.score * 100)}% match)`);
  console.log(`     page:  ${p.found.slice(0, 150)}`);
  console.log(`     canon: ${p.canon}`);
}

console.log(`\nSite definition check: ${scanned} page(s) scanned, ${verbatim} canonical string(s) quoted verbatim, ${problems.length} paraphrased.`);
if (problems.length) {
  console.log('\nA page may name a cluster and gloss it for its domain. Where it states the');
  console.log('definition, generic vulnerability or attacker\'s view, the wording is the');
  console.log("dictionary's — paraphrases go stale silently. Quote it, or rewrite the line so");
  console.log('it is plainly a gloss rather than a restatement.');
  process.exit(1);
}
if (VERBOSE) console.log('VALID — every canonical restatement on the site matches the dictionary.');
