def decide_action(
    confidence,
    elapsed_ms,
    budget_ms=50
):

    remaining = budget_ms - elapsed_ms

    if confidence >= 0.90:
        return "ANSWER"

    if remaining <= 5:
        return "ANSWER_BEST_AVAILABLE"

    if confidence >= 0.70:
        return "REFINE"

    return "DEEP_SEARCH"
