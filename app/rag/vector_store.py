
import hashlib
from pathlib import Path

import chromadb

from app.rag.embeddings import embed_documents, embed_query


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma"
COLLECTION_NAME = "technical_support_kb"


def get_collection():
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def index_documents(chunks):
    if not chunks:
        print("No document chunks to index.")
        return 0

    collection = get_collection()

    texts = [chunk.page_content for chunk in chunks]
    embeddings = embed_documents(texts)

    ids = []
    metadatas = []

    for chunk in chunks:
        source = chunk.metadata.get("source", "unknown")
        page = chunk.metadata.get("page", 0)

        content_hash = hashlib.sha256(
            chunk.page_content.encode("utf-8")
        ).hexdigest()

        document_id = hashlib.sha256(
            f"{source}:{page}:{content_hash}".encode("utf-8")
        ).hexdigest()

        ids.append(document_id)
        metadatas.append(chunk.metadata)

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(ids)


def search_documents(query: str, limit: int = 3):
    collection = get_collection()

    if collection.count() == 0:
        return []

    results = collection.query(
        query_embeddings=[embed_query(query)],
        n_results=min(limit, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    matches = []

    for index, document in enumerate(results["documents"][0]):
        matches.append({
            "content": document,
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index],
        })

    return matches

