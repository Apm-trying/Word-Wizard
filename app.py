import streamlit as st
import learner
from translations import t
from styles import CSS, countdown_ring_html, TOWER_SVG, chime_audio_html

st.set_page_config(page_title="Word Wizard", page_icon="🧙", layout="centered")
st.markdown(CSS, unsafe_allow_html=True)

# --- Session state setup ---
if "setup_stage" not in st.session_state:
    st.session_state.setup_stage = "nickname"  # "nickname" -> "language" -> "topic" -> "done"
if "revealed" not in st.session_state:
    st.session_state.revealed = False
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False
if "just_correct" not in st.session_state:
    st.session_state.just_correct = False
if "show_leaderboard" not in st.session_state:
    st.session_state.show_leaderboard = False

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
TOPIC_KEYS = ["politics", "economy", "health", "technology"]

# ============================================================
# STEP 2: TOPIC PICKER — multi-select, shown in the chosen language
# ============================================================
if st.session_state.setup_stage == "topic":
    st.markdown(f'<div class="app-title">{strings["app_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="app-subtitle">{strings["app_subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-label" style="color:#9CA3AE;">{strings["topic_step_title"]}</div>', unsafe_allow_html=True)
    selected_topics = st.multiselect(
        "topics",
        options=TOPIC_KEYS,
        default=TOPIC_KEYS,
        format_func=lambda x: strings["topics"][x],
        label_visibility="collapsed",
    )

    st.write("")
    if st.button(strings["start_button"], use_container_width=True, type="primary"):
        if not selected_topics:
            st.warning(strings["topic_required_warning"])
        else:
            st.session_state.topics = selected_topics
            st.session_state.setup_stage = "done"
            st.session_state.revealed = False
            st.rerun()

    st.stop()

# ============================================================
# WORD SCREEN — shown once nickname + language + topics are set
# ============================================================
language = st.session_state.language
topics = st.session_state.topics

level_info = learner.get_level_info(nickname)
level_title = strings["titles"][level_info["tier"]]

top_col1, top_col2, top_col3 = st.columns([2.4, 1, 1])
with top_col1:
    st.markdown(
        f'<span class="xp-badge">{strings["level_prefix"]} {level_info["level"]} · {level_title} · {level_info["xp"]} XP</span>',
        unsafe_allow_html=True,
    )
with top_col2:
    if st.button(strings["leaderboard_button"], use_container_width=True):
        st.session_state.show_leaderboard = True
        st.rerun()
with top_col3:
    if st.button(strings["settings_button"], use_container_width=True):
        st.session_state.setup_stage = "language"
        st.rerun()

if st.session_state.show_leaderboard:
    st.markdown(f'<div class="app-title" style="font-size:1.6rem;">{strings["leaderboard_title"]}</div>', unsafe_allow_html=True)

    rows_html = ""
    for i, entry in enumerate(learner.get_leaderboard(), start=1):
        title = strings["titles"][entry["tier"]]
        name_display = entry["nickname"] + (strings["you_suffix"] if entry["nickname"] == nickname else "")
        rows_html += (
            f'<div style="display:flex; justify-content:space-between; padding:0.5rem 0; '
            f'border-bottom:1px solid rgba(237,230,214,0.12);">'
            f'<span>#{i} {name_display}</span>'
            f'<span style="color:var(--muted);">{strings["level_prefix"]} {entry["level"]} · {title} · {entry["xp"]} XP</span>'
            f'</div>'
        )
    st.markdown(f'<div class="word-card" style="text-align:left;">{rows_html}</div>', unsafe_allow_html=True)

    if st.button(strings["back_button"], use_container_width=True):
        st.session_state.show_leaderboard = False
        st.rerun()
    st.stop()

word = learner.get_current_word(nickname, language, topics)

if word is None:
    st.success(strings["all_learned"])
    st.stop()

topic_label = strings["topics"][word["topic"]]

if st.session_state.just_correct:
    # Celebration step: shown right after a correct quiz answer, before moving on
    st.markdown(chime_audio_html(), unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="word-card">
            <span class="topic-tag">{topic_label}</span>
            <div class="word-display">{word['word']}</div>
            <div class="section-label">{strings['correct_heading']}</div>
            <div>{strings['xp_gained_template'].format(xp=learner.XP_PER_CORRECT)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(strings["continue_button"], use_container_width=True, type="primary"):
        learner.advance_word(nickname, language, topics)
        st.session_state.just_correct = False
        st.session_state.revealed = False
        st.rerun()

elif not st.session_state.revealed and not st.session_state.quiz_active:
    # Step 1: show the word, ask if they know it
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
            choices, correct_index = learner.get_quiz_choices(word, language)
            st.session_state.quiz_active = True
            st.session_state.quiz_word_id = word["id"]
            st.session_state.quiz_choices = choices
            st.session_state.quiz_correct_index = correct_index
            st.rerun()
    with col2:
        if st.button(strings["no_button"], use_container_width=True):
            learner.mark_status(nickname, word["id"], "unknown")
            st.session_state.revealed = True
            st.rerun()

elif st.session_state.quiz_active and st.session_state.quiz_word_id == word["id"]:
    # Step 2: verify the claim with a 3-option quiz before trusting "known"
    st.markdown(
        f"""
        <div class="word-card">
            <span class="topic-tag">{topic_label}</span>
            <div class="word-display">{word['word']}</div>
            <div class="section-label">{strings['quiz_prompt']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for i, choice_text in enumerate(st.session_state.quiz_choices):
        if st.button(choice_text, use_container_width=True, key=f"quiz_choice_{i}"):
            st.session_state.quiz_active = False
            if i == st.session_state.quiz_correct_index:
                learner.mark_status(nickname, word["id"], "known")
                learner.award_xp(nickname)
                st.session_state.just_correct = True
            else:
                learner.mark_status(nickname, word["id"], "unknown")
                st.session_state.revealed = True
                st.session_state.quiz_was_wrong = True
            st.rerun()

else:
    # Step 3: reveal — reached either via "No" or a wrong quiz answer
    if st.session_state.pop("quiz_was_wrong", False):
        st.warning(strings["quiz_wrong"])

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

    st.info(strings["locked_message"])
    remaining_seconds, percent_elapsed = learner.get_time_remaining(nickname)
    hours = int(remaining_seconds // 3600)
    minutes = int((remaining_seconds % 3600) // 60)
    countdown_label = strings["countdown_format"].format(h=hours, m=minutes)
    st.markdown(countdown_ring_html(percent_elapsed, countdown_label), unsafe_allow_html=True)
