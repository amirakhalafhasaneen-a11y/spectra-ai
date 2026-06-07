import streamlit as st
from openai import OpenAI

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Spectra AI",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Inter:wght@300;400;500;600&display=swap');

    /* Global theme */
    :root {
        --primary: #00f5d4;
        --secondary: #7b2fff;
        --accent: #ff6b35;
        --bg-dark: #0a0e1a;
        --bg-card: #111827;
        --bg-panel: #0f172a;
        --text-main: #e2e8f0;
        --text-muted: #64748b;
        --border: #1e293b;
        --success: #00f5d4;
        --warning: #fbbf24;
        --info: #60a5fa;
    }

    /* App background */
    .stApp {
        background-color: var(--bg-dark);
        background-image:
            radial-gradient(ellipse at 20% 50%, rgba(123,47,255,0.08) 0%, transparent 60%),
            radial-gradient(ellipse at 80% 20%, rgba(0,245,212,0.06) 0%, transparent 50%);
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
    }

    /* Hide default streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {
        background: var(--bg-panel) !important;
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] > div { padding: 1.5rem 1rem; }

    .sidebar-title {
        font-family: 'Orbitron', monospace;
        font-size: 1rem;
        font-weight: 700;
        color: var(--primary);
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .sidebar-about {
        background: rgba(0,245,212,0.04);
        border: 1px solid rgba(0,245,212,0.15);
        border-radius: 8px;
        padding: 0.9rem;
        font-size: 0.8rem;
        color: var(--text-muted);
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    .sidebar-section-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        color: var(--secondary);
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid var(--border);
    }

    .history-item {
        background: rgba(255,255,255,0.03);
        border-left: 2px solid var(--secondary);
        border-radius: 0 6px 6px 0;
        padding: 0.5rem 0.7rem;
        margin-bottom: 0.4rem;
        font-size: 0.75rem;
        color: var(--text-muted);
        font-family: 'Share Tech Mono', monospace;
    }

    /* ── MAIN HEADER ── */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        margin-bottom: 1.5rem;
        position: relative;
    }

    .main-header::after {
        content: '';
        display: block;
        width: 200px;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--primary), transparent);
        margin: 1rem auto 0 auto;
    }

    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 0.04em;
        line-height: 1.2;
        margin-bottom: 0.4rem;
    }

    .main-caption {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.82rem;
        color: var(--text-muted);
        letter-spacing: 0.08em;
    }

    /* ── INPUT CARD ── */
    .input-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    }

    .input-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.72rem;
        color: var(--primary);
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }

    /* Streamlit input override */
    .stTextInput > div > div > input {
        background: #1e293b !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1rem !important;
        transition: border-color 0.2s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(0,245,212,0.1) !important;
        color: #ffffff !important;
    }
    .stTextInput > div > div > input::placeholder { color: #64748b !important; }

    /* Selectbox text color fix */
    .stSelectbox > div > div {
        background: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }
    .stSelectbox svg { fill: var(--primary) !important; }

    /* ── BUTTONS ── */
    .stButton > button {
        width: 100%;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-family: 'Orbitron', monospace;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        border: none;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    /* Button 1 — Simplify (teal) */
    div[data-testid="column"]:first-child .stButton > button {
        background: linear-gradient(135deg, #00c9a7 0%, #00f5d4 100%);
        color: #0a0e1a;
    }
    div[data-testid="column"]:first-child .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,245,212,0.35);
    }

    /* Button 2 — Research (purple) */
    div[data-testid="column"]:last-child .stButton > button {
        background: linear-gradient(135deg, #6d28d9 0%, #7b2fff 100%);
        color: #ffffff;
    }
    div[data-testid="column"]:last-child .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(123,47,255,0.4);
    }

    /* ── RESPONSE CARD ── */
    .response-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.8rem;
        margin-top: 1.5rem;
        box-shadow: 0 4px 32px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
    }

    .response-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
    }

    .response-card.simplify::before {
        background: linear-gradient(90deg, var(--primary), #00c9a7);
    }

    .response-card.research::before {
        background: linear-gradient(90deg, var(--secondary), #a855f7);
    }

    .response-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 1.2rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid var(--border);
    }

    .response-badge {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-weight: 600;
    }

    .badge-simplify {
        background: rgba(0,245,212,0.1);
        color: var(--primary);
        border: 1px solid rgba(0,245,212,0.3);
    }

    .badge-research {
        background: rgba(123,47,255,0.1);
        color: #a78bfa;
        border: 1px solid rgba(123,47,255,0.3);
    }

    .response-topic {
        font-family: 'Orbitron', monospace;
        font-size: 0.85rem;
        color: var(--text-muted);
        letter-spacing: 0.04em;
    }

    /* Markdown content inside response */
    .response-card p, .response-card li {
        color: var(--text-main) !important;
        font-size: 0.92rem;
        line-height: 1.75;
    }

    .response-card h1, .response-card h2, .response-card h3 {
        font-family: 'Orbitron', monospace;
        color: var(--primary) !important;
        letter-spacing: 0.03em;
    }

    .response-card strong { color: #f1f5f9 !important; }
    .response-card code {
        background: rgba(0,245,212,0.08) !important;
        color: var(--primary) !important;
        border-radius: 4px;
        padding: 0.15em 0.4em;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.85em;
    }

    /* Streamlit markdown override */
    .element-container .stMarkdown p { color: var(--text-main); font-size: 0.92rem; line-height: 1.75; }

    /* ── DIVIDER ── */
    hr { border-color: var(--border) !important; margin: 1.5rem 0; }

    /* ── SPINNER ── */
    .stSpinner > div { border-top-color: var(--primary) !important; }

    /* ── ALERTS ── */
    .stAlert { border-radius: 8px !important; font-family: 'Inter', sans-serif; }

    /* ── STATUS CHIPS ── */
    .status-row {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    .status-chip {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.08em;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.04);
        color: var(--text-muted);
        border: 1px solid var(--border);
    }
    .status-chip.online { color: var(--primary); border-color: rgba(0,245,212,0.3); background: rgba(0,245,212,0.06); }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "last_mode" not in st.session_state:
    st.session_state.last_mode = None

if "last_topic" not in st.session_state:
    st.session_state.last_topic = None


# ─────────────────────────────────────────────
#  OPENAI CLIENT SETUP
# ─────────────────────────────────────────────
def get_client():
    """Initialize OpenAI client from secrets or session state."""
    api_key = st.session_state.get("api_key", "").strip()
    base_url = st.session_state.get("base_url", "").strip()

    if not api_key:
        return None, "⚠️ No API key provided."

    kwargs = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url

    try:
        client = OpenAI(**kwargs)
        return client, None
    except Exception as e:
        return None, f"Client init error: {e}"


# ─────────────────────────────────────────────
#  AI CALL FUNCTION
# ─────────────────────────────────────────────
def call_ai(client, system_prompt: str, user_query: str, model: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ],
        temperature=0.7,
        max_tokens=1500,
    )
    return response.choices[0].message.content


# ─────────────────────────────────────────────
#  SYSTEM PROMPTS
# ─────────────────────────────────────────────
SIMPLIFY_SYSTEM = """You are Professor Spectra, an elite telecommunication engineering professor with 25+ years of experience at MIT and Stanford. Your superpower is making brutally complex engineering mathematics, protocols, and standards feel crystal clear.

When explaining a topic:
- Open with a vivid, memorable real-world analogy that maps perfectly to the technical concept
- Break down the core mechanism into 4-6 crisp bullet points (each bullet: one clear idea, no filler)
- Include the key mathematical intuition in plain English — don't skip the math, but never let it be the obstacle
- Close with a "Why Engineers Care" section: practical applications and career relevance

Formatting rules:
- Use **bold** for key technical terms on first use
- Use `code style` for equations, standards (e.g., `3GPP TS 38.211`), or acronyms
- Use emoji sparingly but strategically (📡 🔁 📶 ⚡) to anchor key ideas visually
- Never condescend. Never oversimplify. Technical precision is non-negotiable.
- Your tone: brilliant friend who happens to be an expert, not a textbook."""

RESEARCH_SYSTEM = """You are Dr. Spectra, a Senior Telecom Research Scientist with deep expertise in IEEE standards bodies and 3GPP working groups. You synthesize the current state of engineering knowledge with the rigor of a Nature review paper and the clarity of a top-tier conference talk.

Structure every response in exactly these three sections with these exact headers:

## 🟢 Scientific Consensus
*What the field agrees on — backed by IEEE, ITU, and 3GPP standards*
(3-5 bullet points of established, peer-reviewed facts with standard references where possible)

## 🟡 Research Gaps & Open Debates
*Where experts disagree or knowledge is incomplete*
(3-4 bullet points covering active controversies, unsolved problems, or competing approaches)

## 🔵 Future Trends & Emerging Directions
*Where the field is heading in the next 5-10 years*
(3-4 bullet points on cutting-edge research, upcoming standards, and transformative technologies)

Formatting rules:
- Each bullet: 1-2 sentences, dense with information, zero fluff
- Reference real standards and research directions (e.g., "3GPP Release 18", "IEEE 802.11be")
- Use **bold** for key terms and `monospace` for standard identifiers
- Maintain scientific objectivity — present debates fairly, not one-sidedly
- Tone: authoritative, precise, intellectually stimulating."""


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🛰️ Spectra AI Navigation</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-about">
        <strong style="color:#e2e8f0;">Your Engineering Second Brain</strong><br><br>
        Spectra AI is built for undergraduate telecom engineers and junior professionals who want to learn faster,
        research smarter, and understand concepts at a deeper level — powered by AI with engineering-grade precision.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── API Configuration ──
    st.markdown('<div class="sidebar-section-label">⚙️ API Configuration</div>', unsafe_allow_html=True)

    api_key_input = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-...",
        key="api_key",
        help="Your OpenAI-compatible API key",
        label_visibility="collapsed",
    )
    st.caption("🔑 API Key")

    base_url_input = st.text_input(
        "Base URL (optional)",
        placeholder="https://api.openai.com/v1",
        key="base_url",
        help="Leave blank for OpenAI default. Set for compatible providers.",
        label_visibility="collapsed",
    )
    st.caption("🌐 Base URL (optional)")

    model_name = st.selectbox(
        "Model",
        options=[
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "gpt-4o-mini",
            "gpt-4o",
        ],
        index=0,
        key="model",
        label_visibility="collapsed",
    )
    st.caption(f"🤖 Model: `{model_name}`")

    st.markdown("---")

    # ── Learning History ──
    st.markdown('<div class="sidebar-section-label">📚 Learning History</div>', unsafe_allow_html=True)

    if st.session_state.history:
        for item in reversed(st.session_state.history[-8:]):
            icon = "✨" if item["mode"] == "simplify" else "📊"
            st.markdown(
                f'<div class="history-item">{icon} {item["topic"][:32]}{"…" if len(item["topic"]) > 32 else ""}</div>',
                unsafe_allow_html=True,
            )
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.markdown(
            '<div class="history-item" style="color:#374151; border-color:#1e293b;">No sessions yet…</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        '<div style="font-family:\'Share Tech Mono\',monospace;font-size:0.65rem;color:#374151;text-align:center;">SPECTRA AI v1.0 · TELECOM EDITION</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  MAIN CONTENT
# ─────────────────────────────────────────────

# Header
st.markdown("""
<div class="main-header">
    <div class="main-title">🛰️ Spectra AI</div>
    <div style="font-family:'Orbitron',monospace;font-size:1rem;color:#94a3b8;letter-spacing:0.08em;margin-bottom:0.3rem;">
        Telecom Engineering Assistant
    </div>
    <div class="main-caption">
        SIMPLIFY · RESEARCH · MASTER · TELECOMMUNICATION ENGINEERING
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input Card ──
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="input-label">📡 Enter a Telecom Topic or Research Query</div>', unsafe_allow_html=True)

topic = st.text_input(
    label="topic_input",
    placeholder='e.g., "Massive MIMO in 5G NR", "QAM Modulation", "OFDM subcarrier spacing"...',
    label_visibility="collapsed",
    key="topic_input",
)

# ── Action Buttons ──
col1, col2 = st.columns(2)

with col1:
    simplify_clicked = st.button("✨ Simplify Concept", use_container_width=True)

with col2:
    research_clicked = st.button("📊 Research Consensus", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  BUTTON LOGIC
# ─────────────────────────────────────────────
def handle_query(mode: str):
    """Shared logic for both buttons."""
    if not topic.strip():
        st.warning("⚠️ Please enter a telecom topic before running a query.")
        return

    client, err = get_client()
    if err:
        st.error(f"**API Error:** {err}\n\n👈 Add your API key in the sidebar to get started.")
        return

    system_prompt = SIMPLIFY_SYSTEM if mode == "simplify" else RESEARCH_SYSTEM
    spinner_msg = (
        "🔬 Professor Spectra is building your breakdown…"
        if mode == "simplify"
        else "🔭 Dr. Spectra is scanning the research landscape…"
    )

    with st.spinner(spinner_msg):
        try:
            result = call_ai(client, system_prompt, topic.strip(), st.session_state.model)
            st.session_state.last_response = result
            st.session_state.last_mode = mode
            st.session_state.last_topic = topic.strip()

            # Save to history
            st.session_state.history.append({"topic": topic.strip(), "mode": mode})

        except Exception as e:
            error_msg = str(e)
            if "authentication" in error_msg.lower() or "api_key" in error_msg.lower():
                st.error("🔑 **Authentication Failed:** Your API key appears to be invalid or expired. Check the sidebar.")
            elif "rate_limit" in error_msg.lower():
                st.error("⏳ **Rate Limit Hit:** Too many requests. Please wait a moment and try again.")
            elif "model_not_found" in error_msg.lower() or "model" in error_msg.lower():
                st.error(f"🤖 **Model Error:** The selected model may not be available with your API key. Try a different model in the sidebar.\n\n`{error_msg}`")
            else:
                st.error(f"❌ **Unexpected Error:**\n\n```\n{error_msg}\n```")


if simplify_clicked:
    handle_query("simplify")

if research_clicked:
    handle_query("research")


# ─────────────────────────────────────────────
#  RESPONSE DISPLAY
# ─────────────────────────────────────────────
if st.session_state.last_response:
    mode = st.session_state.last_mode
    response_text = st.session_state.last_response
    topic_display = st.session_state.last_topic

    badge_class = "badge-simplify" if mode == "simplify" else "badge-research"
    badge_label = "CONCEPT BREAKDOWN" if mode == "simplify" else "RESEARCH CONSENSUS"
    card_class = "simplify" if mode == "simplify" else "research"

    st.markdown(f"""
    <div class="response-card {card_class}">
        <div class="response-header">
            <span class="response-badge {badge_class}">{badge_label}</span>
            <span class="response-topic">// {topic_display}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Render the actual markdown response inside a styled container
    with st.container():
        if mode == "simplify":
            st.success("✨ **Concept Simplified by Professor Spectra**")
        else:
            st.info("📊 **Research Consensus by Dr. Spectra**")

        st.markdown(response_text)

    # Status chips
    st.markdown(f"""
    <div class="status-row">
        <span class="status-chip online">● RESPONSE READY</span>
        <span class="status-chip">MODEL: {st.session_state.model.upper()}</span>
        <span class="status-chip">TOPIC: {topic_display[:30].upper()}{'…' if len(topic_display) > 30 else ''}</span>
        <span class="status-chip">SESSION QUERIES: {len(st.session_state.history)}</span>
    </div>
    """, unsafe_allow_html=True)

# ── Empty state ──
else:
    st.markdown("""
    <div style="
        text-align:center;
        padding: 3rem 2rem;
        background: rgba(255,255,255,0.015);
        border: 1px dashed #1e293b;
        border-radius: 12px;
        margin-top: 1rem;
    ">
        <div style="font-size:2.5rem;margin-bottom:0.8rem;">📡</div>
        <div style="font-family:'Orbitron',monospace;font-size:0.9rem;color:#475569;letter-spacing:0.06em;margin-bottom:0.5rem;">
            AWAITING SIGNAL
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.82rem;color:#334155;max-width:400px;margin:0 auto;line-height:1.6;">
            Enter a telecom topic above and choose your mode.<br>
            Add your API key in the sidebar to activate Spectra AI.
        </div>
    </div>
    """, unsafe_allow_html=True)
