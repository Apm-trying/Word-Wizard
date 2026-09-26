"""Unit tests for styles.word_display_html and styles.speaker_button_html.
Run directly: python3 tests/test_typography_and_speaker.py
"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import styles  # noqa: E402


def test_short_word_gets_no_size_class():
    html = styles.word_display_html("cat")
    assert html == '<div class="word-display">cat</div>', html


def test_boundary_12_chars_is_still_normal():
    word = "abcdefghijkl"  # 12 chars
    assert len(word) == 12
    html = styles.word_display_html(word)
    assert 'class="word-display"' in html and "word-display-" not in html, html


def test_13_chars_steps_to_md():
    word = "abcdefghijklm"  # 13 chars
    assert len(word) == 13
    html = styles.word_display_html(word)
    assert "word-display-md" in html, html


def test_17_chars_is_still_md():
    word = "a" * 17
    html = styles.word_display_html(word)
    assert "word-display-md" in html, html


def test_18_chars_steps_to_sm():
    word = "a" * 18
    html = styles.word_display_html(word)
    assert "word-display-sm" in html, html


def test_real_longest_words_from_word_list():
    # Longest real entries found in words.json at audit time (17 chars each
    # -- lands in the md step, not sm; see the 18-char boundary test above
    # for where sm actually kicks in).
    for word in ("multikulturalisme", "interoperabilitet"):
        assert len(word) == 17
        html = styles.word_display_html(word)
        assert "word-display-md" in html, (word, html)
        assert word in html


def test_word_text_is_not_mangled():
    html = styles.word_display_html("ordinary")
    assert "ordinary" in html


def test_speaker_button_default_language_fallback():
    html = styles.speaker_button_html("cat", "fr")
    assert "en-US" in html, html


def test_speaker_button_english_language_mapping():
    html = styles.speaker_button_html("cat", "en")
    assert "en-US" in html


def test_speaker_button_norwegian_language_mapping():
    html = styles.speaker_button_html("katt", "no")
    assert "nb-NO" in html


def test_speaker_button_no_autoplay_markers():
    html = styles.speaker_button_html("cat", "en")
    # Must only be wired to onclick, never fire on render.
    assert "onclick=" in html
    assert "autoplay" not in html.lower()
    assert "onload=" not in html.lower()


def test_speaker_button_escapes_quotes_and_html_safely():
    tricky = """cat" onmouseover="alert(1)"><script>alert(2)</script>"""
    html = styles.speaker_button_html(tricky, "en")
    # The raw tricky text must never appear verbatim in the output --
    # it must be percent-encoded, so it can't break out of the attribute
    # or inject a script tag.
    assert tricky not in html
    assert "<script>" not in html
    assert urllib.parse.quote(tricky) in html


def test_speaker_button_is_a_plain_button_element():
    html = styles.speaker_button_html("cat", "en")
    assert html.strip().startswith("<button")
    assert html.strip().endswith("</button>")


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
