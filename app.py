import streamlit as st
import learner
from translations import t
from styles import CSS, countdown_ring_html, TOWER_SVG

st.set_page_config(page_title="Word Wizard / Ordtrollmann", page_icon="🧙", layout="centered")
st.markdown(CSS, unsafe_allow_html=True)

# --- Session state setup ---
if "setup_stage" not in st.session_state:
    st.session_state.setup_stage = "nickname"  # "nickname" -> "language" -> "topic" -> "done"
if "revealed" not in st.session_state:
    st.session_state.revealed = False

# ============================================================
# STEP 0: NICKNAME — identifies this person so progress doesn't
# collide with anyone else using the same deployed app
# ============================================================
if st.session_state.setup_stage == "nickname":
    st.markdown(TOWER_SVG, unsafe_allow_html=True)
    st.markdown('<div class="app-title">🧙 Word Wizard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">Enter your name to begin / Skriv inn navnet ditt for å starte</div>',
        unsafe_allow_html=True,
    )

    nickname_input = st.text_input("nickname", label_visibility="collapsed", placeholder="Your name / Ditt navn")

    if st.button("Continue / Fortsett →", use_container_width=True, type="primary"):
        clean_nickname = learner.sanitize_nickname(nickname_input)
        if clean_nickname:
            st.session_state.nickname = clean_nickname
            st.session_state.setup_stage = "language"
            st.rerun()
        else:
            st.error("Please enter a name / Vennligst skriv inn et navn")

    st.stop()

nickname = st.session_state.nickname

# ============================================================
# STEP 1: LANGUAGE PICKER — shown neutrally, no locale set yet
# ============================================================
if st.session_state.setup_stage == "language":
    st.markdown(TOWER_SVG, unsafe_allow_html=True)
    st.markdown('<div class="app-title">🧙 Word Wizard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">Choose your language to continue / Velg språk for å fortsette</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇳🇴 Norsk", use_container_width=True):
            st.session_state.language = "no"
            st.session_state.setup_stage = "topic"
            st.rerun()
    with col2:
        if st.button("🇬🇧 English", use_container_width=True):
            st.session_state.language = "en"
            st.session_state.setup_stage = "topic"
            st.rerun()

    st.stop()

# From here on, we have a language, so all further text comes from translations.py
strings = t(st.session_state.language)

# ============================================================
# STEP 2: TOPIC PICKER — shown in the language just chosen
# ============================================================
if st.session_state.setup_stage == "topic":
    st.markdown(f'<div class="app-title">{strings["app_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="app-subtitle">{strings["app_subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-label" style="color:#9CA3AE;">{strings["topic_step_title"]}</div>', unsafe_allow_html=True)
    topic_choice = st.radio(
        "topic",
        options=["all", "politics", "economy", "health", "technology"],
        format_func=lambda x: strings["topics"][x],
        label_visibility="collapsed",
    )

    st.write("")
    if st.button(strings["start_button"], use_container_width=True, type="primary"):
        st.session_state.topic = topic_choice
        st.session_state.setup_stage = "done"
        st.session_state.revealed = False
        st.rerun()

    st.stop()

# ============================================================
# WORD SCREEN — shown once nickname + language + topic are set
# ============================================================
language = st.session_state.language
topic = st.session_state.topic

top_col1, top_col2 = st.columns([3, 1])
with top_col2:
    if st.button(strings["settings_button"], use_container_width=True):
        st.session_state.setup_stage = "language"
        st.rerun()

word = learner.get_current_word(nickname, language, topic)

if word is None:
    st.success(strings["all_learned"])
    st.stop()

topic_label = strings["topics"][word["topic"]]
word_status = learner.get_word_status(nickname, word["id"])

if not st.session_state.revealed:
    st.markdown(
        f"""
        <div class="word-card">
            <span class="topic-tag">{topic_label}</span>
            <div class="word-display">{word['word']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(strings["know_prompt"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button(strings["yes_button"], use_container_width=True):
            learner.mark_status(nickname, word["id"], "known")
            st.session_state.revealed = True
            st.rerun()
    with col2:
        if st.button(strings["no_button"], use_container_width=True):
            learner.mark_status(nickname, word["id"], "unknown")
            st.session_state.revealed = True
            st.rerun()

else:
    examples_html = "".join(f'<div class="example-line"><em>{ex}</em></div>' for ex in word["examples"])
    st.markdown(
        f"""
        <div class="word-card">
            <span class="topic-tag">{topic_label}</span>
            <div class="word-display">{word['word']}</div>
            <div class="section-label">{strings['definition_label']}</div>
            <div>{word['definition']}</div>
            <div class="section-label">{strings['example_label']}</div>
            {examples_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if word_status == "known":
        st.success(strings["known_success"])
        if st.button(strings["skip_button"], use_container_width=True):
            learner.skip_word(nickname, language, topic)
            st.session_state.revealed = False
            st.rerun()
    else:
        st.info(strings["locked_message"])
        remaining_seconds, percent_elapsed = learner.get_time_remaining(nickname)
        hours = int(remaining_seconds // 3600)
        minutes = int((remaining_seconds % 3600) // 60)
        countdown_label = strings["countdown_format"].format(h=hours, m=minutes)
        st.markdown(countdown_ring_html(percent_elapsed, countdown_label), unsafe_allow_html=True)
