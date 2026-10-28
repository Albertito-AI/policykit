"""Bounded JSON input and exclusive output utilities."""

from __future__ import annotations

import json
from pathlib import Path

MAX_JSON_BYTES = 16 * 1024 * 1024


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError(f"Non-finite JSON constant is not accepted: {value}")


def parse_json(text):
    return json.loads(text, object_pairs_hook=_unique, parse_constant=_reject_constant)


def read_json(path, *, max_bytes=MAX_JSON_BYTES):
    source = Path(path)
    if not source.is_file():
        raise ValueError("JSON input must be a regular file")
    with source.open("rb") as handle:
        data = handle.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError(f"JSON input exceeds {max_bytes} bytes")
    return parse_json(data.decode("utf-8-sig"))


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def write_new(path, content):
    """Never overwrite an existing output or a linked input."""
    target = Path(path)
    with target.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
