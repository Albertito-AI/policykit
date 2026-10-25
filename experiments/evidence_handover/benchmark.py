"""Run the eighteen disclosed synthetic acceptance cases and emit actual results."""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
from pathlib import Path
import platform
import unittest

ROOT = Path(__file__).resolve().parents[2]
TEST_FILE = ROOT / "tests" / "test_evidence_handover.py"


def run():
    spec = importlib.util.spec_from_file_location("handover_acceptance_tests", TEST_FILE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    names = sorted(n for n in unittest.defaultTestLoader.getTestCaseNames(module.HandoverTests)
                   if n.startswith("test_B"))
    if [n.split("_")[1] for n in names] != [f"B{i:02d}" for i in range(1, 19)]:
        raise RuntimeError("The eighteen specified cases must be present exactly once")
    observations = []
    for name in names:
        result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(module.HandoverTests(name))
        state = "ERROR" if result.errors else "FAIL" if result.failures else "SKIPPED" if result.skipped else "PASS"
        observations.append({"id": name.split("_")[1], "test": name, "status": state})
    files = [ROOT / "experiments" / "evidence_handover" / x for x in
             ("workflow.py", "cli.py", "server.py", "demo.py", "benchmark.py")]
    files.append(TEST_FILE)
    return {"kind": "internal_synthetic_engineering_benchmark", "python": platform.python_version(),
            "independent_participants": None, "professional_reference_validation": "NOT_PERFORMED",
            "limits": "Disclosed cases test software behaviour, not blind generalisation, professional assurance or productivity.",
            "files_sha256": {str(p.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
            "case_count": len(observations), "passed": sum(r["status"] == "PASS" for r in observations),
            "cases": observations}


if __name__ == "__main__":
    report = run()
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["passed"] == report["case_count"] else 1)
