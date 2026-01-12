# ==================== app.py ====================
import streamlit as st
from ui import load_styles, app_title, display_chat, display_typing
from pdf_processor import read_pdf_with_metadata, chunk_text_with_metadata
from embeddings import load_model, build_index
from ai_engine import ask_gemini
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
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "index" not in st.session_state:
    st.session_state.index = None
    st.session_state.texts = None
    st.session_state.metadata = None
    st.session_state.filename = None

if "chat" not in st.session_state:
    st.session_state.chat = []


def reset_system():
    st.session_state.index = None
    st.session_state.texts = None
    st.session_state.metadata = None
    st.session_state.filename = None
    st.session_state.chat = []
    st.session_state.uploader_key += 1
    st.rerun()


# ---------- HEADER ----------
app_title()

# ---------- CONTROL BAR ----------
left, mid, right = st.columns([2, 5, 2])

with left:
    with st.popover("LOAD", use_container_width=True):
        file = st.file_uploader(
            "Upload PDF",
            type="pdf",
            label_visibility="collapsed",
            key=f"pdf_{st.session_state.uploader_key}"
        )

with mid:
    if st.session_state.index:
        st.markdown(
            f"<div class='doc-name'>Loaded: {st.session_state.filename}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div class='doc-muted'>No document loaded</div>",
            unsafe_allow_html=True
        )

with right:
    st.button("RESET", use_container_width=True, on_click=reset_system)

# ---------- FILE PROCESSING ----------
if file and (st.session_state.index is None or file.name != st.session_state.filename):
    with st.spinner("Indexing document..."):
        text_data = read_pdf_with_metadata(file)
        chunks, meta = chunk_text_with_metadata(text_data)
        model = load_model()
        index, _ = build_index(chunks, model)

        st.session_state.index = index
        st.session_state.texts = chunks
        st.session_state.metadata = meta
        st.session_state.filename = file.name
        st.session_state.chat = []

    st.rerun()

# ---------- CHAT ----------
display_chat(st.session_state.chat)

if query := st.chat_input("Ask a question…"):
    user_msg = {
        "role": "user",
        "content": query,
        "time": timestamp()
    }
    st.session_state.chat.append(user_msg)
    display_chat([user_msg])

    if not st.session_state.index:
        st.warning("Load a document first.")
    else:
        model = load_model()
        q_emb = model.encode([query]).astype("float32")
        distances, I = st.session_state.index.search(q_emb, k=4)

        context = []
        pages = set()
        for i in I[0]:
            context.append(st.session_state.texts[i])
            pages.add(str(st.session_state.metadata[i]["page"]))

        answer = ask_gemini(query, "\n\n".join(context))
        final = f"{answer}\n\nSources: {', '.join(sorted(pages))}"

        display_typing(final)
        st.session_state.chat.append({
            "role": "assistant",
            "content": final,
            "time": timestamp()
        })
