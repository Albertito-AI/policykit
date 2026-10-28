"""Fictional screening rubrics; no normative thresholds are asserted."""
from copy import deepcopy
import json
import unittest

from regnav_esg.materiality import StandardsRegistry, screen_materiality


def materiality_input():
    rubric = {"rubric_id": "fictional-rubric", "version": "v1", "rationale": "Fictional operator-selected screening rubric", "dimensions": ["magnitude", "likelihood"], "scale_min": "0", "scale_max": "5", "threshold": "3", "aggregation": "weighted_mean", "weights": {"magnitude": "0.75", "likelihood": "0.25"}}
    assessment = {"scores": {"magnitude": "4", "likelihood": "2"}, "rationale": "Fictional supplied facts", "evidence": [{"source_id": "fictional-report", "version": "v1", "pinpoint": "page 2"}]}
    return {"rubrics": {"financial": deepcopy(rubric), "impact": deepcopy(rubric)}, "topics": [{"topic_id": "water", "title": "Fictional water topic", "financial": deepcopy(assessment), "impact": deepcopy(assessment)}]}


def standard():
    return {"framework": "Fictional Standard", "version": "2025", "code": "1.2", "title": "Fictional disclosure", "source": {"url": "https://example.org/fictional-standard", "version": "2025", "pinpoint": "paragraph 1.2"}}


class MaterialityTests(unittest.TestCase):
    def test_rounded_score_cannot_cross_exact_threshold(self):
        payload = materiality_input()
        payload["topics"][0]["financial"]["scores"] = {"magnitude": "5", "likelihood": "0"}
        payload["rubrics"]["financial"]["weights"] = {"magnitude": "1e100", "likelihood": "1e-100"}
        payload["rubrics"]["financial"]["threshold"] = "5"
        result = screen_materiality(payload)["topics"][0]["financial"]
        self.assertEqual(result["score"], "5")
        self.assertTrue(result["score_display_rounded"])
        self.assertEqual(result["status"], "screened_out")

    def test_weighted_screening_and_json_safe(self):
        payload = materiality_input()
        original = deepcopy(payload)
        result = screen_materiality(payload)
        self.assertEqual(result["topics"][0]["financial"]["score"], "3.5")
        self.assertEqual(result["topics"][0]["financial"]["status"], "screened_in")
        self.assertEqual(result["review_status"], "unreviewed")
        self.assertEqual(payload, original)
        json.dumps(result, allow_nan=False)

    def test_financial_and_impact_do_not_override_each_other(self):
        payload = materiality_input()
        payload["topics"][0]["financial"]["scores"] = {"magnitude": "1", "likelihood": "1"}
        result = screen_materiality(payload)["topics"][0]
        self.assertEqual(result["financial"]["status"], "screened_out")
        self.assertEqual(result["impact"]["status"], "screened_in")

    def test_exact_threshold_is_inclusive(self):
        payload = materiality_input()
        payload["topics"][0]["financial"]["scores"] = {"magnitude": "3", "likelihood": "3"}
        self.assertEqual(screen_materiality(payload)["topics"][0]["financial"]["status"], "screened_in")

    def test_maximum_rubric(self):
        payload = materiality_input()
        payload["rubrics"]["impact"]["aggregation"] = "maximum"
        del payload["rubrics"]["impact"]["weights"]
        self.assertEqual(screen_materiality(payload)["topics"][0]["impact"]["score"], "4")

    def test_missing_evidence_prevents_screened_out(self):
        payload = materiality_input()
        payload["topics"][0]["financial"]["evidence"] = []
        result = screen_materiality(payload)["topics"][0]["financial"]
        self.assertEqual(result["status"], "insufficient_information")
        self.assertIsNone(result["score"])
        self.assertIn("evidence_not_supplied", result["reasons"])

    def test_missing_score_is_not_zero(self):
        payload = materiality_input()
        del payload["topics"][0]["financial"]["scores"]["likelihood"]
        result = screen_materiality(payload)["topics"][0]["financial"]
        self.assertEqual(result["status"], "insufficient_information")
        self.assertIn("missing_score:likelihood", result["reasons"])

    def test_missing_perspective_not_inferred(self):
        payload = materiality_input()
        del payload["rubrics"]["impact"]
        self.assertEqual(screen_materiality(payload)["topics"][0]["impact"]["reasons"], ["rubric_not_supplied"])

    def test_invalid_weights_and_threshold_rejected(self):
        for mutation in ({"weights": {"magnitude": "1"}}, {"threshold": "6"}, {"weights": {"magnitude": "0", "likelihood": "1"}}):
            payload = materiality_input()
            payload["rubrics"]["financial"].update(mutation)
            with self.assertRaises(ValueError):
                screen_materiality(payload)

    def test_score_out_of_range_and_unknown_dimension_rejected(self):
        for scores in ({"magnitude": "6", "likelihood": "1"}, {"magnitude": "1", "likelihood": "1", "extra": "2"}):
            payload = materiality_input()
            payload["topics"][0]["financial"]["scores"] = scores
            with self.assertRaises(ValueError):
                screen_materiality(payload)

    def test_registry_exact_version_no_fuzzy_fallback(self):
        registry = StandardsRegistry([standard()])
        self.assertEqual(registry.lookup("Fictional Standard", "2025", "1.2")["source"]["pinpoint"], "paragraph 1.2")
        with self.assertRaisesRegex(ValueError, "Unknown exact"):
            registry.lookup("Fictional Standard", "2026", "1.2")

    def test_registry_validates_pinpoints_and_duplicates(self):
        record = standard()
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            StandardsRegistry([record, deepcopy(record)])
        del record["source"]["pinpoint"]
        with self.assertRaisesRegex(ValueError, "pinpoint"):
            StandardsRegistry([record])

    def test_resolved_citations_preserve_source_and_are_copies(self):
        payload = materiality_input()
        payload["standards"] = [standard()]
        payload["topics"][0]["standard_refs"] = [{"framework": "Fictional Standard", "version": "2025", "code": "1.2"}]
        result = screen_materiality(payload)
        citation = result["topics"][0]["standard_citations"][0]
        self.assertEqual(citation["source_status"], "supplied_not_independently_verified")
        citation["source"]["pinpoint"] = "changed"
        self.assertEqual(payload["standards"][0]["source"]["pinpoint"], "paragraph 1.2")


if __name__ == "__main__":
    unittest.main()
