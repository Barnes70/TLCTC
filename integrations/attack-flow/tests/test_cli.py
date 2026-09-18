import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from cli.tlctc_attack_flow import main

FIX = Path(__file__).resolve().parent / "fixtures" / "corpus"
ROOT = Path(__file__).resolve().parents[3]


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class CliTests(unittest.TestCase):
    def test_classify_single_json(self):
        code, out, _ = run("classify", str(FIX / "Tesla Kubernetes Breach.afb"))
        self.assertEqual(code, 0)
        doc = json.loads(out)
        self.assertEqual(len(doc), 1)
        self.assertEqual(doc[0]["counts"]["actions"], 9)
        self.assertIn("notation_compressed", doc[0])

    def test_classify_dir_md_summary(self):
        code, out, _ = run("classify", str(FIX), "--summary", "--format", "md")
        self.assertEqual(code, 0)
        self.assertIn("Corpus profile", out)
        self.assertIn("| SolarWinds |", out)

    def test_classify_md_per_flow(self):
        code, out, _ = run("classify", str(FIX / "Equifax Breach.afb"), "--format", "md")
        self.assertEqual(code, 0)
        self.assertIn("Derived path (compressed)", out)

    def test_export_to_file(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "sw.json"
            code, out, _ = run("export", str(ROOT / "json-schemas/layer-3/examples/solarwinds-2020.json"), "-o", str(p))
            self.assertEqual(code, 0)
            self.assertEqual(out, "")
            b = json.loads(p.read_text(encoding="utf-8"))
            self.assertEqual(b["type"], "bundle")

    def test_validate_input(self):
        code, out, _ = run("validate-input", str(FIX / "SolarWinds.afb"))
        self.assertEqual(code, 0)
        self.assertIn("33 actions", out)

    def test_exit_2(self):
        code, _, err = run("classify", str(FIX / "nope.afb"))
        self.assertEqual(code, 2)
        self.assertIn("nope.afb", err)
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad.json"
            bad.write_text("{not json", encoding="utf-8")
            code, _, err = run("classify", str(bad))
            self.assertEqual(code, 2)
            code, _, err = run("export", str(bad))
            self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
