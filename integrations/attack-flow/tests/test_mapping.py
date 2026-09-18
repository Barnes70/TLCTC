import unittest

from cli.mapping import ParseError, load_attack_mapping, parse_mapping


class ParseTests(unittest.TestCase):
    def test_forms(self):
        self.assertEqual(parse_mapping("#7"), [["#7"]])
        self.assertEqual(parse_mapping("#10 → #7"), [["#10", "#7"]])
        self.assertEqual(parse_mapping("#2 | #3"), [["#2"], ["#3"]])
        self.assertEqual(parse_mapping("#1 | (#1 → #7) | #4"), [["#1"], ["#1", "#7"], ["#4"]])
        self.assertEqual(parse_mapping("(#2 → #7) | (#3 → #7)"), [["#2", "#7"], ["#3", "#7"]])
        self.assertEqual(parse_mapping("(#2 | #3) → #7"), [["#2", "#7"], ["#3", "#7"]])
        self.assertEqual(parse_mapping("#8.2 → #7"), [["#8", "#7"]])
        self.assertEqual(parse_mapping("#1 -> #7"), [["#1", "#7"]])
        self.assertEqual(parse_mapping("N/A"), [])
        self.assertEqual(parse_mapping(""), [])

    def test_errors(self):
        with self.assertRaises(ParseError):
            parse_mapping("#11")
        with self.assertRaises(ParseError):
            parse_mapping("(#1 → #7")
        with self.assertRaises(ParseError):
            parse_mapping("#1 #7")

    def test_every_repository_mapping_parses(self):
        m = load_attack_mapping()
        for tid, e in m.by_id.items():
            parse_mapping(e["tlctcMapping"])  # raises on failure
        self.assertGreater(len(m.by_id), 600)


class LookupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_attack_mapping()

    def test_statuses(self):
        self.assertEqual(self.m.lookup("T1195.002")["status"], "resolved")
        self.assertEqual(self.m.lookup("T1195.002")["alternatives"], [["#10", "#7"]])
        self.assertEqual(self.m.lookup(None)["status"], "no_technique")
        self.assertEqual(self.m.lookup("T9999")["status"], "unmapped")
        prep = self.m.lookup("T1583.002")  # Acquire Infrastructure: Domains
        self.assertEqual(prep["status"], "preparation")

    def test_parent_fallback(self):
        r = self.m.lookup("T1566.999")
        self.assertEqual(r["technique_used"], "T1566")
        self.assertIn(r["status"], ("resolved", "rule_dependent"))

    def test_case_insensitive(self):
        self.assertEqual(self.m.lookup("t1078")["technique_used"], "T1078")

    def test_atlas_routed(self):
        r = self.m.lookup("AML.T0051.001")  # indirect prompt injection
        self.assertEqual(r["framework"], "atlas")
        self.assertEqual(r["status"], "resolved")
        self.assertEqual(r["alternatives"], [["#1"]])
        self.assertEqual(self.m.lookup("AML.T0010.001")["alternatives"], [["#10", "#7"]])
        self.assertEqual(self.m.lookup("AML.T0048")["status"], "preparation")
        self.assertGreaterEqual(sum(1 for k in self.m.by_id if k.startswith("AML.")), 170)


if __name__ == "__main__":
    unittest.main()
