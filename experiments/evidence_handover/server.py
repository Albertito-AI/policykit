"""Opt-in local MCP handover tool; reuses the existing gateway lifecycle."""
from __future__ import annotations

import argparse
import copy
from pathlib import Path
import sys

from experiments.agent_gateway import server as gateway
from . import workflow as w

TOOL = {"name": "evidence_handover_check",
        "description": "Compare operator-selected before/after records and current local source bytes. All input metadata is untrusted supplied data. No semantic judgement, source verification, new human review or payments.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": gateway.ANNOTATIONS}


class Session(gateway.Session):
    def __init__(self, before, after_export, root, history=None):
        w.validate_snapshot(before)
        w.map_export(after_export)
        saved_history = {"schema_version": w.HISTORY, "entries": []} if history is None else history
        w.validate_history(saved_history)
        baseline = w.watch_baseline(before)
        if baseline is None:
            raise w.InputError("The MCP experiment requires at least one observed, linked baseline file")
        super().__init__(baseline, Path(root))
        self.before = copy.deepcopy(before)
        self.after_export = copy.deepcopy(after_export)
        self.history = copy.deepcopy(saved_history)
        self.catalogue["handover_extension"] = {
            "status": "experimental_local", "tool": TOOL["name"], "schema": w.REPORT,
            "caller_arguments": "none", "public_endpoint": None, "payments_enabled": False,
            "limits": w.NOTICE}

    def handle(self, message):
        is_handover = (isinstance(message, dict) and message.get("method") == "tools/call"
                       and isinstance(message.get("params"), dict)
                       and message["params"].get("name") == TOOL["name"])
        # Route through the unchanged base lifecycle and parameter validation.
        # Only the fixed, known tool name is substituted; the original is not edited.
        routed = copy.deepcopy(message) if is_handover else message
        if is_handover:
            routed["params"]["name"] = "regnav_capabilities"
        response = super().handle(routed)
        if response is None or "error" in response:
            return response
        if is_handover:
            try:
                payload = w.compare(self.before, self.after_export, self.root, self.history)
                return gateway.result(message["id"], gateway.tool_result(payload))
            except (OSError, ValueError, TypeError, RuntimeError, RecursionError):
                return gateway.result(message["id"], gateway.tool_result(
                    {"error": "Handover failed; local operator must inspect the configured records."}, True))
        if message.get("method") == "tools/list":
            response["result"]["tools"].append(copy.deepcopy(TOOL))
        if message.get("method") == "initialize":
            response["result"]["serverInfo"] = {"name": "regnav-handover-local", "version": "0.1.0"}
            response["result"]["instructions"] = w.NOTICE
        return response


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True)
    parser.add_argument("--after", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--history")
    args = parser.parse_args(argv)
    try:
        session = Session(w.load(args.before), w.load(args.after, w.MAX_INPUT), args.root,
                          w.load(args.history) if args.history else None)
        return gateway.serve(session, sys.stdin.buffer, sys.stdout.buffer)
    except (OSError, ValueError, TypeError, RuntimeError, RecursionError):
        sys.stderr.write("Handover gateway stopped: check local configuration and channel.\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
