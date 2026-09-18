import json
import unittest
from pathlib import Path

from cli.classify import classify
from cli.mapping import load_mapping
from cli.summary import pair_hypothesis, render_md, summarize

FIX = Path(__file__).resolve().parent / "fixtures" / "synthetic"


class SummaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        m = load_mapping()
        cls.results = []
        for p in sorted(FIX.glob("*.json")):
            with open(p, encoding="utf-8") as fh:
                cls.results.append(classify(json.load(fh), m))
        cls.s = summarize(cls.results)

    def test_counts(self):
        s = self.s
        self.assertEqual(s["records"], 9)
        # threat-bearing: phish+creds, creds alone, malware, dos, old-schema? (MitM unmapped -> no), potential (theft), partner = 6
        self.assertEqual(s["purity"]["threat_bearing"]["n"], 6)
        self.assertEqual(s["purity"]["operational_only"]["n"], 1)          # error-only
        self.assertEqual(s["purity"]["operational_only.error_or_failure"]["n"], 1)
        self.assertEqual(s["purity"]["unknown_only"]["n"], 1)              # unknown-only
        self.assertEqual(s["purity"]["mixed_threat_and_operational"]["n"], 1)  # partner-vector
        self.assertEqual(s["purity"]["empty"]["n"], 1)                     # old-schema (only unmapped + context + outcome)
        self.assertEqual(s["purity"]["records"]["denominator"], 9)

    def test_recoverability(self):
        r = self.s["recoverability"]
        self.assertEqual(r["threat_bearing"]["denominator"], 6)
        self.assertEqual(r["cause_lost"]["n"], 2)                          # creds alone, malware alone
        self.assertEqual(r["cause_lost.malware_without_enabler"]["n"], 1)
        self.assertEqual(r["cause_lost.credential_use_without_acquisition"]["n"], 1)
        self.assertEqual(r["rule_dependent"]["n"], 2)                      # dos, partner-vector
        self.assertEqual(r["resolved"]["n"], 2)                            # phish+creds, potential-disclosure
        self.assertEqual(r["single_cluster_records"]["n"], 3)              # creds alone, malware alone, theft

    def test_frequency_and_pairs(self):
        f = self.s["frequency"]
        self.assertEqual(f["#4"]["certain"]["n"], 2)
        self.assertEqual(f["#2"]["certain"]["n"], 1)
        self.assertEqual(f["#2"]["upper"]["n"], 2)                         # dos (one_of), partner-vector (certain + one_of, counted once)
        self.assertEqual(f["#6"]["upper"]["n"], 1)
        top = {p["pair"]: p for p in self.s["cooccurrence"]["top_pairs"]}
        self.assertEqual(top["#4 + #9"]["n"], 1)
        self.assertEqual(top["#4 + #9"]["hypothesis"], "#9 → #4")
        self.assertEqual(top["#2 + #7"]["hypothesis"], "#2 → #7")

    def test_availability(self):
        a = self.s["availability"]
        self.assertEqual(a["varieties"]["Obscuration"]["n"], 1)
        self.assertEqual(a["varieties"]["Obscuration"]["dre"], "Ac")
        self.assertEqual(a["ransomware"]["records"]["n"], 1)
        self.assertEqual(a["ransomware"]["with_obscuration_Ac"]["n"], 1)
        self.assertEqual(a["ransomware"]["with_obscuration_Ac"]["denominator"], 1)
        self.assertEqual(a["dre_codes"]["C"]["n"], 5)                      # phish, creds alone, error, old-schema, partner
        self.assertEqual(a["dre_codes"]["A"]["n"], 1)

    def test_unknown(self):
        u = self.s["unknown"]
        self.assertEqual(u["action_unknown"]["n"], 1)
        self.assertEqual(u["unmapped_values"]["n"], 1)
        self.assertEqual(u["per_category"]["malware"]["records"]["n"], 2)

    def test_pair_hypothesis(self):
        self.assertEqual(pair_hypothesis("#9", "#7"), "#9 → #7")
        self.assertEqual(pair_hypothesis("#1", "#7"), "#1 → #7")
        self.assertEqual(pair_hypothesis("#4", "#7"), "#4 → #7 | #7 → #4")
        self.assertEqual(pair_hypothesis("#1", "#2"), "order unknown")

    def test_render_md(self):
        md = render_md(self.s, title="nine fixtures")
        self.assertIn("### nine fixtures", md)
        self.assertIn("| #4 |", md)
        self.assertIn("with_obscuration_Ac", md)


if __name__ == "__main__":
    unittest.main()
