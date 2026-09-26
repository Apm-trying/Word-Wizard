"""Regression tests confirming XP, level, rank-tier, boss mechanics and
daily-goal counting are byte-for-byte unchanged by this update. Per the
user's explicit hard constraint: "Do NOT change the existing XP, rank,
level, boss mechanics, or progression system during this update."

These exercise the real learner.py functions (through the progress cache,
same as production) against a fake Supabase backend -- nothing here
touches the actual XP/rank/boss formulas, it just pins their current
values/outputs so a future change would be caught.

Run directly: python3 tests/test_regression_progression.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import learner  # noqa: E402
from fakes import FakeSupabaseClient  # noqa: E402


def _client_for(nickname, data=None):
    client = FakeSupabaseClient()
    if data is not None:
        client.seed(nickname, data)
    learner._get_client = lambda: client
    learner.reset_progress_cache()
    return client


def test_xp_constants_unchanged():
    assert learner.XP_PER_CORRECT == 10
    assert learner.XP_REVIEW_BONUS == 3


def test_level_xp_curve_unchanged():
    assert learner.xp_required_for_level(0) == 50
    assert learner.xp_required_for_level(1) == 65
    assert learner.xp_required_for_level(10) == 200


def test_level_tiers_and_thresholds_unchanged():
    assert learner.LEVEL_TIERS == [
        (50, "archmage"),
        (40, "master_wizard"),
        (30, "wizard"),
        (20, "spellcaster"),
        (10, "apprentice"),
        (0, "beginner"),
    ]
    assert learner.get_level_tier(0) == "beginner"
    assert learner.get_level_tier(9) == "beginner"
    assert learner.get_level_tier(10) == "apprentice"
    assert learner.get_level_tier(20) == "spellcaster"
    assert learner.get_level_tier(30) == "wizard"
    assert learner.get_level_tier(40) == "master_wizard"
    assert learner.get_level_tier(50) == "archmage"
    assert learner.get_level_tier(999) == "archmage"


def test_boss_constants_unchanged():
    assert learner.BOSS_TRIGGER_CHANCE == 0.12
    assert learner.BOSS_MAX_HP == 5
    assert learner.BOSS_MAX_QUESTIONS == 5
    assert learner.BOSS_WIN_THRESHOLD == 3


def test_boss_bonus_xp_table_unchanged():
    assert learner.boss_bonus_xp(5) == 75  # perfect
    assert learner.boss_bonus_xp(3) == 50  # defeated (win threshold)
    assert learner.boss_bonus_xp(4) == 50  # defeated
    assert learner.boss_bonus_xp(2) == 0   # escaped
    assert learner.boss_bonus_xp(0) == 0


def test_score_correct_answer_awards_full_xp_for_new_word():
    _client_for("greta", {"xp": 0, "languages": {}, "word_status": {}})
    xp_awarded = learner.score_correct_answer("greta", 101)
    assert xp_awarded == learner.XP_PER_CORRECT == 10
    info = learner.get_level_info("greta")
    assert info["xp"] == 10


def test_score_correct_answer_awards_review_bonus_for_known_word():
    _client_for("hank", {"xp": 0, "languages": {}, "word_status": {"101": "known"}})
    xp_awarded = learner.score_correct_answer("hank", 101)
    assert xp_awarded == learner.XP_REVIEW_BONUS == 3


def test_daily_goal_only_counts_new_words_not_reviews():
    _client_for("iris", {
        "xp": 0, "languages": {}, "word_status": {"101": "known"},
        "daily_words_learned": 0, "daily_words_learned_date": None,
    })
    # Reviewing an already-known word must NOT bump the daily goal count.
    learner.score_correct_answer("iris", 101)
    count, _target = learner.get_daily_goal_progress("iris")
    assert count == 0, "reviewing a known word should not count toward the daily goal"

    # A genuinely new word must bump it by 1.
    learner.score_correct_answer("iris", 202)
    count, _target = learner.get_daily_goal_progress("iris")
    assert count == 1


def test_boss_defeat_thresholds_unchanged():
    for correct_count, expected in [(5, "perfect"), (4, "defeated"), (3, "defeated"), (2, "escaped"), (0, "escaped")]:
        nickname = f"boss_test_{correct_count}"
        data = {
            "xp": 0, "word_status": {},
            "languages": {"en": {
                "current_word_id": None, "assigned_at": None, "topics": None,
                "boss_active": True, "boss_hp": learner.BOSS_MAX_HP,
                "boss_correct_count": 0, "boss_questions_answered": 0,
            }},
        }
        _client_for(nickname, data)
        result = None
        for i in range(learner.BOSS_MAX_QUESTIONS):
            correct = i < correct_count
            result = learner.boss_hit(nickname, "en") if correct else learner.boss_miss(nickname, "en")
        assert result["finished"] is True
        assert result["result"] == expected, (correct_count, result)


def test_boss_hp_decreases_only_on_correct_hits():
    nickname = "boss_hp_check"
    data = {
        "xp": 0, "word_status": {},
        "languages": {"en": {
            "current_word_id": None, "assigned_at": None, "topics": None,
            "boss_active": True, "boss_hp": learner.BOSS_MAX_HP,
            "boss_correct_count": 0, "boss_questions_answered": 0,
        }},
    }
    _client_for(nickname, data)
    assert learner.get_boss_hp(nickname, "en") == 5
    learner.boss_miss(nickname, "en")
    assert learner.get_boss_hp(nickname, "en") == 5, "a miss must not drain boss HP"
    learner.boss_hit(nickname, "en")
    assert learner.get_boss_hp(nickname, "en") == 4, "a hit must drain boss HP by 1"


def test_perfect_boss_win_awards_correct_bonus_xp_on_top_of_base_xp():
    nickname = "boss_perfect_xp"
    data = {
        "xp": 100, "word_status": {},
        "languages": {"en": {
            "current_word_id": None, "assigned_at": None, "topics": None,
            "boss_active": True, "boss_hp": learner.BOSS_MAX_HP,
            "boss_correct_count": 0, "boss_questions_answered": 0,
        }},
    }
    _client_for(nickname, data)
    result = None
    for _ in range(learner.BOSS_MAX_QUESTIONS):
        result = learner.boss_hit(nickname, "en")
    assert result["result"] == "perfect"
    assert result["bonus_xp"] == 75
    info = learner.get_level_info(nickname)
    assert info["xp"] == 100 + 75


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
