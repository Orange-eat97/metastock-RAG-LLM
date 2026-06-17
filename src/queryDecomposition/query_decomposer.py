from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal


Bucket = Literal["patterns", "functions", "references"]


@dataclass(frozen=True)
class RetrievalIntent:
    """
    A retrieval intent is not a MetaStock formula fragment.

    It is a planning object that says:
    - which semantic subquery should be used for vector retrieval;
    - which bucket should receive that subquery;
    - which canonical registry concepts should be used as seed nodes.

    Dependencies are intentionally NOT stored here. Dependencies belong to the
    Supabase registry graph: rag_card_registry + rag_card_dependencies.
    """

    query: str
    target_bucket: Bucket
    reason: str
    seed_canonical_ids: tuple[str, ...] = field(default_factory=tuple)
    source_rule: str = ""

    @property
    def force_card_names(self) -> tuple[str, ...]:
        """
        Backward-compatible alias for older debug/test code.

        The values are now canonical IDs, not human card titles.
        """
        return self.seed_canonical_ids


def _normalize_query(user_query: str) -> str:
    return " ".join(user_query.lower().strip().split())


def _has_any(text: str, phrases: list[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def _has_token(text: str, token: str) -> bool:
    """
    Match a standalone token only.

    This prevents the old bug where "making" matched "MA" because it contained
    the substring " ma".
    """
    escaped = re.escape(token.lower())
    return re.search(rf"(^|[^a-z0-9]){escaped}([^a-z0-9]|$)", text) is not None


def _has_moving_average_intent(text: str) -> bool:
    if _has_any(
        text,
        [
            "moving average",
            "simple moving average",
            "exponential moving average",
            "weighted moving average",
            "simple average",
            "exponential average",
        ],
    ):
        return True

    return any(
        _has_token(text, token)
        for token in ["ma", "sma", "ema"]
    )


def _has_previous_or_new_low_intent(text: str) -> bool:
    if _has_any(
        text,
        [
            "previous low",
            "prior low",
            "new low",
            "breaking below",
            "break below",
            "breakdown",
            "break down",
        ],
    ):
        return True

    regex_patterns = [
        r"\bnew\s+\d+\s*(day|period|bar)?\s+low\b",
        r"\bmaking\s+a\s+new\s+\d+\s*(day|period|bar)?\s+low\b",
        r"\bmaking\s+new\s+\d+\s*(day|period|bar)?\s+low\b",
        r"\b\d+\s*(day|period|bar)?\s+low\b",
    ]

    return any(re.search(pattern, text) for pattern in regex_patterns)


def _extract_period(text: str, default: int = 20) -> int:
    """
    Lightweight period extractor.

    Examples:
    - previous 20 day high -> 20
    - 50 day moving average -> 50
    - 30 period volume average -> 30
    """
    patterns = [
        r"previous\s+(\d+)\s*(day|period|bar)?",
        r"prior\s+(\d+)\s*(day|period|bar)?",
        r"new\s+(\d+)\s*(day|period|bar)?",
        r"(\d+)\s*(day|period|bar)?\s*high",
        r"(\d+)\s*(day|period|bar)?\s*low",
        r"(\d+)\s*(day|period|bar)?\s*moving average",
        r"(\d+)\s*(day|period|bar)?\s*ma\b",
        r"(\d+)\s*(day|period|bar)?\s*average",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))

    return default


def decompose_query_for_retrieval(user_query: str) -> list[RetrievalIntent]:
    """
    Deterministic retrieval decomposition.

    The decomposer maps user language to seed canonical concepts only.
    It does NOT expand dependencies like:
        pattern.breakout -> function.hhv + function.ref

    Dependency expansion is handled by the registry resolver through Supabase.
    """
    q = _normalize_query(user_query)
    intents: list[RetrievalIntent] = []

    # Volume above average.
    if _has_any(
        q,
        [
            "volume above average",
            "above average volume",
            "average volume",
            "high volume",
            "volume spike",
            "volume surge",
            "unusual volume",
        ],
    ):
        intents.append(
            RetrievalIntent(
                query="volume above average high volume volume spike average volume",
                target_bucket="patterns",
                reason="User asks for above-average volume or volume confirmation.",
                seed_canonical_ids=("pattern.volume_above_average",),
                source_rule="volume_above_average_pattern",
            )
        )

    # Breakout / previous high.
    if _has_any(
        q,
        [
            "breakout",
            "break out",
            "breaking above",
            "break above",
            "above previous high",
            "above prior high",
            "new high",
            "previous high",
            "prior high",
        ],
    ):
        period = _extract_period(q, default=20)

        intents.append(
            RetrievalIntent(
                query=f"price breakout above previous {period} period high resistance breakout",
                target_bucket="patterns",
                reason="User asks for a price breakout above a previous high.",
                seed_canonical_ids=("pattern.breakout",),
                source_rule="breakout_pattern",
            )
        )

    # Moving average.
    if _has_moving_average_intent(q):
        period = _extract_period(q, default=50)

        intents.append(
            RetrievalIntent(
                query=f"Mov moving average close {period} day simple exponential moving average",
                target_bucket="functions",
                reason="User mentions moving average.",
                seed_canonical_ids=("function.mov",),
                source_rule="moving_average_function",
            )
        )

    # RSI.
    if _has_any(
        q,
        [
            "rsi",
            "relative strength index",
            "oversold",
            "overbought",
        ],
    ):
        intents.append(
            RetrievalIntent(
                query="RSI relative strength index oversold overbought RSI(14)",
                target_bucket="functions",
                reason="User mentions RSI or RSI-style overbought/oversold condition.",
                seed_canonical_ids=("function.rsi",),
                source_rule="rsi_function",
            )
        )

    # Cross above / cross below.
    if _has_any(
        q,
        [
            "cross above",
            "crosses above",
            "crossover",
            "cross over",
            "cross below",
            "crosses below",
            "crossunder",
            "cross under",
        ],
    ):
        intents.append(
            RetrievalIntent(
                query="Cross function crossover cross above cross below Cross(DATA ARRAY 1, DATA ARRAY 2)",
                target_bucket="functions",
                reason="User mentions a crossing condition.",
                seed_canonical_ids=("function.cross",),
                source_rule="cross_function",
            )
        )

    # Previous low / new low.
    # There is currently no confirmed pattern.new_low or pattern.breakdown card.
    # Therefore this maps directly to confirmed function cards.
    if _has_previous_or_new_low_intent(q):
        period = _extract_period(q, default=20)

        intents.append(
            RetrievalIntent(
                query=f"LLV lowest low previous {period} periods new low previous low breakdown support",
                target_bucket="functions",
                reason="New-low or previous-low conditions require LLV.",
                seed_canonical_ids=("function.llv", "function.ref"),
                source_rule="new_or_previous_low_functions",
            )
        )

    # Fallback: keep original semantic query.
    intents.append(
        RetrievalIntent(
            query=user_query,
            target_bucket="references",
            reason="Fallback retrieval using the original query.",
            seed_canonical_ids=(),
            source_rule="original_query_fallback",
        )
    )

    return _dedupe_intents(intents)


def get_seed_canonical_ids(intents: list[RetrievalIntent]) -> list[str]:
    seed_ids: list[str] = []

    for intent in intents:
        for canonical_id in intent.seed_canonical_ids:
            if canonical_id not in seed_ids:
                seed_ids.append(canonical_id)

    return seed_ids


def get_forced_card_names(intents: list[RetrievalIntent]) -> list[str]:
    """
    Backward-compatible helper for old tests.

    It now returns canonical IDs, not card titles.
    Prefer get_seed_canonical_ids() in new code.
    """
    return get_seed_canonical_ids(intents)


def _dedupe_intents(intents: list[RetrievalIntent]) -> list[RetrievalIntent]:
    seen: set[tuple[str, Bucket, tuple[str, ...]]] = set()
    result: list[RetrievalIntent] = []

    for intent in intents:
        key = (
            intent.query.lower(),
            intent.target_bucket,
            intent.seed_canonical_ids,
        )

        if key in seen:
            continue

        seen.add(key)
        result.append(intent)

    return result
