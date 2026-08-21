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
    context = "\n\n".join(
        f"[{i+1}] {text}"
        for i, (text, score) in enumerate(top_chunks)
    )
    return context


def get_language_name(language):
    """Convert language code into a readable language name."""
    return {
        "hi-IN": "Hindi",
        "en-US": "English",
        "en-IN": "English",
    }.get(language, "the same language as the question")


def build_prompt(query, context, language="hi-IN"):
    language_name = get_language_name(language)

    return f"""You are a factual assistant. Answer the question using ONLY the context below.

LANGUAGE RULE:
- The user asked the question in {language_name}.
- Answer entirely in {language_name}.
- Do not switch to another language unless the user explicitly asks you to.
- Keep technical terms in their commonly used form when appropriate.

GROUNDING RULE:
- If the answer is not contained in the context, say the equivalent of "I don't have enough information to answer that" in {language_name}.
- Do not use outside knowledge.
- Cite the passage number(s) you used, e.g. [1], [2].

Context:
{context}

Question: {query}

Answer:"""


def generate_answer(query, retrieved_results, language="hi-IN"):
    language_name = get_language_name(language)

    context = build_context(retrieved_results)
    prompt = build_prompt(query, context, language)

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You answer strictly from the provided context. "
                            f"Answer in {language_name}."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
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
                time.sleep(
                    (RETRY_BACKOFF_MS * attempt) / 1000
                )

    return {
        "answer": None,
        "context_used": context,
        "success": False,
        "error": str(last_error),
        "attempts": MAX_RETRIES,
    }


if __name__ == "__main__":
    from retrieval.hybrid_retrieval import (
        get_dense_results,
        get_bm25_results,
        hybrid_search,
    )

    query = "What is the capital of India?"

    language = "en-IN"

    dense_results = get_dense_results(
        query,
        top_k=50
    )

    bm25_results = get_bm25_results(
        query,
        top_k=50
    )

    retrieved = hybrid_search(
        query,
        dense_results,
        bm25_results,
        alpha=0.5
    )

    result = generate_answer(
        query,
        retrieved,
        language=language
    )

    print(f"\nQuery: {query}")
    print(f"Language: {language}")
    print(f"Success: {result['success']}")
    print(f"Answer: {result['answer']}")