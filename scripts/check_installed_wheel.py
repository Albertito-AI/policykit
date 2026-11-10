"""Smoke-test the built wheel without importing code from the source checkout.

This is an engineering distribution test, not a release, user evaluation or
claim that optional source-tree experiments are available in the wheel.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"


def run(command, cwd, env=None):
    result = subprocess.run(
        [str(part) for part in command],
        cwd=cwd, env=env, text=True, capture_output=True,
        timeout=180, check=False,
    )
    if result.returncode:
        raise RuntimeError(
            "Command failed (exit {}): {}\nstdout:\n{}\nstderr:\n{}".format(
                result.returncode, " ".join(str(x) for x in command),
                result.stdout[-3000:], result.stderr[-3000:]
            )
        )
    return result.stdout


def main():
    with tempfile.TemporaryDirectory(prefix="regnav-installed-wheel-") as root_name:
        temporary = Path(root_name)
        outside = temporary / "outside-checkout"
        wheels_dir = temporary / "wheels"
        outside.mkdir()
        wheels_dir.mkdir()

        run([sys.executable, "-m", "pip", "wheel", "--no-deps",
             "--wheel-dir", wheels_dir, ROOT], outside)
        wheels = list(wheels_dir.glob("*.whl"))
        if len(wheels) != 1 or not wheels[0].name.startswith("regnav_workbench-"):
            raise RuntimeError("Expected exactly one versioned regnav-workbench wheel.")
        wheel = wheels[0]
        with zipfile.ZipFile(wheel) as archive:
            members = archive.namelist()
        required = {"regnav_evidence/__init__.py", "regnav_esg/__init__.py"}
        if not required.issubset(members):
            raise RuntimeError("The built wheel is missing a declared Python package.")
        metadata = [name for name in members if name.endswith(".dist-info/entry_points.txt")]
        if len(metadata) != 1:
            raise RuntimeError("Expected one wheel entry-point manifest.")
        excluded = ("experiments/", "tests/", "examples/", "regnav_expert/")
        if any(name.startswith(excluded) for name in members):
            raise RuntimeError("Source-only experiments, fixtures or tests entered the wheel.")
        if len(members) != len(set(members)):
            raise RuntimeError("Duplicate member in built wheel.")

        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        environment.pop("PYTHONHOME", None)
        environment["PYTHONNOUSERSITE"] = "1"
        run([sys.executable, "-m", "venv", temporary / "venv"], outside, environment)
        binary = temporary / "venv" / ("Scripts" if os.name == "nt" else "bin")
        python = binary / ("python.exe" if os.name == "nt" else "python")
        evidence = binary / ("regnav-evidence.exe" if os.name == "nt" else "regnav-evidence")
        esg = binary / ("regnav-esg.exe" if os.name == "nt" else "regnav-esg")
        run([python, "-m", "pip", "install", "--no-index", "--no-deps", wheel],
            outside, environment)

        # This command executes in a clean directory and verifies import origins.
        origin_check = (
            "import pathlib,sys,regnav_evidence,regnav_esg;"
            "root=pathlib.Path(sys.prefix).resolve();"
            "modules=(regnav_evidence,regnav_esg);"
            "assert all(root in pathlib.Path(x.__file__).resolve().parents for x in modules),"
            "'import escaped installed environment'"
        )
        run([python, "-c", origin_check], outside, environment)
        if VERSION not in run([evidence, "--version"], outside, environment):
            raise RuntimeError("Evidence console script has an unexpected version.")
        if VERSION not in run([esg, "--version"], outside, environment):
            raise RuntimeError("ESG console script has an unexpected version.")

        shutil.copyfile(ROOT / "examples" / "synthetic_ledger.json",
                        outside / "fictional-ledger.json")
        checked = json.loads(run(
            [evidence, "validate", "fictional-ledger.json", "--json"],
            outside, environment,
        ))
        if checked.get("structurally_valid") is not True or checked.get("error_count") != 0:
            raise RuntimeError("Installed ledger validator rejected the fictional fixture.")
        run([evidence, "report", "fictional-ledger.json", "--format", "markdown",
             "--output", "matrix.md"], outside, environment)
        if "Evidence matrix" not in (outside / "matrix.md").read_text(encoding="utf-8"):
            raise RuntimeError("Installed ledger report is incomplete.")

        (outside / "fictional.txt").write_text(
            "FICTIONAL sustainability source for package smoke testing.\n",
            encoding="utf-8",
        )
        run([esg, "ingest", "fictional.txt", "--output", "ingested.json"],
            outside, environment)
        if not isinstance(json.loads((outside / "ingested.json").read_text(encoding="utf-8")), dict):
            raise RuntimeError("Installed ESG command did not produce a JSON object.")

        digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
        print("Installed wheel:", wheel.name)
        print("Wheel bytes:", wheel.stat().st_size)
        print("Wheel SHA-256:", digest)
        print("Wheel members ({}):".format(len(members)))
        for name in sorted(members):
            print("  " + name)
        print("PASS: isolated installed-only console commands, imports and scope.")
        print("NOT TESTED: optional source-tree experiments or independent users.")


if __name__ == "__main__":
    main()
