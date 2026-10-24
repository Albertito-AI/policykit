"""Command-line interface; no network calls, API keys or third-party dependencies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__
from .changes import compare_ledgers, text_report
from .reports import csv_report, markdown_report
from .validation import LedgerReadError, NOTICE, SCHEMA_VERSION, load_ledger, validate


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="regnav_evidence", description="Offline metadata and human-review ledger for scholarly evidence.")
    result.add_argument("--version", action="version", version=__version__)
    commands = result.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create a blank ledger without overwriting a file.")
    init.add_argument("path", type=Path)
    init.add_argument("--title", default="Untitled evidence ledger")
    check = commands.add_parser("validate", help="Check structure and surface recorded review gaps.")
    check.add_argument("path", type=Path)
    check.add_argument("--strict", action="store_true", help="Exit 2 when structural warnings remain.")
    check.add_argument("--json", action="store_true", help="Emit a machine-readable validation result.")
    report = commands.add_parser("report", help="Export a structurally valid ledger as an evidence matrix.")
    report.add_argument("path", type=Path)
    report.add_argument("--format", choices=("markdown", "csv"), default="markdown")
    report.add_argument("--output", type=Path)
    report.add_argument("--force", action="store_true", help="Allow replacement of an existing report, never the input ledger.")
    compare = commands.add_parser("compare", help="Identify potentially stale review declarations between two snapshots.")
    compare.add_argument("before", type=Path, help="Earlier ledger snapshot.")
    compare.add_argument("after", type=Path, help="Revised ledger snapshot.")
    compare.add_argument("--json", action="store_true", help="Emit a machine-readable comparison.")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "init":
        if not args.title.strip():
            print("error: --title must contain text.", file=sys.stderr)
            return 1
        ledger = {"schema_version": SCHEMA_VERSION, "title": args.title, "description": "", "sources": [], "claims": []}
        if validate(ledger).errors:
            print("error: --title contains unsupported characters.", file=sys.stderr)
            return 1
        try:
            with args.path.open("x", encoding="utf-8", newline="\n") as handle:
                json.dump(ledger, handle, indent=2, ensure_ascii=False)
                handle.write("\n")
        except (OSError, UnicodeError) as exc:
            print(f"error: cannot create ledger: {exc}", file=sys.stderr)
            return 1
        print(f"Created {args.path}. Add source records and propositions before review.")
        return 0
    if args.command == "compare":
        try:
            earlier = load_ledger(args.before)
            revised = load_ledger(args.after)
        except LedgerReadError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        for label, value in (("before", earlier), ("after", revised)):
            checked = validate(value)
            if checked.errors:
                for item in checked.errors:
                    print(f"error: {label}: {item.code} {item.path}: {item.message}", file=sys.stderr)
                return 1
        comparison = compare_ledgers(earlier, revised)
        if args.json:
            print(json.dumps(comparison, ensure_ascii=False, indent=2))
        else:
            sys.stdout.write(text_report(comparison))
        return 0
    try:
        ledger = load_ledger(args.path)
    except LedgerReadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    result = validate(ledger)
    if args.command == "validate":
        if args.json:
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        else:
            print(NOTICE)
            for item in result.findings:
                print(f"{item.severity.upper()} {item.code} {item.path}: {item.message}")
            print(f"Structural checks: {len(result.errors)} error(s), {len(result.warnings)} warning(s).")
        return 1 if result.errors else (2 if args.strict and result.warnings else 0)

    if result.errors:
        for item in result.errors:
            print(f"error: {item.code} {item.path}: {item.message}", file=sys.stderr)
        return 1
    print(NOTICE, file=sys.stderr)
    if result.warnings:
        print(f"notice: {len(result.warnings)} warning(s); run validate for their details.", file=sys.stderr)
    contents = markdown_report(ledger, result) if args.format == "markdown" else csv_report(ledger, result)
    if args.output is None:
        sys.stdout.write(contents)
        return 0
    try:
        if args.output.resolve() == args.path.resolve():
            print("error: report output must differ from the input ledger.", file=sys.stderr)
            return 1
        # Also protect input files reached through hard links.
        if args.output.exists() and args.output.samefile(args.path):
            print("error: report output refers to the input ledger.", file=sys.stderr)
            return 1
        with args.output.open("w" if args.force else "x", encoding="utf-8", newline="") as handle:
            handle.write(contents)
    except (OSError, UnicodeError) as exc:
        print(f"error: cannot write report: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {args.output}.", file=sys.stderr)
    return 0
