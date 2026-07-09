from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from supabase import Client, create_client


load_dotenv()


class RagExplorerReadService:
    """
    Controlled read-only service for stored RAG artifacts.

    This service is intentionally narrow:
    - read one explorer_outputs row by id;
    - read one rag_service_logs row by log_id;
    - no arbitrary table access;
    - no write operations;
    - no Supabase URL/key returned to callers.
    """

    def __init__(self) -> None:
        self.client = self._make_supabase_client()

    def get_explorer(self, explorer: str) -> dict[str, Any]:
        explorer_id = self._clean_required_text(explorer, "explorer")

        response = (
            self.client.table("explorer_outputs")
            .select(
                "id, created_at, backend, model, user_query, "
                "full_output_json, validation_passed, validation_errors"
            )
            .eq("id", explorer_id)
            .limit(1)
            .execute()
        )

        if not response.data:
            raise ValueError(f"No explorer_outputs row found for id={explorer_id}")

        return self._flatten_explorer_row(response.data[0])

    def get_service_log(self, log_id: str) -> dict[str, Any]:
        cleaned_log_id = self._clean_required_text(log_id, "log_id")

        response = (
            self.client.table("rag_service_logs")
            .select(
                "log_id, event_type, service_name, user_query, "
                "explorer_output_id, explorer_output_created_at, "
                "stdout_text, stderr_text, metadata, created_at"
            )
            .eq("log_id", cleaned_log_id)
            .limit(1)
            .execute()
        )

        if not response.data:
            raise ValueError(f"No rag_service_logs row found for log_id={cleaned_log_id}")

        return response.data[0]

    def _make_supabase_client(self) -> Client:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        if not url:
            raise RuntimeError("Missing SUPABASE_URL in RAG service environment.")

        if not key:
            raise RuntimeError("Missing SUPABASE_SERVICE_ROLE_KEY in RAG service environment.")

        return create_client(url, key)

    def _flatten_explorer_row(self, row: dict[str, Any]) -> dict[str, Any]:
        """
        explorer_outputs stores the generated Explorer JSON in full_output_json.

        The agent/tool layer expects convenient top-level fields, so this returns
        both:
        - original row fields;
        - flattened explorer_name / explorer_description / explorer_code_body /
          col_definitions.
        """
        full_output = row.get("full_output_json")

        if not isinstance(full_output, dict):
            full_output = {}

        flattened = dict(row)

        flattened["explorer_name"] = str(full_output.get("explorer_name") or "")
        flattened["explorer_description"] = str(
            full_output.get("explorer_description") or ""
        )
        flattened["explorer_code_body"] = str(
            full_output.get("explorer_code_body") or ""
        )

        col_definitions = full_output.get("col_definitions")
        if isinstance(col_definitions, list):
            flattened["col_definitions"] = col_definitions
        else:
            flattened["col_definitions"] = []

        return flattened

    def _clean_required_text(self, value: str, field_name: str) -> str:
        cleaned = str(value or "").strip()

        if not cleaned:
            raise ValueError(f"{field_name} is required.")

        return cleaned