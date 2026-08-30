import streamlit as st
import learner
from translations import t
from styles import CSS, countdown_ring_html, TOWER_SVG, chime_audio_html

st.set_page_config(page_title="Word Wizard", page_icon="🧙", layout="centered")
st.markdown(CSS, unsafe_allow_html=True)

# Typing this as your "name" on the nickname screen opens the hidden admin
# panel instead of starting the app normally. Not shown anywhere in the UI.
ADMIN_TRIGGER = "wizardmasterkey"

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
if "show_my_words" not in st.session_state:
    st.session_state.show_my_words = False

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
        if nickname_input.strip().lower() == ADMIN_TRIGGER:
            st.session_state.setup_stage = "admin_login"
            st.rerun()
        else:
            clean_nickname = learner.sanitize_nickname(nickname_input)
            if not clean_nickname:
                st.error("Please enter a name / Vennligst skriv inn et navn")
            elif not learner.is_nickname_allowed(nickname_input):
                st.error("That name isn't allowed, please choose another. / Det navnet er ikke tillatt, velg et annet.")
            else:
                st.session_state.nickname = clean_nickname
                st.session_state.setup_stage = "language"
                st.rerun()

    st.stop()

# ============================================================
# ADMIN — hidden behind a magic nickname + password, not shown
# to regular users anywhere in the normal UI
# ============================================================
if st.session_state.setup_stage == "admin_login":
    st.markdown('<div class="app-title">🛠️ Admin</div>', unsafe_allow_html=True)
    password_input = st.text_input("password", type="password", label_visibility="collapsed", placeholder="Password")

    if st.button("Enter", use_container_width=True, type="primary"):
        try:
            admin_password = st.secrets.get("ADMIN_PASSWORD", None)
        except Exception:
            admin_password = None
        if admin_password and password_input == admin_password:
            st.session_state.setup_stage = "admin_panel"
            st.rerun()
        else:
            st.error("Incorrect password, or ADMIN_PASSWORD isn't set in Streamlit secrets yet.")

    if st.button("← Back", use_container_width=True):
        st.session_state.setup_stage = "nickname"
        st.rerun()

    st.stop()

if st.session_state.setup_stage == "admin_panel":
    st.markdown('<div class="app-title">🛠️ Admin Panel</div>', unsafe_allow_html=True)
    all_users = learner.get_leaderboard(limit=1000)

    if not all_users:
        st.info("No users yet.")
    for entry in all_users:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f'{entry["nickname"]} — Level {entry["level"]} ({entry["tier"]}), {entry["xp"]} XP')
        with col2:
            if st.button("Delete", key=f"del_{entry['nickname']}"):
                learner.delete_user(entry["nickname"])
                st.rerun()

    if st.button("← Exit Admin", use_container_width=True):
        st.session_state.setup_stage = "nickname"
        st.rerun()

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
TOPIC_KEYS = ["politics", "economy", "health", "technology", "sports", "culture", "science"]

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

top_col1, top_col2, top_col3, top_col4 = st.columns([2.4, 1, 1, 1])
with top_col1:
    st.markdown(
        f'<span class="xp-badge">{strings["level_prefix"]} {level_info["level"]} · {level_title} · {level_info["xp"]} XP</span>',
        unsafe_allow_html=True,
    )
with top_col2:
    if st.button(strings["leaderboard_button"], use_container_width=True, help="Leaderboard"):
        st.session_state.show_leaderboard = True
        st.rerun()
with top_col3:
    if st.button(strings["my_words_button"], use_container_width=True, help=strings["my_words_tooltip"]):
        st.session_state.show_my_words = True
        st.rerun()
with top_col4:
    if st.button(strings["settings_button"], use_container_width=True, help=strings["settings_tooltip"]):
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

if st.session_state.show_my_words:
    known_words = learner.get_words_by_status(nickname, language, "known")
    unknown_words = learner.get_words_by_status(nickname, language, "unknown")

    st.markdown(f'<div class="app-title" style="font-size:1.6rem;">{strings["trophy_room_title"]}</div>', unsafe_allow_html=True)
    if known_words:
        rows_html = "".join(
            f'<div style="padding:0.5rem 0; border-bottom:1px solid rgba(237,230,214,0.12);">'
            f'<strong>{w["word"]}</strong><br>'
            f'<span style="color:var(--muted); font-size:0.85rem;">{w["definition"]}</span></div>'
            for w in known_words
        )
        st.markdown(f'<div class="word-card" style="text-align:left;">{rows_html}</div>', unsafe_allow_html=True)
    else:
        st.info(strings["empty_trophy"])

    st.markdown(f'<div class="app-title" style="font-size:1.6rem;">{strings["graveyard_title"]}</div>', unsafe_allow_html=True)
    if unknown_words:
        rows_html = "".join(
            f'<div style="padding:0.5rem 0; border-bottom:1px solid rgba(237,230,214,0.12);">'
            f'<strong>{w["word"]}</strong><br>'
            f'<span style="color:var(--muted); font-size:0.85rem;">{w["definition"]}</span></div>'
            for w in unknown_words
        )
        st.markdown(f'<div class="word-card" style="text-align:left;">{rows_html}</div>', unsafe_allow_html=True)
    else:
        st.info(strings["empty_graveyard"])

    if st.button(strings["back_button"], use_container_width=True):
        st.session_state.show_my_words = False
        st.rerun()
    st.stop()

word = learner.get_current_word(nickname, language, topics)

if word is None:
    st.success(strings["all_learned"])
    st.stop()

topic_label = strings["topics"][word["topic"]]
is_review = learner.get_word_status(nickname, word["id"]) == "known"
review_tag_html = f'<span class="topic-tag" style="margin-left:0.4rem;">{strings["review_tag"]}</span>' if is_review else ""

if st.session_state.just_correct:
    # Celebration step: shown right after a correct quiz answer, before moving on
    st.markdown(chime_audio_html(), unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="word-card">
            <span class="topic-tag">{topic_label}</span>
            <div class="word-display">{word['word']}</div>
            <div class="section-label">{strings['correct_heading']}</div>
            <div>{strings['xp_gained_template'].format(xp=st.session_state.xp_awarded)}</div>
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
            <span class="topic-tag">{topic_label}</span>{review_tag_html}
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
                xp_awarded = learner.score_correct_answer(nickname, word["id"])
                st.session_state.just_correct = True
                st.session_state.xp_awarded = xp_awarded
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
