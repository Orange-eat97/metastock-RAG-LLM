"""
RAG retrieval service.

Supabase source tables:

rag_cards
  card_id
  card_type
  card_bucket
  title
  category
  source_path
  body_markdown
  content_hash

rag_card_embeddings
  card_id
  embedding
  embedding_model
  content_hash

Registry / knowledge-graph layer:

rag_card_registry
  canonical_id
  concept_type
  source_path
  title
  card_bucket

rag_card_aliases
  canonical_id
  alias_text
  alias_type
  weight

rag_card_dependencies
  from_canonical_id
  to_canonical_id
  edge_type

Context-builder boundary:
  Context builder does not decompose the query.
  It tells RetrievalPlanner to build a plan, then applies the returned plan.

External contract stays unchanged:
    build_context_for_query(...) -> tuple[str, list[dict[str, Any]]]
"""

from __future__ import annotations

import os
from typing import Any, Iterable, Literal

from dotenv import load_dotenv
from openai import OpenAI
from supabase import Client, create_client

from src.queryDecomposition.retrieval_planner import RetrievalPlanner


load_dotenv()


EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

DEFAULT_TOP_K = 12
DEFAULT_MAX_DYNAMIC_FILES = 5

RETRIEVAL_BACKEND = "supabase"
BASE_CONTEXT_SOURCE = "supabase.rag_cards"
DYNAMIC_CONTEXT_SOURCE = "supabase.rpc.match_rag_cards"
FORCED_CONTEXT_SOURCE = "supabase.registry.resolve_rag_registry_cards"


BASE_CONTEXT_SOURCE_PATHS = [
    "references/price_fields.md",
    "templates/explorer_basic.md",
    "templates/explorer_columns_filter.md",
]

Bucket = Literal["patterns", "functions", "references"]


# ============================================================
# Environment / clients
# ============================================================


def require_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


def make_supabase_client() -> Client:
    return create_client(
        require_env("SUPABASE_URL"),
        require_env("SUPABASE_SERVICE_ROLE_KEY"),
    )


def make_openai_client() -> OpenAI:
    return OpenAI(api_key=require_env("OPENAI_API_KEY"))


def create_query_embedding(openai_client: OpenAI, query: str) -> list[float]:
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )

    return response.data[0].embedding


# ============================================================
# Shared card helpers
# ============================================================


def normalize_filename(name: str) -> str:
    return name.strip().lower().replace("\\", "/")


def get_file_name_from_source_path(source_path: str) -> str:
    normalized = source_path.replace("\\", "/")
    return normalized.split("/")[-1]


def should_exclude_from_dynamic(source_path: str, title: str = "") -> bool:
    """
    Avoid retrieving mandatory base cards again as dynamic context.

    This preserves the previous behavior:
    - base templates are always included manually;
    - templates are not retrieved again dynamically;
    - price_fields is not retrieved again dynamically.
    """
    path = source_path.replace("\\", "/").lower()
    file_name = normalize_filename(get_file_name_from_source_path(path))

    base_names = {
        "price_fields.md",
        "explorer_basic.md",
        "explorer_columns_filter.md",
    }

    if file_name in base_names:
        return True

    if path.startswith("templates/"):
        return True

    if path == "references/price_fields.md":
        return True

    return False


def make_dynamic_item(
    row: dict[str, Any],
    *,
    retrieval_source: str = DYNAMIC_CONTEXT_SOURCE,
    score: float | None = None,
    retrieval_reason: str = "",
) -> dict[str, Any]:
    source_path = row.get("source_path", "")

    return {
        "file_name": get_file_name_from_source_path(source_path),
        "file_path": source_path,
        "card_id": row["card_id"],
        "title": row.get("title", ""),
        "card_type": row.get("card_type", ""),
        "card_bucket": row.get("card_bucket", ""),
        "category": row.get("category"),
        "score": float(score if score is not None else (row.get("similarity") or 0)),
        "text": row.get("body_markdown", ""),
        "retrieval_backend": RETRIEVAL_BACKEND,
        "retrieval_source": retrieval_source,
        "retrieval_reason": retrieval_reason,
    }


# ============================================================
# Base context
# ============================================================


def fetch_cards_by_source_paths(
    supabase: Client,
    source_paths: list[str],
) -> list[dict[str, Any]]:
    response = (
        supabase.table("rag_cards")
        .select(
            "card_id,title,card_type,card_bucket,category,source_path,body_markdown"
        )
        .in_("source_path", source_paths)
        .execute()
    )

    rows = response.data or []

    by_path = {
        row["source_path"]: row
        for row in rows
    }

    ordered_rows: list[dict[str, Any]] = []
    missing_paths: list[str] = []

    for source_path in source_paths:
        row = by_path.get(source_path)

        if row is None:
            missing_paths.append(source_path)
            continue

        ordered_rows.append(row)

    if missing_paths:
        raise RuntimeError(
            "Missing mandatory base context cards in Supabase: "
            + ", ".join(missing_paths)
        )

    return ordered_rows


def load_base_context() -> str:
    """
    Fetch mandatory base context from Supabase instead of local markdown files.
    """
    print(f"[context_builder] Loading base context from {BASE_CONTEXT_SOURCE}")

    supabase = make_supabase_client()

    rows = fetch_cards_by_source_paths(
        supabase=supabase,
        source_paths=BASE_CONTEXT_SOURCE_PATHS,
    )

    parts: list[str] = []

    for row in rows:
        parts.append(
            f"## BASE CONTEXT FILE: {row['source_path']}\n"
            f"Card ID: {row['card_id']}\n"
            f"Title: {row['title']}\n"
            f"Retrieved from: {BASE_CONTEXT_SOURCE}\n\n"
            f"{row['body_markdown']}"
        )

    return "\n\n" + ("=" * 80) + "\n\n".join(parts)


# ============================================================
# Supabase retrieval primitives
# ============================================================


def retrieve_cards_from_supabase(
    supabase: Client,
    query_embedding: list[float],
    top_k: int,
    filter_card_type: str | None = None,
    filter_card_bucket: str | None = None,
) -> list[dict[str, Any]]:
    print(
        "[context_builder] Retrieving dynamic context from "
        f"{DYNAMIC_CONTEXT_SOURCE} | "
        f"top_k={top_k} | "
        f"filter_card_type={filter_card_type} | "
        f"filter_card_bucket={filter_card_bucket}"
    )

    response = supabase.rpc(
        "match_rag_cards",
        {
            "query_embedding": query_embedding,
            "match_count": top_k,
            "filter_card_type": filter_card_type,
            "filter_card_bucket": filter_card_bucket,
        },
    ).execute()

    return response.data or []


def retrieve_unique_dynamic_context(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    max_dynamic_files: int = DEFAULT_MAX_DYNAMIC_FILES,
) -> list[dict[str, Any]]:
    """
    Retrieve many cards from Supabase, then deduplicate by source_path.

    This is the non-planned fallback path.
    """
    supabase = make_supabase_client()
    openai_client = make_openai_client()

    query_embedding = create_query_embedding(openai_client, query)

    rows = retrieve_cards_from_supabase(
        supabase=supabase,
        query_embedding=query_embedding,
        top_k=top_k,
        filter_card_type=None,
        filter_card_bucket=None,
    )

    best_by_file: dict[str, dict[str, Any]] = {}

    for row in rows:
        source_path = row.get("source_path", "")
        title = row.get("title", "")

        if should_exclude_from_dynamic(source_path=source_path, title=title):
            continue

        key = normalize_filename(source_path)
        item = make_dynamic_item(row)
        current = best_by_file.get(key)

        if current is None or item["score"] > current["score"]:
            best_by_file[key] = item

    ranked = sorted(
        best_by_file.values(),
        key=lambda x: x["score"],
        reverse=True,
    )

    return ranked[:max_dynamic_files]


# ============================================================
# Planned dynamic retrieval
# ============================================================


def retrieve_planned_dynamic_context(
    query: str,
    max_dynamic_files: int = DEFAULT_MAX_DYNAMIC_FILES,
    debug_plan: bool = True,
) -> list[dict[str, Any]]:
    """
    Tell-style planned retrieval.

    Context builder tells RetrievalPlanner to build a plan.
    RetrievalPlanner owns decomposition, alias matching, canonical-ID collection,
    and registry dependency resolution.

    This function only applies the returned plan:
    1. force-include registry-resolved cards;
    2. run bucketed vector retrieval using planned subqueries;
    3. deduplicate by source_path;
    4. return forced cards first, then vector results.
    """
    supabase = make_supabase_client()
    openai_client = make_openai_client()

    plan = RetrievalPlanner(supabase=supabase).build_plan(query)

    if debug_plan:
        plan.print_summary()

    bucket_plan = {
        "patterns": {
            "top_k": 4,
            "min_keep": 2,
        },
        "functions": {
            "top_k": 4,
            "min_keep": 3,
        },
        "references": {
            "top_k": 2,
            "min_keep": 0,
        },
    }

    selected: list[dict[str, Any]] = []
    selected_paths: set[str] = set()

    # First: force-include registry-resolved cards.
    if plan.forced_cards:
        print("\n=== Forced Cards Matched From Supabase Registry ===")

    for card in plan.forced_cards:
        item = make_dynamic_item(
            card.to_rag_card_row(),
            retrieval_source=FORCED_CONTEXT_SOURCE,
            score=1.0,
            retrieval_reason=(
                f"forced_by_registry_plan; canonical_id={card.canonical_id}; "
                f"depth={card.depth}"
            ),
        )

        path = normalize_filename(item["file_path"])
        if path in selected_paths:
            continue

        print(f"- {item['title']} | {item['file_path']} | {card.canonical_id}")
        selected.append(item)
        selected_paths.add(path)

    if plan.missing_seed_canonical_ids:
        print("\n=== Registry Seed IDs Missing/Unresolved ===")
        for canonical_id in plan.missing_seed_canonical_ids:
            print(f"- {canonical_id}")

    # If forced cards already fill the allowed dynamic slots, stop here.
    # This prevents vector retrieval from displacing required cards.
    if len(selected) >= max_dynamic_files:
        return selected[:max_dynamic_files]

    # Second: retrieve using planned subqueries by bucket.
    bucket_results: dict[str, list[dict[str, Any]]] = {
        bucket: []
        for bucket in bucket_plan
    }

    best_by_file: dict[str, dict[str, Any]] = {}

    for bucket, plan_config in bucket_plan.items():
        queries = plan.retrieval_queries_by_bucket.get(bucket, [])

        if not queries:
            continue

        for subquery in queries:
            query_embedding = create_query_embedding(openai_client, subquery)

            rows = retrieve_cards_from_supabase(
                supabase=supabase,
                query_embedding=query_embedding,
                top_k=plan_config["top_k"],
                filter_card_type=None,
                filter_card_bucket=bucket,
            )

            for row in rows:
                source_path = row.get("source_path", "")
                title = row.get("title", "")

                if should_exclude_from_dynamic(source_path=source_path, title=title):
                    continue

                key = normalize_filename(source_path)

                if key in selected_paths:
                    continue

                item = make_dynamic_item(
                    row,
                    retrieval_source=DYNAMIC_CONTEXT_SOURCE,
                    retrieval_reason=f"bucket={bucket}; subquery={subquery}",
                )

                current = best_by_file.get(key)

                if current is None or item["score"] > current["score"]:
                    best_by_file[key] = item

    for item in best_by_file.values():
        bucket = item.get("card_bucket", "")

        if bucket in bucket_results:
            bucket_results[bucket].append(item)

    for bucket in bucket_results:
        bucket_results[bucket].sort(
            key=lambda x: x["score"],
            reverse=True,
        )

    # Third: keep a minimum from each bucket, without displacing forced cards.
    for bucket, plan_config in bucket_plan.items():
        for item in bucket_results[bucket][: plan_config["min_keep"]]:
            if len(selected) >= max_dynamic_files:
                break

            path = normalize_filename(item["file_path"])

            if path in selected_paths:
                continue

            selected.append(item)
            selected_paths.add(path)

    # Fourth: fill remaining slots by global vector score.
    remaining: list[dict[str, Any]] = []

    for items in bucket_results.values():
        for item in items:
            path = normalize_filename(item["file_path"])

            if path not in selected_paths:
                remaining.append(item)

    remaining.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    for item in remaining:
        if len(selected) >= max_dynamic_files:
            break

        path = normalize_filename(item["file_path"])

        if path in selected_paths:
            continue

        selected.append(item)
        selected_paths.add(path)

    return selected[:max_dynamic_files]


def retrieve_tiered_dynamic_context(
    query: str,
    max_dynamic_files: int = DEFAULT_MAX_DYNAMIC_FILES,
) -> list[dict[str, Any]]:
    """
    Backward-compatible public function name.

    The old implementation retrieved the same query once per bucket. The new
    implementation keeps tiered retrieval but routes planning through
    RetrievalPlanner, so required cards can be resolved through the registry
    before vector results are added.
    """
    return retrieve_planned_dynamic_context(
        query=query,
        max_dynamic_files=max_dynamic_files,
        debug_plan=True,
    )


# ============================================================
# Context formatting / public API
# ============================================================


def format_dynamic_context(items: Iterable[dict[str, Any]]) -> str:
    parts: list[str] = []

    for i, item in enumerate(items, start=1):
        parts.append(
            f"## RETRIEVED CONTEXT {i}: {item['file_name']}\n"
            f"Card ID: {item['card_id']}\n"
            f"Title: {item['title']}\n"
            f"Source path: {item['file_path']}\n"
            f"Card bucket: {item['card_bucket']}\n"
            f"Retrieval backend: {item.get('retrieval_backend', 'unknown')}\n"
            f"Retrieval source: {item.get('retrieval_source', 'unknown')}\n"
            f"Retrieval reason: {item.get('retrieval_reason', '')}\n"
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
    use_tiered_dynamic: bool = True,
) -> tuple[str, list[dict[str, Any]]]:
    """
    Returns:
      final_context: base context + dynamic retrieved context
      dynamic_items: retrieved unique files, useful for logging/debugging

    This function keeps the old external contract used by generate_explorer.py.
    """
    base_context = load_base_context()

    if use_tiered_dynamic:
        dynamic_items = retrieve_tiered_dynamic_context(
            query=query,
            max_dynamic_files=max_dynamic_files,
        )
    else:
        dynamic_items = retrieve_unique_dynamic_context(
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
