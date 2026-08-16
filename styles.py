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

/* App-wide title on the language/topic setup screens */
.app-title {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 2.2rem;
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
    background-color: var(--accent);
    border-color: var(--accent);
    color: var(--ink-deep);
}

div[data-testid="stButton"] button[kind="primary"]:hover {
    background-color: var(--accent-deep);
    border-color: var(--accent-deep);
}

/* Respect reduced-motion preference */
@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; animation: none !important; }
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


TOWER_SVG = """
<div style="display:flex; justify-content:center; margin-bottom: 0.5rem;">
<svg viewBox="0 0 400 280" width="340" style="max-width:100%; height:auto;" xmlns="http://www.w3.org/2000/svg">
<g stroke="#5B6578" stroke-width="2" stroke-linecap="round" opacity="0.5">
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
<circle cx="200" cy="120" r="34" fill="#C79A3C" opacity="0.18"/>
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
<polygon points="194,258 206,258 210,232 190,232" fill="#8B8FA3" stroke="#4A4E5E" stroke-width="1"/>
<circle cx="200" cy="225" r="6.5" fill="#D8D4C4"/>
<path d="M 195 228 Q 200 238 205 228 L 205 231 Q 200 240 195 231 Z" fill="#EDEAE0"/>
<polygon points="188,222 212,222 200,203" fill="#7B7F92" stroke="#4A4E5E" stroke-width="1"/>
<rect x="186" y="220" width="28" height="4" fill="#7B7F92" stroke="#4A4E5E" stroke-width="1"/>
<polygon points="207,233 213,222 217,224 211,236" fill="#8B8FA3" stroke="#4A4E5E" stroke-width="1"/>
<circle cx="215" cy="223" r="2" fill="#D8D4C4"/>
<line x1="215" y1="212" x2="215" y2="260" stroke="#5A4A38" stroke-width="2" stroke-linecap="round"/>
</svg>
</div>
"""
