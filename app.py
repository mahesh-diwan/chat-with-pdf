import streamlit as st
from config import SYSTEM_PROMPT
from ui import load_styles, display_diagnostic, display_chat, display_typing # Added missing imports
from pdf_processor import read_pdf, chunk_text
from embeddings import load_model, build_index
from ai_engine import ask_gemini
from utils import timestamp

# Page Config
st.set_page_config(page_title="SPECTRE", page_icon="🌌", layout="centered")
load_styles()

# ---------------- SESSION INITIALIZATION ----------------
if "index" not in st.session_state:
    st.session_state.index = None
    st.session_state.texts = None
if "chat" not in st.session_state:
    st.session_state.chat = []
    display_diagnostic() # Run boot sequence only on first load

# App Header
st.markdown("<div class='glitch-title'>SPECTRE</div>", unsafe_allow_html=True)
st.markdown("<p style='color:#38bdf8; font-size: 0.8rem;'>NEURAL_LINK_ESTABLISHED // DATA_PORT_OPEN</p>", unsafe_allow_html=True)

# ---------------- DOCUMENT UPLOAD ----------------
with st.expander("📁 SOURCE MANAGEMENT", expanded=(st.session_state.index is None)):
    file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
    if file and st.session_state.index is None:
        with st.status("🏗️ Building Knowledge Base...") as status:
            text = read_pdf(file)
            chunks = chunk_text(text)
            model = load_model()
            index, _ = build_index(chunks, model)
            st.session_state.index = index
            st.session_state.texts = chunks
            status.update(label="Document Synced.", state="complete", expanded=False)
        st.rerun()

# ---------------- CHAT DISPLAY ----------------
chat_container = st.container()
with chat_container:
    display_chat(st.session_state.chat)

# ---------------- CHAT INPUT & ENGINE ----------------
if query := st.chat_input("INITIALIZE SCAN..."):
    # 1. Add User Message
    st.session_state.chat.append({"role": "user", "content": query, "time": timestamp()})
    with chat_container:
        display_chat([st.session_state.chat[-1]])

    if st.session_state.index:
        with st.status("📡 SYSTEM_LOG", expanded=False) as status:
            st.write("Targeting Semantic Sectors...")
            model = load_model()
            q_emb = model.encode([query]).astype("float32")
            _, I = st.session_state.index.search(q_emb, k=5)
            context = "\n\n".join(st.session_state.texts[i] for i in I[0])
            
            st.write("Neural Link Response Pending...")
            answer = ask_gemini(query, context)
            status.update(label="SIGNAL ACQUIRED", state="complete")

        with chat_container:
            st.session_state.chat.append({"role": "assistant", "content": answer, "time": timestamp()})
            display_typing(answer, role="assistant")
    else:
        st.warning("Please upload a PDF to activate SPECTRE.")