import re

def fixed_size_chunk(text, chunk_size=200, overlap=50):
    """Splits text into fixed-size word chunks with overlap."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def semantic_chunk(text, max_sentences=5):
    """Splits text by sentence boundaries, grouping N sentences per chunk."""
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    chunks = []
    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i + max_sentences])
        if chunk:
            chunks.append(chunk)
    return chunks


def metadata_aware_chunk(text, metadata, strategy="fixed", **kwargs):
    """Wraps chunks with metadata (query_id, language, source) for filtering at retrieval time."""
    if strategy == "fixed":
        raw_chunks = fixed_size_chunk(text, **kwargs)
    else:
        raw_chunks = semantic_chunk(text, **kwargs)

    return [
        {"text": chunk, "metadata": {**metadata, "chunk_index": i}}
        for i, chunk in enumerate(raw_chunks)
    ]