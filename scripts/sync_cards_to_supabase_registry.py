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

Registry workflow:
    The script can also sync graph-registry metadata into:
        rag_card_registry
        rag_card_aliases
        rag_card_dependencies

    Registry data comes from card frontmatter and parsed card sections:
        aliases / registry.aliases
        requires / suggests / forbids / conflicts_with / similar_to / expands_to
        dependencies
        registry.properties

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
# Registry / knowledge graph sync
# ============================================================

REGISTRY_CONCEPT_TYPE_BY_CARD_TYPE = {
    "function": "function",
    "pattern": "pattern",
    "reference": "reference",
    "template": "explorer_rule",
    "example": "example",
    "pitfall": "pitfall",
    "field": "field",
}

REGISTRY_DEFAULT_PRIORITY_BY_CONCEPT_TYPE = {
    "explorer_rule": 5,
    "reference": 5,
    "pattern": 10,
    "function": 20,
    "field": 20,
    "example": 60,
    "pitfall": 80,
}

ALLOWED_ALIAS_TYPES = {
    "exact",
    "synonym",
    "phrase",
    "abbreviation",
    "weak_hint",
}

ALLOWED_EDGE_TYPES = {
    "requires",
    "suggests",
    "conflicts_with",
    "forbids",
    "similar_to",
    "expands_to",
}


def as_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default

    if isinstance(value, bool):
        return value

    text = str(value).strip().lower()

    if text in {"true", "1", "yes", "y", "on"}:
        return True

    if text in {"false", "0", "no", "n", "off"}:
        return False

    return default


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, str):
        return extract_list_items(value)

    return [value]


def parse_int(value: Any, default: int) -> int:
    if value is None:
        return default

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def normalize_concept_type(card_type: str) -> str:
    return REGISTRY_CONCEPT_TYPE_BY_CARD_TYPE.get(card_type, "reference")


def registry_config(card: ParsedCard) -> dict[str, Any]:
    raw = card.frontmatter.get("registry") or {}
    if isinstance(raw, dict):
        return raw
    return {}


def registry_enabled(card: ParsedCard) -> bool:
    cfg = registry_config(card)
    return as_bool(cfg.get("enabled"), default=True)


def registry_canonical_id(card: ParsedCard) -> str:
    cfg = registry_config(card)
    explicit = cfg.get("canonical_id") or card.frontmatter.get("canonical_id")
    if explicit:
        return str(explicit).strip()
    return card.card_id


def registry_supports_explorer(card: ParsedCard) -> bool:
    cfg = registry_config(card)
    if "supports_explorer" in cfg:
        return as_bool(cfg.get("supports_explorer"), default=True)
    if "supports_explorer" in card.frontmatter:
        return as_bool(card.frontmatter.get("supports_explorer"), default=True)
    return card.card_type not in {"pitfall"}


def registry_priority(card: ParsedCard, concept_type: str) -> int:
    cfg = registry_config(card)
    default = REGISTRY_DEFAULT_PRIORITY_BY_CONCEPT_TYPE.get(concept_type, 100)
    return parse_int(
        cfg.get("priority", card.frontmatter.get("priority", card.priority)),
        default=default,
    )


def registry_graph_labels(card: ParsedCard, concept_type: str, supports_explorer: bool) -> list[str]:
    cfg = registry_config(card)
    explicit = cfg.get("graph_labels") or card.frontmatter.get("graph_labels")

    if explicit:
        return [str(item).strip() for item in as_list(explicit) if str(item).strip()]

    labels = ["Concept"]

    label_by_type = {
        "function": "Function",
        "pattern": "Pattern",
        "field": "Field",
        "explorer_rule": "ExplorerRule",
        "reference": "Reference",
        "example": "Example",
        "pitfall": "Pitfall",
    }

    type_label = label_by_type.get(concept_type)
    if type_label:
        labels.append(type_label)

    if supports_explorer:
        labels.append("ExplorerSupported")

    return labels


def registry_properties(card: ParsedCard) -> dict[str, Any]:
    cfg = registry_config(card)

    properties: dict[str, Any] = {
        "source_card_id": card.card_id,
        "source_path": card.source_path,
        "category": card.category,
        "function_name": card.function_name,
        "template_name": card.template_name,
        "status": card.status,
    }

    # Keep only meaningful values.
    properties = {
        key: value
        for key, value in properties.items()
        if value is not None
    }

    frontmatter_properties = card.frontmatter.get("properties")
    if isinstance(frontmatter_properties, dict):
        properties.update(frontmatter_properties)

    registry_properties_raw = cfg.get("properties")
    if isinstance(registry_properties_raw, dict):
        properties.update(registry_properties_raw)

    return properties


def infer_alias_type(alias_text: str, default: str = "phrase") -> str:
    cleaned = alias_text.strip()

    if cleaned.upper() == cleaned and len(cleaned) <= 5 and re.search(r"[A-Z]", cleaned):
        return "abbreviation"

    if len(cleaned.split()) == 1:
        return "exact"

    return default


def normalize_alias_entry(
    entry: Any,
    *,
    default_type: str,
    default_weight: float,
    source: str,
) -> dict[str, Any] | None:
    if isinstance(entry, str):
        alias_text = normalize_whitespace(entry)
        if not alias_text:
            return None

        return {
            "alias_text": alias_text,
            "alias_type": infer_alias_type(alias_text, default=default_type),
            "weight": default_weight,
            "source": source,
            "properties": {},
        }

    if isinstance(entry, dict):
        alias_text = normalize_whitespace(
            str(entry.get("text") or entry.get("alias") or entry.get("alias_text") or "")
        )
        if not alias_text:
            return None

        alias_type = str(entry.get("type") or entry.get("alias_type") or infer_alias_type(alias_text, default_type)).strip()
        if alias_type not in ALLOWED_ALIAS_TYPES:
            alias_type = default_type

        return {
            "alias_text": alias_text,
            "alias_type": alias_type,
            "weight": float(entry.get("weight", default_weight)),
            "source": str(entry.get("source") or source),
            "properties": entry.get("properties") if isinstance(entry.get("properties"), dict) else {},
        }

    return None


def build_registry_alias_rows(card: ParsedCard) -> list[dict[str, Any]]:
    canonical_id = registry_canonical_id(card)
    cfg = registry_config(card)

    raw_aliases: list[tuple[Any, str, float, str]] = []

    # Always include the card title as a direct alias.
    raw_aliases.append((card.title, "exact", 1.0, "card_title"))

    if card.function_name:
        raw_aliases.append((card.function_name, "exact", 1.0, "frontmatter_function"))

    if card.template_name:
        raw_aliases.append((card.template_name, "exact", 1.0, "frontmatter_template"))

    for key in ["aliases", "alias"]:
        for item in as_list(card.frontmatter.get(key)):
            raw_aliases.append((item, "phrase", 1.0, "frontmatter"))

    for item in as_list(cfg.get("aliases")):
        raw_aliases.append((item, "phrase", 1.0, "registry_frontmatter"))

    # Section-derived natural language mappings are strong retrieval aliases.
    for item in card.natural_language_mappings:
        raw_aliases.append((item, "phrase", 0.9, "card_section"))

    # Retrieval keywords can be broad, so keep them weaker.
    for item in card.retrieval_keywords:
        raw_aliases.append((item, "weak_hint", 0.6, "card_section"))

    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for entry, default_type, default_weight, source in raw_aliases:
        normalized = normalize_alias_entry(
            entry,
            default_type=default_type,
            default_weight=default_weight,
            source=source,
        )
        if normalized is None:
            continue

        key = (canonical_id, normalized["alias_text"].strip().lower())
        if key in seen:
            continue
        seen.add(key)

        rows.append(
            {
                "canonical_id": canonical_id,
                "alias_text": normalized["alias_text"],
                "alias_type": normalized["alias_type"],
                "weight": normalized["weight"],
                "language_code": "en",
                "source": normalized["source"],
                "properties": normalized["properties"],
                "is_active": True,
            }
        )

    return rows


def normalize_dependency_entry(
    entry: Any,
    *,
    from_canonical_id: str,
    edge_type: str,
    default_priority: int,
    default_source: str,
) -> dict[str, Any] | None:
    if isinstance(entry, str):
        to_canonical_id = entry.strip()
        if not to_canonical_id:
            return None

        return {
            "from_canonical_id": from_canonical_id,
            "to_canonical_id": to_canonical_id,
            "edge_type": edge_type,
            "priority": default_priority,
            "rationale": None,
            "properties": {"source": default_source},
            "is_active": True,
        }

    if isinstance(entry, dict):
        to_canonical_id = str(
            entry.get("to")
            or entry.get("target")
            or entry.get("canonical_id")
            or entry.get("to_canonical_id")
            or ""
        ).strip()

        if not to_canonical_id:
            return None

        entry_edge_type = str(entry.get("edge_type") or entry.get("type") or edge_type).strip()
        if entry_edge_type not in ALLOWED_EDGE_TYPES:
            entry_edge_type = edge_type

        properties = entry.get("properties") if isinstance(entry.get("properties"), dict) else {}
        properties = dict(properties)
        properties.setdefault("source", entry.get("source") or default_source)

        return {
            "from_canonical_id": from_canonical_id,
            "to_canonical_id": to_canonical_id,
            "edge_type": entry_edge_type,
            "priority": parse_int(entry.get("priority"), default=default_priority),
            "rationale": optional_str(entry.get("rationale") or entry.get("why")),
            "properties": properties,
            "is_active": as_bool(entry.get("is_active"), default=True),
        }

    return None


def build_registry_dependency_rows(card: ParsedCard) -> list[dict[str, Any]]:
    from_canonical_id = registry_canonical_id(card)
    cfg = registry_config(card)

    rows: list[dict[str, Any]] = []

    edge_defaults = {
        "requires": 10,
        "suggests": 40,
        "conflicts_with": 50,
        "forbids": 50,
        "similar_to": 80,
        "expands_to": 50,
    }

    # Direct edge-type lists in top-level frontmatter or registry block.
    for edge_type, default_priority in edge_defaults.items():
        values: list[Any] = []
        values.extend(as_list(card.frontmatter.get(edge_type)))
        values.extend(as_list(cfg.get(edge_type)))

        for entry in values:
            row = normalize_dependency_entry(
                entry,
                from_canonical_id=from_canonical_id,
                edge_type=edge_type,
                default_priority=default_priority,
                default_source="frontmatter",
            )
            if row is not None:
                rows.append(row)

    # Generic dependency lists.
    generic_dependencies: list[Any] = []
    generic_dependencies.extend(as_list(card.frontmatter.get("dependencies")))
    generic_dependencies.extend(as_list(cfg.get("dependencies")))

    for entry in generic_dependencies:
        row = normalize_dependency_entry(
            entry,
            from_canonical_id=from_canonical_id,
            edge_type="requires",
            default_priority=10,
            default_source="dependencies",
        )
        if row is not None:
            rows.append(row)

    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    for row in rows:
        key = (
            row["from_canonical_id"],
            row["to_canonical_id"],
            row["edge_type"],
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)

    return deduped


def build_registry_node_row(card: ParsedCard) -> dict[str, Any]:
    canonical_id = registry_canonical_id(card)
    concept_type = normalize_concept_type(card.card_type)
    supports_explorer = registry_supports_explorer(card)

    return {
        "canonical_id": canonical_id,
        "concept_type": concept_type,
        "graph_labels": registry_graph_labels(
            card=card,
            concept_type=concept_type,
            supports_explorer=supports_explorer,
        ),
        "source_path": card.source_path,
        "title": card.title,
        "card_bucket": card.card_bucket,
        "supports_explorer": supports_explorer,
        "priority": registry_priority(card, concept_type),
        "properties": registry_properties(card),
        "is_active": card.status != "inactive",
    }


def upsert_registry_node(
    supabase: Client,
    card: ParsedCard,
    dry_run: bool = False,
) -> None:
    row = build_registry_node_row(card)

    if dry_run:
        print("[DRY RUN] Would upsert rag_card_registry row:")
        print(json.dumps(row, indent=2, ensure_ascii=False)[:4000])
        return

    supabase.table("rag_card_registry").upsert(
        row,
        on_conflict="canonical_id",
    ).execute()


def upsert_registry_aliases(
    supabase: Client,
    card: ParsedCard,
    dry_run: bool = False,
) -> int:
    rows = build_registry_alias_rows(card)

    if not rows:
        return 0

    if dry_run:
        print("[DRY RUN] Would upsert rag_card_aliases rows:")
        print(json.dumps(rows, indent=2, ensure_ascii=False)[:4000])
        return len(rows)

    supabase.table("rag_card_aliases").upsert(
        rows,
        on_conflict="canonical_id,alias_text_norm,language_code",
    ).execute()

    return len(rows)


def upsert_registry_dependencies(
    supabase: Client,
    card: ParsedCard,
    dry_run: bool = False,
) -> int:
    rows = build_registry_dependency_rows(card)

    if not rows:
        return 0

    if dry_run:
        print("[DRY RUN] Would upsert rag_card_dependencies rows:")
        print(json.dumps(rows, indent=2, ensure_ascii=False)[:4000])
        return len(rows)

    supabase.table("rag_card_dependencies").upsert(
        rows,
        on_conflict="from_canonical_id,to_canonical_id,edge_type",
    ).execute()

    return len(rows)


def sync_registry(
    supabase: Client | None,
    cards: list[ParsedCard],
    dry_run: bool,
) -> tuple[int, int, int, list[tuple[str, str]]]:
    """
    Two-pass registry sync:
    1. Upsert all concept nodes first.
    2. Upsert aliases and dependency edges after all nodes exist.

    This avoids FK failures when a card depends on another card that appears
    later in the local knowledge directory.
    """
    enabled_cards = [card for card in cards if registry_enabled(card)]

    node_count = 0
    alias_count = 0
    dependency_count = 0
    failed: list[tuple[str, str]] = []

    print(f"\n=== Registry sync ===")
    print(f"Registry-enabled card(s): {len(enabled_cards)}")

    for card in enabled_cards:
        try:
            print(f"  node: {registry_canonical_id(card)}")
            if dry_run:
                upsert_registry_node(None, card, dry_run=True)  # type: ignore[arg-type]
            else:
                assert supabase is not None
                upsert_registry_node(supabase, card, dry_run=False)
            node_count += 1
        except Exception as exc:
            failed.append((card.source_path, f"registry node: {exc}"))
            print(f"  ERROR node {card.source_path}: {exc}")

    for card in enabled_cards:
        try:
            if dry_run:
                alias_count += upsert_registry_aliases(None, card, dry_run=True)  # type: ignore[arg-type]
                dependency_count += upsert_registry_dependencies(None, card, dry_run=True)  # type: ignore[arg-type]
            else:
                assert supabase is not None
                alias_count += upsert_registry_aliases(supabase, card, dry_run=False)
                dependency_count += upsert_registry_dependencies(supabase, card, dry_run=False)
        except Exception as exc:
            failed.append((card.source_path, f"registry edges/aliases: {exc}"))
            print(f"  ERROR edges/aliases {card.source_path}: {exc}")

    return node_count, alias_count, dependency_count, failed


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
    sync_registry_enabled: bool,
    registry_only: bool,
) -> None:
    if not knowledge_dir.exists():
        raise RuntimeError(f"Knowledge directory does not exist: {knowledge_dir}")

    supabase = None if dry_run else make_supabase_client()
    embedder = Embedder() if (embed and not registry_only) else None

    md_files = iter_markdown_files(knowledge_dir)
    print(f"Found {len(md_files)} markdown card(s) under {knowledge_dir}")

    parsed_cards: list[ParsedCard] = []
    parsed_count = 0
    card_upsert_count = 0
    embedding_upsert_count = 0
    fully_cached_count = 0
    registry_node_count = 0
    registry_alias_count = 0
    registry_dependency_count = 0
    failed: list[tuple[str, str]] = []

    # Pass 1: parse every card first. Registry dependency edges are synced later,
    # after all registry nodes have been created.
    for file_path in md_files:
        print(f"\nParsing: {file_path}")

        try:
            card = parse_card(file_path, knowledge_dir)
            parsed_cards.append(card)
            parsed_count += 1

            print(f"  card_id: {card.card_id}")
            print(f"  type: {card.card_type}")
            print(f"  bucket: {card.card_bucket}")
            print(f"  title: {card.title}")
            print(f"  source_path: {card.source_path}")
            print(f"  hash: {card.content_hash[:12]}...")

        except Exception as exc:
            failed.append((str(file_path), str(exc)))
            print(f"  ERROR: {exc}")

    # Pass 2: sync document cards + embeddings.
    if not registry_only:
        for card in parsed_cards:
            print(f"\nSyncing card: {card.source_path}")

            try:
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
                failed.append((card.source_path, str(exc)))
                print(f"  ERROR: {exc}")
    else:
        print("\nregistry_only=True; skipping rag_cards and rag_card_embeddings sync")

    # Pass 3: sync registry graph metadata.
    if sync_registry_enabled:
        node_count, alias_count, dependency_count, registry_failed = sync_registry(
            supabase=supabase,
            cards=parsed_cards,
            dry_run=dry_run,
        )
        registry_node_count += node_count
        registry_alias_count += alias_count
        registry_dependency_count += dependency_count
        failed.extend(registry_failed)
    else:
        print("\nRegistry sync disabled; skipping rag_card_registry / aliases / dependencies")

    print("\n=== Sync summary ===")
    print(f"Parsed:                 {parsed_count}")
    print(f"Card upserts:           {card_upsert_count}")
    print(f"Embedding upserts:      {embedding_upsert_count}")
    print(f"Fully cached:           {fully_cached_count}")
    print(f"Registry node upserts:  {registry_node_count}")
    print(f"Registry alias upserts: {registry_alias_count}")
    print(f"Registry edge upserts:  {registry_dependency_count}")
    print(f"Failed:                 {len(failed)}")

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

    parser.add_argument(
        "--no-registry",
        action="store_true",
        help="Skip rag_card_registry, rag_card_aliases, and rag_card_dependencies sync.",
    )

    parser.add_argument(
        "--registry-only",
        action="store_true",
        help="Only sync registry graph metadata. Do not upsert rag_cards or embeddings.",
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
        sync_registry_enabled=not args.no_registry,
        registry_only=args.registry_only,
    )


if __name__ == "__main__":
    main()