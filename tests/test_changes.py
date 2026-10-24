"""Record-change comparison regressions use fictional metadata only."""

import copy
import unittest

from regnav_evidence.changes import compare_ledgers, text_report


def fixture():
    return {
        "schema_version": "1.0", "title": "Training test",
        "sources": [
            {"id": "SRC-a", "title": "Fictional rule", "url": "https://example.org/a",
             "source_type": "other", "jurisdiction": "Fictional", "version": "v1", "accessed": "2026-10-20"},
            {"id": "SRC-b", "title": "Other fictional record", "url": "https://example.org/b",
             "source_type": "other", "jurisdiction": "Fictional", "version": "v1"},
        ],
        "claims": [
            {"id": "CLAIM-a", "text": "Original proposition", "review_status": "checked",
             "review": {"reviewer": "Synthetic reviewer", "date": "2026-10-20"},
             "evidence": [{"source_id": "SRC-a", "pinpoint": "p 1", "relation": "supports"}]},
            {"id": "CLAIM-b", "text": "Another proposition", "review_status": "unreviewed",
             "evidence": [{"source_id": "SRC-b", "pinpoint": "p 2", "relation": "context"}]},
        ],
    }


class ComparisonTests(unittest.TestCase):
    def test_identical_and_reordered_arrays_are_unchanged(self):
        original = fixture()
        revised = copy.deepcopy(original)
        revised["sources"].reverse()
        revised["claims"].reverse()
        self.assertEqual(compare_ledgers(original, revised)["summary"],
                         {"changed_ledger_fields": 0, "changed_sources": 0,
                          "changed_claims": 0, "prior_reviews_to_reconsider": 0})

    def test_source_version_change_affects_only_linked_review(self):
        original = fixture()
        revised = copy.deepcopy(original)
        revised["sources"][0]["version"] = "v2"
        result = compare_ledgers(original, revised)
        self.assertEqual(result["sources"][0]["change"], "material")
        self.assertEqual([item["id"] for item in result["claims"]], ["CLAIM-a"])
        self.assertTrue(result["claims"][0]["recheck_prior_review"])
        self.assertIn("SRC-a", result["claims"][0]["reasons"][0])

    def test_access_date_and_review_note_do_not_stale_review(self):
        original = fixture()
        revised = copy.deepcopy(original)
        revised["sources"][0]["accessed"] = "2026-10-21"
        revised["claims"][0]["review"]["note"] = "Editorial reminder"
        result = compare_ledgers(original, revised)
        self.assertEqual(result["sources"][0]["change"], "metadata_only")
        self.assertEqual(result["claims"][0]["change"], "review_declaration_only")
        self.assertFalse(result["claims"][0]["recheck_prior_review"])

    def test_legal_notes_conservatively_trigger_recheck(self):
        original = fixture()
        revised = copy.deepcopy(original)
        revised["sources"][0]["notes"] = "New substantive interpretation"
        revised["claims"][0]["notes"] = "Qualification changed"
        result = compare_ledgers(original, revised)
        self.assertEqual(result["sources"][0]["change"], "material")
        self.assertTrue(result["claims"][0]["recheck_prior_review"])

    def test_claim_text_and_pinpoint_trigger_recheck(self):
        original = fixture()
        revised = copy.deepcopy(original)
        revised["claims"][0]["text"] += " with qualification"
        revised["claims"][0]["evidence"][0]["pinpoint"] = "p 3"
        result = compare_ledgers(original, revised)
        self.assertEqual(result["summary"]["prior_reviews_to_reconsider"], 1)
        self.assertIn("Evidence links changed", result["claims"][0]["reasons"])
        self.assertEqual(original["claims"][0]["review_status"], "checked")
        self.assertEqual(revised["claims"][0]["review_status"], "checked")

    def test_review_declaration_change_is_not_source_recheck(self):
        original = fixture()
        revised = copy.deepcopy(original)
        revised["claims"][0]["review"]["date"] = "2026-10-22"
        result = compare_ledgers(original, revised)
        self.assertEqual(result["claims"][0]["change"], "review_declaration_only")
        self.assertEqual(result["summary"]["prior_reviews_to_reconsider"], 0)

    def test_unreviewed_source_change_does_not_claim_prior_review(self):
        original = fixture()
        revised = copy.deepcopy(original)
        revised["sources"][1]["url"] = "https://example.org/new"
        result = compare_ledgers(original, revised)
        self.assertEqual(result["claims"][0]["change"], "material")
        self.assertFalse(result["claims"][0]["recheck_prior_review"])

    def test_renames_are_removals_and_additions(self):
        original = fixture()
        revised = copy.deepcopy(original)
        revised["sources"][0]["id"] = "SRC-renamed"
        revised["claims"][0]["evidence"][0]["source_id"] = "SRC-renamed"
        revised["claims"][0]["id"] = "CLAIM-renamed"
        result = compare_ledgers(original, revised)
        self.assertEqual([x["change"] for x in result["sources"]], ["removed", "added"])
        self.assertIn("removed", [x["change"] for x in result["claims"]])
        self.assertIn("added", [x["change"] for x in result["claims"]])

    def test_root_description_edit_is_reported_without_review_flag(self):
        original = fixture()
        revised = copy.deepcopy(original)
        revised["description"] = "Corrected project description"
        result = compare_ledgers(original, revised)
        self.assertEqual(result["ledger_fields"], ["description"])
        self.assertEqual(result["summary"]["prior_reviews_to_reconsider"], 0)

    def test_evidence_reordering_does_not_change_review(self):
        original = fixture()
        original["claims"][0]["evidence"].append(
            {"source_id": "SRC-b", "pinpoint": "p 4", "relation": "qualifies"})
        revised = copy.deepcopy(original)
        revised["claims"][0]["evidence"].reverse()
        self.assertEqual(compare_ledgers(original, revised)["summary"]["changed_claims"], 0)
        self.assertIn("Compared: 0 source change", text_report(compare_ledgers(original, revised)))


if __name__ == "__main__":
    unittest.main()
