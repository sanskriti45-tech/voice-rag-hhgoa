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