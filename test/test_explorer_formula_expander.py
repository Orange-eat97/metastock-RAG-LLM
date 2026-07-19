from __future__ import annotations

import pytest

from src.explorer_formula_expander import (
    ExplorerFormulaExpansionError,
    expand_explorer_filter,
)


def test_expands_referenced_columns_recursively() -> None:
    result = expand_explorer_filter(
        {
            "explorer_code_body": "ColB < 30 AND ColA > ColC",
            "col_definitions": [
                {"col_letter": "A", "col_code": "C"},
                {"col_letter": "B", "col_code": "RSI(14)"},
                {"col_letter": "C", "col_code": "Mov(ColA,50,S)"},
            ],
        }
    )

    assert result.expanded_filter == (
        "(RSI(14)) < 30 AND (C) > (Mov((C),50,S))"
    )
    assert result.referenced_columns == ("B", "A", "C")


def test_rejects_undefined_column() -> None:
    with pytest.raises(
        ExplorerFormulaExpansionError,
        match="undefined column ColB",
    ):
        expand_explorer_filter(
            {
                "explorer_code_body": "ColB > 0",
                "col_definitions": [],
            }
        )


def test_rejects_column_cycle() -> None:
    with pytest.raises(
        ExplorerFormulaExpansionError,
        match="cycle",
    ):
        expand_explorer_filter(
            {
                "explorer_code_body": "ColA > 0",
                "col_definitions": [
                    {"col_letter": "A", "col_code": "ColB"},
                    {"col_letter": "B", "col_code": "ColA"},
                ],
            }
        )
