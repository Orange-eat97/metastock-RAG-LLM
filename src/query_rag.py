import chromadb
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


load_dotenv()

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "metastock_primer"


def load_index() -> VectorStoreIndex:
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)

    return index


def main() -> None:
    print("[query_rag] Loading index...")
    index = load_index()

    retriever = index.as_retriever(similarity_top_k=5)

    print("[query_rag] Ready. Type 'exit' to quit.")

    while True:
        query = input("\nUser query: ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        if not query:
            continue

        nodes = retriever.retrieve(query)

        print("\n=== Retrieved Context ===")

        for i, node in enumerate(nodes, start=1):
            file_name = node.metadata.get("file_name", "unknown")
            file_path = node.metadata.get("file_path", "unknown")

            print(f"\n--- Result {i} ---")
            print(f"Score: {node.score}")
            print(f"File: {file_name}")
            print(f"Path: {file_path}")
            print("-" * 60)
            print(node.text[:1200])


if __name__ == "__main__":
    main()