import os
from dotenv import load_dotenv

# 🔑 Load environment FIRST, before any other imports
load_dotenv()

from fastapi import FastAPI
from app.crawler import crawl
from app.cleaner import clean_text
from app.embedder import embed
from app.vectordb import VectorDB
from app.rag import generate_answer

app = FastAPI()
db = VectorDB(1536)

@app.post("/crawl")
def crawl_site(url: str):
    raw = crawl(url)
    clean = clean_text(raw)

    chunks = [clean[i:i+500] for i in range(0, len(clean), 500)]
    vectors = [e.embedding for e in embed(chunks)]

    db.add(vectors, chunks)
    return {"status": "Crawled and indexed", "chunks": len(chunks)}

@app.get("/ask")
def ask(q: str):
    q_vec = embed([q])[0].embedding
    results = db.search(q_vec)
    answer = generate_answer(q, results)
    return {"answer": answer}
