import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from cli.config import Config, load_config


class TestConfig(unittest.TestCase):
    def test_defaults_resolve_repo_mappings(self):
        cfg = load_config(None)
        self.assertTrue(cfg.cwe_mapping_path.name == "tlctc-cwe.json")
        self.assertTrue(cfg.kev_mapping_path.name == "tlctc-kev.json")
        self.assertEqual(cfg.formats, ["json"])

    def test_json_config_overrides(self):
        with TemporaryDirectory() as d:
            p = Path(d) / "c.json"
            p.write_text(json.dumps({
                "formats": ["json", "markdown"],
                "source_globs": {"server": ["**/api/**"], "client": ["**/ui/**"]},
            }))
            cfg = load_config(p)
            self.assertEqual(cfg.formats, ["json", "markdown"])
            self.assertEqual(cfg.source_globs["server"], ["**/api/**"])

    def test_env_overrides_format(self):
        import os
        os.environ["TLCTC_SARIF_FORMATS"] = "sarif"
        try:
            cfg = load_config(None)
            self.assertEqual(cfg.formats, ["sarif"])
        finally:
            del os.environ["TLCTC_SARIF_FORMATS"]


if __name__ == "__main__":
    unittest.main()
