
import os
from dotenv import load_dotenv
from openai import OpenAI
from app.embedder import embed

# Load .env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(query, chunks):
    context = "\n".join(chunks)

    prompt = f"""
Answer ONLY using the context below.
If answer is not in context, say "I don't know."

Context:
{context}

Question:
{query}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output[0].content[0].text
