"""Offline activity-based emissions arithmetic using supplied, versioned factors.

No factors, reporting boundaries or legal requirements are inferred. Results are
calculations on caller-supplied records, not a verified GHG inventory.
"""

from copy import deepcopy
from datetime import date
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import json
from urllib.parse import urlparse


# Canonical quantities within each dimension. This is unit arithmetic, not an
# emissions-factor database. Unknown units are rejected rather than guessed.
_UNITS = {
    "g": ("mass", "0.001"), "kg": ("mass", "1"), "t": ("mass", "1000"),
    "Wh": ("energy", "0.001"), "kWh": ("energy", "1"),
    "MWh": ("energy", "1000"), "MJ": ("energy", "0.27777777777777777777777777777777777777777777777778"),
    "GJ": ("energy", "277.77777777777777777777777777777777777777777777778"),
    "mL": ("volume", "0.001"), "L": ("volume", "1"), "m3": ("volume", "1000"),
    "m": ("distance", "0.001"), "km": ("distance", "1"),
    "passenger-km": ("passenger_distance", "1"),
    "tonne-km": ("freight_distance", "1"), "unit": ("count", "1"),
}
_OUTPUTS = {"kgCO2e": ("CO2e", "1"), "tCO2e": ("CO2e", "1000"),
            "kgCO2": ("CO2", "1"), "tCO2": ("CO2", "1000")}


def _text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _number(value, field):
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise ValueError(f"{field} must be an exact decimal string or integer")
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{field} must be a decimal number") from exc
    if not number.is_finite() or number < 0:
        raise ValueError(f"{field} must be finite and non-negative")
    if len(number.as_tuple().digits) > 50 or abs(number.as_tuple().exponent) > 100:
        raise ValueError(f"{field} exceeds supported numeric precision")
    return number


def _decimal_text(number):
    if number == 0:
        return "0"
    text = format(number, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def _json_safe(value):
    """Detach input and normalise explicit Decimal values to JSON strings."""
    def convert(obj):
        if isinstance(obj, Decimal):
            if not obj.is_finite():
                raise ValueError("Input contains a non-finite decimal")
            return str(obj)
        return _unsupported(obj)
    try:
        return json.loads(json.dumps(value, default=convert, allow_nan=False))
    except (TypeError, OverflowError) as exc:
        raise ValueError("Input must contain only JSON-safe values") from exc


def _date(value, field):
    _text(value, field)
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be YYYY-MM-DD") from exc
    if parsed.isoformat() != value:
        raise ValueError(f"{field} must be YYYY-MM-DD")
    return parsed


def _source(source, field):
    if not isinstance(source, dict):
        raise ValueError(f"{field} must be an object")
    for name in ("url", "version", "pinpoint"):
        _text(source.get(name), f"{field}.{name}")
    parsed = urlparse(source["url"])
    if parsed.scheme not in ("https", "http") or not parsed.netloc:
        raise ValueError(f"{field}.url must be an absolute HTTP(S) URL")
    if parsed.username or parsed.password:
        raise ValueError(f"{field}.url must not contain credentials")
    return deepcopy(source)


def _unit_scales(source_unit, target_unit):
    if source_unit not in _UNITS or target_unit not in _UNITS:
        raise ValueError(f"Unsupported activity unit: {source_unit!r} or {target_unit!r}")
    source_dimension, source_scale = _UNITS[source_unit]
    target_dimension, target_scale = _UNITS[target_unit]
    if source_dimension != target_dimension:
        raise ValueError(f"Incompatible activity units: {source_unit} and {target_unit}")
    # Work in exact joules to avoid repeating-decimal conversion artefacts.
    if source_dimension == "energy":
        joules = {"Wh": 3600, "kWh": 3600000, "MWh": 3600000000,
                  "MJ": 1000000, "GJ": 1000000000}
        return Decimal(joules[source_unit]), Decimal(joules[target_unit])
    return Decimal(source_scale), Decimal(target_scale)


def _bucket(activity, output_kind):
    scope = activity.get("scope")
    if isinstance(scope, bool) or scope not in (1, 2, 3, "1", "2", "3"):
        raise ValueError("activity.scope must be 1, 2 or 3")
    scope = int(scope)
    biogenic = activity.get("biogenic", False)
    if not isinstance(biogenic, bool):
        raise ValueError("activity.biogenic must be a boolean")
    if biogenic:
        if output_kind != "CO2":
            raise ValueError("Biogenic CO2 must use a kgCO2 or tCO2 factor")
        return "biogenic_co2_kg"
    if output_kind != "CO2e":
        raise ValueError("Scope emissions must use a kgCO2e or tCO2e factor")
    if scope == 2:
        basis = activity.get("scope2_basis")
        if basis not in ("location_based", "market_based"):
            raise ValueError("Scope 2 requires location_based or market_based scope2_basis")
        return f"scope2_{basis}_kgco2e"
    if scope == 3:
        category = activity.get("scope3_category")
        if isinstance(category, bool) or not isinstance(category, int) or not 1 <= category <= 15:
            raise ValueError("Scope 3 requires an integer scope3_category from 1 to 15")
    return f"scope{scope}_kgco2e"


def calculate_inventory(payload):
    """Calculate separate scope/basis totals and retain complete input lineage.

    Required top-level fields: inventory_id, period_start, period_end,
    reporting_boundary, factors and activities. See the module tests for the
    complete JSON contract. Invalid or missing data raises ValueError.
    """
    if not isinstance(payload, dict):
        raise ValueError("Inventory must be an object")
    payload = _json_safe(payload)
    inventory_id = _text(payload.get("inventory_id"), "inventory_id")
    period_start = _date(payload.get("period_start"), "period_start")
    period_end = _date(payload.get("period_end"), "period_end")
    if period_end < period_start:
        raise ValueError("period_end precedes period_start")
    boundary = payload.get("reporting_boundary")
    if not isinstance(boundary, dict):
        raise ValueError("reporting_boundary must be an object")
    for name in ("id", "description"):
        _text(boundary.get(name), f"reporting_boundary.{name}")
    approach = boundary.get("consolidation_approach")
    if approach not in ("equity_share", "financial_control", "operational_control"):
        raise ValueError("Unknown consolidation_approach")
    factors, activities = payload.get("factors"), payload.get("activities")
    if not isinstance(factors, list) or not factors:
        raise ValueError("factors must be a non-empty array")
    if not isinstance(activities, list) or not activities:
        raise ValueError("activities must be a non-empty array")
    registry = {}
    for factor in factors:
        if not isinstance(factor, dict):
            raise ValueError("Each factor must be an object")
        key = (_text(factor.get("factor_id"), "factor.factor_id"),
               _text(factor.get("version"), "factor.version"))
        if key in registry:
            raise ValueError(f"Duplicate factor identity: {key}")
        value = _number(factor.get("value"), "factor.value")
        unit = _text(factor.get("activity_unit"), "factor.activity_unit")
        if unit not in _UNITS:
            raise ValueError(f"Unsupported factor activity_unit: {unit}")
        output = _text(factor.get("output_unit"), "factor.output_unit")
        if output not in _OUTPUTS:
            raise ValueError(f"Unsupported factor output_unit: {output}")
        valid_from = _date(factor.get("valid_from"), "factor.valid_from")
        valid_to = _date(factor.get("valid_to"), "factor.valid_to")
        if valid_to < valid_from:
            raise ValueError("factor.valid_to precedes factor.valid_from")
        _source(factor.get("source"), "factor.source")
        registry[key] = (factor, value, valid_from, valid_to)
    buckets = ("scope1_kgco2e", "scope2_location_based_kgco2e",
               "scope2_market_based_kgco2e", "scope3_kgco2e", "biogenic_co2_kg")
    totals = {key: Decimal(0) for key in buckets}
    counts = {key: 0 for key in buckets}
    facilities, categories, results, seen = {}, {}, [], set()
    with localcontext() as context:
        context.prec = 50
        for activity in activities:
            if not isinstance(activity, dict):
                raise ValueError("Each activity must be an object")
            activity_id = _text(activity.get("activity_id"), "activity.activity_id")
            if activity_id in seen:
                raise ValueError(f"Duplicate activity_id: {activity_id}")
            seen.add(activity_id)
            entity = _text(activity.get("entity_id"), "activity.entity_id")
            facility = _text(activity.get("facility_id"), "activity.facility_id")
            observed = _date(activity.get("date"), "activity.date")
            if not period_start <= observed <= period_end:
                raise ValueError(f"Activity {activity_id} is outside the inventory period")
            factor_key = (_text(activity.get("factor_id"), "activity.factor_id"),
                          _text(activity.get("factor_version"), "activity.factor_version"))
            if factor_key not in registry:
                raise ValueError(f"Missing exact factor identity: {factor_key}")
            factor, factor_value, valid_from, valid_to = registry[factor_key]
            if not valid_from <= observed <= valid_to:
                raise ValueError(f"Factor is not valid on activity date: {activity_id}")
            quantity = _number(activity.get("quantity"), "activity.quantity")
            evidence = activity.get("evidence", [])
            if not isinstance(evidence, list):
                raise ValueError("activity.evidence must be an array")
            for reference in evidence:
                if not isinstance(reference, dict):
                    raise ValueError("activity evidence references must be objects")
                for field in ("source_id", "version", "pinpoint"):
                    _text(reference.get(field), f"activity.evidence.{field}")
            unit = _text(activity.get("unit"), "activity.unit")
            unit_numerator, unit_denominator = _unit_scales(unit, factor["activity_unit"])
            fraction = Decimal(1)
            if approach == "equity_share":
                fraction = _number(activity.get("equity_fraction"), "activity.equity_fraction")
                if fraction > 1:
                    raise ValueError("equity_fraction must be between 0 and 1")
            elif "equity_fraction" in activity:
                raise ValueError("equity_fraction requires equity_share consolidation")
            output_kind, output_scale = _OUTPUTS[factor["output_unit"]]
            bucket = _bucket(activity, output_kind)
            # Divide last, so e.g. 1 MJ x 3.6 kgCO2e/kWh is exactly 1 kgCO2e.
            amount = quantity * factor_value * Decimal(output_scale) * fraction * unit_numerator / unit_denominator
            totals[bucket] += amount
            counts[bucket] += 1
            facility_key = (entity, facility)
            if facility_key not in facilities:
                facilities[facility_key] = {key: Decimal(0) for key in buckets}
            facilities[facility_key][bucket] += amount
            if bucket == "scope3_kgco2e":
                category = str(activity["scope3_category"])
                categories[category] = categories.get(category, Decimal(0)) + amount
            results.append({
                "activity_id": activity_id, "entity_id": entity, "facility_id": facility,
                "bucket": bucket, "amount": _decimal_text(amount),
                "output_unit": "kgCO2" if output_kind == "CO2" else "kgCO2e",
                "normalised_activity_quantity": _decimal_text(quantity * unit_numerator / unit_denominator),
                "normalised_activity_unit": factor["activity_unit"],
                "equity_fraction_applied": _decimal_text(fraction),
                "activity": deepcopy(activity), "factor": deepcopy(factor),
                "evidence_status": "references_supplied_unverified" if evidence else "not_supplied",
                "review_status": "unreviewed",
            })
    # Validate the retained JSON contract; Decimal objects are accepted for
    # arithmetic but normalised to strings before serialisation.
    input_hash = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()
    output = {
        "schema_version": "regnav.esg.inventory.v1", "inventory_id": inventory_id,
        "period_start": period_start.isoformat(), "period_end": period_end.isoformat(),
        "reporting_boundary": deepcopy(boundary), "input_sha256": input_hash,
        "activities": results,
        "totals": {key: _decimal_text(value) for key, value in totals.items()},
        "activity_counts_by_bucket": counts,
        "activities_without_evidence": sum(item["evidence_status"] == "not_supplied" for item in results),
        "calculation_precision_digits": 50,
        "scope3_categories_kgco2e": {key: _decimal_text(value) for key, value in sorted(categories.items(), key=lambda item: int(item[0]))},
        "facilities": [{"entity_id": key[0], "facility_id": key[1],
                        "totals": {name: _decimal_text(value) for name, value in values.items()}}
                       for key, values in sorted(facilities.items())],
        "review_status": "unreviewed",
        "limitations": ["Factors, activity records, allocation and boundaries are supplied, not independently verified.",
                        "Scope 2 location-based and market-based totals are alternatives and are not added together.",
                        "Biogenic CO2 is reported separately; other biogenic gases must be supplied as CO2e scope records.",
                        "This calculation does not establish completeness or compliance with a reporting standard."],
    }
    return _json_safe(output)


def _unsupported(obj):
    raise ValueError(f"Input contains non-JSON value: {type(obj).__name__}")
