"""Run a fictional demonstration in a disposable directory. No network or credentials."""
import json
import tempfile
from pathlib import Path
from watch import SCHEMA, check, snapshot

with tempfile.TemporaryDirectory(prefix="regnav-watch-demo-") as directory:
    root = Path(directory)
    (root / "fictional-rule.txt").write_text("FICTIONAL TRAINING RULE: reply within five working days.\n", encoding="utf-8")
    manifest = {"schema": SCHEMA, "files": [
        {"id": "training-rule", "path": "fictional-rule.txt", "claim_ids": ["training-claim-1"]}
    ]}
    before = snapshot(manifest, root)
    assert check(before, root)["observation"] == "UNCHANGED_BYTES"
    (root / "fictional-rule.txt").write_text("FICTIONAL TRAINING RULE: reply within ten working days.\n", encoding="utf-8")
    print(json.dumps(check(before, root), indent=2))
