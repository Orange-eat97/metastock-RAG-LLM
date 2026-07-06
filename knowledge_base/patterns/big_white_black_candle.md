---
canonical_id: pattern.big_white_black_candle
title: 'Pattern: Big White / Big Black Candle'
type: pattern
card_bucket: patterns
category: candlestick
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- bigwhite
- bigblack
aliases:
- text: 'Pattern: Big White / Big Black Candle'
  type: synonym
  weight: 0.85
- text: Big White / Big Black Candle
  type: exact
  weight: 1.0
- text: big white candle
  type: synonym
  weight: 0.85
- text: big black candle
  type: synonym
  weight: 0.85
- text: large bullish candle
  type: synonym
  weight: 0.85
- text: large bearish candle
  type: synonym
  weight: 0.85
- text: big candle scan
  type: synonym
  weight: 0.85
requires:
- canonical_id: reference.candlestick_functions
  rationale: This card usually needs reference.candlestick_functions for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
- canonical_id: reference.candlestick_exploration_load_records
  rationale: This card usually needs reference.candlestick_exploration_load_records for correct formula generation.
  priority: 10
  properties:
    source: registry_ready_transform
    formula_role: requires
suggests:
- canonical_id: pattern.volume_above_average
  rationale: pattern.volume_above_average is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
- canonical_id: function.mov
  rationale: function.mov is often useful context for this card but is not always mandatory.
  priority: 40
  properties:
    source: registry_ready_transform
    formula_role: suggests
semantic:
  concept_role: pattern
  mechanism: candlestick
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - candlestick
  required_components:
  - reference.candlestick_functions
  - reference.candlestick_exploration_load_records
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.big_white_black_candle
  supports_explorer: true
  priority: 10
  properties:
    formula_role: candlestick
    supports_explorer: true
    source_path: patterns/big_white_black_candle.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Big White / Big Black Candle

## Intent

Detect large bullish or bearish candle bodies using MetaStock `bigwhite()` and `bigblack()` candlestick functions.

## Natural Language Triggers

- big white candle
- big black candle
- large bullish candle
- large bearish candle
- big candle scan

## Required Logical Components

- Use `bigwhite()` for large bullish/white candle.
- Use `bigblack()` for large bearish/black candle.
- Use `OR` when user asks for either large candle.
- Optionally combine with volume confirmation.

## Formula Building Blocks

```metastock
bigwhite()
bigblack()
bigwhite() OR bigblack()
bigwhite() AND V > Mov(V,20,S)
```

## Example Compositions

```metastock
bigwhite()
bigblack()
bigwhite() AND V > Mov(V,20,S)
```

## Default Assumptions

- Direction defaults to user phrase: white/bullish = `bigwhite`, black/bearish = `bigblack`.
- Candlestick functions return +1/0.
- Volume confirmation uses existing volume-above-average pattern.

## Pitfalls

- Do not use `white()` for big white candle unless the user asks for any white body.
- Do not use `bigblack()` for bullish candle.
- Do not forget Explorer load-record requirement.

## Related functions and concepts

- reference.candlestick_functions
- reference.candlestick_exploration_load_records
- pattern.volume_above_average
- function.mov

## Retrieval keywords

big white candle, big black candle, large bullish candle, large bearish candle, big candle scan, bigwhite, bigblack.

## Test Queries

- Find big white candle with volume above average
- Find big black candle stocks
