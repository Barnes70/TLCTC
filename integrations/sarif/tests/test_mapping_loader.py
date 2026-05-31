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
