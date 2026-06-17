from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from supabase import Client


DEFAULT_ALLOWED_EDGE_TYPES = ("requires", "suggests")
DEFAULT_MAX_DEPENDENCY_DEPTH = 5


@dataclass(frozen=True)
class RegistryCard:
    canonical_id: str
    source_path: str
    registry_title: str
    concept_type: str
    registry_bucket: str
    depth: int
    priority: int
    card_id: str
    card_title: str
    card_type: str
    card_bucket: str
    category: str | None
    body_markdown: str
    content_hash: str | None = None

    @classmethod
    def from_rpc_row(cls, row: dict[str, Any]) -> "RegistryCard":
        card_title = row.get("card_title") or row.get("registry_title") or ""
        card_bucket = row.get("card_bucket") or row.get("registry_bucket") or ""

        return cls(
            canonical_id=row.get("canonical_id", ""),
            source_path=row.get("source_path", ""),
            registry_title=row.get("registry_title", ""),
            concept_type=row.get("concept_type", ""),
            registry_bucket=row.get("registry_bucket", ""),
            depth=int(row.get("depth") or 0),
            priority=int(row.get("priority") or 100),
            card_id=str(row.get("card_id") or ""),
            card_title=card_title,
            card_type=row.get("card_type") or row.get("concept_type") or "",
            card_bucket=card_bucket,
            category=row.get("category"),
            body_markdown=row.get("body_markdown") or "",
            content_hash=row.get("content_hash"),
        )

    def to_rag_card_row(self) -> dict[str, Any]:
        """
        Convert the registry-resolved card into the same row shape used by
        context_builder.make_dynamic_item().
        """
        return {
            "card_id": self.card_id,
            "title": self.card_title or self.registry_title,
            "card_type": self.card_type,
            "card_bucket": self.card_bucket,
            "category": self.category,
            "source_path": self.source_path,
            "body_markdown": self.body_markdown,
            "content_hash": self.content_hash,
        }


@dataclass(frozen=True)
class AliasMatch:
    canonical_id: str
    title: str
    concept_type: str
    card_bucket: str
    alias_text: str
    alias_type: str
    weight: float
    source_path: str

    @classmethod
    def from_rpc_row(cls, row: dict[str, Any]) -> "AliasMatch":
        return cls(
            canonical_id=row.get("canonical_id", ""),
            title=row.get("title", ""),
            concept_type=row.get("concept_type", ""),
            card_bucket=row.get("card_bucket", ""),
            alias_text=row.get("alias_text", ""),
            alias_type=row.get("alias_type", ""),
            weight=float(row.get("weight") or 0),
            source_path=row.get("source_path", ""),
        )


class RegistryResolver:
    """
    Resolves canonical concept IDs through the Supabase registry graph.

    Tell-style API:
        resolver.resolve_cards(seed_canonical_ids)

    The caller does not fetch registry tables, expand dependencies, or match
    source paths itself. That logic stays behind this object.
    """

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def match_aliases(
        self,
        query_text: str,
        min_weight: float = 0.7,
    ) -> list[AliasMatch]:
        response = self.supabase.rpc(
            "match_rag_card_aliases",
            {
                "query_text": query_text,
                "min_weight": min_weight,
            },
        ).execute()

        return [AliasMatch.from_rpc_row(row) for row in (response.data or [])]

    def resolve_cards(
        self,
        seed_canonical_ids: Sequence[str],
        allowed_edge_types: Sequence[str] = DEFAULT_ALLOWED_EDGE_TYPES,
        max_depth: int = DEFAULT_MAX_DEPENDENCY_DEPTH,
    ) -> tuple[list[RegistryCard], list[str]]:
        """
        Expand seed concepts through registry dependencies and return actual
        rag_cards rows.

        Returns:
        - resolved registry cards
        - missing seed canonical IDs
        """
        ordered_seed_ids = _dedupe_preserve_order(seed_canonical_ids)

        if not ordered_seed_ids:
            return [], []

        response = self.supabase.rpc(
            "resolve_rag_registry_cards",
            {
                "seed_canonical_ids": ordered_seed_ids,
                "allowed_edge_types": list(allowed_edge_types),
                "max_depth": max_depth,
            },
        ).execute()

        rows = response.data or []
        cards = [RegistryCard.from_rpc_row(row) for row in rows]

        # Keep only cards that actually resolve to a rag_cards row with body.
        # The missing list below still reports unresolved seed IDs.
        cards = [card for card in cards if card.card_id and card.body_markdown]

        resolved_ids = {card.canonical_id for card in cards}
        missing_seed_ids = [
            canonical_id
            for canonical_id in ordered_seed_ids
            if canonical_id not in resolved_ids
        ]

        return cards, missing_seed_ids


def _dedupe_preserve_order(values: Sequence[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()

    for value in values:
        if not value:
            continue

        if value in seen:
            continue

        result.append(value)
        seen.add(value)

    return result
