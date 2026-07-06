from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from supabase import Client

from src.queryDecomposition.query_decomposer import (
    RetrievalIntent,
    decompose_query_for_retrieval,
    get_seed_canonical_ids,
)
from src.queryDecomposition.registry_resolver import (
    DEFAULT_ALLOWED_EDGE_TYPES,
    DEFAULT_MAX_DEPENDENCY_DEPTH,
    AliasMatch,
    RegistryCard,
    RegistryConcept,
    RegistryResolver,
)


@dataclass(frozen=True)
class RetrievalPlan:
    original_query: str
    intents: list[RetrievalIntent]
    seed_canonical_ids: list[str]
    alias_matches: list[AliasMatch]
    resolved_cards: list[RegistryCard]
    missing_seed_canonical_ids: list[str]
    retrieval_queries_by_bucket: dict[str, list[str]] = field(default_factory=dict)

    @property
    def forced_cards(self) -> list[RegistryCard]:
        return self.resolved_cards

    def print_summary(self) -> None:
        print("\n=== Retrieval Plan ===")
        print(f"Original query: {self.original_query}")

        print("\n--- Intents ---")
        for i, intent in enumerate(self.intents, start=1):
            print(f"{i}. [{intent.target_bucket}] {intent.query}")
            print(f"   reason: {intent.reason}")
            print(f"   seed canonical IDs: {list(intent.seed_canonical_ids)}")
            print(f"   rule: {intent.source_rule}")

        print("\n--- Alias matches from registry ---")
        if self.alias_matches:
            for match in self.alias_matches:
                print(
                    f"- {match.canonical_id} | alias={match.alias_text!r} "
                    f"| weight={match.weight:.2f}"
                )
        else:
            print("(none)")

        print("\n--- Seed canonical IDs ---")
        if self.seed_canonical_ids:
            for canonical_id in self.seed_canonical_ids:
                print(f"- {canonical_id}")
        else:
            print("(none)")

        print("\n--- Registry-resolved forced cards ---")
        if self.resolved_cards:
            for card in self.resolved_cards:
                print(
                    f"- {card.canonical_id} -> {card.card_title} "
                    f"| {card.source_path} | depth={card.depth}"
                )
        else:
            print("(none)")

        if self.missing_seed_canonical_ids:
            print("\n--- Missing seed canonical IDs ---")
            for canonical_id in self.missing_seed_canonical_ids:
                print(f"- {canonical_id}")

        print("\n--- Retrieval queries by bucket ---")
        for bucket, queries in self.retrieval_queries_by_bucket.items():
            print(f"[{bucket}]")
            for query in queries:
                print(f"  - {query}")


class RetrievalPlanner:
    """
    Tell-style retrieval planner.

    Context builder tells this object:
        build a retrieval plan for this query.

    This object owns:
    - loading active registry concepts;
    - LLM seed extraction;
    - registry alias hints;
    - canonical ID collection;
    - dependency expansion through Supabase;
    - grouping vector-retrieval subqueries by bucket.
    """

    def __init__(
        self,
        supabase: Client,
        *,
        include_alias_hints: bool = True,
        alias_min_weight: float = 0.7,
        allowed_edge_types: Sequence[str] = DEFAULT_ALLOWED_EDGE_TYPES,
        max_dependency_depth: int = DEFAULT_MAX_DEPENDENCY_DEPTH,
    ):
        self.resolver = RegistryResolver(supabase)
        self.include_alias_hints = include_alias_hints
        self.alias_min_weight = alias_min_weight
        self.allowed_edge_types = tuple(allowed_edge_types)
        self.max_dependency_depth = max_dependency_depth

    def build_plan(self, user_query: str) -> RetrievalPlan:
        active_concepts = self.resolver.fetch_active_concepts()

        intents = decompose_query_for_retrieval(
            user_query=user_query,
            available_concepts=active_concepts,
        )

        seed_canonical_ids = get_seed_canonical_ids(intents)

        alias_matches: list[AliasMatch] = []

        if self.include_alias_hints:
            alias_matches = self.resolver.match_aliases(
                query_text=user_query,
                min_weight=self.alias_min_weight,
            )

            for match in alias_matches:
                if match.canonical_id not in seed_canonical_ids:
                    seed_canonical_ids.append(match.canonical_id)

        resolved_cards, missing_seed_canonical_ids = self.resolver.resolve_cards(
            seed_canonical_ids=seed_canonical_ids,
            allowed_edge_types=self.allowed_edge_types,
            max_depth=self.max_dependency_depth,
        )

        return RetrievalPlan(
            original_query=user_query,
            intents=intents,
            seed_canonical_ids=seed_canonical_ids,
            alias_matches=alias_matches,
            resolved_cards=resolved_cards,
            missing_seed_canonical_ids=missing_seed_canonical_ids,
            retrieval_queries_by_bucket=_group_queries_by_bucket(
                intents=intents,
                active_concepts=active_concepts,
            ),
        )


def _group_queries_by_bucket(
    intents: list[RetrievalIntent],
    active_concepts: list[RegistryConcept],
) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {
        "patterns": [],
        "functions": [],
        "references": [],
    }

    concept_bucket_lookup = {
        concept.canonical_id: _safe_bucket(concept.card_bucket)
        for concept in active_concepts
    }

    for intent in intents:
        bucket = _safe_bucket(intent.target_bucket)
        grouped.setdefault(bucket, [])

        if intent.query not in grouped[bucket]:
            grouped[bucket].append(intent.query)

        for canonical_id in intent.seed_canonical_ids:
            concept_bucket = concept_bucket_lookup.get(canonical_id)

            if concept_bucket and intent.query not in grouped[concept_bucket]:
                grouped[concept_bucket].append(intent.query)

    return grouped


def _safe_bucket(value: str) -> str:
    normalized = str(value or "references").lower().strip()

    if normalized in {"pattern", "patterns"}:
        return "patterns"

    if normalized in {"function", "functions"}:
        return "functions"

    return "references"