# SARIF + Sigma TLCTC Integrations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship two TLCTC integrations — a generic SARIF→TLCTC classifier CLI (`integrations/sarif/`) and a static Sigma→TLCTC data mapping (`mappings/sigma/`) — each joining external tool output against canonical mapping tables already in this repo.

**Architecture:** Phase 1 is a standalone, stdlib-only Python CLI that parses any SARIF 2.1.0 file, extracts CWE/CVE identifiers, classifies CWE-first against `mappings/mitre-cwe/tlctc-cwe.json` with a CVE→KEV fallback against `mappings/cisa-kev/tlctc-kev.json`, resolves `#2|#3` ambiguity via R-ROLE file-path globs, and emits JSON/Markdown/enriched-SARIF. Phase 2 is a maintainer build script (PyYAML, build-time only) that walks SigmaHQ rules, reads their ATT&CK tags, joins `mappings/mitre-attack-enterprise/tlctc-enterprise-attack.json`, and writes a committed `tlctc-sigma.json` snapshot + stats (output is pure JSON; consumers need nothing).

**Tech Stack:** Python 3.11+ (3.10-compatible config variant), stdlib only for the SARIF CLI (`json`, `argparse`, `fnmatch`, `pathlib`, `tomllib`), `unittest` for tests; PyYAML for the Sigma generator only.

**Conventions for every task:**
- Run tests from the pack root. SARIF: `cd integrations/sarif && python -m unittest discover tests -v`. Sigma: `cd mappings/sigma && python -m unittest discover tests -v`.
- `primaryCluster` selection rule (locked): when a finding/rule resolves to multiple candidate clusters, `primaryCluster` is the **lowest-numbered** cluster in the resolved set; `clusterSet` preserves all candidates. This is deterministic and matches nothing in KEV that contradicts it.
- Commit after each task with the message shown in its final step.

---

## Phase 1 — `integrations/sarif/` (generic SARIF → TLCTC classifier)

### File structure (Phase 1)

| File | Responsibility |
|---|---|
| `integrations/sarif/cli/config.py` | Load TOML/JSON config + env precedence; resolve canonical mapping paths |
| `integrations/sarif/cli/mapping_loader.py` | Load + index `tlctc-cwe.json` (by CWE-N) and `tlctc-kev.json` (by CVE) |
| `integrations/sarif/cli/sarif_loader.py` | Parse `runs[].results[]`, extract `{cwe,cve}` per finding |
| `integrations/sarif/cli/context_resolver.py` | R-ROLE: pick `#2` vs `#3` from file-URI globs |
| `integrations/sarif/cli/classifier.py` | Resolution ladder → `ClassifiedFinding` with provenance |
| `integrations/sarif/cli/reporters/json_report.py` | Cluster summary + per-finding JSON |
| `integrations/sarif/cli/reporters/markdown_report.py` | PR-comment Markdown |
| `integrations/sarif/cli/reporters/sarif_report.py` | TLCTC-enriched SARIF 2.1.0 |
| `integrations/sarif/cli/tlctc_sarif.py` | argparse dispatch, `classify`, `--fail-on-cluster` |
| `integrations/sarif/tests/*` | unit + golden tests |
| `integrations/sarif/examples/*` | config + golden SARIF in/out fixtures |
| `integrations/sarif/{README,deploy,test-cases}.md`, `pack_metadata.json`, `ReleaseNotes/1_0_0.md` | docs/metadata |

---

### Task 1: Scaffold package + config loader

**Files:**
- Create: `integrations/sarif/cli/__init__.py`
- Create: `integrations/sarif/cli/__main__.py`
- Create: `integrations/sarif/cli/config.py`
- Create: `integrations/sarif/tests/__init__.py`
- Test: `integrations/sarif/tests/test_config.py`

- [ ] **Step 1: Create empty package markers**

`integrations/sarif/cli/__init__.py`:
```python
"""TLCTC SARIF classifier — standalone, stdlib-only."""
__version__ = "1.0.0"
```

`integrations/sarif/cli/__main__.py`:
```python
from cli.tlctc_sarif import main

if __name__ == "__main__":
    raise SystemExit(main())
```

`integrations/sarif/tests/__init__.py`: empty file.

- [ ] **Step 2: Write the failing test**

`integrations/sarif/tests/test_config.py`:
```python
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from cli.config import Config, load_config


class TestConfig(unittest.TestCase):
    def test_defaults_resolve_repo_mappings(self):
        cfg = load_config(None)
        self.assertTrue(cfg.cwe_mapping_path.name == "tlctc-cwe.json")
        self.assertTrue(cfg.kev_mapping_path.name == "tlctc-kev.json")
        self.assertEqual(cfg.formats, ["json"])

    def test_json_config_overrides(self):
        with TemporaryDirectory() as d:
            p = Path(d) / "c.json"
            p.write_text(json.dumps({
                "formats": ["json", "markdown"],
                "source_globs": {"server": ["**/api/**"], "client": ["**/ui/**"]},
            }))
            cfg = load_config(p)
            self.assertEqual(cfg.formats, ["json", "markdown"])
            self.assertEqual(cfg.source_globs["server"], ["**/api/**"])

    def test_env_overrides_format(self):
        import os
        os.environ["TLCTC_SARIF_FORMATS"] = "sarif"
        try:
            cfg = load_config(None)
            self.assertEqual(cfg.formats, ["sarif"])
        finally:
            del os.environ["TLCTC_SARIF_FORMATS"]


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd integrations/sarif && python -m unittest tests.test_config -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'cli.config'`

- [ ] **Step 4: Write minimal implementation**

`integrations/sarif/cli/config.py`:
```python
"""Config loading: TOML or JSON file, env-var precedence, repo-relative defaults."""
import json
import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

# integrations/sarif/cli/config.py -> repo root is 3 parents up.
_REPO_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_CWE = _REPO_ROOT / "mappings" / "mitre-cwe" / "tlctc-cwe.json"
_DEFAULT_KEV = _REPO_ROOT / "mappings" / "cisa-kev" / "tlctc-kev.json"


@dataclass
class Config:
    cwe_mapping_path: Path = _DEFAULT_CWE
    kev_mapping_path: Path = _DEFAULT_KEV
    formats: list = field(default_factory=lambda: ["json"])
    source_globs: dict = field(default_factory=lambda: {"server": [], "client": []})
    fail_on_cluster: list = field(default_factory=list)


def _read_file(path: Path) -> dict:
    if path.suffix == ".toml":
        if tomllib is None:
            raise RuntimeError("TOML config requires Python 3.11+; use a .json config")
        return tomllib.loads(path.read_text(encoding="utf-8"))
    return json.loads(path.read_text(encoding="utf-8"))


def load_config(path) -> Config:
    data = _read_file(Path(path)) if path else {}
    cfg = Config()
    if "cwe_mapping_path" in data:
        cfg.cwe_mapping_path = Path(data["cwe_mapping_path"])
    if "kev_mapping_path" in data:
        cfg.kev_mapping_path = Path(data["kev_mapping_path"])
    if "formats" in data:
        cfg.formats = list(data["formats"])
    if "source_globs" in data:
        cfg.source_globs = {
            "server": list(data["source_globs"].get("server", [])),
            "client": list(data["source_globs"].get("client", [])),
        }
    if "fail_on_cluster" in data:
        cfg.fail_on_cluster = list(data["fail_on_cluster"])
    env_formats = os.environ.get("TLCTC_SARIF_FORMATS")
    if env_formats:
        cfg.formats = [f.strip() for f in env_formats.split(",") if f.strip()]
    return cfg
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd integrations/sarif && python -m unittest tests.test_config -v`
Expected: PASS (3 tests)

- [ ] **Step 6: Commit**

```bash
git add integrations/sarif/cli integrations/sarif/tests
git commit -m "feat(sarif): scaffold package and config loader"
```

---

### Task 2: Mapping loader (CWE + KEV indexes)

**Files:**
- Create: `integrations/sarif/cli/mapping_loader.py`
- Create: `integrations/sarif/tests/fixtures/tiny-cwe.json`
- Create: `integrations/sarif/tests/fixtures/tiny-kev.json`
- Test: `integrations/sarif/tests/test_mapping_loader.py`

- [ ] **Step 1: Create test fixtures**

`integrations/sarif/tests/fixtures/tiny-cwe.json`:
```json
{
  "metadata": {"title": "tiny"},
  "mappings": [
    {"cweId": "CWE-89", "tlctcMapping": "#2", "tlctcMappingName": "Exploiting Server", "mappingVerdict": "Allowed", "contextDependent": false},
    {"cweId": "CWE-79", "tlctcMapping": "#2 | #3", "tlctcMappingName": "Exploiting Server | Exploiting Client", "mappingVerdict": "Allowed-with-Review", "contextDependent": true},
    {"cweId": "CWE-20", "tlctcMapping": "#1", "tlctcMappingName": "Abuse of Functions", "mappingVerdict": "Discouraged", "contextDependent": false},
    {"cweId": "CWE-0", "tlctcMapping": "N/A", "tlctcMappingName": "Unmapped", "mappingVerdict": "Prohibited", "contextDependent": false}
  ]
}
```

`integrations/sarif/tests/fixtures/tiny-kev.json`:
```json
{
  "metadata": {"title": "tiny"},
  "mappings": [
    {"cveID": "CVE-2021-44228", "primaryCluster": "#2", "clusterSet": ["#2"], "confidence": "Allowed-with-Review", "sourceCwes": ["CWE-502"]}
  ]
}
```

- [ ] **Step 2: Write the failing test**

`integrations/sarif/tests/test_mapping_loader.py`:
```python
import unittest
from pathlib import Path

from cli.mapping_loader import MappingLoader

FIX = Path(__file__).resolve().parent / "fixtures"


class TestMappingLoader(unittest.TestCase):
    def setUp(self):
        self.ml = MappingLoader(FIX / "tiny-cwe.json", FIX / "tiny-kev.json")

    def test_cwe_lookup_returns_entry(self):
        e = self.ml.cwe("CWE-89")
        self.assertEqual(e["tlctcMapping"], "#2")
        self.assertEqual(e["mappingVerdict"], "Allowed")

    def test_cwe_lookup_case_insensitive_and_normalized(self):
        self.assertIsNotNone(self.ml.cwe("cwe-89"))
        self.assertIsNotNone(self.ml.cwe("89"))

    def test_cwe_missing_returns_none(self):
        self.assertIsNone(self.ml.cwe("CWE-99999"))

    def test_kev_lookup(self):
        e = self.ml.kev("CVE-2021-44228")
        self.assertEqual(e["primaryCluster"], "#2")

    def test_kev_missing_returns_none(self):
        self.assertIsNone(self.ml.kev("CVE-0000-0000"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd integrations/sarif && python -m unittest tests.test_mapping_loader -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'cli.mapping_loader'`

- [ ] **Step 4: Write minimal implementation**

`integrations/sarif/cli/mapping_loader.py`:
```python
"""Loads and indexes the canonical CWE→TLCTC and KEV→TLCTC mappings."""
import json
import re
from pathlib import Path

_CWE_RE = re.compile(r"(?:cwe[-_]?)?(\d+)", re.IGNORECASE)


def normalize_cwe(raw: str):
    """'cwe-89', 'CWE_89', '89' → 'CWE-89'. Returns None if not a CWE token."""
    if raw is None:
        return None
    m = _CWE_RE.fullmatch(str(raw).strip())
    return f"CWE-{int(m.group(1))}" if m else None


class MappingLoader:
    def __init__(self, cwe_path: Path, kev_path: Path):
        cwe_doc = json.loads(Path(cwe_path).read_text(encoding="utf-8"))
        kev_doc = json.loads(Path(kev_path).read_text(encoding="utf-8"))
        self._cwe = {e["cweId"].upper(): e for e in cwe_doc["mappings"]}
        self._kev = {e["cveID"].upper(): e for e in kev_doc["mappings"]}

    def cwe(self, token: str):
        norm = normalize_cwe(token)
        return self._cwe.get(norm.upper()) if norm else None

    def kev(self, cve_id: str):
        if not cve_id:
            return None
        return self._kev.get(str(cve_id).strip().upper())
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd integrations/sarif && python -m unittest tests.test_mapping_loader -v`
Expected: PASS (5 tests)

- [ ] **Step 6: Commit**

```bash
git add integrations/sarif/cli/mapping_loader.py integrations/sarif/tests
git commit -m "feat(sarif): add CWE+KEV mapping loader with normalization"
```

---

### Task 3: SARIF loader (identifier extraction)

**Files:**
- Create: `integrations/sarif/cli/sarif_loader.py`
- Create: `integrations/sarif/tests/fixtures/semgrep-min.sarif`
- Create: `integrations/sarif/tests/fixtures/trivy-min.sarif`
- Test: `integrations/sarif/tests/test_sarif_loader.py`

- [ ] **Step 1: Create minimal SARIF fixtures (two producer shapes)**

`integrations/sarif/tests/fixtures/semgrep-min.sarif` (CWE via `taxa`/`properties.cwe`):
```json
{
  "version": "2.1.0",
  "runs": [{
    "tool": {"driver": {"name": "Semgrep", "rules": [
      {"id": "sqli", "properties": {"cwe": ["CWE-89: SQL Injection"]}}
    ]}},
    "results": [{
      "ruleId": "sqli",
      "message": {"text": "SQL injection"},
      "locations": [{"physicalLocation": {"artifactLocation": {"uri": "src/api/users.py"}}}]
    }]
  }]
}
```

`integrations/sarif/tests/fixtures/trivy-min.sarif` (CVE via `ruleId`/`properties.cve`, no CWE):
```json
{
  "version": "2.1.0",
  "runs": [{
    "tool": {"driver": {"name": "Trivy", "rules": [
      {"id": "CVE-2021-44228", "properties": {"cve": "CVE-2021-44228"}}
    ]}},
    "results": [{
      "ruleId": "CVE-2021-44228",
      "message": {"text": "log4shell"},
      "locations": [{"physicalLocation": {"artifactLocation": {"uri": "pom.xml"}}}]
    }]
  }]
}
```

- [ ] **Step 2: Write the failing test**

`integrations/sarif/tests/test_sarif_loader.py`:
```python
import unittest
from pathlib import Path

from cli.sarif_loader import load_findings

FIX = Path(__file__).resolve().parent / "fixtures"


class TestSarifLoader(unittest.TestCase):
    def test_semgrep_extracts_cwe_and_uri(self):
        findings = load_findings(FIX / "semgrep-min.sarif")
        self.assertEqual(len(findings), 1)
        f = findings[0]
        self.assertIn("CWE-89", f.cwe)
        self.assertEqual(f.cve, [])
        self.assertEqual(f.uri, "src/api/users.py")
        self.assertEqual(f.tool, "Semgrep")

    def test_trivy_extracts_cve_no_cwe(self):
        findings = load_findings(FIX / "trivy-min.sarif")
        f = findings[0]
        self.assertEqual(f.cwe, [])
        self.assertIn("CVE-2021-44228", f.cve)

    def test_ruleid_cwe_heuristic(self):
        # ruleId like external/cwe/cwe-79 is mined when no properties present
        findings = load_findings(FIX / "semgrep-min.sarif")
        self.assertTrue(all(hasattr(f, "rule_id") for f in findings))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd integrations/sarif && python -m unittest tests.test_sarif_loader -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'cli.sarif_loader'`

- [ ] **Step 4: Write minimal implementation**

`integrations/sarif/cli/sarif_loader.py`:
```python
"""Parse a SARIF 2.1.0 file into Findings, extracting CWE/CVE identifiers.

Producer variance (Semgrep, CodeQL, Trivy, Grype, Bandit, gosec) is absorbed
here: identifiers are mined from taxa, rule relationships, properties, tags,
and ruleId heuristics, in priority order.
"""
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

_CWE_TOKEN = re.compile(r"CWE[-_]?(\d+)", re.IGNORECASE)
_CVE_TOKEN = re.compile(r"CVE-\d{4}-\d{4,}", re.IGNORECASE)


@dataclass
class Finding:
    rule_id: str
    message: str
    uri: str
    tool: str
    cwe: list = field(default_factory=list)
    cve: list = field(default_factory=list)


def _mine(text):
    cwes = [f"CWE-{int(m.group(1))}" for m in _CWE_TOKEN.finditer(text or "")]
    cves = [m.group(0).upper() for m in _CVE_TOKEN.finditer(text or "")]
    return cwes, cves


def _collect_strings(obj):
    """Yield all string scalars under a JSON value (for taxa/properties mining)."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _collect_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _collect_strings(v)


def load_findings(path: Path):
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    findings = []
    for run in doc.get("runs", []):
        driver = run.get("tool", {}).get("driver", {})
        tool = driver.get("name", "unknown")
        rules_by_id = {r.get("id"): r for r in driver.get("rules", [])}
        for res in run.get("results", []):
            rule_id = res.get("ruleId", "")
            rule = rules_by_id.get(rule_id, {})
            uri = ""
            locs = res.get("locations", [])
            if locs:
                uri = locs[0].get("physicalLocation", {}).get(
                    "artifactLocation", {}).get("uri", "")
            cwes, cves = set(), set()
            # Mine result properties/tags, rule properties, taxa, and the ruleId.
            for src in (res.get("properties"), res.get("taxa"),
                        rule.get("properties"), rule.get("relationships"),
                        run.get("taxonomies"), rule_id):
                for s in _collect_strings(src):
                    c, v = _mine(s)
                    cwes.update(c)
                    cves.update(v)
            findings.append(Finding(
                rule_id=rule_id,
                message=res.get("message", {}).get("text", ""),
                uri=uri,
                tool=tool,
                cwe=sorted(cwes),
                cve=sorted(cves),
            ))
    return findings
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd integrations/sarif && python -m unittest tests.test_sarif_loader -v`
Expected: PASS (3 tests)

- [ ] **Step 6: Commit**

```bash
git add integrations/sarif/cli/sarif_loader.py integrations/sarif/tests
git commit -m "feat(sarif): add SARIF loader with multi-producer identifier extraction"
```

---

### Task 4: R-ROLE context resolver

**Files:**
- Create: `integrations/sarif/cli/context_resolver.py`
- Test: `integrations/sarif/tests/test_context_resolver.py`

- [ ] **Step 1: Write the failing test**

`integrations/sarif/tests/test_context_resolver.py`:
```python
import unittest

from cli.context_resolver import resolve_role


class TestContextResolver(unittest.TestCase):
    def setUp(self):
        self.globs = {"server": ["**/api/**", "**/server/**"], "client": ["**/ui/**", "**/*.html"]}

    def test_server_path_picks_2(self):
        cluster, reason = resolve_role("src/api/users.py", self.globs)
        self.assertEqual(cluster, "#2")
        self.assertIn("server", reason)

    def test_client_path_picks_3(self):
        cluster, reason = resolve_role("web/ui/login.html", self.globs)
        self.assertEqual(cluster, "#3")

    def test_no_match_returns_none(self):
        cluster, reason = resolve_role("misc/readme.txt", self.globs)
        self.assertIsNone(cluster)
        self.assertIn("unresolved", reason)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd integrations/sarif && python -m unittest tests.test_context_resolver -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'cli.context_resolver'`

- [ ] **Step 3: Write minimal implementation**

`integrations/sarif/cli/context_resolver.py`:
```python
"""R-ROLE: resolve a '#2 | #3' alternation from the finding's file path.

server-role glob match → #2 (Exploiting Server); client-role → #3
(Exploiting Client). Returns (cluster_or_None, human_reason).
"""
from fnmatch import fnmatch


def _matches(uri, patterns):
    return any(fnmatch(uri, p) for p in patterns)


def resolve_role(uri: str, source_globs: dict):
    server = source_globs.get("server", [])
    client = source_globs.get("client", [])
    s, c = _matches(uri, server), _matches(uri, client)
    if s and not c:
        return "#2", f"server-role: '{uri}' matched a server glob (R-ROLE → #2)"
    if c and not s:
        return "#3", f"client-role: '{uri}' matched a client glob (R-ROLE → #3)"
    return None, f"unresolved: '{uri}' matched no (or both) role globs"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd integrations/sarif && python -m unittest tests.test_context_resolver -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add integrations/sarif/cli/context_resolver.py integrations/sarif/tests/test_context_resolver.py
git commit -m "feat(sarif): add R-ROLE context resolver"
```

---

### Task 5: Classifier (resolution ladder + provenance)

**Files:**
- Create: `integrations/sarif/cli/classifier.py`
- Test: `integrations/sarif/tests/test_classifier.py`

- [ ] **Step 1: Write the failing test**

`integrations/sarif/tests/test_classifier.py`:
```python
import unittest
from pathlib import Path

from cli.classifier import classify
from cli.mapping_loader import MappingLoader
from cli.sarif_loader import Finding

FIX = Path(__file__).resolve().parent / "fixtures"


class TestClassifier(unittest.TestCase):
    def setUp(self):
        self.ml = MappingLoader(FIX / "tiny-cwe.json", FIX / "tiny-kev.json")
        self.globs = {"server": ["**/api/**"], "client": ["**/ui/**"]}

    def _classify(self, finding):
        return classify(finding, self.ml, self.globs)

    def test_allowed_cwe_classifies(self):
        r = self._classify(Finding("sqli", "m", "src/api/u.py", "Semgrep", cwe=["CWE-89"]))
        self.assertEqual(r.primary_cluster, "#2")
        self.assertEqual(r.status, "classified")
        self.assertEqual(r.provenance["table"], "tlctc-cwe")
        self.assertEqual(r.provenance["identifier"], "CWE-89")

    def test_alternation_resolved_by_rrole(self):
        r = self._classify(Finding("xss", "m", "src/api/u.py", "Semgrep", cwe=["CWE-79"]))
        self.assertEqual(r.primary_cluster, "#2")  # api path → server
        self.assertIn("server-role", r.role_reason)

    def test_discouraged_is_low_confidence(self):
        r = self._classify(Finding("v", "m", "x.py", "Semgrep", cwe=["CWE-20"]))
        self.assertEqual(r.status, "low_confidence")

    def test_prohibited_is_skipped(self):
        r = self._classify(Finding("v", "m", "x.py", "Semgrep", cwe=["CWE-0"]))
        self.assertEqual(r.status, "skipped")

    def test_cve_fallback_via_kev(self):
        r = self._classify(Finding("log4shell", "m", "pom.xml", "Trivy", cve=["CVE-2021-44228"]))
        self.assertEqual(r.primary_cluster, "#2")
        self.assertEqual(r.provenance["table"], "tlctc-kev")

    def test_unmapped(self):
        r = self._classify(Finding("x", "m", "x.py", "Trivy", cve=["CVE-0000-0000"]))
        self.assertEqual(r.status, "unmapped")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd integrations/sarif && python -m unittest tests.test_classifier -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'cli.classifier'`

- [ ] **Step 3: Write minimal implementation**

`integrations/sarif/cli/classifier.py`:
```python
"""Resolution ladder: Finding → ClassifiedFinding.

CWE-first (verdict-filtered) against tlctc-cwe.json, then CVE→KEV fallback,
else unmapped. '#2 | #3' alternations are resolved by R-ROLE. Every result
carries a provenance record so the cluster assignment is auditable.
"""
import re
from dataclasses import dataclass, field

from cli.context_resolver import resolve_role

_CLUSTER_RE = re.compile(r"#(\d+)")

# Allowed / Allowed-with-Review classify; Discouraged → low-confidence;
# Prohibited / N/A → skipped.
_CLASSIFY_VERDICTS = {"Allowed", "Allowed-with-Review"}


@dataclass
class ClassifiedFinding:
    finding: object
    status: str                      # classified|low_confidence|skipped|unmapped
    primary_cluster: str = None
    cluster_set: list = field(default_factory=list)
    role_reason: str = ""
    provenance: dict = field(default_factory=dict)


def _clusters(expr: str):
    """'#2 | #3' → ['#2','#3']; lowest-numbered first for primary selection."""
    nums = sorted(int(n) for n in _CLUSTER_RE.findall(expr or ""))
    return [f"#{n}" for n in nums]


def _pick_primary(cluster_set, finding, globs):
    if len(cluster_set) <= 1:
        return (cluster_set[0] if cluster_set else None), ""
    # Multiple candidates → try R-ROLE on #2|#3, else lowest-numbered.
    if set(cluster_set) == {"#2", "#3"}:
        cluster, reason = resolve_role(finding.uri, globs)
        if cluster:
            return cluster, reason
        return cluster_set[0], reason  # lowest-numbered fallback
    return cluster_set[0], "multi-cluster: lowest-numbered chosen as primary"


def classify(finding, mapping_loader, source_globs) -> ClassifiedFinding:
    # 1. CWE-first.
    for cwe in finding.cwe:
        entry = mapping_loader.cwe(cwe)
        if not entry:
            continue
        verdict = entry.get("mappingVerdict", "Unreviewed")
        cset = _clusters(entry.get("tlctcMapping", ""))
        prov = {"identifier": cwe, "table": "tlctc-cwe", "verdict": verdict}
        if not cset:  # N/A
            return ClassifiedFinding(finding, "skipped", provenance=prov)
        if verdict in _CLASSIFY_VERDICTS:
            primary, reason = _pick_primary(cset, finding, source_globs)
            return ClassifiedFinding(finding, "classified", primary, cset, reason, prov)
        if verdict == "Discouraged":
            primary, reason = _pick_primary(cset, finding, source_globs)
            return ClassifiedFinding(finding, "low_confidence", primary, cset, reason, prov)
        return ClassifiedFinding(finding, "skipped", provenance=prov)  # Prohibited
    # 2. CVE → KEV fallback.
    for cve in finding.cve:
        entry = mapping_loader.kev(cve)
        if entry:
            prov = {"identifier": cve, "table": "tlctc-kev",
                    "confidence": entry.get("confidence")}
            return ClassifiedFinding(
                finding, "classified", entry.get("primaryCluster"),
                entry.get("clusterSet", []), "", prov)
    # 3. Unmapped.
    return ClassifiedFinding(finding, "unmapped")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd integrations/sarif && python -m unittest tests.test_classifier -v`
Expected: PASS (6 tests)

- [ ] **Step 5: Commit**

```bash
git add integrations/sarif/cli/classifier.py integrations/sarif/tests/test_classifier.py
git commit -m "feat(sarif): add classifier resolution ladder with provenance"
```

---

### Task 6: Reporters (JSON, Markdown, enriched SARIF)

**Files:**
- Create: `integrations/sarif/cli/reporters/__init__.py`
- Create: `integrations/sarif/cli/reporters/json_report.py`
- Create: `integrations/sarif/cli/reporters/markdown_report.py`
- Create: `integrations/sarif/cli/reporters/sarif_report.py`
- Test: `integrations/sarif/tests/test_reporters.py`

- [ ] **Step 1: Write the failing test**

`integrations/sarif/tests/test_reporters.py`:
```python
import json
import unittest

from cli.classifier import ClassifiedFinding
from cli.sarif_loader import Finding
from cli.reporters import json_report, markdown_report, sarif_report


def _sample():
    return [
        ClassifiedFinding(Finding("sqli", "SQLi", "src/api/u.py", "Semgrep", cwe=["CWE-89"]),
                          "classified", "#2", ["#2"], "",
                          {"identifier": "CWE-89", "table": "tlctc-cwe", "verdict": "Allowed"}),
        ClassifiedFinding(Finding("v", "weak", "x.py", "Semgrep", cwe=["CWE-20"]),
                          "low_confidence", "#1", ["#1"], "",
                          {"identifier": "CWE-20", "table": "tlctc-cwe", "verdict": "Discouraged"}),
        ClassifiedFinding(Finding("x", "u", "x.py", "Trivy", cve=["CVE-0000-0000"]), "unmapped"),
    ]


class TestReporters(unittest.TestCase):
    def test_json_has_summary_and_buckets(self):
        out = json.loads(json_report.render(_sample()))
        self.assertEqual(out["cluster_summary"]["#2"], 1)
        self.assertEqual(len(out["findings"]), 1)
        self.assertEqual(len(out["low_confidence"]), 1)
        self.assertEqual(len(out["unmapped"]), 1)

    def test_markdown_has_cluster_table(self):
        md = markdown_report.render(_sample())
        self.assertIn("| Cluster |", md)
        self.assertIn("#2", md)
        self.assertIn("Low-confidence", md)

    def test_sarif_injects_taxonomy_and_properties(self):
        out = json.loads(sarif_report.render(_sample()))
        run = out["runs"][0]
        self.assertTrue(any(t["name"] == "TLCTC" for t in run["taxonomies"]))
        self.assertEqual(run["results"][0]["properties"]["tlctc"]["cluster"], "#2")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd integrations/sarif && python -m unittest tests.test_reporters -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'cli.reporters'`

- [ ] **Step 3: Write minimal implementations**

`integrations/sarif/cli/reporters/__init__.py`:
```python
from collections import Counter


def cluster_summary(classified):
    c = Counter()
    for r in classified:
        if r.status == "classified" and r.primary_cluster:
            c[r.primary_cluster] += 1
    # Lowest-numbered cluster first for stable output.
    return dict(sorted(c.items(), key=lambda kv: int(kv[0][1:])))
```

`integrations/sarif/cli/reporters/json_report.py`:
```python
import json

from cli.reporters import cluster_summary


def _finding_dict(r):
    f = r.finding
    return {
        "rule_id": f.rule_id, "tool": f.tool, "uri": f.uri, "message": f.message,
        "cwe": f.cwe, "cve": f.cve,
        "primary_cluster": r.primary_cluster, "cluster_set": r.cluster_set,
        "role_reason": r.role_reason, "provenance": r.provenance,
    }


def render(classified) -> str:
    out = {
        "cluster_summary": cluster_summary(classified),
        "findings": [_finding_dict(r) for r in classified if r.status == "classified"],
        "low_confidence": [_finding_dict(r) for r in classified if r.status == "low_confidence"],
        "unmapped": [_finding_dict(r) for r in classified if r.status in ("unmapped", "skipped")],
    }
    return json.dumps(out, indent=2)
```

`integrations/sarif/cli/reporters/markdown_report.py`:
```python
from cli.reporters import cluster_summary


def render(classified) -> str:
    summary = cluster_summary(classified)
    lines = ["## TLCTC cluster exposure (SARIF)", "", "| Cluster | Findings |", "|---|---|"]
    for cluster, n in summary.items():
        lines.append(f"| {cluster} | {n} |")
    lines.append("")
    for r in classified:
        if r.status == "classified":
            lines.append(f"- **{r.primary_cluster}** `{r.finding.uri}` — "
                         f"{r.finding.message} ({r.provenance.get('identifier')})")
    low = [r for r in classified if r.status == "low_confidence"]
    if low:
        lines += ["", "### Low-confidence (Discouraged verdict)"]
        for r in low:
            lines.append(f"- {r.primary_cluster} `{r.finding.uri}` — "
                         f"{r.provenance.get('identifier')}")
    return "\n".join(lines) + "\n"
```

`integrations/sarif/cli/reporters/sarif_report.py`:
```python
import json

_CLUSTERS = {
    "#1": "Abuse of Functions", "#2": "Exploiting Server", "#3": "Exploiting Client",
    "#4": "Identity Theft", "#5": "Man in the Middle", "#6": "Flooding Attack",
    "#7": "Malware", "#8": "Physical Attack", "#9": "Social Engineering",
    "#10": "Supply Chain Attack",
}


def _taxonomy():
    return {
        "name": "TLCTC", "version": "2.1",
        "informationUri": "https://www.tlctc.net/",
        "taxa": [{"id": cid, "name": name} for cid, name in _CLUSTERS.items()],
    }


def render(classified) -> str:
    results = []
    for r in classified:
        if r.status not in ("classified", "low_confidence"):
            continue
        f = r.finding
        results.append({
            "ruleId": f.rule_id,
            "message": {"text": f.message},
            "locations": [{"physicalLocation": {"artifactLocation": {"uri": f.uri}}}],
            "properties": {"tlctc": {
                "cluster": r.primary_cluster, "cluster_set": r.cluster_set,
                "status": r.status, "role_resolution": {"reason": r.role_reason},
                "source": r.provenance,
            }},
        })
    doc = {"version": "2.1.0",
           "$schema": "https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-schema-2.1.0.json",
           "runs": [{"tool": {"driver": {"name": "tlctc-sarif", "version": "1.0.0"}},
                     "taxonomies": [_taxonomy()], "results": results}]}
    return json.dumps(doc, indent=2)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd integrations/sarif && python -m unittest tests.test_reporters -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add integrations/sarif/cli/reporters integrations/sarif/tests/test_reporters.py
git commit -m "feat(sarif): add JSON, Markdown, and enriched-SARIF reporters"
```

---

### Task 7: CLI dispatch + `--fail-on-cluster` + golden end-to-end

**Files:**
- Create: `integrations/sarif/cli/tlctc_sarif.py`
- Create: `integrations/sarif/examples/tlctc-sarif.json`
- Create: `integrations/sarif/examples/semgrep-input.sarif` (copy of the test fixture)
- Create: `integrations/sarif/examples/sample-json-report.json` (generated, committed)
- Test: `integrations/sarif/tests/test_cli.py`

- [ ] **Step 1: Write the failing test**

`integrations/sarif/tests/test_cli.py`:
```python
import json
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from cli.tlctc_sarif import main

FIX = Path(__file__).resolve().parent / "fixtures"
CFG = json.dumps({
    "cwe_mapping_path": str(FIX / "tiny-cwe.json"),
    "kev_mapping_path": str(FIX / "tiny-kev.json"),
    "formats": ["json"],
    "source_globs": {"server": ["**/api/**"], "client": ["**/ui/**"]},
})


class TestCli(unittest.TestCase):
    def _run(self, args):
        with patch("sys.stdout", new=StringIO()) as out:
            code = main(args)
        return code, out.getvalue()

    def setUp(self):
        self.cfgfile = FIX / "_cli-cfg.json"
        self.cfgfile.write_text(CFG, encoding="utf-8")

    def tearDown(self):
        self.cfgfile.unlink(missing_ok=True)

    def test_classify_emits_json_and_exit_zero(self):
        code, out = self._run(["classify", str(FIX / "semgrep-min.sarif"),
                               "--config", str(self.cfgfile)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["cluster_summary"]["#2"], 1)

    def test_fail_on_cluster_exits_nonzero(self):
        code, _ = self._run(["classify", str(FIX / "semgrep-min.sarif"),
                             "--config", str(self.cfgfile), "--fail-on-cluster", "#2"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd integrations/sarif && python -m unittest tests.test_cli -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'cli.tlctc_sarif'`

- [ ] **Step 3: Write minimal implementation**

`integrations/sarif/cli/tlctc_sarif.py`:
```python
"""argparse entrypoint for the TLCTC SARIF classifier."""
import argparse
import sys

from cli import __version__
from cli.config import load_config
from cli.mapping_loader import MappingLoader
from cli.sarif_loader import load_findings
from cli.classifier import classify
from cli.reporters import json_report, markdown_report, sarif_report

_REPORTERS = {"json": json_report, "markdown": markdown_report, "sarif": sarif_report}


def _cmd_classify(args):
    cfg = load_config(args.config)
    if args.fail_on_cluster:
        cfg.fail_on_cluster = [c.strip() for c in args.fail_on_cluster.split(",")]
    if args.format:
        cfg.formats = [f.strip() for f in args.format.split(",")]
    ml = MappingLoader(cfg.cwe_mapping_path, cfg.kev_mapping_path)
    findings = load_findings(args.sarif_file)
    classified = [classify(f, ml, cfg.source_globs) for f in findings]
    for fmt in cfg.formats:
        print(_REPORTERS[fmt].render(classified))
    hit = {r.primary_cluster for r in classified
           if r.status == "classified"} & set(cfg.fail_on_cluster)
    return 2 if hit else 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="tlctc-sarif")
    p.add_argument("--version", action="version", version=f"tlctc-sarif {__version__}")
    sub = p.add_subparsers(dest="command", required=True)
    c = sub.add_parser("classify", help="classify a SARIF file")
    c.add_argument("sarif_file")
    c.add_argument("--config")
    c.add_argument("--format")
    c.add_argument("--fail-on-cluster")
    c.set_defaults(func=_cmd_classify)
    args = p.parse_args(argv)
    return args.func(args)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd integrations/sarif && python -m unittest tests.test_cli -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Generate and commit golden example outputs**

```bash
cd integrations/sarif
cp tests/fixtures/semgrep-min.sarif examples/semgrep-input.sarif
# Write examples/tlctc-sarif.json pointing at the repo canonical mappings:
python - <<'PY'
import json, pathlib
pathlib.Path("examples/tlctc-sarif.json").write_text(json.dumps({
    "formats": ["json", "markdown", "sarif"],
    "source_globs": {"server": ["**/api/**", "**/server/**"],
                     "client": ["**/ui/**", "**/*.html", "**/*.js"]}
}, indent=2))
PY
# Generate the committed golden JSON report against the REAL canonical mappings:
python -m cli classify examples/semgrep-input.sarif --format json > examples/sample-json-report.json
cat examples/sample-json-report.json   # sanity check: #2 present
```

- [ ] **Step 6: Commit**

```bash
git add integrations/sarif/cli/tlctc_sarif.py integrations/sarif/examples integrations/sarif/tests/test_cli.py
git commit -m "feat(sarif): add CLI dispatch, fail-on-cluster gate, golden examples"
```

---

### Task 8: Phase 1 docs, metadata, and index wiring

**Files:**
- Create: `integrations/sarif/README.md`
- Create: `integrations/sarif/deploy.md`
- Create: `integrations/sarif/test-cases.md`
- Create: `integrations/sarif/pack_metadata.json`
- Create: `integrations/sarif/ReleaseNotes/1_0_0.md`
- Modify: `integrations/README.md` (add the `sarif/` row + description block)
- Modify: `README.md` (root — add SARIF entry alongside SonarQube)

- [ ] **Step 1: Write `pack_metadata.json`**

`integrations/sarif/pack_metadata.json`:
```json
{
  "name": "TLCTC SARIF Classifier",
  "version": "1.0.0",
  "description": "Generic SARIF 2.1.0 -> TLCTC cluster classifier. CWE-first via tlctc-cwe.json with a CVE->KEV fallback. Standalone, stdlib-only.",
  "tlctc_version": "2.1",
  "license": "CC-BY-4.0",
  "publisher": "TLCTC Project",
  "supported_producers": ["Semgrep", "CodeQL", "Trivy", "Grype", "Bandit", "gosec", "OWASP Dependency-Check"],
  "canonical_inputs": ["mappings/mitre-cwe/tlctc-cwe.json", "mappings/cisa-kev/tlctc-kev.json"],
  "python_requires": ">=3.10"
}
```

- [ ] **Step 2: Write `README.md`**

Write `integrations/sarif/README.md` mirroring `integrations/sonarqube/README.md` structure: a "What this pack does" section (parse any SARIF, extract CWE/CVE, resolution ladder, R-ROLE, three reporters, `--fail-on-cluster`), a "How TLCTC concepts map to SARIF objects" table, a "Notation convention" note (canonical `#N`, no tag normalization needed), Requirements (Python 3.10+/3.11+, no third-party deps), and an "Out of scope for v1" section (no live tool invocation, no GitHub Action, no NVD CVE→CWE enrichment, no Layer 3). Reference the canonical mappings as the single source of truth.

- [ ] **Step 3: Write `deploy.md`**

Write `integrations/sarif/deploy.md` with: prerequisites (Python, a produced `.sarif`), install (`git clone`, no deps), generate a SARIF from a scanner (one Semgrep + one Trivy example command), run `python -m cli classify scan.sarif --config examples/tlctc-sarif.json`, the CI gate pattern (`--fail-on-cluster`), and a rollback note (read-only tool; nothing to undo — delete reports).

- [ ] **Step 4: Write `test-cases.md`**

Write `integrations/sarif/test-cases.md` enumerating TC-1..TC-7 with acceptance criteria, each mapping to a test in `tests/`: TC-1 CWE→cluster (test_classifier), TC-2 `#2|#3` R-ROLE resolution, TC-3 Discouraged→low-confidence, TC-4 Prohibited→skipped, TC-5 CVE→KEV fallback, TC-6 unmapped bucket, TC-7 `--fail-on-cluster` non-zero exit (test_cli).

- [ ] **Step 5: Write `ReleaseNotes/1_0_0.md`**

`integrations/sarif/ReleaseNotes/1_0_0.md`:
```markdown
# 1.0.0

Initial release. Generic SARIF 2.1.0 -> TLCTC classifier.

- Multi-producer identifier extraction (Semgrep, CodeQL, Trivy, Grype, Bandit, gosec).
- CWE-first classification against tlctc-cwe.json; CVE->KEV fallback against tlctc-kev.json.
- R-ROLE resolution for #2|#3 via file-path globs.
- JSON / Markdown / enriched-SARIF reporters; --fail-on-cluster CI gate.
- Standalone, stdlib-only (no third-party deps).
```

- [ ] **Step 6: Wire the indexes**

In `integrations/README.md`, add a table row:
```markdown
| [`sarif/`](sarif/) | Any **SARIF 2.1.0** producer (Semgrep, CodeQL, Trivy, Grype, Bandit, gosec) | Python 3.10+ CLI (stdlib only) | `git clone` then `python -m cli classify scan.sarif` |
```
And a description block after the SonarQube one:
```markdown
The SARIF build:

- Classifies findings from any SARIF 2.1.0 producer to TLCTC clusters.
- CWE-first via the canonical 987-entry CWE→TLCTC mapping; CVE-only findings fall back to the offline KEV→TLCTC table (`mappings/cisa-kev/tlctc-kev.json`).
- Applies R-ROLE (file-path globs) for ambiguous `#2 | #3` mappings.
- Emits JSON / Markdown / TLCTC-enriched SARIF; `--fail-on-cluster` gates CI.
- Does NOT emit Layer 3 — SARIF findings are weaknesses, not realised attack paths.
```
In the root `README.md`, add a one-line SARIF entry next to the SonarQube integration line (match the existing format).

- [ ] **Step 7: Run the full Phase 1 suite**

Run: `cd integrations/sarif && python -m unittest discover tests -v`
Expected: PASS (all tests across config, mapping_loader, sarif_loader, context_resolver, classifier, reporters, cli)

- [ ] **Step 8: Commit**

```bash
git add integrations/sarif/README.md integrations/sarif/deploy.md integrations/sarif/test-cases.md integrations/sarif/pack_metadata.json integrations/sarif/ReleaseNotes integrations/README.md README.md
git commit -m "docs(sarif): add README, deploy, test-cases, metadata, index wiring"
```

---

## Phase 2 — `mappings/sigma/` (Sigma rules → TLCTC)

### File structure (Phase 2)

| File | Responsibility |
|---|---|
| `mappings/sigma/generate-sigma-mapping.py` | ETL: walk SigmaHQ rules → ATT&CK tags → join ATT&CK→TLCTC → records + stats |
| `mappings/sigma/tlctc-sigma.json` | Committed snapshot of per-rule records |
| `mappings/sigma/tlctc-sigma-stats.json` | Aggregate statistics |
| `mappings/sigma/README.md` | What/why/how-to-regenerate, caveats |
| `mappings/sigma/decision-tree.md` | Sigma → ATT&CK → TLCTC resolution logic |
| `mappings/sigma/tests/*` | generator unit tests against a tiny fixture rules dir |

> **Build dependency:** `generate-sigma-mapping.py` imports PyYAML. Install once
> for the maintainer build: `pip install pyyaml`. Consumers of `tlctc-sigma.json`
> need nothing — the output is plain JSON.

---

### Task 9: Generator core — rule walking + tag extraction

**Files:**
- Create: `mappings/sigma/generate-sigma-mapping.py`
- Create: `mappings/sigma/tests/__init__.py`
- Create: `mappings/sigma/tests/fixtures/rules/clean.yml`
- Create: `mappings/sigma/tests/fixtures/rules/subtech.yml`
- Create: `mappings/sigma/tests/fixtures/rules/untagged.yml`
- Create: `mappings/sigma/tests/fixtures/tiny-attack.json`
- Test: `mappings/sigma/tests/test_extract.py`

- [ ] **Step 1: Create fixture Sigma rules + tiny ATT&CK mapping**

`mappings/sigma/tests/fixtures/rules/clean.yml`:
```yaml
title: Suspicious PowerShell Download
id: 11111111-1111-1111-1111-111111111111
logsource:
  product: windows
  category: process_creation
tags:
  - attack.execution
  - attack.t1059
```

`mappings/sigma/tests/fixtures/rules/subtech.yml`:
```yaml
title: PowerShell Encoded Command
id: 22222222-2222-2222-2222-222222222222
logsource:
  product: windows
  category: process_creation
tags:
  - attack.t1059.001
```

`mappings/sigma/tests/fixtures/rules/untagged.yml`:
```yaml
title: Generic Anomaly
id: 33333333-3333-3333-3333-333333333333
logsource:
  product: windows
tags:
  - attack.defense_evasion
```

`mappings/sigma/tests/fixtures/tiny-attack.json`:
```json
{
  "metadata": {"title": "tiny attack"},
  "mappings": [
    {"techniqueId": "T1059", "tlctcMapping": "#1", "tlctcMappingName": "Abuse of Functions"}
  ]
}
```

- [ ] **Step 2: Write the failing test**

`mappings/sigma/tests/test_extract.py`:
```python
import unittest
from pathlib import Path

import importlib.util

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "gen", HERE.parent / "generate-sigma-mapping.py")
gen = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gen)

RULES = HERE / "fixtures" / "rules"


class TestExtract(unittest.TestCase):
    def test_parse_rule_returns_id_title_logsource_techniques(self):
        rule = gen.parse_rule(RULES / "clean.yml")
        self.assertEqual(rule["ruleTitle"], "Suspicious PowerShell Download")
        self.assertEqual(rule["techniques"], ["T1059"])
        self.assertEqual(rule["logsource"]["category"], "process_creation")

    def test_subtechnique_folds_to_parent(self):
        rule = gen.parse_rule(RULES / "subtech.yml")
        self.assertEqual(rule["techniques"], ["T1059"])

    def test_untagged_has_no_techniques(self):
        rule = gen.parse_rule(RULES / "untagged.yml")
        self.assertEqual(rule["techniques"], [])

    def test_walk_finds_all_three(self):
        rules = list(gen.walk_rules(RULES))
        self.assertEqual(len(rules), 3)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd mappings/sigma && python -m unittest tests.test_extract -v`
Expected: FAIL with `AttributeError: module 'gen' has no attribute 'parse_rule'`

- [ ] **Step 4: Write the generator core**

Create `mappings/sigma/generate-sigma-mapping.py` with this top portion (more is added in Tasks 10-11):
```python
#!/usr/bin/env python3
"""Generate the TLCTC Sigma mapping from SigmaHQ rules.

Deterministic ETL:
  Sigma rule  ->  attack.tXXXX tags  ->  parent technique IDs
  technique   ->  TLCTC cluster (via tlctc-enterprise-attack.json)

Inputs:
  --rules-dir   local clone of SigmaHQ rules (path; commit SHA recorded)
  tlctc-enterprise-attack.json (pinned, in-tree)

Outputs:
  mappings/sigma/tlctc-sigma.json        per-rule records
  mappings/sigma/tlctc-sigma-stats.json  aggregate statistics

No rule detection bodies are copied — only id, title, logsource, techniques,
and our derived clusters (license-safe).
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml  # PyYAML — build-time dependency only

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ATTACK_MAPPING = ROOT / "mappings" / "mitre-attack-enterprise" / "tlctc-enterprise-attack.json"
OUTPUT_MAP = HERE / "tlctc-sigma.json"
OUTPUT_STATS = HERE / "tlctc-sigma-stats.json"

_TECH_RE = re.compile(r"attack\.t(\d+)(?:\.\d+)?$", re.IGNORECASE)


def _techniques_from_tags(tags):
    """Extract parent technique IDs from attack.tXXXX[.YYY] tags, deduped+sorted."""
    out = set()
    for tag in tags or []:
        m = _TECH_RE.match(str(tag).strip())
        if m:
            out.add(f"T{m.group(1)}")
    return sorted(out)


def parse_rule(path: Path):
    doc = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return {
        "ruleId": doc.get("id", ""),
        "ruleTitle": doc.get("title", ""),
        "logsource": doc.get("logsource", {}),
        "techniques": _techniques_from_tags(doc.get("tags", [])),
    }


def walk_rules(rules_dir: Path):
    for path in sorted(Path(rules_dir).rglob("*.yml")):
        try:
            yield parse_rule(path)
        except yaml.YAMLError:
            continue  # skip non-rule YAML (e.g. config) silently
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd mappings/sigma && python -m unittest tests.test_extract -v`
Expected: PASS (4 tests)

- [ ] **Step 6: Commit**

```bash
git add mappings/sigma/generate-sigma-mapping.py mappings/sigma/tests
git commit -m "feat(sigma): generator core — rule walking and ATT&CK tag extraction"
```

---

### Task 10: ATT&CK join + cluster-set derivation

**Files:**
- Modify: `mappings/sigma/generate-sigma-mapping.py` (add join + derivation)
- Test: `mappings/sigma/tests/test_derive.py`

- [ ] **Step 1: Write the failing test**

`mappings/sigma/tests/test_derive.py`:
```python
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("gen", HERE.parent / "generate-sigma-mapping.py")
gen = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gen)

ATTACK = HERE / "fixtures" / "tiny-attack.json"


class TestDerive(unittest.TestCase):
    def setUp(self):
        self.idx = gen.load_attack_index(ATTACK)

    def test_single_technique_ok(self):
        rec = gen.derive_record(
            {"ruleId": "x", "ruleTitle": "t", "logsource": {}, "techniques": ["T1059"]}, self.idx)
        self.assertEqual(rec["primaryCluster"], "#1")
        self.assertEqual(rec["clusterSet"], ["#1"])
        self.assertEqual(rec["derivationStatus"], "ok")

    def test_untagged_is_unmapped(self):
        rec = gen.derive_record(
            {"ruleId": "x", "ruleTitle": "t", "logsource": {}, "techniques": []}, self.idx)
        self.assertEqual(rec["derivationStatus"], "unmapped")
        self.assertIsNone(rec["primaryCluster"])

    def test_unknown_technique_is_unmapped(self):
        rec = gen.derive_record(
            {"ruleId": "x", "ruleTitle": "t", "logsource": {}, "techniques": ["T9999"]}, self.idx)
        self.assertEqual(rec["derivationStatus"], "unmapped")

    def test_alternation_mapping_is_ambiguous(self):
        idx = {"T1001": "#1 | #7"}
        rec = gen.derive_record(
            {"ruleId": "x", "ruleTitle": "t", "logsource": {}, "techniques": ["T1001"]}, idx)
        self.assertEqual(rec["derivationStatus"], "ambiguous")
        self.assertEqual(rec["primaryCluster"], "#1")  # lowest-numbered
        self.assertEqual(rec["clusterSet"], ["#1", "#7"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd mappings/sigma && python -m unittest tests.test_derive -v`
Expected: FAIL with `AttributeError: module 'gen' has no attribute 'load_attack_index'`

- [ ] **Step 3: Append the join + derivation to the generator**

Append to `mappings/sigma/generate-sigma-mapping.py`:
```python
_CLUSTER_RE = re.compile(r"#(\d+)")


def load_attack_index(attack_path=ATTACK_MAPPING):
    """techniqueId -> tlctcMapping expression (e.g. 'T1059' -> '#1')."""
    doc = json.loads(Path(attack_path).read_text(encoding="utf-8"))
    return {e["techniqueId"]: e.get("tlctcMapping", "") for e in doc["mappings"]}


def _clusters(expr):
    """'#1 | #7' -> ['#1','#7'] (lowest-numbered first); 'N/A' -> []."""
    nums = sorted(int(n) for n in _CLUSTER_RE.findall(expr or ""))
    return [f"#{n}" for n in nums]


def derive_record(rule, attack_index):
    cluster_set, any_alt, any_unmapped = [], False, False
    for tech in rule["techniques"]:
        expr = attack_index.get(tech)
        clusters = _clusters(expr) if expr is not None else []
        if not clusters:
            any_unmapped = True
            continue
        if len(clusters) > 1:
            any_alt = True
        for c in clusters:
            if c not in cluster_set:
                cluster_set.append(c)
    cluster_set = [f"#{n}" for n in sorted(int(c[1:]) for c in cluster_set)]
    if not cluster_set:
        status, primary = "unmapped", None
    elif any_alt or len(cluster_set) > 1:
        status, primary = "ambiguous", cluster_set[0]
    else:
        status, primary = "ok", cluster_set[0]
    if any_unmapped and cluster_set:
        status = "ambiguous"  # partial resolution
    return {
        "ruleId": rule["ruleId"],
        "ruleTitle": rule["ruleTitle"],
        "logsource": rule["logsource"],
        "techniques": rule["techniques"],
        "clusterSet": cluster_set,
        "primaryCluster": primary,
        "derivationStatus": status,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd mappings/sigma && python -m unittest tests.test_derive -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add mappings/sigma/generate-sigma-mapping.py mappings/sigma/tests/test_derive.py
git commit -m "feat(sigma): add ATT&CK join and cluster-set derivation"
```

---

### Task 11: Output writers + `main()` + stats

**Files:**
- Modify: `mappings/sigma/generate-sigma-mapping.py` (add `build`, `write_outputs`, `main`)
- Test: `mappings/sigma/tests/test_build.py`

- [ ] **Step 1: Write the failing test**

`mappings/sigma/tests/test_build.py`:
```python
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("gen", HERE.parent / "generate-sigma-mapping.py")
gen = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gen)

RULES = HERE / "fixtures" / "rules"
ATTACK = HERE / "fixtures" / "tiny-attack.json"


class TestBuild(unittest.TestCase):
    def test_build_produces_records_and_stats(self):
        mapping, stats = gen.build(RULES, ATTACK, sigma_commit="abc123")
        self.assertEqual(mapping["metadata"]["sigma_commit"], "abc123")
        self.assertEqual(len(mapping["mappings"]), 3)
        # clean.yml -> #1 ok; subtech.yml -> #1 ok; untagged.yml -> unmapped
        statuses = sorted(r["derivationStatus"] for r in mapping["mappings"])
        self.assertEqual(statuses, ["ok", "ok", "unmapped"])
        self.assertEqual(stats["cluster_distribution"].get("#1"), 2)
        self.assertEqual(stats["status_counts"]["unmapped"], 1)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd mappings/sigma && python -m unittest tests.test_build -v`
Expected: FAIL with `AttributeError: module 'gen' has no attribute 'build'`

- [ ] **Step 3: Append build/stats/main to the generator**

Append to `mappings/sigma/generate-sigma-mapping.py`:
```python
def build(rules_dir, attack_path, sigma_commit="unknown"):
    idx = load_attack_index(attack_path)
    records = [derive_record(r, idx) for r in walk_rules(rules_dir)]
    mapping = {
        "metadata": {
            "title": "TLCTC Sigma Mapping (SigmaHQ rules -> TLCTC)",
            "description": "Per-rule TLCTC cluster derivation from Sigma ATT&CK tags via ATT&CK->TLCTC.",
            "tlctc_version": "2.1",
            "sigma_commit": sigma_commit,
            "attack_mapping": str(Path(attack_path).name),
            "total_rules": len(records),
            "license": "CC-BY-4.0",
            "publisher": "TLCTC Project",
            "caveats": [
                "Mapping quality depends on each rule's attack.t* tagging; untagged rules are 'unmapped'.",
                "Derived mechanically from the experimental AI-generated ATT&CK->TLCTC mapping.",
                "Sub-techniques are folded to their parent technique.",
                "No Sigma rule detection bodies are reproduced — titles + GUIDs + derivation only.",
            ],
        },
        "mappings": records,
    }
    dist = Counter(r["primaryCluster"] for r in records
                   if r["derivationStatus"] == "ok" and r["primaryCluster"])
    stats = {
        "total_rules": len(records),
        "cluster_distribution": dict(sorted(dist.items(), key=lambda kv: int(kv[0][1:]))),
        "status_counts": dict(Counter(r["derivationStatus"] for r in records)),
        "logsource_breakdown": dict(Counter(
            (r["logsource"] or {}).get("category", "(none)") for r in records)),
    }
    return mapping, stats


def write_outputs(mapping, stats):
    OUTPUT_MAP.write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
    OUTPUT_STATS.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")


def main(argv=None):
    p = argparse.ArgumentParser(description="Generate the TLCTC Sigma mapping.")
    p.add_argument("--rules-dir", required=True, help="path to a SigmaHQ rules clone")
    p.add_argument("--sigma-commit", default="unknown", help="commit SHA of the rules clone")
    args = p.parse_args(argv)
    mapping, stats = build(args.rules_dir, ATTACK_MAPPING, args.sigma_commit)
    write_outputs(mapping, stats)
    print(f"Wrote {len(mapping['mappings'])} rule records to {OUTPUT_MAP.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd mappings/sigma && python -m unittest tests.test_build -v`
Expected: PASS (1 test)

- [ ] **Step 5: Run the full Phase 2 suite**

Run: `cd mappings/sigma && python -m unittest discover tests -v`
Expected: PASS (test_extract, test_derive, test_build)

- [ ] **Step 6: Commit**

```bash
git add mappings/sigma/generate-sigma-mapping.py mappings/sigma/tests/test_build.py
git commit -m "feat(sigma): add build, stats, and CLI main"
```

---

### Task 12: Generate the committed snapshot + docs

**Files:**
- Create: `mappings/sigma/tlctc-sigma.json` (generated)
- Create: `mappings/sigma/tlctc-sigma-stats.json` (generated)
- Create: `mappings/sigma/README.md`
- Create: `mappings/sigma/decision-tree.md`

- [ ] **Step 1: Clone SigmaHQ and generate the real snapshot**

```bash
pip install pyyaml
git clone --depth 1 https://github.com/SigmaHQ/sigma /tmp/sigma
SHA=$(git -C /tmp/sigma rev-parse HEAD)
cd mappings/sigma
python generate-sigma-mapping.py --rules-dir /tmp/sigma/rules --sigma-commit "$SHA"
```
Expected: prints `Wrote N rule records to tlctc-sigma.json` (N in the low thousands).

- [ ] **Step 2: Sanity-check the snapshot**

Run:
```bash
python - <<'PY'
import json
d = json.load(open("tlctc-sigma.json", encoding="utf-8"))
s = json.load(open("tlctc-sigma-stats.json", encoding="utf-8"))
assert d["mappings"], "no records"
assert s["status_counts"], "no stats"
print("rules:", d["metadata"]["total_rules"], "| dist:", s["cluster_distribution"])
PY
```
Expected: non-empty distribution across multiple clusters; `ok`/`ambiguous`/`unmapped` all present in `status_counts`.

- [ ] **Step 3: Write `README.md`**

Write `mappings/sigma/README.md` following the `mappings/cisa-kev/README.md` convention: what the mapping is, the derivation chain (Sigma `attack.t*` → parent technique → ATT&CK→TLCTC), how to regenerate (the clone + command from Step 1, noting PyYAML is the only build dependency and the output is consumer-dependency-free), the record schema (the fields from `derive_record`), the `derivationStatus` semantics (`ok`/`ambiguous`/`unmapped`), and the caveats block. State explicitly that no rule detection logic is vendored.

- [ ] **Step 4: Write `decision-tree.md`**

Write `mappings/sigma/decision-tree.md` showing the resolution flow: rule has `attack.t*` tag? → fold sub-technique to parent → look up ATT&CK→TLCTC → single concrete cluster (`ok`) / alternation or multi-cluster (`ambiguous`) / `N/A` or untagged (`unmapped`) → `primaryCluster` = lowest-numbered. Include a worked example for each status using the fixture rules.

- [ ] **Step 5: Add the mappings index entry**

If `mappings/` has an index in the root `README.md`, add a `sigma/` line next to the other mappings (CWE, KEV, npm) in the established format.

- [ ] **Step 6: Commit**

```bash
git add mappings/sigma/tlctc-sigma.json mappings/sigma/tlctc-sigma-stats.json mappings/sigma/README.md mappings/sigma/decision-tree.md README.md
git commit -m "feat(sigma): generate committed snapshot and add README + decision-tree"
```

---

## Final verification

- [ ] Phase 1 full suite: `cd integrations/sarif && python -m unittest discover tests -v` → all pass.
- [ ] Phase 2 full suite: `cd mappings/sigma && python -m unittest discover tests -v` → all pass.
- [ ] `integrations/README.md` and root `README.md` list the SARIF pack.
- [ ] `mappings/sigma/tlctc-sigma.json` + stats are committed and non-empty.
- [ ] No third-party imports in `integrations/sarif/cli/**` (stdlib only); PyYAML used only in `mappings/sigma/generate-sigma-mapping.py`.

