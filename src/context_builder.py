from __future__ import annotations

from pathlib import Path
from typing import Iterable

import chromadb
from llama_index.core import Settings, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "metastock_primer"

KNOWLEDGE_DIR = Path("knowledge_base")

BASE_CONTEXT_FILES = [
    KNOWLEDGE_DIR / "references" / "price_fields.md",
    KNOWLEDGE_DIR / "templates" / "explorer_basic.md",
    KNOWLEDGE_DIR / "templates" / "explorer_columns_filter.md",
]

DEFAULT_TOP_K = 8
DEFAULT_MAX_DYNAMIC_FILES = 3


def load_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Base context file not found: {path}")

    return path.read_text(encoding="utf-8")


def load_base_context() -> str:
    parts = []

    for path in BASE_CONTEXT_FILES:
        text = load_text_file(path)
        parts.append(
            f"## BASE CONTEXT FILE: {path.as_posix()}\n\n{text}"
        )

    return "\n\n" + ("=" * 80) + "\n\n".join(parts)


def load_index() -> VectorStoreIndex:
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    return VectorStoreIndex.from_vector_store(vector_store)


def normalize_filename(name: str) -> str:
    return name.strip().lower().replace("\\", "/")


def should_exclude_from_dynamic(file_path: str, file_name: str) -> bool:
    """
    Avoid retrieving mandatory base cards again as dynamic context.
    They are already included manually.
    """
    path = file_path.replace("\\", "/").lower()
    name = normalize_filename(file_name)

    base_names = {
        "price_fields.md",
        "explorer_basic.md",
        "explorer_columns_filter.md",
    }

    if name in base_names:
        return True

    if "/templates/" in path:
        return True

    if "/reference/price_fields.md" in path:
        return True

    return False


def retrieve_unique_dynamic_context(
    index: VectorStoreIndex,
    query: str,
    top_k: int = DEFAULT_TOP_K,
    max_dynamic_files: int = DEFAULT_MAX_DYNAMIC_FILES,
) -> list[dict]:
    """
    Retrieve many chunks, then deduplicate by file name.

    This prevents one file, e.g. rsi.md, from occupying 3 to 5 slots.
    """
    retriever = index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(query)

    best_by_file: dict[str, dict] = {}

    for node in nodes:
        file_name = node.metadata.get("file_name", "unknown")
        file_path = node.metadata.get("file_path", "")

        if should_exclude_from_dynamic(file_path, file_name):
            continue

        key = normalize_filename(file_name)

        current = best_by_file.get(key)

        item = {
            "file_name": file_name,
            "file_path": file_path,
            "score": float(node.score or 0),
            "text": node.text,
        }

        if current is None or item["score"] > current["score"]:
            best_by_file[key] = item

    ranked = sorted(
        best_by_file.values(),
        key=lambda x: x["score"],
        reverse=True,
    )

    return ranked[:max_dynamic_files]


def format_dynamic_context(items: Iterable[dict]) -> str:
    parts = []

    for i, item in enumerate(items, start=1):
        parts.append(
            f"## RETRIEVED CONTEXT {i}: {item['file_name']}\n"
            f"Source path: {item['file_path']}\n"
            f"Retrieval score: {item['score']:.4f}\n\n"
            f"{item['text']}"
        )

    if not parts:
        return "## RETRIEVED CONTEXT\n\nNo dynamic context retrieved."

    return "\n\n" + ("=" * 80) + "\n\n".join(parts)


def build_context_for_query(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    max_dynamic_files: int = DEFAULT_MAX_DYNAMIC_FILES,
) -> tuple[str, list[dict]]:
    """
    Returns:
      final_context: base context + dynamic retrieved context
      dynamic_items: retrieved unique files, useful for logging/debugging
    """
    index = load_index()

    base_context = load_base_context()

    dynamic_items = retrieve_unique_dynamic_context(
        index=index,
        query=query,
        top_k=top_k,
        max_dynamic_files=max_dynamic_files,
    )

    dynamic_context = format_dynamic_context(dynamic_items)

    final_context = (
        "# Mandatory Base Context\n"
        f"{base_context}\n\n"
        "# Dynamic Retrieved Context\n"
        f"{dynamic_context}"
    )

    return final_context, dynamic_items