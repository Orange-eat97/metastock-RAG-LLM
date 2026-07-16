from __future__ import annotations

import os

from dotenv import load_dotenv
from supabase import Client, create_client

from src.query_identity import (
    DEFAULT_QUERY_EMBEDDING_MODEL,
    build_query_identity,
)


PAGE_SIZE = 100


def get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv(
        "SUPABASE_SERVICE_ROLE_KEY"
    )

    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL and "
            "SUPABASE_SERVICE_ROLE_KEY "
            "are required."
        )

    return create_client(
        url,
        key,
    )


def main() -> None:
    load_dotenv()

    client = get_client()
    start = 0
    updated = 0

    while True:
        end = (
            start
            + PAGE_SIZE
            - 1
        )

        response = (
            client
            .table("explorer_outputs")
            .select(
                "id, user_query, "
                "validation_passed, "
                "revised_from_explorer_id"
            )
            .order("created_at")
            .range(start, end)
            .execute()
        )

        rows = response.data or []

        if not rows:
            break

        for row in rows:
            explorer_id = str(
                row.get("id")
                or ""
            ).strip()

            user_query = str(
                row.get("user_query")
                or ""
            ).strip()

            if (
                not explorer_id
                or not user_query
            ):
                continue

            include_embedding = (
                bool(
                    row.get(
                        "validation_passed"
                    )
                )
                and not row.get(
                    "revised_from_explorer_id"
                )
            )

            identity = (
                build_query_identity(
                    user_query,
                    include_embedding=(
                        include_embedding
                    ),
                    embedding_model=(
                        DEFAULT_QUERY_EMBEDDING_MODEL
                    ),
                )
            )

            payload = {
                "user_query_normalized": (
                    identity.normalized
                ),
                "user_query_hash": (
                    identity.query_hash
                ),
                "user_query_embedding": (
                    identity.embedding
                ),
                "user_query_embedding_model": (
                    identity.embedding_model
                ),
            }

            (
                client
                .table(
                    "explorer_outputs"
                )
                .update(payload)
                .eq("id", explorer_id)
                .execute()
            )

            updated += 1

            print(
                "[query-cache-backfill] "
                f"updated={explorer_id} "
                f"embedded="
                f"{include_embedding}"
            )

        if len(rows) < PAGE_SIZE:
            break

        start += PAGE_SIZE

    print(
        "[query-cache-backfill] "
        f"complete rows_updated={updated}"
    )


if __name__ == "__main__":
    main()