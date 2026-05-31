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
