// Render a TLCTC markdown paper to a machine-readable, Google-Scholar-friendly PDF.
// Deps (package.json is gitignored in this repo): npm install marked puppeteer
// Usage: node scripts/build-pdf.js <input.md> <output.pdf>
const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const { marked } = require("marked");
const puppeteer = require("puppeteer");

const [, , inPath, outPath] = process.argv;
if (!inPath || !outPath) {
  console.error("Usage: node scripts/build-pdf.js <input.md> <output.pdf>");
  process.exit(1);
}

const md = fs.readFileSync(inPath, "utf8");
const bodyHtml = marked.parse(md, { mangle: false, headerIds: true });

const css = `
  @page { size: A4; margin: 22mm 20mm 20mm 20mm; }
  html { -webkit-print-color-adjust: exact; }
  body {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 10.5pt; line-height: 1.5; color: #111; max-width: 100%;
  }
  h1 { font-size: 20pt; line-height: 1.25; margin: 0 0 4pt; }
  h2 { font-size: 14pt; margin: 20pt 0 6pt; border-bottom: 1px solid #ccc; padding-bottom: 3pt; page-break-after: avoid; }
  h3 { font-size: 11.5pt; margin: 14pt 0 4pt; page-break-after: avoid; }
  h4 { font-size: 10.5pt; margin: 12pt 0 4pt; page-break-after: avoid; }
  p { margin: 0 0 8pt; text-align: justify; }
  ul, ol { margin: 0 0 8pt; padding-left: 20pt; }
  li { margin: 0 0 3pt; }
  strong { font-weight: 700; }
  code { font-family: Consolas, "Courier New", monospace; font-size: 9pt; background: #f4f4f4; padding: 0 2px; border-radius: 2px; }
  pre { font-family: Consolas, "Courier New", monospace; font-size: 8.7pt; line-height: 1.35;
        background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 4px; padding: 8px 10px;
        white-space: pre-wrap; word-wrap: break-word; page-break-inside: avoid; margin: 0 0 10pt; }
  pre code { background: none; padding: 0; font-size: inherit; }
  table { border-collapse: collapse; width: 100%; margin: 0 0 10pt; font-size: 9.5pt; page-break-inside: avoid; }
  th, td { border: 1px solid #ccc; padding: 4px 7px; text-align: left; vertical-align: top; }
  th { background: #f0f0f0; }
  h1 + p { color: #333; }
  img { max-width: 100%; height: auto; display: block; margin: 10pt auto; page-break-inside: avoid; }
`;

const html = `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>TLCTC</title><style>${css}</style></head>
<body>${bodyHtml}</body></html>`;

// Serve the HTML from a temp file in the markdown's own directory so that
// relative image paths (e.g. images/foo.svg) resolve; page.setContent()
// renders at about:blank, which cannot load file:// subresources.
const tmpHtmlPath = path.join(
  path.dirname(path.resolve(inPath)),
  `.${path.basename(inPath)}.build-pdf.tmp.html`
);

(async () => {
  fs.writeFileSync(tmpHtmlPath, html);
  const browser = await puppeteer.launch({ headless: true, args: ["--no-sandbox"] });
  const page = await browser.newPage();
  await page.goto(pathToFileURL(tmpHtmlPath).href, { waitUntil: "networkidle0" });
  await page.pdf({
    path: outPath,
    format: "A4",
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate:
      '<div style="font-size:8px; width:100%; text-align:center; color:#888;">' +
      "TLCTC — A Cause-Oriented Cyber Threat Taxonomy &nbsp;·&nbsp; " +
      '<span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: { top: "22mm", bottom: "16mm", left: "20mm", right: "20mm" },
  });
  await browser.close();
  fs.unlinkSync(tmpHtmlPath);
  const kb = (fs.statSync(outPath).size / 1024).toFixed(0);
  console.log(`PDF written: ${path.resolve(outPath)} (${kb} KB)`);
})().catch((e) => {
  try { fs.unlinkSync(tmpHtmlPath); } catch {}
  console.error(e);
  process.exit(1);
});
