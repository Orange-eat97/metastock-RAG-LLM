from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()


TABLE_NAME = "explorer_outputs"


def _get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url:
        raise RuntimeError("Missing SUPABASE_URL in .env")

    if not key:
        raise RuntimeError("Missing SUPABASE_SERVICE_ROLE_KEY in .env")

    return create_client(url, key)


def save_explorer_output_to_supabase(
    *,
    output: dict[str, Any],
    user_query: str,
    backend: str,
    model: str,
    validation_errors: list[str],
) -> str:
    """
    Insert one generated Explorer object into Supabase.

    Returns:
        explorer_outputs.id
    """
    explorer_name = str(output.get("explorer_name", "")).strip()
    explorer_description = str(output.get("explorer_description", "")).strip()
    explorer_code_body = str(output.get("explorer_code_body", "")).strip()
    col_definitions = output.get("col_definitions", [])

    if not explorer_name:
        raise ValueError("Cannot save to Supabase: explorer_name is empty.")

    if not explorer_code_body:
        raise ValueError("Cannot save to Supabase: explorer_code_body is empty.")

    if not isinstance(col_definitions, list):
        raise ValueError("Cannot save to Supabase: col_definitions must be a list.")

    validation_passed = len(validation_errors) == 0

    row = {
        "backend": backend,
        "model": model,
        "user_query": user_query,

        "explorer_name": explorer_name,
        "explorer_description": explorer_description,
        "explorer_code_body": explorer_code_body,

        "col_definitions": col_definitions,
        "full_output_json": output,

        "validation_passed": validation_passed,
        "validation_errors": validation_errors,

        "status": "generated",
    }

    client = _get_supabase_client()

    response = (
        client
        .table(TABLE_NAME)
        .insert(row)
        .execute()
    )

    if not response.data:
        raise RuntimeError(f"Supabase insert returned no data: {response}")

    inserted = response.data[0]
    explorer_id = inserted.get("id")

    if not explorer_id:
        raise RuntimeError(f"Supabase insert did not return id: {inserted}")

    return explorer_id


def find_cached_explorer_output_by_query(
    *,
    user_query: str,
    require_validation_passed: bool = True,
    model: str | None = None,
) -> dict[str, Any] | None:
    """
    Find the newest stored Explorer output for the exact same user_query.

    Returns:
        {
            "id": "...",
            "created_at": "...",
            "full_output_json": {...},
            "validation_passed": True,
            ...
        }

    or None if no cache hit.

    Exact match is intentional for now. This avoids accidentally reusing a
    strategy for a query that only looks similar but means something different.
    """
    query = (user_query or "").strip()

    if not query:
        return None

    client = _get_supabase_client()

    request = (
        client
        .table(TABLE_NAME)
        .select(
            "id, created_at, backend, model, user_query, "
            "full_output_json, validation_passed, validation_errors"
        )
        .eq("user_query", query)
        .order("created_at", desc=True)
        .limit(1)
    )

    if require_validation_passed:
        request = request.eq("validation_passed", True)

    if model:
        request = request.eq("model", model)

    response = request.execute()

    if not response.data:
        return None

    row = response.data[0]

    full_output = row.get("full_output_json")

    if not isinstance(full_output, dict):
        raise ValueError(
            f"Cached row {row.get('id')} has invalid full_output_json: {full_output!r}"
        )

    return row