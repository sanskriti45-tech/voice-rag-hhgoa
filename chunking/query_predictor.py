def predict_queries(partial_query):
    partial = partial_query.lower()

    if "collapse of the" in partial:
        return [
            partial + " roman empire",
            partial + " soviet union",
            partial + " ottoman empire"
        ]

    # add more trigger phrases as you test real queries
    return [partial]