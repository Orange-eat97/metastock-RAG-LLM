---
canonical_id: pattern.bullish_candlestick_reversal
title: 'Pattern: Bullish Candlestick Reversal'
type: pattern
card_bucket: patterns
category: candlestick
source: MetaStock Formula Primer / Formula Primer II / internal project pattern
status: active
priority: 10
supports_explorer: true
functions:
- hammer
- engulfingbull
- morningstar
- piercingline
- bullharami
aliases:
- text: 'Pattern: Bullish Candlestick Reversal'
  type: synonym
  weight: 0.85
- text: Bullish Candlestick Reversal
  type: exact
  weight: 1.0
- text: hammer or bullish engulfing
  type: synonym
  weight: 0.85
- text: morning star reversal
  type: synonym
  weight: 0.85
- text: piercing line bullish reversal
  type: synonym
  weight: 0.85
- text: bullish candlestick scan
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
  canonical_id: pattern.bullish_candlestick_reversal
  supports_explorer: true
  priority: 10
  properties:
    formula_role: candlestick
    supports_explorer: true
    source_path: patterns/bullish_candlestick_reversal.md
    generated_schema_version: registry_ready_v2
---

# Pattern: Bullish Candlestick Reversal

## Intent

Detect bullish Japanese candlestick reversal patterns using MetaStock candlestick functions.

## Natural Language Triggers

- bullish candlestick reversal
- hammer or bullish engulfing
- morning star reversal
- piercing line bullish reversal
- bullish candlestick scan

## Required Logical Components

- Choose one or more bullish candlestick functions.
- Combine alternatives with `OR`.
- Optionally add trend or support context.
- Use Explorer record-load pitfall card for accurate candlestick scans.

## Formula Building Blocks

```metastock
hammer()
engulfingbull()
morningstar()
piercingline()
bullharami()
hammer() OR engulfingbull() OR morningstar() OR piercingline()
```

## Example Compositions

```metastock
hammer() OR engulfingbull() OR morningstar() OR piercingline()
(hammer() OR engulfingbull()) AND C > Mov(C,50,S)
```

## Default Assumptions

- If no pattern is specified, use a small family of common bullish reversal functions.
- Candlestick functions return +1 when pattern is found and 0 otherwise.
- Load at least 10 records in Explorer options for candlestick scans.

## Pitfalls

- Do not use candlestick functions without enough loaded records.
- Do not treat candlestick pattern alone as trend confirmation.
- Do not invent function names outside the candlestick reference card.

## Related functions and concepts

- reference.candlestick_functions
- reference.candlestick_exploration_load_records
- function.mov

## Retrieval keywords

bullish candlestick reversal, hammer or bullish engulfing, morning star reversal, piercing line bullish reversal, bullish candlestick scan, hammer, engulfingbull, morningstar, piercingline, bullharami.

## Test Queries

- Find bullish candlestick reversal stocks
- Find hammer or bullish engulfing pattern
