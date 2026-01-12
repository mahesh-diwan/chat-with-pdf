# ==================== app.py ====================
import streamlit as st
import numpy as np

from ui import load_styles, app_title, display_chat, display_typing
from pdf_processor import read_pdf_with_metadata, chunk_text_with_metadata
from embeddings import load_model, build_index, retrieve_top_k
from ai_engine import ask_groq, rewrite_query
from utils import timestamp

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Spectre",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_styles()

# ---------- SESSION STATE ----------
if "model" not in st.session_state:
    st.session_state.model = load_model()

# Dynamic uploader key
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

for key in ["index", "texts", "meta", "filename", "chat"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "chat" else None


def reset():
    """Clear all session state and force uploader to reset"""
    st.session_state.index = None
    st.session_state.texts = None
    st.session_state.meta = None
    st.session_state.filename = None
    st.session_state.chat = []
    st.session_state.uploader_key += 1


# ---------- HEADER ----------
app_title()

# ---------- TOP CONTROLS ----------
c1, c2, c3 = st.columns([2, 6, 2])

with c1:
    with st.popover("LOAD", use_container_width=True):
        file = st.file_uploader(
            "PDF",
            type="pdf",
            label_visibility="collapsed",
            key=f"pdf_{st.session_state.uploader_key}"  # dynamic key ensures reset
        )

with c2:
    current_file = st.session_state.filename or (file.name if file else None)
    st.markdown(
        f"<div class='doc-name'>{current_file or 'No document loaded'}</div>",
        unsafe_allow_html=True
    )


with c3:
    st.button("RESET", use_container_width=True, on_click=reset)


# ---------- PDF INGEST ----------
if file and file.name != st.session_state.filename:
    with st.spinner("Indexing document…"):
        data = read_pdf_with_metadata(file)
        chunks, meta = chunk_text_with_metadata(data)

        index, _ = build_index(chunks, st.session_state.model)

        st.session_state.index = index
        st.session_state.texts = chunks
        st.session_state.meta = meta
        st.session_state.filename = file.name
        st.session_state.chat = []



# ---------- CHAT HISTORY ----------
display_chat(st.session_state.chat)


# ---------- USER INPUT ----------
if query := st.chat_input("Ask a question…"):
    user_msg = {"role": "user", "content": query, "time": timestamp()}
    st.session_state.chat.append(user_msg)
    display_chat([user_msg])

    if not st.session_state.index:
        st.warning("Load a document first.")
        st.stop()

    # ---------- QUERY REWRITE ----------
    with st.spinner("Understanding your question…"):
        refined_query = rewrite_query(query)

    # ---------- RETRIEVAL ----------
    idxs, scores = retrieve_top_k(
        refined_query,
        st.session_state.index,
        st.session_state.model,
        k=5
    )

    # ---------- BUILD CONTEXT ----------
    context_blocks = []
    sources = {}

    for i in idxs:
        text = st.session_state.texts[i]
        page = st.session_state.meta[i]["page"]

        context_blocks.append(f"[Page {page}] {text}")
        sources.setdefault(page, []).append(text)

    context = "\n\n".join(context_blocks)

    # ---------- GROQ ANSWER ----------
    with st.spinner("Thinking…"):
        answer = ask_groq(
            query=query,
            context=context,
            grounded=True  # citation-aware answering
        )

    # ---------- CONFIDENCE ----------
    confidence = round(float(np.mean(scores)) * 100, 1)

    # ---------- FINAL ANSWER ----------
    final_answer = (
        f"{answer}\n\n"
        f"**Confidence:** {confidence}%\n"
        f"**Sources:** Pages {', '.join(map(str, sorted(sources.keys())))}"
    )

    display_typing(final_answer)

    st.session_state.chat.append({
        "role": "assistant",
        "content": final_answer,
        "time": timestamp()
    })

    # ---------- SOURCE VIEWER ----------
    with st.expander("📄 View source excerpts"):
        for page, snippets in sources.items():
            st.markdown(f"**Page {page}**")
            for s in snippets:
                st.markdown(
                    f"<div class='source-snippet'>{s}</div>",
                    unsafe_allow_html=True
                )
