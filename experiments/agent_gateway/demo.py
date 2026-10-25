"""Exercise the local MCP wire path using fictional files; no remote agent."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
# Import the same operator-controlled implementation used by the server.
sys.path.insert(0, str(HERE))
from server import PROTOCOL, watch


def run_demo() -> dict:
    with tempfile.TemporaryDirectory(prefix="regnav-mcp-demo-") as directory:
        root = Path(directory)
        source = root / "fictional-rule.txt"
        source.write_text("FICTIONAL RULE: five working days.\n", encoding="utf-8")
        manifest = {"schema": watch.SCHEMA, "files": [
            {"id": "training-source", "path": source.name, "claim_ids": ["training-claim"]}
        ]}
        baseline = root / "baseline.json"
        baseline.write_text(json.dumps(watch.snapshot(manifest, root)), encoding="utf-8")
        saved = baseline.read_bytes()
        def exchange():
            messages = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": PROTOCOL, "capabilities": {}, "clientInfo": {"name": "fictional-demo-client", "version": "0.1"}}},
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "source_watch_check", "arguments": {}}},
            ]
            completed = subprocess.run([sys.executable, str(HERE / "server.py"), "--baseline", str(baseline), "--root", str(root)],
                input="".join(json.dumps(item) + "\n" for item in messages), text=True, capture_output=True, timeout=15, check=True)
            replies = [json.loads(line) for line in completed.stdout.splitlines()]
            assert len(replies) == 3 and not completed.stderr
            assert replies[0]["result"]["protocolVersion"] == PROTOCOL
            assert not replies[2]["result"]["isError"]
            return replies
        unchanged = exchange()
        source.write_text("FICTIONAL RULE: ten working days.\n", encoding="utf-8")
        changed = exchange()
        source.unlink()
        missing = exchange()
        assert baseline.read_bytes() == saved
        reports = [items[2]["result"]["structuredContent"] for items in (unchanged, changed, missing)]
        assert [r["files"][0]["status"] for r in reports] == ["UNCHANGED_BYTES", "CHANGED_BYTES", "NOT_OBSERVED"]
        return {"context": "Internal fictional subprocess demonstration, not an external agent or customer.",
                "protocol_version": PROTOCOL,
                "tools": [t["name"] for t in unchanged[1]["result"]["tools"]],
                "reports": dict(zip(("unchanged", "changed", "unavailable"), reports))}


if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2))
