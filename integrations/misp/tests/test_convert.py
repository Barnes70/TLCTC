import json
import unittest
import uuid
from pathlib import Path

from cli.convert import CONVERTER_NS, Options, build_info, convert, dumps, extract_urls
from cli.layer3 import classified_clusters, entry_cluster, load_layer3
from cli.resources import Resources
from cli.validate import validate_event

ROOT = Path(__file__).resolve().parents[3]
EXAMPLES = ROOT / "json-schemas" / "layer-3" / "examples"
ATTACK_PATHS = ROOT / "attack-paths"
ALL_FILES = sorted(ATTACK_PATHS.glob("*.json")) + sorted(EXAMPLES.glob("*.json"))
RES = Resources.load()


def conv(path, **kw):
    return convert(load_layer3(path), Options(**kw), RES, source_bytes=path.read_bytes())


def objects_by_step(event):
    out = {}
    for o in event["Event"]["Object"]:
        if o["name"] == "tlctc-attack-step":
            out[attr(o, "step-id")] = o
    return out


def attr(obj, relation):
    vals = [a["value"] for a in obj["Attribute"] if a["object_relation"] == relation]
    return vals[0] if len(vals) == 1 else (vals or None)


def attrs(obj, relation):
    return [a for a in obj["Attribute"] if a["object_relation"] == relation]


class TestCorpus(unittest.TestCase):
    def test_corpus_present(self):
        self.assertGreaterEqual(len(ALL_FILES), 60)

    def test_every_file_converts_and_validates(self):
        for p in ALL_FILES:
            with self.subTest(file=p.name):
                ev = conv(p)
                self.assertEqual(validate_event(ev, RES), [])

    def test_tags_match_sequence(self):
        for p in ALL_FILES:
            with self.subTest(file=p.name):
                doc = load_layer3(p)
                ev = conv(p)
                names = {t["name"] for t in ev["Event"]["Tag"]}
                expected = {RES.taxonomy.tag("cluster", c)["name"] for c in classified_clusters(doc["path_sequence"])}
                ec = entry_cluster(doc["path_sequence"])
                if ec:
                    expected.add(RES.taxonomy.tag("entry-cluster", ec)["name"])
                self.assertEqual(names, expected)
                self.assertLessEqual(sum(1 for n in names if n.startswith("tlctc:entry-cluster=")), 1)

    def test_info_length_and_determinism(self):
        for p in ALL_FILES:
            with self.subTest(file=p.name):
                a, b = conv(p), conv(p)
                self.assertLessEqual(len(a["Event"]["info"]), 256)
                self.assertEqual(dumps(a), dumps(b))


class TestSolarWinds(unittest.TestCase):
    def setUp(self):
        self.path = EXAMPLES / "solarwinds-2020.json"
        self.ev = conv(self.path)["Event"]
        self.pobj = [o for o in self.ev["Object"] if o["name"] == "tlctc-attack-path"][0]

    def test_event_header(self):
        self.assertEqual(self.ev["uuid"], str(uuid.uuid5(CONVERTER_NS, "SOLARWINDS-SUNBURST-2020")))
        self.assertEqual(self.ev["date"], "2026-02-23")
        self.assertEqual(self.ev["timestamp"], "1771804800")
        self.assertFalse(self.ev["published"])
        self.assertEqual((self.ev["analysis"], self.ev["threat_level_id"], self.ev["distribution"]), ("2", "4", "0"))
        self.assertNotIn("Orgc", self.ev)
        self.assertTrue(self.ev["info"].startswith("TLCTC SOLARWINDS-SUNBURST-2020: #10 ||[update][@Vendor→@Org]|| →[Δt=instant] #7"))

    def test_path_object(self):
        self.assertEqual(self.pobj["template_uuid"], RES.path_template.uuid)
        self.assertEqual(self.pobj["template_version"], "1")
        self.assertEqual(attr(self.pobj, "incident-id"), "SOLARWINDS-SUNBURST-2020")
        self.assertEqual(attr(self.pobj, "entry-cluster"), "#10")
        self.assertEqual(attr(self.pobj, "analyst-confidence"), "high")
        self.assertEqual(attr(self.pobj, "tlctc-version"), "2.3")
        self.assertEqual([a["value"] for a in attrs(self.pobj, "data-risk-event")], ["C"])
        att = attrs(self.pobj, "layer3-json")[0]
        self.assertEqual(att["type"], "attachment")
        self.assertEqual(att["value"], "SOLARWINDS-SUNBURST-2020.json")
        self.assertEqual(att["category"], "External analysis")
        self.assertTrue(att["data"])
        self.assertFalse(attrs(self.pobj, "incident-id")[0]["disable_correlation"])
        self.assertTrue(attrs(self.pobj, "notation")[0]["disable_correlation"])

    def test_includes_and_followed_by(self):
        steps = objects_by_step({"Event": self.ev})
        self.assertEqual(len(steps), 4)
        inc = [r for r in self.pobj["ObjectReference"] if r["relationship_type"] == "includes"]
        self.assertEqual({r["referenced_uuid"] for r in inc}, {o["uuid"] for o in steps.values()})
        s1 = steps["s1-supply-chain"]
        self.assertEqual(len(s1["ObjectReference"]), 1)
        ref = s1["ObjectReference"][0]
        self.assertEqual(ref["relationship_type"], "followed-by")
        self.assertEqual(ref["referenced_uuid"], steps["s2-sunburst-execution"]["uuid"])
        self.assertEqual(ref["object_uuid"], s1["uuid"])
        self.assertEqual(ref["comment"], "Δt=instant")
        self.assertEqual(steps["s2-sunburst-execution"]["ObjectReference"][0]["comment"], "Δt=~14d")
        self.assertEqual(steps["s4-cloud-abuse"]["ObjectReference"], [])

    def test_step_attributes_and_tag(self):
        steps = objects_by_step({"Event": self.ev})
        s1 = steps["s1-supply-chain"]
        self.assertEqual(attr(s1, "status"), "classified")
        self.assertEqual(attr(s1, "cluster"), "#10")
        self.assertEqual(attrs(s1, "cluster")[0]["Tag"], [RES.taxonomy.tag("cluster", "#10")])
        self.assertEqual((attr(s1, "boundary-context"), attr(s1, "boundary-source"), attr(s1, "boundary-target")), ("update", "@Vendor", "@Org"))
        self.assertEqual(attr(steps["s2-sunburst-execution"], "fec-executed"), "1")
        self.assertIsNone(attr(s1, "fec-executed"))
        self.assertEqual([a["value"] for a in attrs(steps["s3-credential-forgery"], "data-risk-event")], ["C"])

    def test_orgc_and_no_attachment(self):
        ev = conv(self.path, orgc="TLCTC Project", attachment=False, distribution=3)["Event"]
        self.assertEqual(ev["Orgc"], {"name": "TLCTC Project"})
        self.assertEqual(ev["distribution"], "3")
        pobj = [o for o in ev["Object"] if o["name"] == "tlctc-attack-path"][0]
        self.assertEqual(attrs(pobj, "layer3-json"), [])
        self.assertEqual(validate_event({"Event": ev}, RES), [])


class TestStructures(unittest.TestCase):
    def test_parallel_group(self):
        ev = conv(ATTACK_PATHS / "agent-btz-usb-2008.json")
        steps = objects_by_step(ev)
        s2 = steps["s2-agent-btz-execution"]["uuid"]
        for member in ("s1a-usb-drop", "s1b-social-lure"):
            refs = steps[member]["ObjectReference"]
            self.assertEqual([(r["referenced_uuid"], r["comment"]) for r in refs], [(s2, "Δt=~10s")])
        self.assertNotIn("tlctc:entry-cluster", " ".join(t["name"] for t in ev["Event"]["Tag"]))
        pobj = [o for o in ev["Event"]["Object"] if o["name"] == "tlctc-attack-path"][0]
        self.assertIsNone(attr(pobj, "entry-cluster"))
        self.assertTrue(attr(pobj, "notation").startswith("(#8 ||[physical]"))

    def test_predecessor_fans_out_into_group(self):
        seq = [{"step_id": "a", "cluster": "#9", "delta_t_to_next": "~1h"},
               {"mode": "parallel", "steps": [{"step_id": "b", "cluster": "#7"}, {"step_id": "c", "cluster": "#1"}], "delta_t_to_next": "~5m"},
               {"step_id": "d", "cluster": "#4"}]
        doc = {"metadata": {"incident_id": "FAN-1", "analyst_confidence": "low", "tlctc_version": "2.5", "created_at": "2026-01-01T00:00:00Z"}, "path_sequence": seq}
        ev = convert(doc, Options(), RES)
        steps = objects_by_step(ev)
        self.assertEqual({r["referenced_uuid"] for r in steps["a"]["ObjectReference"]}, {steps["b"]["uuid"], steps["c"]["uuid"]})
        self.assertEqual([r["comment"] for r in steps["a"]["ObjectReference"]], ["Δt=~1h", "Δt=~1h"])
        for m in ("b", "c"):
            self.assertEqual([(r["referenced_uuid"], r["comment"]) for r in steps[m]["ObjectReference"]], [(steps["d"]["uuid"], "Δt=~5m")])
        self.assertEqual(validate_event(ev, RES), [])

    def test_unresolved_steps(self):
        ev = conv(EXAMPLES / "unresolved-step-example-2026.json")
        steps = objects_by_step(ev)
        u = steps["s3-unknown-activity"]
        self.assertEqual(attr(u, "status"), "unresolved")
        self.assertIsNone(attr(u, "cluster"))
        self.assertEqual(attr(u, "unresolved-type"), "single")
        self.assertEqual([a["value"] for a in attrs(u, "candidates")], ["#2", "#7"])
        self.assertEqual(attrs(u, "data-risk-event"), [])
        self.assertTrue(all("Tag" not in a for a in u["Attribute"]))
        self.assertEqual(attr(steps["s5-lateral-gap"], "unresolved-type"), "gap")
        self.assertEqual(attr(u, "evidence"), "EDR-2026-0410-881")

    def test_unresolved_first_item_has_no_entry_tag(self):
        ev = conv(ATTACK_PATHS / "ad-domain-admin-cascade-2025.json")
        self.assertFalse(any(t["name"].startswith("tlctc:entry-cluster=") for t in ev["Event"]["Tag"]))

    def test_transit_boundary(self):
        steps = objects_by_step(conv(ATTACK_PATHS / "chalk-debug-phishing-2025.json"))
        s4 = steps["s4-trust-acceptance"]
        self.assertEqual(attr(s4, "boundary-source"), "@Maintainer(Qix)")
        self.assertEqual([a["value"] for a in attrs(s4, "boundary-transit")], ["@npm"])

    def test_intra_system_boundary(self):
        steps = objects_by_step(conv(ATTACK_PATHS / "openai-hf-cloud-escalation-2026.json"))
        self.assertEqual([a["value"] for a in attrs(steps["s6-2-kernel-privilege-escalation"], "intra-system-boundary")],
                         ["privilege:@Container→@Kernel"])


class TestHelpers(unittest.TestCase):
    def test_info_truncation(self):
        long = " → ".join(["#1"] * 200)
        info = build_info("X", long)
        self.assertEqual(len(info), 256)
        self.assertTrue(info.endswith("…"))
        self.assertEqual(build_info("X", "#9 → #7\n+ [DRE: C]"), "TLCTC X: #9 → #7 + [DRE: C]")

    def test_extract_urls(self):
        doc = {"metadata": {"incident_id": "U", "notes": "See https://example.org/report. Also (https://a.b/c)."},
               "path_sequence": [{"step_id": "s", "cluster": "#7", "evidence_refs": ["https://example.org/report", "ticket-1"]}]}
        self.assertEqual(extract_urls(doc), ["https://example.org/report", "https://a.b/c"])

    def test_validator_catches_bad_relation_and_dangling_reference(self):
        ev = conv(EXAMPLES / "solarwinds-2020.json")
        ev["Event"]["Object"][1]["Attribute"][0]["object_relation"] = "bogus"
        ev["Event"]["Object"][1]["ObjectReference"][0]["referenced_uuid"] = "00000000-0000-0000-0000-000000000000"
        errs = validate_event(ev, RES)
        self.assertTrue(any("bogus" in e for e in errs))
        self.assertTrue(any("00000000-0000-0000-0000-000000000000" in e for e in errs))
        self.assertTrue(any("step-id" in e and "required" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
