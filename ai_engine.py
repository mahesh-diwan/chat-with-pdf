# ==================== ai_engine.py ====================
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ---------- CLIENT SETUP ----------
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=API_KEY)

# Fast, free, currently supported
MODEL = "llama-3.1-8b-instant"


# ---------- QUERY REWRITING ----------
def rewrite_query(query: str) -> str:
    """
    Rewrite user query to improve semantic retrieval quality.
    Keeps intent intact, removes ambiguity, adds clarity.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You rewrite user questions to optimize semantic search "
                    "over technical and academic documents. "
                    "Preserve intent. Remove fluff. Be precise."
                ),
            },
            {"role": "user", "content": query},
        ],
        temperature=0.15,
        max_tokens=64,
    )

    return response.choices[0].message.content.strip()


# ---------- ANSWER GENERATION ----------
def ask_groq(query: str, context: str, grounded: bool = True) -> str:
    """
    Generate an answer strictly grounded in retrieved context.
    No hallucinations. No external knowledge.
    """
    system_prompt = (
        "You are a document-grounded research assistant.\n"
        "Rules:\n"
        "- Use ONLY the provided context\n"
        "- Do NOT guess or infer beyond the text\n"
        "- If the answer is missing, say you do not know\n"
        "- Be concise, factual, and neutral\n"
    )

    if grounded:
        system_prompt += (
            "- Every factual statement must be supported by the context\n"
        )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Question:\n{query}\n\n"
                    f"Context:\n{context}"
                ),
            },
        ],
        temperature=0.25,
        max_tokens=512,
    )

    return response.choices[0].message.content.strip()
