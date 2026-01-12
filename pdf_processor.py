import PyPDF2

def read_pdf_with_metadata(file):
    reader = PyPDF2.PdfReader(file)
    pages_content = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages_content.append({"text": text, "page": i + 1})
    return pages_content

def chunk_text_with_metadata(pages_content, chunk_size=1000):
    chunks = []
    metadata = []
    for item in pages_content:
        text = item["text"]
        page_num = item["page"]
        # Split text into chunks but keep the page number for each
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i + chunk_size])
            metadata.append({"page": page_num})
    return chunks, metadata