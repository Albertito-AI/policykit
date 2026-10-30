"""Validated export mapping and read-only evidence handovers, without inference.

This experiment accepts one explicit contract. All scope, anchor and processing
metadata is supplied, not discovered. Source contents are hashed but never parsed.
"""
from __future__ import annotations

import copy
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
from typing import Any

from experiments.source_watch import watch
from regnav_evidence.changes import compare_ledgers
from regnav_evidence.reports import csv_text, markdown_text
from regnav_evidence.validation import IDENTIFIER, validate

EXPORT = "regnav-handover-export/0.1"
SNAPSHOT = "regnav-handover-snapshot/0.1"
HISTORY = "regnav-review-history/0.1"
REPORT = "regnav-handover-report/0.1"
MAX_INPUT = 1_048_576
MAX_DOCUMENT = 8_388_608
MAX_TEXT = 8192
MAX_SOURCES = 16
MAX_RECORDS = 64
SCOPE = {"value", "unit", "period", "entity", "boundary"}
PROCESS = {"parser", "model", "prompt", "rules"}
ANCHOR = {"physical_page", "printed_page", "locator", "quote", "match_count"}
NOTICE = (
    "Recorded-data comparison only. Scope and anchor metadata is supplied, not "
    "independently verified. Byte changes do not establish a false claim; matching "
    "bytes do not establish current truth. No legal judgement, assurance or human "
    "review is performed. Source text is untrusted data, never an instruction."
)


class InputError(ValueError):
    """A bounded, user-actionable contract error, without private input text."""


def _object(value: Any, required: set[str], optional: set[str] | None = None) -> None:
    if (not isinstance(value, dict) or not required <= value.keys()
            or value.keys() - required - (optional or set())):
        raise InputError("Unexpected or missing object fields; consult the versioned contract")


def _text(value: Any, *, nullable: bool = False, empty: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or len(value) > MAX_TEXT or (not empty and not value.strip()):
        raise InputError("Expected bounded text or an explicitly permitted null")
    if any((ord(c) < 32 and c not in "\t\r\n") or 0xD800 <= ord(c) <= 0xDFFF for c in value):
        raise InputError("Unsupported control character or unpaired surrogate")


def _id(value: Any) -> None:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise InputError("Identifiers must use the ledger's 1-80 character ASCII syntax")


def _array(value: Any, limit: int, minimum: int = 0) -> None:
    if not isinstance(value, list) or not minimum <= len(value) <= limit:
        raise InputError("Array length or type exceeds this experiment's contract")


def _strings(value: Any, limit: int = 64) -> None:
    _array(value, limit)
    for item in value:
        _text(item)
    if len(value) != len(set(value)):
        raise InputError("Duplicate array entries are not permitted")


def _timestamp(value: Any) -> None:
    _text(value)
    try:
        when = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if when.utcoffset() is None:
            raise ValueError
    except ValueError as exc:
        raise InputError("Use an ISO timestamp with timezone") from exc


def _json_bounds(data: Any, limit: int = MAX_DOCUMENT) -> None:
    pending = [(data, 0)]
    while pending:
        value, depth = pending.pop()
        if depth > 24:
            raise InputError("JSON nesting exceeds 24 levels")
        if isinstance(value, dict):
            if any(not isinstance(k, str) for k in value):
                raise InputError("JSON object keys must be strings")
            pending.extend((v, depth + 1) for v in value.values())
        elif isinstance(value, list):
            pending.extend((v, depth + 1) for v in value)
        elif isinstance(value, str):
            _text(value, empty=True)
        elif value is not None and type(value) not in (bool, int):
            raise InputError("Use exact text for values; floating-point values are unsupported")
    if len(_canonical(data)) > limit:
        raise InputError("JSON exceeds the documented size limit")


def _canonical(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("utf-8")


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InputError("Duplicate JSON key; input was not merged")
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise InputError("Non-standard JSON number")


def load(path: str | Path, limit: int = MAX_DOCUMENT) -> Any:
    with Path(path).open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise InputError("JSON file exceeds the size limit")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique,
                           parse_constant=_constant)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise InputError("Invalid, ambiguous or excessive UTF-8 JSON") from exc
    _json_bounds(value, limit)
    return value


def dumps(value: Any) -> str:
    _json_bounds(value)
    return json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n"


def write_new(path: str | Path, text: str) -> None:
    """Exclusive creation: never overwrite inputs, earlier versions or symlinks."""
    raw = text.encode("utf-8")
    if len(raw) > MAX_DOCUMENT:
        raise InputError("Output exceeds 8 MiB")
    with Path(path).open("xb") as stream:
        stream.write(raw)


def map_export(data: Any) -> dict[str, Any]:
    """Validate this export and return schema-1.0 records, all unreviewed.

    The complete original export is the versioned sidecar in a snapshot. Nothing
    is silently inserted into the original ledger's strict schema.
    """
    _json_bounds(data, MAX_INPUT)
    _object(data, {"schema_version", "title", "sources", "records", "process", "inventory"})
    if data["schema_version"] != EXPORT:
        raise InputError("Unsupported export schema version")
    _text(data["title"])
    _array(data["sources"], MAX_SOURCES, 1)
    _array(data["records"], MAX_RECORDS, 1)
    sources, claims, paths = [], [], set()
    source_fields = {"id", "title", "url", "source_type", "jurisdiction", "path"}
    for source in data["sources"]:
        _object(source, source_fields, {"version", "as_of", "accessed", "notes"})
        _id(source["id"])
        if source["path"] is not None:
            try:
                watch._path(source["path"])
            except ValueError as exc:
                raise InputError("Source path must be a safe relative POSIX path") from exc
            if source["path"] in paths:
                raise InputError("Two source IDs must not silently share a local path")
            paths.add(source["path"])
        sources.append({k: copy.deepcopy(v) for k, v in source.items() if k != "path"})
    source_ids = {s.get("id") for s in sources if isinstance(s.get("id"), str)}
    for record in data["records"]:
        _object(record, {"id", "text", "evidence", "scope", "assurance"})
        _id(record["id"])
        _text(record["text"])
        _array(record["evidence"], 32)
        links = []
        for link in record["evidence"]:
            _object(link, {"source_id", "pinpoint", "relation", "anchor"})
            _id(link["source_id"])
            _text(link["pinpoint"], empty=True)
            _text(link["relation"])
            anchor = link["anchor"]
            if anchor is not None:
                _object(anchor, ANCHOR)
                for field in ("physical_page", "match_count"):
                    value = anchor[field]
                    lower = 1 if field == "physical_page" else 0
                    if value is not None and (type(value) is not int or not lower <= value <= 1_000_000):
                        raise InputError("Invalid physical page or supplied match count")
                for field in ("printed_page", "locator", "quote"):
                    _text(anchor[field], nullable=True)
            links.append({k: copy.deepcopy(v) for k, v in link.items() if k != "anchor"})
        scope = record["scope"]
        if scope is not None:
            _object(scope, SCOPE)
            for value in scope.values():
                _text(value, nullable=True)
        assurance = record["assurance"]
        if assurance is not None:
            _object(assurance, {"status", "statement_source_id", "declared_coverage",
                               "asserted_coverage", "level", "period"})
            if assurance["status"] not in ("reported", "not_located"):
                raise InputError("Assurance status must be reported or not_located")
            _strings(assurance["declared_coverage"])
            _strings(assurance["asserted_coverage"])
            for field in ("level", "period"):
                _text(assurance[field], nullable=True)
            sid = assurance["statement_source_id"]
            if assurance["status"] == "reported":
                if not isinstance(sid, str) or sid not in source_ids or sid not in {x["source_id"] for x in links}:
                    raise InputError("Reported assurance must reference an explicitly linked recorded source")
            elif sid is not None or assurance["declared_coverage"] or assurance["level"] is not None or assurance["period"] is not None:
                raise InputError("Not-located assurance cannot contain invented statement attributes")
        claims.append({"id": record["id"], "text": record["text"],
                       "evidence": links, "review_status": "unreviewed"})
    process = data["process"]
    if process is not None:
        _object(process, PROCESS)
        for value in process.values():
            _text(value, nullable=True)
    inventory = data["inventory"]
    if inventory is not None:
        _strings(inventory, 128)
        for item in inventory:
            try:
                watch._path(item)
            except ValueError as exc:
                raise InputError("Inventory contains an unsafe relative path") from exc
        if not paths <= set(inventory):
            raise InputError("The supplied inventory omits a configured source path")
    ledger = {"schema_version": "1.0", "title": data["title"], "sources": sources, "claims": claims}
    checked = validate(ledger)
    if checked.errors:
        first = checked.errors[0]
        raise InputError("Mapped ledger rejected: " + first.code)
    return ledger


def _mapping(data: dict[str, Any]) -> dict[str, list[str]]:
    result = {s["id"]: set() for s in data["sources"]}
    for record in data["records"]:
        for link in record["evidence"]:
            result[link["source_id"]].add(record["id"])
    return {key: sorted(value) for key, value in result.items()}


def _observe(source: dict[str, Any], claim_ids: list[str], root: Path) -> dict[str, Any]:
    row = {"id": source["id"], "path": source["path"], "claim_ids": claim_ids,
           "status": "NOT_CONFIGURED", "sha256": None}
    if source["path"] is None:
        return row
    # Hashing an unmapped source does not discover which claim it might affect.
    try:
        row["sha256"] = watch._digest(root, source["path"])
        row["status"] = "OBSERVED"
    except (OSError, ValueError, RuntimeError):
        row["status"] = "NOT_OBSERVED"
    return row


def _snapshot(data: dict[str, Any], observations: list[dict[str, Any]]) -> dict[str, Any]:
    ledger = map_export(data)
    content = {"schema_version": SNAPSHOT, "export": copy.deepcopy(data), "ledger": ledger,
               "source_observations": copy.deepcopy(sorted(observations, key=lambda r: r["id"]))}
    # Content identity excludes the observation time; it does not certify authorship.
    content["snapshot_id"] = hashlib.sha256(_canonical(content)).hexdigest()
    content["observed_at"] = datetime.now(timezone.utc).isoformat()
    _json_bounds(content)
    return content


def snapshot(data: Any, root: str | Path) -> dict[str, Any]:
    map_export(data)
    directory = Path(root).resolve(strict=True)
    if not directory.is_dir():
        raise InputError("Root must be a directory")
    mapping = _mapping(data)
    return _snapshot(data, [_observe(s, mapping[s["id"]], directory) for s in data["sources"]])


def validate_snapshot(data: Any) -> None:
    _json_bounds(data)
    _object(data, {"schema_version", "export", "ledger", "source_observations", "snapshot_id", "observed_at"})
    if data["schema_version"] != SNAPSHOT:
        raise InputError("Unsupported snapshot schema")
    ledger = map_export(data["export"])
    if data["ledger"] != ledger:
        raise InputError("Snapshot ledger differs from its explicit export mapping")
    _timestamp(data["observed_at"])
    _array(data["source_observations"], MAX_SOURCES, 1)
    mapping = _mapping(data["export"])
    expected = {s["id"]: s for s in data["export"]["sources"]}
    seen = set()
    for row in data["source_observations"]:
        _object(row, {"id", "path", "claim_ids", "status", "sha256"})
        _id(row["id"])
        if row["id"] in seen or row["id"] not in expected:
            raise InputError("Snapshot source identity is inconsistent")
        seen.add(row["id"])
        if row["path"] != expected[row["id"]]["path"] or row["claim_ids"] != mapping[row["id"]]:
            raise InputError("Snapshot source path or claim mapping is inconsistent")
        if row["status"] not in ("OBSERVED", "NOT_OBSERVED", "NOT_CONFIGURED"):
            raise InputError("Unexpected source observation")
        if (row["status"] == "NOT_CONFIGURED") != (row["path"] is None):
            raise InputError("Source path and observation disagree")
        if row["status"] == "OBSERVED":
            if not isinstance(row["sha256"], str) or not watch.HASH.fullmatch(row["sha256"]):
                raise InputError("Observed source requires its SHA-256 digest")
        elif row["sha256"] is not None:
            raise InputError("Unobserved source cannot carry an observed digest")
    if seen != set(expected):
        raise InputError("Snapshot does not preserve every supplied source")
    content = {k: v for k, v in data.items() if k not in ("snapshot_id", "observed_at")}
    if data["snapshot_id"] != hashlib.sha256(_canonical(content)).hexdigest():
        raise InputError("Snapshot content-identity check failed")


def watch_baseline(data: dict[str, Any]) -> dict[str, Any] | None:
    """Build only the previously observed and explicitly linked watch subset."""
    validate_snapshot(data)
    rows = [{k: copy.deepcopy(row[k]) for k in ("id", "path", "claim_ids", "sha256")}
            for row in data["source_observations"] if row["status"] == "OBSERVED" and row["claim_ids"]]
    return {"schema": watch.SCHEMA, "observed_at": data["observed_at"], "files": rows} if rows else None


def validate_history(data: Any) -> None:
    _json_bounds(data)
    _object(data, {"schema_version", "entries"})
    if data["schema_version"] != HISTORY:
        raise InputError("Unsupported review-history schema")
    _array(data["entries"], 256)
    seen = {}
    for entry in data["entries"]:
        _object(entry, {"id", "snapshot_id", "claim_id", "actor_type", "actor_name", "decision",
                        "recorded_at", "rationale", "reopen_when", "supersedes"})
        _id(entry["id"])
        _id(entry["claim_id"])
        if entry["id"] in seen:
            raise InputError("Duplicate review entry; history is append-only")
        if not isinstance(entry["snapshot_id"], str) or not watch.HASH.fullmatch(entry["snapshot_id"]):
            raise InputError("Review must identify a content snapshot")
        for field in ("actor_name", "rationale", "reopen_when"):
            _text(entry[field])
        _timestamp(entry["recorded_at"])
        if entry["actor_type"] not in ("human_declaration", "ai_suggestion", "fictional_training"):
            raise InputError("Review actor type must be explicit")
        if entry["decision"] not in ("accepted", "contested", "needs_review", "suggested"):
            raise InputError("Unknown review decision")
        if entry["actor_type"] == "ai_suggestion" and entry["decision"] not in ("suggested", "needs_review"):
            raise InputError("AI suggestions cannot declare completed human review")
        prior = entry["supersedes"]
        if prior is not None:
            _id(prior)
            if prior not in seen or seen[prior]["claim_id"] != entry["claim_id"]:
                raise InputError("Supersession must reference an earlier entry for the same claim")
            if entry["actor_type"] != seen[prior]["actor_type"]:
                raise InputError("An actor type cannot supersede a different type of declaration")
        seen[entry["id"]] = entry


def append_review(history: Any, entry: Any) -> dict[str, Any]:
    """Return a new validated history; caller must supply every declaration field."""
    validate_history(history)
    revised = copy.deepcopy(history)
    revised["entries"].append(copy.deepcopy(entry))
    validate_history(revised)
    return revised


def compare(before: Any, after_export: Any, root: str | Path,
            history: Any | None = None) -> dict[str, Any]:
    validate_snapshot(before)
    after_ledger = map_export(after_export)
    directory = Path(root).resolve(strict=True)
    if not directory.is_dir():
        raise InputError("Root must be a directory")
    history = {"schema_version": HISTORY, "entries": []} if history is None else history
    validate_history(history)
    baseline = watch_baseline(before)
    raw = watch.check(baseline, directory) if baseline else {
        "schema": watch.SCHEMA, "observation": "NOT_CHECKED", "affected_claim_ids": [],
        "files": [], "limits": "No previously observed linked files; no unchanged finding is possible."}
    raw_by_id = {r["id"]: r for r in raw["files"]}
    mapping = _mapping(after_export)
    observations = []
    for source in after_export["sources"]:
        previous = raw_by_id.get(source["id"])
        if previous is not None and previous["path"] == source["path"]:
            observations.append({"id": source["id"], "path": source["path"],
                                 "claim_ids": mapping[source["id"]],
                                 "status": "OBSERVED" if previous["current_sha256"] is not None else "NOT_OBSERVED",
                                 "sha256": previous["current_sha256"]})
        else:
            observations.append(_observe(source, mapping[source["id"]], directory))
    after = _snapshot(after_export, observations)
    core = compare_ledgers(before["ledger"], after_ledger)
    attention, deltas = [], []

    def flag(claim: str | None, code: str, detail: str) -> None:
        item = {"claim_id": claim, "code": code, "detail": detail}
        if item not in attention:
            attention.append(item)

    oldmap = _mapping(before["export"])
    oldsources = {r["id"]: r for r in before["source_observations"]}
    newsources = {r["id"]: r for r in observations}
    for row in raw["files"]:
        if row["status"] != "UNCHANGED_BYTES":
            for cid in sorted(set(row["claim_ids"]) | set(mapping.get(row["id"], []))):
                flag(cid, row["status"], "Linked source observation: " + row["id"])
    for sid in sorted(oldsources.keys() | newsources.keys()):
        old, new = oldsources.get(sid), newsources.get(sid)
        related = sorted(set(oldmap.get(sid, [])) | set(mapping.get(sid, [])))
        codes = []
        if old is None:
            codes.append("SOURCE_ADDED")
        elif new is None:
            codes.append("SOURCE_REMOVED")
        else:
            if old["path"] != new["path"]:
                codes.append("SOURCE_PATH_CHANGED")
            if old["status"] != "OBSERVED":
                codes.append("BASELINE_NOT_OBSERVED")
            # Source Watch deliberately excludes previously unlinked files.
            # Compare the retained observation when such a file gains a link;
            # this reports byte drift, not a new semantic or legal conclusion.
            if (not oldmap.get(sid) and mapping.get(sid)
                    and old["path"] == new["path"]
                    and old["status"] == "OBSERVED"
                    and new["status"] == "OBSERVED"
                    and old["sha256"] != new["sha256"]):
                codes.append("NEWLY_LINKED_SOURCE_BYTES_CHANGED")
        if new is not None and new["status"] != "OBSERVED":
            codes.append(new["status"])
        if not related:
            flag(None, "UNMAPPED_SOURCE", "No supplied claim links for source: " + sid)
        for code in codes:
            for cid in related or [None]:
                flag(cid, code, "Source: " + sid)
    for row in core["claims"]:
        flag(row["id"], "RECORDED_CLAIM_" + row["change"].upper(), "; ".join(row["reasons"]))
    oldrecords = {r["id"]: r for r in before["export"]["records"]}
    newrecords = {r["id"]: r for r in after_export["records"]}
    for cid in sorted(oldrecords.keys() & newrecords.keys()):
        old, new = oldrecords[cid], newrecords[cid]
        for field in sorted(SCOPE):
            a, b = (old["scope"] or {}).get(field), (new["scope"] or {}).get(field)
            if a != b:
                deltas.append({"claim_id": cid, "field": "scope." + field, "before": a, "after": b})
                flag(cid, "SCOPE_CHANGED", "Explicitly supplied field: " + field)
        if old["assurance"] != new["assurance"]:
            deltas.append({"claim_id": cid, "field": "assurance", "before": old["assurance"], "after": new["assurance"]})
            flag(cid, "ASSURANCE_RECORD_CHANGED", "Supplied statement metadata changed; no assurance opinion is produced.")
        oldanchors = sorted((_canonical(e).decode() for e in old["evidence"]))
        newanchors = sorted((_canonical(e).decode() for e in new["evidence"]))
        if oldanchors != newanchors:
            flag(cid, "EVIDENCE_LOCATION_OR_LINK_CHANGED", "Inspect supplied locations and links; no automatic relocation was attempted.")
    for record in after_export["records"]:
        cid = record["id"]
        missing = [field for field in sorted(SCOPE) if (record["scope"] or {}).get(field) is None]
        if missing:
            flag(cid, "SCOPE_NOT_SUPPLIED", "Missing declared fields: " + ", ".join(missing))
        for link in record["evidence"]:
            anchor = link["anchor"]
            count = anchor["match_count"] if anchor is not None else None
            if count is None:
                flag(cid, "ANCHOR_NOT_EXAMINED", "No match count supplied for " + link["source_id"])
            elif count == 0:
                flag(cid, "ANCHOR_NOT_LOCATED", "Caller reports no matching location in " + link["source_id"])
            elif count > 1:
                flag(cid, "ANCHOR_AMBIGUOUS", "Caller reports multiple matching locations in " + link["source_id"])
        assurance = record["assurance"]
        if assurance is None or assurance["status"] == "not_located":
            flag(cid, "ASSURANCE_NOT_ESTABLISHED", "Statement not supplied or not located in supplied material; no conclusion about the organisation.")
        elif not assurance["declared_coverage"]:
            flag(cid, "ASSURANCE_SCOPE_UNKNOWN", "No explicit coverage supplied; no assurance opinion is produced.")
        elif set(assurance["asserted_coverage"]) - set(assurance["declared_coverage"]):
            flag(cid, "DECLARED_ASSURANCE_SCOPE_MISMATCH", "Asserted coverage exceeds the supplied declared set; competent review is required.")
    process_changes = []
    for field in sorted(PROCESS):
        a = (before["export"]["process"] or {}).get(field)
        b = (after_export["process"] or {}).get(field)
        state = "UNKNOWN" if a is None or b is None else "CHANGED" if a != b else "UNCHANGED_DECLARATION"
        process_changes.append({"field": field, "before": a, "after": b, "observation": state})
        if state in ("UNKNOWN", "CHANGED"):
            flag(None, "PROCESS_" + state, field + ": no causal or semantic conclusion follows.")
    oldinv, newinv = before["export"]["inventory"], after_export["inventory"]
    paths = {s["path"] for s in after_export["sources"] if s["path"] is not None}
    inventory = {"observation": "UNKNOWN" if oldinv is None or newinv is None else "SUPPLIED_LISTS_COMPARED",
                 "added": sorted(set(newinv or []) - set(oldinv or [])) if oldinv is not None and newinv is not None else None,
                 "removed": sorted(set(oldinv or []) - set(newinv or [])) if oldinv is not None and newinv is not None else None,
                 "outside_watch": sorted(set(newinv or []) - paths) if newinv is not None else None,
                 "directory_scanned": False}
    if inventory["observation"] == "UNKNOWN":
        flag(None, "INVENTORY_UNKNOWN", "A complete source inventory has not been established.")
    if inventory["added"] or inventory["removed"]:
        flag(None, "INVENTORY_CHANGED", "Explicit inventory differs; inspect additions and removals.")
    if inventory["outside_watch"]:
        flag(None, "INVENTORY_OUTSIDE_WATCH", "Supplied inventory includes unwatched paths; affected claims cannot be inferred.")
    review_views = []
    superseded = {e["supersedes"] for e in history["entries"] if e["supersedes"] is not None}
    for entry in history["entries"]:
        same = entry["snapshot_id"] == after["snapshot_id"]
        known = entry["snapshot_id"] in (before["snapshot_id"], after["snapshot_id"])
        status = "CURRENT_CONTENT_ID" if same else "DIFFERENT_CONTENT_ID" if known else "SNAPSHOT_NOT_SUPPLIED"
        review_views.append({"entry": copy.deepcopy(entry), "version_match": status,
                             "superseded": entry["id"] in superseded,
                             "identity_authenticated": False,
                             "human_review_verified": False})
        if not same and entry["id"] not in superseded:
            flag(entry["claim_id"], "REVIEW_VERSION_MISMATCH", "Prior declaration retained without renewal: " + entry["id"])
    attention.sort(key=lambda r: (r["claim_id"] or "", r["code"], r["detail"]))
    report = {"schema_version": REPORT, "notice": NOTICE,
              "before_snapshot_id": before["snapshot_id"], "after_snapshot_id": after["snapshot_id"],
              "source_watch": raw, "current_sources": observations, "ledger_comparison": core,
              "field_changes": deltas, "process_observations": process_changes, "inventory": inventory,
              "attention": attention, "review_history": review_views,
              "structural_notices": validate(after_ledger).to_dict(),
              "coverage": {"sources": len(after_export["sources"]), "records": len(after_export["records"]),
                           "source_contents_parsed": False, "anchor_matches_verified": False,
                           "scope_is_supplied_metadata": True, "unlisted_sources_discovered": False},
              "observation": "ATTENTION_REQUIRED" if attention else "NO_RECORDED_DIFFERENCE_OR_SCOPE_ALERT",
              "after_snapshot": after}
    _json_bounds(report)
    return report


def report_markdown(report: dict[str, Any]) -> str:
    """Safe reviewer view. JSON retains all fields, including the original export."""
    lines = ["# Evidence handover", "", NOTICE, "", "Observation: " + report["observation"],
             "", "Before: `" + report["before_snapshot_id"] + "`",
             "After: `" + report["after_snapshot_id"] + "`", "",
             "## Source-byte observations", "", "| Source | Path | Status | Linked claims |",
             "| --- | --- | --- | --- |"]
    for row in report["source_watch"]["files"]:
        lines.append("| " + " | ".join(markdown_text(str(x)) for x in
                     (row["id"], row["path"], row["status"], ", ".join(row["claim_ids"]))) + " |")
    lines += ["", "## Supplied field changes", "", "| Claim | Field | Before | After |", "| --- | --- | --- | --- |"]
    for row in report["field_changes"]:
        cells = [row["claim_id"], row["field"], json.dumps(row["before"], ensure_ascii=True), json.dumps(row["after"], ensure_ascii=True)]
        lines.append("| " + " | ".join(markdown_text(x) for x in cells) + " |")
    lines += ["", "## Review attention", "", "| Claim | Code | Explanation |", "| --- | --- | --- |"]
    for row in report["attention"]:
        lines.append("| " + " | ".join(markdown_text(x) for x in (row["claim_id"] or "Collection", row["code"], row["detail"])) + " |")
    lines += ["", "## Recorded propositions", "", "| ID | Supplied proposition | Import status |", "| --- | --- | --- |"]
    for row in report["after_snapshot"]["ledger"]["claims"]:
        lines.append("| " + " | ".join(markdown_text(row[k]) for k in ("id", "text", "review_status")) + " |")
    lines += ["", "## Declared review history", "", "| Entry | Actor type | Decision | Version |", "| --- | --- | --- | --- |"]
    for row in report["review_history"]:
        entry = row["entry"]
        lines.append("| " + " | ".join(markdown_text(x) for x in (entry["id"], entry["actor_type"], entry["decision"], row["version_match"])) + " |")
    lines += ["", "This table does not authenticate a person or verify a completed review.",
              "Process and inventory details, exact source locations and the full supplied export remain in the JSON report.",
              "All imported claims remain unreviewed. No prior declaration is altered.\n"]
    return "\n".join(lines)


def report_csv(report: dict[str, Any]) -> str:
    """Flat view of propositions and attention; not a lossless round-trip format."""
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n", quoting=csv.QUOTE_ALL)
    writer.writerow(["Claim ID", "Supplied proposition", "Code", "Explanation"])
    claims = {r["id"]: r["text"] for r in report["after_snapshot"]["ledger"]["claims"]}
    rows = list(report["attention"])
    covered = {r["claim_id"] for r in rows}
    rows += [{"claim_id": key, "code": "NO_RECORDED_ALERT", "detail": "No alert in compared fields; not a completed review."}
             for key in sorted(claims.keys() - covered)]
    for row in rows:
        writer.writerow(csv_text(x) for x in (row["claim_id"] or "", claims.get(row["claim_id"], ""), row["code"], row["detail"]))
    return stream.getvalue()
