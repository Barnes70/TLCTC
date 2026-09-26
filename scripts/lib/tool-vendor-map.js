// Third-party assets used by the standalone tools in tools/, and where tlctc.net
// self-hosts each one.
//
// The repo copy of a tool loads its libraries from public CDNs, so a clone works
// when the file is opened straight from disk. tlctc.net serves the same tools with
// every library self-hosted under /vendor/ (no third-party requests from the site).
// scripts/build-site.js rewrites repo → site with this table, and
// scripts/validate-tools.js fails on any external asset the table does not cover,
// so a tool can never reach the site still pointing at a CDN.
//
// Keep entries exact: the rewrite is a plain string replacement.
'use strict';

const VENDOR_MAP = [
  ['https://cdn.tailwindcss.com/3.4.17', '/vendor/tailwindcss/3.4.17/tailwind.js'],
  ['https://unpkg.com/lucide@0.469.0/dist/umd/lucide.min.js', '/vendor/lucide/0.469.0/lucide.min.js'],
  ['https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js', '/vendor/react/18.3.1/react.production.min.js'],
  ['https://cdn.jsdelivr.net/npm/react-dom@18.3.1/umd/react-dom.production.min.js', '/vendor/react/18.3.1/react-dom.production.min.js'],
  ['https://cdn.jsdelivr.net/npm/@babel/standalone@7.26.4/babel.min.js', '/vendor/babel/7.26.4/babel.min.js'],
  ['https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js', '/vendor/html2canvas/1.4.1/html2canvas.min.js'],
  ['https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js', '/vendor/chartjs/3.9.1/chart.min.js'],
  ['https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js', '/vendor/jspdf/2.5.1/jspdf.umd.min.js'],
  ['https://cdn.jsdelivr.net/npm/@simonwep/pickr@1.9.1/dist/pickr.min.js', '/vendor/pickr/1.9.1/pickr.min.js'],
  ['https://cdn.jsdelivr.net/npm/@simonwep/pickr@1.9.1/dist/themes/monolith.min.css', '/vendor/pickr/1.9.1/monolith.min.css'],
  ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css', '/vendor/font-awesome/6.5.2/css/all.min.css'],
];

// Any Google Fonts stylesheet maps to the site's self-hosted superset, which covers
// every family the tools use (Inter, Plus Jakarta Sans, JetBrains Mono, …).
const GOOGLE_FONTS_RE = /https:\/\/fonts\.googleapis\.com\/css2\?[^"'\s]+/g;
const GOOGLE_FONTS_VENDOR = '/vendor/fonts/google-fonts.css';
// preconnect hints to the font CDNs are meaningless once the fonts are local
const FONT_PRECONNECT_RE = /[ \t]*<link[^>]+rel="preconnect"[^>]+href="https:\/\/fonts\.(?:googleapis|gstatic)\.com"[^>]*>\r?\n?/g;

// Script and stylesheet references that load an external asset — the only kind the
// map must cover. Hyperlinks (<a href>) and canonical/og URLs are not assets.
const ASSET_RE = /<(?:script[^>]*\bsrc|link[^>]*\bhref)="(https?:\/\/[^"]+)"/g;

function toSite(html) {
  let out = html;
  for (const [cdn, local] of VENDOR_MAP) out = out.split(cdn).join(local);
  out = out.replace(FONT_PRECONNECT_RE, '').replace(GOOGLE_FONTS_RE, GOOGLE_FONTS_VENDOR);
  return out;
}

// External assets left after the rewrite, ignoring the site's own origin.
function unmappedAssets(html) {
  const out = [];
  for (const m of html.matchAll(ASSET_RE)) if (!/^https:\/\/www\.tlctc\.net\//.test(m[1])) out.push(m[1]);
  return out;
}

module.exports = { VENDOR_MAP, GOOGLE_FONTS_VENDOR, toSite, unmappedAssets };
