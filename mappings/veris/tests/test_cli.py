import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from cli.tlctc_veris import main

FIX = Path(__file__).resolve().parent / "fixtures" / "synthetic"


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class CliTests(unittest.TestCase):
    def test_single_file_json(self):
        code, out, _ = run("classify", str(FIX / "dos.json"))
        self.assertEqual(code, 0)
        doc = json.loads(out)
        self.assertEqual(len(doc), 1)
        self.assertEqual(doc[0]["clusters"]["one_of"], [["#2", "#3", "#6"]])

    def test_directory_md(self):
        code, out, _ = run("classify", str(FIX), "--format", "md")
        self.assertEqual(code, 0)
        self.assertIn("| incident_id |", out)
        self.assertEqual(out.count("11111111-0000-4000-8000-"), 9)

    def test_joined_array_and_output_file(self):
        records = []
        for p in sorted(FIX.glob("*.json")):
            with open(p, encoding="utf-8") as fh:
                records.append(json.load(fh))
        with tempfile.TemporaryDirectory() as td:
            joined = Path(td) / "joined.json"
            joined.write_text(json.dumps(records), encoding="utf-8")
            out_path = Path(td) / "summary.json"
            code, out, _ = run("classify", str(joined), "--summary", "-o", str(out_path))
            self.assertEqual(code, 0)
            self.assertEqual(out, "")
            s = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(s["records"], 9)

    def test_summary_md(self):
        code, out, _ = run("classify", str(FIX), "--summary", "--format", "md")
        self.assertEqual(code, 0)
        self.assertIn("Threat-axis purity", out)

    def test_attack_check_flag(self):
        code, out, _ = run("classify", str(FIX / "stolen-creds-with-phish.json"), "--attack-check")
        self.assertEqual(code, 0)
        doc = json.loads(out)
        self.assertIn("attack_check", doc[0])
        self.assertIn(doc[0]["attack_check"]["class"], ("agree", "subset", "disjoint", "no-attack-edge"))

    def test_exit_2_on_garbage(self):
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad.json"
            bad.write_text("{not json", encoding="utf-8")
            code, _, err = run("classify", str(bad))
            self.assertEqual(code, 2)
            self.assertIn("bad.json", err)

    def test_exit_2_on_missing(self):
        code, _, err = run("classify", os.path.join(str(FIX), "nope.json"))
        self.assertEqual(code, 2)
        self.assertIn("nope.json", err)


if __name__ == "__main__":
    unittest.main()
