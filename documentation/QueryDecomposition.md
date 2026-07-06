# Query Decomposition MVP Developer Documentation

**Project:** MetaStock RAG LLM  
**Milestone:** Step 2 — Query Decomposition  
**Status:** MVP-complete for query decomposition and retrieval planning  
**Date:** 2026-07-06

---

## 1. Purpose

This milestone makes query decomposition reliable enough for the MetaStock RAG LLM pipeline.

The module now takes a natural-language trading query and determines:

1. Which existing knowledge-card concepts are relevant.
2. Which requested concepts are missing from the current knowledge base.
3. Which accepted concepts should be expanded through the Supabase registry graph.
4. Which retrieval queries are safe to send into vector retrieval.
5. Which retrieval queries should be suppressed because they contain unsupported or missing concepts.

The problem being solved here is **retrieval planning**, not final formula generation.

Before this step, the system could silently map a missing concept to a nearby existing concept. Examples:

```text
"gap up"            -> pattern.breakout
"MACD crossover"    -> function.cross + function.mov
"ATR trailing stop" -> function.ref / function.mov / nearby cards
```

That behavior was dangerous because vector retrieval would pull semantically similar but technically wrong cards, giving the final LLM plausible but unsupported context.

The MVP objective is:

```text
Missing concept should not become nearest wrong card.
Missing concept should become a structured missing-card suggestion.
Existing support cards can still be retrieved safely.
```

---

## 2. Final Architecture

```text
User query
  -> LLM seed planner
  -> Registry validation
  -> Missing seed preservation
  -> Registry alias hints
  -> Runtime card-evidence coverage verification
  -> Accepted / rejected / support seed classification
  -> Registry dependency expansion
  -> Safe retrieval query grouping
  -> Context builder retrieves only safe dynamic context
```

In concrete implementation terms:

1. `query_decomposer.py` asks the LLM to propose canonical seed IDs.
2. Invalid seed IDs are no longer discarded silently. They are stored as `proposed_missing_seed_ids`.
3. `retrieval_planner.py` merges:
   - valid LLM seeds;
   - registry alias matches;
   - missing seed suggestions from the decomposer;
   - missing seed suggestions from the coverage verifier.
4. `seed_coverage_verifier.py` checks whether candidate seeds actually cover the user query using existing knowledge-card evidence.
5. `retrieval_planner.py` accepts only seeds that pass the coverage gate or are useful support concepts.
6. `retrieval_planner.py` suppresses unsafe retrieval queries that contain missing concepts.
7. `context_builder.py` force-includes registry-resolved cards and only runs vector retrieval using safe retrieval queries.

---

## 3. Files Involved

Main files changed or involved:

```text
src/queryDecomposition/query_decomposer.py
src/queryDecomposition/retrieval_planner.py
src/queryDecomposition/seed_coverage_verifier.py
src/queryDecomposition/registry_resolver.py
src/retrieval/context_builder.py
```

No new Supabase semantic-profile table is required for this step.

Earlier, a table named `rag_card_semantic_profiles` was considered, but the query decomposition MVP intentionally avoids requiring it. Instead, semantic coverage verification uses existing card evidence from:

```text
public.rag_card_registry
public.rag_cards
public.rag_card_aliases
public.rag_card_dependencies
```

---

## 4. Implemented Components

### 4.1 LLM Seed Planning

`query_decomposer.py` asks the LLM to map a user query to available registry canonical IDs.

The planner receives active concepts from Supabase, including:

```text
canonical_id
title
concept_type
card_bucket
source_path
aliases
```

The LLM returns retrieval intents containing:

```text
target_bucket
retrieval_query
seed_canonical_ids
reason
```

The decomposer does **not** expand dependencies. Dependency expansion stays inside the registry graph through `RegistryResolver`.

Example:

```text
User query:
Find stocks breaking below the previous 20 day low with volume above average

Expected seed concepts:
pattern.breakout
pattern.volume_above_average

Later dependency expansion:
function.llv
function.ref
function.mov
```

---

### 4.2 Missing Seed Detection

If the LLM proposes a canonical ID that is not in the active registry, the decomposer prints:

```text
suggest adding <seed_id> card
```

Examples:

```text
suggest adding pattern.gap_up card
suggest adding pattern.macd_crossover card
suggest adding function.atr card
```

The important patch is that these missing IDs are no longer only printed. They are now stored inside the retrieval intent as:

```python
proposed_missing_seed_ids
```

This makes missing concepts structured planner data, not just warning text.

---

### 4.3 Missing Concepts Become Retrieval Constraints

The largest design correction is this:

```text
Before:
missing concept -> warning line -> original query still used for vector retrieval

After:
missing concept -> structured missing suggestion -> unsafe retrieval query suppressed
```

This prevents cases like:

```text
Query:
Find stocks where MACD crosses above its signal line

Bad old behavior:
- print suggest adding pattern.macd_crossover card
- still retrieve with "MACD crosses above signal line"
- vector search finds nearest cards even though no MACD card exists

Correct new behavior:
- preserve pattern.macd_crossover as missing
- accept function.cross and function.mov as support cards
- suppress raw MACD retrieval query
- retrieve only with safe concept-based queries such as Cross and Mov
```

---

### 4.4 Alias Hints

`retrieval_planner.py` also queries registry aliases.

Known aliases such as these can add candidate seeds:

```text
crosses above
moving average
volume spike
```

Alias hints are useful, but they do not bypass coverage verification.

---

### 4.5 Runtime Card-Evidence Coverage Verification

`seed_coverage_verifier.py` introduces three coverage statuses:

```text
full_coverage
support_only
not_covered
```

Definitions:

| Status | Meaning |
|---|---|
| `full_coverage` | The card directly satisfies a requested trading concept. |
| `support_only` | The card is useful, but a core concept is still missing. |
| `not_covered` | The card is semantically nearby but does not cover the requested trading mechanism. |

The verifier uses existing card evidence loaded through `RegistryResolver`. It does not depend on a new semantic table.

`registry_resolver.py` builds runtime semantic evidence from:

```text
rag_card_registry.source_path
rag_cards.title
rag_cards.card_type
rag_cards.card_bucket
rag_cards.category
rag_cards.frontmatter
rag_cards.structured_json
rag_cards.plain_text
rag_cards.body_markdown
```

This gives the verifier enough evidence to decide whether a candidate seed actually covers the user query.

---

### 4.6 Safe Retrieval Query Grouping

`retrieval_planner.py` groups retrieval queries by bucket:

```text
patterns
functions
references
```

The key behavior is that it suppresses intent queries containing missing concept spans.

Example:

```text
Missing seed:
pattern.macd_crossover

Derived unsafe spans:
macd crossover
macd
crossover
```

So these raw queries are suppressed:

```text
MACD crosses above signal line
Find stocks where MACD crosses above its signal line
```

Instead, safe retrieval queries are generated from accepted existing concepts:

```text
Cross function functions cross Cross crosses above cross above crosses below cross below
Mov function functions mov Mov moving average simple moving average exponential moving average SMA
```

This avoids searching the vector database for unsupported concepts.

---

### 4.7 Context Builder No Longer Overrides the Planner

`context_builder.py` previously had this fallback behavior:

```python
if no planned query exists for a bucket:
    use the original user query
```

That defeated the planner. Even if the planner suppressed unsafe queries, the context builder could reintroduce them.

This was changed so that if a bucket has no safe planned queries, `context_builder.py` skips retrieval for that bucket.

The context builder now follows the planner instead of overriding it.

---

## 5. Key Behaviors Now Working

### 5.1 Gap Up With Volume Spike

Command:

```powershell
python -m src.generate_explorer "Find stocks that gap up with a volume spike" --dry-run
```

Expected behavior:

```text
suggest adding pattern.gap_up card
keep pattern.volume_above_average
keep function.mov through dependency expansion
do not use pattern.breakout as a substitute for gap up
```

This confirms that a missing price-gap pattern is not hidden by a nearby breakout card.

---

### 5.2 MACD Signal Cross

Command:

```powershell
python -m src.generate_explorer "Find stocks where MACD crosses above its signal line" --dry-run
```

Expected behavior:

```text
suggest adding pattern.macd_crossover card or function.macd card
keep function.cross as a support concept
keep function.mov as a support concept
suppress raw retrieval query containing MACD
```

Observed correct behavior:

```text
pattern.macd_crossover appears under proposed missing seed IDs
Missing-card suggestions include pattern.macd_crossover
Accepted seed canonical IDs include function.cross and function.mov
Retrieval queries by bucket do not contain the raw MACD query
Only safe function queries are sent to vector retrieval
```

This confirms that missing concepts are planner constraints, not warnings.

---

### 5.3 ATR Trailing Stop

Command:

```powershell
python -m src.generate_explorer "Find stocks where close is above a 2 ATR trailing stop" --dry-run
```

Expected behavior:

```text
suggest adding function.atr card
suggest adding pattern.atr_trailing_stop or pattern.trailing_stop card
keep reference.price_fields if selected
reject unrelated substitutions such as function.ref if coverage is not valid
suppress raw retrieval query containing ATR trailing stop
```

This confirms that missing technical indicators and missing strategy patterns are not replaced by nearby existing cards.

---

### 5.4 Fully Covered Complex Breakdown Query

Command:

```powershell
python -m src.generate_explorer "Find stocks breaking below the previous 20 day low with volume above average, RSI below 30, and close above the 200 day moving average" --dry-run
```

Expected resolved concepts:

```text
pattern.breakout
function.llv
function.ref
pattern.volume_above_average
function.mov
function.rsi
```

This query is fully covered by current cards and should not suggest new missing cards.

---

## 6. Current Acceptance Criteria

The query decomposition MVP is complete because it satisfies these criteria:

1. Natural language queries are decomposed into registry canonical seed IDs.
2. Missing canonical concepts are detected.
3. Missing concepts are preserved structurally inside the retrieval plan.
4. Existing support concepts can still be accepted.
5. Bad substitutions can be rejected or suppressed.
6. Missing concepts no longer drive vector retrieval.
7. Accepted seeds are expanded through the Supabase dependency graph.
8. Retrieval queries are bucketed into `patterns`, `functions`, and `references`.
9. `context_builder.py` obeys the retrieval plan and does not fall back to unsafe raw queries.
10. The system is testable with positive and negative decomposition cases.

This makes the module MVP-ready as a query decomposition and retrieval-planning component.

It does **not** mean the whole product is ready.

---

## 7. Known Limitations

### 7.1 Branch-Aware Dependency Expansion Not Yet Implemented

`pattern.breakout` is currently bidirectional. It covers both:

```text
break above previous high
break below previous low
```

The dependency graph may expand to both `HHV` and `LLV`.

Future improvement:

```text
above / high -> HHV + Ref
below / low  -> LLV + Ref
```

This belongs to branch-aware dependency filtering or reranking, not the core query decomposition MVP.

---

### 7.2 Coverage Verification Is Still Candidate-Based

The coverage verifier checks candidate seeds against the full user query.

In some cases, a support card may be classified too strongly. Example:

```text
function.cross may be marked full_coverage for a MACD cross because the Cross card contains a MACD example.
```

This is currently not damaging because the missing MACD concept is preserved and unsafe MACD retrieval is suppressed.

Future improvement:

```text
Use requirement/span-level coverage verification rather than only candidate-seed coverage verification.
```

---

### 7.3 No BM25 / Hybrid Search Yet

Dynamic retrieval is still primarily vector-based through the Supabase `match_rag_cards` RPC.

Future improvement:

```text
alias exact match
+ PostgreSQL full-text search / BM25-like ranking
+ vector search
+ metadata filtering
+ reranking
```

---

### 7.4 Knowledge Base Is Still Small

The system correctly suggests missing cards, but a production user-facing product needs more cards.

High-priority missing cards include:

```text
function.macd
function.atr
function.bollinger_bands
function.stochastic
function.obv
function.cci
function.vwap
pattern.gap_up
pattern.gap_down
pattern.bollinger_band_squeeze
pattern.atr_trailing_stop
pattern.bullish_engulfing
```

---

### 7.5 Generation and Runtime Validation Are Separate

This step only improves query decomposition and retrieval planning.

It does not solve:

```text
final formula correctness
MetaStock syntax validation
Explorer JSON validation
runtime testing inside MetaStock
repair loops
backtest or exploration execution feedback
```

---

## 8. Manual Test Commands

From the repository root:

```powershell
cd C:\GitHub\metastock-RAG-LLM
```

Set environment variables:

```powershell
$env:PYTHONPATH = "."
$env:SEED_PLANNER_MODEL = "gpt-4.1-mini"
$env:SEED_COVERAGE_MODEL = "gpt-4.1-mini"
```

Run dry-run tests:

```powershell
python -m src.generate_explorer "Find stocks that gap up with a volume spike" --dry-run
```

```powershell
python -m src.generate_explorer "Find stocks where MACD crosses above its signal line" --dry-run
```

```powershell
python -m src.generate_explorer "Find stocks where close is above a 2 ATR trailing stop" --dry-run
```

```powershell
python -m src.generate_explorer "Find stocks breaking below the previous 20 day low with volume above average, RSI below 30, and close still above the 200 day moving average" --dry-run
```

```powershell
python -m src.generate_explorer "Find stocks with a Bollinger Band squeeze breakout, volume above average, and MACD crossing above its signal line while price is above the 50 day moving average" --dry-run
```

---

## 9. Expected Test Interpretation

### Covered Concepts

For covered concepts, expected cards should resolve.

```text
volume above average       -> pattern.volume_above_average + function.mov
RSI below 30               -> function.rsi
close above moving average -> function.mov
break below previous low   -> pattern.breakout + function.llv + function.ref
```

### Missing Concepts

For missing concepts, expected suggestions should appear.

```text
gap up            -> suggest adding pattern.gap_up card
MACD crossover    -> suggest adding pattern.macd_crossover or function.macd card
ATR trailing stop -> suggest adding function.atr and pattern.atr_trailing_stop card
Bollinger squeeze -> suggest adding pattern.bollinger_band_squeeze or function.bollinger_bands card
```

### Unsafe Retrieval Suppression

Raw missing-concept queries should be suppressed.

The retrieval queries by bucket should not contain:

```text
MACD crosses above signal line
ATR trailing stop
Bollinger Band squeeze
```

unless those cards have been added to the registry.

---

## 10. Example Regression Test Cases

### 10.1 Fully Covered Query

```python
TestCase(
    name="complex fully covered breakdown volume RSI MA",
    query=(
        "Find stocks breaking below the previous 20 day low with volume above average, "
        "RSI below 30, and close still above the 200 day moving average"
    ),
    must_resolve={
        "pattern.breakout",
        "function.llv",
        "function.ref",
        "pattern.volume_above_average",
        "function.mov",
        "function.rsi",
    },
    should_suggest_missing_card=False,
)
```

### 10.2 Mixed Missing + Covered Query

```python
TestCase(
    name="mixed missing Bollinger MACD with covered breakout volume MA",
    query=(
        "Find stocks with a Bollinger Band squeeze breakout, volume above average, "
        "and MACD crossing above its signal line while price is above the 50 day moving average"
    ),
    must_resolve={
        "pattern.breakout",
        "pattern.volume_above_average",
        "function.mov",
        "function.cross",
    },
    should_suggest_missing_card=True,
    suggestion_tokens_any=("bollinger", "macd"),
)
```

---

## 11. Final Status

```text
Step 2: Query Decomposition is MVP-complete.
```

The module now handles:

```text
seed extraction
registry validation
missing-card suggestion
missing-concept preservation
semantic coverage gating
safe retrieval-query construction
dependency expansion through the registry graph
context-builder integration
```

Recommended next project steps:

1. Add more high-priority knowledge cards.
2. Implement branch-aware dependency filtering.
3. Start Step 3: multi-index / routed retrieval.
4. Start Step 4: hybrid search / BM25.
5. Start Step 5: reranking.

For the current milestone, no further query decomposition changes are required unless new regression cases appear.
