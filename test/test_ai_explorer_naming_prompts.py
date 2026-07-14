from __future__ import annotations

from src.generate_explorer import build_prompt
from src.rag_revision_service import (
    RagExplorerRevisionService,
)


def test_generation_prompt_requires_ai_prefix_without_version() -> None:
    prompt = build_prompt(
        user_query="Find RSI below 30.",
        context="context",
    )

    assert "AI_<generated explorer name>" in prompt
    assert "do not append a version number" in prompt
    assert '"explorer_name": "AI_RSI Below 30"' in prompt


def test_revision_prompt_requires_incremented_version() -> None:
    service = object.__new__(
        RagExplorerRevisionService
    )

    prompt = service._build_revision_prompt(
        original_query="Find RSI below 30.",
        context="context",
        existing_explorer={
            "explorer_name": "AI_RSI Below 30_2",
            "explorer_description": "test",
            "explorer_code_body": "RSI(14) < 30",
            "col_definitions": [],
        },
        revision_instruction="Use 25 instead of 30.",
    )

    assert (
        "AI_<original generated explorer name>_"
        "<version number>"
    ) in prompt
    assert (
        "`AI_RSI Below 30_2` revised again becomes"
        in prompt
    )
    assert "`AI_RSI Below 30_3`" in prompt
