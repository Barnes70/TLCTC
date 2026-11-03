"""Tests for mappings/rsit/upstream/machinetag2tlctc.py. Run from mappings/rsit: python -m unittest discover tests"""
import importlib.util
import json
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
UPSTREAM = HERE.parent / "upstream"
spec = importlib.util.spec_from_file_location("machinetag2tlctc", UPSTREAM / "machinetag2tlctc.py")
m2t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m2t)


def generated():
    return json.loads((UPSTREAM / "machinetag.json").read_text(encoding="utf-8"))


def rows(md):
    return [line for line in md.splitlines() if line.startswith("| ") and not line.startswith("| Classification")]


class RenderTests(unittest.TestCase):
    def test_row_count(self):
        self.assertEqual(len(rows(m2t.render(generated()))), 39)

    def test_tagged_cell(self):
        row = next(r for r in rows(m2t.render(generated())) if "| Infected System |" in r)
        self.assertIn('tlctc:cluster="07-malware"', row)

    def test_unresolved_head_is_question_mark(self):
        row = next(r for r in rows(m2t.render(generated())) if "| Uncategorised |" in r)
        self.assertIn("| ? (unresolved):", row)

    def test_pipe_escaped(self):
        data = {
            "predicates": [{"value": "p", "expanded": "P"}],
            "values": [{"predicate": "p", "entry": [{"value": "v", "expanded": "V", "description": "d",
                        "tlctc": [{"candidates": ["#2", "#3"], "mapping_type": "conditional",
                                   "note": "server | client", "timestamp": 20261103}]}]}],
        }
        row = rows(m2t.render(data))[0]
        self.assertIn("#2 \\| #3", row)
        self.assertIn("server \\| client", row)
        self.assertEqual(row.count(" | "), 3)  # three unescaped inner separators = four cells


if __name__ == "__main__":
    unittest.main()
