import unittest

from cli.resources import OBJECTS_DIR, TAXONOMY_PATH, Resources, load_template, load_taxonomy


class TestResources(unittest.TestCase):
    def setUp(self):
        self.res = Resources.load()

    def test_paths_exist(self):
        self.assertTrue((OBJECTS_DIR / "tlctc-attack-path" / "definition.json").is_file())
        self.assertTrue(TAXONOMY_PATH.is_file())

    def test_templates(self):
        self.assertEqual(self.res.path_template.name, "tlctc-attack-path")
        self.assertEqual(self.res.path_template.uuid, "7bda2ebc-9447-4273-a491-b7bd7a0715db")
        self.assertEqual(self.res.step_template.uuid, "b28f2295-ec5b-4bd8-95dc-a7965b8a1df5")
        self.assertEqual(self.res.step_template.version, 1)
        self.assertEqual(self.res.step_template.meta_category, "misc")
        self.assertIn("step-id", self.res.step_template.attributes)
        self.assertEqual(self.res.path_template.required, ["notation"])

    def test_taxonomy_values(self):
        t = self.res.taxonomy
        self.assertEqual(t.value("#7"), "07-malware")
        self.assertEqual(t.value("#10"), "10-supply-chain-attack")
        self.assertEqual(t.colour("#7"), "#ec4899")

    def test_tag(self):
        self.assertEqual(self.res.taxonomy.tag("cluster", "#7"), {"name": 'tlctc:cluster="07-malware"', "colour": "#ec4899"})
        self.assertEqual(self.res.taxonomy.tag("entry-cluster", "#9")["name"], 'tlctc:entry-cluster="09-social-engineering"')

    def test_all_ten(self):
        for n in range(1, 11):
            self.assertTrue(self.res.taxonomy.value(f"#{n}").startswith(f"{n:02d}-"))

    def test_unknown_predicate_raises(self):
        with self.assertRaises(KeyError):
            self.res.taxonomy.tag("velocity", "#7")

    def test_loaders(self):
        self.assertEqual(load_template("tlctc-attack-step").name, "tlctc-attack-step")
        self.assertEqual(load_taxonomy()["namespace"], "tlctc")


if __name__ == "__main__":
    unittest.main()
