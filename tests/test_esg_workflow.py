"""Integration tests use fictional source text and no model service."""

from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from regnav_esg.cli import main
from regnav_esg.extract import extract_candidates
from regnav_esg.ingest import ingest_document
from regnav_esg.io import read_json
from regnav_esg.reports import render_html, to_ledger
from regnav_esg.workflow import run_workbench
from regnav_esg.workflow import _csv_text
from regnav_evidence.validation import validate


class WorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "fictional.txt"
        self.source.write_text("FICTIONAL TRAINING REPORT.\nScope 1 emissions: 120 tCO2e.\nThe board reviewed the plan.\fLimited assurance covers selected metrics only.", encoding="utf-8")
        self.document = ingest_document(self.source)
        self.extraction = extract_candidates(self.document)

    def test_end_to_end_ledger_is_unreviewed_and_structure_valid(self):
        destination = self.root / "workspace"
        result = run_workbench([self.source], destination, source_urls=["https://example.org/fictional-report"])
        self.assertEqual(result["status"], "completed")
        ledger = read_json(destination / "ledger.json")
        self.assertFalse(validate(ledger).errors)
        self.assertTrue(ledger["claims"])
        self.assertTrue(all(c["review_status"] == "unreviewed" for c in ledger["claims"]))
        self.assertTrue(all(c["evidence"][0]["relation"] == "context" for c in ledger["claims"]))
        self.assertIn("Text segment", ledger["claims"][0]["evidence"][0]["pinpoint"])
        self.assertIn("report.html", result["files"])

    def test_existing_output_not_overwritten(self):
        output = self.root / "workspace"
        output.mkdir()
        sentinel = output / "keep.txt"
        sentinel.write_text("keep")
        with self.assertRaisesRegex(ValueError, "already exists"):
            run_workbench([self.source], output)
        self.assertEqual(sentinel.read_text(), "keep")

    def test_ledger_requires_source_urls(self):
        result = run_workbench([self.source], self.root / "without-url")
        self.assertFalse(result["ledger_exported"])
        self.assertNotIn("ledger.json", result["files"])

    def test_source_mismatch_rejected(self):
        bad = deepcopy(self.extraction)
        bad["source"]["sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "identities"):
            to_ledger([self.document], [bad], ["https://example.org/fictional"])

    def test_tampered_quote_rejected(self):
        bad = deepcopy(self.extraction)
        bad["fields"][0]["candidates"][0]["text"] = "invented"
        with self.assertRaisesRegex(ValueError, "citation"):
            render_html([self.document], [bad])

    def test_tampered_structured_value_rejected(self):
        bad = deepcopy(self.extraction)
        bad["fields"][0]["candidates"][0]["captured_fields"]["value"] = "999999"
        with self.assertRaisesRegex(ValueError, "Captured field"):
            render_html([self.document], [bad])

    def test_malformed_extraction_is_contract_error(self):
        with self.assertRaises(ValueError):
            render_html([self.document], [[]])

    def test_mismatched_lengths_rejected(self):
        with self.assertRaises(ValueError):
            render_html([self.document], [])

    def test_html_source_injection_is_escaped(self):
        self.source.write_text('The board says <script>alert("x")</script>.', encoding="utf-8")
        doc = ingest_document(self.source)
        output = render_html([doc], [extract_candidates(doc)])
        self.assertNotIn('<script>alert("x")</script>', output)
        self.assertIn('&lt;script&gt;', output)
        self.assertIn("Content-Security-Policy", output)

    def test_cli_empty_input_returns_incomplete_status(self):
        self.source.write_text("", encoding="utf-8")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            status = main(["ingest", str(self.source)])
        self.assertEqual(status, 2)
        self.assertEqual(json.loads(out.getvalue())["status"], "empty_document")

    def test_duplicate_json_and_nan_rejected(self):
        for text in ('{"a":1,"a":2}', '{"a":NaN}'):
            path = self.root / "bad.json"
            path.write_text(text)
            with self.assertRaises(ValueError):
                read_json(path)

    def test_cli_wrong_input_no_output(self):
        with patch("sys.stderr", new_callable=io.StringIO):
            self.assertEqual(main(["inventory", str(self.source)]), 1)

    def test_formula_guard_handles_unicode_format_prefixes(self):
        text = _csv_text([{"fields": [{"field_id": "water", "category": "environment", "candidates": [{"text": "\u2060=2+2 water", "citation": {"page_number": 1}}]}]}])
        self.assertIn("'\u2060=2+2 water", text)

    def test_explicit_invalid_assessment_not_replaced_with_empty_object(self):
        for value in ([], False):
            with self.assertRaises(ValueError):
                run_workbench([self.source], self.root / "invalid-output", assessment=value)
        self.assertFalse((self.root / "invalid-output").exists())
