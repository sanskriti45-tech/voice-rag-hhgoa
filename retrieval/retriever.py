from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
client = QdrantClient(":memory:")  # swap to a real host/URL for production

COLLECTION_NAME = "video_rag_chunks"

def init_collection(vector_size=384):
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )

def index_chunks(chunks):
    """chunks: list of {'text': ..., 'metadata': {...}}"""
    vectors = model.encode([c["text"] for c in chunks])
    points = [
        PointStruct(id=i, vector=vectors[i].tolist(), payload=chunks[i])
        for i in range(len(chunks))
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)

def dense_search(query, top_k=5):
    query_vector = model.encode(query).tolist()
    results = client.search(collection_name=COLLECTION_NAME, query_vector=query_vector, limit=top_k)
    return results