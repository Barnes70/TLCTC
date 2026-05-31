import unittest
from pathlib import Path

import importlib.util

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "gen", HERE.parent / "generate-sigma-mapping.py")
gen = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gen)

RULES = HERE / "fixtures" / "rules"


class TestExtract(unittest.TestCase):
    def test_parse_rule_returns_id_title_logsource_techniques(self):
        rule = gen.parse_rule(RULES / "clean.yml")
        self.assertEqual(rule["ruleTitle"], "Suspicious PowerShell Download")
        self.assertEqual(rule["techniques"], ["T1059"])
        self.assertEqual(rule["logsource"]["category"], "process_creation")

    def test_subtechnique_folds_to_parent(self):
        rule = gen.parse_rule(RULES / "subtech.yml")
        self.assertEqual(rule["techniques"], ["T1059"])

    def test_untagged_has_no_techniques(self):
        rule = gen.parse_rule(RULES / "untagged.yml")
        self.assertEqual(rule["techniques"], [])

    def test_walk_finds_all_three(self):
        rules = list(gen.walk_rules(RULES))
        self.assertEqual(len(rules), 3)


if __name__ == "__main__":
    unittest.main()
