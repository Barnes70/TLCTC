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

    def test_skippable_cwe_then_valid_cwe_classifies(self):
        # First CWE is N/A/Prohibited (CWE-0); a later usable CWE must still win.
        r = self._classify(Finding("multi", "m", "src/api/u.py", "CodeQL",
                                   cwe=["CWE-0", "CWE-89"]))
        self.assertEqual(r.status, "classified")
        self.assertEqual(r.primary_cluster, "#2")
        self.assertEqual(r.provenance["identifier"], "CWE-89")

    def test_prohibited_cwe_then_cve_falls_back(self):
        # A Prohibited/N/A CWE must not block the independent CVE→KEV fallback.
        r = self._classify(Finding("mix", "m", "pom.xml", "Trivy",
                                   cwe=["CWE-0"], cve=["CVE-2021-44228"]))
        self.assertEqual(r.status, "classified")
        self.assertEqual(r.provenance["table"], "tlctc-kev")


if __name__ == "__main__":
    unittest.main()
