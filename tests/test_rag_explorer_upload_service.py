from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.rag_explorer_upload_service import (
    ExplorerDuplicateNameError,
    ExplorerUploadValidationError,
    RagExplorerUploadService,
)


def test_invalid_upload_is_rejected_before_insert() -> None:
    service = object.__new__(RagExplorerUploadService)
    service._make_supabase_client = MagicMock()

    with pytest.raises(ExplorerUploadValidationError):
        service.upload_explorer(
            {
                "explorer_name": "Broken",
                "explorer_code_body": "ColB = 1",
                "col_definitions": [
                    {
                        "col_letter": "A",
                        "col_code": "RSI(14)",
                    }
                ],
            }
        )

    service._make_supabase_client.assert_not_called()


def test_duplicate_name_comparison_is_case_insensitive() -> None:
    service = object.__new__(RagExplorerUploadService)
    client = MagicMock()
    (
        client.table.return_value
        .select.return_value
        .range.return_value
        .execute.return_value
    ).data = [
        {
            "id": "existing",
            "full_output_json": {
                "explorer_name": "Manual RSI Explorer"
            },
        }
    ]
    service._make_supabase_client = MagicMock(
        return_value=client
    )

    with pytest.raises(ExplorerDuplicateNameError):
        service._ensure_unique_name(
            "manual rsi explorer"
        )
