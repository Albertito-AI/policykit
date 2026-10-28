"""Compose local ingestion, candidate extraction and optional supplied analyses."""

from __future__ import annotations

import csv
import io
from pathlib import Path

from .io import json_text, write_new
from .reports import render_html, to_ledger


def run_assessments(payload):
    if not isinstance(payload, dict):
        raise ValueError("Assessment input must be an object")
    allowed = {"inventory", "materiality", "action_plan"}
    if set(payload) - allowed:
        raise ValueError("Unknown assessment inputs: " + ", ".join(sorted(set(payload) - allowed)))
    results = {}
    if "inventory" in payload:
        from .accounting import calculate_inventory
        results["inventory"] = calculate_inventory(payload["inventory"])
    if "materiality" in payload:
        from .materiality import screen_materiality
        results["materiality"] = screen_materiality(payload["materiality"])
    if "action_plan" in payload:
        from .planning import build_action_plan
        results["action_plan"] = build_action_plan(payload["action_plan"])
    return results


def _csv_text(extractions):
    from regnav_evidence.reports import csv_text
    # Candidate CSV is a view; source JSON is the complete record.
    out = io.StringIO(newline="")
    writer = csv.writer(out)
    writer.writerow(["document", "field", "category", "page_or_segment", "candidate_text", "review_status"])
    def cell(value):
        return csv_text(str(value))
    for i, extraction in enumerate(extractions, 1):
        for field in extraction.get("fields", []):
            for candidate in field.get("candidates", []):
                citation = candidate.get("citation", {})
                writer.writerow([i, cell(field.get("field_id", field.get("id", ""))), cell(field.get("category", "")),
                                 citation.get("page_number", ""), cell(candidate.get("text", "")), "unreviewed"])
    return out.getvalue()


def run_workbench(paths, output, *, config=None, assessment=None, source_urls=None, jurisdiction="UNSPECIFIED", ocr=False, tables=False):
    from .ingest import ingest_document, document_to_markdown
    from .extract import extract_candidates

    if not paths or len(paths) > 16:
        raise ValueError("Supply between one and sixteen input documents")
    destination = Path(output)
    if destination.exists() or destination.is_symlink():
        raise ValueError("Output directory already exists; choose a new directory")
    documents = [ingest_document(path, ocr=ocr, tables=tables) for path in paths]
    if any(doc.get("status") not in {"ready", "partial_text"} for doc in documents):
        raise ValueError("At least one document has no usable text; inspect it or request OCR")
    extractions = [extract_candidates(doc, config=config) for doc in documents]
    assessments = run_assessments({} if assessment is None else assessment)
    ledger = to_ledger(documents, extractions, source_urls, jurisdiction=jurisdiction) if source_urls is not None else None
    contents = {
        "documents.json": json_text(documents),
        "extractions.json": json_text(extractions),
        "assessments.json": json_text(assessments),
        "candidates.csv": _csv_text(extractions),
        "report.html": render_html(documents, extractions, assessments=assessments),
    }
    if ledger is not None:
        contents["ledger.json"] = json_text(ledger)
    for index, document in enumerate(documents, 1):
        contents[f"source-{index}.md"] = document_to_markdown(document)
    destination.mkdir(parents=False, exist_ok=False)
    for name, text in contents.items():
        write_new(destination / name, text)
    return {"status": "completed", "output_directory": str(destination.resolve()),
            "files": list(contents), "documents": len(documents),
            "review_status": "unreviewed", "ledger_exported": ledger is not None}
