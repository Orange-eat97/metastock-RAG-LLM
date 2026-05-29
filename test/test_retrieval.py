import sys
from dataclasses import dataclass
from typing import List

import chromadb
from llama_index.core import Settings, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "metastock_primer"
SIMILARITY_TOP_K = 5


@dataclass
class RetrievalTestCase:
    name: str
    query: str
    expected_files: List[str]


def load_index() -> VectorStoreIndex:
    print("[test_retrieval] Loading embedding model...")

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    print("[test_retrieval] Connecting to ChromaDB...")

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)

    return index


def normalize_filename(name: str) -> str:
    return name.strip().lower().replace("\\", "/")


def run_test_case(retriever, test_case: RetrievalTestCase) -> bool:
    print("\n" + "=" * 80)
    print(f"TEST: {test_case.name}")
    print(f"QUERY: {test_case.query}")
    print("-" * 80)

    nodes = retriever.retrieve(test_case.query)

    retrieved_files = []

    print("Retrieved files:")

    for i, node in enumerate(nodes, start=1):
        file_name = node.metadata.get("file_name", "unknown")
        retrieved_files.append(normalize_filename(file_name))
        print(f"  {i}. {file_name}  | score={node.score:.4f}")

    expected = [normalize_filename(f) for f in test_case.expected_files]

    missing = [
        file_name
        for file_name in expected
        if file_name not in retrieved_files
    ]

    if missing:
        print("\n[FAILED]")
        print(f"Missing expected file(s) in top {SIMILARITY_TOP_K}: {missing}")
        return False

    print("\n[PASSED]")
    return True


def main() -> None:
    test_cases = [
        RetrievalTestCase(
            name="RSI oversold",
            query="Find stocks where RSI is below 30",
            expected_files=["rsi.md"],
        ),
        RetrievalTestCase(
            name="Close above 50 day moving average",
            query="Find stocks where close is above 50 day moving average",
            expected_files=["mov.md", "price_fields.md"],
        ),
        RetrievalTestCase(
            name="Volume above average volume",
            query="Find stocks where volume is above 20 day average volume",
            expected_files=["volume_above_average.md", "mov.md", "price_fields.md"],
        ),
        RetrievalTestCase(
            name="20 day high breakout",
            query="Find stocks making a 20 day high",
            expected_files=["hhv.md", "breakout.md"],
        ),
        RetrievalTestCase(
            name="Fast MA crosses above slow MA",
            query="Find stocks where fast moving average crosses above slow moving average",
            expected_files=["cross.md", "mov.md"],
        ),
    ]

    index = load_index()
    retriever = index.as_retriever(similarity_top_k=SIMILARITY_TOP_K)

    passed = 0
    failed = 0

    for test_case in test_cases:
        ok = run_test_case(retriever, test_case)

        if ok:
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()