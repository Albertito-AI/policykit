"""Focused checks for the isolated source-watch experiment; no legal claims."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "experiments" / "source_watch" / "watch.py"
spec = importlib.util.spec_from_file_location("source_watch", SCRIPT)
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)


class SourceWatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "source.txt").write_bytes(b"fictional source\n")
        self.manifest = {"schema": w.SCHEMA, "files": [{"id": "s1", "path": "source.txt", "claim_ids": ["c2", "c1"]}]}
        self.before = w.snapshot(self.manifest, self.root)

    def test_unchanged(self):
        self.assertEqual(w.check(self.before, self.root)["observation"], "UNCHANGED_BYTES")

    def test_changed_links_only(self):
        (self.root / "other.txt").write_bytes(b"unrelated")
        self.manifest["files"].append({"id": "s2", "path": "other.txt", "claim_ids": ["c3"]})
        before = w.snapshot(self.manifest, self.root)
        (self.root / "source.txt").write_bytes(b"changed")
        result = w.check(before, self.root)
        self.assertEqual(result["affected_claim_ids"], ["c1", "c2"])
        self.assertEqual(result["files"][1]["status"], "UNCHANGED_BYTES")

    def test_missing_is_not_unchanged(self):
        (self.root / "source.txt").unlink()
        result = w.check(self.before, self.root)
        self.assertEqual(result["files"][0]["status"], "NOT_OBSERVED")
        self.assertEqual(result["observation"], "RECHECK_REQUIRED")

    def test_invalid_hash(self):
        self.before["files"][0]["sha256"] = "bad"
        with self.assertRaises(w.InputError): w.check(self.before, self.root)

    def test_empty_manifest(self):
        self.manifest["files"] = []
        with self.assertRaises(w.InputError): w.snapshot(self.manifest, self.root)

    def test_duplicate_keys(self):
        path = self.root / "bad.json"
        path.write_text('{"schema":1,"schema":2}')
        with self.assertRaises(w.InputError): w.load_json(path)

    def test_duplicate_source_id(self):
        self.manifest["files"].append(copy.deepcopy(self.manifest["files"][0]))
        with self.assertRaises(w.InputError): w.snapshot(self.manifest, self.root)

    def test_invalid_paths(self):
        for value in ("../secret", "/tmp/file", "C:/file", "a\\b", "a//b", "a/./b", "a/../b", "a\x00b"):
            with self.subTest(path=value), self.assertRaises(w.InputError):
                w._path(value)

    def test_symlink(self):
        target = self.root / "alias.txt"
        try: target.symlink_to(self.root / "source.txt")
        except (OSError, NotImplementedError): self.skipTest("Symlink unavailable")
        self.manifest["files"][0]["path"] = "alias.txt"
        with self.assertRaises(w.InputError): w.snapshot(self.manifest, self.root)

    def test_directory_is_not_source(self):
        (self.root / "dir").mkdir()
        self.manifest["files"][0]["path"] = "dir"
        with self.assertRaises(w.InputError): w.snapshot(self.manifest, self.root)

    def test_size_limit(self):
        original = w.MAX_FILE
        w.MAX_FILE = 1
        try:
            with self.assertRaises(w.InputError): w.snapshot(self.manifest, self.root)
        finally: w.MAX_FILE = original

    def test_no_mutation(self):
        original = copy.deepcopy(self.before)
        data = (self.root / "source.txt").read_bytes()
        w.check(self.before, self.root)
        self.assertEqual(self.before, original)
        self.assertEqual((self.root / "source.txt").read_bytes(), data)

    def test_invalid_timestamp(self):
        self.before["observed_at"] = "2026-10-24"
        with self.assertRaises(w.InputError): w.check(self.before, self.root)

    def test_unknown_fields_rejected(self):
        self.manifest["files"][0]["reviewed"] = True
        with self.assertRaises(w.InputError): w.snapshot(self.manifest, self.root)

    def test_cli_and_protected_output(self):
        manifest = self.root / "manifest.json"
        baseline = self.root / "baseline.json"
        manifest.write_text(json.dumps(self.manifest))
        def run(*args):
            return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
        self.assertEqual(run("snapshot", str(manifest), "--root", str(self.root), "--output", str(baseline)).returncode, 0)
        saved = baseline.read_bytes()
        self.assertEqual(run("check", str(baseline), "--root", str(self.root)).returncode, 0)
        (self.root / "source.txt").write_bytes(b"changed")
        result = run("check", str(baseline), "--root", str(self.root))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["affected_claim_ids"], ["c1", "c2"])
        self.assertEqual(run("snapshot", str(manifest), "--root", str(self.root), "--output", str(baseline)).returncode, 1)
        self.assertEqual(baseline.read_bytes(), saved)
        manifest.write_text("invalid JSON")
        self.assertEqual(run("snapshot", str(manifest), "--root", str(self.root)).returncode, 1)

    def test_unlisted_file_not_covered(self):
        (self.root / "unlisted.txt").write_bytes(b"new")
        self.assertEqual(len(w.check(self.before, self.root)["files"]), 1)

    def test_digest_exact_bytes(self):
        self.assertEqual(self.before["files"][0]["sha256"], hashlib.sha256(b"fictional source\n").hexdigest())


if __name__ == "__main__":
    unittest.main()
