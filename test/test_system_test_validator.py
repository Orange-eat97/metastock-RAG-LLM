from __future__ import annotations

from copy import deepcopy

from src.system_test_definition import SystemTestDefinition
from src.system_test_validator import validate_system_test_definition
from sample_payload import EXAMPLE


def test_rejects_future_ref() -> None:
    payload = deepcopy(EXAMPLE)
    payload["orders"]["sell"]["signal_formula"] = "C < Ref(C,1)"
    definition = SystemTestDefinition.model_validate(payload)

    result = validate_system_test_definition(definition)

    assert result.passed is False
    assert any("future lookahead" in error for error in result.errors)


def test_rejects_simulation_inside_historical_function() -> None:
    payload = deepcopy(EXAMPLE)
    payload["orders"]["sell"]["signal_formula"] = (
        "Ref(Simulation.CurrentPositionAge,-1) > 10"
    )
    definition = SystemTestDefinition.model_validate(payload)

    result = validate_system_test_definition(definition)

    assert result.passed is False
    assert any("Simulation" in error for error in result.errors)
