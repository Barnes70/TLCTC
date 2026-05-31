import json
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from cli.tlctc_sarif import main

FIX = Path(__file__).resolve().parent / "fixtures"
CFG = json.dumps({
    "cwe_mapping_path": str(FIX / "tiny-cwe.json"),
    "kev_mapping_path": str(FIX / "tiny-kev.json"),
    "formats": ["json"],
    "source_globs": {"server": ["**/api/**"], "client": ["**/ui/**"]},
})


class TestCli(unittest.TestCase):
    def _run(self, args):
        with patch("sys.stdout", new=StringIO()) as out:
            code = main(args)
        return code, out.getvalue()

    def setUp(self):
        self.cfgfile = FIX / "_cli-cfg.json"
        self.cfgfile.write_text(CFG, encoding="utf-8")

    def tearDown(self):
        self.cfgfile.unlink(missing_ok=True)

    def test_classify_emits_json_and_exit_zero(self):
        code, out = self._run(["classify", str(FIX / "semgrep-min.sarif"),
                               "--config", str(self.cfgfile)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["cluster_summary"]["#2"], 1)

    def test_fail_on_cluster_exits_nonzero(self):
        code, _ = self._run(["classify", str(FIX / "semgrep-min.sarif"),
                             "--config", str(self.cfgfile), "--fail-on-cluster", "#2"])
        self.assertEqual(code, 2)

    def test_unknown_format_errors_cleanly(self):
        with self.assertRaises(SystemExit):
            self._run(["classify", str(FIX / "semgrep-min.sarif"),
                       "--config", str(self.cfgfile), "--format", "csv"])


if __name__ == "__main__":
    unittest.main()
