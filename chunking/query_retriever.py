from retrieval.hybrid_retrieval import hybrid_search


def retrieve_query(query: str, top_k: int = 5):
    """
    Retrieve the most relevant chunks for a user query.

    Args:
        query: The user's text query.
        top_k: Number of results to retrieve.

    Returns:
        A list of retrieved results from hybrid_search().
    """

    if not isinstance(query, str):
        raise TypeError("query must be a string")

    query = query.strip()

    if not query:
        return []

    results = hybrid_search(
        query=query,
        top_k=top_k
    )

    return results


if __name__ == "__main__":
    query = input("Enter your query: ")

    results = retrieve_query(query, top_k=5)

    print("\nRetrieved results:")

    for i, result in enumerate(results, start=1):
        print(f"\n--- Result {i} ---")

        if isinstance(result, dict):
            print(result.get("text", result))
        else:
            print(result)
