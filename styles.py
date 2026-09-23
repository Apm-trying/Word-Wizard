# All visual styling lives here — CSS injected into the Streamlit page.
# Design concept: a dictionary index card resting on a dark study desk.
# The word itself is the hero, set in a characterful serif; everything
# else (labels, topics, buttons) stays quiet and out of its way.

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap');

:root {
    --ink: #14181F;
    --ink-deep: #0D1015;
    --paper: #EFE7D3;
    --paper-text: #201C14;
    --accent: #C79A3C;
    --accent-deep: #A67D2C;
    --success: #5F8B6F;
    --muted: #9CA3AE;
}

/* Page background — twilight gradient instead of flat dark, sets the mood for the tower */
.stApp {
    background: radial-gradient(ellipse at top, #241B3A 0%, #14181F 65%);
}

/* Hide Streamlit's default footer for a cleaner, more "app-like" feel */
footer { visibility: hidden; }

/* Body text defaults */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    color: #EDE6D6;
}

/* The word card itself */
.word-card {
    background-color: var(--paper);
    color: var(--paper-text);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
    margin-bottom: 1.5rem;
}

.topic-tag {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent-deep);
    background-color: rgba(199, 154, 60, 0.15);
    border: 1px solid rgba(199, 154, 60, 0.4);
    border-radius: 999px;
    padding: 0.3rem 0.8rem;
    margin-bottom: 1rem;
}

.word-display {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 2.6rem;
    line-height: 1.15;
    margin: 0.2rem 0 0.4rem 0;
}

.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted-on-paper, #6B665A);
    margin-top: 1.2rem;
    margin-bottom: 0.2rem;
}

.example-line {
    margin-top: 0.4rem;
}

.example-line:first-child {
    margin-top: 0;
}

.xp-badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.05em;
    color: var(--muted);
    border: 1px solid rgba(237, 230, 214, 0.2);
    border-radius: 999px;
    padding: 0.25rem 0.7rem;
}

/* Wraps the main status pill (streak/level/rank/XP) and the smaller daily-
   goal pill so they can sit side by side on desktop but stack as two short,
   separate lines on mobile instead of both being crammed into one bubble
   (see the mobile media query below). */
.status-pills {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    flex-wrap: wrap;
    margin-bottom: 0.8rem;
}

/* Deliberately smaller/quieter than .xp-badge -- it's a secondary indicator,
   not part of the main progression status. */
.daily-goal-badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.05em;
    color: var(--muted);
    opacity: 0.75;
    border: 1px solid rgba(237, 230, 214, 0.12);
    border-radius: 999px;
    padding: 0.2rem 0.55rem;
    white-space: nowrap;
}

/* App-wide title on the language/topic setup screens */
.app-title {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 2.7rem;
    text-align: center;
    margin-bottom: 0.2rem;
    color: #F5F1E6 !important;
}

.app-subtitle {
    font-family: 'IBM Plex Sans', sans-serif;
    color: #C9CDD6 !important;
    text-align: center;
    margin-bottom: 2rem;
}

.hero-title {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 3rem;
    line-height: 1.05;
    text-align: center;
    color: #F5F1E6 !important;
    text-transform: uppercase;
    letter-spacing: 0.02em;
    margin-bottom: 0.4rem;
}

.hero-title-gold {
    color: var(--accent) !important;
}

.value-prop-row {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--accent);
    text-align: center;
    margin-bottom: 1.5rem;
}

.no-account-caption {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.8rem;
    color: var(--muted);
    text-align: center;
    margin-top: 0.6rem;
}

.subtitle-banner {
    display: inline-block;
    background: rgba(199, 154, 60, 0.12);
    border: 1px solid rgba(199, 154, 60, 0.3);
    border-radius: 999px;
    padding: 0.5rem 1.2rem;
    margin: 0 auto 1.2rem;
    color: #E8DFC8 !important;
    font-size: 0.95rem;
}

.feature-col {
    text-align: center;
    padding: 0 0.3rem;
}
.feature-col .feature-icon {
    font-size: 1.6rem;
    margin-bottom: 0.2rem;
}
.feature-col .feature-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.2rem;
}
.feature-col .feature-desc {
    font-size: 0.75rem;
    color: var(--muted);
    line-height: 1.3;
}

.trust-badge {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.5rem 0;
}
.trust-badge .trust-icon {
    font-size: 1.1rem;
    line-height: 1.4;
}
.trust-badge .trust-title {
    font-size: 0.8rem;
    font-weight: 500;
    color: #EDE6D6;
    margin: 0;
}
.trust-badge .trust-desc {
    font-size: 0.72rem;
    color: var(--muted);
    margin: 0;
}

/* Theme Streamlit's selectbox dropdown to match the dark palette */
/* Theme the topic multiselect's selected-chip color: gold (unlocked/chosen)
   instead of Streamlit's default red (which reads as danger/error/delete
   against our theme, not "selected and valuable"). */
span[data-tag] {
    background-color: rgba(199, 154, 60, 0.75) !important;
    border: 1px solid rgba(138, 106, 40, 0.9) !important;
    color: #2A1F0C !important;
}
span[data-tag] button svg {
    stroke: #2A1F0C !important;
}
div[data-testid="stMultiSelect"] div[data-rac][role="group"] {
    background-color: #1C2029 !important;
    border: 1px solid rgba(237,230,214,0.25) !important;
}

div[data-testid="stSelectbox"] > div > div {
    background-color: #1C2029 !important;
    border: 1px solid rgba(237,230,214,0.25) !important;
    border-radius: 999px !important;
}
div[data-testid="stSelectbox"] * {
    color: #EDE6D6 !important;
}
div[data-testid="stSelectbox"] svg {
    fill: #EDE6D6 !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] {
    background-color: #1C2029 !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] li {
    background-color: #1C2029 !important;
    color: #EDE6D6 !important;
}

/* Make sure Streamlit's own widget text (radio labels, captions) stays
   bright and readable on our dark background, regardless of the user's
   system light/dark mode, which Streamlit would otherwise inherit from. */
div[data-testid="stRadio"] label p,
div[data-testid="stMarkdownContainer"] p {
    color: #EDE6D6 !important;
}

/* Countdown ring for the locked state */
.countdown-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 1rem;
}

.countdown-ring {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.6rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: var(--paper-text);
}

.countdown-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    color: var(--muted);
    text-transform: uppercase;
}

/* Buttons: pill-shaped, quiet by default, gold when primary */
div[data-testid="stButton"] button {
    border-radius: 999px;
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 500;
    border: 1px solid rgba(237, 230, 214, 0.25);
    background-color: transparent;
    color: #EDE6D6;
    transition: all 0.15s ease;
}

div[data-testid="stButton"] button:hover {
    border-color: var(--accent);
    color: var(--accent);
}

div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(180deg, #D9AC4E 0%, #C79A3C 55%, #A67D2C 100%);
    border: 1px solid #8A6A28;
    border-radius: 10px;
    color: #2A1F0C;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.35),
        inset 0 -2px 3px rgba(0,0,0,0.15),
        0 2px 4px rgba(0,0,0,0.25);
}

div[data-testid="stButton"] button[kind="primary"]:hover {
    background: linear-gradient(180deg, #E3B95C 0%, #D2A544 55%, #B08430 100%);
    border-color: #8A6A28;
    color: #2A1F0C;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.4),
        inset 0 -2px 3px rgba(0,0,0,0.15),
        0 0 14px rgba(199,154,60,0.5),
        0 2px 4px rgba(0,0,0,0.25);
}

div[data-testid="stButton"] button[kind="primary"]:active {
    transform: scale(0.98);
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.35);
}

div[data-testid="stButton"] button[kind="primary"]:focus-visible {
    outline: 2px solid #F0C674;
    outline-offset: 2px;
}

/* Center the narrower "log back in" link-style button (it doesn't use
   use_container_width, so it shrink-wraps to its own content — margin
   auto centers a shrink-wrapped block within its stretched flex parent) */
div[data-testid="stElementContainer"]:has(button[data-testid="stBaseButton-tertiary"]) {
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Monster encounter — a light cosmetic reskin of the existing correct/wrong
   mechanic. No new game rules, just visual stakes on top of what already exists. */
.hp-bar-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-align: center;
    color: var(--muted);
    margin-top: 0.3rem;
}
.hp-bar-track {
    width: 120px;
    height: 8px;
    background: rgba(237,230,214,0.15);
    border-radius: 999px;
    overflow: hidden;
    margin: 0.4rem auto 0.8rem;
}
.hp-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #E24B4A, #F0C674);
    border-radius: 999px;
}

@keyframes monsterIdleSway {
    0%, 100% { transform: rotate(-2deg); }
    50% { transform: rotate(2deg); }
}
.monster-idle svg { animation: monsterIdleSway 3s ease-in-out infinite; transform-origin: bottom center; }

@keyframes bossAura {
    0%, 100% { box-shadow: 0 0 20px 4px rgba(140, 40, 140, 0.35); }
    50% { box-shadow: 0 0 32px 10px rgba(140, 40, 140, 0.55); }
}
.boss-encounter {
    display: flex;
    justify-content: center;
    border-radius: 50%;
    animation: bossAura 2s ease-in-out infinite, monsterIdleSway 3.5s ease-in-out infinite;
    transform-origin: bottom center;
}
.boss-label {
    text-align: center;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    color: #D68CD6;
    margin-bottom: 0.3rem;
}
.boss-hp-track {
    width: 160px;
    height: 10px;
    background: rgba(237,230,214,0.15);
    border-radius: 999px;
    overflow: hidden;
    margin: 0.4rem auto 0.8rem;
    display: flex;
}
.boss-hp-pip {
    flex: 1;
    border-right: 2px solid rgba(20,24,31,0.6);
}
.boss-hp-pip.filled { background: linear-gradient(90deg, #8C288C, #D68CD6); }
.boss-hp-pip:last-child { border-right: none; }

@keyframes hpDrain {
    0% { width: 100%; }
    100% { width: 0%; }
}
.hp-bar-fill.draining { animation: hpDrain 1s ease-out forwards; }

@keyframes monsterDefeat {
    0% { opacity: 1; transform: scale(1) rotate(0deg); }
    100% { opacity: 0.35; transform: scale(0.82) rotate(-10deg); }
}
.monster-defeated svg { animation: monsterDefeat 1s ease-out forwards; }

@keyframes monsterAttack {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-6px); }
    40% { transform: translateX(6px); }
    60% { transform: translateX(-4px); }
    80% { transform: translateX(4px); }
}
.monster-attacking svg { animation: monsterAttack 0.5s ease-in-out; }

@keyframes cardFlashHurt {
    0%, 100% { box-shadow: 0 12px 40px rgba(0,0,0,0.35); }
    30% { box-shadow: 0 0 0 6px rgba(226,75,74,0.55), 0 12px 40px rgba(0,0,0,0.35); }
}
.word-card.hurt { animation: cardFlashHurt 0.5s ease-in-out; }

/* Respect reduced-motion preference */
@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; animation: none !important; }
}

/* Subtle micro-interactions on the tower scene and CTA */
@keyframes windowFlicker {
    0%, 100% { opacity: 0.18; }
    45% { opacity: 0.24; }
    50% { opacity: 0.12; }
    55% { opacity: 0.20; }
}
.window-glow { animation: windowFlicker 4s ease-in-out infinite; }

@keyframes rainFall {
    0% { transform: translateY(-4px); opacity: 0.2; }
    50% { opacity: 0.7; }
    100% { transform: translateY(10px); opacity: 0.2; }
}
.rain-group line { animation: rainFall 1.1s linear infinite; }
.rain-group line:nth-child(2) { animation-delay: 0.15s; }
.rain-group line:nth-child(3) { animation-delay: 0.3s; }
.rain-group line:nth-child(4) { animation-delay: 0.05s; }
.rain-group line:nth-child(5) { animation-delay: 0.2s; }
.rain-group line:nth-child(6) { animation-delay: 0.4s; }
.rain-group line:nth-child(7) { animation-delay: 0.1s; }
.rain-group line:nth-child(8) { animation-delay: 0.35s; }
.rain-group line:nth-child(9) { animation-delay: 0.25s; }
.rain-group line:nth-child(10) { animation-delay: 0.5s; }

@keyframes lightningFlash {
    0%, 92%, 94%, 96%, 100% { opacity: 0; }
    93% { opacity: 0.85; }
    95% { opacity: 0.5; }
}
.lightning-flash { animation: lightningFlash 7s infinite; }

@keyframes lightningGlow {
    0%, 92%, 94%, 96%, 100% { opacity: 0; }
    93% { opacity: 0.3; }
    95% { opacity: 0.15; }
}
.lightning-glow { animation: lightningGlow 7s infinite; }

@keyframes rainRipple {
    0% { transform: scale(0.3); opacity: 0.5; }
    100% { transform: scale(2.6); opacity: 0; }
}
.ripple-group circle {
    animation: rainRipple 1.6s ease-out infinite;
    transform-box: fill-box;
    transform-origin: center;
}
.ripple-group circle:nth-child(2) { animation-delay: 0.35s; }
.ripple-group circle:nth-child(3) { animation-delay: 0.7s; }
.ripple-group circle:nth-child(4) { animation-delay: 1.05s; }
.ripple-group circle:nth-child(5) { animation-delay: 1.4s; }
.ripple-group circle:nth-child(6) { animation-delay: 0.15s; }
.ripple-group circle:nth-child(7) { animation-delay: 0.5s; }
.ripple-group circle:nth-child(8) { animation-delay: 0.85s; }
.ripple-group circle:nth-child(9) { animation-delay: 1.2s; }
.ripple-group circle:nth-child(10) { animation-delay: 0.6s; }


@keyframes idleBounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
}
.wizard-figure { animation: idleBounce 2.4s ease-in-out infinite; transform-origin: center bottom; }

@keyframes auraPulse {
    0%, 100% { opacity: 0.15; r: 10; }
    50% { opacity: 0.35; r: 14; }
}
.wizard-aura { animation: auraPulse 2.2s ease-in-out infinite; transform-origin: center; }

.encounter-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    padding: 0 12%;
    min-height: 60px;
}
.encounter-row .wizard-slot,
.encounter-row .enemy-slot {
    flex: 0 0 auto;
}

@keyframes spellTravel {
    0% { left: 22%; opacity: 0; transform: translate(-50%, -50%) scale(0.6); }
    15% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
    80% { opacity: 1; }
    100% { left: 78%; opacity: 0; transform: translate(-50%, -50%) scale(1.1); }
}
.spell-projectile {
    position: absolute;
    top: 50%;
    left: 22%;
    transform: translate(-50%, -50%);
    animation: spellTravel 0.7s ease-in forwards;
    pointer-events: none;
}

@keyframes ctaPulse {
    0%, 100% {
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.35),
            inset 0 -2px 3px rgba(0,0,0,0.15),
            0 2px 4px rgba(0,0,0,0.25),
            0 0 0 0 rgba(199,154,60,0.5);
    }
    50% {
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.35),
            inset 0 -2px 3px rgba(0,0,0,0.15),
            0 2px 4px rgba(0,0,0,0.25),
            0 0 0 8px rgba(199,154,60,0);
    }
}
div[data-testid="stButton"] button[kind="primary"] {
    animation: ctaPulse 2.5s ease-in-out 2.5s infinite;
}

/* --- Boss two-stage reveal: entrance banner, punchier hit/miss feedback,
   and an enlarged "portrait" treatment for the boss on the final outcome
   screen. All reuse the existing boss SVG, aura and HP-pip system. --- */
@keyframes bossEntrancePlay {
    /* Quick pop-in, then a long hold at full visibility -- the previous
       version faded back out starting at 72% of a 1.2s animation, leaving
       well under a second of genuinely readable time. This version holds
       at full opacity from ~0.16s to ~1.44s (~1.28s of solid read time)
       before fading, out of a slower 1.8s total. */
    0% { opacity: 0; transform: scale(0.88); }
    9% { opacity: 1; transform: scale(1.04); }
    15% { transform: scale(1); }
    80% { opacity: 1; }
    100% { opacity: 0; transform: scale(1); }
}
@keyframes bossEntranceCollapse {
    /* Only starts shrinking once the text has already faded out (90% =
       1.62s of 1.8s), so the collapse never visibly clips readable
       content -- previously it began at 82% of a 1.2s animation, while
       opacity was still well above 0, which read as an abrupt cut. */
    0%, 90% { max-height: 140px; margin-bottom: 0.7rem; }
    100% { max-height: 0; margin-bottom: 0; }
}
.boss-entrance {
    text-align: center;
    padding: 0.75rem 0.5rem;
    border-radius: 14px;
    background: radial-gradient(circle, rgba(92,31,61,0.45) 0%, rgba(20,10,28,0.1) 78%);
    overflow: hidden;
    animation: bossEntrancePlay 1.8s ease-out forwards, bossEntranceCollapse 1.8s ease-out forwards;
}
.boss-entrance-arrives {
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.22em;
    font-size: 0.8rem;
    color: #F0C674;
    text-shadow: 0 0 12px rgba(240,198,116,0.7);
}
.boss-entrance-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: #EDE6D6;
    margin-top: 0.25rem;
    letter-spacing: 0.04em;
    text-shadow: 0 0 18px rgba(140,40,140,0.85);
}
.boss-entrance-subtitle {
    font-size: 0.78rem;
    font-style: italic;
    color: #D6B8E8;
    margin-top: 0.15rem;
}

@keyframes feedbackPop {
    0% { transform: scale(0.7); opacity: 0; }
    45% { transform: scale(1.08); opacity: 1; }
    65% { transform: scale(1); }
    100% { transform: scale(1); opacity: 1; }
}
.boss-feedback {
    text-align: center;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.06em;
    border-radius: 12px;
    padding: 0.6rem 1rem;
    margin: 0.5rem 0 0.8rem;
    animation: feedbackPop 0.45s ease-out;
}
.boss-feedback-hit {
    font-size: 1.25rem;
    color: #2A1510;
    background: linear-gradient(90deg, #F0C674, #E8A93C);
    box-shadow: 0 0 22px rgba(240,198,116,0.55);
}
.boss-feedback-miss {
    font-size: 1.05rem;
    color: #F5E4E4;
    background: rgba(120,30,30,0.55);
    border: 1px solid rgba(226,75,74,0.6);
}
.boss-feedback-sub {
    display: block;
    font-size: 0.7rem;
    font-weight: 400;
    letter-spacing: 0.04em;
    opacity: 0.85;
    margin-top: 0.2rem;
}

/* Elevated final-outcome treatment: same BOSS_MONSTER_SVG, scaled up via
   CSS (overrides the SVG's own width attribute, no new artwork needed). */
.boss-portrait svg {
    width: 168px;
    height: auto;
}
.boss-outcome-heading {
    text-align: center;
    margin: 0.6rem 0 0.2rem;
}
.boss-outcome-name {
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #EDE6D6;
}
.boss-outcome-subtitle {
    font-size: 0.75rem;
    font-style: italic;
    color: #C9A8DE;
    margin-top: 0.1rem;
}

/* --- Level-up / rank-up celebrations. Ordinary level-ups get a small
   one-shot badge on the screen that's already showing (no extra click);
   crossing into a new rank tier gets a dedicated full celebratory screen,
   reusing the existing wizard-avatar tier system. --- */
@keyframes levelUpBadgePop {
    0% { transform: scale(0.7); opacity: 0; }
    45% { transform: scale(1.08); opacity: 1; }
    65% { transform: scale(1); }
    100% { transform: scale(1); opacity: 1; }
}
.level-up-badge {
    text-align: center;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.06em;
    font-size: 0.95rem;
    color: #2A1510;
    background: linear-gradient(90deg, #F0C674, #E8A93C);
    border-radius: 999px;
    padding: 0.45rem 1rem;
    margin: 0 0 0.8rem;
    box-shadow: 0 0 16px rgba(240,198,116,0.5);
    animation: levelUpBadgePop 0.45s ease-out;
}

@keyframes rankUpAura {
    0%, 100% { box-shadow: 0 0 26px 6px rgba(240,198,116,0.4); }
    50% { box-shadow: 0 0 42px 14px rgba(240,198,116,0.65); }
}
@keyframes rankUpEnter {
    0% { opacity: 0; transform: scale(0.85) translateY(10px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}
.rankup-screen {
    text-align: center;
    animation: rankUpEnter 0.5s ease-out;
}
.rankup-portrait {
    display: flex;
    justify-content: center;
    margin: 0.4rem auto 0.6rem;
    width: 130px;
    height: 130px;
    border-radius: 50%;
    align-items: center;
    background: radial-gradient(circle, rgba(199,154,60,0.22) 0%, rgba(20,10,28,0.05) 75%);
    animation: rankUpAura 2s ease-in-out infinite;
}
.rankup-portrait svg {
    width: 92px;
    height: auto;
}
.rankup-title {
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.2em;
    font-size: 0.9rem;
    color: #F0C674;
    text-shadow: 0 0 14px rgba(240,198,116,0.8);
    margin-bottom: 0.3rem;
}
.rankup-name {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 2.2rem;
    line-height: 1.1;
    background: linear-gradient(90deg, #F0C674, #EDE6D6 50%, #F0C674);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0 0 24px rgba(240,198,116,0.5);
    margin-bottom: 0.3rem;
}
.rankup-level {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    color: #D6B8E8;
    margin-bottom: 0.6rem;
}
.rankup-flavor {
    font-size: 0.9rem;
    font-style: italic;
    color: #C9A8DE;
    margin-bottom: 1rem;
}

/* --- Progression screen. The hero (avatar/rank name/level) reuses the
   .rankup-portrait/.rankup-name/.rankup-level classes above as-is, so the
   focal treatment matches the rank-up celebration exactly. Only the XP
   progress bar, next-rank line, and rank ladder below are new. --- */
.progression-xp-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    text-align: center;
    margin-top: 0.4rem;
}
.progression-xp-track {
    width: 220px;
    height: 10px;
    background: rgba(237,230,214,0.15);
    border-radius: 999px;
    overflow: hidden;
    margin: 0.4rem auto 0.3rem;
}
.progression-xp-fill {
    height: 100%;
    background: linear-gradient(90deg, #8C288C, #F0C674);
    border-radius: 999px;
}
.progression-xp-remaining {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #D6B8E8;
    text-align: center;
    margin-bottom: 0.5rem;
}
.progression-next-rank {
    text-align: center;
    font-size: 0.85rem;
    font-style: italic;
    color: #C9A8DE;
    margin-bottom: 1.4rem;
}
.progression-next-rank strong {
    color: #F0C674;
    font-style: normal;
}

.rank-ladder-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0.2rem;
    border-bottom: 1px solid rgba(42,21,16,0.12);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
}
.rank-ladder-row:last-child { border-bottom: none; }
.rank-ladder-name {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: 0.01em;
}
.rank-ladder-row.completed { opacity: 0.7; }
.rank-ladder-row.completed .rank-ladder-name { color: #8C6A2E; }

.rank-ladder-row.current {
    background: rgba(199,154,60,0.14);
    border-radius: 10px;
    padding: 0.7rem 0.7rem;
    border-bottom: none;
    box-shadow: 0 0 0 1.5px rgba(199,154,60,0.55) inset;
}
.rank-ladder-row.current .rank-ladder-name { color: #A6631E; }
.rank-ladder-row.current .rank-ladder-level { color: #A6631E; }

.rank-ladder-row.future { opacity: 0.45; }
.rank-ladder-row.future .rank-ladder-name { color: #4A453B; }

.rank-ladder-level {
    color: #6B665A;
    font-size: 0.72rem;
}

/* Mobile-only tightening for the progression screen so it fits closer to
   one viewport on a typical phone. Scoped to .progression-hero (an extra
   class alongside .rankup-screen, added only on this screen's hero) and
   .progression-ladder-card (an extra class alongside .word-card, added
   only on this screen's ladder), so the shared rank-up celebration screen
   and the leaderboard/My Words cards are completely unaffected. Desktop
   (>480px) is untouched -- these rules only apply below that width. */
@media (max-width: 480px) {
    .progression-hero .rankup-portrait {
        width: 96px;
        height: 96px;
        margin: 0.15rem auto 0.3rem;
    }
    .progression-hero .rankup-portrait svg {
        width: 64px;
    }
    .progression-hero .rankup-name {
        font-size: 1.7rem;
        margin-bottom: 0.15rem;
    }
    .progression-hero .rankup-level {
        font-size: 0.78rem;
        margin-bottom: 0.25rem;
    }
    .progression-xp-label {
        margin-top: 0.2rem;
        font-size: 0.6rem;
    }
    .progression-xp-track {
        margin: 0.25rem auto 0.15rem;
    }
    .progression-xp-remaining {
        font-size: 0.68rem;
        margin-bottom: 0.25rem;
    }
    .progression-next-rank {
        font-size: 0.78rem;
        margin-bottom: 0.6rem;
    }
    .progression-ladder-card.word-card {
        padding: 1.1rem 1rem;
        margin-bottom: 0.6rem;
    }
    .progression-ladder-card .rank-ladder-row {
        padding: 0.42rem 0.15rem;
        font-size: 0.72rem;
    }
    .progression-ladder-card .rank-ladder-row.current {
        padding: 0.5rem 0.55rem;
    }
    .progression-ladder-card .rank-ladder-name {
        font-size: 0.88rem;
    }
}

/* --- Main word-screen mobile tightening. Goal: the word card, its
   question, and the primary "Yes, I know this" button all fit in one
   phone screen without scrolling. Three things were eating the space:
   1) Streamlit's own responsive behavior stacks st.columns() vertically
      below a width threshold -- the 4 top-nav icon buttons were each
      getting their own full-width row instead of sitting in one row.
      Fixed by forcing nowrap on that specific row only (scoped to the
      "top-nav" keyed container from app.py's st.container(key="top-nav"),
      so no other st.columns() elsewhere in the app is affected).
   2) Streamlit's default page padding-top (96px) and the ~16px gap
      between every top-level element add up fast on a short screen.
      Trimmed both, scoped to the outermost content flow only (the
      direct-child selector below reaches just the page's top-level
      block, not the layout inside columns/cards elsewhere).
   3) The encounter row and word-card had comfortable-but-not-essential
      padding/margins that a phone doesn't have room for. Desktop is
      untouched -- none of this applies above 480px. --- */
@media (max-width: 480px) {
    /* 1) Keep the top-nav row horizontal instead of letting Streamlit
       stack it into 4 separate full-width rows. */
    .st-key-top-nav div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 6px !important;
    }
    .st-key-top-nav div[data-testid="stColumn"] {
        min-width: 0 !important;
        width: auto !important;
    }
    .xp-badge {
        font-size: 0.62rem;
        padding: 0.22rem 0.5rem;
        text-align: center;
    }
    /* Two separate, short pills stacked one per line -- instead of one
       bordered bubble trying to fit streak+level+rank+XP+daily-goal all at
       once, which is what was wrapping awkwardly before this change. */
    .status-pills {
        flex-direction: column;
        align-items: center;
        gap: 0.2rem;
        margin-bottom: 0.5rem;
    }
    .daily-goal-badge {
        font-size: 0.58rem;
        padding: 0.16rem 0.5rem;
    }

    /* 2) Reserve less dead space above the first element, and tighten
       the gap Streamlit inserts between each top-level block. Streamlit's
       own header toolbar is a fixed/absolute 60px bar that overlaps the
       page rather than pushing it down, so padding-top can't go below
       that without content hiding under the toolbar -- 68px keeps a
       small buffer below it while still saving ~28px over the default. */
    div[data-testid="stMainBlockContainer"] {
        padding-top: 68px !important;
    }
    div[data-testid="stMainBlockContainer"] > div[data-testid="stVerticalBlock"] {
        gap: 8px !important;
    }

    /* 3) Trim the encounter row and word card just enough to help the
       primary button fit, without shrinking the word itself or making
       the layout feel cramped. */
    .encounter-row {
        min-height: 46px;
        padding: 0 14%;
    }
    .hp-bar-track, .boss-hp-track {
        margin: 0.25rem auto 0.5rem;
    }
    .word-card {
        padding: 1.5rem 1.5rem;
        margin-bottom: 0.8rem;
    }
}
</style>
"""


def countdown_ring_html(percent_elapsed, remaining_label):
    """
    Builds a small circular progress ring (CSS conic-gradient) showing
    how far through the 12h wait we are, with the remaining time as a caption.
    """
    ring_style = (
        f"background: conic-gradient(var(--accent) {percent_elapsed}%, "
        f"rgba(32,28,20,0.12) {percent_elapsed}%);"
    )
    return f"""
    <div class="countdown-wrap">
        <div class="countdown-ring" style="{ring_style}">
            <div style="background: var(--paper); width: 46px; height: 46px; border-radius: 50%;
                        display: flex; align-items: center; justify-content: center;">
                ⏳
            </div>
        </div>
        <div class="countdown-label">{remaining_label}</div>
    </div>
    """


def chime_audio_html():
    return f'''<audio autoplay="true" style="display:none;">
<source src="data:audio/wav;base64,{CHIME_SOUND_B64}" type="audio/wav">
</audio>'''


def daily_goal_chime_audio_html():
    """
    A distinct short ascending 4-note chime (separate from the plain
    correct-answer chime above) played once, only when the daily 'Learn
    5 new words' goal is completed -- so hitting the goal sounds like its
    own small event rather than just another correct answer.
    """
    return f'''<audio autoplay="true" style="display:none;">
<source src="data:audio/wav;base64,{DAILY_GOAL_CHIME_SOUND_B64}" type="audio/wav">
</audio>'''


HAT_ICON_SVG = """
<div style="display:flex; justify-content:center; margin-bottom: 0.3rem;">
<svg viewBox="0 0 100 100" width="52" xmlns="http://www.w3.org/2000/svg">
<path d="M 50 10 L 72 68 Q 50 80 28 68 Z" fill="#7B7F92" stroke="#4A4E5E" stroke-width="2"/>
<ellipse cx="50" cy="68" rx="30" ry="8" fill="#5B6578" stroke="#4A4E5E" stroke-width="2"/>
<circle cx="50" cy="44" r="4" fill="#EFE7D3"/>
</svg>
</div>
"""


CHIME_SOUND_B64 = "UklGRkI3AABXQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAAZGF0YR43AAAAAAcAHQBAAG8AqADnACsBcAGyAe0BHwJEAlkCWwJIAh8C4AGKAR0BnQAKAGr/vf4J/lT9ofz2+1n7z/pc+gf60vnB+db5FPp6+gn7v/uY/JP9qf7V/xABVAKaA9gEBwYfBxgI6giQCQMKPgo/CgMKiAnRCN4HtQZZBdIDJwJiAIz+r/zX+g/5Yvfb9YP0ZfOJ8vbxsfG98R7y0vLY8yv1x/aj+LX69PxS/8IBOASkBvcIJAseDdYOQhBXEQ4SYRJKEskR3hCND9oNzwt1CdgGBwQQAQX+9vr29xX1ZvL5793tIOzO6vDpjumr6UrqaOsD7RHvivFh9Ib36vp5/h4CxgVdCcwM/g/iEmMVdBcGGQ0agxpiGqkZWhh6FhIULhHcDTAKOwYVAtX9kvll9Wfxr+1T6mnnAuUt4/nhbOGN4V7i2+P+5b3oCuzU7wf0i/hI/SICAAfEC1MQkxRpGL4bfh6YIP0hoyKFIqEh+R+WHYMazxaOEtcNxAhxA/z9hPgn8wbuPunr5CjhDN6q2y/andnm2Qfb+ty03ybjO+fd6/LwXPb9+7QBYgfmDCAS9BZGG/weAiJIJL8lXyYmJhQlLyODIB4dExl6FGwPBwppBLP+BPl78zvuX+kD5UHhLt7b21XapdnP2dLaqNxH36Din+Yv6zbwlfUw++YAlwYjDGoRThazGoEeoSECJJclViY7JkglgCPvIKIdrRknFSgQzgo2BYH/zvk/9PLuBuqX5b7hkd4i3H/asNm82aDaWdzd3h3iBuaE6nvv0PRk+hgAzAVfC7EQpRUeGgIePCG5I2slSCZMJnclzCNXISMeRRrRFeIQkgsBBk4AmvoD9avvsOou5j/i+N5u3K3awNmt2XPaD9x33p3hcOXa6cLuDPSZ+Uv/AAWaCvcP+hSFGYAd0yBrIzolNiZZJqIlFSS7IaEe2hp6FpoRVgzMBhwBZvvJ9WfwXevI5sPiY9+93N/a1Nmi2UraydsU3iHh3eQz6QvuSfPP+H3+NATTCTsPTBTqGPocZiAaIwYlICZhJsklWSQbIhwfaxsfF1ASGA2WB+kBM/yQ9iTxC+xl50rj0t8R3Rbb7dmc2Sbahtu23ajgTeSP6Fbth/IF+LD9ZwMMCX0OnBNMGHIc9h/EIs0kBSZlJuslmSR4IpMf+hvCFwQT2Q1gCLcCAP1Y9+LxvOwE6NTjROBo3VHbCtqa2QXaSNtb3TPgwOPt56Psx/E89+L8mgJDCL4N6hKrF+Ybgh9rIpEk5iVlJgkm1iTRIgYghRxjGLYTmA4oCYQDzf0h+KPycO2m6GHkueDD3Y/bK9qd2enZDtsE3cLfNuNO5/LrCfF09hX8zAF6B/0MNhIIF1cbCh8OIlAkwyVgJiMmDiUmI3YgDh0AGWUUVg/wCVEEm/7r+GTzJe5L6fLkM+Ei3tLbUNqk2dHZ2Nqx3FTfr+Ky5kTrTPCt9Un7/gCvBjoMgBFiFsUakB6tIQsknCVXJjkmQiV3I+Igkx2bGRIVEhC2Ch0Faf+2+Sf03O7y6YXlr+GF3hncedqv2b7Zptpj3OneLOIY5pjqke/n9H36MQDkBXYLyBC5FTAaER5IIcIjcCVKJkomcSXDI0ohFB4zGr0VzBB7C+kFNQCC+uz0le+c6hzmL+Ls3mTcp9q+2a7ZeNoY3IPerOGC5e7p2O4j9LH5ZP8YBbEKDRAOFZgZjx3fIHUjQCU5JlgmnSUMJK8hkx7IGmYWhBE/DLQGAwFO+7L1UPBI67bms+JW37Pc2drS2aPZT9rR2yDeMOHu5EfpIe5g8+f4lv5MBOsJUQ9hFP0YCh1zICQjDCUjJmAmxCVRJBAiDR9aGwwXOhIBDX4H0QEa/Hn2DfH361LnOePE3wbdD9vq2Z3ZKtqO28Hdt+Be5KLoa+2e8h34yP1/AyQJlA6xE18YghwDIM8i1CQJJmUm5yWSJG0ihR/pG68X7hLCDUgInwLn/EH3zPGn7PHnw+M24F3dSdsG2prZCdpP22bdQeDR4wDouOze8VT3+/yyAlsI1Q0AE78X9xuQH3YimCTqJWUmBibPJMYi+B91HFAYoROCDhAJbAO1/Qr4jPJa7ZPoUOSr4LjdiNsn2pzZ7NkV2w7dz99G42HnB+wf8Yz2LvzlAZIHFA1MEhsXaBsZHxkiWCTIJWEmICYHJRwjaSD+HO4YUBRAD9gJOQSC/tP4TfMP7jfp4eQk4RfeyttL2qPZ1Nne2rvcYd+/4sTmWeti8MX1YfsXAccGUQyWEXYW1hqeHrkhEyShJVkmNyY8JW0j1SCDHYkZ/hT8D54KBQVQ/575EPTG7t7pdOWg4XneEdx02q3ZwNms2mzc9t484ivmrOqn7//0lfpJAPwFjgveEM0VQhogHlQhyyN2JUwmSSZsJbojPiEFHiEaqRW2EGQL0QUdAGn61fR/74jqCuYg4t/eW9yh2rzZsNl+2iDcj9674ZTlAuru7jr0yfl8/zEFyQokECMVqhmfHewgfiNGJTsmViaYJQQkoyGEHrcaUhZuESgMnAbrADX7mvU68DPro+aj4knfqtzT2s/ZpdlU2tnbLN4+4QDlW+k27nfz//iu/mQEAwpoD3YUDxkaHYAgLSMTJSYmYCbAJUkkBSL/Hkkb+BYlEuoMZge5AQL8Yfb38OLrP+cp47ff/NwI2+fZndku2pbbzN3F4G/ktuiB7bXyNfjh/ZgDOwmrDsYTchiTHBEg2SLbJAwmZSbjJYskYiJ3H9gbnBfZEqsNMAiGAs/8Kfe18ZLs3uez4yjgU91C2wLamtkN2lbbcN1P4OHjE+jN7PXxbPcT/csCcwjrDRUT0hcHHJ4fgSKfJO4lZSYCJsgkvCLrH2QcPRiLE2sO+QhTA5z98vd18kXtf+g/5J3grd2A2yLanNnv2RvbGd3c31fjdOcc7Dbxo/ZG/P0BqgcrDWESLxd5GycfJCJfJMwlYiYeJgElEiNcIO0c2xg8FCkPwAkgBGr+u/g28/rtI+nP5BXhC97C20faotnX2eTaxdxu38/i1+Zt63nw3PV5+y8B4AZpDKsRihboGq0exCEbJKYlWiY0JjYlZCPJIHMddxnpFOUPhwrtBDj/hvn587Duyuli5ZHhbd4I3G/arNnC2bHaddwC30viPebB6r3vFvWt+mIAFQalC/QQ4hVTGjAeYCHTI3slTiZHJmYlsSMyIfYdDxqVFaAQTAu5BQQAUfq99Gnvc+r45RDi095S3Jzautmy2YPaKdyb3srhpeUW6gTvUfTi+ZX/SQXgCjoQNxW8Ga8d+SCHI0wlPSZVJpMl+yOXIXUepRo+FlgREAyEBtIAHfuD9STwH+uR5pPiPd+g3M3azdmm2Vja4ds33k3hEeVv6UzujvMX+cf+fQQaCn4PihQiGSodjSA3IxklKCZfJrslQST5IfAeOBvkFg8S0wxOB6AB6ftJ9uDwzess5xnjqt/y3ALb5Nme2TLandvX3dPggOTJ6JbtzPJN+Pn9sANTCcEO2xOFGKMcHiDjIuIkDyZkJt8lgyRXImkfxxuIF8QSlA0YCG4CtvwR957xfezL56LjG+BI3Tvb/9mb2RDaXtt73V3g8uMn6OPsC/KD9yz94wKLCAIOKhPlFxgcrB+LIqck8iVmJv8lwSSxIt0fVBwqGHYTVA7hCDsDhP3a917yL+1s6C7kj+Ci3XjbHtqb2fPZItsj3erfZ+OH5zHsTPG79l/8FgLCB0INdxJCF4obNh8vImck0CViJhsm+iQII04g3RzIGCcUEg+pCQgEUf6j+B/z5O0Q6b7kB+EA3rrbQtqh2dnZ69rP3Hvf3+Lp5oLrj/D09ZL7SAH4BoAMwRGdFvkavB7QISQkqiVbJjImMCVaI7wgYx1kGdUUzw9vCtQEH/9u+eLzmu626VDlguFh3gDcatqq2cTZt9p+3A/fW+JP5tXq0+8u9cb6egAtBr0LChH2FWUaPx5sIdwjgCVPJkUmYSWoIyYh5h39GYEVihA1C6AF7f85+qb0U+9f6ublAeLH3kncltq42bPZiNoy3Kfe2uG35SrqGu9p9Pr5rf9hBfgKUBBMFc4Zvh0FIZEjUiU/JlMmjiXzI4whZh6TGioWQxH5C2wGugAF+2v1DfAK637mg+Iw35fcx9rK2afZXdrq20PeXOEj5YLpYu6l8y/53/6VBDIKlQ+fFDQZOh2aIEEjHyUrJl4mtyU5JO4h4h4mG9EW+RG8DDYHiAHR+zH2yfC46xrnCeOd3/rcJtsm2v3ZrNot3HjefuEt5W/pLO5H86T4I/6kAwsJNw4LE20XRRt8HgIhyiLKI/4jZSMFIuUfFB2iGaMVLxFgDFIHIQLs/M/36PJS7ifqfuZr4/7gRN9G3gnejd7O38PhYeSY51TrgO8E9MT4p/2OAmEHAgxZEEwUxhe0GgYdsB6qH+8ffh9bHo4cIhomF6sTxg+OCxsHhwLt/WX5CfXz8Dnt7+ko5/LkWeNl4hrieeJ/4yXlYeck6l7t/fDq9BD5Vv2jAeAF9QnKDUoRYhQCFxoZoRqNG9wbjRuiGiIZFheKFI8RNg6TCroGwgLC/tD6A/dw8yvwRe3P6tboZOd/5i7mb+ZA553oe+rP7IzvoPL79Yf5Mf3jAIoEDwhgC2kOGxFmEz8VmxZ1F8gXkxfaFqAV7xPQEVAPfwxuCS0G0QJs/xL81fjI9fvyfvBf7qjsY+uV6kPqbOoP6yjsru2Z79zxavQ09yn6OP1PAF0DUQYbCaoL8A3iD3YRohJiE7MTkxMEEwsSrhD3Du8MowogCHYFtALr/yn9fvr696n1mvPW8WjwVe+k7ljucO7r7sbv+/CB8k/0WvaW+PX6av3n/1wCvQT8BgwJ5Ap4DMANtw5XD54PjA8iD2QOVg0BDGsKoAiqBpUEbAI9ABX+/vsF+jX4l/Y09RP0OvOs8mzyefLT8nbzXvSF9eP2b/gg+uz7yP2q/4UBUQMDBZMG9gcnCR8K2QpUC4sLgQs1C6sK5wnvCMgHeQYMBYkD+QFkANb+Vf3q+536dfl3+Kr3D/eq9n32hvbF9jf32Pel+Jb5qPrR+wz9Uf6Y/9kADwIyAz0EKAXxBZQGDAdaB3wHcwc/B+MGYwbCBQQFLwRHA1QCWgFgAGz/gv6n/eH8Mvyf+yr71Pqf+or6lfq/+gb7Z/vf+2r8BP2p/Vb+Bf+y/1kA9wCJAQsCfALYAh8DUANsA3IDYwNAAw0DygJ7AiECwQFcAfYAkQAxANf/hf88///+zv6q/pL+h/6H/pL+pv7C/uP+Cv8y/1v/g/+o/8j/4//4/wQACgAIAAAACQAkAE8AhwDHAAwBTwGLAboB2AHfAc0BngFTAewAawDV/y3/ev7E/RT9cPzj+3T7KvsL+xz7YPvX+4D8V/1X/nf/rgDyATYDbgSNBYUGTAfYBx8IHQjNBzAHSAYaBa8DEQJPAHj+nPzO+h75nvde9m311fSh9NT0cfV29tv3mPmf+979QQC2AiUFdgeUCWgL4AzsDX8OkA4cDiINqQu7CWYHvwTcAdb+x/vN+AL2g/No8cbvsO4y7lXuG+9/8Hny+vTt9zr7w/5pAg0GjAnFDJkP7RGoE7gUEBWpFIMTphEfDwMMawh2BEYAA/zQ99bzOfAd7aHq3Ojj58LnfegR6nTsku9S85T3NPwHAeUFnwoLD/4SUxbqGKcaeBtTGzQaIxgvFXARBQ0UCMkCVP3j96ny1+2a6Rrme+PV4T3huuFL4+fleOng7fvynfiT/qcEpApUEIAV+RmTHSsgqCH3IRMhAB/NG5YXfBKsDFgGuv8L+Ynyb+z15lDiq94r3Ona9NpP3PHexuKu53/tEfQX+0kCaAkxEGkW1htJIJojqSVlJsgl1iOhIEYc7RbFEAYK7QK6+630Bu4B6NTirt602wHapNmh2u7cd+Ad5bTqDPHq9xH/PwY3DbcThRluHkQi5iQ8Jjkm3iQ2IlsebhmcExkNIAby/sv37/Ca6gblZeDh3JnaotkF2r7bvd7o4hnoIu7L9Nn7DAMkCuEQBhdcHLEg4SPNJWUmoyWOIzggwRtPFhQQSQkqAvj68/Na7WnnVuJO3nbb5tmu2c/aP93o4KrlWOvB8an41P8AB+0NXRQWGuQemyIaJUwmJCalJNwh4R3aGPMSYQxfBS7+Dfc88PnpfeT435Tcb9qc2STaANwh32njs+jQ7of1nPzPA+AKkBGhF94cFiElJO4lYSZ6JUIjzB84G68VYg+LCGcBN/o687Ds1ebc4fLdPNvQ2b3ZAtuU3V3hOeb+63fyavmXAMAHow4CFaQaVh/uIkslWCYMJmkkfiFlHUQYSBKnC50Ea/1P9ovvWun2447fStxJ2prZRtpG3Iff7eNQ6X/vQ/Zf/ZEEmws9EjoYXR14IWUkCiZZJk4l8yJdH60aDRWuDswHowB2+YLyCOxC5mThmt0F277Zz9k42+zd1OHL5qXsLvMq+loBfwhXD6QVLxvFHz0jdyVgJvAlKSQdIeYcqxebEewK2wOo/JP12+6+6HLjJ98E3CbanNls2o/c8d905O/pMPAB9yL+UwVVDOgS0BjaHdYhoSQjJk0mHiWgIuseHxpoFPkNDAfh/7b4zPFj67Pl8OBF3dLar9nl2XLbSN5O4mDnT+3n8+z6HQI9CQkQRRa4GzEgiSOgJWUmzyXlI7ggZBwQF+0QMQoZA+b71/Qt7iPo8eLE3sLbB9qi2Zfa3Nxe4P3kkOrj8L/35f4UBg0NkRNkGVMeMCLaJDgmPSbqJEoidh6PGcITQg1MBh7/9vcX8b/qJuV/4PPco9qk2f/Zr9un3szi9+f77aH0rvvgAvoJuhDjFj4cmiDRI8UlZSarJZ4jUCDfG3MWPBB0CVYCJPsd9IHti+dy4mPeg9vs2avZxNot3c/giuUz65jxfvio/9UGxA04FPYZyR6IIg8lSSYpJrIk8CH9HfwYGROKDIsFWv4492TwHeqb5BDgpdx42p3ZHNrx2wrfTOOQ6KjuXPVw/KMDtgppEX4XwRwAIRYk5yViJoQlUyPlH1cb0xWLD7YIkwFi+mTz1+z25vfhB95I29XZudn22oHdQuEY5tjrTfI++WsAlAd6Dt0UhBo8H9siQCVWJhImdySTIYIdZhhvEtELyQSX/Xr2su9+6RTkpt9b3FHam9k+2jbccN/P4yzpV+8Y9jP9ZQRxCxYSGBhBHWIhVyQEJlsmWCUFI3cfzRoxFdcO9wfPAKH5rPIu7GPmf+Gt3RHbwdnK2Svb2N254armf+wF8//5LgFUCC4PgBUQG6wfLCNuJV8m9iU4JDMhAx3OF8IRFwsHBNT8vfUC7+Hoj+M+3xTcLdqb2WPaftzZ31Xky+kI8Nb29v0nBSsMwRKvGL4dwSGUJB4mUCYpJbMiBR8/Go0UIg44BwwA4fj18Yjr0+UK4Vjd3dqy2d/ZZNsz3jLiPucp7b3zwPrxARIJ4Q8hFpkbGSB4I5clZCbXJfUjzyCCHDMXFBFbCkUDEvwB9VTuRugN49re0dsO2qDZjdrK3EXg3uRr6rvwlPe5/ugF5AxrE0MZOB4cIs4kMyZBJvYkXiKQHrAZ5xNsDXcGSv8h+EDx5OpF5ZjgBd2u2qbZ+dmh25Ler+LV59Ttd/SC+7QCzwmSEL8WIByDIMEjvSVmJrQlryNoIP0blxZkEJ4JggJQ+0f0qO2t54/ied6R2/LZqdm62hrdteBq5Q7rb/FT+Hz/qQabDRIU1RmvHnQiAyVFJi4mvyQFIhkeHRk/E7QMtwWG/mP3jfBC6rrkKeC23ILan9kV2uLb894v427oge4y9UT8dwOMCkERXBejHOkgByTfJWMmjSVlI/4fdhv3FbMP4Qi/AY76jfP97BjnE+Ib3lXb2tm22erabd0o4fjls+sk8hP5PwBpB1EOuBRkGiMfySI1JVMmFyaEJKkhnh2IGJUS+wv1BMP9pfba76LpMuS932vcWdqb2TbaJtxY37HjCekw7+71B/05BEcL7xH1FyQdTCFIJP4lXSZiJRcjkB/sGlYVAA8iCPwAzfnV8lTshOaa4cHdHdvF2cbZH9vE3Z7hieZZ7Nvy0/kCASgIBg9bFfEakx8aI2QlXSb9JUYkSSEgHfAX6RFBCzMEAP3o9SrvBOmt41XfJNw12pvZW9pu3MHfN+Sn6eDvq/bK/fsEAQybEo0Yoh2sIYYkGCZTJjQlxiIfH2AasxRLDmMHOAAM+R7yrevz5STha93p2rXZ2tlX2x7eF+Ic5wLtk/OU+sUB5wi5D/0VexsBIGcjjiVjJt4lBCTmIJ8cVxc8EYYKcQM+/Cz1e+5p6Cvj8N7g2xTan9mD2rncLeC/5EfqkvBp943+vQW6DEUTIhkdHggiwSQvJkUmAiVxIqse0BkNFJUNowZ2/034afEJ62XlseAX3bjaqdnz2ZPbfN6T4rLnre1N9Fb7iAKlCWoQnBYCHGsgsSO1JWYmvCW/I4AgGxy6FowQyQmuAnz7cfTO7dDnq+KO3p/b+Nmn2a/aCN2b4Erl6epG8Sj4UP9+BnIN7RO0GZQeYSL4JEEmMybMJBkiNB4+GWUT3gziBbP+jve18Gbq2uRC4Mjci9qg2Q/a09vd3hLjS+ha7gf1GPxLA2EKGhE4F4Yc0iD3I9glZCaWJXYjFiCVGxwW2w8MCesBuvq38yPtOecu4jDeY9vf2bLZ39pa3Q7h2OWN6/vx5/gSAD4HKA6TFEQaCR+2IiolUCYdJpIkviG6HaoYvBIlDCEF7/3Q9gPwxulR5NXffNxi2pvZLtoW3EHfk+Pm6Ajvw/Xb/A0EHQvIEdMXBx02ITok9yVfJmwlKSOpHwwbexUoD00IKAH5+f/yeuyl5rXh1d0q28rZwtkT27Ddg+Fo5jTssvKo+dYA/QfdDjcV0Rp6HwgjWiVbJgMmVSRfIT0dExgQEmsLXwQs/RL2Uu8n6cvjbN8z3D3am9lS2l3cqd8Y5IPpuO+A9p790ATXC3QSaxiGHZYheSQSJlUmPyXZIjkfgBrYFHQOjgdkADj5SPLT6xTmPuF+3fTauNnV2UrbCt774fvm3Oxq82n6mQG8CJAP2BVcG+kfViOFJWIm5iUUJP0gvBx5F2MRsAqdA2r8VvWj7ozoSOMH3+/bG9qe2XraqNwU4KDkIupq8D73Yf6RBZAMHxMAGQEe8yG0JComSCYNJYUixR7xGTMUvg3OBqL/ePiS8S7rheXL4Crdw9qr2e3Zhdtm3nbikOeG7SP0KvtcAnoJQhB4FuMbVCChI60lZSbEJc8jlyA5HN4WtBD0CdoCp/ub9PXt8ufH4qTerdv+2aXZpdr23ILgKuXE6h3x/Pck/1IGSA3HE5MZeR5NIuskPSY3JtgkLiJPHmAZixMHDQ4G3/65993wiur55Fvg2tyV2qLZCNrE28fe9eIo6DPu3fTs+x8DNwryEBUXaBy7IOgj0SVlJp8lhyMuILQbQBYDEDcJFwLl+uHzSu1b50riRd5w2+TZr9nU2kfd8+C35Wjr0vG8+Of/Ewf/DW0UJBrvHqMiHyVNJiImnyTTIdYdzBjiEk8MSgUe/gv3UfAu6tfkeuA/3UHbj9ov2xjdOuB05KDpj+8K9tX8sgNnCrQQYxZBGyMf6CF5I8kj1iKsIF8dDxnkEw0OwAc2Aav6WfR57j7p1+Rr4Rbf7d333TPfleEE5WDpgu459FL6kwDIBrYMKRLxFuMa3h3IH5EgNSC4HikcoRhBFDIPognEA8799fds8mftEOmP5QDjeuEJ4a/hZOMX5q/pCu7+8mD4/v2jAx8JQQ7ZEsEW1hn+GyYdRx1hHH0arhcQFMMP8ArDBWsAGvv99UPxFe2Z6ezmJeVT5HrkmeWj54TqIO5X8gH38/sAAfsFtwoKD88S4xUtGJkZHRq2GWgYQRZXE8UPqwsxB38Cwf0f+cT01/B57cnq3OjD54bnJeia6dTrv+4/8jP2ePrl/lEDmAeSCxsPFRJmFPwVyBbGFvgVZhQhEj4P2AsPCAYE5P/K+9/3R/Qf8YXujexJ68Hq+eru65Xt3e+w8vX1i/lU/SoB7QR7CLQLfA68EF8SWhOkEz4TKxJ5EDYOegteCP8EfAH2/Yr6WPd99BDyJ/DS7hruBe6R7rjvb/Gj80D2LflP/Ir/vgLSBagIKAs9DdUO5A9gEEgQng9rDrkMmgojCGsFigKd/7v8APqD91v1mfNM8n/xNvFy8THyafMO9Q/3WfnY+3P+EgGfAwIGJwj7CW8LdwwLDSkNzwwFDNEKQQlkB0wFDAO6AGz+NPwn+lf40/ao9d70fPSC9O/0vvXl9ln4C/rr++f97f/qAc0DhQUDBzwIJQm3CfAJzglVCYsIeAcoBqcEBANPAZj/7f1e/Pj6x/nU+Cj4xfev9+P3YPgd+RT6O/uF/Ob9Uf+4ABACTQNkBEwF/gV2BrAGrAZtBvUFTAV4BIIDdQJZATsAJP8e/jH9ZvzC+0r7APvn+vz6Pvup+zb84Pyf/Wz+Pv8NANQAigEpAq0CEwNXA3kDegNbAx8DygJgAuYBYwHbAFUA1f9g//j+o/5h/jX+Hf4a/ir+Sv54/rH+8P4z/3X/tP/t/xwAQgBdAG0AcQBrAF0ASQAxABgAAAAHABsAOwBjAI8AugDeAPgAAwH6AN0AqQBhAAYAnf8r/7b+R/7k/Zf9ZP1S/WX9oP0B/ob+K//o/7MAhAFPAgcDowMWBFkEZgQ3BM4DKwNWAlYBOAAJ/9n9tvyy+9z6QPrq+eD5J/q++qD7xPwd/p3/LgG/AjoEiwWfBmUH0gfbB38HvgaeBS0EewKbAKf+tfzg+kD57Pf59nT2Z/bX9sD3GvnX+uH8IP94AcsD/AXsB4EJpQpFC1cL1wrJCTYIMAbPAzEBdv7A+zP58fYX9cLzA/Pp8nbzqPRy9r/4dfty/o8BqASTBykKSQzTDbIO2A4/Du0M7wpcCFIF+AF3/vv6svfG9F/ynfCb72fvCPB48ajzf/bb+ZL9dQFVBf4IQQzyDu0QFhJbErURKRDJDbAKAwfwAqr+Z/pd9sLyxO+N7Tzs5OuN7DHuvvAX9BT4gvwpAdEFPAoyDn0R8hNvFd0VNRV7E8IQKw3hCBkEEP8D+jb15fBJ7ZTq6ehi6Afp1eq27YnxIPZB+6sAHAZNC/oP6BPgFrsYXhm+GOAW2RPMD+sKcgWn/9H5PPQx7/Dqs+el5ePkeuVm55Hq1u4A9ND5/P81Bi8MmhEwFrQZ+BvbHE8cWBoLF5ESIA37Bm8A0fly86ftuujs5HDiaeHn4ebjUef/67bxL/ga/x0G4QwOE1QYbRwkH1Ig5R/fHVgaeRV/D7MIagEC+tjySOyo5kHiTd/23U/eWOD44wbpQu9g9gb+0gVjDVcUUxoKHz0iwCN9I3UhvR2DGAcSmQqXAmb6bvIW67zks98/3I3attq83Ijg7OWm7GP0wfxPBZoNOBXIG/cggiQ8JhAmACQmILMa6xMnDMgDOfvn8jvrmORR36rb0dne2dHbkN/r5J/rV/Ov+z4ElwxRFAcbZiApJB8mMSZcJLkgdhvVFCsN2QRL/OvzJexb5eTfBtzy2cLZeNsA3yvkuOpU8p76LAOSC2UTQRrPH8kj+yVJJrEkRiEzHLoVLA7qBV398vQS7STmf+Bq3Bvardkn23becOPV6VTxjvkZAooKdRJ2GTIfYSPOJVom/yTMIescmxYqD/kGcP769QTu8uYf4dXcS9qg2d7a9N274vfoV/CA+AYBgQmCEaUYjh7zIpolZCZFJUsinR13FyYQBwiD/wX3+e7F58bhR92C2pvZm9p43QziHehe73L39P91CIwQzxfkHX0iXyVlJoMlxCJKHk4YHhEUCZYAEfjx753oc+LA3cLandlh2gPdY+FI52fuZ/bh/mgHkQ/1FjUdASIcJV8muiU1I/AeIRkTEh4KqQEg+e3weukl40DeCNun2S3aldy/4HjmdO1d9c79WQaUDhYWfxx9IdIkUSbpJZ8jkB/vGQQTJwu8Ai/66/Fb6t7jx95W27nZAtou3CPgrOWF7Fb0u/xJBZQNMxXEG/MggCQ8JhEmAiQpILca8RMtDM4DQPvt8kDrnORU36zb0tne2c/bjN/n5JrrUfOp+zgEkQxLFAMbYyAnJB8mMSZeJLwgehvaFDEN4ARR/PHzKuxg5ejfCdzz2cHZdtv83ibks+pO8pj6JgOMC2ATPRrMH8Yj+iVKJrMkSSE4HL8VMg7wBWT9+PQY7SnmguBt3Bzardkm23PebOPQ6U/xiPkTAoQKcBJxGS4fXyPNJVsmACXPIe8coBYwD/8Gd/4A9gnu9+Yj4djcTNqg2dza8d234vLoUvB5+AABewl9EaAYih7wIpklZCZGJU4ioR18FywQDQiK/wv3/u7K58rhSt2E2pvZmtp13QjiGOhY72z37v9vCIYQyxfhHXoiXiVlJoQlxiJOHlMYJBEaCZwAGPj376Lod+LD3cPandlf2gDdX+FD52LuYfba/mEHjA/wFjEd/iEaJV8muyU3I/QeJhkYEiQKrwEm+fPwf+kq40PeCtun2Szak9y84HPmb+1X9cf9UwaODhEWexx6IdAkUSbqJaIjkx/zGQkTLQvCAjX68fFg6uLjyt5Y27nZAdos3B/gqOWA7FD0tfxDBY4NLhW/G/AgfiQ7JhImBSQtILwa9hMzDNQDRvvz8kbroORX367b09nd2c3bid/i5JXrS/Oj+zEEiwxGFP4aXyAlJB4mMiZgJMAgfhvfFDcN5gRY/PfzMOxk5evfC9z02cHZddv53iLkrupI8pL6HwOGC1oTOBrIH8Qj+SVKJrUkTCE8HMQVOA72BWr9/vQd7S3mhuBv3B3arNkk23DeaOPL6UnxgvkNAn4KahJsGSsfXCPMJVsmAiXSIfQcpRY2DwYHff4G9g/u/OYn4drcTdqg2dra7t2z4u3oTPBz+PoAdAl3EZsYhx7tIpglZCZIJVEipR2BFzEQFAiQ/xH3BO/P587hTd2F2prZmNpy3QTiE+hS72b35/9pCIAQxhfdHXgiXCVlJoYlySJRHlgYKREgCaIAHvj976foe+LG3cXandle2v7cW+E+51zuW/bU/lsHhg/rFi0d+yEZJV8mvCU6I/ceKxkeEioKtgEs+fjwhOku40beDNun2SvakNy44G7mae1R9cH9TAaJDgwWdxx3Ic4kUCbrJaQjlx/4GQ8TMwvIAjz69/Fl6ubjzd5a27rZANoq3Bzgo+V67Er0rvw8BYgNKBW7G+0gfCQ7JhMmByQwIMAa/BM5DNsDTPv58kvrpeRb37Db09nc2cvbht/e5I/rRfOd+ysEhQxBFPoaXCAiJB0mMyZiJMMggxvlFD0N7ARe/P3zNexp5e/fDdz12cDZc9v23h7kqOpD8oz6GQOAC1UTMxrFH8Ij+CVLJrckTyFAHMkVPg79BXD9BPUj7TLmieBx3B7arNki223eY+PG6UPxfPkGAngKZRJnGScfWiPLJVsmBCXVIfgcqhY8DwwHg/4M9hTuAOcq4d3cTtqf2dna692v4ujoRvBt+PMAbglxEZcYgx7rIpclZCZJJVQiqR2GFzcQGgiW/xf3Cu/U59LhT92G2prZl9pw3QDiDuhN72D34f9jCHoQwRfZHXUiWyVlJoclzCJVHl0YLxEmCakAJPgC8Kzof+LJ3cbandld2vvcV+E551fuVfbO/lUHgA/mFigd+CEXJV4mviU8I/seLxkjEjAKvAEy+f7wieky40neDduo2Srajty04GnmZO1L9bv9RgaDDgcWchx0IcwkUCbsJaYjmh/9GRQTOQvPAkL6/fFr6uvj0N5c27rZ/9ko3Bjgn+V17ET0qPw2BYMNIxW3G+ogeiQ6JhQmCSQ0IMUaARQ/DOEDUvv/8lDrqeRe37Lb1Nnc2cjbgt/Z5IrrP/OW+yUEfww7FPUaWSAgJBwmMyZkJMYghxvqFEIN8gRk/AP0Ouxt5fLfD9z12cDZcdvz3hnko+o98oX6EwN6C08TLxrBH78j9yVLJrgkUiFEHM8VQw4DBnf9CvUo7TfmjeB03B/arNkg22reX+PB6T3xdfkAAnIKXxJjGSMfVyPKJVwmBSXYIfwcrxZCDxIHif4T9hruBecu4d/cT9qf2dfa6N2r4uLoQPBn+O0AaAlsEZIYfx7oIpUlZCZLJVYirR2LFz0QIAid/x33D+/Z59XhUt2I2prZltpt3fzhCehH71r32/9cCHUQvBfVHXIiWSVlJoglziJZHmIYNBEsCa8AKvgI8LHog+LM3cjandlc2vncU+E051HuT/bH/k8Heg/hFiQd9SEVJV4mvyU/I/8eNBkpEjYKwgE4+QTxjuk240zeD9uo2Snai9yx4GXmXu1F9bT9QAZ9DgIWbhxxIcokUCbtJakjnh8BGhkTPwvVAkj6A/Jw6u/j095e27vZ/tkl3BXgmuVw7D70ovwwBX0NHhWyG+YgeCQ5JhUmCyQ3IMkaBhRFDOcDWfsF81brruRh37Tb1dnb2cbbf9/V5IXrOfOQ+x8Eegw2FPEaVSAeJBsmNCZmJMogjBvvFEgN+QRq/An0QOxy5fbfEdz22b/Zb9vw3hXknuo38n/6DAN0C0oTKhq+H70j9iVMJrokViFJHNQVSQ4JBn39EPUu7TvmkeB23CDaq9ke22feW+O76Tfxb/n6AWwKWhJeGR8fVSPJJVwmByXbIQAdtBZHDxgHkP4Z9iDuCucy4eLcUdqf2dba5d2n4t3oO/Bh+OcAYglmEY0Yex7mIpQlZCZMJVkisR2QF0IQJgij/yT3Fe/e59nhVd2J2prZlNpq3fjhBOhB71T31P9WCG8QtxfRHW8iWCVlJool0SJdHmcYOhEyCbUAMPgO8Lboh+LP3cnantla2vbcUOEw50vuSPbB/kkHdQ/cFiAd8iEUJV4mwCVBIwIfORkuEj0KyAE/+Qrxk+k640/eEduo2Sjaidyt4GDmWe0/9a79OgZ3DvwVahxuIckkTybuJasjoh8GGh8TRQvbAk76CfJ16vPj195g27vZ/dkj3BHgluVq7Dj0nPwqBXcNGRWuG+MgdiQ5JhUmDSQ6IM4aDBRLDO0DX/sL81vrsuRl37bb1dna2cTbfN/Q5H/rM/OK+xgEdAwwFOwaUiAcJBsmNSZoJM0gkBv0FE4N/wRx/A/0Rex25fnfFNz32b/Zbdvs3hHkmeox8nn6BgNuC0QTJRq6H7sj9SVMJrwkWSFNHNkVTw4PBoP9FvUz7UDmlOB53CHaq9kd22TeV+O26THxafnzAWYKVBJZGRwfUiPIJVwmCSXeIQQduRZNDx4Hlv4f9iXuD+c24eTcUtqf2dTa4t2j4tjoNfBb+OAAXAlhEYgYdx7jIpMlZCZOJVwitR2VF0gQLAip/yr3G+/j593hV92L2prZk9pn3fTh/+c87073zv9QCGkQshfNHWwiViVlJosl0yJhHmwYQBE4CbwANvgT8Lvoi+LR3cvantlZ2vPcTOEr50buQva7/kMHbw/XFhwd7yESJV4mwSVEIwYfPhk0EkMKzwFF+RDxmOk+41LeE9up2Sfah9yq4FvmU+059aj9NAZxDvcVZhxrIcckTybvJa0jpR8KGiQTSwvhAlT6D/J66vjj2t5i27zZ/Nkh3A7gkeVl7DL0lfwjBXENExWqG+AgdCQ4JhYmDyQ+INIaERRRDPQDZfsQ82Drt+Ro37jb1tnZ2cLbeN/M5HrrLfOE+xIEbgwrFOgaTiAaJBomNSZqJNAglBv6FFQNBQV3/BX0S+x75f3fFtz42b7Za9vp3g3kk+or8nP6AANoCz8TIRq2H7gj9CVNJr4kXCFRHN4VVQ4VBon9HPU57UXmmOB73CLaqtkb22HeU+Ox6SzxY/ntAWAKTxJVGRgfUCPGJVwmCiXhIQgdvhZTDyUHnP4l9ivuFOc54efcU9qf2dLa392e4tPoL/BU+NoAVglbEYMYcx7gIpElZCZPJV8iuR2aF04QMgiw/zD3IO/n5+HhWt2M2prZkdpl3fDh+uc270f3yP9KCGQQrRfJHWoiVSVlJowl1iJlHnEYRRE+CcIAPfgZ8MDoj+LU3czantlY2vHcSOEm50DuPPa1/jwHaQ/SFhgd7CERJV0mwiVGIwofQhk5EkkK1QFL+RXxnulD41XeFNup2SbahNym4FfmTu0z9aL9LQZrDvIVYRxoIcUkTibwJbAjqR8PGioTUQvoAlv6FPJ/6vzj3d5k27zZ+9kf3ArgjOVf7Cz0j/wdBWsNDhWlG90gciQ4JhcmEiRBINcaFhRXDPoDbPsW82bru+Rr37rb19nZ2cDbdd/I5HXrJ/N9+wwEaAwmFOMaSyAYJBkmNiZsJNMgmRv/FFoNCwV9/Bv0UOx/5QDgGNz52b7Zadvm3gjkjuol8mz6+gJiCzkTHBqzH7Yj8yVNJsAkXyFVHOMVWw4cBpD9IvU+7UnmnOB93CPaqtkZ217eTuOs6SbxXfnnAVoKSRJQGRQfTSPFJV0mDCXkIQwdwxZZDysHo/4r9jDuGOc94ercVNqe2dHa3N2a4s7oKvBO+NQAUAlVEX4YcB7eIpAlZSZRJWIivR2fF1MQOAi2/zb3Ju/s5+XhXd2N2prZkNpi3ezh9ecw70H3wf9ECF4QqBfFHWciUyVlJo4l2SJpHnUYSxFFCcgAQ/gf8MXok+LX3c7antlX2u7cROEh5zvuNvau/jYHYw/NFhQd6SEPJV0mwyVJIw4fRxk/Ek8K2wFR+Rvxo+lH41jeFtup2SXagtyi4FLmSO0t9Zv9JwZmDu0VXRxlIcMkTibxJbIjrB8UGi8TVwvuAmH6GvKF6gDk4N5l273Z+9kc3AfgiOVa7Cb0ifwXBWUNCRWhG9kgcCQ3JhgmFCRFINsaHBRdDAAEcvsc82vrv+Rv37zb19nY2b7bcd/D5G/rIfN3+wUEYgwgFN8aSCAWJBgmNiZuJNcgnRsEFWANEgWE/CH0VeyE5QTgGtz62b3ZZ9vj3gTkieof8mb68wJcCzQTGBqvH7Qj8iVOJsIkYiFaHOkVYQ4iBpb9KPVE7U7mn+CA3CTaqtkX21veSuOn6SDxVvnhAVQKRBJLGREfSyPEJV0mDiXnIRAdyBZeDzEHqf4x9jbuHedB4ezcVtqe2c/a2t2W4snoJPBI+M0ASglQEXkYbB7bIo8lZSZSJWUiwR2kF1kQPwi8/zz3LO/x5+nhYN2P2prZj9pl3frhCOhC70v3vP8oCCYQURdNHdAhoSSfJb4kCyKqHdQX1BAECcgAivix8KLptOM031fcQtsB3Inet+JW6B3vtPa7/skGfA5wFU0byh+wItojPCPfIOIcehftEI4JvQHd+VLye+uv5TbhSd4L3Yndvt+K47zoEO839tP9ggXmDJ8TWBnKHb4gDyKuIaIfBhwJF+wQ/gmYAhn73vNE7Z7nM+M74NjeHd8C4XDkOOkd79P1BP1TBGQL3hFvF9EbzR4/IBYgVh4WG4EW0xBVCloDPPxV9fvugekp5Sviq+C64FbiauXM6UPvivVP/DsD+AkvEJMV3xndHGsedB76HBIa4hWhEJEKAgRI/bb2ovBX6xjnGeSB4mDiuON25nXqge9a9bP7OwKhCJIOxBP1F/EakxzJHJIb/RguFVYQtQqRBDv+Avg28h/t/egE5lnkD+Qo5ZTnNOvY70P1MftUAWAHCA0DEhQWCBm6GhcbHBrXF2UU9A++CgYFFv84+bbz2O7Z6uvnM+bE5aPmw+gH7EXwRvXJ+oYANgaRC1IQPhQkF+AYXxmbGJ8WhxN7D68KYgXY/1b6I/WB8KrszOkN6H/nKugC6u/syvBh9Xr60f8jBS0KsA5yEkUVBxehFw8XWRWWEusOiAqkBYAAXvt89hryb+6n6+bpQOm76VDr6u1m8Zb1RPo0/ycE3wgfDbMQbhMuFd8VeRUDFJIRRQ5HCs0FEAFO/MD3ovMo8HvtvesE61Xrrez37hfy4vUo+rH+QwOmB6ALAQ+eEVgTGRTaE6ASexCJDe8J3QWHASb97/gZ9dPxRu+S7crs+OwX7hfw3fJG9iT6R/53AoIGMwpdDdgPhRFREjQSMBFTD7gMfwnUBeUB5v0I+nz2cPMI8WPvk+6i7o3vR/G588L2Ovr2/cMBdAXZCMcLGw63D4gQhxC0DxsO0gv4CLIFKgKO/gr7zff+9MDyL/Fc8FLwD/GH8qj0VPdp+r79KAF9BJIHQQpoDO4Nvw7UDiwO0wzZCloIdwVVAh3/9vsK+Xz2bfT18iXyB/Kb8tfzq/X996/6n/2lAJ0DYAbLCMIKKwz3DBwNmwx8C80JpwckBWcCk//L/DL66fcN9rT07fPB8zH0NfXA9rz4DvuZ/TsA1AJCBWYHKAlwCjALYQsBCxYKrwjdBroEYALx/4j9RftF+aH3a/ay9X71z/Wh9uf3kPmF+6z96/8jAjkEEwabB70IbQmjCV8JpAh/B/8FNwRBAjQALf5D/I/6JvkZ+HP3PPd19xn4H/l4+hP82P2z/4kBRgPTBBwGFAetB+QHtQcmBz4GDAWeAwgCYAC6/iv9xvud+r35MPn8+CL5nvlo+nX7t/wd/pT/CAFpAqUDrQR1BfMFJAYGBpwF7gQFBO4CuAFyAC///P3q/AX8V/vo+rz61Pos+8D7hvxz/Xr+jv+gAKMBjAJOA+EDPwRkBFEECASPA+sCKAJPAWwAi/+3/vn9XP3l/Jn8e/yK/MX8J/2p/UT+7/6h/1AA9QCHAf8BWQKRAqcCmQJrAiECvwFMAc4ATADP/1r/9P6i/mb+Qv43/kT+Z/6b/t7+Kv97/83/GQBdAJYAwgDfAOwA6wDeAMYApgCBAFsANQAUAPr/5v/a/9b/2v/j//H/"
DAILY_GOAL_CHIME_SOUND_B64 = "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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="


# Wizard tower illustration — kept small (backdrop, not the hero) so the
# "Word Wizard" title stays the focal point, per feedback that the art
# was drawing too much attention.
TOWER_SVG = """
<div style="display:flex; justify-content:center; margin-bottom: 0.5rem;">
<svg viewBox="0 0 400 280" width="230" style="max-width:75%; height:auto; opacity:0.97;" xmlns="http://www.w3.org/2000/svg">
<g fill="#454B5C" opacity="0.7">
<ellipse cx="70" cy="18" rx="35" ry="12"/>
<ellipse cx="45" cy="22" rx="22" ry="9"/>
<ellipse cx="100" cy="15" rx="25" ry="10" fill="#3A3F4E"/>
</g>
<g fill="#454B5C" opacity="0.7">
<ellipse cx="320" cy="15" rx="38" ry="13"/>
<ellipse cx="290" cy="20" rx="24" ry="9"/>
<ellipse cx="355" cy="12" rx="22" ry="9" fill="#3A3F4E"/>
</g>
<g fill="#3A3F4E" opacity="0.55">
<ellipse cx="200" cy="10" rx="24" ry="9"/>
<ellipse cx="180" cy="14" rx="16" ry="7"/>
<ellipse cx="222" cy="13" rx="14" ry="6"/>
</g>
<g class="rain-group" stroke="#7A8494" stroke-width="2" stroke-linecap="round" opacity="0.6">
<line x1="40" y1="28" x2="28" y2="68"/>
<line x1="65" y1="30" x2="53" y2="70"/>
<line x1="90" y1="28" x2="78" y2="68"/>
<line x1="115" y1="30" x2="103" y2="70"/>
<line x1="140" y1="32" x2="128" y2="72"/>
<line x1="260" y1="28" x2="248" y2="68"/>
<line x1="285" y1="30" x2="273" y2="70"/>
<line x1="310" y1="28" x2="298" y2="68"/>
<line x1="335" y1="32" x2="323" y2="72"/>
<line x1="360" y1="28" x2="348" y2="68"/>
</g>
<g fill="#2F4A3E">
<polygon points="70,190 90,140 110,190"/>
<polygon points="70,175 90,130 110,175"/>
<rect x="86" y="188" width="8" height="14"/>
<polygon points="40,200 58,160 76,200"/>
<rect x="54" y="198" width="8" height="12"/>
<polygon points="128,205 143,175 158,205"/>
<rect x="139" y="203" width="6" height="10"/>
</g>
<g fill="#2F4A3E">
<polygon points="290,190 310,140 330,190"/>
<polygon points="290,175 310,130 330,175"/>
<rect x="306" y="188" width="8" height="14"/>
<polygon points="324,200 342,160 360,200"/>
<rect x="338" y="198" width="8" height="12"/>
<polygon points="242,205 257,175 272,205"/>
<rect x="253" y="203" width="6" height="10"/>
</g>
<polygon points="130,280 270,280 228,224 172,224" fill="#8A8570" opacity="0.85"/>
<g stroke="#5A5646" stroke-width="1.5" opacity="0.6">
<line x1="145" y1="270" x2="255" y2="270"/>
<line x1="152" y1="256" x2="248" y2="256"/>
<line x1="160" y1="242" x2="240" y2="242"/>
<line x1="167" y1="228" x2="233" y2="228"/>
</g>
<rect x="172" y="216" width="56" height="8" fill="#5B6578" stroke="#333846" stroke-width="1"/>
<rect x="178" y="208" width="44" height="8" fill="#5B6578" stroke="#333846" stroke-width="1"/>
<rect x="184" y="200" width="32" height="8" fill="#5B6578" stroke="#333846" stroke-width="1"/>
<circle class="window-glow" cx="200" cy="120" r="34" fill="#C79A3C" opacity="0.18"/>
<polygon points="165,200 235,200 245,195 155,195" fill="#454B5C"/>
<rect x="170" y="90" width="60" height="110" fill="#5B6578" stroke="#333846" stroke-width="2"/>
<g stroke="#333846" stroke-width="1" opacity="0.5">
<line x1="170" y1="110" x2="230" y2="110"/>
<line x1="170" y1="130" x2="230" y2="130"/>
<line x1="170" y1="150" x2="230" y2="150"/>
</g>
<path d="M 188 200 L 188 175 Q 188 165 200 165 Q 212 165 212 175 L 212 200 Z" fill="#4A3222" stroke="#2E2015" stroke-width="1.5"/>
<circle cx="207" cy="185" r="1.8" fill="#C79A3C"/>
<polygon points="160,90 240,90 200,35" fill="#454B5C" stroke="#333846" stroke-width="2"/>
<path d="M 188 100 Q 188 92 200 92 Q 212 92 212 100 L 212 130 L 188 130 Z" fill="#C79A3C" stroke="#8A6A28" stroke-width="1.5"/>
<line x1="200" y1="96" x2="200" y2="130" stroke="#8A6A28" stroke-width="1"/>
<line x1="189" y1="112" x2="211" y2="112" stroke="#8A6A28" stroke-width="1"/>
<g fill="#5B5850">
<polygon points="85,258 92,250 102,248 110,253 108,262 98,265 88,263"/>
<polygon points="115,266 120,261 126,262 127,268 121,270" fill="#4A4740"/>
<polygon points="298,261 306,253 316,252 322,258 319,266 308,268 300,266"/>
<polygon points="274,268 279,263 285,264 286,270 280,272" fill="#4A4740"/>
</g>
<g class="ripple-group" fill="none" stroke="#8A94A8" stroke-width="1" opacity="0.5">
<circle cx="180" cy="232" r="3"/>
<circle cx="168" cy="245" r="3"/>
<circle cx="155" cy="258" r="3"/>
<circle cx="145" cy="268" r="3"/>
<circle cx="135" cy="277" r="3"/>
<circle cx="220" cy="232" r="3"/>
<circle cx="232" cy="245" r="3"/>
<circle cx="245" cy="258" r="3"/>
<circle cx="255" cy="268" r="3"/>
<circle cx="265" cy="277" r="3"/>
</g>
<g class="wizard-figure">
<polygon points="194,258 206,258 210,232 190,232" fill="#8B8FA3" stroke="#4A4E5E" stroke-width="1"/>
<circle cx="200" cy="225" r="6.5" fill="#D8D4C4"/>
<path d="M 195 228 Q 200 238 205 228 L 205 231 Q 200 240 195 231 Z" fill="#EDEAE0"/>
<polygon points="188,222 212,222 200,203" fill="#7B7F92" stroke="#4A4E5E" stroke-width="1"/>
<rect x="186" y="220" width="28" height="4" fill="#7B7F92" stroke="#4A4E5E" stroke-width="1"/>
<polygon points="207,233 213,222 217,224 211,236" fill="#8B8FA3" stroke="#4A4E5E" stroke-width="1"/>
<circle cx="215" cy="223" r="2" fill="#D8D4C4"/>
<line x1="215" y1="212" x2="215" y2="260" stroke="#5A4A38" stroke-width="2" stroke-linecap="round"/>
</g>
<ellipse class="lightning-glow" cx="258" cy="55" rx="45" ry="50" fill="#F5F0E0" opacity="0"/>
<polygon class="lightning-flash" points="270,22 250,60 265,60 240,105 262,68 250,68 270,22" fill="#F5F0E0" opacity="0"/>
</svg>
</div>
"""


MONSTER_SVG = """
<div style="display:flex; justify-content:center;">
<svg viewBox="0 0 100 100" width="52" xmlns="http://www.w3.org/2000/svg">
<polygon points="30,38 26,20 38,36" fill="#5C2E2E"/>
<polygon points="70,38 74,20 62,36" fill="#5C2E2E"/>
<ellipse cx="50" cy="60" rx="28" ry="24" fill="#7A3B3B" stroke="#4A2020" stroke-width="2"/>
<ellipse cx="26" cy="62" rx="7" ry="9" fill="#7A3B3B" stroke="#4A2020" stroke-width="2"/>
<ellipse cx="74" cy="62" rx="7" ry="9" fill="#7A3B3B" stroke="#4A2020" stroke-width="2"/>
<polygon points="22,68 18,74 26,72" fill="#4A2020"/>
<polygon points="78,68 82,74 74,72" fill="#4A2020"/>
<circle cx="40" cy="56" r="5" fill="#F0C674"/>
<circle cx="60" cy="56" r="5" fill="#F0C674"/>
<circle cx="40" cy="57" r="2" fill="#2A1510"/>
<circle cx="60" cy="57" r="2" fill="#2A1510"/>
<polyline points="38,72 42,76 46,72 50,76 54,72 58,76 62,72" fill="none" stroke="#2A1510" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
</div>
"""

BOSS_MONSTER_SVG = """
<div style="display:flex; justify-content:center;">
<svg viewBox="0 0 100 100" width="88" xmlns="http://www.w3.org/2000/svg">
<polygon points="30,34 24,10 40,32" fill="#3D1B3D"/>
<polygon points="70,34 76,10 60,32" fill="#3D1B3D"/>
<polygon points="20,26 26,4 32,24" fill="#2E1030"/>
<polygon points="80,26 74,4 68,24" fill="#2E1030"/>
<ellipse cx="50" cy="60" rx="32" ry="27" fill="#5C1F3D" stroke="#2E1030" stroke-width="2.5"/>
<ellipse cx="22" cy="62" rx="8" ry="10" fill="#5C1F3D" stroke="#2E1030" stroke-width="2.5"/>
<ellipse cx="78" cy="62" rx="8" ry="10" fill="#5C1F3D" stroke="#2E1030" stroke-width="2.5"/>
<polygon points="14,70 9,78 19,75" fill="#2E1030"/>
<polygon points="86,70 91,78 81,75" fill="#2E1030"/>
<circle cx="38" cy="55" r="6.5" fill="#F0C674"/>
<circle cx="62" cy="55" r="6.5" fill="#F0C674"/>
<circle cx="38" cy="56" r="2.6" fill="#2A1510"/>
<circle cx="62" cy="56" r="2.6" fill="#2A1510"/>
<polyline points="34,74 39,79 44,73 50,79 56,73 61,79 66,74" fill="none" stroke="#2A1510" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
</div>
"""


def hp_bar_html(percent, draining=False, label=None):
    fill_class = "hp-bar-fill draining" if draining else "hp-bar-fill"
    label_html = f'<div class="hp-bar-label">{label}</div>' if label else ""
    return f'{label_html}<div class="hp-bar-track"><div class="{fill_class}" style="width:{percent}%;"></div></div>'


def boss_hp_html(hp, max_hp, label=None):
    label_html = f'<div class="boss-label">{label}</div>' if label else ""
    pips = "".join(
        f'<div class="boss-hp-pip{" filled" if i < hp else ""}"></div>'
        for i in range(max_hp)
    )
    return f'{label_html}<div class="boss-hp-track">{pips}</div>'


def boss_entrance_html(arrives_label, boss_name, boss_subtitle):
    """
    One-shot ~1.2s CSS-only entrance banner shown above the boss the first
    time a boss encounter becomes active. Purely decorative (no JS, no
    blocking) — it plays and then collapses itself via the
    bossEntranceCollapse keyframe, so it never requires an extra click and
    never leaves a gap in the layout once it's done.
    """
    return (
        '<div class="boss-entrance">'
        f'<div class="boss-entrance-arrives">{arrives_label}</div>'
        f'<div class="boss-entrance-name">{boss_name}</div>'
        f'<div class="boss-entrance-subtitle">{boss_subtitle}</div>'
        '</div>'
    )


def boss_feedback_html(headline, sub_text, kind):
    """Punchy DIRECT HIT! / MISSED! banner shown on the boss in-progress
    result screen, in place of the quieter st.info/st.warning box."""
    css_class = "boss-feedback-hit" if kind == "hit" else "boss-feedback-miss"
    return (
        f'<div class="boss-feedback {css_class}">{headline}'
        f'<span class="boss-feedback-sub">{sub_text}</span></div>'
    )


def boss_outcome_heading_html(boss_name, boss_subtitle):
    """Boss name/subtitle shown above the enlarged boss-portrait on the
    final outcome screen (perfect / defeated / escaped)."""
    return (
        '<div class="boss-outcome-heading">'
        f'<div class="boss-outcome-name">{boss_name}</div>'
        f'<div class="boss-outcome-subtitle">{boss_subtitle}</div>'
        '</div>'
    )


def level_up_badge_html(text):
    """Small one-shot gold badge for an ordinary level-up (no rank/tier
    change). Rendered on top of whatever screen is already showing --
    no extra click, no new screen."""
    return f'<div class="level-up-badge">{text}</div>'


def rank_up_html(rank_up_title, rank_name, level_label, flavor, wizard_tier_html):
    """Full celebratory screen shown when a correct answer pushes the
    player across a rank-tier boundary (e.g. Level 9 -> 10: Apprentice).
    Reuses the existing wizard-avatar tier art via wizard_tier_html."""
    return (
        '<div class="rankup-screen">'
        f'<div class="rankup-portrait">{wizard_tier_html}</div>'
        f'<div class="rankup-title">{rank_up_title}</div>'
        f'<div class="rankup-name">{rank_name}</div>'
        f'<div class="rankup-level">{level_label}</div>'
        f'<div class="rankup-flavor">{flavor}</div>'
        '</div>'
    )


def progression_hero_html(wizard_tier_html, rank_name, level_label):
    """Current-rank focal point for the progression screen -- reuses the
    exact same .rankup-portrait/.rankup-name/.rankup-level treatment as
    the rank-up celebration, so it reads as the same visual language.
    The extra "progression-hero" class doesn't change desktop styling at
    all -- it only gives the mobile media query something to scope its
    tightened spacing to, without touching the shared rank-up screen."""
    return (
        '<div class="rankup-screen progression-hero">'
        f'<div class="rankup-portrait">{wizard_tier_html}</div>'
        f'<div class="rankup-name">{rank_name}</div>'
        f'<div class="rankup-level">{level_label}</div>'
        '</div>'
    )


def xp_progress_bar_html(percent, xp_label, remaining_label):
    """Gold/purple XP-to-next-level progress bar, distinct from the
    red/gold monster HP bar and the pip-based boss HP bar."""
    return (
        f'<div class="progression-xp-label">{xp_label}</div>'
        f'<div class="progression-xp-track"><div class="progression-xp-fill" style="width:{percent}%;"></div></div>'
        f'<div class="progression-xp-remaining">{remaining_label}</div>'
    )


def progression_next_rank_html(text):
    return f'<div class="progression-next-rank">{text}</div>'


def rank_ladder_html(rows):
    """rows: list of {"name", "level_label", "state"} dicts, state one of
    'completed' / 'current' / 'future'. Rendered inside the same cream
    .word-card container the leaderboard and My Words screens use, so it
    matches their existing list pattern rather than inventing a new one."""
    icons = {"completed": "✓", "current": "★", "future": "🔒"}
    return "".join(
        f'<div class="rank-ladder-row {row["state"]}">'
        f'<span class="rank-ladder-name">{icons[row["state"]]} {row["name"]}</span>'
        f'<span class="rank-ladder-level">{row["level_label"]}</span>'
        f'</div>'
        for row in rows
    )


WIZARD_AVATAR_TIER_1 = """
<div style="display:flex; justify-content:center;">
<svg viewBox="0 0 100 100" width="52" xmlns="http://www.w3.org/2000/svg">
<polygon points="35,92 65,92 60,50 40,50" fill="#6B7280" stroke="#4A4E5E" stroke-width="2"/>
<circle cx="50" cy="42" r="10" fill="#EFD9B8"/>
<polygon points="50,15 63,40 37,40" fill="#7B7F92" stroke="#4A4E5E" stroke-width="2"/>
<ellipse cx="50" cy="40" rx="17" ry="4" fill="#5B6578" stroke="#4A4E5E" stroke-width="1.5"/>
<line x1="74" y1="30" x2="74" y2="95" stroke="#5A4A38" stroke-width="3" stroke-linecap="round"/>
</svg>
</div>
"""

WIZARD_AVATAR_TIER_2 = """
<div style="display:flex; justify-content:center;">
<svg viewBox="0 0 100 100" width="52" xmlns="http://www.w3.org/2000/svg">
<polygon points="35,92 65,92 60,50 40,50" fill="#4A3D6B" stroke="#2E2447" stroke-width="2"/>
<line x1="40" y1="70" x2="60" y2="70" stroke="#C79A3C" stroke-width="1.5"/>
<circle cx="50" cy="42" r="10" fill="#EFD9B8"/>
<polygon points="50,15 63,40 37,40" fill="#4A3D6B" stroke="#2E2447" stroke-width="2"/>
<ellipse cx="50" cy="40" rx="17" ry="4" fill="#3A2F54" stroke="#2E2447" stroke-width="1.5"/>
<line x1="50" y1="20" x2="50" y2="38" stroke="#C79A3C" stroke-width="1"/>
<line x1="74" y1="30" x2="74" y2="95" stroke="#5A4A38" stroke-width="3" stroke-linecap="round"/>
<circle cx="74" cy="27" r="4" fill="#6B9BD1" stroke="#3A6EA5" stroke-width="1"/>
</svg>
</div>
"""

WIZARD_AVATAR_TIER_3 = """
<div style="display:flex; justify-content:center;">
<svg viewBox="0 0 100 100" width="52" xmlns="http://www.w3.org/2000/svg">
<circle class="wizard-aura" cx="74" cy="24" r="12" fill="#F0C674" opacity="0.25"/>
<polygon points="35,92 65,92 58,50 42,50" fill="#3D2E5C" stroke="#C79A3C" stroke-width="2"/>
<line x1="38" y1="68" x2="62" y2="68" stroke="#C79A3C" stroke-width="1.5"/>
<circle cx="44" cy="80" r="1.5" fill="#C79A3C"/>
<circle cx="56" cy="84" r="1.5" fill="#C79A3C"/>
<circle cx="50" cy="42" r="10" fill="#EFD9B8"/>
<polygon points="50,13 64,40 36,40" fill="#3D2E5C" stroke="#C79A3C" stroke-width="2"/>
<ellipse cx="50" cy="40" rx="18" ry="4" fill="#2E2144" stroke="#C79A3C" stroke-width="1.5"/>
<circle cx="50" cy="22" r="3" fill="#F0C674"/>
<line x1="74" y1="26" x2="74" y2="95" stroke="#5A4A38" stroke-width="3" stroke-linecap="round"/>
<circle cx="74" cy="24" r="5" fill="#F0C674" stroke="#C79A3C" stroke-width="1"/>
</svg>
</div>
"""


def wizard_avatar_html(visual_tier):
    """visual_tier: 1 (Beginner/Apprentice), 2 (Spellcaster/Wizard), or 3 (Master Wizard/Archmage)."""
    return {1: WIZARD_AVATAR_TIER_1, 2: WIZARD_AVATAR_TIER_2, 3: WIZARD_AVATAR_TIER_3}.get(visual_tier, WIZARD_AVATAR_TIER_1)


SPELL_PROJECTILE_TIER_1 = """
<svg viewBox="0 0 40 20" width="40" height="20" xmlns="http://www.w3.org/2000/svg">
<circle cx="20" cy="10" r="4" fill="#D8D4C4"/>
</svg>
"""

SPELL_PROJECTILE_TIER_2 = """
<svg viewBox="0 0 40 20" width="40" height="20" xmlns="http://www.w3.org/2000/svg">
<circle cx="20" cy="10" r="7" fill="#6B9BD1" opacity="0.3"/>
<circle cx="20" cy="10" r="4" fill="#8CB8E8"/>
<circle cx="20" cy="10" r="2" fill="#EFF5FC"/>
</svg>
"""

SPELL_PROJECTILE_TIER_3 = """
<svg viewBox="0 0 40 20" width="40" height="20" xmlns="http://www.w3.org/2000/svg">
<circle cx="20" cy="10" r="9" fill="#F0C674" opacity="0.3"/>
<circle cx="20" cy="10" r="5" fill="#F5D68F"/>
<circle cx="20" cy="10" r="2.5" fill="#FFFBEF"/>
<path d="M 20 1 L 22 8 L 29 10 L 22 12 L 20 19 L 18 12 L 11 10 L 18 8 Z" fill="#F0C674" opacity="0.7"/>
</svg>
"""


def spell_projectile_html(visual_tier):
    return {1: SPELL_PROJECTILE_TIER_1, 2: SPELL_PROJECTILE_TIER_2, 3: SPELL_PROJECTILE_TIER_3}.get(visual_tier, SPELL_PROJECTILE_TIER_1)
