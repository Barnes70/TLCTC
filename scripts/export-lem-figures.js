#!/usr/bin/env node
/*
 * export-lem-figures.js — Export the two inline figures of the Layered Event
 * Modelling web page as standalone, print-safe SVGs for the PDF edition.
 * The page is the single source of the figures; re-run after editing them.
 *
 * Usage: node scripts/export-lem-figures.js <path/to/tlctc-layered-event-modelling.html>
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const OUT = ['documentation/images/lem-five-structures.svg', 'documentation/images/lem-typed-incident.svg'];

// Light-theme values of the page's .lem-fig rules (tlctc-layered-event-modelling.html).
const STYLE = [
  '<style>',
  '  svg { color: #111111; font-family: Inter, "Segoe UI", Arial, sans-serif; }',
  '  .bx { fill: none; stroke: currentColor; stroke-opacity: 0.28; }',
  '  .hair { stroke: currentColor; stroke-opacity: 0.28; fill: none; }',
  '  .lbl { fill: currentColor; font-size: 11px; }',
  '  .mono { fill: #5f6368; font-family: Consolas, "JetBrains Mono", ui-monospace, monospace; font-size: 9.5px; letter-spacing: 0.14em; }',
  '  .mono.in { letter-spacing: 0.06em; }',
  '  .lane { fill: currentColor; fill-opacity: 0.035; stroke: none; }',
  '  .edge { stroke-opacity: 0.75; }',
  '  .dot { stroke-dasharray: 1.5 3; }',
  '  .dash { stroke-dasharray: 4 3; }',
  '  .ddot { stroke-dasharray: 7 3 1.5 3; }',
  '  .acc-bx { fill: none; stroke: #e5484d; stroke-opacity: 0.85; }',
  '  .acc-hair { stroke: #e5484d; stroke-opacity: 0.85; fill: none; }',
  '  .acc-txt { fill: #e5484d; }',
  '  .acc-fill { fill: #e5484d; }',
  '</style>',
].join('\n');

// HTML named entities are not XML: a standalone SVG must use numeric references.
const ENTITIES = { Delta: '&#916;', delta: '&#948;', mdash: '&#8212;', ndash: '&#8211;', rarr: '&#8594;', nbsp: '&#160;', le: '&#8804;', ge: '&#8805;', middot: '&#183;', hellip: '&#8230;', sect: '&#167;' };
const XML_ENTITIES = new Set(['amp', 'lt', 'gt', 'quot', 'apos']);
function numeric(svg) {
  return svg.replace(/&([A-Za-z][A-Za-z0-9]*);/g, (m, name) => {
    if (XML_ENTITIES.has(name)) return m;
    if (!ENTITIES[name]) throw new Error('unknown entity ' + m);
    return ENTITIES[name];
  });
}

function exportFigures(html) {
  const svgs = html.match(/<svg class="lem-fig"[\s\S]*?<\/svg>/g) || [];
  if (svgs.length !== 2) throw new Error(`expected 2 figures, found ${svgs.length}`);
  return svgs.map((svg) => {
    const vb = /viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"/.exec(svg);
    if (!vb) throw new Error('figure without a 0-origin viewBox');
    const opened = svg.replace('<svg class="lem-fig" viewBox=', `<svg width="${vb[1]}" height="${vb[2]}" viewBox=`);
    if (opened === svg) throw new Error('figure <svg> tag not in the expected form');
    return numeric(opened.replace(/^(<svg[^>]*>)/, `$1\n${STYLE}`));
  });
}

module.exports = { exportFigures, STYLE };

if (require.main === module) {
  const page = process.argv[2];
  if (!page) { console.error('Usage: node scripts/export-lem-figures.js <page.html>'); process.exit(1); }
  const out = exportFigures(fs.readFileSync(page, 'utf8'));
  out.forEach((svg, i) => {
    const target = path.join(ROOT, OUT[i]);
    fs.writeFileSync(target, `<?xml version="1.0" encoding="UTF-8"?>\n${svg}\n`);
    console.log(`wrote ${OUT[i]}`);
  });
}
