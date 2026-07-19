EXAMPLE = {
    "schema_version": "1.0",
    "system_test_id": "11111111-1111-1111-1111-111111111111",
    "source_explorer_id": "22222222-2222-2222-2222-222222222222",
    "name": "RAG long-only smoke test",
    "description": "Created from a validated Explorer output.",
    "general": {
        "order_bias": "long",
        "portfolio_bias": "single",
        "position_limit": {"enabled": True, "max_positions": 1},
    },
    "orders": {
        "buy": {
            "enabled": True,
            "signal_formula": (
                "BuySignal := Cross(C, Mov(C,20,S));\n"
                "BuySignal AND Simulation.LongPositionCount = 0"
            ),
        },
        "sell": {
            "enabled": True,
            "signal_formula": "Cross(Mov(C,20,S), C)",
        },
        "sell_short": {"enabled": False, "signal_formula": ""},
        "buy_to_cover": {"enabled": False, "signal_formula": ""},
    },
    "stops": {"enabled": False},
    "optimizations": {"enabled": False},
    "metadata": {
        "generator": "metastock-RAG-LLM",
        "conversion_kind": "explorer_to_system_test",
    },
}
