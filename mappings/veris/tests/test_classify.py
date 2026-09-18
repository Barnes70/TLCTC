import json
import unittest
from pathlib import Path

from cli.classify import classify, veris_ids
from cli.mapping import load_mapping

FIX = Path(__file__).resolve().parent / "fixtures" / "synthetic"


def load(name):
    with open(FIX / f"{name}.json", encoding="utf-8") as fh:
        return json.load(fh)


class VerisIdsTests(unittest.TestCase):
    def test_walks_action_and_attribute(self):
        ids = veris_ids(load("stolen-creds-with-phish"))
        self.assertIn("action.social.variety.Phishing", ids)
        self.assertIn("action.social.vector.Email", ids)
        self.assertIn("action.hacking.variety.Use of stolen creds", ids)
        self.assertIn("attribute.confidentiality.data_disclosure.Yes", ids)
        self.assertNotIn("action.social.target.End-user", ids)

    def test_action_unknown(self):
        ids = veris_ids(load("unknown-only"))
        self.assertEqual(ids[0], "action.unknown")
        self.assertIn("action.unknown.result.Unknown", ids)


class ClassifyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_mapping()

    def c(self, name):
        return classify(load(name), self.m)

    def test_chain_resolved_by_recorded_enabler(self):
        r = self.c("stolen-creds-with-phish")
        self.assertEqual(r["clusters"]["certain"], ["#4", "#9"])
        self.assertEqual(r["clusters"]["one_of"], [])
        chains = {c["cluster"]: c for c in r["chains"]}
        self.assertIsNone(chains["#4"]["missing"])
        self.assertEqual(chains["#4"]["recorded_candidates"], ["#9"])
        self.assertIsNone(chains["#9"]["missing"])
        self.assertEqual(r["dre"], ["C"])
        self.assertEqual(r["context"]["boundary_contexts"], ["human"])
        self.assertEqual(r["context"]["role_hints"], ["server"])
        self.assertEqual(r["partition_rows"], ["attack"])
        self.assertTrue(r["threat_bearing"])
        self.assertFalse(r["mixed"])

    def test_chain_missing_acquisition(self):
        r = self.c("stolen-creds-alone")
        self.assertEqual(r["clusters"]["certain"], ["#4"])
        self.assertEqual(r["chains"][0]["missing"], "before")
        self.assertEqual(r["chains"][0]["recorded_candidates"], [])

    def test_malware_alone_has_lost_enabler_and_ac(self):
        r = self.c("malware-alone")
        self.assertEqual(r["clusters"]["certain"], ["#7"])
        self.assertEqual(r["chains"][0]["missing"], "before")
        self.assertEqual(r["dre"], ["Ac"])
        self.assertEqual(r["unresolved"], ["action.malware.vector.Unknown"])

    def test_conditional_becomes_one_of(self):
        r = self.c("dos")
        self.assertEqual(r["clusters"]["certain"], [])
        self.assertEqual(r["clusters"]["one_of"], [["#2", "#3", "#6"]])
        self.assertEqual(r["clusters_upper"], ["#2", "#3", "#6"])
        self.assertEqual(r["dre"], ["A"])
        self.assertTrue(r["threat_bearing"])

    def test_error_only_is_off_axis(self):
        r = self.c("error-only")
        self.assertTrue(r["off_axis_only"])
        self.assertFalse(r["threat_bearing"])
        self.assertEqual(r["partition_rows"], ["error_in_use"])
        self.assertEqual(r["dre"], ["C"])
        self.assertEqual(r["clusters"]["certain"], [])

    def test_unknown_only(self):
        r = self.c("unknown-only")
        self.assertFalse(r["off_axis_only"])
        self.assertFalse(r["threat_bearing"])
        self.assertEqual(r["unresolved"], ["action.unknown"])
        self.assertEqual(r["dre"], [])
        self.assertEqual(r["dre_potential"], ["C"])

    def test_old_schema_value_is_unmapped(self):
        r = self.c("old-schema")
        self.assertEqual(r["unmapped"], ["action.hacking.variety.MitM"])
        self.assertEqual(r["schema_version"], "1.3.5")
        self.assertEqual(r["context"]["role_hints"], ["server"])

    def test_potential_disclosure(self):
        r = self.c("potential-disclosure")
        self.assertEqual(r["clusters"]["certain"], ["#8"])
        self.assertEqual(r["dre"], [])
        self.assertEqual(r["dre_potential"], ["C"])
        self.assertEqual(r["context"]["boundary_contexts"], ["physical"])

    def test_mixed_record_with_partner_vector(self):
        r = self.c("partner-vector")
        self.assertEqual(r["clusters"]["certain"], ["#2", "#7"])
        self.assertEqual(r["clusters"]["one_of"], [["#2", "#3"]])
        self.assertEqual(r["clusters_upper"], ["#2", "#3", "#7"])
        self.assertEqual(r["context"]["boundaries"], ["@Vendor→@Org"])
        self.assertEqual(r["partition_rows"], ["abuse_of_rights", "attack"])
        self.assertTrue(r["mixed"])
        chains = {c["cluster"]: c for c in r["chains"]}
        self.assertIsNone(chains["#7"]["missing"])
        self.assertEqual(chains["#7"]["recorded_candidates"], ["#2", "#3"])
        self.assertEqual(r["dre"], ["C", "Ii"])


if __name__ == "__main__":
    unittest.main()
