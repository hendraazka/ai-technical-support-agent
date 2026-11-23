
from app.rag.loader import load_documents
from app.rag.chunker import split_documents
from app.rag.vector_store import index_documents


def main():
    print("Loading knowledge base...")
    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    print("Splitting documents...")
    chunks = split_documents(documents)

    print(f"Chunks generated: {len(chunks)}")

    print("Creating embeddings and indexing into ChromaDB...")
    indexed = index_documents(chunks)

    print(f"Successfully indexed: {indexed} chunks")


if __name__ == "__main__":
    main()

