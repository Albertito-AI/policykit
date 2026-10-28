import json
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from regnav_esg.extract import ExtractionError, extract_candidates, extractive_summary
from regnav_esg.ingest import ingest_document


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        path = Path(self.temporary.name) / "fictional.md"
        path.write_text("Fictional training report, not an actual company.\nScope 1 emissions were 1,200 tCO2e.\nWater withdrawal was 200 m3.\fThe board oversees sustainability.\nLimited assurance covers selected indicators only.\nOur target is net-zero by 2050.", encoding="utf-8")
        self.document = ingest_document(path)

    def test_real_rule_extraction_and_exact_citations(self):
        result = extract_candidates(self.document)
        fields = {field["field_id"]: field for field in result["fields"]}
        scope = fields["scope_1"]["candidates"][0]
        self.assertEqual(scope["captured_fields"], {"value": "1,200", "unit": "tCO2e"})
        self.assertEqual(scope["status"], "unreviewed_candidate")
        self.assertEqual(fields["scope_3"]["status"], "not_found_by_rules")
        for field in result["fields"]:
            for item in field["candidates"]:
                anchor = item["citation"]
                text = self.document["pages"][anchor["page_number"] - 1]["text"]
                self.assertEqual(text[anchor["start"]:anchor["end"]], item["text"])
        json.dumps(result, allow_nan=False)

    def test_custom_schema_patterns_capture_strings(self):
        config = {"name": "Operator test rules", "version": "v1", "fields": [
            {"id": "withdrawals", "category": "custom_water", "patterns": [r"Water withdrawal was (?P<value>\d+) (?P<unit>m3)"], "keywords": []}]}
        result = extract_candidates(self.document, config=config)
        self.assertEqual(len(result["fields"]), 1)
        candidate = result["fields"][0]["candidates"][0]
        self.assertEqual(candidate["captured_fields"], {"value": "200", "unit": "m3"})
        self.assertEqual(candidate["citation"]["page_number"], 1)
        self.assertEqual(result["rules"]["version"], "v1")

    def test_summary_is_verbatim_page_cited_and_bounded(self):
        result = extractive_summary(self.document, max_sentences=2)
        self.assertEqual(len(result["sentences"]), 2)
        for sentence in result["sentences"]:
            self.assertEqual(sentence["text"], sentence["citation"]["exact_quote"])
            self.assertIn(sentence["text"], self.document["pages"][sentence["citation"]["page_number"] - 1]["text"])

    def test_config_rejects_duplicates_invalid_regex_and_unbounded_limits(self):
        for config in [
            {"fields": [{"id": "x", "keywords": ["water"]}, {"id": "x", "keywords": ["scope"]}]},
            {"fields": [{"id": "x", "patterns": ["("]}]},
            {"fields": [{"id": "x", "patterns": ["a*"]}]},
            {"fields": [{"id": "x"}]},
        ]:
            with self.assertRaises(ExtractionError):
                extract_candidates(self.document, config=config)
        with self.assertRaises(ExtractionError):
            extract_candidates(self.document, max_per_field=100)

    def test_keywords_use_boundaries_and_case_insensitive_whitespace(self):
        config = {"fields": [{"id": "notword", "keywords": ["waterfall"]}]}
        result = extract_candidates(self.document, config=config)
        self.assertEqual(result["fields"][0]["status"], "not_found_by_rules")

    def test_extraction_does_not_modify_input_document_or_config(self):
        snapshot = json.dumps(self.document, sort_keys=True)
        extract_candidates(self.document)
        self.assertEqual(json.dumps(self.document, sort_keys=True), snapshot)

    def test_pathological_regex_times_out_without_hanging_parent(self):
        path = Path(self.temporary.name) / "pathological.txt"
        path.write_text("a" * 10000 + "!", encoding="utf-8")
        document = ingest_document(path)
        config = {"fields": [{"id": "slow", "patterns": ["(a+)+$"]}]}
        with patch("regnav_esg.extract.PATTERN_TIMEOUT", 0.1):
            with self.assertRaises(ExtractionError) as error:
                extract_candidates(document, config=config)
        self.assertEqual(error.exception.code, "pattern_timeout")

    def test_custom_lookahead_cannot_attach_uncited_value(self):
        config = {"fields": [{"id": "outside", "patterns": [r"Water(?= withdrawal was (?P<value>\d+))"]}]}
        result = extract_candidates(self.document, config=config)
        candidate = result["fields"][0]["candidates"][0]
        self.assertEqual(candidate["captured_fields"], {})
        self.assertEqual(candidate["omitted_capture_groups"], ["value"])

    def test_numeric_match_retains_surrounding_negation_and_qualification(self):
        path = Path(self.temporary.name) / "qualified.txt"
        sentence = "Do not rely on the incorrect claim that Scope 1 emissions were 100 tCO2e."
        path.write_text(sentence, encoding="utf-8")
        result = extract_candidates(ingest_document(path))
        candidate = result["fields"][0]["candidates"][0]
        self.assertEqual(candidate["text"], sentence)
        self.assertEqual(candidate["captured_fields"]["value"], "100")
        self.assertEqual(candidate["status"], "unreviewed_candidate")
        self.assertFalse(candidate["context_truncated"])


if __name__ == "__main__":
    unittest.main()
