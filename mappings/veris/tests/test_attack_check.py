import unittest

from cli import attack_check
from cli.classify import classify
from cli.mapping import load_mapping


def rec(action, attribute=None):
    return {"incident_id": "x", "schema_version": "1.4.1", "action": action, "attribute": attribute or {}}


class AttackCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_mapping()
        cls.va = attack_check.load_veris_attack()
        cls.at = attack_check.load_attack_tlctc()

    def test_loaders(self):
        self.assertIn("action.social.variety.Phishing", self.va)
        self.assertTrue(any(t.startswith("T1566") for t in self.va["action.social.variety.Phishing"]))
        self.assertIn("T1566", self.at)
        self.assertIn("#9", self.at["T1566"])
        self.assertEqual(attack_check.technique_clusters("T1566.999", self.at), self.at["T1566"])

    def test_phishing_agrees(self):
        r = classify(rec({"social": {"variety": ["Phishing"], "vector": ["Email"]}}), self.m)
        c = attack_check.check(r, self.va, self.at, self.m)
        self.assertEqual(c["class"], "agree")
        self.assertIn("#9", c["transitive"])

    def test_error_has_no_attack_edge(self):
        r = classify(rec({"error": {"variety": ["Misdelivery"], "vector": ["Carelessness"]}}), self.m)
        c = attack_check.check(r, self.va, self.at, self.m)
        self.assertEqual(c["class"], "no-attack-edge")

    def test_classes_are_closed(self):
        r = classify(rec({"hacking": {"variety": ["SQLi"], "vector": ["Web application"]}}), self.m)
        c = attack_check.check(r, self.va, self.at, self.m)
        self.assertIn(c["class"], ("agree", "subset", "disjoint", "no-attack-edge"))
        self.assertEqual(c["direct"], ["#2"])

    def test_summarize_agreement(self):
        results = [classify(rec({"social": {"variety": ["Phishing"]}}), self.m), classify(rec({"error": {"variety": ["Loss"]}}), self.m)]
        checks = [attack_check.check(r, self.va, self.at, self.m) for r in results]
        s = attack_check.summarize_agreement(checks, self.m)
        self.assertEqual(s["classes"]["agree"]["n"], 1)
        self.assertEqual(s["classes"]["no-attack-edge"]["n"], 1)
        self.assertEqual(s["classes"]["agree"]["denominator"], 2)
        self.assertIsInstance(s["top_disagreements"], list)


if __name__ == "__main__":
    unittest.main()
