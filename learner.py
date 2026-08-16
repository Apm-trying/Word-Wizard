import json
import re
import random
from datetime import datetime, timedelta

WORDS_FILE = "words.json"
PROGRESS_FILE = "progress.json"
LOCK_HOURS = 12


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
        "topic": None,
        "word_status": {},  # word_id (as string) -> "known" | "unknown"
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


def _matches_filter(word, language, topic):
    if word["language"] != language:
        return False
    if topic != "all" and word["topic"] != topic:
        return False
    return True


def _pick_new_word(words, language, topic, word_status):
    candidates = [
        w for w in words
        if _matches_filter(w, language, topic) and str(w["id"]) not in word_status
    ]
    if not candidates:
        # Everything in this language/topic has been seen — recycle unknowns
        candidates = [
            w for w in words
            if _matches_filter(w, language, topic) and word_status.get(str(w["id"])) == "unknown"
        ]
    if not candidates:
        return None  # this person has learned every word in this language/topic combo!
    return random.choice(candidates)


def _assign_word(nickname, user_progress, word, language, topic, reset_skips=True):
    user_progress["current_word_id"] = word["id"] if word else None
    user_progress["assigned_at"] = datetime.now().isoformat()
    user_progress["language"] = language
    user_progress["topic"] = topic
    if reset_skips:
        user_progress["skips_used"] = 0
    _save_user_progress(nickname, user_progress)
    return word


def get_current_word(nickname, language, topic):
    """
    Returns the word this person should see right now, for their language/topic filter.
    Assigns a new one if none is set, the 12h window expired, or the filter changed.
    """
    words = load_words()
    user_progress = _load_user_progress(nickname)

    filter_changed = user_progress["language"] != language or user_progress["topic"] != topic

    if user_progress["current_word_id"] is None or filter_changed:
        new_word = _pick_new_word(words, language, topic, user_progress["word_status"])
        return _assign_word(nickname, user_progress, new_word, language, topic)

    assigned_at = datetime.fromisoformat(user_progress["assigned_at"])
    if datetime.now() - assigned_at >= timedelta(hours=LOCK_HOURS):
        new_word = _pick_new_word(words, language, topic, user_progress["word_status"])
        return _assign_word(nickname, user_progress, new_word, language, topic)

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
    other words in the same language. Returns (choices, correct_index).
    """
    words = load_words()
    other_words = [w for w in words if w["language"] == language and w["id"] != word["id"]]
    distractors = random.sample(other_words, min(2, len(other_words)))

    choice_items = [(word["definition"], True)] + [(d["definition"], False) for d in distractors]
    random.shuffle(choice_items)
    choices = [c[0] for c in choice_items]
    correct_index = next(i for i, c in enumerate(choice_items) if c[1])
    return choices, correct_index


def advance_word(nickname, language, topic):
    """
    Immediately assigns a new word — used after someone passes the
    verification quiz, since a correct answer proves they already know it.
    """
    words = load_words()
    user_progress = _load_user_progress(nickname)
    new_word = _pick_new_word(words, language, topic, user_progress["word_status"])
    return _assign_word(nickname, user_progress, new_word, language, topic)


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
