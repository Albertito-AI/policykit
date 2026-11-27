import csv
import io
import unittest
from pathlib import Path

from regnav_evidence.reports import csv_report
from regnav_evidence.validation import load_ledger, validate


class DisclosureCaseTests(unittest.TestCase):
    def test_published_evidence_matches_ledger(self):
        case = Path(__file__).resolve().parents[1] / "cases" / "singapore-thailand-disclosure-2023"
        ledger = load_ledger(case / "ledger.json")
        result = validate(ledger)
        self.assertFalse(result.errors, result.errors)

        expected = csv.reader(io.StringIO(csv_report(ledger, result)))
        with (case / "evidence.csv").open(encoding="utf-8", newline="") as published:
            self.assertEqual(list(csv.reader(published)), list(expected))
