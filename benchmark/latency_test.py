import time
import numpy as np
from app import process_voice_query

TEST_QUERIES = [
    (["who was the"], "who was the first president of india"),
    (["collapse of the"], "what caused the collapse of the roman empire"),
    (["what is the"], "what is the capital of india"),
    (["how does"], "how does photosynthesis work"),
    (["when did"], "when did world war two end"),
]


def run_benchmark(n_repeats=20):
    latencies = []

    for i in range(n_repeats):
        partials, final_query = TEST_QUERIES[i % len(TEST_QUERIES)]
        start = time.perf_counter()
        try:
            process_voice_query(partials, final_query)
        except Exception as e:
            print(f"[query failed] {final_query}: {e}")
            continue
        elapsed_ms = (time.perf_counter() - start) * 1000
        latencies.append(elapsed_ms)

    latencies = np.array(latencies)
    p50 = np.percentile(latencies, 50)
    p70 = np.percentile(latencies, 70)
    p100 = np.percentile(latencies, 100)

    print(f"\nRan {len(latencies)} queries")
    print(f"P50:  {p50:.2f} ms")
    print(f"P70:  {p70:.2f} ms")
    print(f"P100: {p100:.2f} ms")

    return {"p50": p50, "p70": p70, "p100": p100, "raw": latencies.tolist()}


if __name__ == "__main__":
    run_benchmark(n_repeats=30)