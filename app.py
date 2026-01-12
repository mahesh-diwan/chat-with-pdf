import streamlit as st
from config import SYSTEM_PROMPT
from ui import load_styles, display_chat
from pdf_processor import read_pdf, chunk_text
from embeddings import load_model, build_index
from ai_engine import ask_gemini
from utils import timestamp

st.set_page_config(page_title="SPECTRE", page_icon="🌌", layout="wide")
load_styles()

st.markdown("<h1 style='color:#38bdf8;font-weight:700;font-size:2.5rem'>SPECTRE</h1><p>AI Document Intelligence Chat</p>", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "index" not in st.session_state:
    st.session_state.index = None
    st.session_state.texts = None
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- PDF UPLOAD ----------------
with st.expander("📄 Upload PDF Document", expanded=True):
    file = st.file_uploader("Upload PDF", type="pdf")

    if file and st.session_state.index is None:
        text = read_pdf(file)
        chunks = chunk_text(text)
        model = load_model()
        index, _ = build_index(chunks, model)
        st.session_state.index = index
        st.session_state.texts = chunks
        st.success("Document indexed successfully!")

from ui import display_chat, load_styles, display_typing

# ---------------- CHAT ----------------
display_chat(st.session_state.chat)

if st.session_state.index:
    query = st.text_input("Ask about the document", key="query_input")

    if query:
        st.session_state.chat.append({"role":"user", "content": query, "time": timestamp()})
        display_chat(st.session_state.chat)  # show user input immediately

        # Retrieve relevant chunks
        model = load_model()
        q_emb = model.encode([query]).astype("float32")
        _, I = st.session_state.index.search(q_emb, k=8)
        context = "\n\n".join(st.session_state.texts[i] for i in I[0])

        # Get AI answer with typing animation
        with st.spinner("🤖 Thinking..."):
            answer = ask_gemini(query, context)

        st.session_state.chat.append({"role":"assistant", "content": answer, "time": timestamp()})
        display_typing(answer, role="assistant")  # animated output

        # Expandable sources
        st.markdown(f"""
        <details>
        <summary style="color:#38bdf8;font-size:13px;cursor:pointer">Show source snippets (optional)</summary>
        <div class='source-container'>""" + "\n\n".join(st.session_state.texts[i][:500]+"..." for i in I[0]) + "</div></details>", unsafe_allow_html=True)

