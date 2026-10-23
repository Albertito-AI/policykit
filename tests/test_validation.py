import copy
import json
from pathlib import Path
import tempfile
import unittest

from regnav_evidence.validation import LedgerReadError, load_ledger, validate


def ledger():
    return {
        "schema_version": "1.0", "title": "Test ledger",
        "sources": [{"id": "SRC-a", "title": "Training fixture", "url": "https://example.org/source", "source_type": "other", "jurisdiction": "Fictional", "version": "1"}],
        "claims": [{"id": "CLAIM-a", "text": "A test proposition.", "review_status": "checked", "evidence": [{"source_id": "SRC-a", "pinpoint": "p 1", "relation": "supports"}], "review": {"reviewer": "Test reviewer", "date": "2025-02-28"}}],
    }


class ValidationTests(unittest.TestCase):
    def codes(self, value):
        return {finding.code for finding in validate(value).findings}

    def test_complete_structure_does_not_claim_truth(self):
        result = validate(ledger())
        self.assertTrue(result.structurally_valid)
        self.assertEqual(result.warnings, [])
        self.assertIn("does not verify", result.to_dict()["notice"])
        self.assertNotIn("verified", result.to_dict())

    def test_duplicate_source_claim_and_cross_kind_ids(self):
        value = ledger()
        value["sources"].append(copy.deepcopy(value["sources"][0]))
        self.assertIn("DUPLICATE_ID", self.codes(value))
        value = ledger()
        value["claims"].append(copy.deepcopy(value["claims"][0]))
        self.assertIn("DUPLICATE_ID", self.codes(value))
        value = ledger()
        value["claims"][0]["id"] = "SRC-a"
        self.assertIn("DUPLICATE_ID", self.codes(value))

    def test_bad_dates_are_rejected(self):
        for bad in ("2025-02-29", "2025-2-01", "20250101", "2025-01-01T12:00:00Z", 20250101, None):
            with self.subTest(bad=bad):
                value = ledger()
                value["claims"][0]["review"]["date"] = bad
                self.assertIn("INVALID_DATE", self.codes(value))
        value = ledger()
        value["sources"][0]["as_of"] = "2024-02-29"
        self.assertTrue(validate(value).structurally_valid)

    def test_unsafe_and_malformed_urls_are_rejected(self):
        for url in ("javascript:alert(1)", "file:///tmp/secret", "/relative", "https://", "https://user:password@example.org", "https://example.org/a b", "https://example.org:99999/a", "https://example.org\\evil", "https://[bad"):
            with self.subTest(url=url):
                value = ledger()
                value["sources"][0]["url"] = url
                self.assertIn("INVALID_URL", self.codes(value))
        value = ledger()
        value["sources"][0]["url"] = "https://example.org:443/a?b=c#paragraph-1"
        self.assertTrue(validate(value).structurally_valid)

    def test_dangling_reference_and_no_evidence(self):
        value = ledger()
        value["claims"][0]["evidence"][0]["source_id"] = "SRC-missing"
        self.assertIn("UNKNOWN_SOURCE", self.codes(value))
        value["claims"][0]["evidence"] = []
        self.assertIn("NO_EVIDENCE", self.codes(value))
        self.assertFalse(validate(value).structurally_valid)

    def test_checked_requires_human_metadata_and_pinpoint(self):
        value = ledger()
        del value["claims"][0]["review"]
        self.assertIn("CHECKED_WITHOUT_REVIEW", self.codes(value))
        value = ledger()
        value["claims"][0]["review"] = {"reviewer": "", "date": "bad"}
        self.assertFalse(validate(value).structurally_valid)
        value = ledger()
        value["claims"][0]["evidence"][0]["pinpoint"] = "  "
        self.assertFalse(validate(value).structurally_valid)
        self.assertIn("MISSING_PINPOINT", self.codes(value))

    def test_incomplete_review_is_warning(self):
        value = ledger()
        value["claims"][0]["review_status"] = "unreviewed"
        del value["claims"][0]["review"]
        value["claims"][0]["evidence"][0]["pinpoint"] = ""
        result = validate(value)
        self.assertTrue(result.structurally_valid)
        self.assertEqual({f.code for f in result.warnings}, {"UNREVIEWED_CLAIM", "MISSING_PINPOINT"})

    def test_contradiction_requires_visible_resolution_to_clear_warning(self):
        value = ledger()
        value["claims"][0]["evidence"].append({"source_id": "SRC-a", "pinpoint": "p 2", "relation": "contradicts"})
        self.assertIn("UNRESOLVED_CONTRADICTION", self.codes(value))
        value["claims"][0]["review"]["resolution"] = "The proposition is limited to draft A, and paragraph 2 addresses draft B."
        self.assertNotIn("UNRESOLVED_CONTRADICTION", self.codes(value))

    def test_unknown_version_unused_source_and_unknown_fields(self):
        value = ledger()
        del value["sources"][0]["version"]
        self.assertIn("UNRECORDED_VERSION", self.codes(value))
        value["claims"] = []
        self.assertIn("UNUSED_SOURCE", self.codes(value))
        value["surprise"] = True
        self.assertIn("UNKNOWN_FIELD", self.codes(value))

    def test_arbitrary_json_shapes_fail_cleanly(self):
        for value in (None, True, [], "text", {"sources": None, "claims": [None]}):
            with self.subTest(value=value):
                self.assertFalse(validate(value).structurally_valid)
        for path, bad in (("evidence", [False]), ("evidence", {}), ("review", []), ("review", None), ("review_status", [])):
            value = ledger()
            value["claims"][0][path] = bad
            self.assertFalse(validate(value).structurally_valid)

    def test_surrogate_and_control_characters_are_not_exportable(self):
        for bad in ("Bad\ud800text", "Bad\x1btext"):
            value = ledger()
            value["claims"][0]["text"] = bad
            self.assertIn("CONTROL_CHARACTER", self.codes(value))
            self.assertFalse(validate(value).structurally_valid)

    def test_duplicate_keys_constants_empty_and_invalid_encoding(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "ledger.json"
            for data in (b"", b"{", b'{"title":"a","title":"b"}', b'{"x":NaN}', b"\xff\xfe"):
                with self.subTest(data=data):
                    path.write_bytes(data)
                    with self.assertRaises(LedgerReadError):
                        load_ledger(path)
            path.write_text(json.dumps(ledger()), encoding="utf-8-sig")
            self.assertTrue(validate(load_ledger(path)).structurally_valid)


if __name__ == "__main__":
    unittest.main()

