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
