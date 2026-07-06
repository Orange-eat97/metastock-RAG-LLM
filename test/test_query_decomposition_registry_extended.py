from __future__ import annotations

import io
from contextlib import redirect_stdout
from dataclasses import dataclass, field

from dotenv import load_dotenv

from src.retrieval.context_builder import make_supabase_client
from src.queryDecomposition.retrieval_planner import RetrievalPlanner


@dataclass(frozen=True)
class TestCase:
    name: str
    query: str

    # Canonical IDs that must appear in resolved cards.
    must_resolve: set[str] = field(default_factory=set)

    # Canonical IDs that must NOT appear in resolved cards.
    # Keep this conservative for now. Do not use this against HHV/LLV for pattern.breakout
    # until branch-aware dependency filtering is implemented.
    must_not_resolve: set[str] = field(default_factory=set)

    # True when the LLM should propose a missing card and the decomposer should print:
    # "suggest adding <seed> card"
    should_suggest_missing_card: bool = False

    # Tokens expected somewhere in the printed suggestion log.
    # Use lowercase terms like "macd", "atr", "bollinger".
    suggestion_tokens_any: tuple[str, ...] = ()


POSITIVE_CASES = [
    TestCase(
        name="bullish breakout with volume confirmation",
        query="Find stocks breaking above the previous 20 day high with volume above average",
        must_resolve={
            "pattern.breakout",
            "function.hhv",
            "function.ref",
            "pattern.volume_above_average",
            "function.mov",
        },
    ),
    TestCase(
        name="bearish breakdown with high volume",
        query="Find stocks breaking below the previous 20 day low with high volume",
        must_resolve={
            "pattern.breakout",
            "function.llv",
            "function.ref",
            "pattern.volume_above_average",
            "function.mov",
        },
    ),
    TestCase(
        name="new 20 day high",
        query="Find stocks making a new 20 day high",
        must_resolve={
            "function.hhv",
        },
    ),
    TestCase(
        name="new 20 day low",
        query="Find stocks making a new 20 day low",
        must_resolve={
            "function.llv",
        },
    ),
    TestCase(
        name="RSI oversold plus moving average filter",
        query="Find stocks where RSI is below 30 and close is above 50 day moving average",
        must_resolve={
            "function.rsi",
            "function.mov",
        },
    ),
    TestCase(
        name="RSI overbought plus unusual volume",
        query="Find overbought stocks with unusual volume",
        must_resolve={
            "function.rsi",
            "pattern.volume_above_average",
            "function.mov",
        },
    ),
    TestCase(
        name="price crosses above moving average",
        query="Find stocks where close crosses above the 50 day moving average",
        must_resolve={
            "function.cross",
            "function.mov",
        },
    ),
    TestCase(
        name="moving average bearish crossover",
        query="Find stocks where the 20 day moving average crosses below the 50 day moving average",
        must_resolve={
            "function.cross",
            "function.mov",
        },
    ),
    TestCase(
        name="previous bar comparison",
        query="Find stocks where close is higher than yesterday's close and volume increased from the previous day",
        must_resolve={
            "function.ref",
        },
    ),
    TestCase(
        name="volume spike only",
        query="Find stocks with a volume spike",
        must_resolve={
            "pattern.volume_above_average",
            "function.mov",
        },
    ),
    TestCase(
        name="continuing MA condition should not use Cross",
        query="Find stocks where close is above the 50 day moving average",
        must_resolve={
            "function.mov",
        },
        must_not_resolve={
            "function.cross",
        },
    ),
]


NEGATIVE_MISSING_CARD_CASES = [
    TestCase(
        name="MACD signal cross missing function card",
        query="Find stocks where MACD crosses above its signal line",
        must_resolve={
            "function.cross",
            "function.mov",
        },
        should_suggest_missing_card=True,
        suggestion_tokens_any=("macd",),
    ),
    TestCase(
        name="stochastic oscillator missing function card",
        query="Find stocks where the stochastic oscillator crosses above 20 from oversold",
        must_resolve={
            "function.cross",
        },
        should_suggest_missing_card=True,
        suggestion_tokens_any=("stochastic", "stoch"),
    ),
    TestCase(
        name="ATR trailing stop missing function or pattern card",
        query="Find stocks where price is above a 2 ATR trailing stop",
        should_suggest_missing_card=True,
        suggestion_tokens_any=("atr", "trailing"),
    ),
    TestCase(
        name="Bollinger Band squeeze missing pattern card",
        query="Find stocks with a Bollinger Band squeeze breakout",
        must_resolve={
            "pattern.breakout",
        },
        should_suggest_missing_card=True,
        suggestion_tokens_any=("bollinger", "squeeze"),
    ),
    TestCase(
        name="gap up missing card with volume fallback",
        query="Find stocks that gap up with a volume spike",
        must_resolve={
            "pattern.volume_above_average",
            "function.mov",
        },
        should_suggest_missing_card=True,
        suggestion_tokens_any=("gap",),
    ),
    TestCase(
        name="candlestick pattern missing card with volume fallback",
        query="Find stocks with bullish engulfing candlestick pattern and high volume",
        must_resolve={
            "pattern.volume_above_average",
            "function.mov",
        },
        should_suggest_missing_card=True,
        suggestion_tokens_any=("engulfing", "candlestick"),
    ),
    TestCase(
        name="OBV missing function card with Mov fallback",
        query="Find stocks where OBV is above its 20 day moving average",
        must_resolve={
            "function.mov",
        },
        should_suggest_missing_card=True,
        suggestion_tokens_any=("obv",),
    ),
    TestCase(
        name="CCI missing function card",
        query="Find stocks where CCI is below -100",
        should_suggest_missing_card=True,
        suggestion_tokens_any=("cci",),
    ),
]


def run_case(planner: RetrievalPlanner, case: TestCase) -> bool:
    print("\n" + "=" * 100)
    print(f"TEST: {case.name}")
    print(f"QUERY: {case.query}")

    stdout_buffer = io.StringIO()

    with redirect_stdout(stdout_buffer):
        plan = planner.build_plan(case.query)

    planner_log = stdout_buffer.getvalue()
    seed_ids = set(plan.seed_canonical_ids)
    resolved_ids = {card.canonical_id for card in plan.resolved_cards}

    if planner_log.strip():
        print("\nPlanner log:")
        print(planner_log.rstrip())

    print("\nSeed canonical IDs:")
    if seed_ids:
        for canonical_id in sorted(seed_ids):
            print(f"- {canonical_id}")
    else:
        print("(none)")

    print("\nResolved canonical IDs:")
    if resolved_ids:
        for canonical_id in sorted(resolved_ids):
            print(f"- {canonical_id}")
    else:
        print("(none)")

    failures: list[str] = []

    missing_required = case.must_resolve - resolved_ids
    if missing_required:
        failures.append("Missing expected resolved IDs:")
        failures.extend(f"  - {canonical_id}" for canonical_id in sorted(missing_required))

    forbidden_present = case.must_not_resolve & resolved_ids
    if forbidden_present:
        failures.append("Forbidden IDs were resolved:")
        failures.extend(f"  - {canonical_id}" for canonical_id in sorted(forbidden_present))

    normalized_log = planner_log.lower()

    if case.should_suggest_missing_card:
        if "suggest adding" not in normalized_log:
            failures.append('Expected missing-card suggestion, but no "suggest adding" line was printed.')

        if case.suggestion_tokens_any:
            if not any(token.lower() in normalized_log for token in case.suggestion_tokens_any):
                failures.append(
                    "Expected suggestion log to contain at least one of: "
                    + ", ".join(case.suggestion_tokens_any)
                )

    if failures:
        print("\n[FAIL]")
        for failure in failures:
            print(failure)
        return False

    print("\n[PASS]")
    return True


def main() -> None:
    load_dotenv()

    supabase = make_supabase_client()
    planner = RetrievalPlanner(supabase=supabase)

    cases = POSITIVE_CASES + NEGATIVE_MISSING_CARD_CASES

    passed = 0
    failed = 0

    for case in cases:
        ok = run_case(planner, case)

        if ok:
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 100)
    print("SUMMARY")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()