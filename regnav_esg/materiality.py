"""Explicit materiality screening and exact, caller-supplied standards lookup.

Scores and thresholds are supplied by the operator. A screening result is not
a conclusion that a matter is legally material or that a standard applies.
"""

from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction

from .accounting import _date, _decimal_text, _json_safe, _number, _source, _text


class StandardsRegistry:
    """Resolve exact framework, version and code tuples without fuzzy guessing."""

    def __init__(self, records):
        if not isinstance(records, list):
            raise ValueError("standards must be an array")
        records = _json_safe(records)
        self._records = {}
        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Each standard record must be an object")
            key = tuple(_text(record.get(field), f"standard.{field}")
                        for field in ("framework", "version", "code"))
            _text(record.get("title"), "standard.title")
            _source(record.get("source"), "standard.source")
            if key in self._records:
                raise ValueError(f"Duplicate standard identity: {key}")
            for field in ("effective_from", "effective_to"):
                if field in record:
                    _date(record[field], f"standard.{field}")
            if record.get("effective_from") and record.get("effective_to"):
                if record["effective_to"] < record["effective_from"]:
                    raise ValueError("standard.effective_to precedes effective_from")
            self._records[key] = deepcopy(record)

    def lookup(self, framework, version, code):
        key = tuple(_text(value, field) for value, field in
                    ((framework, "framework"), (version, "version"), (code, "code")))
        if key not in self._records:
            raise ValueError(f"Unknown exact standard reference: {key}")
        result = deepcopy(self._records[key])
        result["source_status"] = "supplied_not_independently_verified"
        return result


def _rubric(raw, perspective):
    if not isinstance(raw, dict):
        raise ValueError(f"rubrics.{perspective} must be an object")
    for name in ("rubric_id", "version", "rationale"):
        _text(raw.get(name), f"rubrics.{perspective}.{name}")
    dimensions = raw.get("dimensions")
    if not isinstance(dimensions, list) or not dimensions:
        raise ValueError("rubric.dimensions must be a non-empty array")
    for dimension in dimensions:
        _text(dimension, "rubric.dimension")
    if len(set(dimensions)) != len(dimensions):
        raise ValueError("Duplicate rubric dimensions")
    minimum = _number(raw.get("scale_min"), "rubric.scale_min")
    maximum = _number(raw.get("scale_max"), "rubric.scale_max")
    threshold = _number(raw.get("threshold"), "rubric.threshold")
    if minimum >= maximum or not minimum <= threshold <= maximum:
        raise ValueError("Rubric scale or threshold is invalid")
    aggregation = raw.get("aggregation")
    if aggregation not in ("weighted_mean", "maximum"):
        raise ValueError("rubric.aggregation must be weighted_mean or maximum")
    weights = {}
    if aggregation == "weighted_mean":
        supplied = raw.get("weights")
        if not isinstance(supplied, dict) or set(supplied) != set(dimensions):
            raise ValueError("rubric.weights must exactly match rubric dimensions")
        for key, value in supplied.items():
            weights[key] = _number(value, f"rubric.weights.{key}")
            if weights[key] == 0:
                raise ValueError("Rubric weights must be positive")
    elif "weights" in raw:
        raise ValueError("maximum aggregation does not use weights")
    return dimensions, minimum, maximum, threshold, aggregation, weights


def _evidence(records):
    if not isinstance(records, list):
        raise ValueError("assessment.evidence must be an array")
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each evidence reference must be an object")
        _text(record.get("source_id"), "evidence.source_id")
        _text(record.get("version"), "evidence.version")
        _text(record.get("pinpoint"), "evidence.pinpoint")
    return deepcopy(records)


def screen_materiality(payload):
    """Screen financial and impact perspectives independently against rubrics.

    Each rubric specifies rubric_id, version, rationale, dimensions, scale_min,
    scale_max, threshold and aggregation; weighted_mean also needs weights.
    Each topic assessment supplies scores, rationale and pinpointed evidence.
    Missing evidence/dimensions yields insufficient_information, never a pass.
    """
    if not isinstance(payload, dict):
        raise ValueError("Materiality input must be an object")
    payload = _json_safe(payload)
    rubrics = payload.get("rubrics")
    topics = payload.get("topics")
    if not isinstance(rubrics, dict) or not rubrics:
        raise ValueError("rubrics must be a non-empty object")
    if set(rubrics) - {"financial", "impact"}:
        raise ValueError("Only financial and impact rubric perspectives are supported")
    parsed_rubrics = {key: _rubric(value, key) for key, value in rubrics.items()}
    if not isinstance(topics, list) or not topics:
        raise ValueError("topics must be a non-empty array")
    registry = StandardsRegistry(payload.get("standards", []))
    results, seen = [], set()
    for topic in topics:
        if not isinstance(topic, dict):
            raise ValueError("Each topic must be an object")
        topic_id = _text(topic.get("topic_id"), "topic.topic_id")
        title = _text(topic.get("title"), "topic.title")
        if topic_id in seen:
            raise ValueError(f"Duplicate topic_id: {topic_id}")
        seen.add(topic_id)
        references = topic.get("standard_refs", [])
        if not isinstance(references, list):
            raise ValueError("topic.standard_refs must be an array")
        citations = []
        for reference in references:
            if not isinstance(reference, dict):
                raise ValueError("Each standard reference must be an object")
            citations.append(registry.lookup(reference.get("framework"), reference.get("version"), reference.get("code")))
        result = {"topic_id": topic_id, "title": title, "standard_citations": citations,
                  "review_status": "unreviewed"}
        for perspective in ("financial", "impact"):
            assessment = topic.get(perspective)
            if perspective not in parsed_rubrics:
                result[perspective] = {"status": "insufficient_information", "reasons": ["rubric_not_supplied"], "score": None}
                continue
            if assessment is None:
                result[perspective] = {"status": "insufficient_information", "reasons": ["assessment_not_supplied"], "score": None}
                continue
            if not isinstance(assessment, dict):
                raise ValueError(f"topic.{perspective} must be an object")
            dimensions, minimum, maximum, threshold, aggregation, weights = parsed_rubrics[perspective]
            scores = assessment.get("scores", {})
            if not isinstance(scores, dict):
                raise ValueError("assessment.scores must be an object")
            if set(scores) - set(dimensions):
                raise ValueError("Assessment contains dimensions outside its rubric")
            values, reasons = {}, []
            for dimension in dimensions:
                if dimension not in scores or scores[dimension] is None:
                    reasons.append(f"missing_score:{dimension}")
                else:
                    values[dimension] = _number(scores[dimension], f"assessment.scores.{dimension}")
                    if not minimum <= values[dimension] <= maximum:
                        raise ValueError(f"Score outside rubric scale: {dimension}")
            rationale = assessment.get("rationale")
            if not isinstance(rationale, str) or not rationale.strip():
                reasons.append("rationale_not_supplied")
            evidence = _evidence(assessment.get("evidence", []))
            if not evidence:
                reasons.append("evidence_not_supplied")
            score, exact_score = None, None
            if not reasons:
                if aggregation == "maximum":
                    exact_score = Fraction(max(values.values()))
                else:
                    exact_score = sum((Fraction(values[key]) * Fraction(weights[key]) for key in dimensions), Fraction(0)) / sum((Fraction(weight) for weight in weights.values()), Fraction(0))
                with localcontext() as context:
                    context.prec = 50
                    score = Decimal(exact_score.numerator) / Decimal(exact_score.denominator)
            result[perspective] = {
                "status": "insufficient_information" if reasons else ("screened_in" if exact_score >= Fraction(threshold) else "screened_out"),
                "score": _decimal_text(score) if score is not None else None,
                "score_display_rounded": Fraction(score) != exact_score if score is not None else None,
                "exact_score_fraction": {"numerator": str(exact_score.numerator), "denominator": str(exact_score.denominator)} if exact_score is not None else None,
                "threshold_decision_basis": "exact rational arithmetic; display uses 50 significant decimal digits",
                "threshold": _decimal_text(threshold), "threshold_operator": ">=",
                "reasons": reasons, "assessment": deepcopy(assessment),
                "rubric": deepcopy(rubrics[perspective]), "evidence": evidence,
            }
        results.append(result)
    return {"schema_version": "regnav.esg.materiality.v1", "topics": results,
            "review_status": "unreviewed",
            "limitations": ["Screening applies caller-supplied scores, evidence, rubrics and thresholds.",
                            "Financial and impact perspectives remain separate; neither overrides the other.",
                            "A screening result is not a legal materiality decision, legal applicability finding or compliance certification.",
                            "Supplied standards citations are resolved exactly, not independently verified."]}
