#!/usr/bin/env node
/*
 * check-lem-sync.js — Every text block of the Layered Event Modelling markdown
 * must appear in the web page's article. The markdown is canonical; the page
 * is hand-maintained (figures, layout), so this check keeps the prose in step.
 *
 * Usage: node scripts/check-lem-sync.js <page.html> [paper.md]
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { marked } = require('marked');
const puppeteer = require('puppeteer');

const norm = (s) => s.replace(/ /g, ' ').replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, ' ').trim();

(async () => {
  const [htmlPath, mdPath = path.join(__dirname, '..', 'documentation/tlctc-layered-event-modelling.md')] = process.argv.slice(2);
  if (!htmlPath) { console.error('Usage: node scripts/check-lem-sync.js <page.html> [paper.md]'); process.exit(2); }
  const md = fs.readFileSync(mdPath, 'utf8');
  const start = md.indexOf('## Abstract');
  if (start < 0) { console.error('markdown has no "## Abstract" heading'); process.exit(2); }
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setContent(`<div id="md">${marked.parse(md.slice(start))}</div>`);
  const blocks = await page.$$eval('#md p, #md li, #md td, #md th, #md h2, #md h3, #md blockquote, #md div[align]', (els) => els.map((e) => e.textContent));
  await page.goto(pathToFileURL(path.resolve(htmlPath)).href, { waitUntil: 'domcontentloaded' });
  const article = await page.$eval('#article-content', (e) => e.textContent);
  await browser.close();
  const hay = norm(article);
  const missing = blocks
    .map((b) => norm(b).replace(/^\[\d+\]\s*/, ''))
    .filter((b) => b.length >= 20 && !hay.includes(b));
  console.log(`LEM sync: ${blocks.length} markdown blocks checked`);
  if (missing.length) {
    console.log(`DRIFT — ${missing.length} block(s) not found in the page:`);
    for (const m of missing) console.log('  - ' + m.slice(0, 160));
    process.exit(1);
  }
  console.log('IN SYNC');
})().catch((e) => { console.error(e); process.exit(2); });
