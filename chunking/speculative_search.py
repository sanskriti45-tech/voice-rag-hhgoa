from concurrent.futures import ThreadPoolExecutor

def speculative_search(predictions, retrieve_function):
    with ThreadPoolExecutor(max_workers=len(predictions)) as executor:
        futures = {
            executor.submit(retrieve_function, query): query
            for query in predictions
        }
        results = {}
        for future, query in [(f, q) for f, q in futures.items()]:
            results[query] = future.result()
    return results