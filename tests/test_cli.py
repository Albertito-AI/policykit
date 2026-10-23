import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tests.test_validation import ledger


ROOT = Path(__file__).resolve().parents[1]


class CLITests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "ledger.json"

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-m", "regnav_evidence", *map(str, args)], cwd=ROOT, capture_output=True, text=True)

    def write(self, value):
        self.path.write_text(json.dumps(value), encoding="utf-8")

    def test_init_creates_blank_ledger_and_refuses_overwrite(self):
        result = self.run_cli("init", self.path, "--title", "Research register")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(self.path.read_text())["title"], "Research register")
        before = self.path.read_bytes()
        result = self.run_cli("init", self.path)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(before, self.path.read_bytes())

    def test_validation_exit_codes_and_json(self):
        self.write(ledger())
        result = self.run_cli("validate", self.path, "--json", "--strict")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["structurally_valid"])
        value = ledger()
        value["claims"][0]["review_status"] = "unreviewed"
        self.write(value)
        self.assertEqual(self.run_cli("validate", self.path).returncode, 0)
        self.assertEqual(self.run_cli("validate", self.path, "--strict").returncode, 2)
        value["claims"][0]["evidence"][0]["source_id"] = "missing"
        self.write(value)
        self.assertEqual(self.run_cli("validate", self.path).returncode, 1)

    def test_malformed_and_missing_file_errors_are_readable(self):
        self.path.write_text("{", encoding="utf-8")
        result = self.run_cli("validate", self.path)
        self.assertEqual(result.returncode, 1)
        self.assertIn("line 1", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        result = self.run_cli("validate", self.path.parent / "missing.json")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)

    def test_report_stdout_file_and_input_protection(self):
        self.write(ledger())
        result = self.run_cli("report", self.path, "--format", "csv")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stdout.startswith('"Claim ID"'))
        self.assertIn("does not verify", result.stderr)
        output = self.path.parent / "report.md"
        self.assertEqual(self.run_cli("report", self.path, "--output", output).returncode, 0)
        self.assertIn("# Test ledger", output.read_text())
        self.assertEqual(self.run_cli("report", self.path, "--output", output).returncode, 1)
        self.assertEqual(self.run_cli("report", self.path, "--output", output, "--force").returncode, 0)
        before = self.path.read_bytes()
        self.assertEqual(self.run_cli("report", self.path, "--output", self.path, "--force").returncode, 1)
        self.assertEqual(before, self.path.read_bytes())

    def test_invalid_input_creates_no_report(self):
        self.write({"schema_version": "bad"})
        output = self.path.parent / "report.md"
        result = self.run_cli("report", self.path, "--output", output)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(output.exists())

    def test_report_cannot_overwrite_input_via_hard_link(self):
        self.write(ledger())
        output = self.path.parent / "alias.json"
        try:
            os.link(self.path, output)
        except OSError:
            self.skipTest("Hard links are not supported in this test environment.")
        before = self.path.read_bytes()
        result = self.run_cli("report", self.path, "--output", output, "--force")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(before, self.path.read_bytes())


if __name__ == "__main__":
    unittest.main()
