import argparse
import json
import re
import time
from typing import Any

import ollama

from src.context_builder import build_context_for_query
from src.validator import validate_explorer_output


DEFAULT_MODEL = "qwen2.5-coder:3b"


def build_prompt(user_query: str, context: str) -> str:
    return f"""
You are a MetaStock Explorer formula generator.

Your task:
Convert the user's natural language request into MetaStock Explorer columns and filter.

Use the provided context only.

Critical rules:
1. Output JSON only. Do not include markdown.
2. Generate MetaStock Explorer syntax that is likely to run.
3. Use price field abbreviations: C, O, H, L, V, OI.
4. Define columns before referencing them.
5. The filter may reference ColA, ColB, ColC, etc.
6. Do not reference undefined columns.
7. Do not use Ref(ColA,-1). Put Ref(...) inside a column formula instead.
8. Do not invent unsupported functions.
9. Use AND and OR, not && or ||.
10. Use = for equality, not ==.
11. If the user omits common defaults, state assumptions in notes.

Required JSON shape:
{
  "strategy_name": "string",
  "description": "string",
  "interpretation": "string",
  "columns": [
    {
      "letter": "A",
      "name": "string",
      "formula": "string"
    }
  ],
  "filter_code": "string",
  "explorer_summary": "string",
  "notes": ["string"]
}

Field rules:
- strategy_name should be short and suitable as a MetaStock Explorer name.
- description should explain what this Explorer scans for.
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

Return JSON only.
""".strip()


def extract_json_object(text: str) -> dict[str, Any]:
    """
    Ollama usually returns clean JSON when format='json',
    but this keeps the script robust if the model adds extra text.
    """
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in model output:\n{text}")

    return json.loads(match.group(0))


def generate_with_ollama(
    prompt: str,
    model: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    response = ollama.generate(
        model=model,
        prompt=prompt,
        format="json",
        options={
            "temperature": 0,
            "num_ctx": 8192,
        },
    )

    raw_text = response.get("response", "")
    return extract_json_object(raw_text)


def print_context_summary(
    user_query: str,
    dynamic_items: list[dict],
    prompt: str,
    model: str,
) -> None:
    print("\n=== Context Summary ===")
    print(f"Model: {model}")
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate MetaStock Explorer columns/filter using local Ollama."
    )

    parser.add_argument(
        "query",
        nargs="*",
        help="Natural language query. If omitted, interactive mode is used.",
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama model name. Default: {DEFAULT_MODEL}",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build context and show summary without calling Ollama.",
    )

    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="In dry-run mode, print the full prompt.",
    )

    return parser.parse_args()


def run_one_query(
    user_query: str,
    model: str,
    dry_run: bool = False,
    show_prompt: bool = False,
) -> None:
    print("\n[generate_explorer_local] Building context...")
    context, dynamic_items = build_context_for_query(user_query)

    prompt = build_prompt(user_query, context)

    print_context_summary(
        user_query=user_query,
        dynamic_items=dynamic_items,
        prompt=prompt,
        model=model,
    )

    if dry_run:
        if show_prompt:
            print("\n" + "=" * 100)
            print("FULL DRY RUN PROMPT")
            print("=" * 100)
            print(prompt)
        else:
            print("\n[DRY RUN] Ollama call skipped. Use --show-prompt to print the full prompt.")
        return

    print("\n[generate_explorer_local] Calling Ollama...")
    start = time.time()

    output = generate_with_ollama(
        prompt=prompt,
        model=model,
    )
    print(f"[generate_explorer_local] Ollama returned in {time.time() - start:.2f} seconds.")

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
            user_query=user_query,
            model=args.model,
            dry_run=args.dry_run,
            show_prompt=args.show_prompt,
        )
        return

    print("[generate_explorer_local] Interactive mode. Type 'exit' to quit.")

    while True:
        user_query = input("\nUser query: ").strip()

        if user_query.lower() in {"exit", "quit"}:
            break

        if not user_query:
            continue

        run_one_query(
            user_query=user_query,
            model=args.model,
            dry_run=args.dry_run,
            show_prompt=args.show_prompt,
        )


if __name__ == "__main__":
    main()