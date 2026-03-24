#!/bin/bash
# Replace all CDN URLs with local /vendor/ paths in active HTML files
# Can live anywhere in the repo — auto-locates the project root
# Uses absolute paths from webserver root: /vendor/...

set -e

cd "$(dirname "$0")/.."

# Process all root-level active HTML files (not include/)
find . -maxdepth 1 -name "*.html" -not -name "TLCTCWhitePaperVersion1.9.1.html" | while read file; do
  echo "Processing: $file"

  # === TAILWIND ===
  sed -i 's|https://cdn\.tailwindcss\.com"|/vendor/tailwindcss/3.4.17/tailwind.js"|g' "$file"
  sed -i "s|https://cdn\.tailwindcss\.com'|/vendor/tailwindcss/3.4.17/tailwind.js'|g" "$file"
  sed -i 's|https://cdn\.tailwindcss\.com</|/vendor/tailwindcss/3.4.17/tailwind.js</|g' "$file"
  sed -i 's|src="https://cdn\.tailwindcss\.com">|src="/vendor/tailwindcss/3.4.17/tailwind.js">|g' "$file"

  # === LUCIDE ===
  sed -i 's|https://unpkg\.com/lucide@latest|/vendor/lucide/0.469.0/lucide.min.js|g' "$file"
  sed -i 's|https://unpkg\.com/lucide@[0-9.]*|/vendor/lucide/0.469.0/lucide.min.js|g' "$file"

  # === REACT (specific versions first, then generic) ===
  # React 18.2.0 from cdnjs
  sed -i 's|https://cdnjs\.cloudflare\.com/ajax/libs/react/18\.2\.0/umd/react\.production\.min\.js|/vendor/react/18.3.1/react.production.min.js|g' "$file"
  sed -i 's|https://cdnjs\.cloudflare\.com/ajax/libs/react-dom/18\.2\.0/umd/react-dom\.production\.min\.js|/vendor/react/18.3.1/react-dom.production.min.js|g' "$file"
  # React 18.2.0 from unpkg (specific version)
  sed -i 's|https://unpkg\.com/react@18\.2\.0/umd/react\.development\.js|/vendor/react/18.3.1/react.development.js|g' "$file"
  sed -i 's|https://unpkg\.com/react-dom@18\.2\.0/umd/react-dom\.development\.js|/vendor/react/18.3.1/react-dom.development.js|g' "$file"
  # React @18 from unpkg (production)
  sed -i 's|https://unpkg\.com/react@18/umd/react\.production\.min\.js|/vendor/react/18.3.1/react.production.min.js|g' "$file"
  sed -i 's|https://unpkg\.com/react-dom@18/umd/react-dom\.production\.min\.js|/vendor/react/18.3.1/react-dom.production.min.js|g' "$file"
  # React @18 from unpkg (development)
  sed -i 's|https://unpkg\.com/react@18/umd/react\.development\.js|/vendor/react/18.3.1/react.development.js|g' "$file"
  sed -i 's|https://unpkg\.com/react-dom@18/umd/react-dom\.development\.js|/vendor/react/18.3.1/react-dom.development.js|g' "$file"

  # === BABEL ===
  sed -i 's|https://unpkg\.com/@babel/standalone/babel\.min\.js|/vendor/babel/7.26.4/babel.min.js|g' "$file"
  sed -i 's|https://cdnjs\.cloudflare\.com/ajax/libs/babel-standalone/7\.[0-9.]*/babel\.min\.js|/vendor/babel/7.26.4/babel.min.js|g' "$file"

  # === FONT AWESOME (all versions → 6.5.2) ===
  sed -i 's|https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/6\.[0-9.]*/css/all\.min\.css|/vendor/font-awesome/6.5.2/css/all.min.css|g' "$file"
  # Remove SRI and cross-origin attributes (not needed for local files)
  sed -i 's| integrity="sha512-[^"]*"||g' "$file"
  sed -i 's| integrity="sha384-[^"]*"||g' "$file"
  sed -i 's| integrity="sha256-[^"]*"||g' "$file"
  sed -i 's| crossorigin="anonymous"||g' "$file"
  sed -i 's| referrerpolicy="no-referrer"||g' "$file"

  # === MERMAID ===
  sed -i 's|https://cdnjs\.cloudflare\.com/ajax/libs/mermaid/10\.[0-9.]*/mermaid\.min\.js|/vendor/mermaid/10.9.3/mermaid.min.js|g' "$file"
  sed -i 's|https://cdn\.jsdelivr\.net/npm/mermaid@10[^"]*mermaid\.min\.js|/vendor/mermaid/10.9.3/mermaid.min.js|g' "$file"
  sed -i "s|https://cdn\.jsdelivr\.net/npm/mermaid@10[^']*mermaid\.min\.js|/vendor/mermaid/10.9.3/mermaid.min.js|g" "$file"

  # === CHART.JS ===
  sed -i 's|https://cdn\.jsdelivr\.net/npm/chart\.js@3\.9\.1/dist/chart\.min\.js|/vendor/chartjs/3.9.1/chart.min.js|g' "$file"
  sed -i 's|https://cdn\.jsdelivr\.net/npm/chart\.js"|/vendor/chartjs/3.9.1/chart.min.js"|g' "$file"
  sed -i "s|https://cdn\.jsdelivr\.net/npm/chart\.js'|/vendor/chartjs/3.9.1/chart.min.js'|g" "$file"

  # === HTML2CANVAS ===
  sed -i 's|https://cdn\.jsdelivr\.net/npm/html2canvas@1\.4\.1/dist/html2canvas\.min\.js|/vendor/html2canvas/1.4.1/html2canvas.min.js|g' "$file"
  sed -i 's|https://cdnjs\.cloudflare\.com/ajax/libs/html2canvas/1\.4\.1/html2canvas\.min\.js|/vendor/html2canvas/1.4.1/html2canvas.min.js|g' "$file"
  sed -i 's|https://html2canvas\.hertzen\.com/dist/html2canvas\.min\.js|/vendor/html2canvas/1.4.1/html2canvas.min.js|g' "$file"

  # === JSPDF ===
  sed -i 's|https://cdn\.jsdelivr\.net/npm/jspdf@2\.5\.1/dist/jspdf\.umd\.min\.js|/vendor/jspdf/2.5.1/jspdf.umd.min.js|g' "$file"

  # === PICKR ===
  sed -i 's|https://cdn\.jsdelivr\.net/npm/@simonwep/pickr[^"]*pickr\.min\.js|/vendor/pickr/1.9.1/pickr.min.js|g' "$file"
  sed -i 's|https://cdn\.jsdelivr\.net/npm/@simonwep/pickr[^"]*monolith\.min\.css|/vendor/pickr/1.9.1/monolith.min.css|g' "$file"

  # === SVG-PAN-ZOOM ===
  sed -i 's|https://cdn\.jsdelivr\.net/npm/svg-pan-zoom@3\.6\.1/dist/svg-pan-zoom\.min\.js|/vendor/svg-pan-zoom/3.6.1/svg-pan-zoom.min.js|g' "$file"

  # === MATHJAX ===
  sed -i 's|https://cdn\.jsdelivr\.net/npm/mathjax@3/es5/|/vendor/mathjax/3.2.2/es5/|g' "$file"

  # === GOOGLE FONTS ===
  # Replace all Google Fonts CSS2 links with local (double-quoted)
  sed -i 's|https://fonts\.googleapis\.com/css2?[^"]*"|/vendor/fonts/google-fonts.css"|g' "$file"
  # Handle single-quoted href/URLs
  sed -i "s|https://fonts\.googleapis\.com/css2?[^']*'|/vendor/fonts/google-fonts.css'|g" "$file"
  # Handle @import url() with parentheses (no quotes inside url())
  sed -i 's|@import url(https://fonts\.googleapis\.com/css2[^)]*)|@import url(/vendor/fonts/google-fonts.css)|g' "$file"
  # Handle @import url('...') with single quotes inside url()
  sed -i "s|@import url('https://fonts\.googleapis\.com/css2[^']*')|@import url('/vendor/fonts/google-fonts.css')|g" "$file"

  # === REMOVE PRECONNECT HINTS (no longer needed for local files) ===
  sed -i '/<link rel="preconnect" href="https:\/\/fonts\.googleapis\.com"/d' "$file"
  sed -i '/<link rel="preconnect" href="https:\/\/fonts\.gstatic\.com"/d' "$file"

  # === REMOVE crossorigin on React/Babel script tags (not needed locally) ===
  sed -i 's| crossorigin||g' "$file"

done

echo ""
echo "=== Root HTML files processed ==="
echo ""

# Process tools/*.html
find tools -maxdepth 1 -name "*.html" | while read file; do
  echo "Processing: $file"

  # === TAILWIND ===
  sed -i 's|https://cdn\.tailwindcss\.com"|/vendor/tailwindcss/3.4.17/tailwind.js"|g' "$file"
  sed -i "s|https://cdn\.tailwindcss\.com'|/vendor/tailwindcss/3.4.17/tailwind.js'|g" "$file"
  sed -i 's|https://cdn\.tailwindcss\.com</|/vendor/tailwindcss/3.4.17/tailwind.js</|g' "$file"
  sed -i 's|src="https://cdn\.tailwindcss\.com">|src="/vendor/tailwindcss/3.4.17/tailwind.js">|g' "$file"

  # === LUCIDE ===
  sed -i 's|https://unpkg\.com/lucide@latest|/vendor/lucide/0.469.0/lucide.min.js|g' "$file"
  sed -i 's|https://unpkg\.com/lucide@[0-9.]*|/vendor/lucide/0.469.0/lucide.min.js|g' "$file"

  # === CHART.JS ===
  sed -i 's|https://cdn\.jsdelivr\.net/npm/chart\.js@3\.9\.1/dist/chart\.min\.js|/vendor/chartjs/3.9.1/chart.min.js|g' "$file"
  sed -i 's|https://cdn\.jsdelivr\.net/npm/chart\.js"|/vendor/chartjs/3.9.1/chart.min.js"|g' "$file"
  sed -i "s|https://cdn\.jsdelivr\.net/npm/chart\.js'|/vendor/chartjs/3.9.1/chart.min.js'|g" "$file"

  # === HTML2CANVAS ===
  sed -i 's|https://cdn\.jsdelivr\.net/npm/html2canvas@1\.4\.1/dist/html2canvas\.min\.js|/vendor/html2canvas/1.4.1/html2canvas.min.js|g' "$file"
  sed -i 's|https://cdnjs\.cloudflare\.com/ajax/libs/html2canvas/1\.4\.1/html2canvas\.min\.js|/vendor/html2canvas/1.4.1/html2canvas.min.js|g' "$file"
  sed -i 's|https://html2canvas\.hertzen\.com/dist/html2canvas\.min\.js|/vendor/html2canvas/1.4.1/html2canvas.min.js|g' "$file"

  # === JSPDF ===
  sed -i 's|https://cdn\.jsdelivr\.net/npm/jspdf@2\.5\.1/dist/jspdf\.umd\.min\.js|/vendor/jspdf/2.5.1/jspdf.umd.min.js|g' "$file"

  # === GOOGLE FONTS ===
  sed -i 's|https://fonts\.googleapis\.com/css2?[^"]*"|/vendor/fonts/google-fonts.css"|g' "$file"
  sed -i "s|https://fonts\.googleapis\.com/css2?[^']*'|/vendor/fonts/google-fonts.css'|g" "$file"
  sed -i 's|@import url(https://fonts\.googleapis\.com/css2[^)]*)|@import url(/vendor/fonts/google-fonts.css)|g' "$file"
  sed -i "s|@import url('https://fonts\.googleapis\.com/css2[^']*')|@import url('/vendor/fonts/google-fonts.css')|g" "$file"

  # === REMOVE PRECONNECT HINTS ===
  sed -i '/<link rel="preconnect" href="https:\/\/fonts\.googleapis\.com"/d' "$file"
  sed -i '/<link rel="preconnect" href="https:\/\/fonts\.gstatic\.com"/d' "$file"

  # === SRI / crossorigin cleanup ===
  sed -i 's| integrity="sha512-[^"]*"||g' "$file"
  sed -i 's| integrity="sha384-[^"]*"||g' "$file"
  sed -i 's| integrity="sha256-[^"]*"||g' "$file"
  sed -i 's| crossorigin="anonymous"||g' "$file"
  sed -i 's| crossorigin||g' "$file"
  sed -i 's| referrerpolicy="no-referrer"||g' "$file"

done

echo ""
echo "=== tools/ HTML files processed ==="
echo ""

# Process include/dir-header.html (same /vendor/ absolute path)
echo "Processing: include/dir-header.html"
file="./include/dir-header.html"
if [ -f "$file" ]; then
  sed -i 's|https://cdn\.tailwindcss\.com"|/vendor/tailwindcss/3.4.17/tailwind.js"|g' "$file"
  sed -i 's|src="https://cdn\.tailwindcss\.com">|src="/vendor/tailwindcss/3.4.17/tailwind.js">|g' "$file"
  sed -i 's|https://unpkg\.com/lucide@latest|/vendor/lucide/0.469.0/lucide.min.js|g' "$file"
  sed -i 's|https://fonts\.googleapis\.com/css2?[^"]*"|/vendor/fonts/google-fonts.css"|g' "$file"
  sed -i '/<link rel="preconnect" href="https:\/\/fonts\.googleapis\.com"/d' "$file"
  sed -i '/<link rel="preconnect" href="https:\/\/fonts\.gstatic\.com"/d' "$file"
fi

echo "=== All files processed ==="
