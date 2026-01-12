import streamlit as st
import time

def load_styles():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(160deg, #0c0f1e, #010205);
        color: #e5e7eb;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
    }
    header, footer {visibility: hidden;}
    .block-container {padding:1rem 2rem;}

    #chat-window {max-height:650px; overflow-y:auto; padding:10px; margin-bottom:12px; scroll-behavior:smooth;}
    .user-bubble {background:#0d6efd44; color:#38bdf8; border-radius:16px 16px 0 16px; padding:14px; margin:8px 0; max-width:65%; margin-left:auto; font-size:14px; line-height:1.7;}
    .ai-bubble {background: rgba(56,189,248,0.08); color:#e5e7eb; border-radius:16px 16px 16px 0; padding:14px; margin:8px 0; max-width:70%; font-size:14px; line-height:1.8; white-space:pre-wrap;}
    .timestamp {font-size:10px; color:#94a3b8; text-align:right; margin-top:4px;}
    .source-container {background: rgba(31,41,55,0.7); color:#cbd5e1; border-radius:10px; padding:8px; font-size:13px; margin:6px 0; white-space:pre-wrap;}
    </style>
    """, unsafe_allow_html=True)

def display_chat(chat):
    st.markdown("<div id='chat-window'>", unsafe_allow_html=True)
    for msg in chat:
        role_class = "user-bubble" if msg["role"]=="user" else "ai-bubble"
        icon = "🧑" if msg["role"]=="user" else "🤖"
        timestamp = msg.get("time", "")
        st.markdown(f"<div class='{role_class}'>{icon} {msg['content']}<div class='timestamp'>{timestamp}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def display_typing(text, role="assistant"):
    role_class = "ai-bubble" if role=="assistant" else "user-bubble"
    placeholder = st.empty()
    display_text = ""
    for char in text:
        display_text += char
        placeholder.markdown(
            f"<div class='{role_class}'>{display_text}</div>", unsafe_allow_html=True
        )
        time.sleep(0.005)  # typing speed, adjust 0.002~0.008 for faster/slower
    return
