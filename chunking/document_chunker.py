import re

def fixed_size_chunk(text, chunk_size=200, overlap=50):
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
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    chunks = []
    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i + max_sentences])
        if chunk:
            chunks.append(chunk)
    return chunks


def metadata_aware_chunk(text, metadata, strategy="fixed", **kwargs):
    if strategy == "fixed":
        raw_chunks = fixed_size_chunk(text, **kwargs)
    else:
        raw_chunks = semantic_chunk(text, **kwargs)

    return [
        {"text": chunk, "metadata": {**metadata, "chunk_index": i}}
        for i, chunk in enumerate(raw_chunks)
    ]
def choose_strategy(text):
    word_count = len(text.split())
    sentence_count = len(re.split(r'(?<=[.!?]) +', text.strip()))

    if word_count <= 40:
        return "none"
    if sentence_count >= 3:
        return "semantic"
    return "fixed"
def chunk_passage(text, metadata):
    strategy = choose_strategy(text)

    if strategy == "none":
        return [{"text": text, "metadata": {**metadata, "chunk_index": 0, "strategy": "none"}}]

    if strategy == "semantic":
        return metadata_aware_chunk(
            text, {**metadata, "strategy": "semantic"},
            strategy="semantic", max_sentences=3,
        )

    return metadata_aware_chunk(
        text, {**metadata, "strategy": "fixed"},
        strategy="fixed", chunk_size=100, overlap=25,
    )