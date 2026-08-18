import json
import re
import random
from datetime import datetime, timedelta

WORDS_FILE = "words.json"
PROGRESS_FILE = "progress.json"
LOCK_HOURS = 2
XP_PER_CORRECT = 10
XP_REVIEW_BONUS = 3  # smaller reward for correctly reviewing an already-known word


def xp_required_for_level(level):
    """
    How much XP it takes to go from `level` to `level + 1`.
    Grows with level, so early levels come fast and later ones take real effort.
    """
    return 50 + level * 15

# Ordered highest-first so we can find the first tier the level qualifies for.
LEVEL_TIERS = [
    (50, "wizard_king"),
    (40, "wizard"),
    (30, "archmage"),
    (20, "magician"),
    (10, "novice"),
    (0, "beginner"),
]


def sanitize_nickname(raw_nickname):
    """
    Turns whatever someone typed into a safe key for storing their progress.
    Lowercase, letters/numbers/dash/underscore only, max 30 chars.
    Returns None if nothing usable was entered.
    """
    cleaned = re.sub(r"[^a-z0-9_-]", "", raw_nickname.strip().lower().replace(" ", "_"))
    cleaned = cleaned[:30]
    return cleaned if cleaned else None


def load_words():
    with open(WORDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_all_progress():
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def _save_all_progress(all_progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_progress, f, ensure_ascii=False, indent=2)


def _load_user_progress(nickname):
    all_progress = _load_all_progress()
    defaults = {
        "current_word_id": None,
        "assigned_at": None,
        "language": None,
        "topics": None,  # list of topic keys, e.g. ["politics", "economy"]
        "word_status": {},  # word_id (as string) -> "known" | "unknown"
        "xp": 0,
    }
    defaults.update(all_progress.get(nickname, {}))
    return defaults


def _save_user_progress(nickname, user_progress):
    all_progress = _load_all_progress()
    all_progress[nickname] = user_progress
    _save_all_progress(all_progress)


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
    user_progress["current_word_id"] = word["id"] if word else None
    user_progress["assigned_at"] = datetime.now().isoformat()
    user_progress["language"] = language
    user_progress["topics"] = sorted(topics)
    _save_user_progress(nickname, user_progress)
    return word


def get_current_word(nickname, language, topics):
    """
    Returns the word this person should see right now, for their language/topics filter.
    Assigns a new one if none is set, the 12h window expired, or the filter changed.
    """
    words = load_words()
    user_progress = _load_user_progress(nickname)

    filter_changed = (
        user_progress["language"] != language
        or user_progress["topics"] != sorted(topics)
    )

    if user_progress["current_word_id"] is None or filter_changed:
        new_word = _pick_new_word(words, language, topics, user_progress["word_status"])
        return _assign_word(nickname, user_progress, new_word, language, topics)

    assigned_at = datetime.fromisoformat(user_progress["assigned_at"])
    if datetime.now() - assigned_at >= timedelta(hours=LOCK_HOURS):
        new_word = _pick_new_word(words, language, topics, user_progress["word_status"])
        return _assign_word(nickname, user_progress, new_word, language, topics)

    current = next((w for w in words if w["id"] == user_progress["current_word_id"]), None)
    return current


def mark_status(nickname, word_id, status):
    """status should be 'known' or 'unknown'. Recorded for this person only."""
    user_progress = _load_user_progress(nickname)
    user_progress["word_status"][str(word_id)] = status
    _save_user_progress(nickname, user_progress)


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


def advance_word(nickname, language, topics):
    """
    Immediately assigns a new word — used after someone passes the
    verification quiz, since a correct answer proves they already know it.
    """
    words = load_words()
    user_progress = _load_user_progress(nickname)
    new_word = _pick_new_word(words, language, topics, user_progress["word_status"])
    return _assign_word(nickname, user_progress, new_word, language, topics)


def get_time_remaining(nickname):
    """
    Returns (remaining_seconds, percent_elapsed) for this person's current 12h lock window.
    """
    user_progress = _load_user_progress(nickname)
    if not user_progress["assigned_at"]:
        return 0, 0.0

    assigned_at = datetime.fromisoformat(user_progress["assigned_at"])
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


def get_leaderboard(limit=20):
    """
    Returns everyone's nickname/level/tier/xp, ranked highest XP first.
    Reads straight from shared progress storage — no per-user call needed.
    """
    all_progress = _load_all_progress()
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