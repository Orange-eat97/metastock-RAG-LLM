import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.context_builder import build_context_for_query


def main() -> None:
    queries = [
        "Find stocks where close is above 50 day moving average",
        "Find stocks where fast moving average crosses above slow moving average",
        "Find stocks where RSI is below 30 and close is above 50 day moving average",
    ]

    for query in queries:
        print("\n" + "=" * 100)
        print(f"QUERY: {query}")
        print("=" * 100)

        context, dynamic_items = build_context_for_query(query)

        print("\nMandatory base context is included:")
        print("  - price_fields.md")
        print("  - explorer_basic.md")
        print("  - explorer_columns_filter.md")

        print("\nDynamic retrieved files:")

        for i, item in enumerate(dynamic_items, start=1):
            print(f"  {i}. {item['file_name']} | score={item['score']:.4f}")

        print("\nFinal context length:")
        print(f"  {len(context)} characters")


if __name__ == "__main__":
    main()