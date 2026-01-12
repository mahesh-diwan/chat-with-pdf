import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """You are a document intelligence assistant.
Answer ONLY from the given context.
Provide a detailed, structured, multi-paragraph answer using ONLY the document content.
If the answer is not in the document, say: "I couldn't find this in the document."
"""
