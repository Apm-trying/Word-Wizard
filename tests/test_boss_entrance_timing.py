"""Tests for the boss-entrance timing gate added to app.py (task #18).

Verifies, by driving the real app.py through Streamlit's AppTest:
  - When a boss encounter's idle ask-screen renders for the first time,
    time.sleep is called exactly once with a value in the requested
    1.2-1.5s window.
  - On a later rerun of the *same* still-active boss encounter, the sleep
    does NOT fire again (boss_entrance_shown gates it to once).
  - When no boss is active, the sleep never fires at all.

Rather than monkeypatching time.sleep (which would also intercept
Streamlit's/AppTest's own internal sleeps and produce false readings),
this measures real wall-clock duration around each at.run() call. The
sleep is short (~1.3s) so the whole file takes a few seconds to run.

Run directly: python3 tests/test_boss_entrance_timing.py
"""
import os
import sys
import time as time_module
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import learner  # noqa: E402
from fakes import FakeSupabaseClient  # noqa: E402
from streamlit.testing.v1 import AppTest  # noqa: E402

APP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")

WORD_ID = 9  # "predictable", topic "politics", language "en" -- see words.json
TOPICS = ["politics"]


def _progress_with_boss(boss_active):
    return {
        "languages": {
            "en": {
                "current_word_id": WORD_ID,
                "assigned_at": datetime.now().isoformat(),
                "topics": sorted(TOPICS),
                "boss_active": boss_active,
                "boss_hp": 5 if boss_active else 0,
                "boss_correct_count": 0,
                "boss_questions_answered": 0,
            }
        },
        "word_status": {},
        "xp": 0,
        "streak": 0,
        "last_active_date": None,
        "daily_words_learned": 0,
        "daily_words_learned_date": None,
    }


def _make_test(nickname, boss_active):
    client = FakeSupabaseClient()
    client.seed(nickname, _progress_with_boss(boss_active))
    learner._get_client = lambda: client

    at = AppTest.from_file(APP_PATH, default_timeout=30)

    at.run()  # first run just to create session_state slots; values overwritten below
    at.session_state["setup_stage"] = "done"
    at.session_state["nickname"] = nickname
    at.session_state["topics"] = TOPICS
    at.session_state["language"] = "en"
    at.session_state["revealed"] = False
    at.session_state["quiz_active"] = False
    at.session_state["just_correct"] = False
    at.session_state["boss_outcome"] = None
    at.session_state["boss_entrance_shown"] = False
    at.session_state["rank_up_info"] = None
    at.session_state["level_up_info"] = None
    return at


def test_boss_entrance_sleeps_once_within_requested_window():
    at = _make_test("timing_alice", boss_active=True)

    start = time_module.perf_counter()
    at.run()
    elapsed = time_module.perf_counter() - start

    assert not at.exception, at.exception
    assert 1.2 <= elapsed <= 3.0, f"expected a ~1.2-1.5s hold, took {elapsed:.3f}s"


def test_boss_entrance_does_not_resleep_on_later_rerun_same_encounter():
    at = _make_test("timing_bob", boss_active=True)

    start = time_module.perf_counter()
    at.run()
    first_elapsed = time_module.perf_counter() - start
    assert not at.exception, at.exception
    assert first_elapsed >= 1.2, f"first render should hold ~1.2-1.5s, took {first_elapsed:.3f}s"

    # Simulate an ordinary rerun of the same still-active encounter (e.g.
    # some widget interaction caused a rerun without the encounter ending).
    # boss_entrance_shown is still True in session_state at this point.
    start = time_module.perf_counter()
    at.run()
    second_elapsed = time_module.perf_counter() - start

    assert not at.exception, at.exception
    assert second_elapsed < 1.0, (
        f"must not sleep again on a rerun of the same encounter, took {second_elapsed:.3f}s"
    )


def test_no_sleep_when_no_boss_active():
    at = _make_test("timing_carol", boss_active=False)

    start = time_module.perf_counter()
    at.run()
    elapsed = time_module.perf_counter() - start

    assert not at.exception, at.exception
    assert elapsed < 1.0, f"no boss active, should not hold at all, took {elapsed:.3f}s"


ALL_TESTS = [v for k, v in list(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    failures = []
    for test in ALL_TESTS:
        try:
            test()
            print(f"PASS  {test.__name__}")
        except Exception as e:  # noqa: BLE001
            failures.append(test.__name__)
            print(f"FAIL  {test.__name__}: {e}")
    print(f"\n{len(ALL_TESTS) - len(failures)}/{len(ALL_TESTS)} passed")
    if failures:
        sys.exit(1)
