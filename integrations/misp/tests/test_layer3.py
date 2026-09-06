import json
import unittest
from pathlib import Path

from cli.layer3 import (Layer3Error, check_document, classified_clusters, entry_cluster,
                        flat_steps, item_kind, load_layer3, to_strategic)

ROOT = Path(__file__).resolve().parents[3]
SOLARWINDS = ROOT / "json-schemas" / "layer-3" / "examples" / "solarwinds-2020.json"
AGENT_BTZ = ROOT / "attack-paths" / "agent-btz-usb-2008.json"
UNRESOLVED = ROOT / "json-schemas" / "layer-3" / "examples" / "unresolved-step-example-2026.json"
AD_CASCADE = ROOT / "attack-paths" / "ad-domain-admin-cascade-2025.json"


class TestClusters(unittest.TestCase):
    def test_strategic_passthrough(self):
        self.assertEqual(to_strategic("#7"), "#7")
        self.assertEqual(to_strategic("#10"), "#10")

    def test_operational_collapses(self):
        self.assertEqual(to_strategic("TLCTC-07.02"), "#7")
        self.assertEqual(to_strategic("TLCTC-10.01"), "#10")

    def test_garbage_raises(self):
        for bad in ("#11", "7", "TLCTC-7.1", "", None):
            with self.assertRaises(Layer3Error):
                to_strategic(bad)


class TestItemKind(unittest.TestCase):
    def test_kinds(self):
        self.assertEqual(item_kind({"step_id": "s1", "cluster": "#7"}), "step")
        self.assertEqual(item_kind({"mode": "parallel", "steps": []}), "group")
        self.assertEqual(item_kind({"step_id": "s1", "status": "unresolved", "unresolved_type": "single", "notes": "x"}), "unresolved")

    def test_unknown_shape_raises(self):
        with self.assertRaises(Layer3Error):
            item_kind({"step_id": "s1"})


class TestLoad(unittest.TestCase):
    def test_loads_solarwinds(self):
        doc = load_layer3(SOLARWINDS)
        self.assertEqual(doc["metadata"]["incident_id"], "SOLARWINDS-SUNBURST-2020")
        self.assertEqual(len(doc["path_sequence"]), 4)

    def test_missing_sequence_names_file(self):
        with self.assertRaises(Layer3Error) as cm:
            check_document({"metadata": {"incident_id": "X"}}, "some/file.json")
        self.assertIn("some/file.json", str(cm.exception))
        self.assertIn("path_sequence", str(cm.exception))

    def test_bad_item_names_position(self):
        doc = {"metadata": {"incident_id": "X"}, "path_sequence": [{"step_id": "s1", "cluster": "#7"}, {"foo": 1}]}
        with self.assertRaises(Layer3Error) as cm:
            check_document(doc, "f.json")
        self.assertIn("path_sequence[1]", str(cm.exception))

    def test_bad_group_member_named(self):
        doc = {"metadata": {"incident_id": "X"},
               "path_sequence": [{"mode": "parallel", "steps": [{"step_id": "a", "cluster": "#8"}, {"nope": True}]}]}
        with self.assertRaises(Layer3Error) as cm:
            check_document(doc, "f.json")
        self.assertIn("path_sequence[0].steps[1]", str(cm.exception))

    def test_missing_incident_id(self):
        with self.assertRaises(Layer3Error):
            check_document({"metadata": {}, "path_sequence": [{"step_id": "s1", "cluster": "#7"}]}, "f.json")


class TestSequenceHelpers(unittest.TestCase):
    def test_flat_steps_expands_groups(self):
        seq = json.loads(AGENT_BTZ.read_text(encoding="utf-8"))["path_sequence"]
        ids = [s["step_id"] for s in flat_steps(seq)]
        self.assertEqual(ids[:3], ["s1a-usb-drop", "s1b-social-lure", "s2-agent-btz-execution"])

    def test_classified_clusters_distinct_in_order(self):
        seq = json.loads(SOLARWINDS.read_text(encoding="utf-8"))["path_sequence"]
        self.assertEqual(classified_clusters(seq), ["#10", "#7", "#4", "#1"])

    def test_classified_clusters_skips_unresolved(self):
        seq = json.loads(UNRESOLVED.read_text(encoding="utf-8"))["path_sequence"]
        self.assertEqual(classified_clusters(seq), ["#3", "#7", "#4", "#1"])

    def test_entry_cluster_step(self):
        seq = json.loads(SOLARWINDS.read_text(encoding="utf-8"))["path_sequence"]
        self.assertEqual(entry_cluster(seq), "#10")

    def test_entry_cluster_unresolved_first_is_none(self):
        seq = json.loads(AD_CASCADE.read_text(encoding="utf-8"))["path_sequence"]
        self.assertEqual(seq[0]["status"], "unresolved")
        self.assertIsNone(entry_cluster(seq))

    def test_entry_cluster_mixed_group_is_none(self):
        seq = json.loads(AGENT_BTZ.read_text(encoding="utf-8"))["path_sequence"]  # (#8 + #9)
        self.assertIsNone(entry_cluster(seq))

    def test_entry_cluster_uniform_group(self):
        seq = [{"mode": "parallel", "steps": [{"step_id": "a", "cluster": "#6"}, {"step_id": "b", "cluster": "TLCTC-06.01"}]}]
        self.assertEqual(entry_cluster(seq), "#6")


if __name__ == "__main__":
    unittest.main()
