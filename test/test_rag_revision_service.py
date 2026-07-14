from __future__ import annotations

from src.rag_revision_service import RagExplorerRevisionService


def test_revision_prompt_requires_minimal_change() -> None:
    service = RagExplorerRevisionService()
    prompt = service._build_revision_prompt(
        original_query=(
            "RSI below 30 and close above SMA50"
        ),
        context="RSI and Mov syntax",
        existing_explorer={
            "explorer_name": "RSI and SMA",
            "explorer_description": "test",
            "explorer_code_body": (
                "ColB < 30 AND ColA > ColC"
            ),
            "col_definitions": [
                {"col_letter": "A", "col_code": "C"},
                {
                    "col_letter": "B",
                    "col_code": "RSI(14)",
                },
                {
                    "col_letter": "C",
                    "col_code": "Mov(C,50,S)",
                },
            ],
        },
        revision_instruction="Use 25 instead of 30.",
    )

    assert "Preserve every condition" in prompt
    assert "ColB < 30 AND ColA > ColC" in prompt
    assert "RSI(14) < 25" in prompt
    assert "Do not simplify the strategy" in prompt


def test_revision_user_query_contains_lineage() -> None:
    service = RagExplorerRevisionService()
    query = service._build_revision_user_query(
        original_explorer_id="explorer-1",
        original_query="original request",
        revision_instruction="change threshold",
    )

    assert "[revision_of:explorer-1]" in query
    assert "original request" in query
    assert "change threshold" in query
