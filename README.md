# Chat With PDF

## Overview
This project, **Chat With PDF**, is a Streamlit-based application that enables users to upload a PDF file and interact with its content using a chatbot powered by large language models (LLMs). The application leverages embeddings, vector stores, and a question-answering pipeline to extract and analyze text from PDFs, enabling users to ask meaningful questions about the uploaded content.

## Features
- **PDF Upload and Parsing**: Users can upload a PDF file, which is processed to extract text from all pages.
- **Text Chunking**: Text from the PDF is split into manageable chunks using LangChain’s `RecursiveCharacterTextSplitter` for efficient processing.
- **Embeddings**: The application uses HuggingFace embeddings (via the `sentence-transformers/all-MiniLM-L6-v2` model) to create vector representations of text chunks.
- **Vector Storage**: The project uses FAISS for similarity search to retrieve relevant chunks based on user queries.
- **Question Answering**: A transformer-based pipeline (from HuggingFace’s `deepset/roberta-base-squad2` model) answers user questions by analyzing the relevant text chunks.
- **Streamlit Interface**: A simple and interactive UI for uploading PDFs, asking questions, and viewing results.

## Technologies Used
### Libraries and Frameworks
- **Streamlit**: Frontend framework for building interactive web applications.
- **LangChain**: For text processing and chunking.
- **HuggingFace**: Provides pre-trained models for embeddings and question answering.
- **FAISS**: Vector storage and similarity search.
- **PyPDF2**: For reading and extracting text from PDF files.
- **dotenv**: For environment variable management.

### File Details
1. **app.py**:
   - The main script that implements the application’s logic.
   - Defines the UI, PDF processing pipeline, embeddings generation, and QA pipeline.

2. **requirements.txt**:
   - Contains the list of dependencies required to run the application.

## Installation
Follow these steps to set up and run the project locally:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

5. Open the app in your browser at [http://localhost:8501](http://localhost:8501).

## Usage
1. **Upload a PDF File**:
   - Use the "Upload your PDF file" button to upload a document.
2. **Ask Questions**:
   - Enter your question in the text box, and the app will retrieve relevant text chunks and provide an answer.
3. **View Results**:
   - The answer will be displayed along with any supporting context.

## Example Use Case
- Upload a research paper and ask specific questions about methodologies or results.
- Analyze long reports by querying particular sections without manually searching through the document.

## Future Improvements
- Add support for multiple file formats (e.g., Word, Excel).
- Optimize embeddings for faster performance with larger documents.
- Enhance UI/UX with additional features like visualization of search results.

## Developer Information
**Author**: Mahesh  
**Contact**: Feel free to reach out for any queries or suggestions.


## User Interface
Chat WIth PDF

![alt](https://github.com/MaheshD1218/chat-with-pdf/blob/ef4dd28cfa5819f6912bce930635605f19e7fbf2/Assets/first.png)



![alt](https://github.com/MaheshD1218/chat-with-pdf/blob/ef4dd28cfa5819f6912bce930635605f19e7fbf2/Assets/second.png)



![alt](https://github.com/MaheshD1218/chat-with-pdf/blob/ef4dd28cfa5819f6912bce930635605f19e7fbf2/Assets/third.png)
