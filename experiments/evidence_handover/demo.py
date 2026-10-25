"""Generate an actual handover from fictional files in a disposable directory."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
from . import workflow as w

HERE = Path(__file__).resolve().parent


def run_demo():
    export = w.load(HERE / "fixtures" / "export.json", w.MAX_INPUT)
    with tempfile.TemporaryDirectory(prefix="regnav-handover-") as name:
        root = Path(name)
        for filename in ("fictional-report.txt", "fictional-statement.txt"):
            (root / filename).write_bytes((HERE / "fixtures" / filename).read_bytes())
        baseline = w.snapshot(export, root)
        before_export = copy.deepcopy(export)
        updated = copy.deepcopy(export)
        updated["records"][0]["scope"]["value"] = "125"
        updated["records"][0]["text"] = "FICTIONAL: reported Scope 1 emissions are 125 tCO2e for Facility A in 2025."
        (root / "fictional-report.txt").write_text("FICTIONAL REPORT v2: Scope 1 is 125 tCO2e; Scope 2 is 200 tCO2e.\n", encoding="utf-8")
        report = w.compare(baseline, updated, root)
        assert export == before_export
        assert report["source_watch"]["affected_claim_ids"] == ["claim1", "claim2"]
        assert [r["claim_id"] for r in report["field_changes"]] == ["claim1"]
        # Print a deterministic reviewer view; full CLI JSON also retains the export.
        fields = ("before_snapshot_id", "after_snapshot_id", "source_watch", "field_changes",
                  "process_observations", "attention", "coverage")
        return {"context": "Internal fictional demonstration; not a customer trial or professional review.",
                "view": "Selected actual report fields; not an operational snapshot.",
                "report": {key: report[key] for key in fields}}


if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2, ensure_ascii=True))
