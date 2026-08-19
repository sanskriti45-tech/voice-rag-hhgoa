from concurrent.futures import ThreadPoolExecutor
from generation.generator import generate_answer
from retrieval.hybrid_retrieval import get_dense_results, get_bm25_results, hybrid_search


def _generate_for_query(query, top_k=20):
    dense_results = get_dense_results(query, top_k=top_k)
    bm25_results = get_bm25_results(query, top_k=top_k)
    retrieved = hybrid_search(query, dense_results, bm25_results, alpha=0.5)
    result = generate_answer(query, retrieved)
    result["query"] = query
    result["retrieved"] = retrieved  # kept so guardrails can check it later, not just live-search results
    return result


def speculative_generate(predictions):
    """Runs retrieval+generation in parallel for each predicted query."""
    with ThreadPoolExecutor(max_workers=len(predictions)) as executor:
        futures = {executor.submit(_generate_for_query, q): q for q in predictions}
        results = {}
        for future, query in futures.items():
            try:
                results[query] = future.result()
            except Exception as e:
                results[query] = {"answer": None, "success": False, "error": str(e), "query": query, "retrieved": []}
    return results