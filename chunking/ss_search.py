from concurrent.futures import ThreadPoolExecutor


def speculative_search(predictions, retrieve_function):

    with ThreadPoolExecutor(
        max_workers=len(predictions)
    ) as executor:

        futures = {
            executor.submit(retrieve_function, query): query
            for query in predictions
        }

        results = {}

        for future, query in [
            (future, query)
            for future, query in futures.items()
        ]:
            results[query] = future.result()

    return results


def choose_prediction(final_query, predictions):

    final_words = set(final_query.lower().split())

    best_prediction = None
    best_score = 0

    for prediction in predictions:

        prediction_words = set(prediction.lower().split())

        intersection = final_words & prediction_words

        score = len(intersection) / len(final_words)

        if score > best_score:
            best_score = score
            best_prediction = prediction

    return best_prediction, best_score
