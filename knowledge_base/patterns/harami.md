---
canonical_id: pattern.harami
title: 'Pattern: Harami Candlestick Pattern'
type: pattern
card_bucket: patterns
category: candlestick
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- bullharami
- bearharami
aliases:
- text: 'Pattern: Harami Candlestick Pattern'
  type: synonym
  weight: 0.85
- text: Harami Candlestick Pattern
  type: exact
  weight: 1.0
- text: bullish harami
  type: synonym
  weight: 0.85
- text: bearish harami
  type: synonym
  weight: 0.85
- text: harami reversal scan
  type: synonym
  weight: 0.85
- text: find harami stocks
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
  required_components:
  - reference.candlestick_functions
  - reference.candlestick_exploration_load_records
  does_not_cover:
  - unrelated_pattern_substitution
  - guaranteed_trade_profitability
registry:
  enabled: true
  canonical_id: pattern.harami
  supports_explorer: true
  priority: 10
  properties:
    formula_role: candlestick
    supports_explorer: true
    source_path: patterns/harami.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Harami Candlestick Pattern

## Intent

Detect bullish or bearish harami candlestick patterns.

## Natural Language Triggers

- harami candlestick pattern
- bullish harami
- bearish harami
- harami reversal scan
- find harami stocks

## Required Logical Components

- Choose bullish, bearish, or either harami direction.
- Use `bullharami()` for bullish harami.
- Use `bearharami()` for bearish harami.
- Use `OR` when user asks for either harami.

## Formula Building Blocks

```metastock
bullharami()
bearharami()
bullharami() OR bearharami()
```

## Example Compositions

```metastock
bullharami()
bearharami()
bullharami() OR bearharami()
```

## Default Assumptions

- If direction is unspecified, return either bullish or bearish harami.
- Candlestick functions return +1/0.
- Explorer should load at least 10 records.

## Pitfalls

- Do not confuse harami with harami cross.
- Do not use broad alias `reversal` alone.
- Do not forget Explorer load-record requirement.

## Related functions and concepts

- reference.candlestick_functions
- reference.candlestick_exploration_load_records

## Retrieval keywords

harami candlestick pattern, bullish harami, bearish harami, harami reversal scan, find harami stocks, bullharami, bearharami.

## Test Queries

- Find bullish harami stocks
- Find any harami candlestick pattern
