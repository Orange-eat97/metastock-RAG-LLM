from __future__ import annotations

from typing import Any

import pytest

from src.rag_result_store_service import (
    FULL_RESULT_SELECT,
    RESULT_SUMMARY_SELECT,
    RagExplorerResultStoreService,
)


class FakeResponse:
    def __init__(
        self,
        data: list[dict[str, Any]],
    ) -> None:
        self.data = data


class FakeTable:
    def __init__(
        self,
        rows: list[dict[str, Any]],
    ) -> None:
        self._rows = list(rows)
        self.selected: str | None = None
        self.filters: list[
            tuple[str, Any]
        ] = []
        self.order_field: str | None = None
        self.order_desc = False
        self.limit_value: int | None = None

    def select(
        self,
        columns: str,
    ) -> FakeTable:
        self.selected = columns
        return self

    def eq(
        self,
        field: str,
        value: Any,
    ) -> FakeTable:
        self.filters.append(
            (field, value)
        )
        return self

    def order(
        self,
        field: str,
        *,
        desc: bool = False,
    ) -> FakeTable:
        self.order_field = field
        self.order_desc = desc
        return self

    def limit(
        self,
        value: int,
    ) -> FakeTable:
        self.limit_value = value
        return self

    def execute(self) -> FakeResponse:
        rows = list(self._rows)

        for field, value in self.filters:
            rows = [
                row
                for row in rows
                if row.get(field) == value
            ]

        if self.order_field is not None:
            rows.sort(
                key=lambda row: (
                    row.get(
                        self.order_field
                    )
                    or ""
                ),
                reverse=self.order_desc,
            )

        if self.limit_value is not None:
            rows = rows[
                : self.limit_value
            ]

        return FakeResponse(rows)


class FakeClient:
    def __init__(
        self,
        rows: list[dict[str, Any]],
    ) -> None:
        self.rows = rows
        self.queries: list[FakeTable] = []

    def table(
        self,
        name: str,
    ) -> FakeTable:
        assert name == "explorer_result_sets"

        query = FakeTable(self.rows)
        self.queries.append(query)
        return query


def build_row(
    *,
    result_id: str,
    created_at: str,
    explorer_id: str = "explorer-1",
) -> dict[str, Any]:
    return {
        "id": result_id,
        "explorer_id": explorer_id,
        "created_at": created_at,
        "schema_version": "1.0",
        "outcome": "matches_found",
        "expected_count": 1,
        "matched_count": 1,
        "has_matches": True,
        "clipboard_verified": True,
        "clipboard_verification": {
            "passed": True,
            "expected_count": 1,
            "scraped_count": 1,
            "clipboard_count": 1,
            "missing_from_scrape": [],
            "unexpected_in_scrape": [],
            "clipboard_headers": [
                "Instrument",
                "A",
            ],
        },
        "rows": [
            {
                "row_index": 0,
                "instrument_name": (
                    "Test Instrument"
                ),
                "symbol": "TEST.SI",
                "column_values": {
                    "A": "1.0",
                },
            }
        ],
        "capture_started_at": "start",
        "capture_finished_at": "finish",
        "diagnostics": {
            "source": "fake",
        },
    }


def test_get_result_returns_full_artifact() -> None:
    client = FakeClient(
        [
            build_row(
                result_id="result-1",
                created_at=(
                    "2026-07-13T01:00:00+00:00"
                ),
            )
        ]
    )
    service = RagExplorerResultStoreService(
        client=client
    )

    result = service.get_result(
        "result-1"
    )

    assert result["result_id"] == "result-1"
    assert result["schema_version"] == "1.0"
    assert (
        result["rows"][0]["symbol"]
        == "TEST.SI"
    )
    assert result["diagnostics"] == {
        "source": "fake"
    }
    assert (
        client.queries[-1].selected
        == FULL_RESULT_SELECT
    )


def test_get_result_unknown_id_fails() -> None:
    service = RagExplorerResultStoreService(
        client=FakeClient([])
    )

    with pytest.raises(
        ValueError,
        match="No explorer_result_sets row",
    ):
        service.get_result("missing")


def test_get_latest_result_returns_newest() -> None:
    client = FakeClient(
        [
            build_row(
                result_id="result-old",
                created_at=(
                    "2026-07-12T01:00:00+00:00"
                ),
            ),
            build_row(
                result_id="result-new",
                created_at=(
                    "2026-07-13T01:00:00+00:00"
                ),
            ),
        ]
    )
    service = RagExplorerResultStoreService(
        client=client
    )

    result = service.get_latest_result(
        "explorer-1"
    )

    assert result is not None
    assert (
        result["result_id"]
        == "result-new"
    )


def test_get_latest_result_returns_none() -> None:
    service = RagExplorerResultStoreService(
        client=FakeClient([])
    )

    assert (
        service.get_latest_result(
            "explorer-1"
        )
        is None
    )


def test_list_results_returns_summaries() -> None:
    client = FakeClient(
        [
            build_row(
                result_id="result-old",
                created_at=(
                    "2026-07-12T01:00:00+00:00"
                ),
            ),
            build_row(
                result_id="result-new",
                created_at=(
                    "2026-07-13T01:00:00+00:00"
                ),
            ),
            build_row(
                result_id="other",
                explorer_id="explorer-2",
                created_at=(
                    "2026-07-14T01:00:00+00:00"
                ),
            ),
        ]
    )
    service = RagExplorerResultStoreService(
        client=client
    )

    results = service.list_results(
        "explorer-1",
        limit=2,
    )

    assert [
        item["result_id"]
        for item in results
    ] == [
        "result-new",
        "result-old",
    ]

    assert "rows" not in results[0]
    assert "diagnostics" not in results[0]

    assert (
        client.queries[-1].selected
        == RESULT_SUMMARY_SELECT
    )


@pytest.mark.parametrize(
    "invalid_limit",
    [
        0,
        -1,
        101,
    ],
)
def test_list_results_rejects_invalid_limit(
    invalid_limit: int,
) -> None:
    service = RagExplorerResultStoreService(
        client=FakeClient([])
    )

    with pytest.raises(ValueError):
        service.list_results(
            "explorer-1",
            limit=invalid_limit,
        )