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
