#!/usr/bin/env node
// Rewrites the data embedded in an ATT&CK explorer page from the canonical mapping JSON.
// Usage: node scripts/sync-attack-explorer.js <page.html> [--check]
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const SOURCE = path.join(ROOT, 'mappings/mitre-attack-enterprise/tlctc-enterprise-attack.json');
const MARKER = 'let mappingData = [';

function toRow(e) {
  return {
    'MITRE Technique ID': e.techniqueId,
    'Name of MITRE Technique': e.techniqueName,
    'TLCTC Cluster ID (#)': e.tlctcMapping,
    'TLCTC Name': e.tlctcMappingName,
    'Argument for mapping one or more TLCTC clusters (paths)': e.mappingRationale,
    'MITRE Technique Description': e.techniqueDescription,
    'MITRE Tactics': e.tactics.join(', '),
    'MITRE Platforms': e.platforms.join(', '),
  };
}

// The end of the array literal, skipping brackets inside strings.
function arrayEnd(text, open) {
  let depth = 0;
  let inString = false;
  for (let i = open; i < text.length; i++) {
    const c = text[i];
    if (inString) {
      if (c === '\\') i++;
      else if (c === '"') inString = false;
    } else if (c === '"') inString = true;
    else if (c === '[') depth++;
    else if (c === ']' && --depth === 0) return i + 1;
  }
  throw new Error('unterminated mappingData array');
}

function main(argv) {
  const check = argv.includes('--check');
  const page = argv.find((a) => !a.startsWith('--'));
  if (!page) throw new Error('usage: sync-attack-explorer.js <page.html> [--check]');
  const text = fs.readFileSync(page, 'utf8');
  const at = text.indexOf(MARKER);
  if (at < 0) throw new Error(`${page}: no "${MARKER}"`);
  const open = at + MARKER.length - 1;
  const end = arrayEnd(text, open);
  const eol = text.includes('\r\n') ? '\r\n' : '\n';
  const rows = JSON.parse(fs.readFileSync(SOURCE, 'utf8')).mappings.map(toRow);
  const literal = JSON.stringify(rows, null, 2).replace(/\n/g, eol);
  const next = text.slice(0, open) + literal + text.slice(end);
  if (check) {
    if (next !== text) throw new Error(`${page}: embedded data differs from the mapping`);
    console.log(`${page}: in sync (${rows.length} rows)`);
    return;
  }
  fs.writeFileSync(page, next);
  console.log(`${page}: wrote ${rows.length} rows`);
}

main(process.argv.slice(2));
