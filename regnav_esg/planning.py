"""Build accountable action records from supplied gaps and optional templates."""

from copy import deepcopy
from decimal import Decimal, localcontext
import re

from .accounting import _date, _decimal_text, _json_safe, _number, _text


def _budget(raw):
    if not isinstance(raw, dict):
        raise ValueError("budget must be an object")
    currency = _text(raw.get("currency"), "budget.currency")
    if not re.fullmatch(r"[A-Z]{3}", currency):
        raise ValueError("budget.currency must be a three-letter uppercase code")
    lower = _number(raw.get("min"), "budget.min")
    upper = _number(raw.get("max"), "budget.max")
    if lower > upper:
        raise ValueError("budget.min exceeds budget.max")
    _text(raw.get("basis"), "budget.basis")
    result = deepcopy(raw)
    result.update({"min": _decimal_text(lower), "max": _decimal_text(upper),
                   "status": "supplied_estimate_not_verified"})
    return result, currency, lower, upper


def build_action_plan(payload):
    """Create actions without inventing owners, deadlines, budgets or outcomes.

    Supply plan_id, as_of, gaps and optional templates. Each gap requires gap_id
    and description; its action object may supply title, owner, due_date,
    success_criterion and budget. A template_id resolves an exact template.
    Missing scheduling/acceptance fields produce a draft with explicit gaps.
    """
    if not isinstance(payload, dict):
        raise ValueError("Action-plan input must be an object")
    payload = _json_safe(payload)
    plan_id = _text(payload.get("plan_id"), "plan_id")
    as_of = _date(payload.get("as_of"), "as_of")
    gaps = payload.get("gaps")
    if not isinstance(gaps, list):
        raise ValueError("gaps must be an array")
    templates = payload.get("templates", [])
    if not isinstance(templates, list):
        raise ValueError("templates must be an array")
    registry = {}
    for template in templates:
        if not isinstance(template, dict):
            raise ValueError("Each template must be an object")
        identity = _text(template.get("template_id"), "template.template_id")
        if identity in registry:
            raise ValueError(f"Duplicate template_id: {identity}")
        action = template.get("action")
        if not isinstance(action, dict):
            raise ValueError("template.action must be an object")
        registry[identity] = template
    results, skipped, seen, action_ids, totals = [], [], set(), set(), {}
    for gap in gaps:
        if not isinstance(gap, dict):
            raise ValueError("Each gap must be an object")
        gap_id = _text(gap.get("gap_id"), "gap.gap_id")
        description = _text(gap.get("description"), "gap.description")
        if gap_id in seen:
            raise ValueError(f"Duplicate gap_id: {gap_id}")
        seen.add(gap_id)
        gap_status = gap.get("status", "open")
        if gap_status not in ("open", "closed", "deferred"):
            raise ValueError("gap.status must be open, closed or deferred")
        if gap_status != "open":
            skipped.append({"gap_id": gap_id, "status": gap_status, "source_gap": deepcopy(gap)})
            continue
        action = {}
        template_id = gap.get("template_id")
        if template_id is not None:
            _text(template_id, "gap.template_id")
            if template_id not in registry:
                raise ValueError(f"Unknown template_id: {template_id}")
            template = registry[template_id]
            if template.get("gap_code") is not None and template["gap_code"] != gap.get("code"):
                raise ValueError("Template gap_code does not match the gap")
            action = deepcopy(template["action"])
        override = gap.get("action", {})
        if not isinstance(override, dict):
            raise ValueError("gap.action must be an object")
        action.update(deepcopy(override))
        action_id = action.get("action_id", "action-" + gap_id)
        _text(action_id, "action.action_id")
        if action_id in action_ids:
            raise ValueError(f"Duplicate action_id: {action_id}")
        action_ids.add(action_id)
        title = action.get("title", "Resolve gap: " + description)
        _text(title, "action.title")
        missing = []
        for field in ("owner", "due_date", "success_criterion"):
            if action.get(field) is None or action.get(field) == "":
                missing.append(field)
            else:
                _text(action[field], f"action.{field}")
        deadline = None
        if "due_date" not in missing:
            deadline = _date(action["due_date"], "action.due_date")
        budget = None
        if action.get("budget") is not None:
            budget, currency, lower, upper = _budget(action["budget"])
            with localcontext() as context:
                context.prec = 50
                if currency not in totals:
                    totals[currency] = [Decimal(0), Decimal(0)]
                totals[currency][0] += lower
                totals[currency][1] += upper
        priority = gap.get("priority", "unspecified")
        if priority not in ("critical", "high", "medium", "low", "unspecified"):
            raise ValueError("Unknown gap.priority")
        results.append({
            "action_id": action_id, "gap_id": gap_id, "title": title,
            "owner": action.get("owner") or None, "due_date": deadline.isoformat() if deadline else None,
            "success_criterion": action.get("success_criterion") or None,
            "status": "draft_missing_fields" if missing else "proposed",
            "missing_fields": missing, "overdue": deadline < as_of if deadline else None,
            "priority": priority, "budget": budget, "template_id": template_id,
            "template_snapshot": deepcopy(registry[template_id]) if template_id else None,
            "source_gap": deepcopy(gap), "review_status": "unreviewed",
        })
    return {
        "schema_version": "regnav.esg.action_plan.v1", "plan_id": plan_id,
        "as_of": as_of.isoformat(), "actions": results, "skipped_gaps": skipped,
        "budget_totals": [{"currency": currency, "min": _decimal_text(values[0]),
                           "max": _decimal_text(values[1])} for currency, values in sorted(totals.items())],
        "budget_coverage": {"actions_with_supplied_budget": sum(item["budget"] is not None for item in results),
                            "total_actions": len(results),
                            "complete": all(item["budget"] is not None for item in results)},
        "review_status": "unreviewed",
        "limitations": ["Actions derive from supplied gaps and templates; scheduling and budget fields are never invented.",
                        "Budgets are supplied estimates and are aggregated separately by currency without conversion.",
                        "Proposed and overdue actions are not evidence of a legal breach, completion or achieved impact."],
    }
