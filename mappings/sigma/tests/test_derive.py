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

    def test_partial_resolution_is_ambiguous(self):
        # One known technique (#1) + one unknown → status upgraded to ambiguous,
        # but primaryCluster is preserved.
        rec = gen.derive_record(
            {"ruleId": "x", "ruleTitle": "t", "logsource": {},
             "techniques": ["T1059", "T9999"]}, self.idx)
        self.assertEqual(rec["derivationStatus"], "ambiguous")
        self.assertEqual(rec["primaryCluster"], "#1")
        self.assertEqual(rec["clusterSet"], ["#1"])


if __name__ == "__main__":
    unittest.main()
