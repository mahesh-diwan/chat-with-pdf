# ==================== pdf_processor.py ====================
"""
PDF ingestion and chunking logic for SPECTRE.

Responsibilities:
- Extract text with page-level metadata
- Chunk text deterministically while preserving source traceability
"""

from typing import Dict, List, Tuple

import PyPDF2


# ---------- PDF READING ----------
def read_pdf_with_metadata(file) -> List[Dict]:
    """
    Extract text from a PDF file with page numbers.

    Returns:
        List of dicts:
        [
            {"text": "...", "page": 1},
            ...
        ]
    """
    reader = PyPDF2.PdfReader(file)
    pages_content: List[Dict] = []

    for page_index, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            cleaned = text.strip()
            if cleaned:
                pages_content.append(
                    {
                        "text": cleaned,
                        "page": page_index + 1,
                    }
                )

    return pages_content


# ---------- CHUNKING ----------
def chunk_text_with_metadata(
    pages_content: List[Dict],
    chunk_size: int = 800,
    overlap: int = 120,
) -> Tuple[List[str], List[Dict]]:
    """
    Chunk text with overlap while preserving page metadata.

    Overlap improves semantic continuity during retrieval.

    Returns:
        chunks   : List[str]
        metadata : List[{"page": int}]
    """
    chunks: List[str] = []
    metadata: List[Dict] = []

    for item in pages_content:
        text = item["text"]
        page_num = item["page"]

        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]

            chunks.append(chunk)
            metadata.append({"page": page_num})

            start = end - overlap
            if start < 0:
                start = 0

    return chunks, metadata
