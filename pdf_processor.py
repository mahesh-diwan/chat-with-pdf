from pypdf import PdfReader

def read_pdf(file):
    reader = PdfReader(file)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text

def chunk_text(text, chunk_size=800, overlap=80):
    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(text), step):
        chunks.append(text[i:i+chunk_size])
    return chunks
