# TLCTC Tools

Standalone, self-contained HTML applications that implement the TLCTC framework. No build system, no backend — open any file directly in a browser.

## Available Tools

| Tool | File | Description |
|------|------|-------------|
| **Threat Modeling** | [`threat-modeling.html`](threat-modeling.html) | Design threat models by placing components on a canvas, define interfaces, auto-assign threat clusters, generate threat registers and attack chain analysis |
| **Attack Path Architect** | [`attack-path-architect.html`](attack-path-architect.html) | Document cyber incidents as TLCTC attack paths with velocity analysis, MITRE/CVE references, DRE outcomes, and compliant JSON export for CTI exchange |

## How to Use

1. Open the HTML file in any modern browser
2. No installation, no server, no API keys required
3. Models persist in browser `localStorage`
4. Export/import models as JSON for sharing

## Technology

All tools are single-file HTML applications using:
- React (via CDN)
- Tailwind CSS
- SVG rendering
- Browser localStorage for persistence

## License

CC BY 4.0 — See [LICENSE](../LICENSE).
