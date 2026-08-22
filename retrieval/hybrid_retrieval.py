import os
import pickle
import numpy as np
import pandas as pd
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from rank_bm25 import BM25Okapi

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DEFAULT_CHUNK_SIZE = 200
DEFAULT_CHUNK_OVERLAP = 30
DEFAULT_MIN_CHUNK_WORDS = 20

# Persistent index directory
INDEX_DIR = "data/rag_index"
EMBEDDINGS_FILE = os.path.join(INDEX_DIR, "embeddings.npy")
CHUNKS_FILE = os.path.join(INDEX_DIR, "chunks.pkl")
BM25_FILE = os.path.join(INDEX_DIR, "bm25.pkl")

LANGUAGE = "hi"
COLLECTION = "rag_passages"

_index_state = {"built": False}

embed_model = None
client = None
bm25 = None
all_chunks = None


def chunk_passage(
    passage_text,
    metadata=None,
    chunk_size=DEFAULT_CHUNK_SIZE,
    overlap=DEFAULT_CHUNK_OVERLAP,
    min_chunk_words=DEFAULT_MIN_CHUNK_WORDS,
):
    if passage_text is None:
        return []

    text = str(passage_text).strip()

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap must be >= 0")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()

    if len(words) <= chunk_size:
        payload = dict(metadata or {})
        payload["text"] = text
        return [payload]

    step = chunk_size - overlap

    if step <= 0:
        step = 1

    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words).strip()

        if not chunk_text:
            break

        if len(chunk_words) < min_chunk_words and start != 0:
            if chunks:
                chunks[-1]["text"] = (
                    chunks[-1]["text"] + " " + chunk_text
                ).strip()
            break

        payload = dict(metadata or {})
        payload["text"] = chunk_text
        chunks.append(payload)

        if end == len(words):
            break

        start += step

    if not chunks:
        payload = dict(metadata or {})
        payload["text"] = text
        return [payload]

    return chunks


def _build_chunks_from_dataset():
    """Build chunks from the original dataset."""

    df = pd.read_pickle("data/msmarco_slice.pkl")

    passage_field = (
        "English_passages"
        if LANGUAGE == "en"
        else "Translated_passages"
    )

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

            chunks.extend(
                chunk_passage(
                    passage_text,
                    base_metadata
                )
            )

    return chunks


def _build_index_from_scratch():
    """Build the persistent index for the first time."""

    global embed_model
    global client
    global bm25
    global all_chunks

    print("\n==========================================")
    print("BUILDING RAG INDEX FOR THE FIRST TIME")
    print("==========================================\n")

    os.makedirs(INDEX_DIR, exist_ok=True)

    # -----------------------------------------
    # 1. Build chunks
    # -----------------------------------------

    all_chunks = _build_chunks_from_dataset()

    corpus = [
        chunk["text"]
        for chunk in all_chunks
    ]

    print(
        f"Total chunks in corpus: {len(corpus)}"
    )

    # -----------------------------------------
    # 2. Load embedding model
    # -----------------------------------------

    if LANGUAGE == "en":
        embed_model_name = "all-MiniLM-L6-v2"
    else:
        embed_model_name = (
            "paraphrase-multilingual-MiniLM-L12-v2"
        )

    print(
        f"Loading embedding model: {embed_model_name}"
    )

    embed_model = SentenceTransformer(
        embed_model_name
    )

    # -----------------------------------------
    # 3. Generate embeddings ONCE
    # -----------------------------------------

    print("\nGenerating embeddings...")

    embeddings = embed_model.encode(
        corpus,
        show_progress_bar=True,
        batch_size=64
    )

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )

    np.save(
        EMBEDDINGS_FILE,
        embeddings
    )

    print(
        f"Saved embeddings to: {EMBEDDINGS_FILE}"
    )

    # -----------------------------------------
    # 4. Save chunks
    # -----------------------------------------

    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(
            all_chunks,
            f,
            protocol=pickle.HIGHEST_PROTOCOL
        )

    print(
        f"Saved chunks to: {CHUNKS_FILE}"
    )

    # -----------------------------------------
    # 5. Build BM25
    # -----------------------------------------

    tokenized_corpus = [
        doc.lower().split()
        for doc in corpus
    ]

    bm25 = BM25Okapi(
        tokenized_corpus
    )

    with open(BM25_FILE, "wb") as f:
        pickle.dump(
            bm25,
            f,
            protocol=pickle.HIGHEST_PROTOCOL
        )

    print(
        f"Saved BM25 index to: {BM25_FILE}"
    )

    # -----------------------------------------
    # 6. Build Qdrant
    # -----------------------------------------

    client = QdrantClient(":memory:")

    if client.collection_exists(COLLECTION):
        client.delete_collection(COLLECTION)

    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(
            size=embeddings.shape[1],
            distance=Distance.COSINE,
        ),
    )

    points = [
        PointStruct(
            id=i,
            vector=embeddings[i].tolist(),
            payload=all_chunks[i],
        )
        for i in range(len(corpus))
    ]

    client.upsert(
        collection_name=COLLECTION,
        points=points,
    )

    print("Dense index built in Qdrant.")

    print("\n==========================================")
    print("RAG INDEX BUILD COMPLETE")
    print("==========================================\n")


def _load_persistent_index():
    """Load previously saved chunks, embeddings and BM25."""

    global embed_model
    global client
    global bm25
    global all_chunks

    print("\n==========================================")
    print("LOADING EXISTING RAG INDEX")
    print("==========================================\n")

    # -----------------------------------------
    # 1. Load chunks
    # -----------------------------------------

    with open(CHUNKS_FILE, "rb") as f:
        all_chunks = pickle.load(f)

    print(
        f"Loaded {len(all_chunks)} chunks."
    )

    # -----------------------------------------
    # 2. Load embeddings
    # -----------------------------------------

    embeddings = np.load(
        EMBEDDINGS_FILE
    )

    print(
        f"Loaded embeddings: {embeddings.shape}"
    )

    # -----------------------------------------
    # 3. Load BM25
    # -----------------------------------------

    with open(BM25_FILE, "rb") as f:
        bm25 = pickle.load(f)

    print("Loaded BM25 index.")

    # -----------------------------------------
    # 4. Load embedding model
    # -----------------------------------------

    if LANGUAGE == "en":
        embed_model_name = "all-MiniLM-L6-v2"
    else:
        embed_model_name = (
            "paraphrase-multilingual-MiniLM-L12-v2"
        )

    embed_model = SentenceTransformer(
        embed_model_name
    )

    # -----------------------------------------
    # 5. Rebuild Qdrant collection in memory
    # -----------------------------------------

    # The expensive embeddings are NOT regenerated.
    # We only load the saved vectors.

    client = QdrantClient(":memory:")

    if client.collection_exists(COLLECTION):
        client.delete_collection(COLLECTION)

    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(
            size=embeddings.shape[1],
            distance=Distance.COSINE,
        ),
    )

    points = [
        PointStruct(
            id=i,
            vector=embeddings[i].tolist(),
            payload=all_chunks[i],
        )
        for i in range(len(all_chunks))
    ]

    client.upsert(
        collection_name=COLLECTION,
        points=points,
    )

    print("Dense index restored in Qdrant.")

    print("\n==========================================")
    print("RAG INDEX LOADED")
    print("==========================================\n")


def _ensure_index_built():

    global _index_state

    if _index_state["built"]:
        return

    # -----------------------------------------
    # Check whether persistent files exist
    # -----------------------------------------

    index_exists = (
        os.path.exists(EMBEDDINGS_FILE)
        and os.path.exists(CHUNKS_FILE)
        and os.path.exists(BM25_FILE)
    )

    if index_exists:

        print(
            "[INDEX] Existing persistent index found."
        )

        _load_persistent_index()

    else:

        print(
            "[INDEX] No persistent index found."
        )

        _build_index_from_scratch()

    _index_state["built"] = True


def get_dense_results(query, top_k=50):

    _ensure_index_built()

    try:

        query_vec = embed_model.encode(
            query
        ).tolist()

        hits = client.query_points(
            collection_name=COLLECTION,
            query=query_vec,
            limit=top_k,
        ).points

        return hits

    except Exception as e:

        print(
            f"[dense retrieval error] {e}"
        )

        return []


def get_bm25_results(query, top_k=50):

    _ensure_index_built()

    try:

        tokenized_query = (
            query.lower().split()
        )

        scores = bm25.get_scores(
            tokenized_query
        )

        top_ids = np.argsort(scores)[::-1][
            :top_k
        ]

        return [
            (
                all_chunks[i],
                float(scores[i])
            )
            for i in top_ids
        ]

    except Exception as e:

        print(
            f"[bm25 retrieval error] {e}"
        )

        return []


def hybrid_search(
    query,
    dense_results=None,
    bm25_results=None,
    alpha=0.5,
):

    if (
        dense_results is None
        or bm25_results is None
    ):

        dense_results = get_dense_results(
            query,
            top_k=50
        )

        bm25_results = get_bm25_results(
            query,
            top_k=50
        )

    scores = {}

    # -----------------------------------------
    # Dense ranking
    # -----------------------------------------

    for rank, r in enumerate(
        dense_results or []
    ):

        text = (
            r.payload["text"]
            if hasattr(r, "payload")
            else r.get("text")
        )

        if text is None:
            continue

        scores[text] = (
            scores.get(text, 0)
            + alpha * (1 / (rank + 1))
        )

    # -----------------------------------------
    # BM25 ranking
    # -----------------------------------------

    for rank, item in enumerate(
        bm25_results or []
    ):

        if (
            isinstance(item, tuple)
            and len(item) == 2
        ):

            chunk, _ = item

            text = (
                chunk["text"]
                if isinstance(chunk, dict)
                else str(chunk)
            )

        elif isinstance(item, dict):

            text = item.get("text")

        else:

            continue

        if text is None:
            continue

        scores[text] = (
            scores.get(text, 0)
            + (1 - alpha)
            * (1 / (rank + 1))
        )

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked


if __name__ == "__main__":

    query = "कॉर्पोरेशन क्या है?"

    dense_results = get_dense_results(
        query,
        top_k=50
    )

    bm25_results = get_bm25_results(
        query,
        top_k=50
    )

    results = hybrid_search(
        query,
        dense_results,
        bm25_results,
        alpha=0.5
    )

    print(
        f"\nQuery: {query}\n"
    )

    for rank, (text, score) in enumerate(
        results[:5],
        start=1
    ):

        print(
            f"{rank}. [score={score:.4f}]"
        )

        print(
            f"   {text[:150]}...\n"
        )