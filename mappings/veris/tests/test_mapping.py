import json
import unittest
from pathlib import Path

from cli.mapping import load_mapping

ROOT = Path(__file__).resolve().parents[1]
PINNED = ROOT / "pinned"

COVERED_ACTION = {
    "hacking": ("variety", "vector", "result"), "malware": ("variety", "vector", "result"),
    "social": ("variety", "vector", "result"), "misuse": ("variety", "vector", "result"),
    "physical": ("variety", "vector", "result"), "error": ("variety", "vector"),
    "environmental": ("variety",), "unknown": ("result",),
}
COVERED_ATTRIBUTE = {"confidentiality": ("data_disclosure",), "integrity": ("variety",), "availability": ("variety",)}
FIELDS_BY_TYPE = {
    "direct": {"targets"}, "conditional": {"targets"}, "chain": {"targets", "companion"},
    "context": {"context"}, "no-cluster": {"partition_row", "basis", "out_of_scope"},
    "outcome": {"dre", "certainty"}, "unresolved": set(),
}
BASE = {"veris_id", "veris_description", "mapping_type", "rationale"}


class MappingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_mapping()
        with open(PINNED / "verisc-enum.json", encoding="utf-8") as fh:
            cls.enum = json.load(fh)

    def expected_ids(self):
        ids = {"action.unknown"}
        for cat, fields in COVERED_ACTION.items():
            for f in fields:
                ids.update(f"action.{cat}.{f}.{v}" for v in self.enum["action"][cat][f])
        for cat, fields in COVERED_ATTRIBUTE.items():
            for f in fields:
                ids.update(f"attribute.{cat}.{f}.{v}" for v in self.enum["attribute"][cat][f])
        return ids

    def test_total_coverage_of_pinned_enum(self):
        have = {e["veris_id"] for e in self.m.entries}
        self.assertEqual(self.expected_ids() - have, set(), "enum values without an entry")
        self.assertEqual(have - self.expected_ids(), set(), "entries that are not enum values")

    def test_no_duplicate_ids(self):
        ids = [e["veris_id"] for e in self.m.entries]
        self.assertEqual(len(ids), len(set(ids)))

    def test_field_pairing(self):
        for e in self.m.entries:
            allowed = BASE | FIELDS_BY_TYPE[e["mapping_type"]]
            self.assertEqual(set(e) - allowed, set(), e["veris_id"])
            if e["mapping_type"] in ("direct", "chain"):
                self.assertEqual(len(e["targets"]), 1, e["veris_id"])
            if e["mapping_type"] == "conditional":
                self.assertGreaterEqual(len(e["targets"]), 2, e["veris_id"])
                for t in e["targets"]:
                    self.assertIn("condition", t, e["veris_id"])
            if e["mapping_type"] == "chain":
                self.assertTrue(e["companion"].get("before") or e["companion"].get("after"), e["veris_id"])
            if e["mapping_type"] == "no-cluster" and e["partition_row"] == "attack":
                self.assertIn("out_of_scope", e, e["veris_id"])

    def test_known_rows(self):
        self.assertEqual(self.m.get("action.hacking.variety.SQLi")["targets"][0]["tlctc"], "#2")
        self.assertEqual(self.m.get("action.hacking.variety.Use of stolen creds")["mapping_type"], "chain")
        self.assertEqual(self.m.get("action.hacking.variety.Use of stolen creds")["targets"][0]["rule"], "R-CRED")
        self.assertEqual(self.m.get("action.malware.variety.Ransomware")["targets"][0]["tlctc"], "#7")
        self.assertEqual(self.m.get("attribute.availability.variety.Obscuration")["dre"], "Ac")
        self.assertEqual(self.m.get("attribute.availability.variety.Loss")["dre"], "Av")
        self.assertEqual(self.m.get("action.error.variety.Misdelivery")["partition_row"], "error_in_use")
        self.assertEqual(self.m.get("action.misuse.variety.Unapproved software")["partition_row"], "abuse_of_rights")
        self.assertEqual(self.m.get("action.misuse.variety.Privilege abuse")["partition_row"], "abuse_of_rights")
        self.assertEqual(self.m.get("action.misuse.variety.Password or Session Sharing")["targets"][0]["tlctc"], "#4")
        self.assertEqual(self.m.get("action.hacking.variety.CSRF")["targets"][0]["tlctc"], "#1")
        self.assertEqual(self.m.get("action.hacking.variety.XSS")["mapping_type"], "conditional")
        self.assertEqual(self.m.get("action.hacking.vector.Partner")["context"]["boundary"], "@Vendor→@Org")
        self.assertEqual(self.m.get("action.unknown")["mapping_type"], "unresolved")

    def test_metadata(self):
        self.assertEqual(self.m.veris_version, "1.4.1")
        self.assertEqual(self.m.tlctc_version, "2.5")
        self.assertEqual(self.m.metadata["entry_count"], len(self.m))


if __name__ == "__main__":
    unittest.main()
