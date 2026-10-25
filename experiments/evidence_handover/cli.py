"""Command-line access to the experimental handover workflow."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from . import workflow as w


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    mapped = commands.add_parser("map", help="Validate one export and emit an unreviewed ledger")
    mapped.add_argument("export")
    mapped.add_argument("--output")
    snap = commands.add_parser("snapshot", help="Retain supplied records and observed file identities")
    snap.add_argument("export")
    snap.add_argument("--root", required=True)
    snap.add_argument("--output")
    comparison = commands.add_parser("compare", help="Produce a read-only handover")
    comparison.add_argument("before")
    comparison.add_argument("after")
    comparison.add_argument("--root", required=True)
    comparison.add_argument("--history")
    comparison.add_argument("--format", choices=("json", "markdown", "csv"), default="json")
    comparison.add_argument("--output")
    add = commands.add_parser("review-add", help="Create a NEW history from a supplied declaration")
    add.add_argument("history")
    add.add_argument("entry")
    add.add_argument("--snapshot", required=True)
    add.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        status = 0
        if args.command == "map":
            data = w.map_export(w.load(args.export, w.MAX_INPUT))
        elif args.command == "snapshot":
            data = w.snapshot(w.load(args.export, w.MAX_INPUT), args.root)
            status = 2 if any(r["status"] != "OBSERVED" for r in data["source_observations"]) else 0
        elif args.command == "review-add":
            basis = w.load(args.snapshot)
            w.validate_snapshot(basis)
            entry = w.load(args.entry, w.MAX_INPUT)
            if (not isinstance(entry, dict) or entry.get("snapshot_id") != basis["snapshot_id"]
                    or entry.get("claim_id") not in {r["id"] for r in basis["ledger"]["claims"]}):
                raise w.InputError("Declaration must identify the supplied snapshot and one of its claims")
            data = w.append_review(w.load(args.history), entry)
        else:
            data = w.compare(w.load(args.before), w.load(args.after, w.MAX_INPUT), args.root,
                             w.load(args.history) if args.history else None)
            status = 2 if data["attention"] else 0
        text = w.dumps(data)
        if args.command == "compare" and args.format != "json":
            text = w.report_markdown(data) if args.format == "markdown" else w.report_csv(data)
        if args.output:
            w.write_new(args.output, text)
        else:
            sys.stdout.write(text)
        return status
    except w.InputError as exc:
        sys.stderr.write("Contract error: " + str(exc) + "\n")
        return 1
    except (OSError, ValueError, TypeError, RuntimeError, RecursionError):
        sys.stderr.write("Input/output error: check the configured files, directory, limits and NEW output destination.\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
