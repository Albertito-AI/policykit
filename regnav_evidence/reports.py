"""Transparent exports of recorded evidence, with text-safe rendering."""

from __future__ import annotations

import csv
import html
import io
import re
from typing import Any
import unicodedata

from .validation import NOTICE, ValidationResult


COLUMNS = [
    "Claim ID", "Proposition", "User-declared review", "Reviewer", "Review date",
    "Source ID", "Source title", "Source type", "Jurisdiction", "Version", "As of",
    "URL", "Pinpoint", "Relation", "Treatment of contrary evidence",
]


def markdown_text(value: str) -> str:
    """Keep user text inside its table cell and render HTML/Markdown literally."""
    value = html.escape(value, quote=True).replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    return re.sub(r"([\\|`*_~\[\]])", r"\\\1", value)


def csv_text(value: str) -> str:
    """Neutralise common spreadsheet formula prefixes, including hidden prefixes.

    CSV is a spreadsheet-view export. The JSON ledger remains the lossless record.
    """
    offset = 0
    while offset < len(value) and (value[offset].isspace() or unicodedata.category(value[offset]) in {"Cc", "Cf"}):
        offset += 1
    probe = value[offset:]
    if probe.startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r", "\n")):
        return "'" + value
    return value


def evidence_rows(ledger: dict[str, Any]) -> list[list[str]]:
    """Call only after structural validation succeeds."""
    sources = {source["id"]: source for source in ledger["sources"]}
    rows: list[list[str]] = []
    for claim in ledger["claims"]:
        review = claim.get("review") or {}
        for evidence in claim["evidence"] or [{}]:
            source = sources.get(evidence.get("source_id"), {})
            rows.append([
                claim["id"], claim["text"], claim["review_status"],
                review.get("reviewer", ""), review.get("date", ""),
                source.get("id", ""), source.get("title", ""), source.get("source_type", ""),
                source.get("jurisdiction", ""), source.get("version", ""), source.get("as_of", ""),
                source.get("url", ""), evidence.get("pinpoint", ""), evidence.get("relation", ""),
                review.get("resolution", ""),
            ])
    return rows


def markdown_report(ledger: dict[str, Any], result: ValidationResult) -> str:
    if not result.structurally_valid:
        raise ValueError("Resolve structural errors before producing an evidence matrix.")
    lines = [f"# {markdown_text(ledger['title'])}", "", NOTICE, ""]
    if ledger.get("description"):
        lines += [markdown_text(ledger["description"]), ""]
    counts = {status: sum(claim["review_status"] == status for claim in ledger["claims"])
              for status in ("unreviewed", "checked", "contested")}
    matrix_columns = (0, 1, 2, 5, 12, 13)
    lines += [
        f"Sources: {len(ledger['sources'])}. Propositions: {len(ledger['claims'])}.",
        f"User-declared statuses: {counts['unreviewed']} unreviewed, {counts['checked']} checked, {counts['contested']} contested.",
        "", "## Evidence matrix", "",
        "| " + " | ".join(COLUMNS[index] for index in matrix_columns) + " |",
        "| " + " | ".join("---" for _ in matrix_columns) + " |",
    ]
    for row in evidence_rows(ledger):
        lines.append("| " + " | ".join(markdown_text(row[index]) for index in matrix_columns) + " |")
    if not ledger["claims"]:
        lines += ["", "No propositions have been entered."]
    lines += ["", "## Source register", "", "| Source ID | Title | Type | Jurisdiction | Version / as of | URL |", "| --- | --- | --- | --- | --- | --- |"]
    for source in ledger["sources"]:
        version = " / ".join(value for value in (source.get("version"), source.get("as_of")) if value)
        row = (source["id"], source["title"], source["source_type"], source["jurisdiction"], version, source["url"])
        lines.append("| " + " | ".join(markdown_text(value) for value in row) + " |")
    lines += ["", "## Human-review declarations", "", "| Claim ID | Reviewer | Review date | Treatment of contrary evidence |", "| --- | --- | --- | --- |"]
    for claim in ledger["claims"]:
        review = claim.get("review") or {}
        row = (claim["id"], review.get("reviewer", ""), review.get("date", ""), review.get("resolution", ""))
        lines.append("| " + " | ".join(markdown_text(value) for value in row) + " |")
    lines += ["", "## Outstanding structural and review notices", ""]
    if result.warnings:
        for finding in result.warnings:
            lines.append(f"- {markdown_text(finding.code)} ({markdown_text(finding.path)}): {markdown_text(finding.message)}")
    else:
        lines.append("No structural warnings were found. This is not a substantive evidence assessment.")
    lines += ["", "The ledger's JSON is the authoritative record. This matrix is a view of its recorded entries.", ""]
    return "\n".join(lines)


def csv_report(ledger: dict[str, Any], result: ValidationResult) -> str:
    if not result.structurally_valid:
        raise ValueError("Resolve structural errors before producing an evidence matrix.")
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n", quoting=csv.QUOTE_ALL)
    writer.writerow(COLUMNS)
    for row in evidence_rows(ledger):
        writer.writerow(csv_text(value) for value in row)
    return stream.getvalue()

