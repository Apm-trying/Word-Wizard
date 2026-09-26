"""Runs every test module in this folder and prints a combined summary.

Must be run from the project root (relative to this file's parent), since
learner.py loads words.json via a relative path:
    python3 tests/run_all.py
"""
import os
import subprocess
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TESTS_DIR)

TEST_FILES = [
    "test_typography_and_speaker.py",
    "test_progress_cache.py",
    "test_regression_progression.py",
    "test_boss_entrance_timing.py",
    "test_full_quiz_flow_smoke.py",
]

if __name__ == "__main__":
    overall_ok = True
    for filename in TEST_FILES:
        path = os.path.join(TESTS_DIR, filename)
        print(f"\n=== {filename} ===")
        result = subprocess.run(
            [sys.executable, path],
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        print(result.stdout.strip())
        if result.returncode != 0:
            overall_ok = False
    print("\n" + ("ALL TESTS PASSED" if overall_ok else "SOME TESTS FAILED"))
    sys.exit(0 if overall_ok else 1)
