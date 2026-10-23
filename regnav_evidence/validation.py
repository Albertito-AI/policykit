"""Validate recorded metadata, without asserting the truth of any proposition."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlsplit


SCHEMA_VERSION = "1.0"
NOTICE = (
    "Structural checks only. Review status is a user-declared human assessment; "
    "this software does not verify sources, quotations, legal validity or factual truth."
)
SOURCE_TYPES = {
    "legislation", "case", "regulation", "guidance", "article", "book", "dataset", "other"
}
REVIEW_STATUSES = {"unreviewed", "checked", "contested"}
RELATIONS = {"supports", "qualifies", "contradicts", "context"}
IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9._-]{0,79}\Z")
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")


class LedgerReadError(ValueError):
    """An input file cannot be decoded as an unambiguous JSON ledger."""


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str


@dataclass
class ValidationResult:
    findings: list[Finding]

    @property
    def errors(self) -> list[Finding]:
        return [item for item in self.findings if item.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [item for item in self.findings if item.severity == "warning"]

    @property
    def structurally_valid(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "structurally_valid": self.structurally_valid,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "findings": [asdict(item) for item in self.findings],
            "notice": NOTICE,
        }


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise LedgerReadError(f"Duplicate JSON key {key!r}; no value was silently replaced.")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise LedgerReadError(f"{value} is not a valid JSON value.")


def load_ledger(path: str | Path) -> Any:
    """Read UTF-8 JSON, rejecting duplicate keys and nonstandard NaN/Infinity."""
    try:
        with Path(path).open("r", encoding="utf-8-sig") as handle:
            return json.load(
                handle, object_pairs_hook=_unique_object, parse_constant=_reject_constant
            )
    except json.JSONDecodeError as exc:
        raise LedgerReadError(
            f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}."
        ) from exc
    except (OSError, UnicodeError, RecursionError) as exc:
        raise LedgerReadError(f"Cannot read ledger: {exc}.") from exc


def validate(ledger: Any) -> ValidationResult:
    findings: list[Finding] = []

    def add(severity: str, code: str, path: str, message: str) -> None:
        findings.append(Finding(severity, code, path, message))

    def obj(value: Any, path: str, allowed: set[str], required: set[str]) -> bool:
        if not isinstance(value, dict):
            add("error", "OBJECT_REQUIRED", path, "Expected a JSON object.")
            return False
        for key in sorted(required - value.keys()):
            add("error", "MISSING_FIELD", f"{path}.{key}", "Required field is missing.")
        for key in sorted(value.keys() - allowed):
            add("error", "UNKNOWN_FIELD", f"{path}[{json.dumps(key, ensure_ascii=True)}]", "Field is not in schema 1.0.")
        return True

    def text(value: Any, path: str, *, empty_ok: bool = False) -> bool:
        if not isinstance(value, str) or (not empty_ok and not value.strip()):
            add("error", "TEXT_REQUIRED", path, "Expected a non-empty string." if not empty_ok else "Expected a string.")
            return False
        if any((ord(char) < 32 and char not in "\t\r\n") or 0xD800 <= ord(char) <= 0xDFFF for char in value):
            add("error", "CONTROL_CHARACTER", path, "Text contains an unsupported control character or an unpaired Unicode surrogate.")
            return False
        return True

    def dated(value: Any, path: str) -> bool:
        if not isinstance(value, str) or not ISO_DATE.fullmatch(value):
            add("error", "INVALID_DATE", path, "Use an actual calendar date in YYYY-MM-DD form.")
            return False
        try:
            date.fromisoformat(value)
        except ValueError:
            add("error", "INVALID_DATE", path, "Use an actual calendar date in YYYY-MM-DD form.")
            return False
        return True

    def choice(value: Any, path: str, choices: set[str]) -> bool:
        if not isinstance(value, str) or value not in choices:
            add("error", "INVALID_CHOICE", path, f"Expected one of: {', '.join(sorted(choices))}.")
            return False
        return True

    def identifier(value: Any, path: str, known: set[str]) -> bool:
        if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
            add("error", "INVALID_ID", path, "Use 1-80 ASCII letters, digits, dots, hyphens or underscores, starting with a letter.")
            return False
        if value in known:
            add("error", "DUPLICATE_ID", path, f"Identifier {value!r} is already used in this ledger.")
            return False
        known.add(value)
        return True

    root_fields = {"schema_version", "title", "description", "sources", "claims"}
    if not obj(ledger, "$", root_fields, root_fields - {"description"}):
        return ValidationResult(findings)
    if ledger.get("schema_version") != SCHEMA_VERSION:
        add("error", "SCHEMA_VERSION", "$.schema_version", 'Only schema_version "1.0" is supported.')
    text(ledger.get("title"), "$.title")
    if "description" in ledger:
        text(ledger["description"], "$.description", empty_ok=True)

    sources = ledger.get("sources")
    claims = ledger.get("claims")
    if not isinstance(sources, list):
        add("error", "ARRAY_REQUIRED", "$.sources", "Expected an array of source objects.")
        sources = []
    elif not sources:
        add("warning", "NO_SOURCES", "$.sources", "No sources are recorded.")
    if not isinstance(claims, list):
        add("error", "ARRAY_REQUIRED", "$.claims", "Expected an array of claim objects.")
        claims = []
    elif not claims:
        add("warning", "NO_CLAIMS", "$.claims", "No propositions are recorded.")

    known_ids: set[str] = set()
    source_ids: set[str] = set()
    used_sources: set[str] = set()
    source_fields = {"id", "title", "url", "source_type", "jurisdiction", "version", "as_of", "accessed", "notes"}
    source_required = {"id", "title", "url", "source_type", "jurisdiction"}
    for index, source in enumerate(sources):
        path = f"$.sources[{index}]"
        if not obj(source, path, source_fields, source_required):
            continue
        if identifier(source.get("id"), path + ".id", known_ids):
            source_ids.add(source["id"])
        for key in ("title", "jurisdiction"):
            text(source.get(key), path + "." + key)
        for key in ("version", "notes"):
            if key in source:
                text(source[key], path + "." + key, empty_ok=key == "notes")
        for key in ("as_of", "accessed"):
            if key in source:
                dated(source[key], path + "." + key)
        choice(source.get("source_type"), path + ".source_type", SOURCE_TYPES)
        if not source.get("version") and not source.get("as_of"):
            add("warning", "UNRECORDED_VERSION", path, "Record a source version or an as_of date to identify the material consulted.")
        url = source.get("url")
        if text(url, path + ".url"):
            try:
                parts = urlsplit(url)
                # Reject whitespace, credentials, relative URLs and non-web schemes.
                valid_url = (
                    parts.scheme.lower() in {"https", "http"}
                    and bool(parts.hostname)
                    and parts.username is None
                    and parts.password is None
                    and not any(char.isspace() or ord(char) < 32 for char in url)
                    and "\\" not in url
                )
                _ = parts.port  # Raises on a malformed or out-of-range port.
            except ValueError:
                valid_url = False
            if not valid_url:
                add("error", "INVALID_URL", path + ".url", "Use an absolute HTTP(S) URL without credentials, whitespace or backslashes. URLs are not fetched.")

    claim_fields = {"id", "text", "review_status", "evidence", "review", "notes"}
    review_fields = {"reviewer", "date", "note", "resolution"}
    evidence_fields = {"source_id", "pinpoint", "relation"}
    for index, claim in enumerate(claims):
        path = f"$.claims[{index}]"
        if not obj(claim, path, claim_fields, {"id", "text", "review_status", "evidence"}):
            continue
        identifier(claim.get("id"), path + ".id", known_ids)
        text(claim.get("text"), path + ".text")
        if "notes" in claim:
            text(claim["notes"], path + ".notes", empty_ok=True)
        status = claim.get("review_status")
        choice(status, path + ".review_status", REVIEW_STATUSES)
        if status == "unreviewed":
            add("warning", "UNREVIEWED_CLAIM", path, "No completed human review is declared for this proposition.")
        elif status == "contested":
            add("warning", "CONTESTED_CLAIM", path, "This proposition is recorded as contested; retain the disagreement in any summary.")

        review = claim.get("review")
        if "review" in claim:
            if obj(review, path + ".review", review_fields, {"reviewer", "date"}):
                text(review.get("reviewer"), path + ".review.reviewer")
                dated(review.get("date"), path + ".review.date")
                for key in ("note", "resolution"):
                    if key in review:
                        text(review[key], path + ".review." + key)
            else:
                review = None
        elif status == "checked":
            add("error", "CHECKED_WITHOUT_REVIEW", path + ".review", "A user-declared checked proposition needs the reviewer's name and review date.")

        evidence = claim.get("evidence")
        if not isinstance(evidence, list):
            add("error", "ARRAY_REQUIRED", path + ".evidence", "Expected an array of evidence links.")
            continue
        if not evidence:
            add("error" if status == "checked" else "warning", "NO_EVIDENCE", path + ".evidence", "No source is linked to this proposition.")
        has_contradiction = False
        has_support = False
        seen_links: set[tuple[str, str, str]] = set()
        for evidence_index, item in enumerate(evidence):
            epath = f"{path}.evidence[{evidence_index}]"
            if not obj(item, epath, evidence_fields, evidence_fields):
                continue
            source_id = item.get("source_id")
            if not isinstance(source_id, str) or source_id not in source_ids:
                add("error", "UNKNOWN_SOURCE", epath + ".source_id", "This link does not identify a recorded source.")
            else:
                used_sources.add(source_id)
            pinpoint = item.get("pinpoint")
            if text(pinpoint, epath + ".pinpoint", empty_ok=True) and not pinpoint.strip():
                add("error" if status == "checked" else "warning", "MISSING_PINPOINT", epath + ".pinpoint", "Identify a page, paragraph, provision, section or other reproducible location.")
            relation = item.get("relation")
            choice(relation, epath + ".relation", RELATIONS)
            has_contradiction |= relation == "contradicts"
            has_support |= relation in ("supports", "qualifies")
            if all(isinstance(value, str) for value in (source_id, pinpoint, relation)):
                key = (source_id, pinpoint, relation)
                if key in seen_links:
                    add("warning", "DUPLICATE_LINK", epath, "The same source, pinpoint and relation are already linked to this proposition.")
                seen_links.add(key)
        if status == "checked" and evidence and not has_support:
            add("warning", "NO_SUPPORTING_LINK", path, "The user-declared checked proposition has no source marked as supporting or qualifying it.")
        resolution = review.get("resolution") if isinstance(review, dict) else None
        if status == "checked" and has_contradiction and not resolution:
            add("warning", "UNRESOLVED_CONTRADICTION", path, "Contrary evidence is recorded. Explain its treatment in review.resolution or mark the proposition contested.")

    for source_id in sorted(source_ids - used_sources):
        add("warning", "UNUSED_SOURCE", "$.sources", f"Source {source_id!r} is not linked to any proposition.")
    return ValidationResult(findings)

