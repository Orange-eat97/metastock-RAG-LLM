from __future__ import annotations

from uuid import UUID

from src.rag_system_test_service import (
    ConvertExplorerToSystemTestInput,
    FIXED_PROFIT_TARGET_EXIT,
    RagSystemTestConversionService,
)


def test_system_test_uses_derived_name_and_fixed_exit() -> None:
    service = RagSystemTestConversionService()
    service._fetch_explorer_output = lambda _explorer_id: {
        "created_at": "2026-01-01T00:00:00Z",
        "user_query": "RSI below 30",
        "validation_passed": True,
        "full_output_json": {
            "explorer_name": "RSI Explorer",
            "explorer_description": "",
            "explorer_code_body": "ColA < 30",
            "col_definitions": [
                {
                    "col_letter": "A",
                    "col_code": "RSI(14)",
                }
            ],
        },
    }
    service._load_system_test_context = lambda: ("context", [])
    service._save_system_test = lambda **_kwargs: {
        "created_at": "2026-01-01T00:00:01Z"
    }
    service._save_rag_service_log = lambda **_kwargs: {
        "log_id": "00000000-0000-4000-8000-000000000003",
        "created_at": "2026-01-01T00:00:02Z",
    }
    service._attach_service_log = lambda **_kwargs: None

    response = service.convert_explorer_to_system_test(
        ConvertExplorerToSystemTestInput(
            source_explorer_id=UUID(
                "00000000-0000-4000-8000-000000000002"
            )
        )
    )

    assert response.system_test.name == (
        "AI - RSI Explorer - System Test"
    )
    assert response.system_test.orders.sell.signal_formula == (
        FIXED_PROFIT_TARGET_EXIT
    )
    assert response.validation.passed is True
