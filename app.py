import streamlit as st
import streamlit.components.v1 as components
import time
import learner
from translations import t
from styles import CSS, countdown_ring_html, TOWER_SVG, chime_audio_html, MONSTER_SVG, hp_bar_html, BOSS_MONSTER_SVG, boss_hp_html, wizard_avatar_html, spell_projectile_html, boss_entrance_html, boss_feedback_html, boss_outcome_heading_html, rank_up_html, level_up_badge_html, progression_hero_html, xp_progress_bar_html, progression_next_rank_html, rank_ladder_html

st.set_page_config(page_title="Word Wizard", page_icon="🧙", layout="centered")
components.html(
    """
    <script>
    const doc = window.parent.document;
    if (!doc.querySelector('meta[name="apple-mobile-web-app-capable"]')) {
        const capable = doc.createElement('meta');
        capable.name = 'apple-mobile-web-app-capable';
        capable.content = 'yes';
        doc.head.appendChild(capable);

        const statusBar = doc.createElement('meta');
        statusBar.name = 'apple-mobile-web-app-status-bar-style';
        statusBar.content = 'black-translucent';
        doc.head.appendChild(statusBar);

        const title = doc.createElement('meta');
        title.name = 'apple-mobile-web-app-title';
        title.content = 'Word Wizard';
        doc.head.appendChild(title);

        const touchIcon = doc.createElement('link');
        touchIcon.rel = 'apple-touch-icon';
        touchIcon.href = window.parent.location.origin + '/app/static/apple-touch-icon.png';
        doc.head.appendChild(touchIcon);

        const icon192 = doc.createElement('link');
        icon192.rel = 'icon';
        icon192.href = window.parent.location.origin + '/app/static/icon-192.png';
        doc.head.appendChild(icon192);
    }
    </script>
    """,
    height=0,
)
st.markdown(CSS, unsafe_allow_html=True)

# Typing this as your "name" at the name-entry screen opens the hidden admin
# panel instead of saving progress normally. Not shown anywhere in the UI.
ADMIN_TRIGGER = "wizardmasterkey"

# --- Session state setup ---
if "setup_stage" not in st.session_state:
    st.session_state.setup_stage = "landing"
if "language" not in st.session_state:
    # Default to English always. The only way to get Norwegian is an explicit
    # choice on the language screen, or a "remember me" URL from a previous
    # explicit choice — never automatic browser-language detection.
    query_lang = st.query_params.get("lang")
    st.session_state.language = query_lang if query_lang in ("en", "no") else "en"
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
if "show_progression" not in st.session_state:
    st.session_state.show_progression = False
if "boss_outcome" not in st.session_state:
    st.session_state.boss_outcome = None
if "boss_entrance_shown" not in st.session_state:
    # Tracks whether the "⚔ BOSS APPROACHES" entrance has already played for
    # the currently-active boss encounter, so it fires exactly once per
    # encounter and never replays on ordinary Streamlit reruns.
    st.session_state.boss_entrance_shown = False
if "rank_up_info" not in st.session_state:
    # Set right after a correct answer pushes the player into a new rank
    # tier (e.g. Level 9 -> 10: Apprentice). Shown as a full celebratory
    # screen that takes priority over whatever would normally show next.
    st.session_state.rank_up_info = None
if "level_up_info" not in st.session_state:
    # Set right after a correct answer pushes the player up a level
    # *without* crossing into a new rank tier. Shown as a small one-shot
    # badge on the very next screen, no extra click or screen required.
    st.session_state.level_up_info = None

# --- Remember me: if the URL already has a recognized nickname (saved there
# after a previous login, e.g. via "Add to Home Screen"), skip straight past
# landing/login. If topics are saved too, skip straight into the game. ---
if "nickname" not in st.session_state and st.session_state.setup_stage == "landing":
    url_nickname = st.query_params.get("nickname")
    if url_nickname:
        remembered_nickname = learner.sanitize_nickname(url_nickname)
        if remembered_nickname and learner.user_exists(remembered_nickname):
            st.session_state.nickname = remembered_nickname
            url_topics = st.query_params.get("topics")
            if url_topics:
                st.session_state.topics = url_topics.split(",")
                st.session_state.setup_stage = "done"
            else:
                st.session_state.setup_stage = "language"

# ============================================================
# STEP 0: LANDING — no name required, just start playing
# ============================================================
if st.session_state.setup_stage == "landing":
    landing_strings = t(st.session_state.language)

    st.markdown(
        '<div style="display:flex; align-items:center; gap:8px; padding-top:0.4rem; margin-bottom:1rem;">'
        '<svg viewBox="0 0 100 100" width="26" xmlns="http://www.w3.org/2000/svg">'
        '<path d="M 50 10 L 72 68 Q 50 80 28 68 Z" fill="#7B7F92" stroke="#4A4E5E" stroke-width="2"/>'
        '<ellipse cx="50" cy="68" rx="30" ry="8" fill="#5B6578" stroke="#4A4E5E" stroke-width="2"/>'
        '</svg>'
        '<span style="font-family:\'Fraunces\',serif; font-weight:600; font-size:0.9rem; '
        'color:#F5F1E6; line-height:1.15; text-transform:uppercase; letter-spacing:0.02em;">Word<br>Wizard</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(TOWER_SVG, unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Word</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title hero-title-gold">Wizard</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="text-align:center; margin-bottom:1rem;"><span class="subtitle-banner">{landing_strings["landing_subtitle"]}</span></div>',
        unsafe_allow_html=True,
    )

    if st.button(f'✨ {landing_strings["landing_start_button"]}', use_container_width=True, type="primary"):
        with st.spinner("✨ Casting your spell..."):
            time.sleep(1.2)
        st.session_state.setup_stage = "language"
        st.rerun()
    st.markdown(
        f'<div class="no-account-caption">{landing_strings["no_account_caption"]}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div style="text-align:center; margin-top:0.8rem;">', unsafe_allow_html=True)
    if st.button(landing_strings["log_back_in_button"], use_container_width=False, type="tertiary"):
        st.session_state.setup_stage = "returning_login"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# ============================================================
# RETURNING USER — logs back in with an existing nickname,
# completely separate from the guest flow so there are no
# guest-word side effects on your real progress
# ============================================================
if st.session_state.setup_stage == "returning_login":
    returning_strings = t(st.session_state.language)
    st.markdown(
        f'<div class="app-title" style="font-size:1.6rem;">{returning_strings["welcome_back_title"]}</div>',
        unsafe_allow_html=True,
    )
    returning_nickname_input = st.text_input(
        "returning_nickname", label_visibility="collapsed",
        placeholder=returning_strings["wizard_name_placeholder"],
    )

    if st.button(returning_strings["returning_continue_button"], use_container_width=True, type="primary"):
        clean_nickname = learner.sanitize_nickname(returning_nickname_input)
        if not clean_nickname:
            st.error(returning_strings["empty_name_error"])
        elif not learner.user_exists(clean_nickname):
            st.error(returning_strings["no_wizard_found_error"])
        else:
            st.session_state.nickname = clean_nickname
            st.query_params["nickname"] = clean_nickname
            st.session_state.setup_stage = "language"
            st.rerun()

    if st.button("← Back", use_container_width=True):
        st.session_state.setup_stage = "landing"
        st.rerun()

    st.stop()

# ============================================================
# STEP 1: LANGUAGE PICKER — shown neutrally, no locale set yet
# ============================================================
if st.session_state.setup_stage == "language":
    st.markdown('<div class="app-title" style="font-size:1.6rem;">Choose your language</div>', unsafe_allow_html=True)

    if st.button("🇬🇧  English  ›", use_container_width=True, type="secondary"):
        st.session_state.language = "en"
        st.session_state.setup_stage = "topic"
        st.rerun()
    if st.button("🇳🇴  Norsk  ›", use_container_width=True, type="secondary"):
        st.session_state.language = "no"
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
        default=TOPIC_KEYS[:3],
        format_func=lambda x: strings["topics"][x],
        label_visibility="collapsed",
    )

    st.write("")
    if st.button(strings["start_button"], use_container_width=True, type="primary"):
        if not selected_topics:
            st.warning(strings["topic_required_warning"])
        else:
            st.session_state.topics = selected_topics
            if "nickname" in st.session_state:
                # Returning user — already logged in, skip the guest flow entirely
                st.query_params["nickname"] = st.session_state.nickname
                st.query_params["lang"] = st.session_state.language
                st.query_params["topics"] = ",".join(selected_topics)
                st.session_state.setup_stage = "done"
                st.session_state.revealed = False
                st.session_state.quiz_active = False
                st.session_state.just_correct = False
            else:
                st.session_state.guest_word = learner.pick_guest_word(st.session_state.language, selected_topics)
                st.session_state.setup_stage = "guest_word"
            st.rerun()

    st.stop()

language = st.session_state.language

# ============================================================
# GUEST FLOW — a real word, shown before any name is collected
# ============================================================
if st.session_state.setup_stage in ("guest_word", "guest_quiz", "name_entry"):
    guest_word = st.session_state.guest_word
    topic_label = strings["topics"][guest_word["topic"]]

    if st.session_state.setup_stage == "guest_word":
        st.markdown(
            f"""
            <div class="word-card">
                <span class="topic-tag">{topic_label}</span>
                <div class="word-display">{guest_word['word']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(strings["know_prompt"])

        col1, col2 = st.columns(2)
        with col1:
            if st.button(strings["yes_button"], use_container_width=True):
                choices, correct_index = learner.get_quiz_choices(guest_word, language)
                st.session_state.guest_quiz_choices = choices
                st.session_state.guest_quiz_correct_index = correct_index
                st.session_state.setup_stage = "guest_quiz"
                st.rerun()
        with col2:
            if st.button(strings["no_button"], use_container_width=True):
                st.session_state.guest_correct = False
                st.session_state.setup_stage = "name_entry"
                st.rerun()
        st.stop()

    if st.session_state.setup_stage == "guest_quiz":
        st.markdown(
            f"""
            <div class="word-card">
                <span class="topic-tag">{topic_label}</span>
                <div class="word-display">{guest_word['word']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for i, choice_text in enumerate(st.session_state.guest_quiz_choices):
            if st.button(choice_text, use_container_width=True, key=f"guest_quiz_choice_{i}"):
                st.session_state.guest_correct = (i == st.session_state.guest_quiz_correct_index)
                st.session_state.setup_stage = "name_entry"
                st.rerun()
        st.stop()

    if st.session_state.setup_stage == "name_entry":
        if st.session_state.guest_correct:
            st.markdown(chime_audio_html(), unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="word-card">
                    <span class="topic-tag">{topic_label}</span>
                    <div class="word-display">{guest_word['word']}</div>
                    <div class="section-label">{strings['correct_heading']}</div>
                    <div>{strings['xp_gained_template'].format(xp=learner.XP_PER_CORRECT)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(strings["save_progress_correct"])
        else:
            examples_html = "".join(f'<div class="example-line"><em>{ex}</em></div>' for ex in guest_word["examples"])
            st.markdown(
                f"""
                <div class="word-card">
                    <span class="topic-tag">{topic_label}</span>
                    <div class="word-display">{guest_word['word']}</div>
                    <div class="section-label">{strings['definition_label']}</div>
                    <div>{guest_word['definition']}</div>
                    <div class="section-label">{strings['example_label']}</div>
                    {examples_html}
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(strings["save_progress_incorrect"])

        nickname_input = st.text_input("nickname", label_visibility="collapsed", placeholder="Your name / Ditt navn")

        if st.button(strings["continue_button"], use_container_width=True, type="primary"):
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
                    if st.session_state.guest_correct:
                        learner.score_correct_answer(clean_nickname, guest_word["id"])
                        learner.advance_word(clean_nickname, language, st.session_state.topics)
                    else:
                        learner.mark_status(clean_nickname, guest_word["id"], "unknown")
                        learner.lock_guest_word(clean_nickname, guest_word, language, st.session_state.topics)
                    with st.spinner("✨ Casting your spell..."):
                        time.sleep(1.2)
                    st.session_state.nickname = clean_nickname
                    st.query_params["nickname"] = clean_nickname
                    st.query_params["lang"] = language
                    st.query_params["topics"] = ",".join(st.session_state.topics)
                    st.session_state.setup_stage = "done"
                    st.session_state.revealed = False
                    st.session_state.quiz_active = False
                    st.session_state.just_correct = False
                    st.rerun()
        st.stop()

# ============================================================
# ADMIN — hidden behind a magic name + password, not shown
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
        st.session_state.setup_stage = "landing"
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
        st.session_state.setup_stage = "landing"
        st.rerun()

    st.stop()

# ============================================================
# WORD SCREEN — shown once nickname + language + topics are set
# ============================================================
nickname = st.session_state.nickname
topics = st.session_state.topics

level_info = learner.get_level_info(nickname)
level_title = strings["titles"][level_info["tier"]]
streak = learner.get_streak(nickname)

# Maps the 6 rank tiers down to 3 visual bands for the wizard avatar —
# your character's robe/hat/staff gets more elaborate as you rank up.
WIZARD_VISUAL_TIER = {
    "beginner": 1, "apprentice": 1,
    "spellcaster": 2, "wizard": 2,
    "master_wizard": 3, "archmage": 3,
}
wizard_visual_tier = WIZARD_VISUAL_TIER.get(level_info["tier"], 1)


def render_encounter(enemy_svg, enemy_class, casting=False):
    """
    Shows your wizard (leveling up in appearance with your rank) beside the
    enemy, in one flexbox row so positioning is fully in our control — needed
    for the spell projectile below to travel accurately between the two.
    casting=True (only on a correct answer) adds a one-shot projectile that
    flies from the wizard to the enemy, in a style that matches your rank tier.
    """
    projectile_html = (
        f'<div class="spell-projectile">{spell_projectile_html(wizard_visual_tier)}</div>' if casting else ""
    )
    # Built without leading whitespace per line — indented HTML inside a
    # triple-quoted string gets misread by Streamlit's markdown parser as a
    # code block (4+ spaces = code block in standard Markdown), which
    # silently overrides unsafe_allow_html and shows raw text instead.
    html = (
        '<div class="encounter-row">'
        f'<div class="wizard-slot">{wizard_avatar_html(wizard_visual_tier)}</div>'
        f'{projectile_html}'
        f'<div class="enemy-slot {enemy_class}">{enemy_svg}</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


top_col1, top_col2, top_col3, top_col4, top_col5 = st.columns([2.0, 1, 1, 1, 1])
with top_col1:
    st.markdown(
        f'<span class="xp-badge">🔥 {streak} · {strings["level_prefix"]} {level_info["level"]} · {level_title} · {level_info["xp"]} XP</span>',
        unsafe_allow_html=True,
    )
with top_col2:
    if st.button(strings["progression_button"], use_container_width=True, help=strings["progression_tooltip"]):
        st.session_state.show_progression = True
        st.rerun()
with top_col3:
    if st.button(strings["leaderboard_button"], use_container_width=True, help="Leaderboard"):
        st.session_state.show_leaderboard = True
        st.rerun()
with top_col4:
    if st.button(strings["my_words_button"], use_container_width=True, help=strings["my_words_tooltip"]):
        st.session_state.show_my_words = True
        st.rerun()
with top_col5:
    if st.button(strings["settings_button"], use_container_width=True, help=strings["settings_tooltip"]):
        st.session_state.setup_stage = "language"
        st.rerun()

if st.session_state.show_progression:
    st.markdown(f'<div class="app-title" style="font-size:1.6rem;">{strings["progression_title"]}</div>', unsafe_allow_html=True)

    st.markdown(
        progression_hero_html(
            wizard_tier_html=wizard_avatar_html(wizard_visual_tier),
            rank_name=level_title,
            level_label=f'{strings["level_prefix"]} {level_info["level"]}',
        ),
        unsafe_allow_html=True,
    )

    xp_percent = (level_info["xp_into_level"] / level_info["xp_for_next"]) * 100 if level_info["xp_for_next"] else 100
    xp_remaining = level_info["xp_for_next"] - level_info["xp_into_level"]
    st.markdown(
        xp_progress_bar_html(
            percent=xp_percent,
            xp_label=strings["progression_xp_label"],
            remaining_label=strings["progression_xp_remaining_template"].format(
                xp=xp_remaining, level=level_info["level"] + 1
            ),
        ),
        unsafe_allow_html=True,
    )

    next_tier = learner.get_next_tier(level_info["tier"])
    if next_tier:
        next_level_required, next_tier_name = next_tier
        st.markdown(
            progression_next_rank_html(
                strings["progression_next_rank_template"].format(
                    rank=f'<strong>{strings["titles"][next_tier_name]}</strong>',
                    level_label=f'{strings["level_prefix"]} {next_level_required}',
                )
            ),
            unsafe_allow_html=True,
        )
    else:
        st.markdown(progression_next_rank_html(strings["progression_max_rank_message"]), unsafe_allow_html=True)

    # Rank ladder: every tier, lowest first, marked completed / current /
    # future purely by comparing tier names against the player's current
    # tier -- reuses learner.RANK_LADDER (a display-only reordering of the
    # real LEVEL_TIERS thresholds) rather than any new progression logic.
    ladder_rows = []
    found_current = False
    for threshold, tier_name in learner.RANK_LADDER:
        if tier_name == level_info["tier"]:
            state = "current"
            found_current = True
        elif found_current:
            state = "future"
        else:
            state = "completed"
        level_display = 1 if threshold == 0 else threshold
        ladder_rows.append({
            "name": strings["titles"][tier_name],
            "level_label": f'{strings["level_prefix"]} {level_display}',
            "state": state,
        })
    st.markdown(
        f'<div class="word-card" style="text-align:left;">{rank_ladder_html(ladder_rows)}</div>',
        unsafe_allow_html=True,
    )

    if st.button(strings["back_button"], use_container_width=True):
        st.session_state.show_progression = False
        st.rerun()
    st.stop()

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

if st.session_state.rank_up_info is not None:
    # The big, "amazing" moment -- takes priority over whatever would
    # otherwise show next (a boss outcome, a plain correct-answer screen),
    # which still shows normally on the next rerun once this is dismissed.
    rank_up = st.session_state.rank_up_info
    st.markdown(chime_audio_html(), unsafe_allow_html=True)
    st.markdown(
        rank_up_html(
            rank_up_title=strings["rank_up_title"],
            rank_name=strings["titles"][rank_up["new_tier"]],
            level_label=f'{strings["level_prefix"]} {rank_up["new_level"]}',
            flavor=strings["rank_up_flavor"],
            wizard_tier_html=wizard_avatar_html(WIZARD_VISUAL_TIER.get(rank_up["new_tier"], 1)),
        ),
        unsafe_allow_html=True,
    )
    if st.button(strings["continue_button"], use_container_width=True, type="primary"):
        st.session_state.rank_up_info = None
        st.rerun()

elif st.session_state.boss_outcome is not None:
    outcome = st.session_state.boss_outcome
    q_num = st.session_state.get("boss_question_number", 1)
    correct_so_far = st.session_state.get("boss_correct_so_far", 0)
    bonus_xp = st.session_state.get("boss_bonus_xp", 0)

    level_up = st.session_state.pop("level_up_info", None)
    if level_up:
        st.markdown(
            level_up_badge_html(strings["level_up_badge"].format(level=level_up["new_level"])),
            unsafe_allow_html=True,
        )

    if outcome == "perfect":
        st.markdown(chime_audio_html(), unsafe_allow_html=True)
        st.markdown(boss_outcome_heading_html(strings["boss_name"], strings["boss_subtitle"]), unsafe_allow_html=True)
        render_encounter(BOSS_MONSTER_SVG, "monster-defeated boss-portrait", casting=True)
        st.markdown(boss_hp_html(0, learner.BOSS_MAX_HP, label=strings["boss_hp_label"]), unsafe_allow_html=True)
        st.success(strings["boss_perfect_message"].format(xp=bonus_xp))
    elif outcome == "defeated":
        st.markdown(chime_audio_html(), unsafe_allow_html=True)
        st.markdown(boss_outcome_heading_html(strings["boss_name"], strings["boss_subtitle"]), unsafe_allow_html=True)
        render_encounter(BOSS_MONSTER_SVG, "monster-defeated boss-portrait", casting=True)
        st.markdown(boss_hp_html(0, learner.BOSS_MAX_HP, label=strings["boss_hp_label"]), unsafe_allow_html=True)
        st.success(strings["boss_defeated_message"].format(correct=correct_so_far, xp=bonus_xp))
    elif outcome == "escaped":
        st.markdown(boss_outcome_heading_html(strings["boss_name"], strings["boss_subtitle"]), unsafe_allow_html=True)
        render_encounter(BOSS_MONSTER_SVG, "boss-encounter boss-portrait", casting=False)
        st.markdown(boss_hp_html(learner.get_boss_hp(nickname, language), learner.BOSS_MAX_HP, label=strings["boss_hp_label"]), unsafe_allow_html=True)
        st.warning(strings["boss_escaped_message"].format(correct=correct_so_far))
    elif outcome == "hit":
        st.markdown(chime_audio_html(), unsafe_allow_html=True)
        render_encounter(BOSS_MONSTER_SVG, "boss-encounter", casting=True)
        current_hp = learner.get_boss_hp(nickname, language)
        st.markdown(
            boss_hp_html(current_hp, learner.BOSS_MAX_HP,
                         label=strings["boss_question_label"].format(n=q_num, max=learner.BOSS_MAX_QUESTIONS)),
            unsafe_allow_html=True,
        )
        st.markdown(
            boss_feedback_html(strings["boss_hit_headline"], strings["boss_hit_message"].format(correct=correct_so_far), "hit"),
            unsafe_allow_html=True,
        )
    else:  # "miss"
        render_encounter(BOSS_MONSTER_SVG, "boss-encounter")
        current_hp = learner.get_boss_hp(nickname, language)
        st.markdown(
            boss_hp_html(current_hp, learner.BOSS_MAX_HP,
                         label=strings["boss_question_label"].format(n=q_num, max=learner.BOSS_MAX_QUESTIONS)),
            unsafe_allow_html=True,
        )
        st.markdown(
            boss_feedback_html(strings["boss_miss_headline"], strings["boss_miss_message"].format(correct=correct_so_far), "miss"),
            unsafe_allow_html=True,
        )

    if st.button(strings["continue_button"], use_container_width=True, type="primary"):
        if outcome in ("perfect", "defeated", "escaped"):
            # This boss encounter is fully over — clear the entrance flag so
            # a freshly-triggered new boss (advance_word can roll one for
            # the very next word) gets its own "⚔ BOSS APPROACHES" moment.
            st.session_state.boss_entrance_shown = False
        learner.advance_word(nickname, language, topics)
        st.session_state.boss_outcome = None
        st.session_state.revealed = False
        st.session_state.quiz_active = False
        st.session_state.just_correct = False
        st.rerun()

elif st.session_state.just_correct:
    level_up = st.session_state.pop("level_up_info", None)
    if level_up:
        st.markdown(
            level_up_badge_html(strings["level_up_badge"].format(level=level_up["new_level"])),
            unsafe_allow_html=True,
        )
    st.markdown(chime_audio_html(), unsafe_allow_html=True)
    render_encounter(MONSTER_SVG, "monster-defeated", casting=True)
    st.markdown(hp_bar_html(0, draining=True, label=strings["monster_hp_label"]), unsafe_allow_html=True)
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
    boss_active = learner.is_boss_active(nickname, language)
    if boss_active:
        if not st.session_state.boss_entrance_shown:
            # Plays once, the first time this specific boss encounter is
            # seen on the idle ask-screen; resets below once the encounter
            # ends, ready for the next boss to trigger its own entrance.
            st.session_state.boss_entrance_shown = True
            st.markdown(
                boss_entrance_html(strings["boss_arrives_label"], strings["boss_name"], strings["boss_subtitle"]),
                unsafe_allow_html=True,
            )
        render_encounter(BOSS_MONSTER_SVG, "boss-encounter")
        st.markdown(
            boss_hp_html(learner.get_boss_hp(nickname, language), learner.BOSS_MAX_HP,
                         label=strings["boss_question_label"].format(n=learner.get_boss_question_number(nickname, language), max=learner.BOSS_MAX_QUESTIONS)),
            unsafe_allow_html=True,
        )
    else:
        st.session_state.boss_entrance_shown = False
        render_encounter(MONSTER_SVG, "monster-idle")
        st.markdown(hp_bar_html(100, label=strings["monster_hp_label"]), unsafe_allow_html=True)
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
            if boss_active:
                result_info = learner.boss_miss(nickname, language)
                st.session_state.boss_outcome = result_info["result"] if result_info["finished"] else "miss"
                st.session_state.boss_question_number = result_info["question_number"]
                st.session_state.boss_correct_so_far = result_info["correct_so_far"]
                st.session_state.boss_bonus_xp = result_info["bonus_xp"]
            else:
                st.session_state.revealed = True
            st.rerun()

elif st.session_state.quiz_active and st.session_state.quiz_word_id == word["id"]:
    boss_active = learner.is_boss_active(nickname, language)
    if boss_active:
        render_encounter(BOSS_MONSTER_SVG, "boss-encounter")
        st.markdown(
            boss_hp_html(learner.get_boss_hp(nickname, language), learner.BOSS_MAX_HP,
                         label=strings["boss_question_label"].format(n=learner.get_boss_question_number(nickname, language), max=learner.BOSS_MAX_QUESTIONS)),
            unsafe_allow_html=True,
        )
    else:
        render_encounter(MONSTER_SVG, "monster-idle")
        st.markdown(hp_bar_html(100, label=strings["monster_hp_label"]), unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="word-card">
            <span class="topic-tag">{topic_label}</span>
            <div class="word-display">{word['word']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for i, choice_text in enumerate(st.session_state.quiz_choices):
        if st.button(choice_text, use_container_width=True, key=f"quiz_choice_{i}"):
            st.session_state.quiz_active = False
            # Snapshot level/rank from before this answer's XP (whether
            # per-word XP, boss bonus XP on a finishing hit, or boss bonus
            # XP on a finishing miss) is awarded below, so we can tell
            # afterwards whether it pushed the player up a level and/or
            # into a new rank tier.
            old_level = level_info["level"]
            old_tier = level_info["tier"]
            if i == st.session_state.quiz_correct_index:
                xp_awarded = learner.score_correct_answer(nickname, word["id"])
                if boss_active:
                    result_info = learner.boss_hit(nickname, language)
                    st.session_state.boss_outcome = result_info["result"] if result_info["finished"] else "hit"
                    st.session_state.boss_question_number = result_info["question_number"]
                    st.session_state.boss_correct_so_far = result_info["correct_so_far"]
                    st.session_state.boss_bonus_xp = result_info["bonus_xp"]
                else:
                    st.session_state.just_correct = True
                    st.session_state.xp_awarded = xp_awarded
            else:
                learner.mark_status(nickname, word["id"], "unknown")
                if boss_active:
                    result_info = learner.boss_miss(nickname, language)
                    st.session_state.boss_outcome = result_info["result"] if result_info["finished"] else "miss"
                    st.session_state.boss_question_number = result_info["question_number"]
                    st.session_state.boss_correct_so_far = result_info["correct_so_far"]
                    st.session_state.boss_bonus_xp = result_info["bonus_xp"]
                else:
                    st.session_state.revealed = True
                    st.session_state.quiz_was_wrong = True
            new_level_info = learner.get_level_info(nickname)
            if new_level_info["tier"] != old_tier:
                st.session_state.rank_up_info = {
                    "new_tier": new_level_info["tier"],
                    "new_level": new_level_info["level"],
                }
            elif new_level_info["level"] != old_level:
                st.session_state.level_up_info = {"new_level": new_level_info["level"]}
            st.rerun()

else:
    if st.session_state.pop("quiz_was_wrong", False):
        st.warning(strings["quiz_wrong"])

    examples_html = "".join(f'<div class="example-line"><em>{ex}</em></div>' for ex in word["examples"])
    render_encounter(MONSTER_SVG, "monster-attacking")
    st.markdown(hp_bar_html(100, label=strings["monster_hp_label"]), unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="word-card hurt">
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
    remaining_seconds, percent_elapsed = learner.get_time_remaining(nickname, language)
    hours = int(remaining_seconds // 3600)
    minutes = int((remaining_seconds % 3600) // 60)
    countdown_label = strings["countdown_format"].format(h=hours, m=minutes)
    st.markdown(countdown_ring_html(percent_elapsed, countdown_label), unsafe_allow_html=True)
