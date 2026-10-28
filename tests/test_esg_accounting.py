"""Fictional arithmetic fixtures, not real emissions factors."""
from copy import deepcopy
from decimal import Decimal
import json
import unittest

from regnav_esg.accounting import calculate_inventory


def inventory():
    return {
        "inventory_id": "fictional-inventory", "period_start": "2025-01-01", "period_end": "2025-12-31",
        "reporting_boundary": {"id": "fictional-boundary", "description": "Fictional facilities A and B", "consolidation_approach": "operational_control"},
        "factors": [{"factor_id": "fictional-electricity", "version": "v1", "value": "0.25", "activity_unit": "kWh", "output_unit": "kgCO2e", "valid_from": "2025-01-01", "valid_to": "2025-12-31", "source": {"url": "https://example.org/fictional-factors", "version": "v1", "pinpoint": "row 1"}}],
        "activities": [{"activity_id": "a1", "entity_id": "fictional-entity", "facility_id": "A", "date": "2025-06-30", "quantity": "2", "unit": "MWh", "factor_id": "fictional-electricity", "factor_version": "v1", "scope": 2, "scope2_basis": "location_based"}],
    }


class AccountingTests(unittest.TestCase):
    def test_activity_evidence_absence_is_explicit(self):
        payload = inventory()
        output = calculate_inventory(payload)
        self.assertEqual(output["activities_without_evidence"], 1)
        payload["activities"][0]["evidence"] = [{"source_id": "fictional-meter", "version": "v1", "pinpoint": "record 1"}]
        output = calculate_inventory(payload)
        self.assertEqual(output["activities_without_evidence"], 0)
        self.assertEqual(output["activities"][0]["evidence_status"], "references_supplied_unverified")

    def test_exact_conversion_and_lineage(self):
        payload = inventory()
        before = deepcopy(payload)
        output = calculate_inventory(payload)
        self.assertEqual(output["totals"]["scope2_location_based_kgco2e"], "500")
        self.assertEqual(output["activities"][0]["normalised_activity_quantity"], "2000")
        self.assertEqual(output["activities"][0]["factor"], payload["factors"][0])
        self.assertEqual(output["activities"][0]["activity"], payload["activities"][0])
        self.assertEqual(payload, before)
        json.dumps(output, allow_nan=False)

    def test_scope2_bases_are_not_added(self):
        payload = inventory()
        second = deepcopy(payload["activities"][0])
        second.update(activity_id="market-record", scope2_basis="market_based", quantity="1")
        payload["activities"].append(second)
        result = calculate_inventory(payload)
        self.assertEqual(result["totals"]["scope2_location_based_kgco2e"], "500")
        self.assertEqual(result["totals"]["scope2_market_based_kgco2e"], "250")
        self.assertNotIn("grand_total", result)

    def test_biogenic_is_outside_scope_totals(self):
        payload = inventory()
        factor = deepcopy(payload["factors"][0])
        factor.update(factor_id="fictional-biogenic", activity_unit="kg", output_unit="kgCO2", value="2")
        payload["factors"].append(factor)
        activity = deepcopy(payload["activities"][0])
        activity.update(activity_id="bio", factor_id="fictional-biogenic", scope=1, biogenic=True, unit="kg", quantity="3")
        payload["activities"].append(activity)
        result = calculate_inventory(payload)
        self.assertEqual(result["totals"]["biogenic_co2_kg"], "6")
        self.assertEqual(result["totals"]["scope1_kgco2e"], "0")

    def test_biogenic_co2e_cannot_be_mislabeled(self):
        payload = inventory()
        payload["activities"][0]["biogenic"] = True
        with self.assertRaisesRegex(ValueError, "Biogenic CO2"):
            calculate_inventory(payload)

    def test_factors_must_match_exact_version(self):
        payload = inventory()
        payload["activities"][0]["factor_version"] = "v2"
        with self.assertRaisesRegex(ValueError, "Missing exact"):
            calculate_inventory(payload)

    def test_factor_date_validity(self):
        payload = inventory()
        payload["factors"][0]["valid_to"] = "2025-03-31"
        with self.assertRaisesRegex(ValueError, "not valid"):
            calculate_inventory(payload)

    def test_missing_factor_metadata_rejected(self):
        for field in ("version", "valid_from", "valid_to", "source"):
            with self.subTest(field=field):
                payload = inventory()
                del payload["factors"][0][field]
                with self.assertRaises(ValueError):
                    calculate_inventory(payload)

    def test_factor_source_pinpoint_required(self):
        payload = inventory()
        del payload["factors"][0]["source"]["pinpoint"]
        with self.assertRaisesRegex(ValueError, "pinpoint"):
            calculate_inventory(payload)

    def test_incompatible_dimensions_rejected(self):
        payload = inventory()
        payload["activities"][0]["unit"] = "kg"
        with self.assertRaisesRegex(ValueError, "Incompatible"):
            calculate_inventory(payload)

    def test_ambiguous_unit_rejected(self):
        payload = inventory()
        payload["activities"][0]["unit"] = "gallon"
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            calculate_inventory(payload)

    def test_invalid_quantities_rejected(self):
        for value in ("NaN", "Infinity", "-1", True, 0.1):
            with self.subTest(value=value):
                payload = inventory()
                payload["activities"][0]["quantity"] = value
                with self.assertRaises(ValueError):
                    calculate_inventory(payload)

    def test_decimal_and_output_tonnes(self):
        payload = inventory()
        payload["activities"][0].update(quantity="0.1", unit="kWh")
        payload["factors"][0].update(value="0.2", output_unit="tCO2e")
        self.assertEqual(calculate_inventory(payload)["totals"]["scope2_location_based_kgco2e"], "20")

    def test_energy_conversion_divides_after_factor_multiplication(self):
        payload = inventory()
        payload["activities"][0].update(quantity="1", unit="MJ")
        payload["factors"][0]["value"] = "3.6"
        self.assertEqual(calculate_inventory(payload)["totals"]["scope2_location_based_kgco2e"], "1")

    def test_decimal_object_inputs_are_retained_as_json_strings(self):
        payload = inventory()
        payload["activities"][0]["quantity"] = Decimal("0.1")
        output = calculate_inventory(payload)
        self.assertEqual(output["activities"][0]["activity"]["quantity"], "0.1")
        json.dumps(output, allow_nan=False)

    def test_unobserved_buckets_are_identified(self):
        output = calculate_inventory(inventory())
        self.assertEqual(output["activity_counts_by_bucket"]["scope1_kgco2e"], 0)
        self.assertEqual(output["activity_counts_by_bucket"]["scope2_location_based_kgco2e"], 1)

    def test_nonfinite_metadata_rejected(self):
        payload = inventory()
        payload["other_metadata"] = float("nan")
        with self.assertRaises(ValueError):
            calculate_inventory(payload)

    def test_equity_share_requires_explicit_fraction(self):
        payload = inventory()
        payload["reporting_boundary"]["consolidation_approach"] = "equity_share"
        with self.assertRaisesRegex(ValueError, "equity_fraction"):
            calculate_inventory(payload)
        payload["activities"][0]["equity_fraction"] = "0.3"
        self.assertEqual(calculate_inventory(payload)["totals"]["scope2_location_based_kgco2e"], "150")

    def test_scope3_category_and_facility_rollup(self):
        payload = inventory()
        payload["activities"][0].update(scope=3, scope3_category=1)
        second = deepcopy(payload["activities"][0])
        second.update(activity_id="second", entity_id="another-entity", facility_id="B", scope3_category=4, quantity="1")
        payload["activities"].append(second)
        result = calculate_inventory(payload)
        self.assertEqual(result["scope3_categories_kgco2e"], {"1": "500", "4": "250"})
        self.assertEqual(len(result["facilities"]), 2)
        self.assertEqual(result["totals"]["scope3_kgco2e"], "750")

    def test_missing_scope2_and_scope3_classification(self):
        payload = inventory()
        del payload["activities"][0]["scope2_basis"]
        with self.assertRaisesRegex(ValueError, "scope2_basis"):
            calculate_inventory(payload)
        payload["activities"][0]["scope"] = 3
        with self.assertRaisesRegex(ValueError, "scope3_category"):
            calculate_inventory(payload)

    def test_duplicate_ids_and_out_of_period_rejected(self):
        payload = inventory()
        payload["activities"].append(deepcopy(payload["activities"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate activity"):
            calculate_inventory(payload)
        payload = inventory()
        payload["activities"][0]["date"] = "2024-12-31"
        with self.assertRaisesRegex(ValueError, "outside"):
            calculate_inventory(payload)

    def test_input_hash_tracks_factor_revision(self):
        payload = inventory()
        first = calculate_inventory(payload)["input_sha256"]
        payload["factors"][0]["source"]["pinpoint"] = "row 2"
        second = calculate_inventory(payload)["input_sha256"]
        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
