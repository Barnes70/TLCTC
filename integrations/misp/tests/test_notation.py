import json
import unittest
from pathlib import Path

from cli.notation import render_boundary, render_intra, render_item, render_path, render_step, strip_dre

ROOT = Path(__file__).resolve().parents[3]
SOLARWINDS = ROOT / "json-schemas" / "layer-3" / "examples" / "solarwinds-2020.json"
AGENT_BTZ = ROOT / "attack-paths" / "agent-btz-usb-2008.json"
UNRESOLVED = ROOT / "json-schemas" / "layer-3" / "examples" / "unresolved-step-example-2026.json"

# Copied verbatim from metadata.notes of the SolarWinds example (spec §7.8).
SOLARWINDS_NOTES_NOTATION = "#10 ||[update][@Vendor→@Org]|| →[Δt=instant] #7 →[Δt=~14d] #4 →[Δt=~2h] #1 + [DRE: C]"
# JSON-faithful rendering: s3 and s4 both carry outcomes ["C"].
SOLARWINDS_EXPECTED = "#10 ||[update][@Vendor→@Org]|| →[Δt=instant] #7 →[Δt=~14d] #4 + [DRE: C] →[Δt=~2h] #1 + [DRE: C]"


def seq(path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestPieces(unittest.TestCase):
    def test_boundary_plain(self):
        self.assertEqual(render_boundary({"context": "update", "source_sphere": "@Vendor", "target_sphere": "@Org"}),
                         "||[update][@Vendor→@Org]||")

    def test_boundary_transit_in_order(self):
        b = {"context": "sms", "source_sphere": "@Attacker", "target_sphere": "@Victim", "transit_spheres": ["@Carrier1", "@Carrier2"]}
        self.assertEqual(render_boundary(b), "||[sms][@Attacker⇒@Carrier1⇒@Carrier2→@Victim]||")

    def test_intra(self):
        self.assertEqual(render_intra({"type": "privilege", "from": "@Container", "to": "@Kernel"}), "|[privilege][@Container→@Kernel]|")

    def test_step_full(self):
        step = {"step_id": "s", "cluster": "#2",
                "topology_boundary": {"context": "api", "source_sphere": "@External", "target_sphere": "@Org"},
                "intra_system_boundaries": [{"type": "privilege", "from": "@Container", "to": "@Kernel"}],
                "outcomes": ["C", "Ii"]}
        self.assertEqual(render_step(step), "#2 ||[api][@External→@Org]|| |[privilege][@Container→@Kernel]| + [DRE: C, Ii]")

    def test_operational_id_rendered_raw(self):
        self.assertEqual(render_step({"step_id": "s", "cluster": "TLCTC-07.02"}), "TLCTC-07.02")

    def test_unresolved_single_and_gap(self):
        self.assertEqual(render_step({"step_id": "u", "status": "unresolved", "unresolved_type": "single", "notes": "n"}), "?")
        self.assertEqual(render_step({"step_id": "u", "status": "unresolved", "unresolved_type": "gap", "notes": "n"}), "…")

    def test_unresolved_keeps_boundary_never_dre(self):
        u = {"step_id": "u", "status": "unresolved", "unresolved_type": "single", "notes": "n",
             "topology_boundary": {"context": "human", "source_sphere": "@External", "target_sphere": "@Org"}}
        self.assertEqual(render_step(u), "? ||[human][@External→@Org]||")

    def test_group(self):
        g = {"mode": "parallel", "steps": [{"step_id": "a", "cluster": "#8"}, {"step_id": "b", "cluster": "#9"}]}
        self.assertEqual(render_item(g), "(#8 + #9)")


class TestPaths(unittest.TestCase):
    def test_solarwinds_exact(self):
        doc = seq(SOLARWINDS)
        self.assertEqual(render_path(doc["path_sequence"]), SOLARWINDS_EXPECTED)

    def test_solarwinds_matches_notes_modulo_dre(self):
        doc = seq(SOLARWINDS)
        self.assertIn(SOLARWINDS_NOTES_NOTATION, doc["metadata"]["notes"])
        self.assertEqual(strip_dre(render_path(doc["path_sequence"])), strip_dre(SOLARWINDS_NOTES_NOTATION))

    def test_group_with_velocity(self):
        doc = seq(AGENT_BTZ)
        rendered = render_path(doc["path_sequence"])
        self.assertTrue(rendered.startswith(
            "(#8 ||[physical][@External→@Military]|| + #9 ||[human][@External→@Military]||) →[Δt=~10s] #7 →[Δt=~2d] #4"), rendered)

    def test_unresolved_example(self):
        doc = seq(UNRESOLVED)
        self.assertEqual(render_path(doc["path_sequence"]),
                         "#3 →[Δt=instant] #7 →[Δt=4h] ? →[Δt=<10m] #4 →[Δt=instant] … →[Δt=instant] #1 + [DRE: Ac]")

    def test_connector_without_delta(self):
        self.assertEqual(render_path([{"step_id": "a", "cluster": "#9"}, {"step_id": "b", "cluster": "#7"}]), "#9 → #7")

    def test_strip_dre(self):
        self.assertEqual(strip_dre("#4 + [DRE: C] → #1 + [DRE: C, Ii]"), "#4 → #1")


if __name__ == "__main__":
    unittest.main()
