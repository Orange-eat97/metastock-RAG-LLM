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
    "AND",
    "OR"
}

VALID_COL_LETTERS = set("ABCDEFGHIJKL")

FORBIDDEN_TOKENS = {
    "==": "Use = instead of ==.",
    "&&": "Use AND instead of &&.",
    "||": "Use OR instead of ||.",
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

    if not formula or not formula.strip():
        errors.append("Formula is empty.")
        return errors

    formula = formula.strip()
    errors.extend(check_parentheses(formula))

    lower_formula = formula.lower()

    for token, message in FORBIDDEN_TOKENS.items():
        if token in lower_formula:
            errors.append(message)

    if "filter:" in lower_formula:
        errors.append("Do not include the label 'Filter:' in code fields.")

    if re.search(r"\bcol\s+[A-L]\s*=", lower_formula, re.IGNORECASE):
        errors.append("Do not include 'col A =' inside col_code. Store only the formula body.")

    allowed_lower = {f.lower() for f in ALLOWED_FUNCTIONS}

    for func in extract_functions(formula):
        if func.lower() not in allowed_lower:
            errors.append(f"Function may be unsupported or missing from whitelist: {func}")

    return errors


def validate_explorer_output(output: dict[str, Any]) -> list[str]:
    errors = []

    explorer_name = str(output.get("explorer_name", "")).strip()
    explorer_code_body = str(output.get("explorer_code_body", "")).strip()
    col_definitions = output.get("col_definitions", [])

    if not explorer_name:
        errors.append("explorer_name is required.")

    if not explorer_code_body:
        errors.append("explorer_code_body is required.")

    if not isinstance(col_definitions, list):
        errors.append("col_definitions must be a list.")
        col_definitions = []

    for e in validate_formula(explorer_code_body):
        errors.append(f"explorer_code_body: {e}")

    seen_letters = set()

    for i, col in enumerate(col_definitions):
        if not isinstance(col, dict):
            errors.append(f"col_definitions[{i}] must be an object.")
            continue

        col_letter = str(col.get("col_letter", "")).strip().upper()
        col_code = str(col.get("col_code", "")).strip()

        if col_letter not in VALID_COL_LETTERS:
            errors.append(
                f"col_definitions[{i}].col_letter must be one of A-L, got {col_letter!r}."
            )

        if col_letter in seen_letters:
            errors.append(f"Duplicate col_letter: {col_letter}.")

        seen_letters.add(col_letter)

        if not col_code:
            errors.append(f"col_definitions[{i}].col_code is required.")
        else:
            for e in validate_formula(col_code):
                errors.append(f"col {col_letter}: {e}")

    return errors