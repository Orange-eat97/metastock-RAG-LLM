---
canonical_id: pattern.dark_cloud_cover
title: 'Pattern: Dark Cloud Cover'
type: pattern
card_bucket: patterns
category: candlestick
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- darkcloud
aliases:
- text: 'Pattern: Dark Cloud Cover'
  type: synonym
  weight: 0.85
- text: Dark Cloud Cover
  type: exact
  weight: 1.0
- text: darkcloud candlestick
  type: synonym
  weight: 0.85
- text: bearish dark cloud cover
  type: synonym
  weight: 0.85
- text: dark cloud reversal
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
  canonical_id: pattern.dark_cloud_cover
  supports_explorer: true
  priority: 10
  properties:
    formula_role: candlestick
    supports_explorer: true
    source_path: patterns/dark_cloud_cover.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Dark Cloud Cover

## Intent

Detect the Dark Cloud Cover bearish candlestick pattern.

## Natural Language Triggers

- dark cloud cover
- darkcloud candlestick
- bearish dark cloud cover
- dark cloud reversal

## Required Logical Components

- Use `darkcloud()` for the Dark Cloud Cover function.
- Optionally combine with prior uptrend or resistance context.
- Load enough Explorer records for candlestick accuracy.

## Formula Building Blocks

```metastock
darkcloud()
darkcloud() AND C < Mov(C,20,S)
```

## Example Compositions

```metastock
darkcloud()
darkcloud() AND C < Mov(C,20,S)
```

## Default Assumptions

- Dark Cloud Cover is bearish by default.
- Candlestick functions return +1 when pattern is found.
- Explorer should load at least 10 records.

## Pitfalls

- Do not invent `darkcloudcover()`; use `darkcloud()`.
- Do not use it as bullish reversal.
- Do not forget Explorer load-record requirement.

## Related functions and concepts

- reference.candlestick_functions
- reference.candlestick_exploration_load_records
- function.mov

## Retrieval keywords

dark cloud cover, darkcloud candlestick, bearish dark cloud cover, dark cloud reversal, darkcloud.

## Test Queries

- Find dark cloud cover stocks
- Find bearish dark cloud cover reversal
