"""Compare two valid ledger snapshots without modifying human-review declarations."""

from __future__ import annotations

from collections import Counter
from typing import Any


# Metadata changes do not imply that the legal proposition or source text changed.
SOURCE_MATERIAL = ("title", "url", "source_type", "jurisdiction", "version", "as_of", "notes")


def _links(claim: dict[str, Any]) -> Counter[tuple[str, str, str]]:
    """Keep duplicates significant but ignore evidence-link display order."""
    return Counter(
        (item["source_id"], item["pinpoint"], item["relation"])
        for item in claim["evidence"]
    )


def compare_ledgers(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    """Describe source and claim changes; never infer that review took place.

    Inputs must first pass structural validation against the existing schema.
    Identifiers are compared literally. A rename appears as removal and addition.
    """
    old_sources = {item["id"]: item for item in before["sources"]}
    new_sources = {item["id"]: item for item in after["sources"]}
    ledger_fields = sorted(key for key in ("title", "description")
                           if before.get(key) != after.get(key))
    source_changes: list[dict[str, Any]] = []
    material_source_ids: set[str] = set()
    for source_id in sorted(old_sources.keys() | new_sources.keys()):
        previous, current = old_sources.get(source_id), new_sources.get(source_id)
        if previous is None:
            category, fields = "added", []
        elif current is None:
            category, fields = "removed", []
        else:
            fields = sorted(key for key in previous.keys() | current.keys()
                            if previous.get(key) != current.get(key))
            if not fields:
                continue
            category = "material" if set(fields) & set(SOURCE_MATERIAL) else "metadata_only"
        if category != "metadata_only":
            material_source_ids.add(source_id)
        source_changes.append({"id": source_id, "change": category, "fields": fields})

    old_claims = {item["id"]: item for item in before["claims"]}
    new_claims = {item["id"]: item for item in after["claims"]}
    claim_changes: list[dict[str, Any]] = []
    for claim_id in sorted(old_claims.keys() | new_claims.keys()):
        previous, current = old_claims.get(claim_id), new_claims.get(claim_id)
        if previous is None or current is None:
            claim_changes.append({
                "id": claim_id,
                "change": "added" if previous is None else "removed",
                "recheck_prior_review": False,
                "reasons": ["New proposition" if previous is None else "Proposition removed"],
            })
            continue
        changed_text = previous["text"] != current["text"]
        changed_links = _links(previous) != _links(current)
        relevant_sources = {link["source_id"] for link in previous["evidence"] + current["evidence"]}
        changed_sources = sorted(relevant_sources & material_source_ids)
        review_changed = (previous["review_status"] != current["review_status"]
                          or previous.get("review") != current.get("review"))
        notes_changed = previous.get("notes") != current.get("notes")
        material = changed_text or changed_links or notes_changed or bool(changed_sources)
        if not (material or review_changed or notes_changed):
            continue
        reasons = []
        if changed_text:
            reasons.append("Proposition text changed")
        if changed_links:
            reasons.append("Evidence links changed")
        if changed_sources:
            reasons.append("Linked source changed: " + ", ".join(changed_sources))
        if review_changed:
            reasons.append("Review declaration changed")
        if notes_changed:
            reasons.append("Notes changed")
        prior_review = previous["review_status"] in ("checked", "contested")
        claim_changes.append({
            "id": claim_id,
            "change": ("material" if material else
                       "review_declaration_only" if review_changed else "metadata_only"),
            "recheck_prior_review": bool(material and prior_review),
            "reasons": reasons,
        })

    rechecks = [item["id"] for item in claim_changes if item["recheck_prior_review"]]
    return {
        "notice": (
            "Comparison of recorded data only. A recheck flag identifies a potentially stale "
            "previous declaration; it does not revoke, perform or certify human review."
        ),
        "summary": {
            "changed_ledger_fields": len(ledger_fields),
            "changed_sources": len(source_changes),
            "changed_claims": len(claim_changes),
            "prior_reviews_to_reconsider": len(rechecks),
        },
        "ledger_fields": ledger_fields,
        "sources": source_changes,
        "claims": claim_changes,
    }


def text_report(result: dict[str, Any]) -> str:
    """Render a deterministic, readable comparison for the command line."""
    lines = [result["notice"], "", "Ledger metadata: " +
             (", ".join(result["ledger_fields"]) if result["ledger_fields"] else "unchanged"),
             "Source changes:"]
    if not result["sources"]:
        lines.append("  None")
    for source in result["sources"]:
        fields = f" ({', '.join(source['fields'])})" if source["fields"] else ""
        lines.append(f"  {source['id']}: {source['change']}{fields}")
    lines.append("Claim changes:")
    if not result["claims"]:
        lines.append("  None")
    for claim in result["claims"]:
        suffix = " [RECONSIDER PRIOR REVIEW]" if claim["recheck_prior_review"] else ""
        lines.append(f"  {claim['id']}: {claim['change']}{suffix}")
        lines.extend(f"    {reason}" for reason in claim["reasons"])
    summary = result["summary"]
    lines.append(f"Compared: {summary['changed_sources']} source change(s), "
                 f"{summary['changed_claims']} claim change(s), "
                 f"{summary['prior_reviews_to_reconsider']} prior review(s) to reconsider.")
    return "\n".join(lines) + "\n"
