import json
import tempfile
import unittest
from pathlib import Path

from cli.afb import read_afb
from cli.stixflow import detect_and_read, read_stix

FIX = Path(__file__).resolve().parent / "fixtures"
PINNED = Path(__file__).resolve().parents[1] / "pinned"


class AfbReaderTests(unittest.TestCase):
    def test_solarwinds(self):
        f = read_afb(FIX / "corpus" / "SolarWinds.afb")
        self.assertEqual(f.name, "SolarWinds")
        self.assertEqual(f.scope, "incident")
        self.assertEqual(len(f.actions), 33)
        self.assertEqual(len(f.conditions), 5)
        self.assertEqual(len(f.operators), 6)
        self.assertEqual(len(f.edges), 54)
        labels = [e.label for e in f.edges if e.label]
        self.assertEqual(labels.count("true"), 8)
        self.assertEqual(labels.count("false"), 2)
        self.assertFalse(f.has_cycle())
        techs = {a.technique_id for a in f.actions.values()}
        self.assertIn("T1195.002", techs)
        # attachments never become flow edges
        for e in f.edges:
            self.assertIsNotNone(f.kind(e.src))
            self.assertIsNotNone(f.kind(e.dst))
        self.assertTrue(any("tool" in x or "malware" in x for v in f.attachments.values() for x in v))

    def test_tesla(self):
        f = read_afb(FIX / "corpus" / "Tesla Kubernetes Breach.afb")
        self.assertEqual(len(f.actions), 9)
        self.assertEqual(len(f.conditions), 1)
        self.assertEqual([o.operator for o in f.operators.values()], ["AND"])
        order = f.topological_order()
        self.assertEqual(len(order), len(f.nodes()))
        first = order[0]
        self.assertEqual(f.actions[first].technique_id, "T1583.004")

    def test_rejects_other_schema(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.afb"
            p.write_text(json.dumps({"schema": "attack_flow_v3", "objects": []}), encoding="utf-8")
            with self.assertRaises(ValueError):
                read_afb(p)


class StixReaderTests(unittest.TestCase):
    def test_pinned_example_shape(self):
        # Build a minimal Attack Flow STIX bundle: flow → action A → condition → (true) action B, (false) action C
        objs = [
            {"type": "attack-flow", "spec_version": "2.1", "id": "attack-flow--00000000-0000-4000-8000-000000000001", "name": "t", "scope": "incident", "start_refs": ["attack-action--00000000-0000-4000-8000-00000000000a"]},
            {"type": "attack-action", "spec_version": "2.1", "id": "attack-action--00000000-0000-4000-8000-00000000000a", "name": "A", "technique_id": "T1566", "effect_refs": ["attack-condition--00000000-0000-4000-8000-00000000000c"], "asset_refs": ["attack-asset--00000000-0000-4000-8000-00000000000e"]},
            {"type": "attack-condition", "spec_version": "2.1", "id": "attack-condition--00000000-0000-4000-8000-00000000000c", "description": "opened?", "on_true_refs": ["attack-action--00000000-0000-4000-8000-00000000000b"], "on_false_refs": ["attack-action--00000000-0000-4000-8000-00000000000d"]},
            {"type": "attack-action", "spec_version": "2.1", "id": "attack-action--00000000-0000-4000-8000-00000000000b", "name": "B", "technique_id": "T1204.002"},
            {"type": "attack-action", "spec_version": "2.1", "id": "attack-action--00000000-0000-4000-8000-00000000000d", "name": "C", "technique_id": "T1598"},
            {"type": "attack-asset", "spec_version": "2.1", "id": "attack-asset--00000000-0000-4000-8000-00000000000e", "name": "mailbox"},
        ]
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "b.json"
            p.write_text(json.dumps({"type": "bundle", "id": "bundle--00000000-0000-4000-8000-000000000000", "objects": objs}), encoding="utf-8")
            f = read_stix(p)
            self.assertEqual(len(f.actions), 3)
            self.assertEqual(len(f.conditions), 1)
            self.assertEqual({(e.src[-1], e.dst[-1], e.label) for e in f.edges}, {("a", "c", None), ("c", "b", "true"), ("c", "d", "false")})
            self.assertEqual(f.starts(), ["attack-action--00000000-0000-4000-8000-00000000000a"])
            self.assertEqual(f.attachments["attack-action--00000000-0000-4000-8000-00000000000a"], ["attack-asset: mailbox"])
            g = detect_and_read(p)
            self.assertEqual(len(g.actions), 3)

    def test_detect_afb(self):
        f = detect_and_read(FIX / "corpus" / "Equifax Breach.afb")
        self.assertEqual(len(f.actions), 12)


if __name__ == "__main__":
    unittest.main()
