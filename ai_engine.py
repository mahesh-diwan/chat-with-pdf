import google.generativeai as genai
from config import SYSTEM_PROMPT

def ask_gemini(query, context, top_k=8):
    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{query}
"""
    model_gemini = genai.GenerativeModel("gemini-2.5-flash")
    response = model_gemini.generate_content(prompt)
    return response.text
