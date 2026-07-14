from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def replace_once(
    path: Path,
    old: str,
    new: str,
    *,
    already: str,
) -> None:
    content = path.read_text(encoding="utf-8")

    if already in content:
        print(f"Already patched: {path}")
        return

    count = content.count(old)
    if count != 1:
        raise RuntimeError(
            f"Expected one patch target in {path}; found {count}."
        )

    path.write_text(
        content.replace(old, new, 1),
        encoding="utf-8",
    )
    print(f"Patched: {path}")


def patch_generation_prompt() -> None:
    path = ROOT / "src" / "generate_explorer.py"

    replace_once(
        path,
        '''    explorer_name: str = Field(
        description="Short readable explorer name suitable for MetaStock. This maps to explorer_body.explorer_name."
    )
''',
        '''    explorer_name: str = Field(
        description=(
            "Short readable AI-managed Explorer name suitable for MetaStock. "
            "For an initial generation, prefix the otherwise generated name "
            "with the literal string AI_ and do not add a version suffix. "
            "This maps to explorer_body.explorer_name."
        )
    )
''',
        already="For an initial generation, prefix the otherwise generated name",
    )

    replace_once(
        path,
        '''10. If the user omits a common default, state the assumption by reflecting it in the description.

Output must be valid JSON matching this exact schema:
''',
        '''10. If the user omits a common default, state the assumption by reflecting it in the description.

Explorer naming rules:
- Every newly generated Explorer is AI-managed.
- explorer_name must begin with the exact prefix `AI_`.
- After `AI_`, keep the concise descriptive Explorer name that you would
  otherwise generate.
- For an initial generation, do not append a version number.
- Initial-name format: `AI_<generated explorer name>`.
- Do not add `AI_` more than once.
- Keep the name concise enough for practical MetaStock searching.

Output must be valid JSON matching this exact schema:
''',
        already="Initial-name format: `AI_<generated explorer name>`",
    )

    replace_once(
        path,
        '''  "explorer_name": "RSI Below 30",
''',
        '''  "explorer_name": "AI_RSI Below 30",
''',
        already='"explorer_name": "AI_RSI Below 30"',
    )


def patch_revision_prompt() -> None:
    path = ROOT / "src" / "rag_revision_service.py"

    replace_once(
        path,
        '''- Repair incidental syntax errors only when necessary for the revised output to
  validate.

Return valid JSON only with this schema:
''',
        '''- Repair incidental syntax errors only when necessary for the revised output to
  validate.

Explorer naming and version rules:
- A revision always creates a whole new Explorer.
- Preserve the existing Explorer's descriptive base name; do not rename it
  according to the changed formula.
- The AI-managed base name must begin with the exact prefix `AI_`.
- If the existing name does not begin with `AI_`, treat it as a legacy
  AI-generated name and add the `AI_` prefix.
- The initial Explorer is version 1 but does not display a version suffix.
- The first revised Explorer must append `_2`.
- Each later revision must increment only the final revision suffix:
  `_2` becomes `_3`, `_3` becomes `_4`, and so on.
- Revised-name format: `AI_<original generated explorer name>_<version number>`.
- Do not add `AI_` more than once.
- Do not omit the numeric suffix from a revised Explorer.

Examples:
- `RSI Below 30` revised for the first time becomes
  `AI_RSI Below 30_2`.
- `AI_RSI Below 30` revised for the first time becomes
  `AI_RSI Below 30_2`.
- `AI_RSI Below 30_2` revised again becomes
  `AI_RSI Below 30_3`.

Return valid JSON only with this schema:
''',
        already="Revised-name format: `AI_<original generated explorer name>_<version number>`",
    )


def main() -> None:
    patch_generation_prompt()
    patch_revision_prompt()
    print("AI Explorer naming prompt rules applied.")


if __name__ == "__main__":
    main()
