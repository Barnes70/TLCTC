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
