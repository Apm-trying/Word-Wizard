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
    margin-bottom: 0.8rem;
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

/* Monster encounter — a light cosmetic reskin of the existing correct/wrong
   mechanic. No new game rules, just visual stakes on top of what already exists. */
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
@keyframes fogDrift {
    0% { transform: translateX(-15px); }
    50% { transform: translateX(15px); }
    100% { transform: translateX(-15px); }
}
.fog-layer-1 { animation: fogDrift 18s ease-in-out infinite; }
.fog-layer-2 { animation: fogDrift 24s ease-in-out infinite reverse; }

@keyframes windowFlicker {
    0%, 100% { opacity: 0.18; }
    45% { opacity: 0.24; }
    50% { opacity: 0.12; }
    55% { opacity: 0.20; }
}
.window-glow { animation: windowFlicker 4s ease-in-out infinite; }

@keyframes rainFall {
    0% { transform: translateY(-4px); opacity: 0.2; }
    50% { opacity: 0.6; }
    100% { transform: translateY(8px); opacity: 0.2; }
}
.rain-group line { animation: rainFall 1.4s linear infinite; }
.rain-group line:nth-child(2) { animation-delay: 0.2s; }
.rain-group line:nth-child(3) { animation-delay: 0.4s; }
.rain-group line:nth-child(4) { animation-delay: 0.1s; }
.rain-group line:nth-child(5) { animation-delay: 0.3s; }
.rain-group line:nth-child(6) { animation-delay: 0.5s; }

@keyframes idleBounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
}
.wizard-figure { animation: idleBounce 2.4s ease-in-out infinite; transform-origin: center bottom; }

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


HAT_ICON_SVG = """
<div style="display:flex; justify-content:center; margin-bottom: 0.3rem;">
<svg viewBox="0 0 100 100" width="52" xmlns="http://www.w3.org/2000/svg">
<path d="M 50 10 L 72 68 Q 50 80 28 68 Z" fill="#C79A3C" stroke="#8A6A28" stroke-width="2"/>
<ellipse cx="50" cy="68" rx="30" ry="8" fill="#A67D2C" stroke="#8A6A28" stroke-width="2"/>
<circle cx="50" cy="44" r="4" fill="#EFE7D3"/>
</svg>
</div>
"""


CHIME_SOUND_B64 = "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"


# Wizard tower illustration — kept small (backdrop, not the hero) so the
# "Word Wizard" title stays the focal point, per feedback that the art
# was drawing too much attention.
TOWER_SVG = """
<div style="display:flex; justify-content:center; margin-bottom: 0.5rem;">
<svg viewBox="0 0 400 280" width="260" style="max-width:80%; height:auto; opacity:0.92;" xmlns="http://www.w3.org/2000/svg">
<ellipse class="fog-layer-1" cx="90" cy="230" rx="70" ry="14" fill="#5B6578" opacity="0.15"/>
<ellipse class="fog-layer-2" cx="310" cy="240" rx="80" ry="16" fill="#5B6578" opacity="0.13"/>
<g class="rain-group" stroke="#5B6578" stroke-width="2" stroke-linecap="round" opacity="0.5">
<line x1="40" y1="20" x2="30" y2="55"/>
<line x1="65" y1="10" x2="55" y2="45"/>
<line x1="90" y1="30" x2="80" y2="65"/>
<line x1="310" y1="15" x2="300" y2="50"/>
<line x1="335" y1="35" x2="325" y2="70"/>
<line x1="360" y1="10" x2="350" y2="45"/>
</g>
<g fill="#2F4A3E">
<polygon points="70,190 90,140 110,190"/>
<polygon points="70,175 90,130 110,175"/>
<rect x="86" y="188" width="8" height="14"/>
<polygon points="40,200 58,160 76,200"/>
<rect x="54" y="198" width="8" height="12"/>
</g>
<g fill="#2F4A3E">
<polygon points="290,190 310,140 330,190"/>
<polygon points="290,175 310,130 330,175"/>
<rect x="306" y="188" width="8" height="14"/>
<polygon points="324,200 342,160 360,200"/>
<rect x="338" y="198" width="8" height="12"/>
</g>
<polygon points="130,280 270,280 228,224 172,224" fill="#3A3F4E" opacity="0.7"/>
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
</svg>
</div>
"""


MONSTER_SVG = """
<div style="display:flex; justify-content:center;">
<svg viewBox="0 0 100 100" width="70" xmlns="http://www.w3.org/2000/svg">
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


def hp_bar_html(percent, draining=False):
    fill_class = "hp-bar-fill draining" if draining else "hp-bar-fill"
    return f'<div class="hp-bar-track"><div class="{fill_class}" style="width:{percent}%;"></div></div>'
