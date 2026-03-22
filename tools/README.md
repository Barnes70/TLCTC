# TLCTC Tools

Standalone, self-contained HTML applications that implement the TLCTC framework. No build system, no backend — open any file directly in a browser.

## Available Tools

| Tool | File | Description |
|------|------|-------------|
| **Threat Modeling** | [`threat-modeling.html`](threat-modeling.html) | Design threat models by placing components on a canvas, define interfaces, auto-assign threat clusters, generate threat registers and attack chain analysis |
| **Attack Path Architect** | [`attack-path-architect.html`](attack-path-architect.html) | Document cyber incidents as TLCTC attack paths with velocity analysis, MITRE/CVE references, DRE outcomes, and compliant JSON export for CTI exchange |
| **Actor Profile Designer** | [`actor-profile-designer.html`](actor-profile-designer.html) | Build threat actor capability profiles scored across all 10 TLCTC clusters, link observed incidents, compare actors side-by-side, and export for CTI sharing |
| **Threat Radar** | [`radar-tlctc-app.html`](radar-tlctc-app.html) | Interactive threat radar visualization with configurable sectors, zone thresholds, trend tracking (old vs current values), report/tolerance flags, and PNG export with optional legend |

## How to Use

1. Open the HTML file in any modern browser
2. No installation, no server, no API keys required
3. Models persist in browser `localStorage`
4. Export/import models as JSON for sharing

## Template Files

Starter templates are provided in [`examples/`](examples/) for each tool. Import them directly into the app or use them as a reference for building JSON programmatically.

| Template | For Tool | Description |
|----------|----------|-------------|
| [`template-attack-path.json`](examples/template-attack-path.json) | Attack Path Architect | 4-step phishing→credential→malware→exfil path with instructional descriptions |
| [`template-threat-model.json`](examples/template-threat-model.json) | Threat Modeling | 3-component web app (browser, API, database) with group, interfaces, and threat register |
| [`template-actor-profile.json`](examples/template-actor-profile.json) | Actor Profile Designer | 3 actor archetypes: blank template, nation-state APT, ransomware operator |

### Example Data Files

Real-world examples contributed by the community:

| File | For Tool | Content |
|------|----------|---------|
| [`CTA-CrowdStrike2025.json`](examples/CTA-CrowdStrike2025.json) | Actor Profile Designer | Threat actor profiles from CrowdStrike Global Threat Report 2025 |
| [`CTA-Google-APT-Groups.json`](examples/CTA-Google-APT-Groups.json) | Actor Profile Designer | APT group profiles from Google Threat Intelligence |
| [`npm-chalk-debug-phishing-2025.json`](examples/npm-chalk-debug-phishing-2025.json) | Attack Path Architect | Chalk/Debug npm phishing campaign (7 steps) |
| [`npm-s1ngularity-nx-2025.json`](examples/npm-s1ngularity-nx-2025.json) | Attack Path Architect | S1ngularity CI abuse via malicious nx packages (10 steps) |
| [`npm-shai-hulud-worm-2025.json`](examples/npm-shai-hulud-worm-2025.json) | Attack Path Architect | Shai-Hulud recursive worm propagation (14 steps) |
| [`ncsc-google-2024-JB-bericht.json`](examples/ncsc-google-2024-JB-bericht.json) | Threat Radar | Swiss NCSC/BACS 2024 annual report — national overview (CH vs Global) |
| [`ncsc-google-2024-JB-bericht-sectors.json`](examples/ncsc-google-2024-JB-bericht-sectors.json) | Threat Radar | Swiss NCSC 2024 — by industry sector (Financial, Government, IT, Healthcare, Telecom, Retail) |
| [`ncsc-google-2024-JB-bericht-actors.json`](examples/ncsc-google-2024-JB-bericht-actors.json) | Threat Radar | Swiss NCSC 2024 — by threat actor type (Criminals, APTs, Hacktivists) |
| [`ncsc-google-2024-JB-bericht-cia.json`](examples/ncsc-google-2024-JB-bericht-cia.json) | Threat Radar | Swiss NCSC 2024 — by CIA impact (Confidentiality, Integrity, Availability) |
| [`ncsc-google-2024-JB-bericht-it-types.json`](examples/ncsc-google-2024-JB-bericht-it-types.json) | Threat Radar | Swiss NCSC 2024 — by IT asset type (Servers, Endpoints, Network Devices, Cloud) |

---

## JSON Format Reference

Each tool uses a distinct JSON schema. Below are the key structures for programmatic integration.

### Attack Path Architect

**Schema identifier:** Internal format (compatible with `tlctc-attack-sequence.schema.json` on export)

```jsonc
{
  "title": "Incident Title",
  "metadata": {
    "sequence_id": "INC-YYYY-NNN",          // required
    "description": "...",
    "analyst": "Name",
    "organization": "Org",
    "threat_actor": {
      "name": "...",
      "motivation": "financial | espionage | hacktivism | destructive | unknown",
      "sophistication": "basic | intermediate | advanced | state-level"
    },
    "created": "ISO-8601",                   // required
    "modified": "ISO-8601",                  // required
    "framework_version": "2.1"               // required
  },
  "path": [                                  // required — array of steps
    {
      "id": 1,                               // unique step ID
      "cluster": 9,                          // 1–10, required
      "sphere": "Org | Vendor | Customer | External | Maintainer(Name)",
      "dtVal": "24",                         // delta-t value (optional)
      "dtUnit": "s | m | h | d | w",        // delta-t unit
      "velocityClass": "VC-1 | VC-2 | VC-3 | VC-4",
      "description": "...",                  // required
      "mitre": "T1566.002",                 // comma-separated MITRE TIDs
      "cve": "CVE-2024-XXXXX",              // comma-separated CVEs
      "confidence": "high | medium | low",
      "stage": "initial | intermediate | final",
      "boundary": {                          // required for bridge clusters #8, #9, #10
        "context": "human | physical | update | dev | auth | api | cloud",
        "source": "SphereA",
        "target": "SphereB",
        "transit": ["Carrier1"]              // optional, v2.1 transit parties
      },
      "intraBoundaries": [                   // optional, v2.1
        { "type": "sandbox | privilege | process | hypervisor", "from": "x", "to": "y" }
      ],
      "dre": {                               // Data Risk Event, optional
        "types": ["C", "I", "A", "Ac"],
        "title": "Short title",
        "desc": "Description"
      },
      "bizRisk": {                           // Business impact, optional
        "title": "Impact category",
        "desc": "Description"
      },
      "evidence": "Source citation"
    }
  ]
}
```

**Key rules:**
- One step = one cluster (Axiom VI). Split dual-cluster actions into separate steps or use `cluster2` for parallel execution.
- Credential use is always `cluster: 4` regardless of acquisition method (R-CRED).
- FEC execution requires a `cluster: 7` step at the execution moment (R-EXEC).
- Bridge clusters (#8, #9, #10) require a `boundary` object.

### Threat Modeling

**Schema identifier:** `tlctc-threat-identification-v2`

```jsonc
{
  "$schema": "tlctc-threat-identification-v2",
  "tlctc_version": "2.0",
  "metadata": {
    "name": "Project Name",                  // required
    "version": "1.0.0",                      // required
    "author": "Name",
    "sdlcPhase": "Design | Development | Testing | Operations | Deployment | Decommissioned",
    "description": "...",
    "created": "ISO-8601"
  },
  "system_model": {
    "groups": [{                             // container/trust zones
      "id": "unique-id",
      "name": "Group Name",
      "type": "group-server | group-container | group-pod",
      "position": { "x": 0, "y": 0 },
      "size": { "width": 500, "height": 300 },
      "metadata": {
        "owner": "@Org | @Vendor | @Customer | @User | ...",
        "isThirdParty": false,
        "environment": "Production | Staging | Development"
      }
    }],
    "components": [{                         // system components
      "id": "unique-id",
      "type": "api-endpoint | web-server | database | client-browser | ...",
      "name": "Component Name",
      "layer": "infrastructure | platform | runtime | application | library | external",
      "groupId": "parent-group-id | null",
      "position": { "x": 0, "y": 0 },
      "metadata": {
        "owner": "@Org | @Vendor | ...",
        "isThirdParty": false,
        "criticality": "Low | Medium | High | Critical"
      },
      "threats": [{
        "cluster": { "strategic": "#1", "operational": "TLCTC-01.00" },
        "applicable": true,
        "status": "Identified | Accepted | Mitigated | Verified",
        "velocity_class": "VC-1 | VC-2 | VC-3 | VC-4",
        "residual_risk": "Low | Medium | High | Critical",
        "notes": "Threat description",
        "control_ref": "Control reference"
      }]
    }],
    "interfaces": [{                         // connections between components
      "id": "unique-id",
      "name": "From → To",
      "from": "component-id",               // required
      "to": "component-id",                 // required
      "protocol": "HTTPS | TCP | WebSocket | ...",
      "port": "443",
      "clientComponentId": "id",
      "serverComponentId": "id",
      "crossesTrustBoundary": true,
      "sourceSphere": "@User",
      "targetSphere": "@Org",
      "threats": [/* same structure as component threats */]
    }]
  },
  "threat_register": [{                     // flattened threat list
    "elementType": "component | interface",
    "componentId": "id",
    "componentName": "Name",
    "cluster": "#1",
    "clusterName": "Abuse of Functions",
    "status": "Identified",
    "velocityClass": "VC-3",
    "residualRisk": "High",
    "notes": "...",
    "controlRef": ""
  }]
}
```

**Component types:** `vm`, `container`, `serverless`, `host`, `os-linux`, `os-windows`, `k8s-pod`, `runtime-node`, `runtime-jvm`, `runtime-python`, `runtime-dotnet`, `api-endpoint`, `web-server`, `app-logic`, `auth-module`, `file-handler`, `queue-consumer`, `db-client`, `http-client`, `auth-library`, `crypto-library`, `framework`, `orm`, `database`, `cache`, `queue`, `storage`, `idp`, `third-party-api`, `cdn`, `user`, `admin`, `client-browser`, `client-mobile`

### Actor Profile Designer

**Schema identifier:** `tlctc-actor-profile.v2`

```jsonc
{
  "schema_version": "tlctc-actor-profile.v2",
  "score_scale": "1=Low,2=Medium,3=High,4=Champion",
  "exported_at": "ISO-8601",
  "actors": [{
    "threat_actor": "Actor Name",            // required
    "tlctc_scores": {                        // required — capability per cluster
      "TLCTC-01.00": 1,                     // 1=Low, 2=Medium, 3=High, 4=Champion
      "TLCTC-02.00": 1,
      "TLCTC-03.00": 1,
      "TLCTC-04.00": 1,
      "TLCTC-05.00": 1,
      "TLCTC-06.00": 1,
      "TLCTC-07.00": 1,
      "TLCTC-08.00": 1,
      "TLCTC-09.00": 1,
      "TLCTC-10.00": 1
    },
    "notes": "Operational profile summary",
    "sources": ["Intelligence source"],
    "sequence": "#09 → #04 → #07",          // typical attack chain notation
    "last_updated": "YYYY-MM-DD",
    "origin_country": "Country or Unknown",
    "motivation": ["Financial Gain", "Espionage", "Hacktivism", "Destructive"],
    "target_sectors": ["Technology", "Financial Services"],
    "observed_paths": [{                     // linked incident data, optional
      "incident_id": "INC-YYYY-NNN",
      "notation": "#9 → #4 → #7 + [DRE: C]",
      "cluster_sequence": [9, 4, 7],
      "dre_outcomes": { "C": 1, "I": 0, "A": 0, "Ac": 0 }
    }]
  }]
}
```

**Alternate score formats accepted on import:**
- Object with `cluster_01` … `cluster_10` keys
- Array of 10 integers: `[3, 1, 1, 2, 1, 1, 3, 1, 4, 1]`

### Threat Radar

**Format:** Radar configuration JSON (import/export via the Data toolbar)

```jsonc
{
  "sectors": [{                                // one sector = one ring on the radar
    "id": "unique-id",
    "name": "Sector Name",                    // displayed around the radar
    "color": "#e74c3c",                       // bubble/line color
    "backgroundColor": "rgba(R,G,B,A)",       // sector background fill
    "activeThreats": {                         // which clusters are enabled (keyed 1–10)
      "1": true, "2": true, /* ... */ "10": true
    },
    "values": {                                // current threat levels per cluster (0–100)
      "1": 13, "2": 11, /* ... */ "10": 16
    },
    "oldValues": {                             // previous period values for trend comparison
      "1": 12, "2": 7, /* ... */ "10": 11
    },
    "zoneLimits": {                            // per-cluster zone thresholds
      "1": { "latent": 0, "low": 10, "medium": 16, "high": 26 },
      // ... one entry per cluster
    },
    "toBeReported": { "1": false, /* ... */ }, // report flag (!) per cluster
    "riskToleranceCrashed": { "1": false },    // tolerance flag (⚡) per cluster
    "collapsed": false                         // editor panel state
  }],
  // Optional global settings (included on export):
  "radarBgColor": "#FFFFFF",                   // radar canvas background
  "radarTextColor": "#111827",                 // sector name / line color
  "zoneLabelColor": "#374151",                 // zone name label color
  "zoneLineStyle": "dashed",                   // dashed | solid | dotted
  "radarShape": "full",                        // full (360°) | half (180°)
  "clusterDisplayMode": "name",                // name | number | both
  "zoneSizeMultipliers": {                     // bubble size per zone
    "latent": 0.8, "low": 0.9, "medium": 1.05, "high": 1.2
  },
  "oldBubbleSizeMultiplier": 0.8,              // trend bubble relative size
  "threatClustersData": [/* cluster definitions with custom shortNames */]
}
```

**Key concepts:**
- Each **sector** is an independent ring on the radar (e.g., "Financial Services", "Government", or "Confidentiality Impact").
- **values** vs **oldValues** enable trend visualization — current bubbles are filled, old bubbles are outlined.
- **zoneLimits** define the thresholds that place bubbles into latent/low/medium/high zones per cluster.
- **Flags** mark clusters for special attention: `toBeReported` (!) and `riskToleranceCrashed` (⚡).
- Multiple analytical perspectives from one report (by sector, by actor, by CIA, by asset type) are modeled as separate JSON files with different sector configurations.

## Technology

All tools are single-file HTML applications using:
- React (via CDN)
- Tailwind CSS
- SVG rendering
- Browser localStorage for persistence

## License

CC BY 4.0 — See [LICENSE](../LICENSE).
