# ==================== embeddings.py ====================
"""
Embedding and retrieval layer for SPECTRE.

Responsibilities:
- Load a lightweight, high-quality embedding model
- Build a normalized FAISS index
- Retrieve top-k relevant chunks with similarity scores
"""

from typing import List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# ---------- MODEL CONFIG ----------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# ---------- MODEL LOADING ----------
def load_model() -> SentenceTransformer:
    """
    Load and return the sentence embedding model.
    Cached at the Streamlit session level.
    """
    return SentenceTransformer(MODEL_NAME)


# ---------- INDEX BUILDING ----------
def build_index(
    texts: List[str],
    model: SentenceTransformer,
) -> Tuple[faiss.IndexFlatIP, np.ndarray]:
    """
    Build a FAISS inner-product index with L2-normalized embeddings.

    Returns:
        index      : FAISS index
        embeddings : Normalized embedding matrix
    """
    if not texts:
        raise ValueError("No texts provided to build_index")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False,
    ).astype("float32")

    faiss.normalize_L2(embeddings)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index, embeddings


# ---------- RETRIEVAL ----------
def retrieve_top_k(
    query: str,
    index: faiss.IndexFlatIP,
    model: SentenceTransformer,
    k: int = 4,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Retrieve top-k most relevant chunk indices and similarity scores.

    Returns:
        indices : array of chunk indices
        scores  : cosine similarity scores (0–1 range)
    """
    if index is None or index.ntotal == 0:
        raise RuntimeError("FAISS index is empty or not initialized")

    q_emb = model.encode(
        [query],
        convert_to_numpy=True,
        show_progress_bar=False,
    ).astype("float32")

    faiss.normalize_L2(q_emb)

    scores, indices = index.search(q_emb, k)

    return indices[0], scores[0]
