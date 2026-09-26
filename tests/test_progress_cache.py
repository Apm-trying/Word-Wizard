"""Tests for the per-rerun progress cache added to learner.py (lag fix).

Verifies:
  - Multiple loads of the same nickname within one "rerun" hit Supabase once.
  - A save updates the cache in place, so a load right after a save in the
    same rerun sees the new data without a second network round trip.
  - reset_progress_cache() (called once per rerun in app.py) makes the next
    load fetch fresh again -- so a save from another session/device is
    picked up on the very next rerun, not stuck behind a stale cache.
  - The cache never hands back a reference callers can corrupt: mutating a
    loaded dict must not affect what a later load returns.

Run directly: python3 tests/test_progress_cache.py
"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import learner  # noqa: E402
from fakes import FakeSupabaseClient  # noqa: E402


def _fresh_client(monkeypatch_store):
    client = FakeSupabaseClient()
    monkeypatch_store["client"] = client
    learner._get_client = lambda: client
    return client


def test_repeated_load_within_one_rerun_hits_supabase_once():
    store = {}
    client = _fresh_client(store)
    client.seed("alice", {"xp": 40, "languages": {}, "word_status": {}})

    learner.reset_progress_cache()
    learner._load_user_progress("alice")
    learner._load_user_progress("alice")
    learner._load_user_progress("alice")

    assert client.select_calls == 1, client.select_calls


def test_save_updates_cache_so_next_load_same_rerun_is_free():
    store = {}
    client = _fresh_client(store)
    client.seed("bob", {"xp": 0, "languages": {}, "word_status": {}})

    learner.reset_progress_cache()
    progress = learner._load_user_progress("bob")
    assert client.select_calls == 1

    progress["xp"] = 999
    learner._save_user_progress("bob", progress)
    assert client.upsert_calls == 1

    reloaded = learner._load_user_progress("bob")
    assert client.select_calls == 1, "a load right after a save must not re-fetch"
    assert reloaded["xp"] == 999


def test_cache_reset_between_reruns_refetches():
    store = {}
    client = _fresh_client(store)
    client.seed("carol", {"xp": 5, "languages": {}, "word_status": {}})

    learner.reset_progress_cache()
    learner._load_user_progress("carol")
    assert client.select_calls == 1

    # Simulate the next Streamlit rerun.
    learner.reset_progress_cache()
    learner._load_user_progress("carol")
    assert client.select_calls == 2, "a fresh rerun must fetch again, not reuse a stale cache"


def test_save_from_elsewhere_is_visible_on_next_rerun():
    """Guards the deliberate per-rerun (not per-session) cache lifetime:
    if nickname 'dave' is saved by another device between reruns, this
    session's next rerun must see the new value, not a stale cached one."""
    store = {}
    client = _fresh_client(store)
    client.seed("dave", {"xp": 1, "languages": {}, "word_status": {}})

    learner.reset_progress_cache()
    first = learner._load_user_progress("dave")
    assert first["xp"] == 1

    # Someone else (a different device/session) updates Supabase directly,
    # bypassing this process's cache entirely.
    client.rows["dave"]["data"]["xp"] = 77

    # Still mid-rerun in *this* session -- would incorrectly see 77 if the
    # cache leaked in a way it shouldn't, but we haven't reloaded, so this
    # just documents that the cache doesn't proactively poll.
    learner.reset_progress_cache()
    second = learner._load_user_progress("dave")
    assert second["xp"] == 77


def test_loaded_dict_is_a_safe_copy_not_a_live_reference():
    store = {}
    client = _fresh_client(store)
    client.seed("erin", {"xp": 10, "languages": {}, "word_status": {}})

    learner.reset_progress_cache()
    progress = learner._load_user_progress("erin")
    progress["xp"] = 123456  # mutate the caller's copy

    progress_again = learner._load_user_progress("erin")
    assert progress_again["xp"] == 10, "mutating a loaded dict must not corrupt the cache"


def test_defaults_merge_still_works_for_legacy_records():
    """Old records missing newer fields (e.g. saved before the boss system
    existed) must still load without crashing -- unrelated to the cache,
    but this cache sits directly in front of that merge and must not skip
    it on a cache miss."""
    store = {}
    client = _fresh_client(store)
    client.seed("frank", {"xp": 20})  # no "languages"/"word_status" at all

    learner.reset_progress_cache()
    progress = learner._load_user_progress("frank")
    assert progress["languages"] == {}
    assert progress["word_status"] == {}
    assert progress["xp"] == 20


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
