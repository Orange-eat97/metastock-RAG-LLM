---
canonical_id: reference.candlestick_functions
title: Candlestick Reversal Function Reference
type: reference
card_bucket: references
category: candlestick_reference
source: generated_curated_from_primer
status: active
priority: 10
supports_explorer: true
aliases:
- text: candlestick functions
  type: exact
  weight: 1.0
- text: candlestick reversal functions
  type: exact
  weight: 1.0
- text: Japanese candlestick patterns
  type: phrase
  weight: 0.9
- text: bullish candlestick reversal
  type: phrase
  weight: 0.9
- text: bearish candlestick reversal
  type: phrase
  weight: 0.9
suggests:
- canonical_id: reference.candlestick_exploration_load_records
  rationale: Candlestick Explorer scans need sufficient loaded records.
  priority: 30
  properties:
    formula_role: load_records_rule
semantic:
  concept_role: reference
  mechanism: candlestick_reference
  market_object: formula_environment
  outputs:
  - generation_rule
  - validation_rule
  supports_conditions:
  - environment_validation
  - syntax_validation
  does_not_cover:
  - specific_trading_signal_by_itself
registry:
  enabled: true
  canonical_id: reference.candlestick_functions
  supports_explorer: true
  priority: 10
  properties:
    formula_role: candlestick_reference
    source_path: references/candlestick_functions.md
    curation_level: upgraded_to_curated_quality
---

# Candlestick Reversal Function Reference

## Purpose

This card explains how MetaStock candlestick functions should be used in Explorer generation. Candlestick functions generally return `1` when the pattern is found and `0` otherwise. Pattern interpretation is subjective, and MetaStock relies on predefined rules.

## Rules

- Use the specific candlestick function name; do not invent generic names.
- Candlestick functions can be used directly as Explorer filters because non-zero means true.
- When using candlestick functions in explorations, load enough records; the Primer warns that at least 10 records should be loaded for candlestick explorations.
- Treat candlestick interpretation as a pattern hint, not a complete strategy by itself.
- Combine candlestick functions with trend, support/resistance, volume, or momentum filters when the user asks for confirmation.

## Examples

```metastock
BullHarami()
BearHarami()
DarkCloud()
BigWhite()
BigBlack()
BullHarami() AND C > Mov(C,50,S)
```

## What Not To Do

- Bad: `CandlestickBullishReversal()` invented function.
- Bad: assuming every bullish candlestick is a complete buy signal.
- Bad: running candlestick exploration with too few loaded records.
- Bad: using broad alias `candle` as exact retrieval alias.

## Validation checklist

- Function names are known candlestick functions.
- Explorer filter compares function result to true/non-zero or uses it directly.
- If generated as a standalone signal, assumptions say it is a pattern scan only.
- If in Explorer, user is reminded to load sufficient records.

## Related functions and concepts

- pattern.bullish_candlestick_reversal
- pattern.bearish_candlestick_reversal
- reference.candlestick_exploration_load_records



## Test Queries

- Find bullish candlestick reversals
- Find bearish harami patterns with trend confirmation
