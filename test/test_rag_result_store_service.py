from __future__ import annotations

from src.rag_result_store_service import (
    RagExplorerResultStoreService,
)


class FakeResponse:
    def __init__(self, data):
        self.data = data


class FakeTable:
    def __init__(self):
        self.inserted = None

    def insert(self, row):
        self.inserted = row
        return self

    def execute(self):
        return FakeResponse(
            [
                {
                    "id": "result-1",
                    "explorer_id": (
                        self.inserted[
                            "explorer_id"
                        ]
                    ),
                    "created_at": "created",
                }
            ]
        )


class FakeClient:
    def __init__(self):
        self.table_name = None
        self.table_instance = FakeTable()

    def table(self, name):
        self.table_name = name
        return self.table_instance


def test_store_service_inserts_verified_result() -> None:
    client = FakeClient()
    service = (
        RagExplorerResultStoreService(
            client=client
        )
    )

    stored = service.save_explorer_results(
        explorer_id="explorer-1",
        schema_version="1.0",
        outcome="matches_found",
        expected_count=1,
        matched_count=1,
        has_matches=True,
        clipboard_verification={
            "passed": True,
            "expected_count": 1,
            "scraped_count": 1,
            "clipboard_count": 1,
        },
        rows=[
            {
                "row_index": 0,
                "instrument_name": (
                    "Test Instrument"
                ),
                "symbol": "TEST.SI",
                "column_values": {
                    "A": "1.0"
                },
            }
        ],
        diagnostics={},
    )

    assert (
        client.table_name
        == "explorer_result_sets"
    )
    assert stored["result_id"] == "result-1"
    assert (
        client.table_instance
        .inserted["clipboard_verified"]
        is True
    )


def test_store_service_accepts_zero_matches() -> None:
    client = FakeClient()
    service = (
        RagExplorerResultStoreService(
            client=client
        )
    )

    stored = service.save_explorer_results(
        explorer_id="explorer-1",
        schema_version="1.0",
        outcome="no_matches",
        expected_count=0,
        matched_count=0,
        has_matches=False,
        clipboard_verification=None,
        rows=[],
        diagnostics={},
    )

    assert stored["result_id"] == "result-1"
    assert (
        client.table_instance
        .inserted["clipboard_verified"]
        is None
    )
