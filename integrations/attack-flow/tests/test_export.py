import json
import unittest
from pathlib import Path

from cli.export import export_layer3, strategic, sub_cluster
from cli.stixflow import read_stix
from cli.stixutil import AF_EXT_ID, TLCTC_EXT_ID, TLCTC_IDENTITY_ID

ROOT = Path(__file__).resolve().parents[3]
SOLARWINDS = ROOT / "json-schemas/layer-3/examples/solarwinds-2020.json"
AGENT_BTZ = ROOT / "attack-paths/agent-btz-usb-2008.json"
AD_CASCADE = ROOT / "attack-paths/ad-domain-admin-cascade-2025.json"
EXAMPLES = Path(__file__).resolve().parents[1] / "stix/examples"


class HelperTests(unittest.TestCase):
    def test_strategic_and_sub(self):
        self.assertEqual(strategic("#7"), "#7")
        self.assertEqual(strategic("#10"), "#10")
        self.assertEqual(strategic("TLCTC-07.30"), "#7")
        self.assertEqual(strategic("#8.2"), "#8")
        self.assertEqual(sub_cluster("TLCTC-08.20"), "TLCTC-08.20")
        self.assertEqual(sub_cluster("#8.2"), "TLCTC-08.20")
        self.assertIsNone(sub_cluster("#8"))
        with self.assertRaises(ValueError):
            strategic("#11")


class ExportTests(unittest.TestCase):
    def test_solarwinds_round_trip(self):
        b = export_layer3(SOLARWINDS)
        types = [o["type"] for o in b["objects"]]
        self.assertEqual(types.count("attack-flow"), 1)
        self.assertEqual(types.count("attack-action"), 4)
        self.assertEqual(types.count("extension-definition"), 2)
        ids = {o["id"] for o in b["objects"]}
        self.assertIn(TLCTC_EXT_ID, ids)
        self.assertIn(AF_EXT_ID, ids)
        self.assertIn(TLCTC_IDENTITY_ID, ids)
        actions = [o for o in b["objects"] if o["type"] == "attack-action"]
        clusters = [o["extensions"][TLCTC_EXT_ID]["tlctc_cluster"] for o in actions]
        self.assertEqual(clusters, ["#10", "#7", "#4", "#1"])
        first = actions[0]["extensions"][TLCTC_EXT_ID]
        self.assertEqual(first["tlctc_boundary"]["context"], "update")
        self.assertEqual(first["tlctc_delta_t_to_next"], "instant")
        self.assertTrue(actions[1]["extensions"][TLCTC_EXT_ID]["tlctc_fec_executed"])
        for a in actions:
            self.assertEqual(a["extensions"][AF_EXT_ID]["extension_type"], "new-sdo")
        # chain: each action except the last has exactly one effect_ref pointing at the next
        for a, nxt in zip(actions, actions[1:]):
            self.assertEqual(a["effect_refs"], [nxt["id"]])
        self.assertNotIn("effect_refs", actions[-1])
        flow = next(o for o in b["objects"] if o["type"] == "attack-flow")
        self.assertEqual(flow["start_refs"], [actions[0]["id"]])
        self.assertTrue(flow["extensions"][TLCTC_EXT_ID]["tlctc_notation"].startswith("#10"))
        # deterministic
        self.assertEqual(export_layer3(SOLARWINDS), b)
        # readable by our own STIX reader
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.json"
            p.write_text(json.dumps(b), encoding="utf-8")
            f = read_stix(p)
            self.assertEqual(len(f.actions), 4)
            self.assertEqual(len(f.edges), 3)

    def test_parallel_group_becomes_operator(self):
        b = export_layer3(AGENT_BTZ)
        ops = [o for o in b["objects"] if o["type"] == "attack-operator"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0]["operator"], "AND")
        members = [o for o in b["objects"] if o["type"] == "attack-action" and o.get("effect_refs") == [ops[0]["id"]]]
        self.assertGreaterEqual(len(members), 2, "every member of the group leads into the AND operator")
        self.assertEqual(len(ops[0]["effect_refs"]), 1, "the operator leads on to exactly the next step")
        flow = next(o for o in b["objects"] if o["type"] == "attack-flow")
        self.assertEqual(set(flow["start_refs"]), {m["id"] for m in members}, "a leading parallel group starts the flow at its members")
        self.assertEqual(ops[0]["extensions"][TLCTC_EXT_ID]["tlctc_group_id"], "g1-usb-plant")

    def test_unresolved_step(self):
        b = export_layer3(AD_CASCADE)
        unresolved = [o for o in b["objects"] if o["type"] == "attack-action" and o["extensions"][TLCTC_EXT_ID]["tlctc_status"] == "unresolved"]
        self.assertGreaterEqual(len(unresolved), 1)
        ext = unresolved[0]["extensions"][TLCTC_EXT_ID]
        self.assertNotIn("tlctc_cluster", ext)
        self.assertNotIn("tlctc_dre", ext)
        self.assertIn("tlctc_unresolved_type", ext)
        self.assertIn("tlctc_notes", ext)

    def test_examples_on_disk_are_current(self):
        for src, name in ((SOLARWINDS, "solarwinds-2020"), (AGENT_BTZ, "agent-btz-usb-2008"), (AD_CASCADE, "ad-domain-admin-cascade-2025")):
            with open(EXAMPLES / f"{name}.attack-flow.json", encoding="utf-8") as fh:
                self.assertEqual(json.load(fh), export_layer3(src), name)


if __name__ == "__main__":
    unittest.main()
