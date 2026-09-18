"""The twenty real VCDB records (CC BY-SA 4.0, see fixtures/vcdb/LICENSE.md) classify without
error and match the golden results in fixtures/vcdb/expected.json.

Regenerate the golden file on purpose only:
    python -m cli classify tests/fixtures/vcdb -o tests/fixtures/vcdb/expected.json
"""
import json
import unittest
from pathlib import Path

from cli.classify import classify
from cli.mapping import load_mapping

FIX = Path(__file__).resolve().parent / "fixtures" / "vcdb"


class VcdbFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_mapping()
        with open(FIX / "expected.json", encoding="utf-8") as fh:
            cls.expected = {r["incident_id"]: r for r in json.load(fh)}
        cls.records = {}
        for p in sorted(FIX.glob("*.json")):
            if p.name == "expected.json":
                continue
            with open(p, encoding="utf-8") as fh:
                rec = json.load(fh)
            cls.records[rec["incident_id"]] = rec

    def test_twenty_records(self):
        self.assertEqual(len(self.records), 20)
        self.assertEqual(set(self.records), set(self.expected))

    def test_golden(self):
        for iid, rec in self.records.items():
            with self.subTest(incident_id=iid):
                self.assertEqual(classify(rec, self.m), self.expected[iid])

    def test_no_unmapped_on_current_schema(self):
        for iid, rec in self.records.items():
            if str(rec.get("schema_version", "")).startswith("1.4"):
                with self.subTest(incident_id=iid):
                    self.assertEqual(classify(rec, self.m)["unmapped"], [])

    def test_licence_files_present(self):
        self.assertTrue((FIX / "LICENSE.md").exists())
        self.assertTrue((FIX / "SELECTION.md").exists())
        text = (FIX / "LICENSE.md").read_text(encoding="utf-8")
        for iid in self.records:
            self.assertIn(iid, text)


if __name__ == "__main__":
    unittest.main()
