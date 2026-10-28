"""CLI for explicitly selected local inputs; external model calls are opt-in."""

from __future__ import annotations

import argparse
import os
import sys

from . import __version__
from .io import json_text, read_json, write_new


def parser():
    p = argparse.ArgumentParser(prog="regnav_esg", description="RegNav ESG workbench: extracted evidence and transparent calculations for review")
    p.add_argument("--version", action="version", version=__version__)
    commands = p.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="Produce an offline evidence workspace from local PDFs, text or Markdown")
    run.add_argument("paths", nargs="+")
    run.add_argument("--output", required=True)
    run.add_argument("--config", help="Custom candidate-field configuration JSON")
    run.add_argument("--assessment", help="Supplied accounting, materiality and/or action-plan input JSON")
    run.add_argument("--source-url", action="append", help="One original URL per document, enabling core ledger export")
    run.add_argument("--jurisdiction", default="UNSPECIFIED")
    run.add_argument("--ocr", action="store_true", help="Explicitly request local OCR, if supported by the installed parser")
    run.add_argument("--tables", action="store_true", help="Extract candidate PDF table cells using optional pdfplumber")
    ingest = commands.add_parser("ingest", help="Extract page-preserving text and source identity")
    ingest.add_argument("path")
    ingest.add_argument("--ocr", action="store_true")
    ingest.add_argument("--tables", action="store_true")
    ingest.add_argument("--output")
    markdown = commands.add_parser("markdown", help="Export retained pages and candidate tables to Markdown")
    markdown.add_argument("document")
    markdown.add_argument("--output")
    extract = commands.add_parser("extract", help="Extract transparent candidate fields from an ingested document")
    extract.add_argument("document")
    extract.add_argument("--config")
    extract.add_argument("--output")
    search = commands.add_parser("search", help="Retrieve matching source pages locally")
    search.add_argument("document")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=5)
    search.add_argument("--output")
    quote = commands.add_parser("locate", help="Check quotation presence in extracted page text")
    quote.add_argument("document")
    quote.add_argument("quote")
    quote.add_argument("--page", type=int)
    quote.add_argument("--normalise-whitespace", action="store_true")
    quote.add_argument("--output")
    for command, description in [("inventory", "Calculate emissions from supplied activity data and versioned factors"),
                                 ("materiality", "Apply a supplied financial/impact materiality screening rubric"),
                                 ("plan", "Create an action plan from supplied gaps and action templates")]:
        sub = commands.add_parser(command, help=description)
        sub.add_argument("input")
        sub.add_argument("--output")
    standards = commands.add_parser("standard", help="Exact lookup of a supplied standard code and version")
    standards.add_argument("registry")
    standards.add_argument("framework")
    standards.add_argument("version")
    standards.add_argument("code")
    standards.add_argument("--output")
    tabular = commands.add_parser("import-activities", help="Import explicit activity data from CSV or optional XLSX")
    tabular.add_argument("path")
    tabular.add_argument("--mapping", help="JSON mapping of canonical fields to file column names")
    tabular.add_argument("--sheet")
    tabular.add_argument("--delimiter", default=",")
    tabular.add_argument("--output")
    model = commands.add_parser("model-extract", help="Opt-in model extraction, with exact source-quotation checks")
    model.add_argument("document")
    model.add_argument("--model", required=True)
    model.add_argument("--key-env", default="REGNAV_MODEL_API_KEY")
    model.add_argument("--endpoint", default="https://api.openai.com/v1/responses")
    model.add_argument("--allow-network", action="store_true", help="Allow selected source pages to be sent to the named provider")
    model.add_argument("--query", help="Retrieve only pages relevant to this query before sending")
    model.add_argument("--output")
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "run":
            from .workflow import run_workbench
            result = run_workbench(args.paths, args.output,
                                   config=read_json(args.config) if args.config else None,
                                   assessment=read_json(args.assessment) if args.assessment else None,
                                   source_urls=args.source_url, jurisdiction=args.jurisdiction, ocr=args.ocr, tables=args.tables)
        elif args.command == "ingest":
            from .ingest import ingest_document
            result = ingest_document(args.path, ocr=args.ocr, tables=args.tables)
        elif args.command == "markdown":
            from .ingest import document_to_markdown
            result = document_to_markdown(read_json(args.document))
        elif args.command == "extract":
            from .extract import extract_candidates
            result = extract_candidates(read_json(args.document), config=read_json(args.config) if args.config else None)
        elif args.command == "search":
            from .retrieval import search_pages
            result = search_pages(read_json(args.document), args.query, limit=args.limit)
        elif args.command == "locate":
            from .ingest import match_quote
            result = match_quote(read_json(args.document), args.quote, page_number=args.page, normalise_whitespace=args.normalise_whitespace)
        elif args.command == "inventory":
            from .accounting import calculate_inventory
            result = calculate_inventory(read_json(args.input))
        elif args.command == "materiality":
            from .materiality import screen_materiality
            result = screen_materiality(read_json(args.input))
        elif args.command == "plan":
            from .planning import build_action_plan
            result = build_action_plan(read_json(args.input))
        elif args.command == "standard":
            from .materiality import StandardsRegistry
            result = StandardsRegistry(read_json(args.registry)).lookup(args.framework, args.version, args.code)
        elif args.command == "import-activities":
            from .tabular import import_activity_rows
            result = import_activity_rows(args.path, mapping=read_json(args.mapping) if args.mapping else None,
                                          sheet=args.sheet, delimiter=args.delimiter)
        elif args.command == "model-extract":
            from .model import model_extract
            result = model_extract(read_json(args.document), model=args.model, api_key=os.environ.get(args.key_env, ""),
                                   endpoint=args.endpoint, allow_network=args.allow_network, query=args.query)
        else:
            raise ValueError("Unsupported command")
        if args.command != "run" and getattr(args, "output", None):
            write_new(args.output, result if args.command == "markdown" else json_text(result))
            print(f"Wrote {args.output}")
        else:
            sys.stdout.write(result if args.command == "markdown" else json_text(result))
        return 2 if args.command == "ingest" and result.get("status") not in {"ready", "partial_text"} else 0
    except (ValueError, OSError, UnicodeError, ImportError, RecursionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
