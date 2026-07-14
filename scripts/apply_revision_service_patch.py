from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def replace_once(
    path: Path,
    old: str,
    new: str,
    *,
    already: str | None = None,
) -> None:
    content = path.read_text(encoding="utf-8")

    if already and already in content:
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


def patch_rag_service() -> None:
    path = ROOT / "src" / "rag_service.py"
    replace_once(
        path,
        'ResponseSource = Literal["cache", "generated", "repair"]\n',
        '''ResponseSource = Literal[
    "cache",
    "generated",
    "repair",
    "revision",
]
''',
        already='"revision",',
    )
    replace_once(
        path,
        '''                "retrieved_refs, service_log_id, repaired_from_explorer_id, "
                "repair_instruction"
''',
        '''                "retrieved_refs, service_log_id, repaired_from_explorer_id, "
                "repair_instruction, revised_from_explorer_id, "
                "revision_instruction"
''',
        already="revised_from_explorer_id",
    )


def patch_supabase_store() -> None:
    path = ROOT / "src" / "supabase_store.py"
    replace_once(
        path,
        '''    repaired_from_explorer_id: str | None = None,
    repair_instruction: str | None = None,
) -> str:
''',
        '''    repaired_from_explorer_id: str | None = None,
    repair_instruction: str | None = None,
    revised_from_explorer_id: str | None = None,
    revision_instruction: str | None = None,
) -> str:
''',
        already="revised_from_explorer_id: str | None",
    )

    replace_once(
        path,
        '''    repair_instruction = (
        str(repair_instruction).strip()
        if repair_instruction and str(repair_instruction).strip()
        else None
    )

    validation_passed = len(validation_errors) == 0
''',
        '''    repair_instruction = (
        str(repair_instruction).strip()
        if repair_instruction and str(repair_instruction).strip()
        else None
    )
    revised_from_explorer_id = (
        str(revised_from_explorer_id).strip()
        if revised_from_explorer_id
        else None
    )
    revision_instruction = (
        str(revision_instruction).strip()
        if revision_instruction
        and str(revision_instruction).strip()
        else None
    )

    if bool(repaired_from_explorer_id) and bool(revised_from_explorer_id):
        raise ValueError(
            "An Explorer row cannot be both a repair and a revision."
        )

    validation_passed = len(validation_errors) == 0
''',
        already="cannot be both a repair and a revision",
    )

    replace_once(
        path,
        '''        "repaired_from_explorer_id": repaired_from_explorer_id,
        "repair_instruction": repair_instruction,

        "status": "generated",
''',
        '''        "repaired_from_explorer_id": repaired_from_explorer_id,
        "repair_instruction": repair_instruction,
        "revised_from_explorer_id": revised_from_explorer_id,
        "revision_instruction": revision_instruction,

        "status": "generated",
''',
        already='"revised_from_explorer_id": revised_from_explorer_id',
    )

    replace_once(
        path,
        '''            "retrieved_refs, service_log_id, repaired_from_explorer_id, "
            "repair_instruction"
''',
        '''            "retrieved_refs, service_log_id, repaired_from_explorer_id, "
            "repair_instruction, revised_from_explorer_id, "
            "revision_instruction"
''',
        already='"repair_instruction, revised_from_explorer_id, "',
    )


def patch_read_service() -> None:
    path = ROOT / "src" / "rag_read_service.py"
    replace_once(
        path,
        '''                "retrieved_refs, service_log_id, repaired_from_explorer_id, "
                "repair_instruction"
''',
        '''                "retrieved_refs, service_log_id, repaired_from_explorer_id, "
                "repair_instruction, revised_from_explorer_id, "
                "revision_instruction"
''',
        already="revised_from_explorer_id",
    )


def main() -> None:
    patch_rag_service()
    patch_supabase_store()
    patch_read_service()
    print("RAG revision service support applied.")


if __name__ == "__main__":
    main()
