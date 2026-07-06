---
canonical_id: pattern.bearish_candlestick_reversal
title: 'Pattern: Bearish Candlestick Reversal'
type: pattern
card_bucket: patterns
category: candlestick
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- hangingman
- engulfingbear
- darkcloud
- eveningstar
- shootingstar
aliases:
- text: 'Pattern: Bearish Candlestick Reversal'
  type: synonym
  weight: 0.85
- text: Bearish Candlestick Reversal
  type: exact
  weight: 1.0
- text: hanging man or bearish engulfing
  type: synonym
  weight: 0.85
- text: dark cloud cover bearish reversal
  type: synonym
  weight: 0.85
- text: evening star reversal
  type: synonym
  weight: 0.85
- text: shooting star bearish scan
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
  canonical_id: pattern.bearish_candlestick_reversal
  supports_explorer: true
  priority: 10
  properties:
    formula_role: candlestick
    supports_explorer: true
    source_path: patterns/bearish_candlestick_reversal.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Bearish Candlestick Reversal

## Intent

Detect bearish Japanese candlestick reversal patterns using MetaStock candlestick functions.

## Natural Language Triggers

- bearish candlestick reversal
- hanging man or bearish engulfing
- dark cloud cover bearish reversal
- evening star reversal
- shooting star bearish scan

## Required Logical Components

- Choose one or more bearish candlestick functions.
- Combine alternatives with `OR`.
- Optionally add trend or resistance context.
- Use Explorer record-load pitfall card for accurate candlestick scans.

## Formula Building Blocks

```metastock
hangingman()
engulfingbear()
darkcloud()
eveningstar()
shootingstar()
hangingman() OR engulfingbear() OR darkcloud() OR eveningstar() OR shootingstar()
```

## Example Compositions

```metastock
hangingman() OR engulfingbear() OR darkcloud() OR eveningstar() OR shootingstar()
(engulfingbear() OR darkcloud()) AND C < Mov(C,50,S)
```

## Default Assumptions

- If no pattern is specified, use a small family of common bearish reversal functions.
- Candlestick functions return +1 when pattern is found and 0 otherwise.
- Load at least 10 records in Explorer options for candlestick scans.

## Pitfalls

- Do not use candlestick functions without enough loaded records.
- Do not treat candlestick pattern alone as a complete short strategy.
- Do not invent function names outside the candlestick reference card.

## Related functions and concepts

- reference.candlestick_functions
- reference.candlestick_exploration_load_records
- function.mov

## Retrieval keywords

bearish candlestick reversal, hanging man or bearish engulfing, dark cloud cover bearish reversal, evening star reversal, shooting star bearish scan, hangingman, engulfingbear, darkcloud, eveningstar, shootingstar.

## Test Queries

- Find bearish candlestick reversal stocks
- Find dark cloud cover bearish reversal
