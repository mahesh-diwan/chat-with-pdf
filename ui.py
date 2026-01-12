import streamlit as st
import time

def load_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=JetBrains+Mono:wght@300;500;800&display=swap');

    /* 1. TOTAL INTERFACE CLEANUP */
    header, footer, .stAppDeployButton, #MainMenu {visibility: hidden !important; display: none !important;}
    
    /* This targets the fixed bar at the bottom that holds the input */
    [data-testid="stBottom"] {
        background-color: transparent !important;
        border: none !important;
    }
    
    [data-testid="stChatInputContainer"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* 2. CORE THEME & GRID (The Ghost Look) */
    .stApp {
        background-color: #010203 !important;
        background-image: linear-gradient(0deg, transparent 24%, rgba(56, 189, 248, .05) 25%, rgba(56, 189, 248, .05) 26%, transparent 27%, transparent 74%, rgba(56, 189, 248, .05) 75%, rgba(56, 189, 248, .05) 76%, transparent 77%, transparent), 
                          linear-gradient(90deg, transparent 24%, rgba(56, 189, 248, .05) 25%, rgba(56, 189, 248, .05) 26%, transparent 27%, transparent 74%, rgba(56, 189, 248, .05) 75%, rgba(56, 189, 248, .05) 76%, transparent 77%, transparent);
        background-size: 50px 50px;
    }

    /* 3. THE FLOATING INPUT */
    /* We style the inner div so it looks like a floating console */
    [data-testid="stChatInput"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 0px !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.2) !important;
        padding: 5px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #00f2ff !important;
        font-family: 'Share Tech Mono', monospace !important;
        background: transparent !important;
    }

    /* 4. CHAT READABILITY */
    .ai-bubble {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-left: 4px solid #00f2ff;
        padding: 25px;
        color: #e2e8f0;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 30px;
        position: relative;
    }

    .ai-bubble::before {
        content: "SIGNAL_DECODED //";
        position: absolute;
        top: -12px; left: 10px;
        background: #010203;
        color: #00f2ff;
        font-family: 'Share Tech Mono', monospace;
        font-size: 10px;
        padding: 0 5px;
        letter-spacing: 2px;
    }

    .user-bubble {
        border-right: 3px solid #ff0055;
        color: #f8fafc;
        font-family: 'JetBrains Mono', monospace;
        padding: 15px;
        margin: 15px 0;
        text-align: right;
        background: rgba(255, 0, 85, 0.05);
    }

    /* Glitch Title */
    .glitch-title {
        font-family: 'Share Tech Mono', monospace;
        font-size: 4rem;
        font-weight: 800;
        color: #38bdf8;
        text-shadow: 3px 3px #ff0055, -3px -3px #00ff41;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def display_diagnostic():
    log_placeholder = st.empty()
    logs = [
        "SYSTEM_BOOT_INITIATED...", 
        "BYPASSING_STREAMLIT_CHROME...", 
        "NEURAL_LINK_ESTABLISHED.", 
        "SPECTRE_READY."
    ]
    for log in logs:
        log_placeholder.markdown(f"<p style='color:#38bdf8; font-family:\"Share Tech Mono\"; font-size:12px;'>[CONSOLE] {log}</p>", unsafe_allow_html=True)
        time.sleep(0.4)
    log_placeholder.empty()

def display_chat(chat_history):
    for msg in chat_history:
        role_class = "user-bubble" if msg["role"] == "user" else "ai-bubble"
        prefix = "USR > " if msg["role"] == "user" else ""
        st.markdown(f"<div class='{role_class}'>{prefix}{msg['content']}</div>", unsafe_allow_html=True)

def display_typing(text, role="assistant"):
    role_class = "ai-bubble" if role == "assistant" else "user-bubble"
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(f"<div class='{role_class}'>{full_text}█</div>", unsafe_allow_html=True)
        time.sleep(0.003) # Slightly faster for a modern feel
    placeholder.markdown(f"<div class='{role_class}'>{full_text}</div>", unsafe_allow_html=True)