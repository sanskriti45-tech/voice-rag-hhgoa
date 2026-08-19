import time

from retrieval.hybrid_retrieval import hybrid_search
from chunking.query_state import predict_queries
from chunking.ss_search import ss_search
from chunking.latency_admin import decide_action


def choose_prediction(
    final_query: str,
    predictions: list[str]
):
    if not predictions:
        return None

    final_words = set(
        final_query.lower().split()
    )

    best_prediction = None
    best_score = 0.0

    for prediction in predictions:

        prediction_words = set(
            prediction.lower().split()
        )

        if not final_words:
            continue

        intersection = final_words & prediction_words

        score = len(intersection) / len(final_words)

        if score > best_score:
            best_score = score
            best_prediction = prediction

    return best_prediction


def calculate_confidence(results):

    if not results:
        return 0.0

    if isinstance(results, dict):
        return 0.0

    first = results[0]

    return first.get("score", 0.0)


def chrono_rag(final_query: str, state):

    start = time.perf_counter()

    state.final_query = final_query

    prediction = choose_prediction(
        final_query,
        state.predictions
    )

    # Reuse speculative results
    if prediction in state.speculative_results:

        candidates = state.speculative_results[prediction]

    else:

        candidates = hybrid_search(
            final_query
        )

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    confidence = calculate_confidence(
        candidates
    )

    action = decide_action(
        confidence,
        elapsed_ms
    )

    if action == "REFINE":

        candidates = hybrid_search(
            final_query
        )

    elif action == "DEEP_SEARCH":

        candidates = hybrid_search(
            final_query,
            deep=True
        )

    return {
        "query": final_query,
        "results": candidates,
        "confidence": confidence,
        "action": action,
        "latency_ms": (
            time.perf_counter() - start
        ) * 1000
    }