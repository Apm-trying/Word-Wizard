"""End-to-end smoke test: drives the real app.py through a full non-boss
question (idle ask-screen -> Yes -> quiz choice -> correct answer screen)
via AppTest, to catch any regression the word_display_html /
speaker_button_html / cache changes might have introduced into the normal
click-handling flow (XP awarded, no exceptions, word-card renders).

Run directly: python3 tests/test_full_quiz_flow_smoke.py
"""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import learner  # noqa: E402
from fakes import FakeSupabaseClient  # noqa: E402
from streamlit.testing.v1 import AppTest  # noqa: E402

APP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")
WORD_ID = 9  # "predictable" -- topic "politics", language "en"
TOPICS = ["politics"]


def _progress():
    return {
        "languages": {
            "en": {
                "current_word_id": WORD_ID,
                "assigned_at": datetime.now().isoformat(),
                "topics": sorted(TOPICS),
                "boss_active": False,
                "boss_hp": 0,
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


def test_full_non_boss_question_flow_no_exceptions_and_xp_awarded():
    nickname = "smoke_alice"
    client = FakeSupabaseClient()
    client.seed(nickname, _progress())
    learner._get_client = lambda: client

    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
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
    at.run()
    assert not at.exception, at.exception

    # Idle ask-screen: word-card with the speaker button should be present.
    markdown_html = "\n".join(m.value for m in at.markdown if hasattr(m, "value"))
    assert "predictable" in markdown_html
    assert "speaker-button" in markdown_html, "speaker button should render next to the word"

    # Click "Yes, I know it" -> should move into the quiz. (The word screen
    # also has nav icon buttons above it, so select by label, not index.)
    yes_button = next(b for b in at.button if "yes" in (b.label or "").lower())
    yes_button.click().run()
    assert not at.exception, at.exception
    assert at.session_state["quiz_active"] is True

    # Answer the quiz correctly.
    correct_index = at.session_state["quiz_correct_index"]
    correct_choice_text = at.session_state["quiz_choices"][correct_index]
    quiz_button = next(b for b in at.button if b.label == correct_choice_text)
    quiz_button.click().run()
    assert not at.exception, at.exception

    assert at.session_state["just_correct"] is True
    info = learner.get_level_info(nickname)
    assert info["xp"] == learner.XP_PER_CORRECT, info


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
