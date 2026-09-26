"""Unit tests for styles.word_display_html and styles.speaker_button_html.
Run directly: python3 tests/test_typography_and_speaker.py
"""
import json
import os
import sys

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


def test_speaker_button_no_autoplay():
    html = styles.speaker_button_html("cat", "en")
    # Must only speak from the click listener, never fire on render/load.
    assert "addEventListener" in html and '"click"' in html
    assert "autoplay" not in html.lower()
    assert "onload=" not in html.lower()


def test_speaker_button_escapes_quotes_and_html_safely():
    tricky = """cat" onmouseover="alert(1)"><script>alert(2)</script>"""
    html = styles.speaker_button_html(tricky, "en")
    # Quotes must be JS-escaped (json.dumps) so they can't break out of the
    # string literal, AND a literal "</script" must never appear verbatim
    # -- even inside a JS string, it closes the <script> tag at the
    # HTML-parser level, so it must come out escaped as "<\/script".
    assert "alert(2)</script>" not in html, "unescaped </script must not survive"
    assert "alert(2)<\\/script>" in html, "must be present, just escaped"
    assert json.dumps(tricky).replace("</script", "<\\/script") in html


def test_speaker_button_is_a_full_html_document_for_components_html():
    """speaker_button_html() is meant to be rendered via
    st.components.v1.html(...), which needs a full HTML document (it's
    rendered inside its own <iframe srcdoc>) -- NOT via
    st.markdown(..., unsafe_allow_html=True), whose sanitizer was found
    (by hand-testing in a real browser) to silently strip inline onXxx
    event-handler attributes, which is why an earlier version of this
    button rendered but did nothing when clicked."""
    html = styles.speaker_button_html("cat", "en")
    assert "<!doctype html>" in html.lower()
    assert '<button type="button" class="speaker-button"' in html
    assert "<script>" in html and "</script>" in html


def test_speaker_button_uses_addeventlistener_not_inline_onclick():
    html = styles.speaker_button_html("cat", "en")
    assert "onclick=" not in html


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
