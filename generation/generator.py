import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"
MAX_RETRIES = 2
RETRY_BACKOFF_MS = 50
MAX_CONTEXT_CHUNKS = 5


def build_context(retrieved_results, max_chunks=MAX_CONTEXT_CHUNKS):
    """retrieved_results: list of (text, score) tuples from hybrid_search."""
    top_chunks = retrieved_results[:max_chunks]
    context = "\n\n".join(f"[{i+1}] {text}" for i, (text, score) in enumerate(top_chunks))
    return context


def build_prompt(query, context):
    return f"""You are a factual assistant. Answer the question using ONLY the context below.
If the answer is not contained in the context, say "I don't have enough information to answer that."
Do not use outside knowledge. Cite the passage number(s) you used, e.g. [1], [2].

Context:
{context}

Question: {query}

Answer:"""


def generate_answer(query, retrieved_results):
    context = build_context(retrieved_results)
    prompt = build_prompt(query, context)

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You answer strictly from provided context."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=300,
            )
            answer_text = response.choices[0].message.content.strip()
            return {
                "answer": answer_text,
                "context_used": context,
                "success": True,
                "attempts": attempt,
            }
        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                time.sleep((RETRY_BACKOFF_MS * attempt) / 1000)  # milliseconds, not seconds
    return {
        "answer": None,
        "context_used": context,
        "success": False,
        "error": str(last_error),
        "attempts": MAX_RETRIES,
    }


if __name__ == "__main__":
    from retrieval.hybrid_retrieval import get_dense_results, get_bm25_results, hybrid_search

    query = "What is the capital of India?"
    dense_results = get_dense_results(query, top_k=50)
    bm25_results = get_bm25_results(query, top_k=50)
    retrieved = hybrid_search(query, dense_results, bm25_results, alpha=0.5)

    result = generate_answer(query, retrieved)

    print(f"\nQuery: {query}")
    print(f"Success: {result['success']}")
    print(f"Answer: {result['answer']}")