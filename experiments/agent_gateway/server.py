"""Local MCP tools for an operator-selected Source Watch baseline. No network."""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, BinaryIO

# Resolve only repository-controlled code, never a module named by a request.
WATCH_PATH = Path(__file__).resolve().parents[1] / "source_watch" / "watch.py"
_spec = importlib.util.spec_from_file_location("regnav_gateway_watch", WATCH_PATH)
assert _spec is not None and _spec.loader is not None
watch = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(watch)

PROTOCOL = "2025-11-25"
MAX_FRAME = 65_536
MAX_DEPTH = 32
MAX_FILES = 16
MAX_CLAIMS_PER_FILE = 64
MAX_OUTPUT = 2_097_152
CATALOGUE = Path(__file__).with_name("services.json")
ANNOTATIONS = {"readOnlyHint": True, "destructiveHint": False,
               "idempotentHint": True, "openWorldHint": False}
TOOLS = [
    {"name": "regnav_capabilities", "description": "Describe this local prototype, its limits and rights. No partner or payment discovery.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
     "annotations": ANNOTATIONS},
    {"name": "source_watch_check", "description": "Compare only the operator-configured local files with their saved baseline. Return affected supplied claim IDs. Byte checks are not legal verification or human review. Relative filenames and hashes appear in the result.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
     "annotations": ANNOTATIONS},
]


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate key")
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise ValueError("Non-JSON number")


def decode(raw: bytes) -> Any:
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique,
                      parse_constant=_constant)
    pending = [(data, 0)]
    while pending:
        value, depth = pending.pop()
        if depth > MAX_DEPTH:
            raise ValueError("Message too deep")
        if isinstance(value, dict):
            pending.extend((item, depth + 1) for item in value.values())
        elif isinstance(value, list):
            pending.extend((item, depth + 1) for item in value)
    return data


def error(ident: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": ident,
            "error": {"code": code, "message": message}}


def result(ident: Any, payload: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": ident, "result": payload}


def tool_result(payload: dict[str, Any], failed: bool = False) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=True, allow_nan=False)}],
            "structuredContent": payload, "isError": failed}


class Session:
    """One local client and an immutable copy of the selected baseline."""

    def __init__(self, baseline: dict[str, Any], root: Path):
        rows = watch.validate(baseline, snapshot=True)
        if len(rows) > MAX_FILES or any(len(row["claim_ids"]) > MAX_CLAIMS_PER_FILE for row in rows):
            raise ValueError("Gateway configuration exceeds its pilot limits")
        self.root = Path(root).resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError("Root is not a directory")
        self.baseline = copy.deepcopy(baseline)
        self.catalogue = decode(CATALOGUE.read_bytes())
        self.state = "new"

    def handle(self, message: Any) -> dict[str, Any] | None:
        if not isinstance(message, dict) or message.get("jsonrpc") != "2.0":
            return error(None, -32600, "Invalid JSON-RPC request")
        method = message.get("method")
        if not isinstance(method, str) or not method:
            return error(None, -32600, "Method is required")
        has_id = "id" in message
        ident = message.get("id")
        if has_id and (type(ident) not in (str, int) or (isinstance(ident, str) and len(ident) > 256)):
            return error(None, -32600, "Request ID must be a bounded string or integer")
        params = message.get("params", {})
        if not isinstance(params, dict) or ("_meta" in params and not isinstance(params["_meta"], dict)):
            return error(ident, -32602, "Parameters must be an object") if has_id else None
        if not has_id:
            if method == "notifications/initialized" and self.state == "initialising" and not (params.keys() - {"_meta"}):
                self.state = "ready"
            return None  # Notifications never receive a response.
        if method == "ping":
            return result(ident, {})
        if method == "initialize":
            info = params.get("clientInfo")
            if (self.state != "new" or not isinstance(params.get("protocolVersion"), str)
                    or not params["protocolVersion"] or not isinstance(params.get("capabilities"), dict)
                    or not isinstance(info, dict) or not isinstance(info.get("name"), str)
                    or not info["name"] or not isinstance(info.get("version"), str) or not info["version"]):
                return error(ident, -32602, "Invalid or repeated initialisation")
            self.state = "initialising"
            return result(ident, {"protocolVersion": PROTOCOL,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "regnav-source-watch-local", "version": "0.1.0"},
                "instructions": "Use only with the operator's permission. Results are byte observations, not legal findings. No payments or external delegation are available."})
        if self.state != "ready":
            return error(ident, -32000, "Complete MCP initialisation first")
        if method == "tools/list":
            if params.keys() - {"_meta"}:
                return error(ident, -32602, "This fixed tool list has no pagination cursor")
            return result(ident, {"tools": copy.deepcopy(TOOLS)})
        if method != "tools/call":
            return error(ident, -32601, "Method not available")
        if params.keys() - {"name", "arguments", "_meta"} or not isinstance(params.get("name"), str):
            return error(ident, -32602, "Invalid tool request")
        if params.get("arguments", {}) != {}:
            return error(ident, -32602, "These tools accept no arguments; paths and baselines are configured by the operator")
        name = params["name"]
        if name not in {item["name"] for item in TOOLS}:
            return error(ident, -32602, "Unknown tool")
        try:
            payload = copy.deepcopy(self.catalogue) if name == "regnav_capabilities" else watch.check(self.baseline, self.root)
            return result(ident, tool_result(payload))
        except (OSError, ValueError, RuntimeError):
            return result(ident, tool_result({"error": "Configured check could not complete. Ask the local operator to inspect the configuration."}, True))


def serve(session: Session, incoming: BinaryIO, outgoing: BinaryIO) -> int:
    while True:
        raw = incoming.readline(MAX_FRAME + 1)
        if not raw:
            return 0
        oversized = len(raw) > MAX_FRAME
        try:
            response = error(None, -32600, "Message exceeds 64 KiB; session closed") if oversized else session.handle(decode(raw))
        except (ValueError, UnicodeError, RecursionError, OverflowError):
            response = error(None, -32700, "Invalid or excessive JSON input")
        if response is not None:
            encoded = json.dumps(response, ensure_ascii=True, allow_nan=False).encode("utf-8") + b"\n"
            if len(encoded) > MAX_OUTPUT:
                encoded = (json.dumps(error(response.get("id"), -32603, "Result exceeds the local output limit")) + "\n").encode()
            outgoing.write(encoded)
            outgoing.flush()
        if oversized:
            return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, help="Operator-selected existing Source Watch snapshot")
    parser.add_argument("--root", required=True, help="Trusted, stable local source directory")
    args = parser.parse_args(argv)
    try:
        session = Session(watch.load_json(args.baseline), Path(args.root))
        return serve(session, sys.stdin.buffer, sys.stdout.buffer)
    except (OSError, ValueError, RuntimeError, RecursionError):
        sys.stderr.write("Gateway stopped: inspect the local configuration or input/output channel. No absolute paths are logged.\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
