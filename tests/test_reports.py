import csv
import io
import unittest

from regnav_evidence.reports import csv_report, csv_text, markdown_report
from regnav_evidence.validation import validate
from tests.test_validation import ledger


class ReportTests(unittest.TestCase):
    def test_csv_formulas_are_text_in_every_user_column(self):
        for text in ("=1+1", "+SUM(A1)", "-1+2", "@SUM(A1)", " \t=1+1", "\ufeff=1+1", "\u200b=1+1", "\u00a0=1+1", "\u202e=1+1", "\ttext", "\rtext"):
            with self.subTest(text=text):
                self.assertTrue(csv_text(text).startswith("'"))
        value = ledger()
        value["claims"][0]["text"] = '=HYPERLINK("https://example.org")'
        value["sources"][0]["title"] = "+SUM(A1:A2)"
        value["claims"][0]["review"]["reviewer"] = "@SUM(A1)"
        rows = list(csv.reader(io.StringIO(csv_report(value, validate(value)))))
        self.assertEqual(len(rows), 2)
        self.assertTrue(rows[1][1].startswith("'="))
        self.assertTrue(rows[1][3].startswith("'@"))
        self.assertTrue(rows[1][6].startswith("'+"))
        self.assertEqual(csv_text("Ordinary legal analysis"), "Ordinary legal analysis")

    def test_csv_commas_quotes_and_multiline_text_round_trip(self):
        value = ledger()
        value["claims"][0]["text"] = 'A, B and "C"\ncontinued'
        rows = list(csv.reader(io.StringIO(csv_report(value, validate(value)))))
        self.assertEqual(rows[1][1], value["claims"][0]["text"])

    def test_markdown_does_not_execute_html_or_break_table_cells(self):
        value = ledger()
        value["claims"][0]["text"] = '<img src=x onerror=alert(1)> | [link](javascript:x)\nnext'
        report = markdown_report(value, validate(value))
        self.assertNotIn("<img", report)
        self.assertIn("&lt;img", report)
        self.assertIn("\\|", report)
        self.assertIn("\\[link\\]", report)
        self.assertNotIn("\nnext", report)
        self.assertIn("User-declared", report)
        self.assertIn("does not verify", report)

    def test_gfm_strikethrough_markers_remain_literal(self):
        value = ledger()
        value["title"] = "Ledger ~~archived~~"
        value["claims"][0]["text"] = "An ~~excluded~~ qualification remains recorded."
        value["sources"][0]["title"] = "Source ~~draft~~"
        report = markdown_report(value, validate(value))
        self.assertTrue(report.startswith(r"# Ledger \~\~archived\~\~"))
        self.assertIn(r"\~\~excluded\~\~", report)
        self.assertIn(r"\~\~draft\~\~", report)
        self.assertNotIn("~~excluded~~", report)

    def test_unlinked_claims_and_unused_sources_remain_visible(self):
        value = ledger()
        value["claims"][0]["review_status"] = "unreviewed"
        value["claims"][0]["evidence"] = []
        report = markdown_report(value, validate(value))
        self.assertIn("CLAIM-a", report)
        self.assertIn("SRC-a", report)
        self.assertIn("UNUSED", report)
        self.assertIn("NO", report)

    def test_invalid_ledgers_are_not_exported(self):
        value = ledger()
        value["claims"][0]["evidence"][0]["source_id"] = "missing"
        for render in (markdown_report, csv_report):
            with self.subTest(render=render):
                with self.assertRaises(ValueError):
                    render(value, validate(value))


if __name__ == "__main__":
    unittest.main()

