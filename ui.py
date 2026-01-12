# ==================== ui.py ====================
import streamlit as st
import time

def load_styles():
    st.markdown("""
    <style>
    /* ---------- GLOBAL ---------- */
    html, body {
        background: #0b0b0b;
        color: #e5e7eb;
        font-family: 'Sora', 'Space Grotesk', 'JetBrains Mono', Inter, system-ui, sans-serif;
    }

    /* ---------- TITLE ---------- */
    .app-title {
        font-size: 2.2rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }

    .app-subtitle {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-bottom: 1.5rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    /* ---------- BUTTONS ---------- */
    .stButton > button {
        height: 38px;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        background: #0f172a;
        border: 1px solid #1f2937;
        color: #9ca3af;
        border-radius: 6px;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background: #020617;
        color: #e5e7eb;
    }

    /* ---------- CHAT ---------- */
    .chat-line {
        padding: 0.65rem 0.9rem;
        border-radius: 6px;
        background-color: #1f2937;
        margin-bottom: 0.5rem;
        word-wrap: break-word;
        transition: background 0.2s;
        font-family: 'Sora', sans-serif;
    }

    .chat-line:hover {
        background-color: #272e3d;
    }

    .chat-user {
        font-size: 0.75rem;
        letter-spacing: 0.08em;
        color: #9ca3af;
        font-weight: 500;
        margin-bottom: 0.15rem;
    }

    .chat-text {
        font-size: 0.875rem;
        line-height: 1.5;
        color: #e5e7eb;
    }

    /* ---------- SOURCE SNIPPET (unchanged) ---------- */
    .source-snippet {
        background-color: #111827;
        color: #e5e7eb;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #4f46e5;
        overflow-wrap: break-word;
        line-height: 1.5;
    }

    /* ---------- DOCUMENT STATUS ---------- */
    .doc-name {
        font-size: 0.9rem;
        color: #e5e7eb;
        padding-top: 8px;
        font-weight: 500;
    }

    .doc-muted {
        font-size: 0.9rem;
        color: #6b7280;
        padding-top: 8px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)


def app_title():
    st.markdown("<div class='app-title'>SPECTRE</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='app-subtitle'>Document Intelligence Console</div>",
        unsafe_allow_html=True
    )


def display_chat(messages):
    for m in messages:
        st.markdown(
            f"""
            <div class='chat-line'>
                <div class='chat-user'>{m['role'].upper()} · {m['time']}</div>
                <div class='chat-text'>{m['content']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def display_typing(text):
    placeholder = st.empty()
    out = ""
    for c in text:
        out += c
        placeholder.markdown(
            f"""
            <div class='chat-line'>
                <div class='chat-user'>ASSISTANT</div>
                <div class='chat-text'>{out}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.004)
