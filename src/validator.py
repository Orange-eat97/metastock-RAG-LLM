import re
from typing import Any


ALLOWED_FUNCTIONS = {
    "RSI",
    "Mov",
    "Cross",
    "Ref",
    "HHV",
    "LLV",
    "MACD",
    "If",
    "Abs",
    "Sum",
    "ROC",
    "ATR",
    "Max",
    "Min",
    "Cum",
    "ValueWhen",
    "BarsSince",
    "LastValue",
}

FORBIDDEN_TOKENS = {
    "==": "Use = instead of ==.",
    "&&": "Use AND instead of &&.",
    "||": "Use OR instead of ||.",
    "close": "Use C instead of close inside formulas.",
    "volume": "Use V instead of volume inside formulas.",
    "open": "Use O instead of open inside formulas.",
    "high": "Use H instead of high inside formulas.",
    "low": "Use L instead of low inside formulas.",
}


def check_parentheses(text: str) -> list[str]:
    errors = []
    stack = []

    for i, ch in enumerate(text):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            if not stack:
                errors.append(f"Unmatched closing parenthesis at position {i}.")
            else:
                stack.pop()

    if stack:
        errors.append("Unmatched opening parenthesis.")

    return errors


def extract_functions(formula: str) -> list[str]:
    return re.findall(r"\b([A-Za-z][A-Za-z0-9_]*)\s*\(", formula)


def validate_formula(formula: str) -> list[str]:
    errors = []

    if not formula:
        errors.append("Formula is empty.")
        return errors

    errors.extend(check_parentheses(formula))

    lower_formula = formula.lower()

    for token, message in FORBIDDEN_TOKENS.items():
        if token in lower_formula:
            errors.append(message)

    allowed_lower = {f.lower() for f in ALLOWED_FUNCTIONS}

    for func in extract_functions(formula):
        if func.lower() not in allowed_lower:
            errors.append(f"Function may be unsupported or missing from whitelist: {func}")

    return errors


def validate_explorer_output(output: dict[str, Any]) -> list[str]:
    errors = []

    columns = output.get("columns", [])
    filter_formula = output.get("filter_code") or output.get("filter", "")

    if not columns:
        errors.append("No columns were generated.")

    expected_letters = [chr(ord("A") + i) for i in range(len(columns))]

    for i, col in enumerate(columns):
        formula = col.get("formula", "")
        col_name = col.get("name", f"Column {i + 1}")

        letter = str(col.get("letter", "")).strip().upper()
        expected = expected_letters[i]

        if letter != expected:
            errors.append(
                f"Column {i + 1} should have letter {expected}, but got {letter!r}."
            )

        for e in validate_formula(formula):
            errors.append(f"{col_name}: {e}")

    for e in validate_formula(filter_formula):
        errors.append(f"Filter: {e}")

    if "Filter:" in filter_formula:
        errors.append(
            "filter_code should not include the label 'Filter:'. Use only the formula body."
        )

    max_col_index = len(columns)
    refs = re.findall(r"\bCol([A-Z])\b", filter_formula)

    for ref in refs:
        col_num = ord(ref) - ord("A") + 1
        if col_num > max_col_index:
            errors.append(
                f"Filter references Col{ref}, but only {max_col_index} columns are defined."
            )

    if re.search(r"Ref\s*\(\s*Col[A-Z]", filter_formula, re.IGNORECASE):
        errors.append(
            "Do not use Ref(ColA,-1). Put Ref(...) inside a column formula instead."
        )

    return errors