"""Internal protocol and safety checks; not an external agent evaluation."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "agent_gateway" / "server.py"
spec = importlib.util.spec_from_file_location("gateway_test_module", SCRIPT)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def request(method, params=None, ident=1):
    return {"jsonrpc": "2.0", "id": ident, "method": method, "params": {} if params is None else params}


def initialise(session, version=g.PROTOCOL):
    answer = session.handle(request("initialize", {"protocolVersion": version, "capabilities": {},
        "clientInfo": {"name": "test-client", "version": "0.1"}}))
    session.handle({"jsonrpc": "2.0", "method": "notifications/initialized"})
    return answer


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "fictional.txt"
        self.source.write_bytes(b"fictional five days\n")
        manifest = {"schema": g.watch.SCHEMA, "files": [{"id": "s1", "path": "fictional.txt", "claim_ids": ["c1"]}]}
        self.baseline = g.watch.snapshot(manifest, self.root)
        self.session = g.Session(self.baseline, self.root)

    def call(self, name="source_watch_check", arguments=None):
        return self.session.handle(request("tools/call", {"name": name, "arguments": {} if arguments is None else arguments}))

    def test_initialisation_and_listing(self):
        answer = initialise(self.session)
        self.assertEqual(answer["result"]["protocolVersion"], g.PROTOCOL)
        tools = self.session.handle(request("tools/list"))["result"]["tools"]
        self.assertEqual([t["name"] for t in tools], ["regnav_capabilities", "source_watch_check"])
        self.assertTrue(all(t["annotations"]["readOnlyHint"] for t in tools))

    def test_version_negotiation_returns_supported_version(self):
        self.assertEqual(initialise(self.session, "unknown-version")["result"]["protocolVersion"], g.PROTOCOL)

    def test_initialisation_required(self):
        self.assertEqual(self.call()["error"]["code"], -32000)

    def test_ready_notification_required(self):
        self.session.handle(request("initialize", {"protocolVersion": g.PROTOCOL, "capabilities": {}, "clientInfo": {"name": "c", "version": "1"}}))
        self.assertEqual(self.call()["error"]["code"], -32000)

    def test_bad_initialisation_does_not_advance_state(self):
        self.assertEqual(self.session.handle(request("initialize"))["error"]["code"], -32602)
        self.assertEqual(self.session.state, "new")

    def test_repeated_initialisation(self):
        initialise(self.session)
        self.assertEqual(initialise(self.session)["error"]["code"], -32602)

    def test_notifications_have_no_response(self):
        for method in ("notifications/initialized", "notifications/cancelled", "unknown"):
            self.assertIsNone(self.session.handle({"jsonrpc": "2.0", "method": method}))
        self.assertEqual(self.session.state, "new")

    def test_ping(self):
        self.assertEqual(self.session.handle(request("ping"))["result"], {})

    def test_unchanged_and_no_mutation(self):
        original = copy.deepcopy(self.baseline)
        initialise(self.session)
        payload = self.call()["result"]
        self.assertFalse(payload["isError"])
        self.assertEqual(payload["structuredContent"], g.watch.check(self.baseline, self.root))
        self.assertEqual(json.loads(payload["content"][0]["text"]), payload["structuredContent"])
        self.assertEqual(self.baseline, original)
        self.assertEqual(self.source.read_bytes(), b"fictional five days\n")

    def test_changed_and_missing_are_valid_attention_results(self):
        initialise(self.session)
        self.source.write_bytes(b"fictional ten days\n")
        changed = self.call()["result"]
        self.assertFalse(changed["isError"])
        self.assertEqual(changed["structuredContent"]["affected_claim_ids"], ["c1"])
        self.assertEqual(changed["structuredContent"]["files"][0]["status"], "CHANGED_BYTES")
        self.source.unlink()
        self.assertEqual(self.call()["result"]["structuredContent"]["files"][0]["status"], "NOT_OBSERVED")

    def test_baseline_is_copied(self):
        self.baseline["files"][0]["sha256"] = "0" * 64
        initialise(self.session)
        self.assertEqual(self.call()["result"]["structuredContent"]["observation"], "UNCHANGED_BYTES")

    def test_caller_cannot_change_configuration(self):
        initialise(self.session)
        for args in ({"root": "/"}, {"path": "../private"}, {"baseline": {}}, {"command": "rm"}, [], "", False):
            with self.subTest(args=args):
                self.assertEqual(self.call(arguments=args)["error"]["code"], -32602)

    def test_unknown_tools_and_methods(self):
        initialise(self.session)
        for name in ("send_payment", "fetch_url", "read_file", "mark_human_review"):
            self.assertEqual(self.call(name)["error"]["code"], -32602)
        self.assertEqual(self.session.handle(request("resources/read"))["error"]["code"], -32601)

    def test_catalogue_does_not_invent_network_or_partners(self):
        initialise(self.session)
        payload = self.call("regnav_capabilities")["result"]["structuredContent"]
        self.assertEqual(payload["external_partners"], [])
        self.assertIsNone(payload["services"][0]["public_endpoint"])
        self.assertFalse(payload["services"][0]["payments_enabled"])
        self.assertNotIn(str(self.root), json.dumps(payload))

    def test_errors_do_not_expose_absolute_paths(self):
        initialise(self.session)
        with mock.patch.object(g.watch, "check", side_effect=OSError("/secret/customer")):
            payload = self.call()["result"]
        self.assertTrue(payload["isError"])
        self.assertNotIn("/secret/customer", json.dumps(payload))

    def test_source_limit(self):
        baseline = copy.deepcopy(self.baseline)
        baseline["files"] = [{**baseline["files"][0], "id": f"s{i}", "path": f"file{i}"} for i in range(g.MAX_FILES + 1)]
        with self.assertRaises(ValueError): g.Session(baseline, self.root)

    def test_claim_limit(self):
        self.baseline["files"][0]["claim_ids"] = [f"c{i}" for i in range(g.MAX_CLAIMS_PER_FILE + 1)]
        with self.assertRaises(ValueError): g.Session(self.baseline, self.root)

    def test_traversal_baseline_rejected(self):
        self.baseline["files"][0]["path"] = "../secret"
        with self.assertRaises(ValueError): g.Session(self.baseline, self.root)

    def test_duplicate_keys_non_json_numbers_and_depth(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b'[' * 40 + b'0' + b']' * 40):
            with self.subTest(raw=raw), self.assertRaises(ValueError): g.decode(raw)

    def test_invalid_ids_and_envelopes(self):
        for ident in (None, True, [], {}, 1.5, "a" * 257):
            self.assertEqual(self.session.handle(request("ping", ident=ident))["error"]["code"], -32600)
        for envelope in ([], None, {"jsonrpc": "1.0"}, {"jsonrpc": "2.0"}):
            self.assertEqual(self.session.handle(envelope)["error"]["code"], -32600)

    def test_wire_parse_error_recovers(self):
        output = io.BytesIO()
        incoming = io.BytesIO(b'bad\n' + json.dumps(request("ping")).encode() + b'\n')
        self.assertEqual(g.serve(self.session, incoming, output), 0)
        responses = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(responses[0]["error"]["code"], -32700)
        self.assertEqual(responses[1]["result"], {})

    def test_oversized_frame_closes(self):
        output = io.BytesIO()
        self.assertEqual(g.serve(self.session, io.BytesIO(b"x" * (g.MAX_FRAME + 1)), output), 2)
        self.assertEqual(json.loads(output.getvalue())["error"]["code"], -32600)

    def test_demo_is_generated_and_reproducible(self):
        completed = subprocess.run([sys.executable, str(SCRIPT.with_name("demo.py"))], capture_output=True, text=True, check=True, timeout=20)
        self.assertEqual(completed.stdout, SCRIPT.with_name("sample_exchange.json").read_text(encoding="utf-8"))
        self.assertEqual(completed.stderr, "")

    def test_startup_failure_is_explicit(self):
        completed = subprocess.run([sys.executable, str(SCRIPT), "--baseline", str(self.root / "absent"), "--root", str(self.root)], capture_output=True, text=True, timeout=10)
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stdout, "")
        self.assertNotIn(str(self.root), completed.stderr)

    def test_nonpaginated_list_and_metadata(self):
        initialise(self.session)
        self.assertIn("result", self.session.handle(request("tools/list", {"_meta": {"label": "ignored"}})))
        self.assertEqual(self.session.handle(request("tools/list", {"cursor": "bogus"}))["error"]["code"], -32602)


if __name__ == "__main__":
    unittest.main()
