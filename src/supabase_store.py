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
    validation_errors: list[str] | None = None,
    retrieved_refs: list[dict[str, Any]] | None = None,
    repaired_from_explorer_id: str | None = None,
    repair_instruction: str | None = None,
) -> str:
    
    """
    Insert one generated Explorer object into Supabase.

    Returns:
        explorer_outputs.id
    """
    validation_errors = validation_errors or []
    retrieved_refs = retrieved_refs or []

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

    if not isinstance(retrieved_refs, list):
        raise ValueError("Cannot save to Supabase: retrieved_refs must be a list.")

    repaired_from_explorer_id = (
        str(repaired_from_explorer_id).strip()
        if repaired_from_explorer_id
        else None
    )
    repair_instruction = (
        str(repair_instruction).strip()
        if repair_instruction and str(repair_instruction).strip()
        else None
    )

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

        "retrieved_refs": retrieved_refs,
        "repaired_from_explorer_id": repaired_from_explorer_id,
        "repair_instruction": repair_instruction,

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


def update_explorer_service_log_id(
    *,
    explorer_id: str,
    service_log_id: str,
) -> None:
    """Attach the creation/repair RAG log to an existing Explorer row."""
    cleaned_explorer_id = str(explorer_id or "").strip()
    cleaned_service_log_id = str(service_log_id or "").strip()

    if not cleaned_explorer_id:
        raise ValueError("explorer_id is required.")

    if not cleaned_service_log_id:
        raise ValueError("service_log_id is required.")

    client = _get_supabase_client()

    response = (
        client
        .table(TABLE_NAME)
        .update({"service_log_id": cleaned_service_log_id})
        .eq("id", cleaned_explorer_id)
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "Supabase update did not return an explorer_outputs row for "
            f"id={cleaned_explorer_id}"
        )


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
            "full_output_json, validation_passed, validation_errors, "
            "retrieved_refs, service_log_id, repaired_from_explorer_id, "
            "repair_instruction"
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