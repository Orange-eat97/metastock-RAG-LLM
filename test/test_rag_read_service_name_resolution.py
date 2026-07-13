from __future__ import annotations

import sys
import types

import pytest


fake_supabase = types.ModuleType("supabase")
fake_supabase.Client = object
fake_supabase.create_client = lambda url, key: None
sys.modules["supabase"] = fake_supabase

from src.rag_read_service import (
    EXPLORER_NAME_LOOKUP_PAGE_SIZE,
    ExplorerNameAmbiguousError,
    ExplorerNotFoundError,
    RagExplorerReadService,
)


class FakeResponse:
    def __init__(self, data):
        self.data = data


class FakeTable:
    def __init__(self, rows):
        self.rows = rows
        self.start = 0
        self.end = len(rows) - 1
        self.selected = None
        self.ordered_by = None

    def select(self, columns):
        self.selected = columns
        return self

    def order(self, column):
        self.ordered_by = column
        return self

    def range(self, start, end):
        self.start = start
        self.end = end
        return self

    def execute(self):
        return FakeResponse(
            self.rows[self.start : self.end + 1]
        )


class FakeClient:
    def __init__(self, rows):
        self.rows = rows
        self.table_names = []

    def table(self, name):
        self.table_names.append(name)
        return FakeTable(self.rows)


def make_row(
    explorer_id: str,
    explorer_name: str,
) -> dict:
    return {
        "id": explorer_id,
        "full_output_json": {
            "explorer_name": explorer_name,
        },
    }


def test_exact_unique_match_returns_uuid() -> None:
    client = FakeClient(
        [
            make_row("id-1", "RSI Scanner"),
            make_row("id-2", "Breakout Scanner"),
        ]
    )
    service = RagExplorerReadService(client=client)

    assert (
        service.resolve_explorer_id_by_name(
            "RSI Scanner"
        )
        == "id-1"
    )


def test_matching_is_trimmed_and_case_insensitive() -> None:
    service = RagExplorerReadService(
        client=FakeClient(
            [
                make_row(
                    "id-1",
                    "  RSI Scanner  ",
                )
            ]
        )
    )

    assert (
        service.resolve_explorer_id_by_name(
            "  rsi scanner "
        )
        == "id-1"
    )


def test_unknown_name_raises_not_found() -> None:
    service = RagExplorerReadService(
        client=FakeClient(
            [make_row("id-1", "RSI Scanner")]
        )
    )

    with pytest.raises(ExplorerNotFoundError):
        service.resolve_explorer_id_by_name(
            "MACD Scanner"
        )


def test_duplicate_exact_names_raise_ambiguous() -> None:
    service = RagExplorerReadService(
        client=FakeClient(
            [
                make_row("id-1", "RSI Scanner"),
                make_row("id-2", "rsi scanner"),
            ]
        )
    )

    with pytest.raises(
        ExplorerNameAmbiguousError
    ):
        service.resolve_explorer_id_by_name(
            "RSI Scanner"
        )


def test_partial_match_is_rejected() -> None:
    service = RagExplorerReadService(
        client=FakeClient(
            [make_row("id-1", "RSI Scanner")]
        )
    )

    with pytest.raises(ExplorerNotFoundError):
        service.resolve_explorer_id_by_name("RSI")


def test_lookup_paginates_past_first_page() -> None:
    rows = [
        make_row(
            f"id-{index}",
            f"Explorer {index}",
        )
        for index in range(
            EXPLORER_NAME_LOOKUP_PAGE_SIZE
        )
    ]
    rows.append(
        make_row(
            "target-id",
            "Target Explorer",
        )
    )

    service = RagExplorerReadService(
        client=FakeClient(rows)
    )

    assert (
        service.resolve_explorer_id_by_name(
            "Target Explorer"
        )
        == "target-id"
    )