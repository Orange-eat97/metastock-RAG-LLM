from __future__ import annotations

from uuid import UUID

import pytest

from src.system_test_definition import SystemTestDefinition
from src.system_test_validator import validate_system_test_definition


from sample_payload import EXAMPLE



def test_exact_automator_contract_is_accepted() -> None:
    definition = SystemTestDefinition.model_validate(EXAMPLE)

    assert definition.system_test_id == UUID(
        "11111111-1111-1111-1111-111111111111"
    )
    assert definition.model_dump(mode="json") == EXAMPLE
    assert validate_system_test_definition(definition).passed is True


def test_rejects_explorer_column_reference() -> None:
    invalid = {
        **EXAMPLE,
        "orders": {
            **EXAMPLE["orders"],
            "buy": {
                "enabled": True,
                "signal_formula": "ColA > 0",
            },
        },
    }

    with pytest.raises(ValueError, match="Explorer column references"):
        SystemTestDefinition.model_validate(invalid)


def test_rejects_enabled_stops() -> None:
    invalid = {
        **EXAMPLE,
        "stops": {"enabled": True},
    }

    with pytest.raises(ValueError):
        SystemTestDefinition.model_validate(invalid)
