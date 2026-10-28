"""Mocked provider-contract tests. No live model accuracy is claimed."""

from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from regnav_esg.ingest import ingest_document
from regnav_esg.model import model_extract, validate_model_items, _response_text


class ModelAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        path = Path(self.tmp.name) / "fictional.txt"
        path.write_text("FICTIONAL report. Scope 1 emissions: 100 tCO2e.\fThe board adopted a plan.")
        self.document = ingest_document(path)
        self.item = {"category": "emissions", "claim": "Reported Scope 1 emissions are 100 tCO2e.",
                     "source_id": self.document["source"]["source_id"], "page_number": 1,
                     "quote": "Scope 1 emissions: 100 tCO2e.", "metric": "Scope 1", "value": "100",
                     "unit": "tCO2e", "period": None}

    def test_valid_quote_still_not_verified_claim(self):
        output = validate_model_items(self.document, {"items": [self.item], "unresolved": []})
        self.assertEqual(len(output["items"]), 1)
        self.assertFalse(output["items"][0]["claim_support_verified"])
        self.assertEqual(output["items"][0]["review_status"], "unreviewed")

    def test_wrong_quote_page_and_source_are_rejected(self):
        for update in ({"quote": "Scope 1 emissions: 900 tCO2e."}, {"page_number": 2},
                       {"page_number": 99}, {"page_number": True}, {"source_id": "other"}):
            item = {**self.item, **update}
            result = validate_model_items(self.document, {"items": [item], "unresolved": []})
            self.assertEqual(result["items"], [])
            self.assertEqual(len(result["rejected_items"]), 1)

    def test_invented_numeric_or_period_field_rejected(self):
        for update in ({"value": "999999"}, {"value": "10"}, {"period": "2025"}, {"unit": "kgCO2e"}):
            item = {**self.item, **update}
            result = validate_model_items(self.document, {"items": [item], "unresolved": []})
            self.assertEqual(result["items"], [])
            self.assertEqual(result["rejected_items"][0]["reason"], "structured_fields_not_in_quote")

    def test_quoted_page_must_have_been_sent(self):
        result = validate_model_items(self.document, {"items": [self.item], "unresolved": []}, permitted_pages={2})
        self.assertEqual(result["rejected_items"][0]["reason"], "page_not_supplied_to_model")

    def test_duplicate_quote_is_ambiguous(self):
        from hashlib import sha256
        doc = deepcopy(self.document)
        doc["pages"][0]["text"] += " " + self.item["quote"]
        doc["pages"][0]["text_sha256"] = sha256(doc["pages"][0]["text"].encode()).hexdigest()
        result = validate_model_items(doc, {"items": [self.item], "unresolved": []})
        self.assertEqual(result["rejected_items"][0]["reason"], "quotation_ambiguous_exact")

    def test_network_is_opt_in(self):
        with patch("urllib.request.build_opener") as opener:
            with self.assertRaisesRegex(ValueError, "allow_network"):
                model_extract(self.document, model="operator-selected-model", api_key="fixture")
            opener.assert_not_called()

    def test_https_and_credentials_restrictions(self):
        for endpoint in ("http://example.org/v1/responses", "https://user:secret@example.org/v1/responses"):
            with self.assertRaises(ValueError):
                model_extract(self.document, model="fixture", api_key="fixture", allow_network=True, endpoint=endpoint)

    def test_mocked_request_and_checked_response(self):
        payload = {"status": "completed", "id": "fictional-response", "output": [{"type": "message", "content": [{"type": "output_text", "text": json.dumps({"items": [self.item], "unresolved": ["Period not supplied"]})}]}]}
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(payload).encode()
        opener = MagicMock()
        opener.open.return_value = response
        with patch("urllib.request.build_opener", return_value=opener):
            result = model_extract(self.document, model="fixture", api_key="fixture", allow_network=True)
        request = opener.open.call_args.args[0]
        sent = json.loads(request.data)
        self.assertFalse(sent["store"])
        self.assertNotIn("tools", sent)
        self.assertEqual(sent["text"]["format"]["type"], "json_schema")
        self.assertEqual(len(result["items"]), 1)
        self.assertEqual(result["process"]["pages_sent"], [1, 2])

    def test_incomplete_refused_and_malformed_responses_rejected(self):
        for payload in ({"status": "incomplete"}, {"status": "completed", "output": None},
                        {"status": "completed", "output": ["bad"]},
                        {"status": "completed", "output": [{"type": "message", "content": ["bad"]}]},
                        {"status": "completed", "output": [{"type": "message", "content": [{"type": "refusal"}]}]}):
            with self.assertRaises(ValueError):
                _response_text(payload)
