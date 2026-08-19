import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from rank_bm25 import BM25Okapi

from chunking.document_chunker import chunk_passage

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LANGUAGE = "hi"
COLLECTION = "rag_passages"

_index_state = {"built": False}
embed_model = None
client = None
bm25 = None
all_chunks = None


def _ensure_index_built():
    global embed_model, client, bm25, all_chunks
    if _index_state["built"]:
        return

    df = pd.read_pickle("data/msmarco_slice.pkl")
    passage_field = "English_passages" if LANGUAGE == "en" else "Translated_passages"

    chunks = []
    for idx, row in df.iterrows():
        passages = row["passages"][passage_field]
        for p_idx, passage_text in enumerate(passages):
            base_metadata = {
                "query_id": row.get("query_id", idx),
                "passage_index": p_idx,
                "is_selected": row["passages"]["is_selected"][p_idx],
                "language": LANGUAGE,
            }
            chunks.extend(chunk_passage(passage_text, base_metadata))

    all_chunks = chunks
    corpus = [c["text"] for c in all_chunks]
    print(f"Total chunks in corpus: {len(corpus)}  (from {len(df)} queries, field={passage_field})")

    embed_model_name = "all-MiniLM-L6-v2" if LANGUAGE == "en" else "paraphrase-multilingual-MiniLM-L12-v2"
    embed_model = SentenceTransformer(embed_model_name)
    embeddings = embed_model.encode(corpus, show_progress_bar=True, batch_size=64)

    client = QdrantClient(":memory:")
    if client.collection_exists(COLLECTION):
        client.delete_collection(COLLECTION)
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=embeddings.shape[1], distance=Distance.COSINE),
    )
    points = [
        PointStruct(id=i, vector=embeddings[i].tolist(), payload=all_chunks[i])
        for i in range(len(corpus))
    ]
    client.upsert(collection_name=COLLECTION, points=points)
    print("Dense index built in Qdrant.")

    tokenized_corpus = [doc.lower().split() for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    print("BM25 index built.")

    _index_state["built"] = True
def get_dense_results(query, top_k=50):
    _ensure_index_built()
    try:
        query_vec = embed_model.encode(query).tolist()
        hits = client.query_points(collection_name=COLLECTION, query=query_vec, limit=top_k).points
        return hits
    except Exception as e:
        print(f"[dense retrieval error] {e}")
        return []


def get_bm25_results(query, top_k=50):
    _ensure_index_built()
    try:
        tokenized_query = query.lower().split()
        scores = bm25.get_scores(tokenized_query)
        top_ids = np.argsort(scores)[::-1][:top_k]
        return [(all_chunks[i], float(scores[i])) for i in top_ids]
    except Exception as e:
        print(f"[bm25 retrieval error] {e}")
        return []


def hybrid_search(query, dense_results, bm25_results, alpha=0.5):
    scores = {}
    for rank, r in enumerate(dense_results):
        scores[r.payload["text"]] = scores.get(r.payload["text"], 0) + alpha * (1 / (rank + 1))
    for rank, (chunk, _) in enumerate(bm25_results):
        scores[chunk["text"]] = scores.get(chunk["text"], 0) + (1 - alpha) * (1 / (rank + 1))
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked


if __name__ == "__main__":
    query = "कॉर्पोरेशन क्या है?"

    dense_results = get_dense_results(query, top_k=50)
    bm25_results = get_bm25_results(query, top_k=50)

    results = hybrid_search(query, dense_results, bm25_results, alpha=0.5)

    print(f"\nQuery: {query}\n")
    for rank, (text, score) in enumerate(results[:5], start=1):
        print(f"{rank}. [score={score:.4f}]")
        print(f"   {text[:150]}...\n")