from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

from dotenv import load_dotenv
from supabase import Client, create_client

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: PyYAML\n\nInstall with:\n  pip install pyyaml\n"
    ) from exc


load_dotenv()

ALLOWED_ALIAS_TYPES = {"exact", "synonym", "phrase", "abbreviation", "weak_hint"}
SUPPORTED_EDGE_TYPES = {
    "requires",
    "suggests",
    "conflicts_with",
    "forbids",
    "similar_to",
    "expands_to",
}
VALID_CARD_TYPES = {"function", "pattern", "reference", "template", "example", "pitfall"}
VALID_BUCKETS = {"functions", "patterns", "references", "templates", "examples", "pitfalls"}

TYPE_TO_BUCKET = {
    "function": "functions",
    "pattern": "patterns",
    "reference": "references",
    "template": "templates",
    "example": "examples",
    "pitfall": "pitfalls",
}

BUCKET_TO_TYPE = {
    "functions": "function",
    "patterns": "pattern",
    "references": "reference",
    "templates": "template",
    "examples": "example",
    "pitfalls": "pitfall",
}


@dataclass(frozen=True)
class RegistryRow:
    canonical_id: str
    title: str
    concept_type: str
    card_bucket: str
    source_path: str
    is_active: bool = True

    def to_db_row(self) -> dict[str, Any]:
        return {
            "canonical_id": self.canonical_id,
            "title": self.title,
            "concept_type": self.concept_type,
            "card_bucket": self.card_bucket,
            "source_path": self.source_path,
            "is_active": self.is_active,
        }


@dataclass(frozen=True)
class AliasRow:
    canonical_id: str
    alias_text: str
    alias_type: str
    weight: float
    is_active: bool = True

    def to_db_row(self) -> dict[str, Any]:
        return {
            "canonical_id": self.canonical_id,
            "alias_text": self.alias_text,
            "alias_type": self.alias_type,
            "weight": self.weight,
            "is_active": self.is_active,
        }


@dataclass(frozen=True)
class DependencyRow:
    from_canonical_id: str
    to_canonical_id: str
    edge_type: str
    priority: int
    rationale: str
    properties: dict[str, Any] = field(default_factory=dict)
    is_active: bool = True

    def to_db_row(self) -> dict[str, Any]:
        return {
            "from_canonical_id": self.from_canonical_id,
            "to_canonical_id": self.to_canonical_id,
            "edge_type": self.edge_type,
            "priority": self.priority,
            "rationale": self.rationale,
            "properties": self.properties,
            "is_active": self.is_active,
        }


@dataclass(frozen=True)
class ParsedCard:
    path: Path
    source_path: str
    frontmatter: dict[str, Any]
    registry_row: RegistryRow
    aliases: list[AliasRow]
    dependencies: list[DependencyRow]


@dataclass
class SyncPlan:
    cards: list[ParsedCard] = field(default_factory=list)
    registry_rows: list[RegistryRow] = field(default_factory=list)
    alias_rows: list[AliasRow] = field(default_factory=list)
    dependency_rows: list[DependencyRow] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


# ============================================================
# CLI
# ============================================================


def main() -> None:
    args = parse_args()
    knowledge_dir = Path(args.knowledge_dir).resolve()

    if not knowledge_dir.exists():
        raise SystemExit(f"Knowledge directory does not exist: {knowledge_dir}")

    plan = build_sync_plan(
        knowledge_dir=knowledge_dir,
        source_prefix=args.source_prefix,
        strict=args.strict,
    )

    print_plan(plan, verbose=args.verbose)

    if plan.errors:
        print("\n[ERROR] Sync plan has validation errors. Fix the cards first.", file=sys.stderr)
        raise SystemExit(1)

    if not args.apply:
        print("\n[DRY RUN] No Supabase writes were made. Use --apply to upsert.")
        return

    supabase = make_supabase_client()

    if args.require_rag_cards:
        validate_rag_cards_exist(
            supabase=supabase,
            registry_rows=plan.registry_rows,
            fail_on_missing=True,
        )
    else:
        validate_rag_cards_exist(
            supabase=supabase,
            registry_rows=plan.registry_rows,
            fail_on_missing=False,
        )

    existing_or_batch_ids = fetch_existing_registry_ids(supabase) | {
        row.canonical_id for row in plan.registry_rows
    }

    dependency_rows = filter_dependency_rows(
        dependency_rows=plan.dependency_rows,
        known_registry_ids=existing_or_batch_ids,
        fail_missing_targets=args.fail_missing_dependency_targets,
    )

    upsert_registry_rows(supabase, plan.registry_rows, batch_size=args.batch_size)
    upsert_alias_rows(supabase, plan.alias_rows, batch_size=args.batch_size)
    upsert_dependency_rows(supabase, dependency_rows, batch_size=args.batch_size)

    print("\n[DONE] Registry, aliases, and dependencies synced.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sync registry, alias, and dependency metadata from registry-ready "
            "MetaStock markdown knowledge cards."
        )
    )
    parser.add_argument(
        "--knowledge-dir",
        default="knowledge_base",
        help="Root folder containing markdown cards. Default: knowledge_base",
    )
    parser.add_argument(
        "--source-prefix",
        default="",
        help=(
            "Optional prefix to prepend to source_path. Normally leave empty so "
            "knowledge_base/functions/macd.md becomes functions/macd.md."
        ),
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write to Supabase. Without this flag, the script runs as a dry run.",
    )
    parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Fail on missing required registry-ready frontmatter. Default: true.",
    )
    parser.add_argument(
        "--require-rag-cards",
        action="store_true",
        help="Fail if a registry source_path does not already exist in rag_cards.",
    )
    parser.add_argument(
        "--fail-missing-dependency-targets",
        action="store_true",
        help=(
            "Fail if a dependency target is not already in rag_card_registry "
            "or in the current batch. Default: warn and skip that edge."
        ),
    )
    parser.add_argument("--batch-size", type=int, default=500)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


# ============================================================
# Parse cards
# ============================================================


def build_sync_plan(
    *,
    knowledge_dir: Path,
    source_prefix: str,
    strict: bool,
) -> SyncPlan:
    plan = SyncPlan()

    markdown_paths = sorted(knowledge_dir.rglob("*.md"))
    if not markdown_paths:
        plan.errors.append(f"No .md files found under {knowledge_dir}")
        return plan

    for path in markdown_paths:
        try:
            parsed = parse_card(
                path=path,
                knowledge_dir=knowledge_dir,
                source_prefix=source_prefix,
                strict=strict,
            )
        except CardValidationError as exc:
            plan.errors.append(str(exc))
            continue
        except Exception as exc:
            plan.errors.append(f"{path}: unexpected parse error: {exc}")
            continue

        if parsed is None:
            continue

        plan.cards.append(parsed)
        plan.registry_rows.append(parsed.registry_row)
        plan.alias_rows.extend(parsed.aliases)
        plan.dependency_rows.extend(parsed.dependencies)

    plan.registry_rows = dedupe_registry_rows(plan.registry_rows)
    plan.alias_rows = dedupe_alias_rows(plan.alias_rows)
    plan.dependency_rows = dedupe_dependency_rows(plan.dependency_rows)

    plan.warnings.extend(validate_duplicate_source_paths(plan.registry_rows))
    plan.warnings.extend(validate_duplicate_canonical_ids(plan.registry_rows))

    return plan


def parse_card(
    *,
    path: Path,
    knowledge_dir: Path,
    source_prefix: str,
    strict: bool,
) -> ParsedCard | None:
    frontmatter, body = read_markdown_frontmatter(path)
    source_path = make_source_path(path, knowledge_dir, source_prefix=source_prefix)

    registry_config = as_dict(frontmatter.get("registry"))
    if registry_config.get("enabled") is False:
        print(f"[SKIP] registry.enabled=false | {source_path}")
        return None

    registry_row = parse_registry_row(
        source_path=source_path,
        frontmatter=frontmatter,
        body=body,
        strict=strict,
        card_path=path,
    )

    aliases = parse_aliases(
        canonical_id=registry_row.canonical_id,
        title=registry_row.title,
        frontmatter=frontmatter,
        strict=strict,
        card_path=path,
    )

    dependencies = parse_dependencies(
        from_canonical_id=registry_row.canonical_id,
        source_path=source_path,
        frontmatter=frontmatter,
        strict=strict,
        card_path=path,
    )

    return ParsedCard(
        path=path,
        source_path=source_path,
        frontmatter=frontmatter,
        registry_row=registry_row,
        aliases=aliases,
        dependencies=dependencies,
    )


def read_markdown_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, flags=re.DOTALL)
    if not match:
        raise CardValidationError(f"{path}: malformed YAML frontmatter fence")

    raw_yaml = match.group(1)
    body = match.group(2)
    data = yaml.safe_load(raw_yaml) or {}

    if not isinstance(data, dict):
        raise CardValidationError(f"{path}: YAML frontmatter must be a mapping")

    return data, body


def parse_registry_row(
    *,
    source_path: str,
    frontmatter: dict[str, Any],
    body: str,
    strict: bool,
    card_path: Path,
) -> RegistryRow:
    canonical_id = clean_text(frontmatter.get("canonical_id"))
    title = clean_text(frontmatter.get("title")) or first_heading(body)
    concept_type = clean_text(frontmatter.get("type") or frontmatter.get("concept_type"))
    card_bucket = clean_text(frontmatter.get("card_bucket"))
    status = clean_text(frontmatter.get("status") or "active").lower()

    missing = []
    for field_name, value in [
        ("canonical_id", canonical_id),
        ("title", title),
        ("type", concept_type),
        ("card_bucket", card_bucket),
        ("category", clean_text(frontmatter.get("category"))),
        ("source", clean_text(frontmatter.get("source"))),
        ("status", status),
        ("priority", frontmatter.get("priority")),
        ("supports_explorer", frontmatter.get("supports_explorer")),
    ]:
        if value in (None, ""):
            missing.append(field_name)

    if missing and strict:
        raise CardValidationError(
            f"{card_path}: missing required frontmatter field(s): {', '.join(missing)}"
        )

    if not canonical_id:
        canonical_id = derive_canonical_id(source_path, concept_type, card_bucket)

    if not title:
        title = title_from_source_path(source_path)

    if not concept_type:
        concept_type = derive_type(canonical_id, card_bucket)

    if not card_bucket:
        card_bucket = TYPE_TO_BUCKET.get(concept_type, derive_bucket(source_path))

    concept_type = normalize_identifier_value(concept_type)
    card_bucket = normalize_identifier_value(card_bucket)
    canonical_id = normalize_canonical_id(canonical_id)

    if concept_type not in VALID_CARD_TYPES:
        raise CardValidationError(
            f"{card_path}: type must be one of {sorted(VALID_CARD_TYPES)}, got {concept_type!r}"
        )

    if card_bucket not in VALID_BUCKETS:
        raise CardValidationError(
            f"{card_path}: card_bucket must be one of {sorted(VALID_BUCKETS)}, got {card_bucket!r}"
        )

    expected_prefix = concept_type
    if not canonical_id.startswith(expected_prefix + "."):
        raise CardValidationError(
            f"{card_path}: canonical_id {canonical_id!r} should start with {expected_prefix!r}."
        )

    return RegistryRow(
        canonical_id=canonical_id,
        title=title,
        concept_type=concept_type,
        card_bucket=card_bucket,
        source_path=source_path,
        is_active=(status == "active"),
    )


def parse_aliases(
    *,
    canonical_id: str,
    title: str,
    frontmatter: dict[str, Any],
    strict: bool,
    card_path: Path,
) -> list[AliasRow]:
    rows: list[AliasRow] = []

    raw_aliases = frontmatter.get("aliases")
    if raw_aliases is None:
        if strict:
            raise CardValidationError(f"{card_path}: missing required aliases list")
        raw_aliases = []

    if not isinstance(raw_aliases, list):
        raise CardValidationError(f"{card_path}: aliases must be a list")

    # The title is useful as an exact alias, but only when it is not overly generic.
    if title:
        rows.append(
            AliasRow(
                canonical_id=canonical_id,
                alias_text=normalize_alias_text(title),
                alias_type="exact",
                weight=1.0,
                is_active=True,
            )
        )

    for index, item in enumerate(raw_aliases):
        row = parse_one_alias(
            canonical_id=canonical_id,
            item=item,
            index=index,
            strict=strict,
            card_path=card_path,
        )
        rows.append(row)

    rows = dedupe_alias_rows(rows)

    if strict and not rows:
        raise CardValidationError(f"{card_path}: at least one alias is required")

    return rows


def parse_one_alias(
    *,
    canonical_id: str,
    item: Any,
    index: int,
    strict: bool,
    card_path: Path,
) -> AliasRow:
    if isinstance(item, str):
        alias_text = normalize_alias_text(item)
        alias_type = infer_alias_type(alias_text)
        weight = default_alias_weight(alias_type)
    elif isinstance(item, dict):
        alias_text = normalize_alias_text(item.get("text") or item.get("alias_text") or item.get("alias"))
        alias_type = clean_text(item.get("type") or item.get("alias_type") or "phrase")
        weight = parse_weight(item.get("weight"), default=default_alias_weight(alias_type))
    else:
        raise CardValidationError(f"{card_path}: aliases[{index}] must be string or object")

    alias_type = normalize_identifier_value(alias_type)

    if not alias_text:
        raise CardValidationError(f"{card_path}: aliases[{index}] has empty text")

    if alias_type not in ALLOWED_ALIAS_TYPES:
        raise CardValidationError(
            f"{card_path}: aliases[{index}] has unsupported alias type {alias_type!r}; "
            f"allowed={sorted(ALLOWED_ALIAS_TYPES)}"
        )

    return AliasRow(
        canonical_id=canonical_id,
        alias_text=alias_text,
        alias_type=alias_type,
        weight=weight,
        is_active=True,
    )


def parse_dependencies(
    *,
    from_canonical_id: str,
    source_path: str,
    frontmatter: dict[str, Any],
    strict: bool,
    card_path: Path,
) -> list[DependencyRow]:
    rows: list[DependencyRow] = []

    for edge_type in SUPPORTED_EDGE_TYPES:
        raw_items = frontmatter.get(edge_type) or []
        if raw_items is None:
            raw_items = []
        if isinstance(raw_items, (str, dict)):
            raw_items = [raw_items]
        if not isinstance(raw_items, list):
            raise CardValidationError(f"{card_path}: {edge_type} must be a list")

        for index, item in enumerate(raw_items):
            row = parse_one_dependency(
                from_canonical_id=from_canonical_id,
                source_path=source_path,
                edge_type=edge_type,
                item=item,
                index=index,
                card_path=card_path,
            )

            if row.from_canonical_id == row.to_canonical_id:
                if strict:
                    raise CardValidationError(
                        f"{card_path}: self dependency is not allowed: {row.from_canonical_id}"
                    )
                continue

            rows.append(row)

    return dedupe_dependency_rows(rows)


def parse_one_dependency(
    *,
    from_canonical_id: str,
    source_path: str,
    edge_type: str,
    item: Any,
    index: int,
    card_path: Path,
) -> DependencyRow:
    if isinstance(item, str):
        to_canonical_id = normalize_canonical_id(item)
        rationale = f"Declared in {edge_type} frontmatter for {source_path}."
        properties: dict[str, Any] = {"source": "frontmatter", "source_path": source_path}
        priority = (index + 1) * 10
    elif isinstance(item, dict):
        to_canonical_id = normalize_canonical_id(
            item.get("canonical_id") or item.get("to_canonical_id") or item.get("target") or item.get("to")
        )
        rationale = clean_text(item.get("rationale")) or f"Declared in {edge_type} frontmatter for {source_path}."
        properties = as_dict(item.get("properties"))
        properties.setdefault("source", "frontmatter")
        properties.setdefault("source_path", source_path)
        priority = parse_int(item.get("priority"), default=(index + 1) * 10)
    else:
        raise CardValidationError(f"{card_path}: {edge_type}[{index}] must be string or object")

    if not to_canonical_id:
        raise CardValidationError(f"{card_path}: {edge_type}[{index}] missing canonical_id")

    if "." not in to_canonical_id:
        raise CardValidationError(
            f"{card_path}: {edge_type}[{index}] dependency must use canonical ID, got {to_canonical_id!r}"
        )

    return DependencyRow(
        from_canonical_id=from_canonical_id,
        to_canonical_id=to_canonical_id,
        edge_type=edge_type,
        priority=priority,
        rationale=rationale,
        properties=properties,
        is_active=True,
    )


# ============================================================
# Supabase writes
# ============================================================


def make_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url:
        raise RuntimeError("Missing SUPABASE_URL")
    if not key:
        raise RuntimeError("Missing SUPABASE_SERVICE_ROLE_KEY")
    return create_client(url, key)


def fetch_existing_registry_ids(supabase: Client) -> set[str]:
    rows = []
    page_size = 1000
    start = 0

    while True:
        response = (
            supabase.table("rag_card_registry")
            .select("canonical_id")
            .range(start, start + page_size - 1)
            .execute()
        )
        batch = response.data or []
        rows.extend(batch)
        if len(batch) < page_size:
            break
        start += page_size

    return {row["canonical_id"] for row in rows if row.get("canonical_id")}


def validate_rag_cards_exist(
    *,
    supabase: Client,
    registry_rows: list[RegistryRow],
    fail_on_missing: bool,
) -> None:
    source_paths = [row.source_path for row in registry_rows]
    if not source_paths:
        return

    existing: set[str] = set()
    for chunk in chunks(source_paths, 500):
        response = (
            supabase.table("rag_cards")
            .select("source_path")
            .in_("source_path", chunk)
            .execute()
        )
        existing.update(row["source_path"] for row in (response.data or []) if row.get("source_path"))

    missing = [path for path in source_paths if path not in existing]
    if not missing:
        return

    message = "The following source_path values are not present in rag_cards:\n" + "\n".join(
        f"- {path}" for path in missing
    )

    if fail_on_missing:
        raise RuntimeError(message)

    print("\n[WARNING] " + message)


def filter_dependency_rows(
    *,
    dependency_rows: list[DependencyRow],
    known_registry_ids: set[str],
    fail_missing_targets: bool,
) -> list[DependencyRow]:
    result: list[DependencyRow] = []
    missing_messages: list[str] = []

    for row in dependency_rows:
        if row.to_canonical_id in known_registry_ids:
            result.append(row)
            continue

        missing_messages.append(
            f"{row.from_canonical_id} --{row.edge_type}--> {row.to_canonical_id}"
        )

    if missing_messages:
        message = "Dependency target(s) missing from rag_card_registry:\n" + "\n".join(
            f"- {item}" for item in missing_messages
        )
        if fail_missing_targets:
            raise RuntimeError(message)
        print("\n[WARNING] Skipping missing dependency targets:\n" + "\n".join(f"- {x}" for x in missing_messages))

    return result


def upsert_registry_rows(supabase: Client, rows: list[RegistryRow], *, batch_size: int) -> None:
    if not rows:
        return
    print(f"\n[WRITE] Upserting {len(rows)} rag_card_registry rows")
    for batch in chunks([row.to_db_row() for row in rows], batch_size):
        supabase.table("rag_card_registry").upsert(
            batch,
            on_conflict="canonical_id",
        ).execute()


def upsert_alias_rows(supabase: Client, rows: list[AliasRow], *, batch_size: int) -> None:
    if not rows:
        return
    print(f"[WRITE] Upserting {len(rows)} rag_card_aliases rows")
    for batch in chunks([row.to_db_row() for row in rows], batch_size):
        supabase.table("rag_card_aliases").upsert(
            batch,
            on_conflict="canonical_id,alias_text",
        ).execute()


def upsert_dependency_rows(supabase: Client, rows: list[DependencyRow], *, batch_size: int) -> None:
    if not rows:
        print("[WRITE] No rag_card_dependencies rows to upsert")
        return
    print(f"[WRITE] Upserting {len(rows)} rag_card_dependencies rows")
    for batch in chunks([row.to_db_row() for row in rows], batch_size):
        supabase.table("rag_card_dependencies").upsert(
            batch,
            on_conflict="from_canonical_id,to_canonical_id,edge_type",
        ).execute()


# ============================================================
# Printing / validation
# ============================================================


def print_plan(plan: SyncPlan, *, verbose: bool) -> None:
    print("\n=== Registry Graph Sync Plan ===")
    print(f"Cards parsed:        {len(plan.cards)}")
    print(f"Registry rows:       {len(plan.registry_rows)}")
    print(f"Alias rows:          {len(plan.alias_rows)}")
    print(f"Dependency rows:     {len(plan.dependency_rows)}")
    print(f"Warnings:            {len(plan.warnings)}")
    print(f"Errors:              {len(plan.errors)}")

    if plan.warnings:
        print("\n--- Warnings ---")
        for warning in plan.warnings:
            print(f"- {warning}")

    if plan.errors:
        print("\n--- Errors ---")
        for error in plan.errors:
            print(f"- {error}")

    print("\n--- Registry rows ---")
    for row in plan.registry_rows:
        print(
            f"- {row.canonical_id} | {row.title} | {row.concept_type} | "
            f"{row.card_bucket} | {row.source_path} | active={row.is_active}"
        )

    print("\n--- Alias counts ---")
    alias_counts: dict[str, int] = {}
    for row in plan.alias_rows:
        alias_counts[row.canonical_id] = alias_counts.get(row.canonical_id, 0) + 1
    for canonical_id in sorted(alias_counts):
        print(f"- {canonical_id}: {alias_counts[canonical_id]}")

    print("\n--- Dependency edges ---")
    if not plan.dependency_rows:
        print("(none)")
    else:
        for row in plan.dependency_rows:
            print(
                f"- {row.from_canonical_id} --{row.edge_type}--> {row.to_canonical_id} "
                f"| priority={row.priority}"
            )

    if verbose:
        print("\n--- Alias rows ---")
        for row in plan.alias_rows:
            print(
                f"- {row.canonical_id} | {row.alias_text!r} | {row.alias_type} | "
                f"weight={row.weight:.2f}"
            )


def validate_duplicate_source_paths(rows: list[RegistryRow]) -> list[str]:
    seen: dict[str, str] = {}
    warnings: list[str] = []
    for row in rows:
        previous = seen.get(row.source_path)
        if previous and previous != row.canonical_id:
            warnings.append(
                f"source_path {row.source_path!r} used by both {previous} and {row.canonical_id}"
            )
        seen[row.source_path] = row.canonical_id
    return warnings


def validate_duplicate_canonical_ids(rows: list[RegistryRow]) -> list[str]:
    seen: dict[str, str] = {}
    warnings: list[str] = []
    for row in rows:
        previous = seen.get(row.canonical_id)
        if previous and previous != row.source_path:
            warnings.append(
                f"canonical_id {row.canonical_id!r} appears in both {previous} and {row.source_path}"
            )
        seen[row.canonical_id] = row.source_path
    return warnings


# ============================================================
# Helpers
# ============================================================


class CardValidationError(ValueError):
    pass


def make_source_path(path: Path, knowledge_dir: Path, *, source_prefix: str) -> str:
    relative = path.relative_to(knowledge_dir).as_posix()
    prefix = source_prefix.strip().replace("\\", "/").strip("/")
    if not prefix:
        return relative
    return f"{prefix}/{relative}"


def first_heading(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return ""


def title_from_source_path(source_path: str) -> str:
    return Path(source_path).stem.replace("_", " ").replace("-", " ").title()


def derive_canonical_id(source_path: str, concept_type: str, card_bucket: str) -> str:
    prefix = concept_type or BUCKET_TO_TYPE.get(card_bucket, "reference")
    return f"{prefix}.{slugify(Path(source_path).stem)}"


def derive_type(canonical_id: str, card_bucket: str) -> str:
    if "." in canonical_id:
        return canonical_id.split(".", 1)[0]
    return BUCKET_TO_TYPE.get(card_bucket, "reference")


def derive_bucket(source_path: str) -> str:
    first = source_path.split("/", 1)[0]
    return first if first in VALID_BUCKETS else "references"


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_identifier_value(value: str) -> str:
    return clean_text(value).lower().replace("-", "_")


def normalize_canonical_id(value: Any) -> str:
    text = clean_text(value).lower().replace("-", "_")
    text = re.sub(r"\s+", "_", text)
    return text


def normalize_alias_text(value: Any) -> str:
    text = clean_text(value)
    return re.sub(r"\s+", " ", text)


def infer_alias_type(alias_text: str) -> str:
    compact = alias_text.replace(".", "").replace("_", "").replace("-", "")
    if compact.isupper() and 1 <= len(compact) <= 8:
        return "abbreviation"
    return "phrase"


def default_alias_weight(alias_type: str) -> float:
    alias_type = normalize_identifier_value(alias_type)
    if alias_type in {"exact", "abbreviation"}:
        return 1.0
    if alias_type == "synonym":
        return 0.9
    if alias_type == "phrase":
        return 0.85
    return 0.65


def parse_weight(value: Any, *, default: float) -> float:
    try:
        parsed = float(value)
    except Exception:
        parsed = default
    return max(0.0, min(1.0, parsed))


def parse_int(value: Any, *, default: int) -> int:
    try:
        return int(value)
    except Exception:
        return default


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def slugify(value: str) -> str:
    text = clean_text(value).lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")


def dedupe_registry_rows(rows: Sequence[RegistryRow]) -> list[RegistryRow]:
    result: dict[str, RegistryRow] = {}
    for row in rows:
        result[row.canonical_id] = row
    return list(result.values())


def dedupe_alias_rows(rows: Sequence[AliasRow]) -> list[AliasRow]:
    result: dict[tuple[str, str], AliasRow] = {}
    for row in rows:
        key = (row.canonical_id, row.alias_text.lower())
        current = result.get(key)
        if current is None or row.weight > current.weight:
            result[key] = row
    return list(result.values())


def dedupe_dependency_rows(rows: Sequence[DependencyRow]) -> list[DependencyRow]:
    result: dict[tuple[str, str, str], DependencyRow] = {}
    for row in rows:
        key = (row.from_canonical_id, row.to_canonical_id, row.edge_type)
        current = result.get(key)
        if current is None or row.priority < current.priority:
            result[key] = row
    return list(result.values())


def chunks(values: Sequence[Any], size: int) -> Iterable[list[Any]]:
    for start in range(0, len(values), size):
        yield list(values[start : start + size])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        raise SystemExit(130)
