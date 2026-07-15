from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Callable, TypeVar

from dotenv import load_dotenv
from supabase import Client, create_client

from src.rag_service import (
    ExplorerDraftResponse,
    RagExplorerService,
    RagServiceConfig,
)


BASE_QUERY = (
    "Find stocks where RSI(14) is below 30 "
    "and the close is above its 50-day "
    "simple moving average"
)

NORMALIZED_VARIANT = (
    "   FIND   stocks where RSI(14) is below 30 "
    "and the close is above its 50-day "
    "simple moving average!!!   "
)

SEMANTIC_VARIANT = (
    "Screen for securities with a 14-period RSI "
    "under 30 while the closing price remains above "
    "the 50-period simple moving average."
)

DIFFERENT_THRESHOLD = (
    "Find stocks where RSI(14) is below 35 "
    "and the close is above its 50-day "
    "simple moving average"
)

CROSS_INSTEAD_OF_STATE = (
    "Find stocks where RSI(14) is below 30 "
    "and the close crosses above its 50-day "
    "simple moving average"
)

OR_INSTEAD_OF_AND = (
    "Find stocks where RSI(14) is below 30 "
    "or the close is above its 50-day "
    "simple moving average"
)


CONVERSATION_ID = "query-cache-acceptance-test"

MAX_TRANSIENT_ATTEMPTS = 5
INITIAL_RETRY_DELAY_SECONDS = 3.0
MAX_RETRY_DELAY_SECONDS = 30.0


T = TypeVar("T")


@dataclass(frozen=True)
class CaseResult:
    label: str
    query: str
    response: ExplorerDraftResponse
    event_type: str | None
    cache_match_type: str | None
    log_metadata: dict[str, Any]


def get_supabase_client() -> Client:
    url = str(
        os.getenv("SUPABASE_URL") or ""
    ).strip()

    key = str(
        os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        or ""
    ).strip()

    if not url:
        raise RuntimeError(
            "SUPABASE_URL is missing."
        )

    if not key:
        raise RuntimeError(
            "SUPABASE_SERVICE_ROLE_KEY is missing."
        )

    return create_client(url, key)


def is_transient_remote_error(
    exc: Exception,
) -> bool:
    message = str(exc).lower()

    transient_markers = (
        "connection timed out",
        "error code 522",
        "'code': 522",
        '"code": 522',
        "json could not be generated",
        "cloudflare",
        "bad gateway",
        "service unavailable",
        "gateway timeout",
        "connection reset",
        "connection aborted",
        "temporarily unavailable",
        "remote end closed connection",
        "'code': 500",
        "'code': 502",
        "'code': 503",
        "'code': 504",
        "'code': 520",
        "'code': 521",
        "'code': 523",
        "'code': 524",
        '"code": 500',
        '"code": 502',
        '"code": 503',
        '"code": 504',
        '"code": 520',
        '"code": 521',
        '"code": 523',
        '"code": 524',
    )

    return any(
        marker in message
        for marker in transient_markers
    )


def call_with_retry(
    operation_name: str,
    operation: Callable[[], T],
) -> T:
    delay = INITIAL_RETRY_DELAY_SECONDS

    for attempt in range(
        1,
        MAX_TRANSIENT_ATTEMPTS + 1,
    ):
        try:
            return operation()

        except Exception as exc:
            is_last_attempt = (
                attempt
                >= MAX_TRANSIENT_ATTEMPTS
            )

            if (
                not is_transient_remote_error(exc)
                or is_last_attempt
            ):
                raise

            print()
            print(
                "[acceptance_test] "
                f"{operation_name} failed with a "
                "transient remote error."
            )
            print(
                "[acceptance_test] "
                f"attempt={attempt}/"
                f"{MAX_TRANSIENT_ATTEMPTS}"
            )
            print(
                "[acceptance_test] "
                f"error={type(exc).__name__}: {exc}"
            )
            print(
                "[acceptance_test] "
                f"retrying in {delay:.1f} seconds"
            )

            time.sleep(delay)

            delay = min(
                delay * 2,
                MAX_RETRY_DELAY_SECONDS,
            )

    raise RuntimeError(
        f"{operation_name} exhausted retries."
    )


def check_supabase_connectivity(
    client: Client,
) -> None:
    def operation() -> Any:
        return (
            client
            .table("explorer_outputs")
            .select("id")
            .limit(1)
            .execute()
        )

    call_with_retry(
        "Supabase connectivity check",
        operation,
    )


def read_service_log(
    client: Client,
    log_id: str | None,
) -> dict[str, Any]:
    if not log_id:
        return {}

    def operation() -> Any:
        return (
            client
            .table("rag_service_logs")
            .select(
                "log_id, event_type, user_query, "
                "explorer_output_id, metadata"
            )
            .eq("log_id", log_id)
            .limit(1)
            .execute()
        )

    response = call_with_retry(
        f"Read service log {log_id}",
        operation,
    )

    if not response.data:
        raise AssertionError(
            "No rag_service_logs row found for "
            f"log_id={log_id}"
        )

    row = response.data[0]

    if not isinstance(row, dict):
        raise AssertionError(
            "Service-log response is not a dictionary."
        )

    return row


def generate_with_retry(
    *,
    service: RagExplorerService,
    query: str,
) -> ExplorerDraftResponse:
    def operation() -> ExplorerDraftResponse:
        return service.generate_explorer(
            user_message=query,
            conversation_id=CONVERSATION_ID,
        )

    return call_with_retry(
        "Explorer generation/cache lookup",
        operation,
    )


def run_case(
    *,
    service: RagExplorerService,
    client: Client,
    label: str,
    query: str,
) -> CaseResult:
    print()
    print("=" * 80)
    print(f"CASE: {label}")
    print("=" * 80)
    print(f"Query: {query}")

    response = generate_with_retry(
        service=service,
        query=query,
    )

    service_log = read_service_log(
        client,
        response.service_log,
    )

    metadata = service_log.get("metadata")

    if not isinstance(metadata, dict):
        metadata = {}

    cache_match_type = metadata.get(
        "cache_match_type"
    )

    if cache_match_type is not None:
        cache_match_type = str(
            cache_match_type
        )

    event_type = service_log.get(
        "event_type"
    )

    if event_type is not None:
        event_type = str(event_type)

    displayed_result = {
        "explorer": response.explorer,
        "source": response.source,
        "validation_passed": (
            response.validation.passed
        ),
        "validation_errors": (
            response.validation.errors
        ),
        "service_log": response.service_log,
        "event_type": event_type,
        "cache_match_type": (
            cache_match_type
        ),
        "matched_query": metadata.get(
            "matched_query"
        ),
        "similarity": metadata.get(
            "similarity"
        ),
        "equivalence_confidence": (
            metadata.get(
                "equivalence_confidence"
            )
        ),
        "equivalence_reason": (
            metadata.get(
                "equivalence_reason"
            )
        ),
        "semantic_cache_error": (
            metadata.get(
                "semantic_cache_error"
            )
        ),
    }

    print(
        json.dumps(
            displayed_result,
            indent=2,
            ensure_ascii=False,
        )
    )

    return CaseResult(
        label=label,
        query=query,
        response=response,
        event_type=event_type,
        cache_match_type=cache_match_type,
        log_metadata=metadata,
    )


def assert_source(
    result: CaseResult,
    expected: str,
) -> None:
    actual = result.response.source

    if actual != expected:
        raise AssertionError(
            f"{result.label}: expected source="
            f"{expected!r}, got {actual!r}."
        )


def assert_source_in(
    result: CaseResult,
    expected: set[str],
) -> None:
    actual = result.response.source

    if actual not in expected:
        raise AssertionError(
            f"{result.label}: expected source in "
            f"{sorted(expected)!r}, got {actual!r}."
        )


def assert_validation_passed(
    result: CaseResult,
) -> None:
    if not result.response.validation.passed:
        raise AssertionError(
            f"{result.label}: Explorer did not pass "
            "validation. Errors: "
            f"{result.response.validation.errors}"
        )


def assert_same_explorer(
    result: CaseResult,
    expected_explorer: str,
) -> None:
    actual = result.response.explorer

    if actual != expected_explorer:
        raise AssertionError(
            f"{result.label}: expected Explorer "
            f"{expected_explorer}, got {actual}."
        )


def assert_different_explorer(
    result: CaseResult,
    forbidden_explorer: str,
) -> None:
    actual = result.response.explorer

    if actual == forbidden_explorer:
        raise AssertionError(
            f"{result.label}: incorrectly reused "
            f"Explorer {forbidden_explorer}."
        )


def assert_cache_match_type(
    result: CaseResult,
    expected: str,
) -> None:
    actual = result.cache_match_type

    if actual != expected:
        raise AssertionError(
            f"{result.label}: expected "
            f"cache_match_type={expected!r}, "
            f"got {actual!r}."
        )


def assert_no_semantic_cache_error(
    result: CaseResult,
) -> None:
    semantic_error = result.log_metadata.get(
        "semantic_cache_error"
    )

    if semantic_error:
        raise AssertionError(
            f"{result.label}: semantic cache failed "
            f"open with error: {semantic_error}"
        )


def main() -> None:
    load_dotenv()

    client = get_supabase_client()

    print(
        "[acceptance_test] Checking Supabase "
        "connectivity"
    )
    check_supabase_connectivity(client)

    config = RagServiceConfig(
        use_cache=True,
        use_semantic_cache=True,
        semantic_cache_min_similarity=0.75,
        semantic_cache_min_confidence=0.97,
        semantic_cache_max_candidates=5,
    )

    service = RagExplorerService(
        config=config
    )

    # ------------------------------------------------------------------
    # 1. Establish the seed Explorer.
    #
    # On a completely empty table this must be generated.
    #
    # If a previous acceptance run inserted the row and then failed because
    # Supabase timed out, rerunning this script may return the existing seed
    # from cache. Both outcomes are accepted so the test is resumable.
    # ------------------------------------------------------------------
    seed = run_case(
        service=service,
        client=client,
        label="Establish seed Explorer",
        query=BASE_QUERY,
    )

    assert_source_in(
        seed,
        {
            "generated",
            "cache",
        },
    )
    assert_validation_passed(seed)

    seed_explorer = seed.response.explorer

    if seed.response.source == "generated":
        print(
            "[acceptance_test] Seed Explorer was "
            "generated during this run."
        )
    else:
        print(
            "[acceptance_test] Existing seed Explorer "
            "was reused. This is expected when resuming "
            "a partially completed test."
        )

    # ------------------------------------------------------------------
    # 2. Identical request must reuse the seed.
    # ------------------------------------------------------------------
    exact = run_case(
        service=service,
        client=client,
        label="Identical request",
        query=BASE_QUERY,
    )

    assert_source(
        exact,
        "cache",
    )
    assert_validation_passed(exact)
    assert_same_explorer(
        exact,
        seed_explorer,
    )
    assert_cache_match_type(
        exact,
        "normalized_exact",
    )

    # ------------------------------------------------------------------
    # 3. Case, spacing and terminal punctuation differences must reuse it.
    # ------------------------------------------------------------------
    normalized = run_case(
        service=service,
        client=client,
        label="Normalized exact request",
        query=NORMALIZED_VARIANT,
    )

    assert_source(
        normalized,
        "cache",
    )
    assert_validation_passed(normalized)
    assert_same_explorer(
        normalized,
        seed_explorer,
    )
    assert_cache_match_type(
        normalized,
        "normalized_exact",
    )

    # ------------------------------------------------------------------
    # 4. A paraphrase with the same strategy meaning must reuse the seed.
    #
    # A transient Supabase failure is retried. If the duplicate guard fails
    # open and normal RAG generation occurs, this assertion will fail.
    # ------------------------------------------------------------------
    semantic = run_case(
        service=service,
        client=client,
        label="Semantic-equivalent request",
        query=SEMANTIC_VARIANT,
    )

    assert_source(
        semantic,
        "cache",
    )
    assert_validation_passed(semantic)
    assert_same_explorer(
        semantic,
        seed_explorer,
    )
    assert_cache_match_type(
        semantic,
        "semantic_equivalent",
    )
    assert_no_semantic_cache_error(
        semantic
    )

    # ------------------------------------------------------------------
    # 5. A changed threshold must not reuse the seed.
    #
    # On the first successful run this should be generated. On a resumed run,
    # its previously generated row may be served from cache. Both are valid as
    # long as it is not the seed Explorer.
    # ------------------------------------------------------------------
    threshold = run_case(
        service=service,
        client=client,
        label="Different RSI threshold",
        query=DIFFERENT_THRESHOLD,
    )

    assert_source_in(
        threshold,
        {
            "generated",
            "cache",
        },
    )
    assert_validation_passed(threshold)
    assert_different_explorer(
        threshold,
        seed_explorer,
    )

    # ------------------------------------------------------------------
    # 6. A continuing state and a crossing event are not equivalent.
    # ------------------------------------------------------------------
    crossing = run_case(
        service=service,
        client=client,
        label="Cross instead of state",
        query=CROSS_INSTEAD_OF_STATE,
    )

    assert_source_in(
        crossing,
        {
            "generated",
            "cache",
        },
    )
    assert_validation_passed(crossing)
    assert_different_explorer(
        crossing,
        seed_explorer,
    )

    # ------------------------------------------------------------------
    # 7. AND and OR must not share the seed Explorer.
    # ------------------------------------------------------------------
    logical_or = run_case(
        service=service,
        client=client,
        label="OR instead of AND",
        query=OR_INSTEAD_OF_AND,
    )

    assert_source_in(
        logical_or,
        {
            "generated",
            "cache",
        },
    )
    assert_validation_passed(logical_or)
    assert_different_explorer(
        logical_or,
        seed_explorer,
    )

    print()
    print("=" * 80)
    print(
        "QUERY CACHE ACCEPTANCE TEST PASSED"
    )
    print("=" * 80)

    summary = {
        "seed": {
            "explorer": seed_explorer,
            "source": seed.response.source,
        },
        "identical": {
            "explorer": (
                exact.response.explorer
            ),
            "source": exact.response.source,
            "cache_match_type": (
                exact.cache_match_type
            ),
        },
        "normalized": {
            "explorer": (
                normalized.response.explorer
            ),
            "source": (
                normalized.response.source
            ),
            "cache_match_type": (
                normalized.cache_match_type
            ),
        },
        "semantic": {
            "explorer": (
                semantic.response.explorer
            ),
            "source": (
                semantic.response.source
            ),
            "cache_match_type": (
                semantic.cache_match_type
            ),
            "similarity": (
                semantic.log_metadata.get(
                    "similarity"
                )
            ),
            "equivalence_confidence": (
                semantic.log_metadata.get(
                    "equivalence_confidence"
                )
            ),
        },
        "different_threshold": {
            "explorer": (
                threshold.response.explorer
            ),
            "source": (
                threshold.response.source
            ),
        },
        "cross_instead_of_state": {
            "explorer": (
                crossing.response.explorer
            ),
            "source": (
                crossing.response.source
            ),
        },
        "or_instead_of_and": {
            "explorer": (
                logical_or.response.explorer
            ),
            "source": (
                logical_or.response.source
            ),
        },
    }

    print(
        json.dumps(
            summary,
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()