import json
import re
import random
import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta

WORDS_FILE = "words.json"
LOCK_HOURS = 2
XP_PER_CORRECT = 10
XP_REVIEW_BONUS = 3  # smaller reward for correctly reviewing an already-known word

# Random boss encounters — a rare, higher-stakes detour from the normal loop
BOSS_TRIGGER_CHANCE = 0.12  # ~12% chance on each new word, when no boss is already active
BOSS_MAX_HP = 5
BOSS_MAX_QUESTIONS = 5  # always exactly 5 questions — outcome decided only after the 5th
BOSS_WIN_THRESHOLD = 3  # 3 or more correct out of 5 = defeated


def boss_bonus_xp(correct_count):
    """Tiered bonus XP by final result: 0-2 correct = escaped (no bonus),
    3-4 = defeated, 5 = Perfect Victory."""
    if correct_count >= BOSS_MAX_QUESTIONS:
        return 75
    elif correct_count >= BOSS_WIN_THRESHOLD:
        return 50
    else:
        return 0


def xp_required_for_level(level):
    """
    How much XP it takes to go from `level` to `level + 1`.
    Grows with level, so early levels come fast and later ones take real effort.
    """
    return 50 + level * 15

# Ordered highest-first so we can find the first tier the level qualifies for.
LEVEL_TIERS = [
    (50, "archmage"),
    (40, "master_wizard"),
    (30, "wizard"),
    (20, "spellcaster"),
    (10, "apprentice"),
    (0, "beginner"),
]


def sanitize_nickname(raw_nickname):
    """
    Turns whatever someone typed into a safe key for storing their progress.
    Lowercase, letters/numbers/dash/underscore only (including Norwegian
    æøå), max 30 chars. Returns None if nothing usable was entered.
    """
    cleaned = re.sub(r"[^a-z0-9æøå_-]", "", raw_nickname.strip().lower().replace(" ", "_"))
    cleaned = cleaned[:30]
    return cleaned if cleaned else None


# Add any extra words you want blocked here (lowercase, no spaces needed —
# substring matching catches them either way). Kept separate from the
# better-profanity library's built-in list so you can extend it yourself,
# e.g. for Norwegian-specific terms, without digging through library internals.
CUSTOM_BLOCKED_TERMS = set()


def is_nickname_allowed(raw_nickname):
    """
    Checks the ORIGINAL input (before spaces become underscores) for
    profanity or slurs — word-boundary detection works better before that
    conversion happens. Uses the better-profanity library for broad
    coverage, plus CUSTOM_BLOCKED_TERMS above for anything you add yourself.
    """
    from better_profanity import profanity
    if profanity.contains_profanity(raw_nickname):
        return False
    lowered = raw_nickname.lower()
    if any(term in lowered for term in CUSTOM_BLOCKED_TERMS):
        return False
    return True


def load_words():
    with open(WORDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_resource
def _get_client():
    """
    One Supabase client shared across reruns (st.cache_resource keeps it
    alive between script runs instead of reconnecting every time).
    """
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


def _load_user_progress(nickname):
    defaults = {
        "languages": {},  # lang code -> {"current_word_id":, "assigned_at":, "topics":}
        "word_status": {},  # word_id (as string) -> "known" | "unknown" — shared across languages
        "xp": 0,
        "streak": 0,
        "last_active_date": None,  # ISO date string, e.g. "2026-08-30"
    }
    client = _get_client()
    result = client.table("progress").select("data").eq("nickname", nickname).execute()
    if result.data:
        defaults.update(result.data[0]["data"])
    if "languages" not in defaults or not isinstance(defaults["languages"], dict):
        defaults["languages"] = {}
    return defaults


def _get_lang_state(user_progress, language):
    """
    Returns this language's state, filling in any missing fields with
    defaults. Handles both a language never touched before AND an existing
    record saved by older code that predates a field (e.g. accounts that
    played before the boss system existed won't have boss_active/boss_hp/
    boss_misses stored yet) — without this, existing users would crash.
    """
    defaults = {
        "current_word_id": None, "assigned_at": None, "topics": None,
        "boss_active": False, "boss_hp": 0,
        "boss_correct_count": 0, "boss_questions_answered": 0,
    }
    stored = user_progress["languages"].get(language, {})
    merged = dict(defaults)
    merged.update(stored)
    return merged


def _save_user_progress(nickname, user_progress):
    client = _get_client()
    client.table("progress").upsert({"nickname": nickname, "data": user_progress}).execute()


def _get_all_progress():
    """Returns {nickname: progress_dict} for everyone — used by the leaderboard and admin panel."""
    client = _get_client()
    result = client.table("progress").select("nickname, data").execute()
    return {row["nickname"]: row["data"] for row in result.data}


def pick_guest_word(language, topics):
    """
    Picks a random word for someone who hasn't named themselves yet —
    no progress history to check against, since none exists.
    """
    words = load_words()
    return _pick_new_word(words, language, topics, {})


def get_topics_for_language(language):
    """Returns the sorted list of distinct topics available for a given language."""
    words = load_words()
    topics = {w["topic"] for w in words if w["language"] == language}
    return sorted(topics)


def _matches_filter(word, language, topics):
    return word["language"] == language and word["topic"] in topics


def _pick_new_word(words, language, topics, word_status):
    candidates = [
        w for w in words
        if _matches_filter(w, language, topics) and str(w["id"]) not in word_status
    ]
    if not candidates:
        # Everything's been seen — recycle unknowns first, they need it most
        candidates = [
            w for w in words
            if _matches_filter(w, language, topics) and word_status.get(str(w["id"])) == "unknown"
        ]
    if not candidates:
        # Everything is known — bring back known words for spaced review
        # instead of hitting a dead end
        candidates = [
            w for w in words
            if _matches_filter(w, language, topics) and word_status.get(str(w["id"])) == "known"
        ]
    if not candidates:
        return None  # this filter genuinely has zero matching words
    return random.choice(candidates)


def _assign_word(nickname, user_progress, word, language, topics):
    existing = _get_lang_state(user_progress, language)
    user_progress["languages"][language] = {
        "current_word_id": word["id"] if word else None,
        "assigned_at": datetime.now().isoformat(),
        "topics": sorted(topics),
        "boss_active": existing["boss_active"],
        "boss_hp": existing["boss_hp"],
        "boss_correct_count": existing["boss_correct_count"],
        "boss_questions_answered": existing["boss_questions_answered"],
    }
    _save_user_progress(nickname, user_progress)
    maybe_trigger_boss(nickname, language)
    return word


def get_current_word(nickname, language, topics):
    """
    Returns the word this person should see right now, for their language/topics filter.
    Each language tracks its own current word and lock timer independently —
    switching languages resumes wherever that language was, it doesn't reset anything.
    Assigns a new word if none is set for this language, the lock window expired,
    or the topic filter changed.
    """
    words = load_words()
    user_progress = _load_user_progress(nickname)
    lang_state = _get_lang_state(user_progress, language)

    filter_changed = lang_state["topics"] != sorted(topics)

    if lang_state["current_word_id"] is None or filter_changed:
        new_word = _pick_new_word(words, language, topics, user_progress["word_status"])
        return _assign_word(nickname, user_progress, new_word, language, topics)

    assigned_at = datetime.fromisoformat(lang_state["assigned_at"])
    if datetime.now() - assigned_at >= timedelta(hours=LOCK_HOURS):
        new_word = _pick_new_word(words, language, topics, user_progress["word_status"])
        return _assign_word(nickname, user_progress, new_word, language, topics)

    current = next((w for w in words if w["id"] == lang_state["current_word_id"]), None)
    return current


def _update_streak(nickname):
    """
    Bumps a person's daily streak. One calendar day answered = streak day.
    Answering again same day doesn't double-count; missing a day resets to 1.
    """
    user_progress = _load_user_progress(nickname)
    today = datetime.now().date().isoformat()
    last_date = user_progress.get("last_active_date")

    if last_date == today:
        return  # already counted today
    if last_date is not None:
        gap_days = (datetime.fromisoformat(today) - datetime.fromisoformat(last_date)).days
        if gap_days == 1:
            user_progress["streak"] = user_progress.get("streak", 0) + 1
        else:
            user_progress["streak"] = 1
    else:
        user_progress["streak"] = 1

    user_progress["last_active_date"] = today
    _save_user_progress(nickname, user_progress)


def get_streak(nickname):
    return _load_user_progress(nickname).get("streak", 0)


def mark_status(nickname, word_id, status):
    """status should be 'known' or 'unknown'. Recorded for this person only."""
    user_progress = _load_user_progress(nickname)
    user_progress["word_status"][str(word_id)] = status
    _save_user_progress(nickname, user_progress)
    _update_streak(nickname)


def get_word_status(nickname, word_id):
    user_progress = _load_user_progress(nickname)
    return user_progress["word_status"].get(str(word_id))


def get_quiz_choices(word, language):
    """
    Builds a 3-option multiple choice quiz for verifying someone actually
    knows this word: the real definition plus 2 distractors pulled from
    OTHER WORDS IN THE SAME TOPIC (so the choices are genuinely similar,
    not obviously different subjects). Falls back to any topic in the same
    language if that topic doesn't have enough other words yet.
    Returns (choices, correct_index).
    """
    words = load_words()
    same_topic = [
        w for w in words
        if w["language"] == language and w["topic"] == word["topic"] and w["id"] != word["id"]
    ]
    if len(same_topic) >= 2:
        pool = same_topic
    else:
        pool = [w for w in words if w["language"] == language and w["id"] != word["id"]]

    distractors = random.sample(pool, min(2, len(pool)))

    choice_items = [(word["definition"], True)] + [(d["definition"], False) for d in distractors]
    random.shuffle(choice_items)
    choices = [c[0] for c in choice_items]
    correct_index = next(i for i, c in enumerate(choice_items) if c[1])
    return choices, correct_index


def lock_guest_word(nickname, word, language, topics):
    """
    Explicitly locks a word as this person's current word for a language,
    starting the wait timer now. Needed specifically for the guest flow:
    a word picked before someone has a name was never assigned through
    the normal per-user tracking, so without this, naming yourself after
    answering wrong would accidentally skip the lock entirely and hand
    you a free new word instead of making you wait.
    """
    user_progress = _load_user_progress(nickname)
    return _assign_word(nickname, user_progress, word, language, topics)


def is_boss_active(nickname, language):
    user_progress = _load_user_progress(nickname)
    return _get_lang_state(user_progress, language)["boss_active"]


def get_boss_hp(nickname, language):
    user_progress = _load_user_progress(nickname)
    return _get_lang_state(user_progress, language)["boss_hp"]


def get_boss_misses(nickname, language):
    user_progress = _load_user_progress(nickname)
    lang_state = _get_lang_state(user_progress, language)
    return lang_state["boss_questions_answered"] - lang_state["boss_correct_count"]


def maybe_trigger_boss(nickname, language):
    """
    Rolls a random chance to start a boss encounter when a new word is
    assigned, but only if one isn't already active. Returns True if a
    boss encounter just started.
    """
    user_progress = _load_user_progress(nickname)
    lang_state = _get_lang_state(user_progress, language)
    if lang_state["boss_active"]:
        return False
    if random.random() < BOSS_TRIGGER_CHANCE:
        lang_state["boss_active"] = True
        lang_state["boss_hp"] = BOSS_MAX_HP
        lang_state["boss_correct_count"] = 0
        lang_state["boss_questions_answered"] = 0
        user_progress["languages"][language] = lang_state
        _save_user_progress(nickname, user_progress)
        return True
    return False


def get_boss_question_number(nickname, language):
    """Which question number (1-based, up to BOSS_MAX_QUESTIONS) is currently being asked."""
    user_progress = _load_user_progress(nickname)
    lang_state = _get_lang_state(user_progress, language)
    return lang_state["boss_questions_answered"] + 1


def _register_boss_answer(nickname, language, correct):
    """
    Records one answer during the 5-question boss encounter. Always exactly
    5 questions are asked — a wrong answer never ends the encounter early or
    costs XP already earned; it just doesn't count toward defeating the boss.
    The outcome (defeated / perfect / escaped) is only decided after the 5th.

    Returns a dict: {"finished", "question_number", "correct_so_far",
    "result" (None until finished, then "defeated"/"perfect"/"escaped"),
    "bonus_xp"}.
    """
    user_progress = _load_user_progress(nickname)
    lang_state = _get_lang_state(user_progress, language)

    lang_state["boss_questions_answered"] += 1
    if correct:
        lang_state["boss_correct_count"] += 1
        lang_state["boss_hp"] = max(0, BOSS_MAX_HP - lang_state["boss_correct_count"])

    question_number = lang_state["boss_questions_answered"]
    finished = question_number >= BOSS_MAX_QUESTIONS
    result = None
    bonus_xp = 0

    if finished:
        correct_count = lang_state["boss_correct_count"]
        bonus_xp = boss_bonus_xp(correct_count)
        if correct_count >= BOSS_MAX_QUESTIONS:
            result = "perfect"
        elif correct_count >= BOSS_WIN_THRESHOLD:
            result = "defeated"
        else:
            result = "escaped"
        lang_state["boss_active"] = False
        if bonus_xp:
            user_progress["xp"] = user_progress.get("xp", 0) + bonus_xp

    user_progress["languages"][language] = lang_state
    _save_user_progress(nickname, user_progress)

    return {
        "finished": finished,
        "question_number": question_number,
        "correct_so_far": lang_state["boss_correct_count"],
        "result": result,
        "bonus_xp": bonus_xp,
    }


def boss_hit(nickname, language):
    """Registers one correct answer during a boss encounter. See _register_boss_answer."""
    return _register_boss_answer(nickname, language, correct=True)


def boss_miss(nickname, language):
    """Registers one wrong answer during a boss encounter. See _register_boss_answer."""
    return _register_boss_answer(nickname, language, correct=False)


def advance_word(nickname, language, topics):
    """
    Immediately assigns a new word — used after someone passes the
    verification quiz, since a correct answer proves they already know it.
    """
    words = load_words()
    user_progress = _load_user_progress(nickname)
    new_word = _pick_new_word(words, language, topics, user_progress["word_status"])
    return _assign_word(nickname, user_progress, new_word, language, topics)


def get_time_remaining(nickname, language):
    """
    Returns (remaining_seconds, percent_elapsed) for this person's lock window
    in the given language specifically (each language has its own timer).
    """
    user_progress = _load_user_progress(nickname)
    lang_state = _get_lang_state(user_progress, language)
    if not lang_state["assigned_at"]:
        return 0, 0.0

    assigned_at = datetime.fromisoformat(lang_state["assigned_at"])
    elapsed = (datetime.now() - assigned_at).total_seconds()
    total = LOCK_HOURS * 3600
    remaining = max(0, total - elapsed)
    percent = min(100.0, (elapsed / total) * 100)
    return remaining, percent


def score_correct_answer(nickname, word_id):
    """
    Marks a word as known and awards XP for a correct quiz answer.
    Full XP the first time; a smaller review bonus if this word was
    already known (i.e. this is a spaced-repetition review, not new learning).
    Returns the XP amount actually awarded, for display.
    """
    was_already_known = get_word_status(nickname, word_id) == "known"
    mark_status(nickname, word_id, "known")
    amount = XP_REVIEW_BONUS if was_already_known else XP_PER_CORRECT
    award_xp(nickname, amount)
    return amount


def award_xp(nickname, amount=XP_PER_CORRECT):
    """Adds XP for this person (called on a correct quiz answer). Returns new total."""
    user_progress = _load_user_progress(nickname)
    user_progress["xp"] = user_progress.get("xp", 0) + amount
    _save_user_progress(nickname, user_progress)
    return user_progress["xp"]


def get_level_tier(level):
    for threshold, tier in LEVEL_TIERS:
        if level >= threshold:
            return tier
    return "beginner"


def _level_from_xp(xp):
    """Walks the increasing XP curve to find (level, xp_into_current_level)."""
    level = 0
    remaining = xp
    while remaining >= xp_required_for_level(level):
        remaining -= xp_required_for_level(level)
        level += 1
    return level, remaining


def get_level_info(nickname):
    """Returns a dict with xp, level, tier (a title key), and progress into the current level."""
    user_progress = _load_user_progress(nickname)
    xp = user_progress.get("xp", 0)
    level, xp_into_level = _level_from_xp(xp)
    return {
        "xp": xp,
        "level": level,
        "tier": get_level_tier(level),
        "xp_into_level": xp_into_level,
        "xp_for_next": xp_required_for_level(level),
    }


def get_words_by_status(nickname, language, status):
    """
    Returns this person's words with the given status ('known' or 'unknown'),
    filtered to the current language. Used for the trophy room / graveyard.
    """
    words = load_words()
    user_progress = _load_user_progress(nickname)
    word_status = user_progress["word_status"]
    matching_ids = {int(wid) for wid, s in word_status.items() if s == status}
    return [w for w in words if w["id"] in matching_ids and w["language"] == language]


def user_exists(nickname):
    """Checks whether this nickname already has progress saved (a returning user)."""
    client = _get_client()
    result = client.table("progress").select("nickname").eq("nickname", nickname).execute()
    return len(result.data) > 0


def delete_user(nickname):
    """Permanently removes a person's progress entirely (used by the admin panel)."""
    client = _get_client()
    client.table("progress").delete().eq("nickname", nickname).execute()
    return True


def get_leaderboard(limit=20):
    """
    Returns everyone's nickname/level/tier/xp, ranked highest XP first.
    Reads straight from shared progress storage — no per-user call needed.
    """
    all_progress = _get_all_progress()
    entries = []
    for nickname, prog in all_progress.items():
        xp = prog.get("xp", 0)
        level, _ = _level_from_xp(xp)
        entries.append({
            "nickname": nickname,
            "xp": xp,
            "level": level,
            "tier": get_level_tier(level),
        })
    entries.sort(key=lambda e: e["xp"], reverse=True)
    return entries[:limit]
