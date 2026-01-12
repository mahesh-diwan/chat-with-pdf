# ==================== ui.py ====================
import streamlit as st
import time

def load_styles():
    st.markdown("""
    <style>
    html, body {
        background: #0b0b0b;
        color: #e5e7eb;
        font-family: Inter, system-ui, sans-serif;
    }

    /* ---------- TITLE ---------- */
    .app-title {
        font-size: 2.1rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        font-size: 0.75rem;
        color: #9ca3af;
        margin-bottom: 1.2rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
    }

    /* ---------- BUTTONS ---------- */
    .stButton > button {
        height: 38px;
        font-size: 0.7rem;
        letter-spacing: 0.12em;
        background: #0f172a;
        border: 1px solid #1f2937;
        color: #9ca3af;
        border-radius: 4px;
    }

    .stButton > button:hover {
        background: #020617;
        color: #e5e7eb;
    }

    /* ---------- POPOVER ---------- */
    div[data-testid="stPopover"] button {
        height: 38px;
        font-size: 0.7rem;
        letter-spacing: 0.12em;
    }

    /* ---------- FILE UPLOADER ---------- */
    div[data-testid="stFileUploader"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* ---------- DOCUMENT STATUS ---------- */
    .doc-name {
        font-size: 0.85rem;
        color: #e5e7eb;
        padding-top: 8px;
    }

    .doc-muted {
        font-size: 0.85rem;
        color: #6b7280;
        padding-top: 8px;
    }

    /* ---------- CHAT ---------- */
    .chat-line {
        padding: 0.6rem 0;
        border-bottom: 1px solid #1f2933;
    }

    .chat-user {
        font-size: 0.65rem;
        letter-spacing: 0.1em;
        color: #9ca3af;
    }

    .chat-text {
        margin-top: 0.2rem;
        line-height: 1.6;
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
