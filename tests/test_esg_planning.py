"""Fictional plans test traceability, missing data and budget integrity."""
from copy import deepcopy
import json
import unittest

from regnav_esg.planning import build_action_plan


def plan():
    return {"plan_id": "fictional-plan", "as_of": "2026-10-28", "gaps": [{"gap_id": "g1", "description": "Missing source pinpoint", "priority": "high", "action": {"title": "Locate underlying source passage", "owner": "Fictional reviewer", "due_date": "2026-11-02", "success_criterion": "Record reproducible source pinpoint", "budget": {"currency": "SGD", "min": "10.10", "max": "20.20", "basis": "Fictional supplied estimate"}}}]}


class PlanningTests(unittest.TestCase):
    def test_plan_preserves_gap_and_scheduling(self):
        payload = plan()
        original = deepcopy(payload)
        result = build_action_plan(payload)
        self.assertEqual(result["actions"][0]["owner"], "Fictional reviewer")
        self.assertEqual(result["actions"][0]["status"], "proposed")
        self.assertFalse(result["actions"][0]["overdue"])
        self.assertEqual(result["actions"][0]["source_gap"], payload["gaps"][0])
        self.assertEqual(payload, original)
        json.dumps(result, allow_nan=False)

    def test_missing_fields_are_not_invented(self):
        payload = plan()
        del payload["gaps"][0]["action"]
        result = build_action_plan(payload)
        action = result["actions"][0]
        self.assertEqual(action["status"], "draft_missing_fields")
        self.assertIsNone(action["owner"])
        self.assertIsNone(action["due_date"])
        self.assertIsNone(action["budget"])
        self.assertEqual(action["missing_fields"], ["owner", "due_date", "success_criterion"])
        self.assertFalse(result["budget_coverage"]["complete"])

    def test_exact_budget_total(self):
        payload = plan()
        second = deepcopy(payload["gaps"][0])
        second["gap_id"] = "g2"
        payload["gaps"].append(second)
        self.assertEqual(build_action_plan(payload)["budget_totals"], [{"currency": "SGD", "min": "20.2", "max": "40.4"}])

    def test_currencies_are_not_combined(self):
        payload = plan()
        second = deepcopy(payload["gaps"][0])
        second["gap_id"] = "g2"
        second["action"]["budget"]["currency"] = "USD"
        payload["gaps"].append(second)
        self.assertEqual(len(build_action_plan(payload)["budget_totals"]), 2)

    def test_invalid_budget_ranges_rejected(self):
        for change in ({"min": "21"}, {"min": "-1"}, {"currency": "usd"}, {"basis": ""}, {"max": "NaN"}):
            payload = plan()
            payload["gaps"][0]["action"]["budget"].update(change)
            with self.assertRaises(ValueError):
                build_action_plan(payload)

    def test_overdue_is_date_based_not_legal_finding(self):
        payload = plan()
        payload["gaps"][0]["action"]["due_date"] = "2026-10-27"
        result = build_action_plan(payload)["actions"][0]
        self.assertTrue(result["overdue"])
        self.assertEqual(result["status"], "proposed")
        self.assertEqual(result["review_status"], "unreviewed")

    def test_closed_and_deferred_are_retained_not_reopened(self):
        for status in ("closed", "deferred"):
            payload = plan()
            payload["gaps"][0]["status"] = status
            result = build_action_plan(payload)
            self.assertEqual(result["actions"], [])
            self.assertEqual(result["skipped_gaps"][0]["status"], status)

    def test_exact_template_resolution_and_overrides(self):
        payload = plan()
        action = payload["gaps"][0].pop("action")
        payload["templates"] = [{"template_id": "pinpoint", "gap_code": "missing_pinpoint", "action": action}]
        payload["gaps"][0].update(template_id="pinpoint", code="missing_pinpoint", action={"owner": "Another fictional reviewer"})
        result = build_action_plan(payload)["actions"][0]
        self.assertEqual(result["owner"], "Another fictional reviewer")
        self.assertEqual(result["due_date"], "2026-11-02")
        self.assertEqual(result["template_id"], "pinpoint")

    def test_unknown_or_wrong_template_rejected(self):
        payload = plan()
        payload["gaps"][0]["template_id"] = "missing"
        with self.assertRaisesRegex(ValueError, "Unknown template"):
            build_action_plan(payload)
        payload["templates"] = [{"template_id": "missing", "gap_code": "different", "action": {}}]
        with self.assertRaisesRegex(ValueError, "does not match"):
            build_action_plan(payload)

    def test_duplicate_gap_and_action_ids_rejected(self):
        payload = plan()
        payload["gaps"].append(deepcopy(payload["gaps"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate gap"):
            build_action_plan(payload)
        payload["gaps"][1]["gap_id"] = "g2"
        for gap in payload["gaps"]:
            gap["action"]["action_id"] = "same"
        with self.assertRaisesRegex(ValueError, "Duplicate action"):
            build_action_plan(payload)

    def test_partial_budget_total_reports_incomplete(self):
        payload = plan()
        payload["gaps"].append({"gap_id": "g2", "description": "Unknown action cost"})
        coverage = build_action_plan(payload)["budget_coverage"]
        self.assertEqual(coverage, {"actions_with_supplied_budget": 1, "total_actions": 2, "complete": False})


if __name__ == "__main__":
    unittest.main()
