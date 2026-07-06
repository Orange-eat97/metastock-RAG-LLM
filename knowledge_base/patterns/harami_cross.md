---
canonical_id: pattern.harami_cross
title: 'Pattern: Harami Cross Candlestick Pattern'
type: pattern
card_bucket: patterns
category: candlestick
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- bullharamicross
- bearharamicross
aliases:
- text: 'Pattern: Harami Cross Candlestick Pattern'
  type: phrase
  weight: 0.9
- text: Harami Cross Candlestick Pattern
  type: exact
  weight: 1.0
- text: harami cross candlestick
  type: phrase
  weight: 0.9
- text: bullish harami cross
  type: phrase
  weight: 0.9
- text: bearish harami cross
  type: phrase
  weight: 0.9
- text: find harami cross stocks
  type: phrase
  weight: 0.9
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
semantic:
  concept_role: pattern
  mechanism: candlestick
  market_object: price
  directions_supported:
  - bullish
  - bearish
  operations_supported:
  - candlestick
  - crossover_detection
  required_components:
  - reference.candlestick_functions
  - reference.candlestick_exploration_load_records
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.harami_cross
  supports_explorer: true
  priority: 10
  properties:
    formula_role: candlestick
    supports_explorer: true
    source_path: patterns/harami_cross.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Harami Cross Candlestick Pattern

## Intent

Detect bullish or bearish harami cross candlestick patterns.

## Natural Language Triggers

- harami cross candlestick
- bullish harami cross
- bearish harami cross
- find harami cross stocks

## Required Logical Components

- Choose bullish, bearish, or either harami cross direction.
- Use `bullharamicross()` for bullish harami cross.
- Use `bearharamicross()` for bearish harami cross.
- Use `OR` when direction is unspecified.

## Formula Building Blocks

```metastock
bullharamicross()
bearharamicross()
bullharamicross() OR bearharamicross()
```

## Example Compositions

```metastock
bullharamicross()
bearharamicross()
bullharamicross() OR bearharamicross()
```

## Default Assumptions

- If direction is unspecified, return either bullish or bearish harami cross.
- Candlestick functions return +1/0.
- Explorer should load at least 10 records.

## Pitfalls

- Do not confuse harami cross with ordinary harami.
- Do not omit parentheses.
- Do not forget Explorer load-record requirement.

## Related functions and concepts

- reference.candlestick_functions
- reference.candlestick_exploration_load_records

## Retrieval keywords

harami cross candlestick, bullish harami cross, bearish harami cross, find harami cross stocks, bullharamicross, bearharamicross.

## Test Queries

- Find bullish harami cross stocks
- Find any harami cross candlestick pattern
