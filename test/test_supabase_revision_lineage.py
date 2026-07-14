from __future__ import annotations

import pytest

from src import supabase_store


class Response:
    def __init__(self, data):
        self.data = data


class Table:
    def __init__(self):
        self.row = None

    def insert(self, row):
        self.row = row
        return self

    def execute(self):
        return Response(
            [
                {
                    "id": "revised-1",
                }
            ]
        )


class Client:
    def __init__(self):
        self.table_instance = Table()

    def table(self, name):
        assert name == "explorer_outputs"
        return self.table_instance


def output():
    return {
        "explorer_name": "Revised Explorer",
        "explorer_description": "description",
        "explorer_code_body": "RSI(14) < 25",
        "col_definitions": [],
    }


def test_saves_revision_lineage(monkeypatch) -> None:
    client = Client()
    monkeypatch.setattr(
        supabase_store,
        "_get_supabase_client",
        lambda: client,
    )

    explorer_id = (
        supabase_store
        .save_explorer_output_to_supabase(
            output=output(),
            user_query="revision request",
            backend="openai_revision",
            model="test-model",
            revised_from_explorer_id=(
                "original-1"
            ),
            revision_instruction=(
                "Use 25 instead of 30."
            ),
        )
    )

    assert explorer_id == "revised-1"
    assert client.table_instance.row[
        "revised_from_explorer_id"
    ] == "original-1"
    assert client.table_instance.row[
        "revision_instruction"
    ] == "Use 25 instead of 30."
    assert client.table_instance.row[
        "repaired_from_explorer_id"
    ] is None


def test_rejects_repair_and_revision_lineage_together(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        supabase_store,
        "_get_supabase_client",
        lambda: Client(),
    )

    with pytest.raises(
        ValueError,
        match="both a repair and a revision",
    ):
        (
            supabase_store
            .save_explorer_output_to_supabase(
                output=output(),
                user_query="invalid",
                backend="test",
                model="test",
                repaired_from_explorer_id=(
                    "repair-source"
                ),
                revised_from_explorer_id=(
                    "revision-source"
                ),
            )
        )
