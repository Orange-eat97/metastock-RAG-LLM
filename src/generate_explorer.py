import argparse
import json
from typing import Any

from dotenv import load_dotenv, parser
from pydantic import BaseModel, Field, field_validator

from llama_index.core import Settings
from llama_index.llms.openai import OpenAI

from src.context_builder import build_context_for_query
from src.validator import validate_explorer_output
from src.explorer_excel_store import save_explorer_output_to_excel


load_dotenv()


VALID_COL_LETTERS = set("ABCDEFGHIJKL")
MODEL = "gpt-5.5"


class ColDefinition(BaseModel):
    col_letter: str = Field(
        description="Explorer column letter from A to L"
    )
    col_code: str = Field(
        description="MetaStock formula code body for this column, not natural language"
    )

    @field_validator("col_letter")
    @classmethod
    def validate_col_letter(cls, value: str) -> str:
        letter = value.strip().upper()
        if letter not in VALID_COL_LETTERS:
            raise ValueError("col_letter must be one of A through L.")
        return letter


class ExplorerOutput(BaseModel):
    explorer_name: str = Field(
        description="Short readable explorer name suitable for MetaStock. This maps to explorer_body.explorer_name."
    )
    explorer_description: str = Field(
        description="Optional explanation for the Explorer. This maps to explorer_body.explorer_description."
    )
    explorer_code_body: str = Field(
        description="Actual MetaStock Explorer Filter code body. Do not include the word Filter:"
    )
    col_definitions: list[ColDefinition] = Field(
        description="Column definitions for this Explorer. Each maps to col_definitions."
    )


def build_prompt(user_query: str, context: str) -> str:
    return f"""
You are a MetaStock Explorer formula generator.

Your task:
Convert the user's natural language request into a MetaStock Explorer object.

Use the provided context only.

Generation priorities:
1. Generate MetaStock syntax that is likely to run in MetaStock Explorer.
2. Use price field abbreviations from base context: C, O, H, L, V, OI.
3. Use dynamically retrieved function cards for formula logic.
4. Do not invent unsupported MetaStock functions.
5. Prefer simple formulas.
6. Use AND and OR, not && or ||.
7. Use = for equality, not ==.
8. If the user omits a common default, state the assumption by reflecting it in the description.

Output must be valid JSON matching this exact schema:

{{
  "explorer_name": "string",
  "explorer_description": "string",
  "explorer_code_body": "string",
  "col_definitions": [
    {{
      "col_letter": "A",
      "col_code": "string"
    }}
  ]
}}

Database and automator contract:
- explorer_name maps to explorer_body.explorer_name.
- explorer_description maps to explorer_body.explorer_description.
- explorer_code_body maps to explorer_body.explorer_code_body.
- col_definitions maps to the col_definitions table.
- col_letter must be one uppercase letter from A to L.
- col_code must be the MetaStock formula body for that column.
- explorer_code_body must be the actual MetaStock Explorer Filter code body to paste into the Filter editor.
- explorer_code_body may be independent from col_definitions.
- Prefer direct formulas in explorer_code_body, for example RSI(14) < 30.
- Do not include "Filter:" inside explorer_code_body.
- Do not include "col A =" inside col_code.
- Do not include natural language inside explorer_code_body or col_code.

Column definition examples:
- If col_letter is A and col_code is RSI(14), the automator can construct: col A = RSI(14)
- If col_letter is B and col_code is Mov(C,50,S), the automator can construct: col B = Mov(C,50,S)

Good output example:
{{
  "explorer_name": "RSI Below 30",
  "explorer_description": "Finds stocks where RSI is below 30, indicating potential oversold conditions.",
  "explorer_code_body": "RSI(14) < 30",
  "col_definitions": [
    {{
      "col_letter": "A",
      "col_code": "RSI(14)"
    }}
  ]
}}

Context:
{context}

User request:
{user_query}

Return JSON only.
""".strip()


def generate_with_openai(prompt: str) -> dict[str, Any]:
    Settings.llm = OpenAI(
        model=MODEL,
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

    parser.add_argument(
    "--no-save",
    action="store_true",
    help="Do not save generated JSON output to local Excel.",
    )

    parser.add_argument(
    "--excel-path",
    default="data/explorer_outputs.xlsx",
    help="Path to local Excel output file.",
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
    save_output: bool = True,
    excel_path: str = "data/explorer_outputs.xlsx",
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

        if save_output:
            saved_path = save_explorer_output_to_excel(
            output=output,
            user_query=user_query,
            backend="openai",
            model=MODEL,
            validation_errors=errors,
            excel_path=excel_path,
        )
        print(f"\n[generate_explorer] Saved output to: {saved_path}")


def main() -> None:
    args = parse_args()

    if args.query:
        user_query = " ".join(args.query).strip()
        run_one_query(
            user_query,
            dry_run=args.dry_run,
            show_prompt=args.show_prompt,
            save_output=not args.no_save,
            excel_path=args.excel_path,
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
            save_output=not args.no_save,
            excel_path=args.excel_path,
        )


if __name__ == "__main__":
    main()