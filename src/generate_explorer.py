import argparse
import json
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from llama_index.core import Settings
from llama_index.llms.openai import OpenAI

from src.context_builder import build_context_for_query
from src.validator import validate_explorer_output


load_dotenv()


class ExplorerColumn(BaseModel):
    letter: str = Field(description="Explorer column letter, e.g. A, B, C")
    name: str = Field(description="Short column name, e.g. Close, RSI14, MA50")
    formula: str = Field(description="MetaStock formula for this column")


class ExplorerOutput(BaseModel):
    strategy_name: str = Field(
        description="Short readable strategy/explorer name suitable for MetaStock"
    )
    description: str = Field(
        description="One or two sentence description of what this Explorer does"
    )
    interpretation: str = Field(
        description="How the user query was interpreted"
    )
    columns: list[ExplorerColumn]
    filter_code: str = Field(
        description="MetaStock Explorer Filter code body only, without the word Filter:"
    )
    explorer_summary: str = Field(
        description="Human-readable summary containing Column A/B/C lines and Filter line"
    )
    notes: list[str] = Field(
        description="Assumptions, warnings, or defaults used"
    )


def build_prompt(user_query: str, context: str) -> str:
    return f"""
You are a MetaStock Explorer formula generator.

Your task:
Convert the user's natural language request into MetaStock Explorer columns and filter.

Use the context below.

Generation priorities:
1. Generate syntax that is likely to run in MetaStock Explorer.
2. Use price field abbreviations from base context: C, O, H, L, V, OI.
3. Use Explorer column/filter rules from base context.
4. Use dynamically retrieved function cards for formula logic.
5. Do not invent unsupported functions.
6. Prefer simple formulas.
7. Define columns before referencing them.
8. The filter may reference ColA, ColB, ColC, etc.
9. Do not use Ref(ColA,-1). Instead define a column such as Ref(C,-1).
10. If the user omits a common default, state the assumption in notes.

Output must be valid JSON matching this schema:

{{
  "strategy_name": "string",
  "description": "string",
  "interpretation": "string",
  "columns": [
    {{
      "letter": "A",
      "name": "string",
      "formula": "string"
    }}
  ],
  "filter_code": "string",
  "explorer_summary": "string",
  "notes": ["string"]
}}

Field rules:
- strategy_name should be short and suitable as a MetaStock Explorer name.
- description should explain what the strategy scans for.
- columns must contain the Explorer columns to define.
- column letters must start from A and continue sequentially: A, B, C, D...
- formula must contain only the formula body for that column.
- filter_code must contain only the MetaStock Filter formula body.
- Do not include "Filter:" inside filter_code.
- explorer_summary should contain a readable version like:
  Column A: C
  Column B: RSI(14)
  Column C: Mov(C,50,S)
  Filter: ColB < 30 AND ColA > ColC

Context:
{context}

User request:
{user_query}
""".strip()


def generate_with_openai(prompt: str) -> dict[str, Any]:
    Settings.llm = OpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    structured_llm = Settings.llm.as_structured_llm(ExplorerOutput)
    result = structured_llm.complete(prompt)

    output: ExplorerOutput = result.raw
    return output.model_dump()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate MetaStock Explorer columns/filter from natural language."
    )

    parser.add_argument(
        "query",
        nargs="*",
        help="Natural language query. If omitted, interactive mode is used.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build context and show a brief summary without calling the LLM.",
    )

    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="In dry-run mode, print the full prompt. This can be very long.",
    )

    return parser.parse_args()


def print_context_summary(
    user_query: str,
    dynamic_items: list[dict],
    prompt: str,
) -> None:
    print("\n=== Context Summary ===")
    print(f"User query: {user_query}")

    print("\nMandatory base files:")
    print("  1. price_fields.md")
    print("  2. explorer_basic.md")
    print("  3. explorer_columns_filter.md")

    print("\nDynamic retrieved files:")
    if not dynamic_items:
        print("  No dynamic files retrieved.")
    else:
        for i, item in enumerate(dynamic_items, start=1):
            print(f"  {i}. {item['file_name']} | score={item['score']:.4f}")

    print("\nPrompt size:")
    print(f"  {len(prompt)} characters")


def run_one_query(
    user_query: str,
    dry_run: bool = False,
    show_prompt: bool = False,
) -> None:
    print("\n[generate_explorer] Building context...")
    context, dynamic_items = build_context_for_query(user_query)

    prompt = build_prompt(user_query, context)

    print_context_summary(
        user_query=user_query,
        dynamic_items=dynamic_items,
        prompt=prompt,
    )

    if dry_run:
        if show_prompt:
            print("\n" + "=" * 100)
            print("FULL DRY RUN PROMPT")
            print("=" * 100)
            print(prompt)
        else:
            print("\n[DRY RUN] LLM call skipped. Use --show-prompt to print the full prompt.")
        return

    print("\n[generate_explorer] Calling LLM...")

    output = generate_with_openai(prompt)

    print("\n=== Explorer Output ===")
    print(json.dumps(output, indent=2))

    errors = validate_explorer_output(output)

    print("\n=== Validation ===")
    if errors:
        print("[FAILED]")
        for e in errors:
            print(f"- {e}")
    else:
        print("[PASSED]")


def main() -> None:
    args = parse_args()

    if args.query:
        user_query = " ".join(args.query).strip()
        run_one_query(
            user_query,
            dry_run=args.dry_run,
            show_prompt=args.show_prompt,
        )
        return

    print("[generate_explorer] Interactive mode. Type 'exit' to quit.")

    while True:
        user_query = input("\nUser query: ").strip()

        if user_query.lower() in {"exit", "quit"}:
            break

        if not user_query:
            continue

        run_one_query(
            user_query,
            dry_run=args.dry_run,
            show_prompt=args.show_prompt,
        )


if __name__ == "__main__":
    main()