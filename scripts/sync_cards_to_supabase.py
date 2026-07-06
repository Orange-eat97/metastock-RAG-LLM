"""
sync_cards_to_supabase.py

Purpose:
    Sync local MetaStock markdown knowledge cards into Supabase.

Cache behavior:
    1. If card exists and card content_hash is unchanged, skip card upsert.
    2. If card exists and card content_hash changed, replace the stored card.
    3. If card does not exist, upload the card.
    4. If embedding exists and embedding content_hash is unchanged, skip embedding.
    5. If embedding is missing or outdated, generate and upsert latest embedding.

Expects compact Supabase tables, with these mandatory fields:

rag_cards
row = {
    "card_id": card.card_id,
    "card_type": card.card_type,
    "card_bucket": card.card_bucket,
    "title": card.title,
    "category": card.category,
    "source": card.source,
    "priority": card.priority,
    "status": card.status,
    "source_path": card.source_path,
    "frontmatter": card.frontmatter,
    "body_markdown": card.body_markdown,
    "plain_text": card.plain_text,
    "structured_json": build_structured_json(card),
    "content_hash": card.content_hash,
    "top_folder": card.source_path.split("/")[0] if "/" in card.source_path else None,
    "file_stem": Path(card.source_path).stem if card.source_path else None,
}

rag_card_embeddings
row = {
    "card_id": card.card_id,
    "embedding_model": embedding_model,
    "embedding": embedding,
    "embedded_text": card.canonical_text,
    "content_hash": card.content_hash,
}

Recommended command:
    python scripts/sync_cards_to_supabase.py --knowledge-dir knowledge_base

Optional:
    python scripts/sync_cards_to_supabase.py --knowledge-dir knowledge_base --no-embed
    python scripts/sync_cards_to_supabase.py --knowledge-dir knowledge_base --force-embed
    python scripts/sync_cards_to_supabase.py --knowledge-dir knowledge_base --dry-run
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from supabase import Client, create_client


# ============================================================
# Data model
# ============================================================

@dataclass
class ParsedCard:
    card_id: str
    title: str
    source_file: str
    source_path: str

    frontmatter: dict[str, Any]
    body_markdown: str
    plain_text: str
    sections: dict[str, str]

    card_type: str
    card_bucket: str
    category: str | None
    function_name: str | None
    template_name: str | None
    source: str | None
    priority: str | None
    status: str | None

    retrieval_keywords: list[str]
    natural_language_mappings: list[str]
    related_functions: list[str]

    canonical_text: str
    content_hash: str


# ============================================================
# General helpers
# ============================================================

def load_env() -> None:
    load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def make_supabase_client() -> Client:
    url = get_required_env("SUPABASE_URL")
    key = get_required_env("SUPABASE_SERVICE_ROLE_KEY")
    return create_client(url, key)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def optional_str(value: Any) -> str | None:
    if value is None:
        return None
    cleaned = str(value).strip()
    return cleaned if cleaned else None


def dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []

    for item in items:
        cleaned = normalize_whitespace(str(item))
        if not cleaned:
            continue

        key = cleaned.lower()
        if key not in seen:
            seen.add(key)
            output.append(cleaned)

    return output


# ============================================================
# Markdown parsing
# ============================================================

def split_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    """
    Parses YAML frontmatter like:

    ---
    type: function
    function: Cross
    category: crossover
    ---

    Returns:
        (frontmatter_dict, markdown_body)
    """
    raw = raw.lstrip("\ufeff")

    if not raw.startswith("---"):
        return {}, raw.strip()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, flags=re.DOTALL)
    if not match:
        raise ValueError(
            "Markdown file appears to start with frontmatter but could not be parsed."
        )

    frontmatter_raw = match.group(1)
    body = match.group(2)

    parsed = yaml.safe_load(frontmatter_raw) or {}
    if not isinstance(parsed, dict):
        raise ValueError("YAML frontmatter must parse into a dictionary.")

    return parsed, body.strip()


def extract_title(body_markdown: str, file_path: Path) -> str:
    """
    Uses first H1 as title. Falls back to filename stem.
    """
    for line in body_markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()

    return file_path.stem.replace("_", " ").replace("-", " ").title()


def parse_markdown_sections(body_markdown: str) -> dict[str, str]:
    """
    Parses markdown sections by headings.

    Example:
        ## Purpose
        ...
        ## Syntax
        ...

    Returns:
        {
          "Purpose": "...",
          "Syntax": "..."
        }
    """
    sections: dict[str, list[str]] = {}
    current_heading = "Body"
    sections[current_heading] = []

    for line in body_markdown.splitlines():
        heading_match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading_match:
            current_heading = heading_match.group(2).strip()
            sections.setdefault(current_heading, [])
        else:
            sections.setdefault(current_heading, []).append(line)

    return {
        heading: "\n".join(lines).strip()
        for heading, lines in sections.items()
        if "\n".join(lines).strip()
    }


def markdown_to_plain_text(markdown: str) -> str:
    """
    Lightweight markdown-to-text conversion for retrieval text.
    Keeps formula content mostly intact.
    """
    text = markdown

    # Remove fenced code markers but keep code content.
    text = re.sub(r"```[a-zA-Z0-9_-]*", "", text)
    text = text.replace("```", "")

    # Remove markdown heading markers.
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)

    # Remove bold/italic markers.
    text = text.replace("**", "").replace("__", "")
    text = text.replace("*", "").replace("_", "_")

    # Convert markdown links [text](url) -> text.
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    return normalize_whitespace(text)


def extract_list_items(section_text: str) -> list[str]:
    """
    Extract bullet/list-ish items from a section.

    Handles:
        - item
        * item
        item, item, item
        one item per line
    """
    if not section_text:
        return []

    items: list[str] = []

    for raw_line in section_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        line = re.sub(r"^[-*]\s+", "", line).strip()
        line = re.sub(r"^\d+\.\s+", "", line).strip()

        # Skip code fence markers.
        if line.startswith("```"):
            continue

        # If the line is comma-separated keywords, split it.
        if "," in line and len(line) < 300:
            parts = [part.strip() for part in line.split(",") if part.strip()]
            items.extend(parts)
        else:
            items.append(line)

    return dedupe_preserve_order(items)


def section_lookup(sections: dict[str, str], possible_names: list[str]) -> str:
    """
    Case-insensitive lookup for known section headings.
    """
    normalized = {slugify(k): v for k, v in sections.items()}

    for name in possible_names:
        key = slugify(name)
        if key in normalized:
            return normalized[key]

    return ""


def extract_retrieval_keywords(sections: dict[str, str]) -> list[str]:
    text = section_lookup(
        sections,
        [
            "Retrieval keywords",
            "Keywords",
            "Search keywords",
        ],
    )
    return extract_list_items(text)


def extract_natural_language_mappings(sections: dict[str, str]) -> list[str]:
    text = section_lookup(
        sections,
        [
            "Natural language mappings",
            "Natural language triggers",
            "Natural language",
            "User request mappings",
            "Mappings",
        ],
    )
    return extract_list_items(text)


def extract_related_functions(
    sections: dict[str, str],
    frontmatter: dict[str, Any],
) -> list[str]:
    related_from_frontmatter = (
        frontmatter.get("related_functions")
        or frontmatter.get("functions")
        or frontmatter.get("required_functions")
    )

    items: list[str] = []

    if isinstance(related_from_frontmatter, list):
        items.extend(str(x).strip() for x in related_from_frontmatter if str(x).strip())
    elif isinstance(related_from_frontmatter, str):
        items.extend(extract_list_items(related_from_frontmatter))

    related_text = section_lookup(
        sections,
        [
            "Related functions and concepts",
            "Related functions",
            "Required function cards",
            "Related concepts",
        ],
    )
    items.extend(extract_list_items(related_text))

    # Try extracting "Cross: crossover detection" -> "Cross"
    cleaned: list[str] = []
    for item in items:
        if ":" in item and len(item.split(":")[0]) <= 40:
            cleaned.append(item.split(":")[0].strip())
        else:
            cleaned.append(item.strip())

    return dedupe_preserve_order(cleaned)


# ============================================================
# Card identity and canonical text
# ============================================================

def infer_card_id(
    file_path: Path,
    knowledge_dir: Path,
    frontmatter: dict[str, Any],
    title: str,
) -> str:
    """
    Stable card_id rules:

    function card:
        function.cross

    template card:
        template.explorer_basic

    reference card:
        reference.price_fields

    pattern card:
        pattern.breakout
        pattern.volume_above_average

    fallback:
        relative.path.without.extension
    """
    card_type = str(frontmatter.get("type") or "").strip().lower()

    function_name = frontmatter.get("function")
    template_name = frontmatter.get("template")
    category = frontmatter.get("category")

    if card_type == "function" and function_name:
        return f"function.{slugify(str(function_name))}"

    if card_type == "template" and template_name:
        return f"template.{slugify(str(template_name))}"

    if card_type == "reference" and category:
        return f"reference.{slugify(str(category))}"

    if card_type == "pattern":
        relative = file_path.relative_to(knowledge_dir).with_suffix("")
        return f"pattern.{slugify(relative.stem)}"

    if card_type == "example":
        return f"example.{slugify(title)}"

    relative = file_path.relative_to(knowledge_dir).with_suffix("")
    return slugify(".".join(relative.parts))


def infer_card_bucket(
    file_path: Path,
    knowledge_dir: Path,
    frontmatter: dict[str, Any],
) -> str:
    """
    Maps cards into retrieval buckets.

    These bucket names should match context_builder.py bucket_plan:
        functions
        patterns
        references
        templates
    """
    explicit_bucket = frontmatter.get("card_bucket") or frontmatter.get("bucket")
    if explicit_bucket:
        return str(explicit_bucket).strip().lower()

    card_type = str(frontmatter.get("type") or "").strip().lower()

    if card_type == "function":
        return "functions"

    if card_type == "pattern":
        return "patterns"

    if card_type == "reference":
        return "references"

    if card_type == "template":
        return "templates"

    # Fallback to first folder name.
    try:
        relative = file_path.relative_to(knowledge_dir)
        if len(relative.parts) > 1:
            return slugify(relative.parts[0])
    except Exception:
        pass

    return "unknown"


def build_structured_json(card: ParsedCard) -> dict[str, Any]:
    """
    Not uploaded in compact schema yet.
    Kept for future iterations or debugging.
    """
    return {
        "title": card.title,
        "sections": card.sections,
        "retrieval": {
            "keywords": card.retrieval_keywords,
            "natural_language_mappings": card.natural_language_mappings,
            "related_functions": card.related_functions,
        },
        "metadata": {
            "card_type": card.card_type,
            "card_bucket": card.card_bucket,
            "category": card.category,
            "function_name": card.function_name,
            "template_name": card.template_name,
            "source": card.source,
            "priority": card.priority,
            "status": card.status,
        },
    }


def build_canonical_text(
    title: str,
    frontmatter: dict[str, Any],
    sections: dict[str, str],
    plain_text: str,
    retrieval_keywords: list[str],
    natural_language_mappings: list[str],
    related_functions: list[str],
    card_bucket: str,
) -> str:
    """
    This is the exact text that gets embedded.

    Design principle:
        Include metadata + title + important mappings + full body.
        This makes retrieval work for both exact syntax and natural language.
    """
    lines: list[str] = []

    lines.append(f"Title: {title}")

    card_type = frontmatter.get("type")
    category = frontmatter.get("category")
    function_name = frontmatter.get("function")
    template_name = frontmatter.get("template")
    source = frontmatter.get("source")
    priority = frontmatter.get("priority")
    status = frontmatter.get("status")

    if card_type:
        lines.append(f"Type: {card_type}")
    if card_bucket:
        lines.append(f"Bucket: {card_bucket}")
    if category:
        lines.append(f"Category: {category}")
    if function_name:
        lines.append(f"Function: {function_name}")
    if template_name:
        lines.append(f"Template: {template_name}")
    if source:
        lines.append(f"Source: {source}")
    if priority:
        lines.append(f"Priority: {priority}")
    if status:
        lines.append(f"Status: {status}")

    if natural_language_mappings:
        lines.append("Natural language mappings:")
        for item in natural_language_mappings:
            lines.append(f"- {item}")

    if retrieval_keywords:
        lines.append("Retrieval keywords:")
        for item in retrieval_keywords:
            lines.append(f"- {item}")

    if related_functions:
        lines.append("Related functions and concepts:")
        for item in related_functions:
            lines.append(f"- {item}")

    # Prefer important sections in a stable order, then include full plain text.
    important_section_names = [
        # Existing function/template/reference sections
        "Purpose",
        "Syntax",
        "Meaning",
        "Common formulas",
        "Formula mappings",
        "Explorer examples",
        "Explorer column usage",
        "Output rules",
        "Rules for column references",
        "Important Explorer limitation",
        "What not to do",
        "Assumptions",
        "Pitfalls",

        # Pattern-card sections
        "Intent",
        "Natural Language Triggers",
        "Keywords",
        "Required Logical Components",
        "Optional Confirmation Components",
        "Formula Building Blocks",
        "Composition Guidance",
        "Example Compositions",
        "Observable Outputs",
        "Default Assumptions",
    ]

    for section_name in important_section_names:
        section_text = section_lookup(sections, [section_name])
        if section_text:
            lines.append(f"{section_name}:")
            lines.append(markdown_to_plain_text(section_text))

    lines.append("Full card text:")
    lines.append(plain_text)

    return "\n".join(line for line in lines if str(line).strip()).strip()


def parse_card(file_path: Path, knowledge_dir: Path) -> ParsedCard:
    raw = file_path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(raw)

    title = extract_title(body, file_path)
    sections = parse_markdown_sections(body)
    plain_text = markdown_to_plain_text(body)

    retrieval_keywords = extract_retrieval_keywords(sections)
    natural_language_mappings = extract_natural_language_mappings(sections)
    related_functions = extract_related_functions(sections, frontmatter)

    card_id = infer_card_id(file_path, knowledge_dir, frontmatter, title)
    card_bucket = infer_card_bucket(file_path, knowledge_dir, frontmatter)

    canonical_text = build_canonical_text(
        title=title,
        frontmatter=frontmatter,
        sections=sections,
        plain_text=plain_text,
        retrieval_keywords=retrieval_keywords,
        natural_language_mappings=natural_language_mappings,
        related_functions=related_functions,
        card_bucket=card_bucket,
    )

    content_hash = sha256_text(canonical_text)

    return ParsedCard(
        card_id=card_id,
        title=title,
        source_file=file_path.name,
        source_path=str(file_path.relative_to(knowledge_dir)).replace("\\", "/"),

        frontmatter=frontmatter,
        body_markdown=body,
        plain_text=plain_text,
        sections=sections,

        card_type=str(frontmatter.get("type") or "unknown").strip().lower(),
        card_bucket=card_bucket,
        category=optional_str(frontmatter.get("category")),
        function_name=optional_str(frontmatter.get("function")),
        template_name=optional_str(frontmatter.get("template")),
        source=optional_str(frontmatter.get("source")),
        priority=optional_str(frontmatter.get("priority")),
        status=optional_str(frontmatter.get("status")),

        retrieval_keywords=retrieval_keywords,
        natural_language_mappings=natural_language_mappings,
        related_functions=related_functions,

        canonical_text=canonical_text,
        content_hash=content_hash,
    )


# ============================================================
# Embeddings
# ============================================================

class Embedder:
    def __init__(self) -> None:
        provider = os.getenv("EMBEDDING_PROVIDER", "sbert").strip().lower()
        self.provider = provider

        if provider == "none":
            self.model_name = "none"
            self.model = None
            return

        if provider == "sbert":
            from sentence_transformers import SentenceTransformer

            self.model_name = os.getenv(
                "SBERT_MODEL",
                "sentence-transformers/all-MiniLM-L6-v2",
            )
            self.model = SentenceTransformer(self.model_name)
            return

        if provider == "openai":
            from openai import OpenAI

            self.model_name = os.getenv(
                "OPENAI_EMBEDDING_MODEL",
                "text-embedding-3-small",
            )
            self.model = OpenAI(api_key=get_required_env("OPENAI_API_KEY"))
            return

        raise ValueError(
            f"Unsupported EMBEDDING_PROVIDER={provider!r}. "
            "Use one of: sbert, openai, none."
        )

    def embed(self, text: str) -> list[float]:
        if self.provider == "none":
            raise RuntimeError("Embedding provider is set to none.")

        if self.provider == "sbert":
            assert self.model is not None
            vector = self.model.encode(text, normalize_embeddings=True)
            return [float(x) for x in vector.tolist()]

        if self.provider == "openai":
            assert self.model is not None
            response = self.model.embeddings.create(
                model=self.model_name,
                input=text,
            )
            return [float(x) for x in response.data[0].embedding]

        raise RuntimeError(f"Unsupported provider: {self.provider}")

    @property
    def embedding_model_name(self) -> str:
        # Prefer explicit EMBEDDING_MODEL only if you already use it elsewhere.
        # Otherwise use the actual model name.
        return os.getenv("EMBEDDING_MODEL", self.model_name)


# ============================================================
# Supabase cache checks
# ============================================================

def existing_card_hash(
    supabase: Client,
    card_id: str,
) -> str | None:
    response = (
        supabase.table("rag_cards")
        .select("content_hash")
        .eq("card_id", card_id)
        .limit(1)
        .execute()
    )

    rows = response.data or []
    if not rows:
        return None

    return rows[0].get("content_hash")


def existing_embedding_hash(
    supabase: Client,
    card_id: str,
    embedding_model: str,
) -> str | None:
    response = (
        supabase.table("rag_card_embeddings")
        .select("content_hash")
        .eq("card_id", card_id)
        .eq("embedding_model", embedding_model)
        .limit(1)
        .execute()
    )

    rows = response.data or []
    if not rows:
        return None

    return rows[0].get("content_hash")


# ============================================================
# Supabase upsert
# ============================================================

def upsert_card(supabase: Client, card: ParsedCard, dry_run: bool = False) -> None:
    row = {
        "card_id": card.card_id,
        "card_type": card.card_type,
        "card_bucket": card.card_bucket,

        "title": card.title,
        "category": card.category,
        "source": card.source,
        "priority": card.priority,
        "status": card.status,

        "source_path": card.source_path,
        "frontmatter": card.frontmatter,
        "body_markdown": card.body_markdown,
        "plain_text": card.plain_text,
        "structured_json": build_structured_json(card),

        "content_hash": card.content_hash,

        "top_folder": card.source_path.split("/")[0] if "/" in card.source_path else None,
        "file_stem": Path(card.source_path).stem if card.source_path else None,
    }

    if dry_run:
        print("[DRY RUN] Would upsert rag_cards row:")
        print(json.dumps(row, indent=2, ensure_ascii=False)[:4000])
        return

    supabase.table("rag_cards").upsert(
        row,
        on_conflict="card_id",
    ).execute()

def upsert_embedding(
    supabase: Client,
    card: ParsedCard,
    embedder: Embedder,
    dry_run: bool = False,
) -> None:
    embedding_model = embedder.embedding_model_name

    print(f"  embedding card: {card.card_id}")
    embedding = embedder.embed(card.canonical_text)

    row = {
        "card_id": card.card_id,
        "embedding_model": embedding_model,
        "embedding": embedding,
        "embedded_text": card.canonical_text,
        "content_hash": card.content_hash,
    }

    if dry_run:
        print("[DRY RUN] Would upsert rag_card_embeddings row:")
        preview = dict(row)
        preview["embedding"] = f"<{len(embedding)} floats>"
        preview["embedded_text"] = preview["embedded_text"][:1000] + "..."
        print(json.dumps(preview, indent=2, ensure_ascii=False)[:4000])
        return

    supabase.table("rag_card_embeddings").upsert(
        row,
        on_conflict="card_id,embedding_model",
    ).execute()


# ============================================================
# Sync flow
# ============================================================

def iter_markdown_files(knowledge_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in knowledge_dir.rglob("*.md")
        if path.is_file()
    )


def sync_cards(
    knowledge_dir: Path,
    embed: bool,
    force_embed: bool,
    dry_run: bool,
) -> None:
    if not knowledge_dir.exists():
        raise RuntimeError(f"Knowledge directory does not exist: {knowledge_dir}")

    supabase = None if dry_run else make_supabase_client()
    embedder = Embedder() if embed else None

    md_files = iter_markdown_files(knowledge_dir)
    print(f"Found {len(md_files)} markdown card(s) under {knowledge_dir}")

    parsed_count = 0
    card_upsert_count = 0
    embedding_upsert_count = 0
    fully_cached_count = 0
    failed: list[tuple[str, str]] = []

    for file_path in md_files:
        print(f"\nProcessing: {file_path}")

        try:
            card = parse_card(file_path, knowledge_dir)
            parsed_count += 1

            print(f"  card_id: {card.card_id}")
            print(f"  type: {card.card_type}")
            print(f"  bucket: {card.card_bucket}")
            print(f"  title: {card.title}")
            print(f"  hash: {card.content_hash[:12]}...")

            card_needs_upsert = True
            embedding_needs_upsert = embed

            if dry_run:
                print("  cache check skipped in dry-run")
            else:
                assert supabase is not None

                old_card_hash = existing_card_hash(
                    supabase=supabase,
                    card_id=card.card_id,
                )

                if old_card_hash == card.content_hash:
                    card_needs_upsert = False
                    print("  card unchanged; skipping card upsert")
                elif old_card_hash is None:
                    print("  card not found in Supabase; will insert card")
                else:
                    print("  card changed; will replace stored card")

                if embed:
                    assert embedder is not None

                    old_embedding_hash = existing_embedding_hash(
                        supabase=supabase,
                        card_id=card.card_id,
                        embedding_model=embedder.embedding_model_name,
                    )

                    if force_embed:
                        embedding_needs_upsert = True
                        print("  force_embed=True; will regenerate embedding")
                    elif old_embedding_hash == card.content_hash:
                        embedding_needs_upsert = False
                        print("  embedding unchanged; skipping embedding")
                    elif old_embedding_hash is None:
                        embedding_needs_upsert = True
                        print("  embedding not found; will create embedding")
                    else:
                        embedding_needs_upsert = True
                        print("  embedding outdated; will replace embedding")

            if card_needs_upsert:
                if dry_run:
                    upsert_card(None, card, dry_run=True)  # type: ignore[arg-type]
                else:
                    assert supabase is not None
                    upsert_card(supabase, card, dry_run=False)

                card_upsert_count += 1

            if embed and embedding_needs_upsert:
                assert embedder is not None

                if dry_run:
                    upsert_embedding(
                        supabase=None,  # type: ignore[arg-type]
                        card=card,
                        embedder=embedder,
                        dry_run=True,
                    )
                else:
                    assert supabase is not None
                    upsert_embedding(
                        supabase=supabase,
                        card=card,
                        embedder=embedder,
                        dry_run=False,
                    )

                embedding_upsert_count += 1

            if not card_needs_upsert and not embedding_needs_upsert:
                fully_cached_count += 1
                print("  fully cached; no upload needed")

        except Exception as exc:
            failed.append((str(file_path), str(exc)))
            print(f"  ERROR: {exc}")

    print("\n=== Sync summary ===")
    print(f"Parsed:             {parsed_count}")
    print(f"Card upserts:       {card_upsert_count}")
    print(f"Embedding upserts:  {embedding_upsert_count}")
    print(f"Fully cached:       {fully_cached_count}")
    print(f"Failed:             {len(failed)}")

    if failed:
        print("\nFailures:")
        for path, error in failed:
            print(f"- {path}: {error}")

        raise SystemExit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync MetaStock markdown knowledge cards to Supabase."
    )

    parser.add_argument(
        "--knowledge-dir",
        default=os.getenv("KNOWLEDGE_DIR", "knowledge_base"),
        help="Path to local knowledge_base directory.",
    )

    parser.add_argument(
        "--no-embed",
        action="store_true",
        help="Only upsert rag_cards. Do not generate/upsert embeddings.",
    )

    parser.add_argument(
        "--force-embed",
        action="store_true",
        help="Regenerate embeddings even if content_hash is unchanged.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and print rows without writing to Supabase.",
    )

    return parser.parse_args()


def main() -> None:
    load_env()
    args = parse_args()

    knowledge_dir = Path(args.knowledge_dir).resolve()

    sync_cards(
        knowledge_dir=knowledge_dir,
        embed=not args.no_embed,
        force_embed=args.force_embed,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()