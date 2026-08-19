import time
from chunking.query_state import QueryState
from chunking.query_predictor import predict_queries
from chunking.query_selector import choose_prediction
from chunking.latency_admin import decide_action
from generation.speculative_generator import speculative_generate
from generation.generator import generate_answer
from retrieval.hybrid_retrieval import get_dense_results, get_bm25_results, hybrid_search
from guardrails.guardrails import apply_guardrails


def process_voice_query(partial_transcripts, final_query):
    start = time.perf_counter()
    state = QueryState()
    speculative_results = {}

    for partial in partial_transcripts:
        state.update(partial)
        predictions = predict_queries(state.partial_query)
        state.set_predictions(predictions)
        speculative_results.update(speculative_generate(predictions))

    state.set_speculative_results(speculative_results)
    state.set_final_query(final_query)

    prediction, score = choose_prediction(final_query, list(speculative_results.keys()) or [final_query])
    elapsed_ms = (time.perf_counter() - start) * 1000

    action = decide_action(confidence=score, elapsed_ms=elapsed_ms, budget_ms=50)

    if action == "ANSWER" and prediction in speculative_results:
        result = speculative_results[prediction]
        result["source"] = "speculative_cache"

    elif action == "ANSWER_BEST_AVAILABLE" and speculative_results:
        best_query = max(speculative_results, key=lambda q: speculative_results[q].get("success", False))
        result = speculative_results[best_query]
        result["source"] = "best_available_fallback"

    else:
        dense_results = get_dense_results(final_query, top_k=50)
        bm25_results = get_bm25_results(final_query, top_k=50)
        retrieved = hybrid_search(final_query, dense_results, bm25_results, alpha=0.5)
        result = generate_answer(final_query, retrieved)
        result["source"] = "live_search"
        result["retrieved"] = retrieved  # so the line below is consistent across all 3 branches

    result["action_taken"] = action
    result["elapsed_ms"] = elapsed_ms

    guard_check = apply_guardrails(final_query, result.get("retrieved", []), result)
    result["final_answer"] = guard_check["final_answer"]
    result["guardrail_passed"] = guard_check["allowed"]
    result["guardrail_reason"] = guard_check["reason"]

    return result


if __name__ == "__main__":
    partials = ["who was the", "who was the collapse of the"]
    final = "what caused the collapse of the roman empire"
    result = process_voice_query(partials, final)
    print(result)