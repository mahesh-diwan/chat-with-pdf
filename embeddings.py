from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def build_index(chunks, model):
    embeddings = model.encode(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index, embeddings
