#!/usr/bin/env python3
"""Run fresh-process claims and negative controls; retain every run."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
import threading
import uuid

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments/001-reliable-tasks"
SPEC = json.loads((EXPERIMENT / "experiment.json").read_text())
REQUIRED = SPEC["measurements"]["required_exercise"]


def passes(result):
    return (set(result["claims"]) == set(REQUIRED)
            and all(result["claims"].values())
            and all(result["exercised"].get(name, 0) > 0 for name in REQUIRED))


def control_rejected(variant, result):
    expected = {
        "volatile": ("restart", "AssertionError: acknowledged task absent in fresh process"),
        "duplicates": ("concurrent_retry", "AssertionError: concurrent retries returned different IDs"),
    }
    scenario, reason = expected[variant]
    return (not passes(result)
            and all(result["exercised"].get(name, 0) > 0 for name in REQUIRED)
            and result["failures"].get(scenario) == reason)


def exercise(variant):
    command = [sys.executable, "-m", "tiny_tasks"] if variant == "sqlite" else [
        sys.executable, "lab/broken_tasks.py", "--mode", variant]
    result = {"claims": {}, "exercised": {}, "failures": {}, "trace": []}
    lock = threading.Lock()
    with TemporaryDirectory(prefix="edd-tasks-") as scratch:
        def call(db, *args):
            process = subprocess.run([*command, "--db", str(db), *args], cwd=ROOT,
                                     capture_output=True, text=True, timeout=20)
            payload = json.loads(process.stdout)
            with lock:
                result["trace"].append({"database": db.name, "arguments": list(args),
                                        "exit_code": process.returncode, "response": payload})
            return process.returncode, payload

        def add(db, title, key):
            status, response = call(db, "add", title, "--request-id", key)
            assert status == 0, "create did not succeed"
            return response

        def listing(db):
            status, response = call(db, "list")
            assert status == 0, "list did not succeed"
            return response["tasks"]

        def restart(db):
            for i in range(SPEC["measurements"]["restart_rounds"]):
                added = add(db, f"Task {i}", f"restart-{i}")
                rows = listing(db)
                result["exercised"]["restart"] += 1
                assert added["task"] in rows and len(rows) == i + 1, "acknowledged task absent in fresh process"

        def ignored_response_retry(db):
            # The caller ignores a successful acknowledgement; the process exits.
            add(db, "Water plants", "plant-1")
            retried = add(db, "Water plants", "plant-1")
            result["exercised"]["ignored_response_retry"] += 1
            assert retried["created"] is False, "retry reported another creation"
            assert listing(db) == [retried["task"]], "retry changed the stored task count or contents"

        def concurrent_retry(db):
            listing(db)  # Initialize schema before the concurrent workload.
            count = SPEC["measurements"]["concurrent_requests"]
            barrier = threading.Barrier(count)
            def worker(_):
                barrier.wait(timeout=10)
                return add(db, "Read a chapter", "book-1")
            with ThreadPoolExecutor(max_workers=count) as pool:
                replies = list(pool.map(worker, range(count)))
            result["exercised"]["concurrent_retry"] += count
            assert len({reply["task"]["id"] for reply in replies}) == 1, "concurrent retries returned different IDs"
            assert sum(reply["created"] for reply in replies) == 1, "concurrent retries created more than once"
            assert listing(db) == [replies[0]["task"]], "concurrent retries changed stored count or contents"

        def conflict(db):
            original = add(db, "Water plants", "same-key")
            status, response = call(db, "add", "Read a chapter", "--request-id", "same-key")
            result["exercised"]["conflict"] += 1
            assert status == 2 and response.get("error") == "conflict", "conflicting key was not rejected"
            assert listing(db) == [original["task"]], "conflicting retry changed saved data"

        def validation(db):
            status, response = call(db, "add", "   ", "--request-id", "blank")
            result["exercised"]["validation"] += 1
            assert status == 2 and response.get("error") == "invalid_input", "blank title was accepted"
            assert listing(db) == [], "invalid create added a task"

        for scenario in (restart, ignored_response_retry, concurrent_retry, conflict, validation):
            name = scenario.__name__
            result["exercised"][name] = 0
            try:
                scenario(Path(scratch) / f"{name}.sqlite")
                result["claims"][name] = True
            except Exception as error:
                result["claims"][name] = False
                result["failures"][name] = f"{type(error).__name__}: {error}"
    result["passed"] = passes(result)
    return result


def main():
    if not __debug__:
        raise SystemExit("Run without -O: this teaching harness uses Python assertions.")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    run = EXPERIMENT / "runs" / run_id
    run.mkdir(parents=True, exist_ok=False)
    def save(name, value):
        with (run / name).open("x") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
    sources = sorted([*ROOT.glob("tiny_tasks/*.py"), *ROOT.glob("lab/*.py"),
                      ROOT / "scripts/prove.py", EXPERIMENT / "experiment.json"])
    hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    save("manifest.json", {"python": platform.python_version(), "sqlite": sqlite3.sqlite_version,
                           "source_sha256": hashes, "command": "python3 scripts/prove.py"})
    results = {}
    for variant in ("volatile", "duplicates", "sqlite"):
        repeats = [exercise(variant) for _ in range(SPEC["measurements"]["independent_repeats"])]
        for i, result in enumerate(repeats, 1):
            save(f"{variant}-{i}.json", result)
        stable = all((r["claims"], r["exercised"]) == (repeats[0]["claims"], repeats[0]["exercised"]) for r in repeats)
        results[variant] = {"passed": all(r["passed"] for r in repeats), "stable": stable,
                            "claims": repeats[0]["claims"], "exercised": repeats[0]["exercised"]}
        if variant != "sqlite":
            results[variant]["targeted_control_verified"] = all(control_rejected(variant, r) for r in repeats)
    empty = {"claims": {name: True for name in REQUIRED}, "exercised": {name: 0 for name in REQUIRED}}
    gate = (results["sqlite"]["passed"] and all(r["stable"] for r in results.values())
            and all(r["targeted_control_verified"] for v, r in results.items() if v != "sqlite")
            and not passes(empty))
    summary = {"run_id": run_id, "promotion_gate_passed": gate, "variants": results,
               "zero_exercise_rejected": not passes(empty), "independent_repeats": SPEC["measurements"]["independent_repeats"],
               "scope": SPEC["scope"]}
    save("summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("Evidence:", run.relative_to(ROOT))
    return 0 if gate else 1


if __name__ == "__main__":
    raise SystemExit(main())
