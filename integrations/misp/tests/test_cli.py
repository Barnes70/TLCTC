import json
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from cli.tlctc_misp import main

ROOT = Path(__file__).resolve().parents[3]
SOLARWINDS = ROOT / "json-schemas" / "layer-3" / "examples" / "solarwinds-2020.json"
UNRESOLVED = ROOT / "json-schemas" / "layer-3" / "examples" / "unresolved-step-example-2026.json"


def run(args):
    with patch("sys.stdout", new=StringIO()) as out, patch("sys.stderr", new=StringIO()) as err:
        code = main(args)
    return code, out.getvalue(), err.getvalue()


class TestCli(unittest.TestCase):
    def test_convert_to_stdout(self):
        code, out, _ = run(["convert", str(SOLARWINDS)])
        self.assertEqual(code, 0)
        ev = json.loads(out)["Event"]
        self.assertEqual(ev["Object"][0]["name"], "tlctc-attack-path")
        self.assertEqual(len(ev["Object"]), 5)

    def test_convert_to_file_and_validate(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "sw.misp.json"
            code, out, err = run(["convert", str(SOLARWINDS), "-o", str(target), "--orgc", "TLCTC Project"])
            self.assertEqual(code, 0)
            self.assertEqual(out, "")
            self.assertIn("sw.misp.json", err)
            self.assertEqual(json.loads(target.read_text(encoding="utf-8"))["Event"]["Orgc"]["name"], "TLCTC Project")
            code, out, _ = run(["validate", str(target)])
            self.assertEqual(code, 0)
            self.assertIn("OK", out)

    def test_out_dir_batch(self):
        with tempfile.TemporaryDirectory() as d:
            code, _, _ = run(["convert", str(SOLARWINDS), str(UNRESOLVED), "--out-dir", d, "--no-attachment"])
            self.assertEqual(code, 0)
            names = sorted(p.name for p in Path(d).iterdir())
            self.assertEqual(names, ["solarwinds-2020.misp.json", "unresolved-step-example-2026.misp.json"])

    def test_output_with_many_inputs_rejected(self):
        with self.assertRaises(SystemExit):
            run(["convert", str(SOLARWINDS), str(UNRESOLVED), "-o", "x.json"])

    def test_bad_layer3_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "bad.json"
            bad.write_text(json.dumps({"metadata": {"incident_id": "B"}, "path_sequence": [{"nope": 1}]}), encoding="utf-8")
            code, out, err = run(["convert", str(bad)])
            self.assertEqual(code, 2)
            self.assertIn("bad.json", err)
            self.assertIn("path_sequence[0]", err)
            self.assertEqual(out, "")

    def test_validate_reports_problems(self):
        with tempfile.TemporaryDirectory() as d:
            _, out, _ = run(["convert", str(SOLARWINDS)])
            ev = json.loads(out)
            ev["Event"]["Object"][1]["template_uuid"] = "not-the-template"
            broken = Path(d) / "broken.json"
            broken.write_text(json.dumps(ev), encoding="utf-8")
            code, out, _ = run(["validate", str(broken)])
            self.assertEqual(code, 1)
            self.assertIn("template_uuid", out)

    def test_distribution_range_enforced(self):
        with self.assertRaises(SystemExit):
            run(["convert", str(SOLARWINDS), "--distribution", "7"])


if __name__ == "__main__":
    unittest.main()
