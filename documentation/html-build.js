#!/usr/bin/env node
// ─────────────────────────────────────────────────────────────
// html-build.js — Convert TLCTC documents from Markdown to HTML (+ PDF)
// v2.5-ready: builds the v2.5 core paper, v2.5 application paper,
// glossary (v2.5), and the v2.0-named whitepaper (v2.1 structure,
// definitions current per the v2.5 dictionary).
//
// Usage:  node html-build.js           (HTML + PDF where enabled)
//         node html-build.js --no-pdf  (HTML only, skip PDF)
//
// NOTE: the core and application papers have pdf:false here on purpose.
// Their canonical, Google-Scholar-facing PDFs are built by
// scripts/build-pdf.js and must not be overwritten by this styled build.
// ─────────────────────────────────────────────────────────────

const fs   = require('fs');
const path = require('path');
const { marked } = require('marked');

const skipPdf = process.argv.includes('--no-pdf');

marked.setOptions({ gfm: true, breaks: false });

// ─── Helper: parse frontmatter from markdown ────────────────

function parseFrontmatter(raw) {
  const lines = raw.split(/\r?\n/); // tolerate CRLF sources
  let title = '', mainTitle = '', subtitle = '', author = '', initials = '', lastUpdated = '';
  let version = '', abstractText = '', contentStart = 0;
  let descriptionText = '';
  const preambleLines = []; // header-block lines (License, DOI, Implements, declarations, intro prose) kept for rendering

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (!title && line.startsWith('# ')) {
      title = line.replace(/^# /, '').trim();
      const parts = title.split(' — ');
      mainTitle = parts[0];
      subtitle  = parts.slice(1).join(' — ');
      continue;
    }

    // Glossary-style author line: *Author: X | Last Updated: Y*
    const am = line.match(/^\*Author:\s*(.+?)\s*\|\s*Last Updated:\s*(.+?)\*$/);
    if (am) {
      author      = am[1].trim();
      lastUpdated = am[2].trim();
      continue;
    }

    // Paper-style header fields: **Author:** X / **Version:** X / **Date:** X
    const bm = line.match(/^\*\*(Author|Version|Date):\*\*\s*(.+)$/);
    if (bm) {
      const val = bm[2].trim();
      if (bm[1] === 'Author')  author = val;
      if (bm[1] === 'Version') version = val;
      if (bm[1] === 'Date' && !lastUpdated) lastUpdated = val;
      continue;
    }

    // Description line: *Some italic text.* (not the author line)
    const dm = line.match(/^\*([^*]+)\*$/);
    if (dm && !descriptionText && !line.startsWith('*Author')) {
      descriptionText = dm[1].trim();
      continue;
    }

    // Abstract as bare keyword or as a heading (papers use "## Abstract")
    if (line.trim() === 'Abstract' || line.trim() === '## Abstract') {
      let j = i + 1;
      while (j < lines.length && lines[j].trim() === '') j++;
      const buf = [];
      while (j < lines.length && !/^#{1,6} /.test(lines[j])) {
        buf.push(lines[j]);
        j++;
      }
      abstractText = buf.join('\n').trim();
      contentStart = j;
      break;
    }

    // First ## heading without an Abstract: content starts here
    if (line.startsWith('## ')) {
      contentStart = i;
      break;
    }

    // Anything else in the header region (License/DOI/Companion/Implements
    // lines, canonical-declaration blockquotes, glossary intro prose) is
    // preserved and rendered ahead of the content instead of being dropped.
    if (title && line.trim() !== '---' && line.trim() !== '&nbsp;') {
      preambleLines.push(line);
    }
  }

  if (author) initials = author.split(/\s+/).map(w => w[0]).join('').toUpperCase();

  return { title, mainTitle, subtitle, author, initials, lastUpdated, version, abstractText, descriptionText, preambleLines, contentStart, lines };
}

// ─── Helper: post-process HTML ──────────────────────────────

function postProcessHTML(html) {
  // Add IDs to headings (h2–h5) for TOC and direct linking
  html = html.replace(/<h([2-5])>([\s\S]*?)<\/h\1>/gi, (match, level, inner) => {
    const text = inner.replace(/<[^>]*>/g, '');
    const id   = text.toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '')
      .replace(/-+/g, '-');
    return `<h${level} id="${id}">${inner}</h${level}>`;
  });

  // Convert image + italic-caption into <figure>
  //   Case A: same <p>
  html = html.replace(
    /<p>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*\/?>\s*\n?\s*<em>([\s\S]*?)<\/em>\s*<\/p>/gi,
    (_, src, alt, caption) => {
      const cleaned = caption.replace(/^Figure:\s*/i, '');
      return `<figure class="my-8 group">
  <img src="${src}" alt="${alt}" class="rounded-xl border border-border/60 bg-card/30 shadow-sm w-full cursor-zoom-in transition-transform group-hover:scale-[1.01]" onclick="openZoomModal(this)">
  <figcaption class="border-t border-border/50 bg-muted/30 p-3 text-center font-sans text-xs text-muted-foreground"><strong>Figure:</strong> ${cleaned}</figcaption>
</figure>`;
    }
  );
  //   Case B: separate <p> tags
  html = html.replace(
    /<p>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*\/?>\s*<\/p>\s*<p>\s*<em>([\s\S]*?)<\/em>\s*<\/p>/gi,
    (_, src, alt, caption) => {
      const cleaned = caption.replace(/^Figure:\s*/i, '');
      return `<figure class="my-8 group">
  <img src="${src}" alt="${alt}" class="rounded-xl border border-border/60 bg-card/30 shadow-sm w-full cursor-zoom-in transition-transform group-hover:scale-[1.01]" onclick="openZoomModal(this)">
  <figcaption class="border-t border-border/50 bg-muted/30 p-3 text-center font-sans text-xs text-muted-foreground"><strong>Figure:</strong> ${cleaned}</figcaption>
</figure>`;
    }
  );
  // Standalone images without caption
  html = html.replace(
    /<p>\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*\/?>\s*<\/p>/gi,
    (_, src, alt) => {
      return `<figure class="my-8 group">
  <img src="${src}" alt="${alt}" class="rounded-xl border border-border/60 bg-card/30 shadow-sm w-full cursor-zoom-in transition-transform group-hover:scale-[1.01]" onclick="openZoomModal(this)">
</figure>`;
    }
  );

  return html;
}

// ─── Helper: build a single document ────────────────────────

function buildDocument(inputFile, outputFile, opts = {}) {
  const raw = fs.readFileSync(inputFile, 'utf8');
  const fm  = parseFrontmatter(raw);

  const contentMd  = fm.lines.slice(fm.contentStart).join('\n');
  const contentHTML = postProcessHTML(marked.parse(contentMd));

  const abstractHTML = fm.abstractText ? marked.parse(fm.abstractText) : '';
  const preambleMd   = fm.preambleLines.join('\n').trim();
  const preambleHTML = preambleMd ? marked.parse(preambleMd) : '';
  const descSnippet  = fm.abstractText || fm.descriptionText || '';

  // Badge suffix follows the version declared in the document itself;
  // opts.badgeSuffix only serves docs that carry no **Version:** field.
  const badgeSuffix = fm.version ? `TLCTC v${fm.version}` : (opts.badgeSuffix || 'TLCTC v2.5');

  const html = renderPage({
    pageTitle:   fm.title,
    mainTitle:   fm.mainTitle,
    subtitle:    fm.subtitle,
    author:      fm.author || opts.author || '',
    initials:    (fm.author || opts.author || '').split(/\s+/).filter(Boolean).map(w => w[0]).join('').toUpperCase(),
    lastUpdated: fm.lastUpdated || opts.lastUpdated || '',
    abstractHTML,
    preambleHTML,
    contentHTML,
    descSnippet,
    badge:       opts.badge || 'White Paper',
    badgeSuffix,
    extraNavHTML: opts.extraNavHTML || '',
    extraNavLinks: opts.extraNavLinks || [],
  });

  fs.writeFileSync(outputFile, html, 'utf8');
  const stats = fs.statSync(outputFile);
  console.log(`Done  ${outputFile}  (${(stats.size / 1024).toFixed(0)} KB)`);
}

// ─── Helper: generate PDF from HTML via Puppeteer ───────────

async function buildPdf(htmlFile) {
  const puppeteer = require('puppeteer');
  const pdfFile = htmlFile.replace(/\.html$/, '.pdf');

  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  // Load from file:// so relative image paths (images/*.svg) resolve
  const fileUrl = 'file:///' + htmlFile.replace(/\\/g, '/');
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 60000 });

  await page.pdf({
    path: pdfFile,
    format: 'A4',
    printBackground: true,
    margin: { top: '18mm', right: '16mm', bottom: '20mm', left: '16mm' },
    displayHeaderFooter: false,
  });

  await browser.close();

  const stats = fs.statSync(pdfFile);
  console.log(`Done  ${pdfFile}  (${(stats.size / 1024).toFixed(0)} KB)`);
}

// ─── Build all documents ────────────────────────────────────

async function main() {
  const navLink = (href, text) =>
    `<a href="${href}" class="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">${text}</a>`;

  const DOCS = [
    {
      input:  path.join(__dirname, 'tlctc-v2.5-core.md'),
      output: path.join(__dirname, 'tlctc-v2.5-core.html'),
      pdf:    false, // canonical Scholar PDF comes from scripts/build-pdf.js — do not overwrite
      opts:   {
        badge: 'Core Paper',
        extraNavHTML: navLink('tlctc-v2.5-application.html', 'Application Paper') + '\n' + navLink('tlctc-glossary.html', 'Glossary'),
        extraNavLinks: [
          { href: 'tlctc-v2.5-application.html', text: 'Application Paper' },
          { href: 'tlctc-glossary.html', text: 'Glossary' },
        ],
      },
    },
    {
      input:  path.join(__dirname, 'tlctc-v2.5-application.md'),
      output: path.join(__dirname, 'tlctc-v2.5-application.html'),
      pdf:    false, // canonical Scholar PDF comes from scripts/build-pdf.js — do not overwrite
      opts:   {
        badge: 'Application Paper',
        extraNavHTML: navLink('tlctc-v2.5-core.html', 'Core Paper') + '\n' + navLink('tlctc-glossary.html', 'Glossary'),
        extraNavLinks: [
          { href: 'tlctc-v2.5-core.html', text: 'Core Paper' },
          { href: 'tlctc-glossary.html', text: 'Glossary' },
        ],
      },
    },
    {
      input:  path.join(__dirname, 'tlctc-v2.0-whitepaper.md'),
      output: path.join(__dirname, 'tlctc-v2.0-whitepaper.html'),
      pdf:    true,
      opts:   {
        // v2.1 paper structure; cluster definitions current per the v2.5 dictionary
        badge: 'White Paper', badgeSuffix: 'TLCTC v2.5',
        author: 'Bernhard Kreinz',
        extraNavHTML: navLink('tlctc-v2.5-core.html', 'Core Paper') + '\n' + navLink('tlctc-glossary.html', 'Glossary'),
        extraNavLinks: [
          { href: 'tlctc-v2.5-core.html', text: 'Core Paper' },
          { href: 'tlctc-glossary.html', text: 'Glossary' },
        ],
      },
    },
    {
      input:  path.join(__dirname, 'tlctc-glossary.md'),
      output: path.join(__dirname, 'tlctc-glossary.html'),
      pdf:    true,
      opts:   {
        badge: 'Glossary', badgeSuffix: 'TLCTC v2.5',
        extraNavHTML: navLink('tlctc-v2.5-core.html', 'Core Paper') + '\n' + navLink('tlctc-v2.0-whitepaper.html', 'White Paper'),
        extraNavLinks: [
          { href: 'tlctc-v2.5-core.html', text: 'Core Paper' },
          { href: 'tlctc-v2.0-whitepaper.html', text: 'White Paper' },
        ],
      },
    },
  ];

  const pdfTargets = [];
  for (const { input, output, pdf, opts } of DOCS) {
    if (!fs.existsSync(input)) {
      console.warn(`Skip  ${input} (not found)`);
      continue;
    }
    buildDocument(input, output, opts);
    if (pdf) pdfTargets.push(output);
  }

  if (!skipPdf) {
    console.log('\nGenerating PDFs…');
    for (const htmlFile of pdfTargets) {
      await buildPdf(htmlFile);
    }
  }
}

main().catch(err => { console.error(err); process.exit(1); });

// ─── Template ───────────────────────────────────────────────

function renderPage(p) {
  return `<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${p.pageTitle}</title>
    <meta name="description" content="${(p.descSnippet || '').slice(0, 200).replace(/"/g, '&quot;')}…">
    <meta name="keywords" content="TLCTC, Top Level Cyber Threat Clusters, cybersecurity, threat framework, threat modeling, risk management, CISO, incident analysis, governance, Bow-Tie">
    <meta name="author" content="${p.author}">
    <meta property="og:title" content="${p.pageTitle}">
    <meta property="og:type" content="article">

    <script src="/vendor/tailwindcss/3.4.17/tailwind.js"></script>
    <script src="/vendor/lucide/0.469.0/lucide.min.js"></script>

    <script>
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Segoe UI', 'Arial', 'sans-serif'],
                        display: ['Segoe UI', 'Arial', 'sans-serif'],
                    },
                    colors: {
                        border: "hsl(var(--border))",
                        input: "hsl(var(--input))",
                        ring: "hsl(var(--ring))",
                        background: "hsl(var(--background))",
                        foreground: "hsl(var(--foreground))",
                        primary: {
                            DEFAULT: "hsl(var(--primary))",
                            foreground: "hsl(var(--primary-foreground))"
                        },
                        secondary: {
                            DEFAULT: "hsl(var(--secondary))",
                            foreground: "hsl(var(--secondary-foreground))"
                        },
                        muted: {
                            DEFAULT: "hsl(var(--muted))",
                            foreground: "hsl(var(--muted-foreground))"
                        },
                        accent: {
                            DEFAULT: "hsl(var(--accent))",
                            foreground: "hsl(var(--accent-foreground))"
                        },
                        card: {
                            DEFAULT: "hsl(var(--card))",
                            foreground: "hsl(var(--card-foreground))"
                        },
                        destructive: {
                            DEFAULT: "hsl(var(--destructive))",
                            foreground: "hsl(var(--destructive-foreground))"
                        },
                    },
                },
            }
        }
    </script>

    <style type="text/tailwindcss">
        @layer base {
            :root {
                --radius: 0.75rem;
                --background: 0 0% 100%;
                --foreground: 240 10% 3.9%;
                --card: 0 0% 100%;
                --card-foreground: 240 10% 3.9%;
                --primary: 240 5.9% 10%;
                --primary-foreground: 0 0% 98%;
                --secondary: 240 4.8% 95.9%;
                --secondary-foreground: 240 5.9% 10%;
                --muted: 240 4.8% 95.9%;
                --muted-foreground: 240 3.8% 46.1%;
                --accent: 240 4.8% 95.9%;
                --accent-foreground: 240 5.9% 10%;
                --destructive: 0 84.2% 60.2%;
                --destructive-foreground: 0 0% 98%;
                --border: 240 5.9% 90%;
                --input: 240 5.9% 90%;
                --ring: 240 5.9% 10%;
            }

            .dark {
                --background: 240 10% 3.9%;
                --foreground: 0 0% 98%;
                --card: 240 10% 3.9%;
                --card-foreground: 0 0% 98%;
                --primary: 0 0% 98%;
                --primary-foreground: 240 5.9% 10%;
                --secondary: 240 3.7% 15.9%;
                --secondary-foreground: 0 0% 98%;
                --muted: 240 3.7% 15.9%;
                --muted-foreground: 240 5% 64.9%;
                --accent: 240 3.7% 15.9%;
                --accent-foreground: 0 0% 98%;
                --destructive: 0 62.8% 30.6%;
                --destructive-foreground: 0 0% 98%;
                --border: 240 3.7% 15.9%;
                --input: 240 3.7% 15.9%;
                --ring: 240 4.9% 83.9%;
            }

            body {
                @apply bg-background text-foreground selection:bg-primary/20;
            }
        }

        @layer components {
            .container-custom { @apply mx-auto max-w-7xl px-4 sm:px-6 lg:px-8; }

            .btn { @apply inline-flex items-center justify-center rounded-lg text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background active:scale-95; }
            .btn-sm { @apply h-9 px-3 text-xs; }
            .btn-primary { @apply bg-primary text-primary-foreground shadow-lg shadow-primary/20 hover:bg-primary/90 hover:shadow-xl hover:shadow-primary/30 hover:-translate-y-0.5; }
            .btn-ghost { @apply hover:bg-accent hover:text-accent-foreground; }

            .glass-card { @apply bg-card/50 backdrop-blur-xl border border-border/50 shadow-sm transition-all duration-300; }

            .grid-bg {
                background-image: linear-gradient(to right, hsl(var(--border) / 0.1) 1px, transparent 1px),
                                linear-gradient(to bottom, hsl(var(--border) / 0.1) 1px, transparent 1px);
                background-size: 40px 40px;
                mask-image: radial-gradient(ellipse at center, black, transparent 80%);
            }

            .callout { @apply rounded-xl border p-5 my-6 flex gap-4 backdrop-blur-sm shadow-sm; }
            .callout-note { @apply border-primary/20 bg-primary/5 text-foreground; }

            .prose-custom { @apply text-[17px]; }
            .prose-custom h1 { @apply font-display text-3xl sm:text-4xl font-bold mt-8 mb-6 scroll-mt-24; }
            .prose-custom h2 { @apply font-display text-2xl font-bold mt-10 mb-4 scroll-mt-24 gradient-text w-fit; }
            .prose-custom h3 { @apply font-display text-xl font-semibold mt-8 mb-3 scroll-mt-24; }
            .prose-custom h4 { @apply font-display text-lg font-semibold mt-6 mb-2 scroll-mt-24; }
            .prose-custom h5 { @apply font-display text-base font-semibold mt-5 mb-2 scroll-mt-24; }
            .prose-custom p { @apply leading-7 mb-6 text-muted-foreground; }
            .prose-custom hr { @apply my-10 border-border/60; }
            .prose-custom img { @apply rounded-xl border border-border/60 bg-card/30 shadow-sm my-8; }
            .prose-custom table { @apply w-full my-8 text-sm border border-border/60 rounded-xl overflow-hidden; }
            .prose-custom thead { @apply bg-muted/50; }
            .prose-custom th { @apply text-left font-semibold text-foreground px-4 py-2 border-b border-border/60; }
            .prose-custom td { @apply align-top px-4 py-2 border-b border-border/40; }
            .prose-custom tr:last-child td { @apply border-b-0; }
            .prose-custom pre { @apply rounded-xl border border-border bg-muted/40 my-6 p-4 overflow-x-auto text-sm leading-relaxed; }
            .prose-custom code { @apply text-primary bg-muted/60 px-1 py-0.5 rounded font-mono text-[0.95em]; }
            .prose-custom pre code { @apply bg-transparent p-0; }
            .prose-custom blockquote { @apply border-l-4 border-primary/60 pl-4 italic text-foreground/80 my-6; }
            .prose-custom ul, .prose-custom ol { @apply mb-6 ml-6 list-outside text-muted-foreground; }
            .prose-custom li { @apply mb-2; }
            .prose-custom a { @apply text-primary underline decoration-dotted underline-offset-4 hover:text-primary/80 transition-colors; }
            .prose-custom .footnotes { @apply text-sm text-muted-foreground border-t border-border/60 mt-12 pt-6; }

            .gradient-text {
                @apply bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/70;
            }

            .toc-link { @apply block py-1.5 px-3 text-sm text-muted-foreground hover:text-primary hover:bg-primary/5 rounded-md transition-all border-l-2 border-transparent; }
            .toc-link.active { @apply text-primary font-medium bg-primary/5 border-primary; }
            .toc-link[data-level="h3"] { @apply pl-6 text-xs; }
        }
    </style>

    <style>
@media print {
  @page { margin: 18mm 16mm 20mm; }
  html, body { background: #fff !important; color: #000 !important; }
  * { box-shadow: none !important; text-shadow: none !important; filter: none !important; }
  header, footer, aside, #mobile-menu, #theme-toggle, hr, #scrollTopBtn, #zoom-modal, .grid-bg, .fixed.inset-0.-z-10 { display: none !important; }
  main { padding: 0 !important; }
  .container-custom { max-width: none !important; padding: 0 16mm !important; }
  .container-custom.grid { display: block !important; }
  #article-content { font-size: 11pt !important; line-height: 1.45 !important; }
  #article-content .max-w-3xl { max-width: none !important; }
  #article-content p, #article-content li, #article-content blockquote, #article-content .text-muted-foreground { color: #000 !important; }
  .gradient-text { color: #000 !important; background: none !important; -webkit-text-fill-color: #000 !important; }
  #article-content h1, #article-content h2, #article-content h3, #article-content h4 { color: #000 !important; break-after: avoid-page; page-break-after: avoid; }
  #article-content h2[id^="part-"] { break-before: page; page-break-before: always; margin-top: 0 !important; }
  a { color: #000 !important; text-decoration: underline !important; }
  #article-content pre, #article-content code, .codeblock { background: none !important; color: #000 !important; border: 1px solid #999 !important; }
  #article-content pre { white-space: pre-wrap !important; word-break: break-word !important; }
  #article-content table { width: 100% !important; border-collapse: collapse !important; }
  #article-content thead { display: table-header-group; }
  #article-content th, #article-content td { border: 1px solid #999 !important; color: #000 !important; }
  #article-content tr { break-inside: avoid; page-break-inside: avoid; }
  #article-content img, #article-content svg { max-width: 100% !important; height: auto !important; border: none !important; break-inside: avoid; page-break-inside: avoid; }
  p { orphans: 3; widows: 3; }
}
    </style>
</head>
<body class="min-h-screen font-sans antialiased relative overflow-x-hidden">

    <div class="fixed inset-0 -z-10 h-full w-full bg-background">
        <div class="absolute inset-0 grid-bg"></div>
        <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-[1000px] h-[600px] bg-primary/5 rounded-full blur-[100px] opacity-50 pointer-events-none"></div>
    </div>

    <header class="sticky top-4 z-50 mx-auto max-w-7xl px-4">
        <div class="rounded-2xl border border-border/40 bg-background/70 backdrop-blur-md shadow-sm">
            <div class="flex h-16 items-center justify-between px-4 sm:px-6">
                <div class="flex items-center gap-3">
                    <a href="index.html" class="flex items-center gap-2 group">
                        <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary group-hover:scale-105 transition-transform">
                           <img src="/images/logo-small.png" alt="Logo" class="h-full w-full object-contain p-1" onerror="this.style.display='none'; this.nextElementSibling.style.display='block'">
                           <i data-lucide="shield" class="h-5 w-5 hidden"></i>
                        </div>
                        <div class="flex flex-col">
                            <span class="font-display font-bold text-lg leading-tight">TLCTC</span>
                            <span class="text-[10px] text-muted-foreground font-medium hidden sm:block uppercase tracking-wider">Top Level Cyber Threat Clusters</span>
                        </div>
                    </a>
                </div>
                <nav class="hidden md:flex items-center gap-6">
                    <a href="https://github.com/Barnes70/TLCTC" class="flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors group">
                        <i data-lucide="github" class="h-4 w-4 text-grey-400 fill-grey-400/20 group-hover:rotate-12 transition-transform"></i>
                        GitHub
                    </a>
${p.extraNavHTML || ''}
                    <a href="tlctc-infographics.html" class="flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors group">
                        <i data-lucide="banana" class="h-4 w-4 text-yellow-400 fill-yellow-400/20 group-hover:rotate-12 transition-transform"></i>
                    </a>
                </nav>
                <div class="flex items-center gap-3">
                    <button onclick="window.print()" class="p-2 rounded-lg text-slate-500 hover:bg-slate-100 hover:text-blue-600 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-blue-400 transition-colors duration-200" aria-label="Print Page" title="Print this article">
                        <i data-lucide="printer" class="w-5 h-5"></i>
                    </button>
                    <button id="theme-toggle" onclick="toggleDarkMode()" class="btn btn-ghost btn-sm h-9 w-9 p-0 rounded-full" aria-label="Toggle theme">
                        <i id="theme-toggle-dark-icon" data-lucide="sun" class="h-4 w-4 hidden dark:block"></i>
                        <i id="theme-toggle-light-icon" data-lucide="moon" class="h-4 w-4 block dark:hidden"></i>
                    </button>
                    <button onclick="toggleMenu()" class="md:hidden btn btn-ghost btn-sm h-9 w-9 p-0 rounded-full">
                        <i data-lucide="menu" class="h-5 w-5"></i>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <div id="mobile-menu" class="fixed inset-0 z-[60] bg-background/95 backdrop-blur-sm md:hidden hidden transition-all duration-300 opacity-0">
        <div class="flex h-20 items-center justify-between px-6 border-b border-border">
            <span class="font-display font-bold text-lg">TLCTC</span>
            <button onclick="toggleMenu()" class="btn btn-ghost h-10 w-10 p-0 rounded-full">
                <i data-lucide="x" class="h-6 w-6"></i>
            </button>
        </div>
        <nav class="flex flex-col p-8 gap-6 text-lg font-medium">
            <a href="index.html" onclick="toggleMenu()" class="text-muted-foreground hover:text-foreground">Home</a>
            <a href="tlctc-10-definitions.html" onclick="toggleMenu()" class="text-muted-foreground hover:text-foreground">The 10 Clusters</a>
            <a href="index.html#blog" onclick="toggleMenu()" class="text-primary font-semibold">White Paper</a>
${(p.extraNavLinks || []).map(l => `            <a href="${l.href}" onclick="toggleMenu()" class="text-muted-foreground hover:text-foreground">${l.text}</a>`).join('\n')}
            <hr class="border-border">
            <a href="javascript:window.print()" class="text-primary font-semibold">Print</a>
        </nav>
    </div>

    <main class="pt-12 pb-24">
        <section class="container-custom mb-12 md:mb-20 text-center animate-fade-in-up">
            <div class="inline-flex items-center gap-2 rounded-full border border-border bg-secondary/50 px-3 py-1 text-xs font-medium text-secondary-foreground backdrop-blur-sm mb-6">
                <span class="text-primary">${p.badge}</span> / ${p.badgeSuffix}
            </div>
            <h1 class="font-display text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight mb-6 max-w-4xl mx-auto leading-tight gradient-text">
                ${p.mainTitle}
            </h1>
            <p class="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
                ${p.subtitle}
            </p>
            <div class="flex flex-wrap items-center justify-center gap-4 text-sm text-muted-foreground">
                <div class="flex items-center gap-2">
                    <div class="h-8 w-8 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-xs border border-primary/20">${p.initials}</div>
                    <span class="font-medium text-foreground">${p.author}</span>
                </div>
                <span class="text-border">&bull;</span>
                <time>Last updated: ${p.lastUpdated}</time>
                <span class="text-border">&bull;</span>
                <span id="reading-time">Loading read time...</span>
            </div>
        </section>

        <div class="container-custom grid lg:grid-cols-12 gap-12 relative">
            <article id="article-content" class="lg:col-span-8 prose-custom min-w-0">
<div class="max-w-3xl mx-auto">

${p.preambleHTML ? `<div class="rounded-xl border border-border/60 bg-muted/20 p-5 my-6 text-sm leading-6 text-muted-foreground [&_blockquote]:border-l-4 [&_blockquote]:border-primary/60 [&_blockquote]:pl-4 [&_blockquote]:not-italic">
${p.preambleHTML}
</div>` : ''}

${p.abstractHTML ? `<div class="callout callout-note">
  <div class="mt-0.5 text-primary flex-shrink-0"><i data-lucide="file-text" class="h-5 w-5"></i></div>
  <div>
    <div class="text-sm font-bold text-foreground mb-1">Abstract</div>
    <div class="text-sm leading-6 text-muted-foreground">${p.abstractHTML}</div>
  </div>
</div>` : ''}

${p.contentHTML}

</div>
            </article>

            <aside class="hidden lg:block lg:col-span-4 pl-8">
                <div class="sticky top-24 space-y-6">
                    <div class="glass-card rounded-xl p-5">
                        <div class="text-xs font-bold uppercase tracking-widest text-muted-foreground mb-4 flex items-center gap-2">
                            <i data-lucide="list" class="h-3 w-3"></i> Table of Contents
                        </div>
                        <nav id="toc" class="space-y-1 max-h-[70vh] overflow-y-auto custom-scroll pr-2"></nav>
                    </div>
                </div>
            </aside>
        </div>
    </main>

    <footer class="bg-card border-t border-border py-12 text-sm mt-12 opacity-90">
        <div class="container-custom flex flex-col md:flex-row justify-between items-center gap-6">
            <div class="flex items-center gap-2 opacity-80">
                <img src="/favicon.png" alt="TLCTC">
                <span class="font-bold">TLCTC Framework</span>
            </div>
            <div class="text-muted-foreground text-center md:text-right">
                <p>&copy; <span id="year"></span> Top Level Cyber Threat Clusters.</p>
                <p class="mt-1">Licensed under <a href="https://creativecommons.org/licenses/by/4.0/" class="underline decoration-dotted hover:text-primary">CC BY 4.0</a>.</p>
            </div>
        </div>
    </footer>

    <div id="zoom-modal" class="fixed inset-0 z-[100] hidden" aria-hidden="true">
        <div class="absolute inset-0 bg-background/90 backdrop-blur-sm transition-opacity duration-300 opacity-0" id="modal-backdrop" onclick="closeZoomModal()"></div>
        <div class="fixed inset-0 z-10 overflow-y-auto">
            <div class="flex min-h-full items-center justify-center p-2 text-center sm:p-4">
                <div id="modal-panel" class="relative transform overflow-hidden rounded-xl bg-card border border-border shadow-2xl transition-all opacity-0 scale-95 duration-300 ease-out w-full md:w-[95vw] flex flex-col my-8">
                    <div class="absolute top-0 right-0 pt-4 pr-4 z-50 flex gap-2">
                        <button type="button" class="rounded-md bg-background/80 backdrop-blur-md text-foreground hover:bg-destructive hover:text-destructive-foreground focus:outline-none ring-1 ring-border p-2 transition-colors shadow-sm" onclick="closeZoomModal()">
                            <i data-lucide="x" class="h-6 w-6"></i>
                        </button>
                    </div>
                    <div id="modal-content" class="p-4 sm:p-8 overflow-auto flex items-center justify-center min-h-[50vh]"></div>
                </div>
            </div>
        </div>
    </div>

    <button id="scrollTopBtn" onclick="scrollToTop()" class="fixed bottom-8 right-8 btn btn-primary rounded-full h-12 w-12 p-0 shadow-xl opacity-0 translate-y-10 transition-all duration-500 z-50">
        <i data-lucide="arrow-up" class="h-5 w-5"></i>
    </button>

<script>
    // Icons & Year
    lucide.createIcons();
    document.getElementById('year').textContent = new Date().getFullYear();

    // Theme
    const htmlEl = document.documentElement;
    function updateThemeIcons() {
        const d = document.getElementById('theme-toggle-dark-icon');
        const l = document.getElementById('theme-toggle-light-icon');
        if (htmlEl.classList.contains('dark')) { d.classList.remove('hidden'); l.classList.add('hidden'); }
        else { d.classList.add('hidden'); l.classList.remove('hidden'); }
    }
    function toggleDarkMode() {
        htmlEl.classList.toggle('dark');
        localStorage.theme = htmlEl.classList.contains('dark') ? 'dark' : 'light';
        updateThemeIcons();
    }
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        htmlEl.classList.add('dark');
    } else { htmlEl.classList.remove('dark'); }
    updateThemeIcons();

    // Mobile Menu
    const mobileMenu = document.getElementById('mobile-menu');
    function toggleMenu() {
        const isHidden = mobileMenu.classList.contains('hidden');
        if (isHidden) { mobileMenu.classList.remove('hidden'); setTimeout(() => mobileMenu.classList.remove('opacity-0'), 10); document.body.style.overflow = 'hidden'; }
        else { mobileMenu.classList.add('opacity-0'); setTimeout(() => mobileMenu.classList.add('hidden'), 300); document.body.style.overflow = ''; }
    }

    // Scroll Top + TOC highlight
    const scrollBtn = document.getElementById('scrollTopBtn');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) { scrollBtn.classList.remove('opacity-0', 'translate-y-10'); }
        else { scrollBtn.classList.add('opacity-0', 'translate-y-10'); }
        highlightTOC();
    });
    function scrollToTop() { window.scrollTo({ top: 0, behavior: 'smooth' }); }

    // Reading Time
    (function() {
        const el = document.getElementById('article-content');
        if (!el) return;
        const words = (el.innerText || '').trim().split(/\\s+/).length;
        const mins = Math.max(1, Math.round(words / 200));
        const t = document.getElementById('reading-time');
        if (t) t.textContent = mins + ' min read';
    })();

    // Build TOC
    function buildTOC() {
        const toc = document.getElementById('toc');
        const headers = document.querySelectorAll('#article-content h2, #article-content h3');
        if (!toc || !headers.length) return;
        headers.forEach((h) => {
            if (!h.id) h.id = h.textContent.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-');
            const a = document.createElement('a');
            a.href = '#' + h.id;
            a.className = 'toc-link';
            a.textContent = h.textContent;
            if (h.tagName === 'H3') a.setAttribute('data-level', 'h3');
            toc.appendChild(a);
        });
    }
    buildTOC();

    function highlightTOC() {
        const headers = document.querySelectorAll('#article-content h2, #article-content h3');
        const tocLinks = document.querySelectorAll('.toc-link');
        let current = '';
        headers.forEach(h => { if (window.scrollY >= h.offsetTop - 150) current = h.id; });
        tocLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current) && current !== '') link.classList.add('active');
        });
    }

    // Zoom Modal
    const modal = document.getElementById('zoom-modal');
    const backdrop = document.getElementById('modal-backdrop');
    const modalPanel = document.getElementById('modal-panel');
    const modalContent = document.getElementById('modal-content');

    function openZoomModal(sourceElement) {
        if (!sourceElement) return;
        const clone = sourceElement.cloneNode(true);
        clone.classList.remove('h-full', 'w-full', 'max-w-md', 'max-w-4xl', 'cursor-zoom-in', 'group-hover:scale-[1.02]', 'drop-shadow-sm');
        clone.style.width = 'auto'; clone.style.height = 'auto';
        clone.style.maxWidth = '100%'; clone.style.maxHeight = '85vh'; clone.style.margin = '0 auto';
        modalContent.innerHTML = '';
        modalContent.appendChild(clone);
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        requestAnimationFrame(() => {
            backdrop.classList.remove('opacity-0');
            modalPanel.classList.remove('opacity-0', 'scale-95');
            modalPanel.classList.add('opacity-100', 'scale-100');
        });
    }
    function closeZoomModal() {
        backdrop.classList.add('opacity-0');
        modalPanel.classList.remove('opacity-100', 'scale-100');
        modalPanel.classList.add('opacity-0', 'scale-95');
        setTimeout(() => { modal.classList.add('hidden'); modalContent.innerHTML = ''; document.body.style.overflow = ''; }, 300);
    }
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeZoomModal(); });
</script>
</body>
</html>`;
}
