"""Unit tests for reporters."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cli.classifier import classify, summarize
from cli.context_resolver import ROLE_SERVER, RoleConfig
from cli.mapping_loader import VERDICT_ALLOWED, VERDICT_REVIEW, load
from cli.reporters import json_report, markdown_report, sarif_report

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "tiny-cwe-mapping.json"
DEFAULT_VERDICTS = (VERDICT_ALLOWED, VERDICT_REVIEW)


def _issue(key: str, cwe: str, component: str) -> dict:
    return {
        "key": key,
        "rule": "test:rule",
        "severity": "MAJOR",
        "component": component,
        "project": "demo",
        "type": "VULNERABILITY",
        "message": "test",
        "tags": [],
        "securityStandards": [cwe],
    }


class TestReporters(unittest.TestCase):
    def setUp(self) -> None:
        self.index = load(FIXTURE)
        self.role_config = RoleConfig(
            server_globs=("**/src/main/java/**",),
            client_globs=("**/*.tsx",),
            default_role=ROLE_SERVER,
        )
        self.findings = [
            classify(i, self.index, self.role_config, DEFAULT_VERDICTS)
            for i in [
                _issue("I1", "cwe:89", "demo:src/main/java/A.java"),
                _issue("I2", "cwe:79", "demo:src/main/webapp/X.tsx"),
                _issue("I3", "cwe:20", "demo:src/main/java/Y.java"),
            ]
        ]
        self.summary = summarize(self.findings)

    def test_json_report_well_formed(self) -> None:
        body = json_report.render(self.findings, self.summary, "2.1", "demo")
        d = json.loads(body)
        self.assertEqual(d["tlctc_version"], "2.1")
        self.assertIn("#2", d["cluster_summary"])
        self.assertIn("#3", d["cluster_summary"])
        self.assertEqual(d["totals"]["issues_classified"], 2)
        self.assertEqual(d["totals"]["issues_low_confidence"], 1)

    def test_markdown_report_contains_cluster_table(self) -> None:
        body = markdown_report.render(self.findings, self.summary, "2.1", "demo")
        self.assertIn("## TLCTC SAST Report", body)
        self.assertIn("Cluster Exposure", body)
        self.assertIn("| `#2` |", body)
        self.assertIn("| `#3` |", body)
        self.assertIn("Low-confidence", body)

    def test_sarif_report_is_valid_sarif_shape(self) -> None:
        body = sarif_report.render(self.findings, self.summary, "2.1", "demo")
        sarif = json.loads(body)
        self.assertEqual(sarif["version"], "2.1.0")
        self.assertEqual(len(sarif["runs"]), 1)
        run = sarif["runs"][0]
        rule_ids = {r["id"] for r in run["tool"]["driver"]["rules"]}
        self.assertIn("tlctc-02", rule_ids)
        self.assertIn("tlctc-03", rule_ids)
        # I1 -> #2; I2 -> #3 (resolved client); I3 Discouraged -> not in results
        self.assertEqual(len(run["results"]), 2)
        primary_ids = {r["ruleId"] for r in run["results"]}
        self.assertEqual(primary_ids, {"tlctc-02", "tlctc-03"})


if __name__ == "__main__":
    unittest.main()
