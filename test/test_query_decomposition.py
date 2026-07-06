from src.queryDecomposition.query_decomposer import (
    decompose_query_for_retrieval,
    get_forced_card_names,
)


def main() -> None:
    queries = [
        "Find stocks breaking above the previous 20 day high with volume above average",
        "Find stocks where RSI is below 30 and close is above 50 day moving average",
        "Find stocks where fast MA crosses above slow MA",
        "Find stocks making a new 20 day low",
    ]

    for query in queries:
        print("\n" + "=" * 80)
        print(f"QUERY: {query}")

        intents = decompose_query_for_retrieval(query)
        forced_names = get_forced_card_names(intents)

        print("\n--- Retrieval intents ---")
        for i, intent in enumerate(intents, start=1):
            print(f"{i}. [{intent.target_bucket}] {intent.query}")
            print(f"   reason: {intent.reason}")
            print(f"   force: {list(intent.force_card_names)}")
            print(f"   rule: {intent.source_rule}")

        print("\n--- Forced card names ---")
        for name in forced_names:
            print(f"- {name}")


if __name__ == "__main__":
    main()