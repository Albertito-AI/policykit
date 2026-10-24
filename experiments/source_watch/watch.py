"""Experimental offline source-file change checks. No legal verification."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

SCHEMA = "regnav-source-watch/0.1"
MAX_JSON = 1_048_576
MAX_FILE = 16_777_216
ID = re.compile(r"[A-Za-z0-9_.:-]{1,100}\Z")
HASH = re.compile(r"[0-9a-f]{64}\Z")


class InputError(ValueError):
    """An input record cannot be safely interpreted."""


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError("Duplicate JSON key")
        result[key] = value
    return result


def load_json(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_JSON + 1)
    if len(raw) > MAX_JSON:
        raise InputError("JSON input exceeds 1 MiB")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_unique)


def _path(value):
    if not isinstance(value, str) or not value or len(value) > 512:
        raise InputError("File path must be a nonempty relative POSIX path")
    if "\\" in value or ":" in value or any(ord(c) < 32 for c in value):
        raise InputError("Unsupported path syntax")
    parts = value.split("/")
    if any(p in ("", ".", "..") for p in parts) or PurePosixPath(value).is_absolute():
        raise InputError("Absolute, empty and traversal path components are forbidden")
    return value


def validate(data, snapshot=False):
    keys = {"schema", "files", "observed_at"} if snapshot else {"schema", "files"}
    if not isinstance(data, dict) or set(data) != keys or data.get("schema") != SCHEMA:
        raise InputError("Unexpected schema or top-level fields")
    if snapshot:
        when = data["observed_at"]
        if not isinstance(when, str):
            raise InputError("Snapshot timestamp is required")
        try:
            moment = datetime.fromisoformat(when.replace("Z", "+00:00"))
        except ValueError as exc:
            raise InputError("Invalid snapshot timestamp") from exc
        if moment.utcoffset() is None:
            raise InputError("Snapshot timestamp must have a timezone")
    rows = data.get("files")
    if not isinstance(rows, list) or not 1 <= len(rows) <= 1000:
        raise InputError("Require between 1 and 1000 source records")
    seen_ids, seen_paths = set(), set()
    expected = {"id", "path", "claim_ids"} | ({"sha256"} if snapshot else set())
    for row in rows:
        if not isinstance(row, dict) or set(row) != expected:
            raise InputError("Unexpected source-record fields")
        ident = row["id"]
        if not isinstance(ident, str) or not ID.fullmatch(ident) or ident in seen_ids:
            raise InputError("Invalid or duplicate source identifier")
        path = _path(row["path"])
        if path in seen_paths:
            raise InputError("Duplicate source path")
        claims = row["claim_ids"]
        if not isinstance(claims, list) or not 1 <= len(claims) <= 1000:
            raise InputError("Each source needs 1 to 1000 linked claim identifiers")
        if any(not isinstance(c, str) or not ID.fullmatch(c) for c in claims):
            raise InputError("Invalid claim identifier")
        if len(claims) != len(set(claims)):
            raise InputError("Duplicate claim identifier within a source")
        if snapshot and (not isinstance(row["sha256"], str) or not HASH.fullmatch(row["sha256"])):
            raise InputError("Invalid SHA-256 digest")
        seen_ids.add(ident)
        seen_paths.add(path)
    return rows


def _digest(root, relative):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise InputError("Source root is not a directory")
    path = root
    for part in PurePosixPath(_path(relative)).parts:
        path = path / part
        if path.is_symlink():
            raise InputError("Symlinks are not accepted")
    if not path.resolve(strict=True).is_relative_to(root):
        raise InputError("Source is outside the root")
    if not stat.S_ISREG(path.stat().st_mode):
        raise InputError("Source is not a regular file")
    digest, total = hashlib.sha256(), 0
    with path.open("rb") as stream:
        before = path.stat()
        if before.st_size > MAX_FILE:
            raise InputError("Source exceeds 16 MiB")
        while chunk := stream.read(65_536):
            total += len(chunk)
            if total > MAX_FILE:
                raise InputError("Source exceeds 16 MiB")
            digest.update(chunk)
        after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns) or total != after.st_size:
        raise InputError("Source changed during observation")
    return digest.hexdigest()


def snapshot(manifest, root):
    rows = validate(manifest)
    observed = []
    for row in sorted(rows, key=lambda x: x["id"]):
        observed.append({**row, "claim_ids": sorted(row["claim_ids"]),
                         "sha256": _digest(root, row["path"])})
    return {"schema": SCHEMA, "observed_at": datetime.now(timezone.utc).isoformat(),
            "files": observed}


def check(baseline, root):
    rows = validate(baseline, snapshot=True)
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise InputError("Source root is not a directory")
    results, affected = [], set()
    for row in sorted(rows, key=lambda x: x["id"]):
        current, reason = None, None
        try:
            current = _digest(root, row["path"])
            status = "UNCHANGED_BYTES" if current == row["sha256"] else "CHANGED_BYTES"
        except (OSError, ValueError, RuntimeError):
            status, reason = "NOT_OBSERVED", "Missing, unreadable, unsafe or unstable source file"
        if status != "UNCHANGED_BYTES":
            affected.update(row["claim_ids"])
        results.append({"id": row["id"], "path": row["path"], "status": status,
                        "claim_ids": sorted(row["claim_ids"]), "baseline_sha256": row["sha256"],
                        "current_sha256": current, "reason": reason})
    return {"schema": SCHEMA, "observation": "RECHECK_REQUIRED" if affected else "UNCHANGED_BYTES",
            "affected_claim_ids": sorted(affected), "files": results,
            "limits": "Byte comparison of listed local files only; no source authentication, current-law check, legal conclusion or human-review declaration."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("snapshot", "check"))
    parser.add_argument("input", help="Manifest for snapshot; saved snapshot for check")
    parser.add_argument("--root", required=True, help="Trusted local directory containing source files")
    parser.add_argument("--output", help="Create a new JSON file; existing paths are never overwritten")
    args = parser.parse_args(argv)
    try:
        data = load_json(args.input)
        result = snapshot(data, args.root) if args.operation == "snapshot" else check(data, args.root)
        text = json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
        if args.output:
            with Path(args.output).open("x", encoding="utf-8") as stream:
                stream.write(text)
        else:
            sys.stdout.write(text)
        return 2 if result.get("observation") == "RECHECK_REQUIRED" else 0
    except (OSError, ValueError, RuntimeError, RecursionError):
        # Avoid exposing private absolute paths or untrusted terminal control text.
        sys.stderr.write("Input/output error: check JSON/schema, local paths, limits and new output destination.\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
